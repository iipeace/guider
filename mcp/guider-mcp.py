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

import json
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
from guider_catalog import CATALOG, BLOCKED_COMMANDS, get_tool_commands, validate_catalog

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
    instructions=(
        "Guider Linux/Android performance analysis toolkit. "
        "10 tools covering system monitoring, BPF tracing, ftrace profiling, "
        "network tracing, Android performance, memory analysis, visualization, "
        "log analysis, generic command execution, and built-in help."
    ),
)

adapter = get_adapter()

# Validate catalog integrity at startup — log warnings if broken
for _issue in validate_catalog():
    logger.warning("catalog: %s", _issue)

# Pre-built frozensets of allowed commands per tool (avoid repeated O(n) scans)
_ALLOWED: dict[str, frozenset] = {
    t: frozenset(get_tool_commands(t))
    for t in [
        "systemMonitor", "bpfTrace", "ftraceProfile", "networkTrace",
        "androidPerf", "memoryAnalyze", "visualize", "logAnalyze",
    ]
}

# Reverse index: command name → correct MCP tool name (for helpful error messages)
_CMD_TO_TOOL: dict[str, str] = {cmd: meta["mcp_tool"] for cmd, meta in CATALOG.items()}


# ---------------------------------------------------------------------------
# Helper: build result summary for the LLM
# ---------------------------------------------------------------------------
def _wrap(result: dict[str, Any]) -> str:
    """Serialise the adapter envelope to a compact string for the LLM."""
    if result.get("truncated"):
        result.setdefault("warnings", []).insert(0, "output truncated to 500 KB")
    return json.dumps(result, ensure_ascii=False, default=str)


def _wrong_tool_error(command: str, tool_name: str) -> str:
    """Return a structured error pointing to the correct MCP tool."""
    correct = _CMD_TO_TOOL.get(command)
    hint = (
        f" Try {correct}(command='{command}', ...)."
        if correct
        else " Use guiderHelp() to list available commands."
    )
    return _wrap({"ok": False, "error": f"'{command}' is not in {tool_name}.{hint}"})


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

    Commands: top, ttop, atop, mtop, vtop, wtop, ftop, disktop,
              irqtop, swaptop, slabtop, kstop, stacktop, ctop, cgtop,
              contop, oomtop, pytop, rtop

    Args:
        command:    guider sub-command name (e.g. "ttop")
        duration:   monitoring duration in seconds (default 5)
        interval:   sampling interval in seconds (default 1)
        target:     optional process name or PID to filter (-g)
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    if command not in _ALLOWED["systemMonitor"]:
        return _wrong_tool_error(command, "systemMonitor")
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=list(extra_opts or []),
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
    device_id: str = "",
) -> str:
    """
    eBPF-based kernel/user tracing (requires CAP_BPF or root, kernel ≥5.8).

    Commands: bpftop, bpfsnoop, bpfstacktop, bpfwaittop, bpfblktop,
              bpfrunqtop, bpfreclaimtop, bpflocktop, bpfbinderlat,
              bpfbindersnoop, bpfbinderpool, bpfsyscalltop, bpfsyscallsnoop,
              bpfwatch, bpfwatchtop, bpfwqtop, bpfcachetop, bpfkleaktop,
              bpflsmopen, bpfprogtop, bpfsigtop, irqlattop

    Args:
        command:    guider sub-command name (e.g. "bpfstacktop")
        duration:   tracing duration in seconds (default 10)
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-g)
        func_name:  kernel function name for bpftop/bpfsnoop (passed as positional arg)
        extra_opts: list of -q KEY[:VALUE] option strings (e.g. ["LAT", "ADDUSERSTACK"])
        device_id:  Android device serial for bpfbinder* commands (adb -s <device_id>)
    """
    if command not in _ALLOWED["bpfTrace"]:
        return _wrong_tool_error(command, "bpfTrace")

    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=list(extra_opts or []),
        main_arg=func_name or None,
        device_id=device_id or None,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 3. ftraceProfile
# ---------------------------------------------------------------------------
@mcp.tool()
def ftraceProfile(
    command: str,
    duration: int = 3,
    interval: int = 1,
    target: str = "",
    input_file: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    ftrace / perf / ptrace-based function profiling and tracing.
    Genuine ftrace commands require root and kernel ≥4.4 and are serialized to
    1 concurrent run (tracefs semaphore); ptrace-based commands (utrace, btrace,
    strace, pytrace, sigtrace) and perf-based commands (utop, ptop, fperf, stat)
    need neither. filerec/genrec are not ftrace-based either (no root/kernel
    requirement for genrec; filerec still needs root for /proc access).

    Commands: trtop, tptop, bpfmarktop, funcrec, btop, utop, ktop, ptop,
              fperf, utrace, strace, pytrace, btrace, sigtrace, iorec, filerec,
              genrec, rec, report, sysrec, logtrace, stat

    Args:
        command:    guider sub-command name (e.g. "trtop")
        duration:   profiling duration in seconds (default 3)
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-g)
        input_file: path to a .dat file previously recorded by rec/funcrec/
                    iorec/sysrec/genrec, for offline analysis (-I); required
                    by "report"
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    if command not in _ALLOWED["ftraceProfile"]:
        return _wrong_tool_error(command, "ftraceProfile")
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        input_file=input_file or None,
        extra_opts=list(extra_opts or []),
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
        target:     optional process name or PID to filter (-g)
        extra_opts: list of -q KEY[:VALUE] option strings
    """
    if command not in _ALLOWED["networkTrace"]:
        return _wrong_tool_error(command, "networkTrace")
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        extra_opts=list(extra_opts or []),
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 5. androidPerf
# ---------------------------------------------------------------------------
@mcp.tool()
def androidPerf(
    command: str,
    duration: int = 3,
    interval: int = 1,
    device_id: str = "",
    input_file: str = "",
    extra_opts: list[str] | None = None,
    sub_command: str = "",
) -> str:
    """
    Android performance analysis (Perfetto, Binder, ATrace, logcat, CAN, etc.).
    Requires adb connection for most commands.

    Commands: perfetto, bdtop, attop, gfxtop, andtop, bugrec, mdtop,
              andcmd, hprof, scrcap, logand, lmksnoop, cantop, cansnoop, sperf,
              getprop, watchprop, bugrep, scrrec, printboot

    Args:
        command:     guider sub-command name (e.g. "perfetto")
        duration:    monitoring duration in seconds (default 3)
        interval:    display interval in seconds (default 1)
        device_id:   Android device serial (adb -s <device_id>); leave empty for default
        input_file:  path to existing trace file for offline analysis (-I)
        extra_opts:  list of -q KEY[:VALUE] option strings (e.g. ["PERF:5s", "CPUFREQ"])
        sub_command: positional main argument, reused across several commands:
                     - andcmd: sub-command (e.g. "getselinux", "getpkglist",
                       "getproclist", "getbinderstats", "getappstat", "getpkgattr")
                     - getprop: property name/wildcard (e.g. "ro.build.*")
                     - watchprop: property name/wildcard, optionally "|value"
                     - bugrep: optional output directory
                     Ignored for other commands.
    """
    if command not in _ALLOWED["androidPerf"]:
        return _wrong_tool_error(command, "androidPerf")
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        device_id=device_id or None,
        input_file=input_file or None,
        extra_opts=list(extra_opts or []),
        main_arg=sub_command or None,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 6. memoryAnalyze
# ---------------------------------------------------------------------------
@mcp.tool()
def memoryAnalyze(
    command: str,
    duration: int = 3,
    interval: int = 1,
    target: str = "",
    extra_opts: list[str] | None = None,
) -> str:
    """
    Memory analysis: duplicate mapping detection, leak tracking, OOM monitoring.

    Commands: checkdup, leaktop, leaktrace, mtrace, dump, mem

    Args:
        command:    guider sub-command name (e.g. "checkdup")
        duration:   monitoring duration in seconds (default 5); 0 for one-shot
        interval:   display interval in seconds (default 1)
        target:     optional process name or PID to filter (-g)
        extra_opts: list of -q KEY[:VALUE] option strings (e.g. ["SKIPEXMAPPED"])
    """
    if command not in _ALLOWED["memoryAnalyze"]:
        return _wrong_tool_error(command, "memoryAnalyze")
    result = adapter.run(
        command,
        duration=duration if duration > 0 else None,
        interval=interval,
        target_pid=target or None,
        extra_opts=list(extra_opts or []),
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 7. visualize
# ---------------------------------------------------------------------------
_DRAWAVG_COMMANDS = {"drawavg", "drawcpuavg", "drawmemavg", "drawvssavg", "drawrssavg"}


@mcp.tool()
def visualize(
    command: str,
    input_file: str = "",
    input_files: list[str] | None = None,
    target: str = "",
    extra_opts: list[str] | None = None,
    draw_format: str = "",
    draw_layout: str = "",
    top_number: int = 0,
    output_dir: str = "",
) -> str:
    """
    Generate performance graphs and visualizations from recorded data files.

    Commands: draw, drawtime, drawcpu, drawmem, drawnet, drawdisk,
              drawflame, drawflamediff, drawscatter, drawhist, drawviolin,
              drawstack, drawbitmap, drawconn, drawpsi, drawreq, drawrss,
              drawdiff, drawdelay, drawio, drawleak, drawpri, drawvss, convert,
              drawavg, drawcpuavg, drawmemavg, drawvssavg, drawrssavg

    Note: drawconn does NOT read a data file — it's a live scan of the
    current IPC pipe/socket connections. Pass an optional PID via `target`
    to focus the graph on one process; leave both input_file and target
    empty to show all connections.

    The drawavg-family commands (drawavg, drawcpuavg, drawmemavg, drawvssavg,
    drawrssavg) average data across MULTIPLE recorded files and require
    `input_files` (a list of >= 2 paths) instead of `input_file`.

    Every other command requires input_file.

    Args:
        command:     guider sub-command name (e.g. "drawflame")
        input_file:  path to the recorded data file (-I); required for every
                     command except drawconn and the drawavg-family
        input_files: list of >= 2 recorded data file paths, passed as
                     positional args; required for the drawavg-family commands
        target:      optional PID to focus on; used only by drawconn
                     (ignored by every other command)
        extra_opts:  list of -q KEY[:VALUE] option strings
        draw_format: image output format (-F): svg/png/pdf/ps/eps/html
        draw_layout: graph layout spec (-L), e.g. "C:CPU|M:Memory". Only the
                     generic "draw" command reads this; every single-purpose
                     draw* command hardcodes its own layout and ignores it.
        top_number:  top-N number to show in the graph (-T). Has no effect on
                     drawmem/drawmemavg, whose default view has no per-process
                     top-N panel; use drawcpu/drawvss/drawrss for that.
        output_dir:  directory to write the generated graph file to (-o)
    """
    if command not in _ALLOWED["visualize"]:
        return _wrong_tool_error(command, "visualize")

    common_kwargs = {
        "extra_opts": list(extra_opts or []),
        "draw_format": draw_format or None,
        "draw_layout": draw_layout or None,
        "top_number": top_number or None,
        "output_dir": output_dir or None,
        "json_output": False,  # visualization produces HTML/SVG output files
    }

    if command == "drawconn":
        result = adapter.run(command, main_arg=target or None, **common_kwargs)
    elif command in _DRAWAVG_COMMANDS:
        if not input_files or len(input_files) < 2:
            return _wrap({
                "ok": False,
                "error": f"'{command}' requires input_files with at least 2 file paths",
            })
        result = adapter.run(command, input_files=input_files, **common_kwargs)
    else:
        if not input_file:
            return _wrap({"ok": False, "error": "input_file is required for visualize commands"})
        result = adapter.run(command, input_file=input_file, **common_kwargs)
    return _wrap(result)


# ---------------------------------------------------------------------------
# 8. logAnalyze
# ---------------------------------------------------------------------------
@mcp.tool()
def logAnalyze(
    command: str,
    duration: int = 10,
    interval: int = 1,
    target: str = "",
    input_file: str = "",
    extra_opts: list[str] | None = None,
    json_output: bool = False,
) -> str:
    """
    Log streaming and analysis (kernel messages, DLT, journald, Android logcat, etc.).

    Commands: logand, logdlt, logjrl, logkmsg, logsys, logtrace, convlog,
              printand, printkmsg, printdlt, printjrl, printtrace, printsyslog

    Note: logand/logdlt/logjrl/logkmsg/logsys/logtrace WRITE a single message
    to their log sink and never produce JSON. printand/printkmsg/printdlt/
    printjrl/printtrace/printsyslog READ/stream the log source and support
    json_output=True and target (-g) filtering.

    Args:
        command:     guider sub-command name (e.g. "printkmsg")
        duration:    streaming duration in seconds for live logs (default 10)
        interval:    sampling interval in seconds for streaming logs (default 1)
        target:      optional process/tag name or PID to filter (-g); printX only
        input_file:  path to existing log file for offline analysis (-I)
        extra_opts:  list of -q KEY[:VALUE] option strings (e.g. ["FILTER:tag"])
        json_output: request JSON output (-J); only the printX read commands support it
    """
    if command not in _ALLOWED["logAnalyze"]:
        return _wrong_tool_error(command, "logAnalyze")
    result = adapter.run(
        command,
        duration=duration,
        interval=interval,
        target_pid=target or None,
        input_file=input_file or None,
        extra_opts=list(extra_opts or []),
        json_output=json_output,
    )
    return _wrap(result)


# ---------------------------------------------------------------------------
# 9. runCommand
# ---------------------------------------------------------------------------
@mcp.tool()
def runCommand(
    command: str,
    duration: int = 3,
    interval: int = 1,
    target: str = "",
    input_file: str = "",
    device_id: str = "",
    extra_opts: list[str] | None = None,
    json_output: bool = True,
    main_arg: str = "",
) -> str:
    """
    Generic guider command runner — for any whitelisted command not covered by
    the specialized tools above. Blocked commands (kill, exec, LLM-loop) are rejected.

    Args:
        command:     guider sub-command name
        duration:    run duration in seconds (ignored for non-streaming commands)
        interval:    sampling interval in seconds (default 1)
        target:      optional process name or PID to filter (-g)
        input_file:  input file path for offline analysis (-I)
        device_id:   Android device serial
        extra_opts:  list of -q KEY[:VALUE] option strings
        json_output: request JSON output with -J flag (default True)
        main_arg:    positional argument the command itself takes, e.g.
                     "250" (cputest CPU%), "1G" (memtest size),
                     "read:FILE" (iotest path), "tcp:IP:PORT" (nettest target)
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
        extra_opts=list(extra_opts or []),
        json_output=json_output,
        main_arg=main_arg or None,
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
    if tool_name:
        # runCommand is a pass-through for any CATALOG command — no dedicated mcp_tool tag
        if tool_name == "runCommand":
            return json.dumps({
                "ok": True,
                "tool": "runCommand",
                "description": (
                    "Generic pass-through runner for any command in the CATALOG. "
                    "Accepts any non-blocked command. Use guiderHelp() with no args "
                    "to see all available commands grouped by their primary tool, or "
                    "guiderHelp(query='keyword') to search."
                ),
                "blocked_commands": sorted(BLOCKED_COMMANDS),
                "total_available": len(CATALOG),
            }, ensure_ascii=False)
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
            cmd: {k: v for k, v in {
                "description": meta["description"],
                "requires_root": meta["requires_root"],
                "streaming": meta["streaming"],
                "default_duration": meta.get("default_duration", ""),
                "mcp_tool": meta["mcp_tool"],
                "main_arg_name": meta.get("main_arg_name", ""),
                "main_arg_desc": meta.get("main_arg_desc", ""),
                "examples": meta.get("examples", []),
            }.items() if v != ""}
            for cmd, meta in results.items()
        },
    }, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
