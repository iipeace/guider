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
MAX_DURATION_SEC: int = 300                 # matches openapi/guider-rest.py's Field(ge=1, le=300)
MAX_EXTRA_OPTS_COUNT: int = 50              # fail fast on a runaway/hallucinated opts list
MAX_EXTRA_OPT_LEN: int = 4096               # per-item length cap, same rationale
_TRACEFS_SEM = threading.Semaphore(1)       # only 1 tracefs command at a time
_CALL_SEM = threading.Semaphore(MAX_CONCURRENT_CALLS)

# Regex patterns for path safety validation
_SAFE_DEVICE_ID = re.compile(r'^[a-zA-Z0-9:._-]+$')
_SAFE_IFACE = re.compile(r'^[a-zA-Z0-9_.-]{1,16}$')

# Path markers/suffixes that always indicate a credential file — blocked from
# input_file/FILE:/PATH:/DIR: values regardless of the /tmp or existence checks,
# since guider's format-agnostic file-reading commands (print/less/printtrace)
# echo file contents verbatim into the MCP/REST response.
_SENSITIVE_PATH_MARKERS = (
    "/etc/shadow", "/etc/gshadow", "/etc/sudoers",
    "/.ssh/", "/.gnupg/", "/.aws/", "/.kube/", "/.docker/config.json",
    # /var/run is a symlink to /run on virtually every distro and
    # realpath() resolves it, so this also catches Kubernetes service
    # account tokens under the mounted secrets path
    "/run/secrets/", "/.config/gcloud/", "/.azure/",
)
_SENSITIVE_PATH_SUFFIXES = (
    ".pem", "_rsa", "_dsa", "_ecdsa", "_ed25519",
    # .netrc/.git-credentials (plaintext creds), .key (TLS private-key
    # naming convention missed by the SSH-style suffixes above), .jks/
    # .keystore (Java KeyStore, common on the JVM services guider
    # diagnoses — Kafka/Elasticsearch/Tomcat/etc.)
    ".netrc", ".git-credentials", ".key", ".jks", ".keystore",
)

# Commands whose main_arg is a file/directory path (comma-separated for
# merge/mkcache/dirdiff) rather than a numeric/target value (e.g. cputest's
# "250", memtest's "1G") — these bypass input_file's validation entirely
# since main_arg is appended to argv unchecked, so they get the same
# _is_sensitive_path() denylist applied explicitly in run().
_MAIN_ARG_PATH_COMMANDS = {
    "comp", "decomp", "merge", "split", "mkcache", "dirdiff",
    "retrace", "printdir", "printext", "elftree", "addr2sym", "sym2addr",
    "topdiff", "topsum", "sync", "readahead", "flush",
    # android_only, but _build_cmd() only routes to the adb-shell path
    # when device_id is actually supplied — omit it and this runs
    # LOCALLY, with main_arg (out_path) reaching AndroidMgr.doBugRecord()'s
    # os.path.join(main_arg, filename) unvalidated. bugrec shares the
    # exact same doBugRecord() sink (dump=False vs dump=True is the only
    # difference).
    "bugrep", "bugrec",
    # These have no main_arg_desc in the catalog, so validate_path_coverage() cannot flag them. print/less/
    # strings echo the file verbatim and convert renders it into an SVG embedding the text, yet the denylist was
    # only wired to input_file, not to their real calling convention (main_arg). readelf/readdex/readapk/convlog
    # have the same gap with a narrower blast radius; printdlt/logdlt/dlttop take comma-separated file lists.
    "print", "less", "strings", "convert", "readelf", "readdex", "readapk",
    "convlog", "printdlt", "logdlt", "dlttop",
    # every draw-mode command shares SysMgr.setVisualAttr() (path =
    # sys.argv[2] i.e. main_arg), which is passed unchecked to
    # TaskAnalyzer.getInitTime() -> open(fname, "rb"). The dedicated
    # visualize() MCP tool forces a validated input_file for most of
    # these, but the generic runCommand tool has no per-command
    # restriction and forwards main_arg verbatim for any of them.
    "draw", "drawavg", "drawbitmap", "drawconn", "drawcpu", "drawcpuavg",
    "drawdelay", "drawdiff", "drawdisk", "drawflame", "drawflamediff",
    "drawhist", "drawio", "drawleak", "drawmem", "drawmemavg", "drawnet",
    "drawpri", "drawpsi", "drawreq", "drawrss", "drawrssavg", "drawscatter",
    "drawstack", "drawtime", "drawviolin", "drawvss", "drawvssavg",
}

# Commands whose main_arg embeds a path alongside a non-path field via a
# colon (e.g. iotest's "read:/tmp/testfile") rather than being (or
# comma-listing) the path(s) outright — comma-splitting the raw main_arg
# would realpath() the whole "OP:PATH" string as one bogus relative
# filename and miss the embedded path entirely, so each needs its own
# extractor pulling out just the path segment before the _is_sensitive_path()
# check. Falls back to the whole string when the expected colon is absent.
def _extract_iotest_path(arg):
    # guider.py's doIoTest() splits on ":" with no limit: len==1 means the
    # whole string is the path (op defaults to "read"); len==2 is
    # "OP:PATH"; len==3 is "OP:PATH:SIZE" — path is index 1 in both of the
    # latter cases, not "everything after the first colon" (a naive
    # split(":",1)[1] would leave a trailing ":SIZE" glued onto the path
    # for the 3-field form, defeating _is_sensitive_path()'s suffix checks
    # e.g. "...id_ed25519:1M" no longer ends in "_ed25519").
    parts = arg.split(":")
    if len(parts) == 1:
        return parts[0]
    if len(parts) in (2, 3):
        return parts[1]
    return arg  # malformed - guider.py's own parser will reject it anyway


_MAIN_ARG_COLON_PATH_EXTRACTORS = {
    "iotest": _extract_iotest_path,                                 # "OP:PATH" or "OP:PATH:SIZE"
    # guider.py's doFadviseCmd() splits on ":" up to 4 fields and always
    # takes index 0 as the path ("FILE:ADVICE{:POS:SIZE}"), never the last
    # field — rsplit(":",1)[0] would only work for the bare 2-field form;
    # for "FILE:ADVICE:POS:SIZE" it leaves ":POS" glued onto the path,
    # defeating the suffix check.
    "fadvise": lambda arg: arg.split(":", 1)[0],                     # "FILE:ADVICE{:POS:SIZE}"
    "watch": lambda arg: arg.split(":", 1)[0],                           # "PATH:EVENT:FILE:CMD"
    "fetop": lambda arg: arg.split(":", 1)[0],
}

# Commands whose target/target_pid (-g) is a raw filesystem path rather than a PID/COMM when main_arg is
# absent (doWatch, doSync, doFlush fall back to -g). Checked unconditionally: non-path values never match
# _is_sensitive_path()'s markers.
_TARGET_PID_PATH_COMMANDS = {"watch", "fetop", "sync", "flush"}

# iotest/fadvise's doIoTest()/doFadvise() have the identical
# "elif SysMgr.filterGroup:" fallback as sync/watch above, but unlike
# sync's plain-path fallback, theirs reuses the EXACT SAME colon-compound
# format as their main_arg ("OP:PATH[:SIZE]" / "FILE:ADVICE{:POS:SIZE}"),
# leaving -g as a complete bypass of both the colon-extraction AND the
# sensitive-path check (iotest's write: op is a real O_TRUNC overwrite
# primitive). Reuses the same extractor functions from
# _MAIN_ARG_COLON_PATH_EXTRACTORS rather than duplicating the OP:PATH
# parsing logic.
_TARGET_PID_COLON_EXTRACTOR_COMMANDS = {"iotest", "fadvise"}

# For these, input_file (-I) is not read: SysMgr.createWatchList() (via the shared runTaskTop() loop) splits
# it on commas and execs each item. A path denylist cannot make an exec target safe, so input_file is
# rejected outright; normal monitoring does not use it. (bgtop shares the bug but is not cataloged.)
_INPUT_FILE_SPAWNS_PROCESS_COMMANDS = {
    "top", "ttop", "atop", "wtop", "ctop", "ntop", "rtop", "ptop",
    "mtop", "disktop", "stacktop", "contop", "ftop", "trtop",
}

# SysMgr.doTrace() (these 12 commands) treats main_arg as a command to launch and trace
# (parseCommand -> execvpe in a forked child) for every mode except remote/hook/bind. That is documented
# guider behavior, but the catalog declares no main_arg_desc for them, so runCommand would forward an
# arbitrary command line (no root needed for most). Attach to an existing process with target_pid (-g).
_MAIN_ARG_SPAWNS_PROCESS_COMMANDS = {
    "utop", "pytop", "utrace", "btrace", "strace", "pytrace", "sigtrace",
    "stat", "mtrace", "btop", "systop", "kstop",
    # DbusMgr.runDbusSnooper() has the same shape: without target_pid and outside the read-only list modes
    # (getpidlist/getunitlist/getunitstat) it executes main_arg verbatim. printsdinfo/printsdunit are only exempt
    # when jsonEnable is set, so json_output=False reopens it for those two.
    "printdbus", "printdbusintro", "printdbusstat", "printdbussub",
    "printsdinfo", "printsdunit",
}

# req's main_arg format is "METHOD#..." with #-delimited
# sub-fields undocumented in the catalog's abbreviated main_arg_desc —
# DATAFILE:/JSONFILE:/FILE:name:path open a local file and send its bytes
# as the request body/attachment, and @@@FILE:<path>@@@ inlines a local
# file's bytes anywhere inside a DATA:/JSONDATA: value — an arbitrary
# local-file-read-and-exfiltrate-to-attacker-URL primitive. "FILE:" alone
# covers DATAFILE:/JSONFILE:/@@@FILE: as substrings; @@@BIN:<size>@@@ is
# checked separately since it doesn't contain "FILE:".
_REQ_DANGEROUS_MARKERS = ("FILE:", "@@@BIN:")

# -q option keys whose value is a filesystem path but whose name contains
# none of "FILE"/"PATH"/"DIR", so they'd otherwise evade _filter_opts()'s
# substring heuristic entirely. RALIST in particular is opened for writing
# (FileAnalyzer.makeReadaheadFile), not just read.
_EXTRA_PATH_OPT_KEYS = {
    "RALIST", "RAADDLIST", "RAALLOWLIST", "RADENYLIST",
    # TaskAnalyzer.drawFlame() uses these verbatim as a write destination
    # (SysMgr.writeFile(samplePath, ...)) when given an explicit value
    # (not the bare "SET" form) — same unvalidated-write pattern as
    # RALIST above, reachable from drawflame/drawflamediff and any other
    # command whose internal flamegraph path calls drawFlame().
    "SAVESAMPLE", "SAVESAMPLEJSON",
    # perfetto/hprof's doPerfetto() casts this verbatim as the directory
    # to save a downloaded profiling binary into (same unvalidated-write-
    # target pattern as RALIST/SAVESAMPLE above) — lower severity since
    # the download URL itself is a hardcoded Google CDN link, but the
    # destination directory is fully caller-controlled.
    "AUTODOWNLOAD",
}

# guider's -F image output format values (drawSubStr help block)
_SAFE_DRAW_FORMAT = {"svg", "png", "pdf", "ps", "eps", "html"}

# andcmd's sub_command is a positional main_arg, not a "-q KEY:VALUE"
# option, so it is invisible to BLOCKED_OPTS/_filter_opts() below, and
# "andcmd" itself is a normal cataloged command so BLOCKED_COMMANDS never
# sees it either. guider.py's AndroidMgr.checkAndCmd() accepts ANY value
# in ConfigMgr.ANDCMDLIST (50+ entries), most of which are state-mutating
# (INSTALLPKG, GRANTPERM/REVOKEPERM, BROADCAST, CLEARDATA, SETSETTINGS,
# ...) — restrict this adapter to the read-only diagnostic subset the
# andcmd catalog entry actually documents (guider_catalog.py's
# "main_arg_desc" for andcmd)
_ANDCMD_ALLOWED_SUBCOMMANDS = {
    "GETSELINUX",
    "GETPKGLIST",
    "GETPROCLIST",
    "GETBINDERSTATS",
    "GETAPPSTAT",
    "GETPKGATTR",
}

# sperf is android_only, but omitting device_id makes _build_cmd() run it
# LOCALLY instead of via adb-shell. main_arg here is not a path —
# AndroidMgr.doSimplePerf() treats it as a COMMAND to execute
# (`simpleperf record ... <main_arg>` via SysMgr.executeCmdSync()), so no
# path denylist can make this safe. The only correct fix is refusing the
# local-execution fallback entirely.
#
# hprof/perfetto share doPerfetto(), which has the identical
# no-isAndroid-guard/main_arg-executed-via-createCmdProcess() shape as
# sperf's doSimplePerf(). mdtop also dispatches to doPerfetto()
# (heapProf=True) and shares the same gap.
_REQUIRES_DEVICE_ID_COMMANDS = {"sperf", "hprof", "perfetto", "mdtop"}

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
        input_files: list[str] | None = None,
        target_pid: str | None = None,
        device_id: str | None = None,
        timeout_sec: int | None = None,
        json_output: bool = True,
        main_arg: str | None = None,
        draw_format: str | None = None,
        draw_layout: str | None = None,
        top_number: int | None = None,
        output_dir: str | None = None,
    ) -> dict[str, Any]:
        """
        Run a guider command and return a structured result envelope.

        Args:
            command:      guider sub-command name (e.g. "ttop", "bpftop")
            duration:     seconds to run (overrides catalog default_duration)
            interval:     sampling interval in seconds (-i N)
            extra_opts:   list of extra -q KEY[:VALUE] strings
            input_file:   -I <file> for offline analysis commands
            input_files:  positional multi-file input for drawavg-family commands
                          (e.g. drawavg/drawcpuavg/drawmemavg/drawvssavg/drawrssavg,
                          which require >= 2 files); mutually exclusive with input_file
            target_pid:   -g <pid/name> for per-process targeting
            device_id:    Android device serial (validated)
            timeout_sec:  wall-clock timeout; defaults to duration+30
            json_output:  append -J flag for JSON output
            main_arg:     positional argument after command (e.g. function name for bpftop)
            draw_format:  -F <fmt> image output format (svg/png/pdf/ps/eps/html)
            draw_layout:  -L <RES:PER> graph layout spec for draw commands
            top_number:   -T <N> top-N number for draw commands
            output_dir:   -o <dir> output directory for draw commands

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
            envelope["error"] = f"unknown command '{command}'. Use guiderHelp to list."
            return envelope

        # andcmd's sub-command is a positional arg, so it bypasses BLOCKED_OPTS; enforce its allowlist here.
        # Normalize like AndroidMgr.checkAndCmd() (split on ':', then upper()). checkAndCmd() comma-splits main_arg
        # and runs every item, so check each one or "GETSELINUX:1,GRANTPERM:..." slips through.
        if command == "andcmd":
            if not (main_arg or "").strip():
                envelope["error"] = "andcmd requires a sub-command in main_arg"
                return envelope
            for _sub in main_arg.split(","):
                sub_key = _sub.split(":", 1)[0].strip().upper()
                if sub_key and sub_key not in _ANDCMD_ALLOWED_SUBCOMMANDS:
                    envelope["error"] = (
                        f"andcmd sub-command '{_sub.strip()}' is not "
                        f"permitted (allowed: "
                        f"{sorted(_ANDCMD_ALLOWED_SUBCOMMANDS)})"
                    )
                    return envelope

        # commands that MUST run device-side — omitting device_id doesn't
        # just skip a nicety, it silently falls through to local host
        # execution (see _REQUIRES_DEVICE_ID_COMMANDS comment above)
        if command in _REQUIRES_DEVICE_ID_COMMANDS and not device_id:
            envelope["error"] = (
                f"command '{command}' requires device_id — refusing to run "
                "locally, since its main_arg is executed as a host command"
            )
            return envelope

        # reject a runaway/hallucinated extra_opts list before doing any
        # per-item work (stat() calls in _filter_opts, then argv assembly)
        if extra_opts:
            if len(extra_opts) > MAX_EXTRA_OPTS_COUNT:
                envelope["error"] = (
                    f"too many extra_opts ({len(extra_opts)} > {MAX_EXTRA_OPTS_COUNT})"
                )
                return envelope
            oversized = next((o for o in extra_opts if len(o) > MAX_EXTRA_OPT_LEN), None)
            if oversized is not None:
                envelope["error"] = (
                    f"an extra_opts entry exceeds the {MAX_EXTRA_OPT_LEN}-byte limit"
                )
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

        # reject input_file outright for commands that spawn it as a
        # process rather than reading it — see
        # _INPUT_FILE_SPAWNS_PROCESS_COMMANDS comment above; the ordinary
        # existence/sensitive-path checks below assume a READ threat model
        # that doesn't apply here at all
        if input_file and command in _INPUT_FILE_SPAWNS_PROCESS_COMMANDS:
            envelope["error"] = (
                f"command '{command}' does not accept input_file — it "
                "spawns input_file's value as a process rather than "
                "reading it"
            )
            return envelope

        # validate input_file path (must exist, realpath check)
        if input_file:
            real_input = self._check_input_exists(input_file)
            if real_input is None:
                envelope["error"] = f"input_file not found: {input_file}"
                return envelope
            input_file = real_input

        # validate input_files paths (must exist, realpath check each; fail closed)
        if input_files:
            real_inputs: list[str] = []
            for f in input_files:
                real_f = self._check_input_exists(f)
                if real_f is None:
                    envelope["error"] = f"input_files entry not found: {f}"
                    return envelope
                real_inputs.append(real_f)
            input_files = real_inputs

        # reject main_arg outright for commands that spawn it as a new
        # process to trace rather than treating it as a target selector —
        # see _MAIN_ARG_SPAWNS_PROCESS_COMMANDS comment above; no path
        # denylist can make an arbitrary-exec target safe, so main_arg is
        # rejected outright here (use target_pid to attach to an existing
        # process instead)
        if main_arg and command in _MAIN_ARG_SPAWNS_PROCESS_COMMANDS:
            envelope["error"] = (
                f"command '{command}' does not accept main_arg — it "
                "spawns main_arg's value as a new process to trace rather "
                "than treating it as a target. Use target_pid to attach "
                "to an existing process instead."
            )
            return envelope

        # validate main_arg for commands where it's a file/directory path
        # (comma-separated for merge/mkcache/dirdiff/etc.) — unlike input_file,
        # main_arg is appended to argv unchecked in _build_common_args(),
        # so it would otherwise bypass _is_sensitive_path() entirely.
        if main_arg and command in _MAIN_ARG_PATH_COMMANDS:
            for part in main_arg.split(","):
                part = part.strip()
                if not part:
                    continue
                if self._is_sensitive_path(os.path.realpath(part)):
                    envelope["error"] = f"main_arg path is blocked for security reasons: {part}"
                    return envelope

        # For commands whose main_arg embeds a path next to a non-path field via a colon (iotest/fadvise/watch/
        # fetop), extract only the path segment first; realpath() on the raw "OP:PATH" would resolve a bogus relative
        # name. guider's parsers comma-split main_arg and process every item, so check each one.
        if main_arg and command in _MAIN_ARG_COLON_PATH_EXTRACTORS:
            extractor = _MAIN_ARG_COLON_PATH_EXTRACTORS[command]
            for _item in main_arg.split(","):
                _item = _item.strip()
                if not _item:
                    continue
                candidate = extractor(_item).strip()
                if candidate and self._is_sensitive_path(os.path.realpath(candidate)):
                    envelope["error"] = f"main_arg path is blocked for security reasons: {candidate}"
                    return envelope

        # watch/fetop's main_arg format is "PATH:EVENT:FILE:CMD" — a
        # non-empty CMD field is executed verbatim (execvp, no shell, but
        # full command control) by SysMgr.runFileCmd() whenever the watched
        # path/event/file matches. There's no way to sanitize an arbitrary
        # command string, so the CMD field itself is rejected outright
        # rather than validated — plain path/glob main_args (no colons, or
        # fewer than 4 fields) are untouched. Checked per comma-separated
        # item (matching guider.py's own per-item processing) rather than
        # a merged whole-string colon count, since the latter's safety
        # against a bypass is coincidental rather than structural.
        if main_arg and command in ("watch", "fetop"):
            for _item in main_arg.split(","):
                parts = _item.split(":", 3)
                if len(parts) == 4 and parts[3].strip():
                    envelope["error"] = (
                        f"command '{command}' does not allow a CMD field in "
                        "main_arg (PATH:EVENT:FILE:CMD) — arbitrary command "
                        "execution risk"
                    )
                    return envelope

        # req's main_arg can embed a local-file-read-and-exfiltrate marker
        # (DATAFILE:/JSONFILE:/FILE:name:path/@@@FILE:...@@@/@@@BIN:...@@@)
        # undocumented in the catalog — see _REQ_DANGEROUS_MARKERS comment
        # above. Like watch/fetop's CMD field, there's no safe way to
        # sanitize an embedded local-file reference, so the markers are
        # rejected outright; ordinary req usage (plain URL, DATA:/JSONDATA:
        # with literal values) is unaffected.
        if main_arg and command == "req":
            upper_arg = main_arg.upper()
            if any(marker in upper_arg for marker in _REQ_DANGEROUS_MARKERS):
                envelope["error"] = (
                    "req's main_arg may not embed a local file reference "
                    "(DATAFILE:/JSONFILE:/FILE:/@@@FILE:.../@@@BIN:...) — "
                    "arbitrary file read + exfiltration risk"
                )
                return envelope

        # validate target_pid for commands that fall back to -g as a raw
        # filesystem path when main_arg is absent (doWatch, backing
        # watch/fetop) — unlike target_pid's usual PID/COMM meaning
        # elsewhere, this never went through any path check.
        if target_pid and command in _TARGET_PID_PATH_COMMANDS:
            for part in target_pid.split(","):
                part = part.strip()
                if not part:
                    continue
                if self._is_sensitive_path(os.path.realpath(part)):
                    envelope["error"] = f"target path is blocked for security reasons: {part}"
                    return envelope

        # validate target_pid for iotest/fadvise's -g fallback, which reuses
        # the exact same colon-compound format as their main_arg (see
        # _TARGET_PID_COLON_EXTRACTOR_COMMANDS comment above) — reuses the
        # same extractor functions and comma-split loop already applied to
        # main_arg above.
        if target_pid and command in _TARGET_PID_COLON_EXTRACTOR_COMMANDS:
            extractor = _MAIN_ARG_COLON_PATH_EXTRACTORS[command]
            for _item in target_pid.split(","):
                _item = _item.strip()
                if not _item:
                    continue
                candidate = extractor(_item).strip()
                if candidate and self._is_sensitive_path(os.path.realpath(candidate)):
                    envelope["error"] = f"target path is blocked for security reasons: {candidate}"
                    return envelope

        # validate draw_format against guider's supported -F values
        if draw_format and draw_format.lower() not in _SAFE_DRAW_FORMAT:
            envelope["error"] = (
                f"invalid draw_format '{draw_format}' "
                f"(allowed: {sorted(_SAFE_DRAW_FORMAT)})"
            )
            return envelope

        # validate output_dir (same allow-list as FILE/PATH/DIR -q values:
        # /tmp/ or an already-existing path)
        if output_dir:
            real_out = os.path.realpath(output_dir)
            if not self._is_accessible_path(output_dir):
                envelope["error"] = f"output_dir not accessible: {output_dir}"
                return envelope
            if real_out.startswith("/tmp/") and not os.path.exists(real_out):
                try:
                    os.makedirs(real_out, exist_ok=True)
                except OSError as exc:
                    envelope["error"] = (
                        f"failed to create output_dir '{output_dir}': {exc}"
                    )
                    return envelope
            output_dir = real_out

        # determine duration
        run_duration: int | None = None
        if meta["streaming"]:
            if duration is not None:
                run_duration = min(MAX_DURATION_SEC, max(1, int(duration)))
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
            input_files=input_files,
            target_pid=target_pid,
            device_id=device_id,
            json_output=json_output,
            main_arg=main_arg,
            draw_format=draw_format,
            draw_layout=draw_layout,
            top_number=top_number,
            output_dir=output_dir,
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
                    # Filter known-harmless lines:
                    # - stty probe output on non-tty stdin
                    # - guider's generic "please report guider.err" notice,
                    #   which its Tee-wrapper emits with an "[ERROR]" prefix
                    #   on the FIRST stderr write of the process regardless
                    #   of cause (e.g. a harmless MatplotlibDeprecationWarning),
                    #   so its mere presence doesn't indicate real failure
                    filtered = "\n".join(
                        line for line in stderr_text.splitlines()
                        if "stty:" not in line
                        and "guider/issues" not in line
                    ).strip()
                    if filtered:
                        filtered = GuiderAdapter._ANSI_ESCAPE.sub('', filtered)
                        envelope["warnings"].append(f"stderr: {filtered[:500]}")
                        # guider's own printErr() writes fatal errors to stderr
                        # with an "[ERROR]" prefix but most call paths still
                        # exit 0 (SysMgr.doExit defaults exitCode to 0) — treat
                        # that as a real failure instead of a silent success.
                        if envelope["ok"] and "[ERROR]" in filtered:
                            envelope["ok"] = False
                            envelope["error"] = filtered[:500]

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
        input_files: list[str] | None = None,
        draw_format: str | None = None,
        draw_layout: str | None = None,
        top_number: int | None = None,
        output_dir: str | None = None,
    ) -> list[str]:
        """Construct the subprocess argument list.

        For android_only commands with a device_id, the command is executed
        on-device via ``adb -s <device_id> shell env LD_LIBRARY_PATH=... python3 guider.py``
        instead of running guider.py on the host machine.
        """
        # Bug-0b: visualize/file commands use a positional FILE arg, not -I FILE.
        # Auto-promote input_file to main_arg when the command takes a file
        # as positional argument and no explicit main_arg was given.
        if (
            meta.get("output_type") == "file"
            and input_file
            and not main_arg
            and not input_files
        ):
            main_arg = input_file
            input_file = None

        # only add -J when the command actually produces JSON output;
        # text/file output_type commands silently drop output when -J is
        # passed. The LOCAL execution branch (taken whenever device_id is
        # absent, including for android_only text/file commands like
        # bugrep/scrcap/andcmd/logand/watchprop/getprop that aren't in
        # _REQUIRES_DEVICE_ID_COMMANDS) must apply the same filtering as
        # the adb-shell branch, or a caller relying on run()'s
        # json_output=True default gets -J silently appended to a command
        # that can't honor it, and an empty response with no error back.
        # Computed once here so both branches apply it identically.
        effective_json = json_output and meta.get("output_type") == "json"

        if meta.get("android_only") and device_id:
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

        cmd += self._build_common_args(
            streaming=meta.get("streaming", False),
            interval=interval,
            duration=duration,
            main_arg=main_arg,
            input_files=input_files,
            input_file=input_file,
            target_pid=target_pid,
            device_id=device_id,
            draw_format=draw_format,
            draw_layout=draw_layout,
            top_number=top_number,
            output_dir=output_dir,
            extra_opts=extra_opts,
            json_output=effective_json,
        )

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

        guider_args += self._build_common_args(
            streaming=streaming,
            interval=interval,
            duration=duration,
            main_arg=main_arg,
            input_files=None,
            input_file=None,
            target_pid=target_pid,
            device_id=None,
            draw_format=None,
            draw_layout=None,
            top_number=None,
            output_dir=None,
            extra_opts=extra_opts,
            json_output=json_output,
        )

        # Bug-2: use shlex.join so options with spaces (e.g. "FILTER:my app")
        # are properly quoted when passed through the adb shell.
        cmd.append(shlex.join(guider_args))
        return cmd

    @staticmethod
    def _build_common_args(
        *,
        streaming: bool,
        interval: int,
        duration: int | None,
        main_arg: str | None,
        input_files: list[str] | None,
        input_file: str | None,
        target_pid: str | None,
        device_id: str | None,
        draw_format: str | None,
        draw_layout: str | None,
        top_number: int | None,
        output_dir: str | None,
        extra_opts: list[str],
        json_output: bool,
    ) -> list[str]:
        """Build the guider CLI argument list shared by host and adb execution.

        Callers prepend their own process-launch prefix (``[python3, guider.py,
        CMD]`` for host execution, or the ``env ... python3 guider.py CMD``
        prefix for adb execution) and pass ``None``/empty values for any
        argument their call site doesn't support, so the result matches
        exactly what each original inline implementation produced.
        """
        args: list[str] = []

        # positional multi-file input (drawavg-family: >= 2 files, no -I/comma-join)
        if input_files:
            args += input_files
        # positional main argument (e.g. function name for bpftop/bpfsnoop)
        elif main_arg:
            args.append(main_arg)

        # Bug-0a: -i (interval) is interpreted as an input file path by guider
        # for non-streaming commands — only add it for live streaming commands.
        if streaming:
            args += ["-i", str(interval)]

        # duration (-R Ns) for streaming commands
        if duration is not None:
            args += ["-R", f"{duration}s"]

        if input_file:
            args += ["-I", input_file]

        # target pid/name (guider's task-filter flag is -g, not -e;
        # -e is "enable options", an unrelated per-command flag-character string)
        if target_pid:
            args += ["-g", str(target_pid)]

        # android device (for non-android_only commands that still use -d)
        if device_id:
            args += ["-d", device_id]

        # draw command options (guider's own -d "disable options" char-flag string
        # is unrelated to the adapter's Android-device-serial -d above)
        if draw_format:
            args += ["-F", draw_format]
        if draw_layout:
            args += ["-L", draw_layout]
        if top_number is not None:
            args += ["-T", str(top_number)]
        if output_dir:
            args += ["-o", output_dir]

        # Force-disable ElfAnalyzer's on-disk pickle cache for every MCP/REST invocation. loadObject() pickle.load()s
        # a path derived predictably from the analyzed file's path, and cacheDirPath falls back to world-writable /tmp
        # when the default cannot be written (the supported unprivileged mode for readelf/elftree/addr2sym/sym2addr/
        # mkcache), so a local user can pre-plant a payload. -q NOELFCACHE makes loadObject() return before the load.
        # The mitigation forces a safe option on (plain use reaches the path, so there is nothing to block); the
        # only cost is cross-process cache reuse, and each call is a fresh subprocess anyway.
        extra_opts = list(extra_opts) if extra_opts else []
        if not any(
            opt.split(":", 1)[0].strip().upper() == "NOELFCACHE"
            for opt in extra_opts
        ):
            extra_opts.append("NOELFCACHE")

        # extra -q options (already sanitised). guider.py's own SysMgr.parseOption()
        # rejects a SECOND occurrence of the same flag letter as "redundant use", so
        # multiple settings must be passed as ONE -q flag with comma-separated
        # KEY:VALUE items (SysMgr.parseEnvironVars -> UtilMgr.splitString). Escape
        # literal commas in values so they survive splitString's "\," unescape.
        if extra_opts:
            args += ["-q", ",".join(opt.replace(",", r"\,") for opt in extra_opts)]

        if json_output:
            args += ["-J"]

        return args

    @staticmethod
    def _is_sensitive_path(real: str) -> bool:
        """True if a resolved path points at a well-known credential file.

        guider's format-agnostic file-reading commands (print/less/printtrace)
        echo file contents verbatim into the MCP/REST response, so these are
        blocked regardless of the /tmp or existence checks below. This is a
        denylist (not a sandbox) — it preserves guider's core ability to read
        arbitrary host logs/procfs/dumps for diagnostics while blocking the
        highest-value credential paths.
        """
        # os.path.realpath() preserves trailing whitespace verbatim
        # (unlike leading whitespace, which turns the path relative) — a
        # trailing space would defeat the suffix .endswith() check below
        # without this. Doesn't affect the marker check (already a
        # substring match, immune to trailing whitespace either way).
        real = real.rstrip()

        # Directory markers (e.g. "/.ssh/") only match as substrings of a
        # FILE path inside them (".../.ssh/id_rsa"); a bare directory path
        # (".../.ssh", no trailing slash) needs one appended first so
        # dirdiff-style directory-only main_args are caught too.
        real_for_match = real if real.endswith("/") else real + "/"
        if any(marker in real_for_match for marker in _SENSITIVE_PATH_MARKERS):
            return True
        return real.endswith(_SENSITIVE_PATH_SUFFIXES)

    @staticmethod
    def _is_accessible_path(path: str) -> bool:
        """Allow a path if it resolves under /tmp/ or already exists on disk.

        Shared predicate for output_dir validation and FILE/PATH/DIR -q option
        values. realpath is used (not abspath) so symlinks are resolved before
        the /tmp/ prefix check and existence check, matching the original
        behavior of both call sites.
        """
        real = os.path.realpath(path)
        if GuiderAdapter._is_sensitive_path(real):
            return False
        return real.startswith("/tmp/") or os.path.exists(real)

    @staticmethod
    def _check_input_exists(path: str) -> str | None:
        """Resolve path and return it if it exists on disk, else None."""
        real = os.path.realpath(path)
        if GuiderAdapter._is_sensitive_path(real):
            return None
        return real if os.path.exists(real) else None

    def _filter_opts(self, opts: list[str], warnings: list[str]) -> list[str]:
        """Remove blocked -q options and validate FILE/PATH values."""
        safe: list[str] = []
        for opt in opts:
            # strip BEFORE key/value extraction — guider.py's own parser
            # (UtilMgr.splitString()) strips each comma-split item, so
            # " TCPDUMP:SET" becomes key "TCPDUMP" once it reaches
            # guider.py; without this strip() here key would be
            # " TCPDUMP" (leading space intact), which never matches
            # BLOCKED_OPTS — a single leading space would defeat every
            # entry in that set at once.
            opt = opt.strip()
            key = opt.split(":")[0].upper()
            if key in BLOCKED_OPTS:
                warnings.append(f"blocked option: {opt}")
                continue
            # Check FILE/PATH/DIR values for path traversal (plus a few
            # known path-bearing keys whose name doesn't contain those
            # substrings — see _EXTRA_PATH_OPT_KEYS)
            if any(t in key for t in ("FILE", "PATH", "DIR")) or key in _EXTRA_PATH_OPT_KEYS:
                value_part = opt[len(key) + 1:] if ":" in opt else ""
                if value_part:
                    # Allow paths under /tmp/ or that already exist on disk
                    if not self._is_accessible_path(value_part):
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


_PATH_LOOKING_DESC = re.compile(r"\b(path|file|dir|directory)\b", re.IGNORECASE)


def validate_path_coverage() -> list[str]:
    """Warn (non-blocking) about CATALOG commands whose main_arg_desc looks
    path-shaped but aren't covered by any main_arg/target_pid validation set.

    A permanent, startup-time regression check for the gap class covered
    by _MAIN_ARG_PATH_COMMANDS/_MAIN_ARG_COLON_PATH_EXTRACTORS/
    _TARGET_PID_PATH_COMMANDS above — same style/severity (warning, not a
    hard failure) as the existing validate_catalog()/
    validate_openai_function_defs() checks it runs alongside. A false
    positive here costs a log line, not a broken server.
    """
    covered = (
        _MAIN_ARG_PATH_COMMANDS
        | set(_MAIN_ARG_COLON_PATH_EXTRACTORS)
        | _TARGET_PID_PATH_COMMANDS
    )
    issues: list[str] = []
    for cmd, meta in CATALOG.items():
        desc = meta.get("main_arg_desc") or ""
        if desc and _PATH_LOOKING_DESC.search(desc) and cmd not in covered:
            issues.append(
                f"'{cmd}' main_arg_desc looks path-shaped ({desc!r}) but isn't "
                "in _MAIN_ARG_PATH_COMMANDS/_MAIN_ARG_COLON_PATH_EXTRACTORS/"
                "_TARGET_PID_PATH_COMMANDS"
            )
    return issues
