"""
guider_adapter.py — Subprocess execution engine for Guider MCP integration.

Handles:
- Command whitelist enforcement
- Secure argument construction (no shell=True)
- Per-command timeout with SIGTERM→SIGKILL cleanup
- MCP server lifecycle cleanup (atexit + signal handlers)
- Output truncation for large responses
- tracefs semaphore (max 1 concurrent)
"""

from __future__ import annotations

import atexit
import json
import logging
import os
import re
import shlex
import shutil
import signal
import subprocess
import threading
import time
from typing import Any

from guider_catalog import BLOCKED_COMMANDS, BLOCKED_OPTS, CATALOG, get_catalog_entry

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_OUTPUT_BYTES: int = 500 * 1024          # 500 KB — truncate beyond this
MAX_CONCURRENT_CALLS: int = 3               # global concurrency limit
_TRACEFS_SEM = threading.Semaphore(1)       # only 1 tracefs command at a time
_CALL_SEM = threading.Semaphore(MAX_CONCURRENT_CALLS)

# Regex patterns for path safety validation
_SAFE_DEVICE_ID = re.compile(r'^[a-zA-Z0-9:._-]+$')
_SAFE_IFACE = re.compile(r'^[a-zA-Z0-9_.-]{1,16}$')

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# GuiderAdapter
# ---------------------------------------------------------------------------
class GuiderAdapter:
    """
    Execute guider commands securely via subprocess.

    Usage::

        adapter = GuiderAdapter()
        result = adapter.run("ttop", duration=3)
        # result["ok"] is True/False
        # result["data"] contains parsed JSON or text
    """

    # Default on-device paths (override via env vars in .mcp.json)
    _ANDROID_GUIDER_PATH: str = os.environ.get(
        "ANDROID_GUIDER_PATH", "/data/local/tmp/guider/guider.py"
    )
    _ANDROID_PYTHON_PATH: str = os.environ.get(
        "ANDROID_PYTHON_PATH",
        "/data/local/tmp/python3.13.11_android_aarch64/usr/bin/python3",
    )
    _ANDROID_PYTHON_LIB: str = os.environ.get(
        "ANDROID_PYTHON_LIB",
        "/data/local/tmp/python3.13.11_android_aarch64/usr/lib",
    )

    def __init__(
        self,
        guider_path: str | None = None,
        python_bin: str | None = None,
    ) -> None:
        # Resolve guider.py location
        self._guider_path = guider_path or self._find_guider()
        self._python_bin = python_bin or shutil.which("python3") or "python3"
        # Track live subprocess PIDs for cleanup
        self._active_procs: set[int] = set()
        self._lock = threading.Lock()

        # Register cleanup handlers once
        atexit.register(self.kill_all)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        command: str,
        *,
        duration: int | None = None,
        interval: int = 1,
        extra_opts: list[str] | None = None,
        input_file: str | None = None,
        target_pid: str | None = None,
        device_id: str | None = None,
        timeout_sec: int | None = None,
        json_output: bool = True,
        main_arg: str | None = None,
    ) -> dict[str, Any]:
        """
        Run a guider command and return a structured result envelope.

        Args:
            command:      guider sub-command name (e.g. "ttop", "bpftop")
            duration:     seconds to run (overrides catalog default_duration)
            interval:     sampling interval in seconds (-i N)
            extra_opts:   list of extra -q KEY[:VALUE] strings
            input_file:   -I <file> for offline analysis commands
            target_pid:   -e <pid/name> for per-process targeting
            device_id:    Android device serial (validated)
            timeout_sec:  wall-clock timeout; defaults to duration+30
            json_output:  append -J flag for JSON output
            main_arg:     positional argument after command (e.g. function name for bpftop)

        Returns:
            dict with keys: ok, command, timestamp, duration_sec,
                            data, truncated, warnings, error
        """
        ts_start = time.monotonic()
        envelope: dict[str, Any] = {
            "ok": False,
            "command": command,
            "timestamp": time.time(),
            "duration_sec": 0.0,
            "data": None,
            "truncated": False,
            "warnings": [],
            "error": None,
        }

        # --- security checks ---
        if command in BLOCKED_COMMANDS:
            envelope["error"] = f"command '{command}' is not permitted"
            return envelope

        meta = get_catalog_entry(command)
        if meta is None:
            envelope["error"] = f"unknown command '{command}'"
            return envelope

        # validate extra_opts
        warnings: list[str] = []
        safe_opts = self._filter_opts(extra_opts or [], warnings)
        envelope["warnings"] = warnings

        # early pre-flight checks (saves subprocess startup + gives clear errors)
        if meta.get("requires_root") and os.getuid() != 0:
            envelope["error"] = (
                f"command '{command}' requires root or CAP_BPF"
                + (f" (kernel >= {meta['min_kernel']})" if meta.get("min_kernel") else "")
                + ". Re-run the MCP server with sudo."
            )
            return envelope

        if meta.get("android_only") and not device_id:
            warnings.append(
                f"command '{command}' requires an Android device — "
                "pass device_id='<serial>' (adb devices to list)"
            )

        # validate device_id
        if device_id and not _SAFE_DEVICE_ID.match(device_id):
            envelope["error"] = f"invalid device_id '{device_id}'"
            return envelope

        # validate input_file path (must exist, realpath check)
        if input_file:
            real_input = os.path.realpath(input_file)
            if not os.path.exists(real_input):
                envelope["error"] = f"input_file not found: {input_file}"
                return envelope
            input_file = real_input

        # determine duration
        run_duration: int | None = None
        if meta["streaming"]:
            if duration is not None:
                run_duration = max(1, int(duration))
            elif meta.get("default_duration"):
                run_duration = int(meta["default_duration"].rstrip("s"))
            else:
                run_duration = 5

        # timeout = duration + 30s buffer
        if timeout_sec is None:
            timeout_sec = (run_duration or 0) + 30

        # --- build command list ---
        cmd = self._build_cmd(
            command=command,
            meta=meta,
            duration=run_duration,
            interval=interval,
            extra_opts=safe_opts,
            input_file=input_file,
            target_pid=target_pid,
            device_id=device_id,
            json_output=json_output,
            main_arg=main_arg,
        )
        logger.debug("exec: %s", " ".join(cmd))

        # --- acquire semaphores ---
        if not _CALL_SEM.acquire(timeout=5):
            envelope["error"] = "too many concurrent guider calls (max 3)"
            return envelope

        tracefs_held = False
        if meta.get("semaphore"):
            sem_timeout = (run_duration or 0) + 5
            tracefs_held = _TRACEFS_SEM.acquire(timeout=sem_timeout)
            if not tracefs_held:
                _CALL_SEM.release()
                envelope["error"] = "tracefs busy — another ftrace command is running"
                return envelope

        # --- execute ---
        try:
            out, err, rc = self._exec(cmd, timeout_sec)
            elapsed = time.monotonic() - ts_start
            envelope["duration_sec"] = round(elapsed, 3)

            raw = out.decode("utf-8", errors="replace")

            # truncation check
            if len(out) > MAX_OUTPUT_BYTES:
                raw = out[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
                envelope["truncated"] = True

            # parse JSON
            if json_output and meta["output_type"] == "json":
                # guider emits one JSON object per sampling interval (concatenated,
                # no separator). Use raw_decode to collect all objects; return the last.
                objects = self._parse_json_stream(raw)
                if objects:
                    envelope["data"] = objects  # always a list; len=1 for single-interval
                    envelope["ok"] = True
                elif envelope.get("truncated"):
                    # Output cut at 500 KB — JSON boundary lost; return raw text
                    # so the LLM can still see partial data instead of a failure.
                    envelope["data"] = raw
                    envelope["ok"] = True
                else:
                    envelope["error"] = "no JSON output" if rc == 0 else f"exit code {rc}"
                    envelope["data"] = raw
            else:
                # Strip ANSI escape codes from text output so LLMs see clean text
                envelope["data"] = GuiderAdapter._ANSI_ESCAPE.sub('', raw)
                envelope["ok"] = rc == 0 or bool(raw.strip())

            if err:
                stderr_text = err.decode("utf-8", errors="replace").strip()
                if stderr_text:
                    # Filter known-harmless terminal probe lines (stty on non-tty stdin)
                    filtered = "\n".join(
                        line for line in stderr_text.splitlines()
                        if "stty:" not in line
                    ).strip()
                    if filtered:
                        filtered = GuiderAdapter._ANSI_ESCAPE.sub('', filtered)
                        envelope["warnings"].append(f"stderr: {filtered[:500]}")

        except Exception as exc:  # pylint: disable=broad-except
            envelope["error"] = str(exc)
            envelope["duration_sec"] = round(time.monotonic() - ts_start, 3)
        finally:
            if tracefs_held:
                _TRACEFS_SEM.release()
            _CALL_SEM.release()

        return envelope

    def kill_all(self) -> None:
        """Terminate all tracked subprocesses (called on MCP server exit)."""
        with self._lock:
            pids = list(self._active_procs)
        for pid in pids:
            self._kill_pgid(pid)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_guider(self) -> str:
        """Locate guider.py relative to this file or on PATH."""
        # Same directory or parent guider/
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(here, "..", "guider", "guider.py"),
            os.path.join(here, "..", "guider.py"),
            os.path.join(here, "guider.py"),
        ]
        for c in candidates:
            real = os.path.realpath(c)
            if os.path.isfile(real):
                return real
        # fallback: assume guider on PATH
        found = shutil.which("guider")
        if found:
            return found
        raise FileNotFoundError(
            "guider.py not found. Set GUIDER_PATH env or pass guider_path="
        )

    def _build_cmd(
        self,
        *,
        command: str,
        meta: dict,
        duration: int | None,
        interval: int,
        extra_opts: list[str],
        input_file: str | None,
        target_pid: str | None,
        device_id: str | None,
        json_output: bool,
        main_arg: str | None = None,
    ) -> list[str]:
        """Construct the subprocess argument list.

        For android_only commands with a device_id, the command is executed
        on-device via ``adb -s <device_id> shell env LD_LIBRARY_PATH=... python3 guider.py``
        instead of running guider.py on the host machine.
        """
        # Bug-0b: visualize/file commands use a positional FILE arg, not -I FILE.
        # Auto-promote input_file to main_arg when the command takes a file
        # as positional argument and no explicit main_arg was given.
        if meta.get("output_type") == "file" and input_file and not main_arg:
            main_arg = input_file
            input_file = None

        if meta.get("android_only") and device_id:
            # Only add -J when the command actually produces JSON output;
            # text/file output_type commands silently drop output when -J is passed.
            effective_json = json_output and meta.get("output_type") == "json"
            return self._build_adb_cmd(
                command=command,
                duration=duration,
                interval=interval,
                extra_opts=extra_opts,
                target_pid=target_pid,
                device_id=device_id,
                json_output=effective_json,
                main_arg=main_arg,
                streaming=meta.get("streaming", False),
            )

        is_py = self._guider_path.endswith(".py")
        if is_py:
            cmd: list[str] = [self._python_bin, self._guider_path, command]
        else:
            cmd = [self._guider_path, command]

        # positional main argument (e.g. function name for bpftop/bpfsnoop)
        if main_arg:
            cmd.append(main_arg)

        # Bug-0a: -i (interval) is interpreted as an input file path by guider
        # for non-streaming commands — only add it for live streaming commands.
        if meta.get("streaming"):
            cmd += ["-i", str(interval)]

        # duration (-R Ns) for streaming commands
        if duration is not None:
            cmd += ["-R", f"{duration}s"]

        # input file
        if input_file:
            cmd += ["-I", input_file]

        # target pid/name
        if target_pid:
            cmd += ["-e", str(target_pid)]

        # android device (for non-android_only commands that still use -d)
        if device_id:
            cmd += ["-d", device_id]

        # extra -q options (already sanitised)
        for opt in extra_opts:
            cmd += ["-q", opt]

        # JSON output flag
        if json_output:
            cmd += ["-J"]

        return cmd

    def _build_adb_cmd(
        self,
        *,
        command: str,
        duration: int | None,
        interval: int,
        extra_opts: list[str],
        target_pid: str | None,
        device_id: str,
        json_output: bool,
        main_arg: str | None,
        streaming: bool = True,
    ) -> list[str]:
        """Build an adb-shell command that runs guider on the Android device."""
        adb = shutil.which("adb") or "adb"
        cmd: list[str] = [adb, "-s", device_id, "shell"]

        # guider invocation on the device: env LD_LIBRARY_PATH=... python3 guider.py CMD
        guider_args: list[str] = []
        if self._ANDROID_PYTHON_LIB:
            guider_args += ["env", f"LD_LIBRARY_PATH={self._ANDROID_PYTHON_LIB}"]
        guider_args += [self._ANDROID_PYTHON_PATH, self._ANDROID_GUIDER_PATH, command]

        if main_arg:
            guider_args.append(main_arg)

        # Bug-0a: only add -i for streaming/live commands
        if streaming:
            guider_args += ["-i", str(interval)]

        if duration is not None:
            guider_args += ["-R", f"{duration}s"]

        if target_pid:
            guider_args += ["-e", str(target_pid)]

        for opt in extra_opts:
            guider_args += ["-q", opt]

        if json_output:
            guider_args.append("-J")

        # Bug-2: use shlex.join so options with spaces (e.g. "FILTER:my app")
        # are properly quoted when passed through the adb shell.
        cmd.append(shlex.join(guider_args))
        return cmd

    def _filter_opts(self, opts: list[str], warnings: list[str]) -> list[str]:
        """Remove blocked -q options and validate FILE/PATH values."""
        safe: list[str] = []
        for opt in opts:
            key = opt.split(":")[0].upper()
            if key in BLOCKED_OPTS:
                warnings.append(f"blocked option: {opt}")
                continue
            # Check FILE/PATH/DIR values for path traversal
            if any(t in key for t in ("FILE", "PATH", "DIR")):
                value_part = opt[len(key) + 1:] if ":" in opt else ""
                if value_part:
                    real = os.path.realpath(value_part)
                    # Allow /tmp/guider_mcp_* and readable existing paths
                    if not (real.startswith("/tmp/") or os.path.exists(real)):
                        warnings.append(f"path not accessible: {opt}")
                        continue
            safe.append(opt)
        return safe

    def _exec(
        self, cmd: list[str], timeout_sec: int
    ) -> tuple[bytes, bytes, int]:
        """Run subprocess with timeout and cleanup."""
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,   # own process group → clean kill
        )
        with self._lock:
            self._active_procs.add(proc.pid)
        try:
            out, err = proc.communicate(timeout=timeout_sec)
            return out, err, proc.returncode
        except subprocess.TimeoutExpired:
            logger.warning("guider command timed out: %s", cmd[2] if len(cmd) > 2 else cmd)
            self._kill_pgid(proc.pid)
            # drain remaining output
            try:
                out, err = proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                out, err = b"", b""
            return out, err, -signal.SIGTERM
        finally:
            with self._lock:
                self._active_procs.discard(proc.pid)

    @staticmethod
    def _kill_pgid(pid: int) -> None:
        """Send SIGTERM then SIGKILL to the process group.

        Polls up to 2 s in 0.1 s increments so fast-exiting processes are
        reaped immediately rather than always waiting the full 2 s.
        """
        try:
            pgid = os.getpgid(pid)
            os.killpg(pgid, signal.SIGTERM)
            # Poll for up to 2s (20 × 0.1s) before escalating to SIGKILL
            for _ in range(20):
                time.sleep(0.1)
                try:
                    os.killpg(pgid, 0)  # signal 0: check existence only
                except ProcessLookupError:
                    return  # process group already gone
            # Still alive → SIGKILL
            try:
                os.killpg(pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        except (ProcessLookupError, PermissionError, OSError):
            pass

    def _signal_handler(self, signum: int, _frame: Any) -> None:
        """Handle SIGTERM/SIGINT by cleaning up children then exiting."""
        self.kill_all()
        raise SystemExit(0)

    # Compiled regex for stripping ANSI escape codes and terminal control chars
    _ANSI_ESCAPE = re.compile(r'\x1b(?:\[[0-9;]*[A-Za-z]|\(B|[=><])|[\x00-\x08\x0b-\x1f\x7f]')

    @staticmethod
    def _parse_json_stream(text: str) -> list:
        """
        Parse a stream of concatenated JSON objects from guider output.

        guider prints one pretty-printed JSON object per sampling interval with
        no separator between them, optionally preceded by INFO/WARN lines and
        ANSI terminal escape sequences.
        Uses json.JSONDecoder.raw_decode() to collect all top-level objects.
        Returns a list (may be empty if no valid JSON found).
        """
        # Strip ANSI escape codes and non-printable control chars (keep \t \n \r)
        text = GuiderAdapter._ANSI_ESCAPE.sub('', text)

        decoder = json.JSONDecoder()
        objects: list = []
        idx = 0
        n = len(text)
        # find first JSON start character
        while idx < n and text[idx] not in ('{', '['):
            idx += 1
        while idx < n:
            try:
                obj, end = decoder.raw_decode(text, idx)
                objects.append(obj)
                idx = end
                # skip whitespace between objects
                while idx < n and text[idx] in ' \t\n\r':
                    idx += 1
            except json.JSONDecodeError:
                # skip past current position to find next JSON start character
                idx += 1
                while idx < n and text[idx] not in ('{', '['):
                    idx += 1
        return objects


# ---------------------------------------------------------------------------
# Module-level singleton (for MCP server reuse)
# ---------------------------------------------------------------------------
_default_adapter: GuiderAdapter | None = None


def get_adapter(guider_path: str | None = None) -> GuiderAdapter:
    """Return (or create) the module-level GuiderAdapter singleton."""
    global _default_adapter
    if _default_adapter is None:
        path = guider_path or os.environ.get("GUIDER_PATH")
        _default_adapter = GuiderAdapter(guider_path=path)
    return _default_adapter
