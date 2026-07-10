#!/usr/bin/env python3
"""
guider-mcp.py — MCP server exposing Guider performance analysis tools.

10 MCP tools (camelCase):
  systemMonitor   bpfTrace       ftraceProfile   networkTrace
  androidPerf     memoryAnalyze  visualize       logAnalyze
  runCommand      guiderHelp

Start:
    python3 guider-mcp.py
or via .mcp.json stdio transport (Claude Code picks this up automatically).
"""

from __future__ import annotations

import os
import sys
import logging
from typing import Any

# ---------------------------------------------------------------------------
# Ensure catalog/adapter are importable from the same directory
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from guider_adapter import get_adapter
from guider_catalog import CATALOG, BLOCKED_COMMANDS, get_tool_commands

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "ERROR: 'mcp' package not found.\n"
        "Install with:  pip install fastmcp\n"
        "or:            pip install mcp",
        file=sys.stderr,
    )
    sys.exit(1)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("guider-mcp")

# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "guider",
    description=(
        "Guider Linux/Android performance analysis toolkit. "
        "10 tools covering system monitoring, BPF tracing, ftrace profiling, "
        "network tracing, Android performance, memory analysis, visualization, "
        "log analysis, generic command execution, and built-in help."
    ),
)

adapter = get_adapter()


# ---------------------------------------------------------------------------
# Helper: build result summary for the LLM
# ---------------------------------------------------------------------------
def _wrap(result: dict[str, Any]) -> str:
    """Serialise the adapter envelope to a compact string for the LLM."""
    import json
    if result.get("truncated"):
        result.setdefault("warnings", []).insert(0, "output truncated to 500 KB")
    return json.dumps(result, ensure_ascii=False, default=str)


# ---------------------------------------------------------------------------
# 1. systemMonitor
# ---------------------------------------------------------------------------
@mcp.tool()
def systemMonitor(
    command: str,
    duration: int = 5,
    interval: int = 1,
    target: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    System-wide resource monitoring (CPU, memory, IO, threads, containers, etc.).

    Commands: top, ttop, atop, mtop, vtop, wtop, ftop, ntop, disktop,
              irqtop, swaptop, slabtop, kstop, stacktop, ctop, cgtop,
              contop, oomtop, pytop, rtop, sigtop, dbustop

    Args:
        command:    guider sub-command name (e.g. "ttop")
        duration:   monitoring duration in seconds (default 5)
        interval:   sampling interval in seconds (default 1)
        target:     optional process name or PID to filter (-e)
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    allowed = set(get_tool_commands("systemMonitor"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in systemMonitor. Use guiderHelp."})
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=extra_opts,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 2. bpfTrace
# ---------------------------------------------------------------------------
@mcp.tool()
def bpfTrace(
    command: str,
    duration: int = 10,
    interval: int = 1,
    target: str = "",
    func_name: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    eBPF-based kernel/user tracing (requires CAP_BPF or root, kernel ≥5.8).

    Commands: bpftop, bpfsnoop, bpfstacktop, bpfwaittop, bpfblktop,
              bpfrunqtop, bpfreclaimtop, bpftcpretrans, bpfdroptop,
              bpftcplat, bpflocktop, bpfbinderlat, bpfbindersnoop,
              bpfbinderpool, bpfsyscalltop, bpfsyscallsnoop, bpfpkttop,
              bpfpktsnoop, bpfnetlat, bpfwatch, bpfwatchtop, bpfwqtop,
              bpfcachetop, bpfkleaktop, bpflsmopen, bpfprogtop, irqlattop

    Args:
        command:    guider sub-command name (e.g. "bpfstacktop")
        duration:   tracing duration in seconds (default 10)
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-e)
        func_name:  kernel function name for bpftop/bpfsnoop (passed as positional arg)
        extra_opts: list of -q KEY[:VALUE] option strings (e.g. ["LAT", "ADDUSERSTACK"])
    """
    allowed = set(get_tool_commands("bpfTrace"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in bpfTrace. Use guiderHelp."})

    opts = list(extra_opts or [])
    # func_name for bpftop/bpfsnoop is passed via extra_opts mechanism using FUNC
    # Actually guider passes it as main arg; we embed in -q FUNC: approach won't work.
    # Use a workaround: prepend to args via adapter's target_pid channel isn't right.
    # The correct approach is that adapter's _build_cmd accepts it inline.
    # We'll use a custom run that prepends the function as main arg.
    if func_name:
        opts_with_func = [f"FUNC:{func_name}"] + opts
    else:
        opts_with_func = opts

    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=opts_with_func,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 3. ftraceProfile
# ---------------------------------------------------------------------------
@mcp.tool()
def ftraceProfile(
    command: str,
    duration: int = 5,
    interval: int = 1,
    target: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    ftrace / perf-based kernel function profiling (requires root, kernel ≥4.4).
    At most 1 ftrace command runs concurrently (tracefs semaphore enforced).

    Commands: trtop, tptop, bpfmarktop, funcrec, btop, utop, ktop, ptop,
              fperf, utrace, btrace, iorec, filerec, sysrec, stat

    Args:
        command:    guider sub-command name (e.g. "trtop")
        duration:   profiling duration in seconds (default 5)
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-e)
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    allowed = set(get_tool_commands("ftraceProfile"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in ftraceProfile. Use guiderHelp."})
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=extra_opts,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 4. networkTrace
# ---------------------------------------------------------------------------
@mcp.tool()
def networkTrace(
    command: str,
    duration: int = 10,
    interval: int = 1,
    target: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    Network performance tracing (TCP retransmits, packet drops, latency, etc.).

    Commands: ntop, bpftcpretrans, bpftcplife, bpfdroptop, bpftcplat,
              bpfpkttop, bpfpktsnoop, bpfnetlat, dbustop

    Args:
        command:    guider sub-command name (e.g. "bpftcpretrans")
        duration:   tracing duration in seconds (default 10)
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-e)
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    allowed = set(get_tool_commands("networkTrace"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in networkTrace. Use guiderHelp."})
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=extra_opts,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 5. androidPerf
# ---------------------------------------------------------------------------
@mcp.tool()
def androidPerf(
    command: str,
    duration: int = 5,
    interval: int = 1,
    device_id: str = "",
    input_file: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    Android performance analysis (Perfetto, Binder, ATrace, logcat, CAN, etc.).
    Requires adb connection for most commands.

    Commands: perfetto, bdtop, attop, gfxtop, bpfbinderlat, bpfbindersnoop,
              bpfbinderpool, andtop, bugrec, mdtop, andcmd, hprof, scrcap,
              logand, cantop, cansnoop

    Args:
        command:    guider sub-command name (e.g. "perfetto")
        duration:   monitoring duration in seconds (default 5)
        interval:   display interval in seconds (default 1)
        device_id:  Android device serial (adb -s <device_id>); leave empty for default
        input_file: path to existing trace file for offline analysis (-I)
        extra_opts: list of -q KEY[:VALUE] option strings (e.g. ["PERF:5s", "CPUFREQ"])
    """
    allowed = set(get_tool_commands("androidPerf"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in androidPerf. Use guiderHelp."})
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        device_id=device_id or None,
        input_file=input_file or None,
        extra_opts=extra_opts,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 6. memoryAnalyze
# ---------------------------------------------------------------------------
@mcp.tool()
def memoryAnalyze(
    command: str,
    duration: int = 5,
    interval: int = 1,
    target: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    Memory analysis: duplicate mapping detection, leak tracking, OOM monitoring.

    Commands: mtop, checkdup, bpfreclaimtop, leaktop, leaktrace,
              mtrace, oomtop, vtop, dump, slabtop

    Args:
        command:    guider sub-command name (e.g. "checkdup")
        duration:   monitoring duration in seconds (default 5); 0 for one-shot
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-e)
        extra_opts: list of -q KEY[:VALUE] option strings (e.g. ["SKIPEXMAPPED"])
    """
    allowed = set(get_tool_commands("memoryAnalyze"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in memoryAnalyze. Use guiderHelp."})
    result = adapter.run(
        command,
        duration=duration if duration > 0 else None,
        interval=interval,
        target_pid=target or None,
        extra_opts=extra_opts,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 7. visualize
# ---------------------------------------------------------------------------
@mcp.tool()
def visualize(
    command: str,
    input_file: str,
    extra_opts: list[str] | None = None,
) -> str:
    """
    Generate performance graphs and visualizations from recorded data files.

    Commands: draw, drawtime, drawcpu, drawmem, drawnet, drawdisk,
              drawflame, drawflamediff, drawscatter, drawhist, drawviolin,
              drawstack, drawbitmap, drawconn, drawpsi, drawreq, drawrss,
              drawgantt, drawdiff, convert

    Args:
        command:    guider sub-command name (e.g. "drawflame")
        input_file: path to the recorded data file (-I); REQUIRED
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    allowed = set(get_tool_commands("visualize"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in visualize. Use guiderHelp."})
    if not input_file:
        return _wrap({"ok": False, "error": "input_file is required for visualize commands"})
    result = adapter.run(
        command,
        input_file=input_file,
        extra_opts=extra_opts,
        json_output=False,  # visualization produces HTML/SVG output files
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 8. logAnalyze
# ---------------------------------------------------------------------------
@mcp.tool()
def logAnalyze(
    command: str,
    duration: int = 10,
    input_file: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    Log streaming and analysis (kernel messages, DLT, journald, Android logcat, etc.).

    Commands: logand, logkmsg, logdlt, logjrl, logsys, logtrace, convlog,
              printand, printkmsg, printdlt, printjrl, printtrace

    Args:
        command:    guider sub-command name (e.g. "logkmsg")
        duration:   streaming duration in seconds for live logs (default 10)
        input_file: path to existing log file for offline analysis (-I)
        extra_opts: list of -q KEY[:VALUE] option strings (e.g. ["FILTER:tag"])
    """
    allowed = set(get_tool_commands("logAnalyze"))
    if command not in allowed:
        return _wrap({"ok": False, "error": f"'{command}' not in logAnalyze. Use guiderHelp."})
    result = adapter.run(
        command,
        duration=duration,
        input_file=input_file or None,
        extra_opts=extra_opts,
        json_output=False,  # log commands produce text output
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 9. runCommand
# ---------------------------------------------------------------------------
@mcp.tool()
def runCommand(
    command: str,
    duration: int = 5,
    interval: int = 1,
    target: str = "",
    input_file: str = "",
    device_id: str = "",
    extra_opts: list[str] | None = None,
    json_output: bool = True,
) -> str:
    """
    Generic guider command runner — for any whitelisted command not covered by
    the specialized tools above. Blocked commands (kill, exec, LLM-loop) are rejected.

    Args:
        command:     guider sub-command name
        duration:    run duration in seconds (ignored for non-streaming commands)
        interval:    sampling interval in seconds (default 1)
        target:      optional process name or PID to filter (-e)
        input_file:  input file path for offline analysis (-I)
        device_id:   Android device serial
        extra_opts:  list of -q KEY[:VALUE] option strings
        json_output: request JSON output with -J flag (default True)
    """
    if command in BLOCKED_COMMANDS:
        return _wrap({"ok": False, "error": f"command '{command}' is blocked"})
    if command not in CATALOG:
        return _wrap({"ok": False, "error": f"unknown command '{command}'. Use guiderHelp to list."})
    meta = CATALOG[command]
    result = adapter.run(
        command,
        duration=duration if meta.get("streaming") else None,
        interval=interval,
        target_pid=target or None,
        input_file=input_file or None,
        device_id=device_id or None,
        extra_opts=extra_opts,
        json_output=json_output,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 10. guiderHelp
# ---------------------------------------------------------------------------
@mcp.tool()
def guiderHelp(
    query: str = "",
    tool_name: str = "",
) -> str:
    """
    List available guider commands and their metadata. No subprocess is launched.

    Args:
        query:     keyword to filter commands by name or description
        tool_name: MCP tool name to list (e.g. "bpfTrace"); empty = all tools
    """
    import json

    if tool_name:
        cmds = get_tool_commands(tool_name)
        if not cmds:
            return json.dumps({
                "ok": False,
                "error": f"unknown mcp_tool '{tool_name}'",
                "valid_tools": [
                    "systemMonitor", "bpfTrace", "ftraceProfile", "networkTrace",
                    "androidPerf", "memoryAnalyze", "visualize", "logAnalyze",
                    "runCommand", "guiderHelp",
                ],
            })
        results = {cmd: CATALOG[cmd] for cmd in cmds}
    elif query:
        q = query.lower()
        results = {
            cmd: meta
            for cmd, meta in CATALOG.items()
            if q in cmd or q in meta.get("description", "").lower()
        }
    else:
        # Return summary grouped by mcp_tool
        grouped: dict[str, list[str]] = {}
        for cmd, meta in CATALOG.items():
            t = meta["mcp_tool"]
            grouped.setdefault(t, []).append(cmd)
        return json.dumps({
            "ok": True,
            "total_commands": len(CATALOG),
            "mcp_tools": grouped,
            "usage": (
                "Call guiderHelp(tool_name='bpfTrace') to list BPF commands, "
                "or guiderHelp(query='tcp') to search by keyword."
            ),
        }, ensure_ascii=False)

    return json.dumps({
        "ok": True,
        "count": len(results),
        "commands": {
            cmd: {
                "description": meta["description"],
                "requires_root": meta["requires_root"],
                "streaming": meta["streaming"],
                "default_duration": meta.get("default_duration", ""),
                "mcp_tool": meta["mcp_tool"],
                "examples": meta.get("examples", []),
            }
            for cmd, meta in results.items()
        },
    }, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
