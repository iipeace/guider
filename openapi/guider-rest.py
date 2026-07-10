#!/usr/bin/env python3
"""
guider-rest.py — FastAPI REST server for Guider performance analysis toolkit.

Provides HTTP endpoints compatible with OpenAI function calling and
Google Gemini Code Assist function definitions.

Usage:
    pip install fastapi uvicorn
    python3 guider-rest.py [--port 8080] [--host 0.0.0.0]
    # OpenAPI spec: http://localhost:8080/openapi.json
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

_HERE = os.path.dirname(os.path.abspath(__file__))
_MCP_DIR = os.path.join(_HERE, "..", "mcp")
if _MCP_DIR not in sys.path:
    sys.path.insert(0, _MCP_DIR)

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    print(
        "ERROR: fastapi and uvicorn are required.\n"
        "Install with: pip install fastapi uvicorn",
        file=sys.stderr,
    )
    sys.exit(1)

from guider_adapter import get_adapter
from guider_catalog import CATALOG, get_tool_commands
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Guider Performance Analysis API",
    description=(
        "REST API for the Guider Linux/Android performance analysis toolkit. "
        "10 endpoints covering system monitoring, BPF tracing, ftrace profiling, "
        "network tracing, Android performance, memory analysis, visualization, "
        "log analysis, generic command execution, and built-in help."
    ),
    version="1.0.0",
)
adapter = get_adapter()


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class SystemMonitorRequest(BaseModel):
    command: str = Field(..., description="guider sub-command (e.g. ttop)")
    duration: int = Field(5, ge=1, le=300, description="monitoring duration in seconds")
    interval: int = Field(1, ge=1, description="sampling interval in seconds")
    target: str = Field("", description="process name or PID (-e)")
    extra_opts: list[str] = Field(default_factory=list, description="-q KEY[:VALUE] options")


class BpfTraceRequest(BaseModel):
    command: str = Field(..., description="guider BPF sub-command (e.g. bpfstacktop)")
    duration: int = Field(10, ge=1, le=300)
    interval: int = Field(1, ge=1)
    target: str = Field("")
    func_name: str = Field("", description="kernel function name for bpftop/bpfsnoop")
    extra_opts: list[str] = Field(default_factory=list)


class FtraceProfileRequest(BaseModel):
    command: str = Field(...)
    duration: int = Field(5, ge=1, le=300)
    interval: int = Field(1, ge=1)
    target: str = Field("")
    extra_opts: list[str] = Field(default_factory=list)


class NetworkTraceRequest(BaseModel):
    command: str = Field(...)
    duration: int = Field(10, ge=1, le=300)
    interval: int = Field(1, ge=1)
    target: str = Field("")
    extra_opts: list[str] = Field(default_factory=list)


class AndroidPerfRequest(BaseModel):
    command: str = Field(...)
    duration: int = Field(5, ge=1, le=300)
    interval: int = Field(1, ge=1)
    device_id: str = Field("", description="Android device serial")
    input_file: str = Field("", description="trace file for offline analysis")
    extra_opts: list[str] = Field(default_factory=list)


class MemoryAnalyzeRequest(BaseModel):
    command: str = Field(...)
    duration: int = Field(5, ge=0, le=300)
    interval: int = Field(1, ge=1)
    target: str = Field("")
    extra_opts: list[str] = Field(default_factory=list)


class VisualizeRequest(BaseModel):
    command: str = Field(...)
    input_file: str = Field(..., description="path to recorded data file")
    extra_opts: list[str] = Field(default_factory=list)


class LogAnalyzeRequest(BaseModel):
    command: str = Field(...)
    duration: int = Field(10, ge=1, le=300)
    input_file: str = Field("")
    extra_opts: list[str] = Field(default_factory=list)


class RunCommandRequest(BaseModel):
    command: str = Field(...)
    duration: int = Field(5, ge=0, le=300)
    interval: int = Field(1, ge=1)
    target: str = Field("")
    input_file: str = Field("")
    device_id: str = Field("")
    extra_opts: list[str] = Field(default_factory=list)
    json_output: bool = Field(True)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _check_command(command: str, allowed_cmds: list[str]) -> None:
    if command not in allowed_cmds:
        raise HTTPException(
            status_code=400,
            detail=f"'{command}' not in allowed set: {allowed_cmds}. "
                   f"Use GET /guiderHelp to see all commands.",
        )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "guider_path": adapter._guider_path}


@app.post("/systemMonitor")
def system_monitor(req: SystemMonitorRequest) -> dict:
    _check_command(req.command, get_tool_commands("systemMonitor"))
    return adapter.run(
        req.command,
        duration=req.duration,
        interval=req.interval,
        target_pid=req.target or None,
        extra_opts=req.extra_opts,
    )


@app.post("/bpfTrace")
def bpf_trace(req: BpfTraceRequest) -> dict:
    _check_command(req.command, get_tool_commands("bpfTrace"))
    return adapter.run(
        req.command,
        duration=req.duration,
        interval=req.interval,
        target_pid=req.target or None,
        extra_opts=list(req.extra_opts),
        main_arg=req.func_name or None,
    )


@app.post("/ftraceProfile")
def ftrace_profile(req: FtraceProfileRequest) -> dict:
    _check_command(req.command, get_tool_commands("ftraceProfile"))
    return adapter.run(
        req.command,
        duration=req.duration,
        interval=req.interval,
        target_pid=req.target or None,
        extra_opts=req.extra_opts,
    )


@app.post("/networkTrace")
def network_trace(req: NetworkTraceRequest) -> dict:
    _check_command(req.command, get_tool_commands("networkTrace"))
    return adapter.run(
        req.command,
        duration=req.duration,
        interval=req.interval,
        target_pid=req.target or None,
        extra_opts=req.extra_opts,
    )


@app.post("/androidPerf")
def android_perf(req: AndroidPerfRequest) -> dict:
    _check_command(req.command, get_tool_commands("androidPerf"))
    return adapter.run(
        req.command,
        duration=req.duration,
        interval=req.interval,
        device_id=req.device_id or None,
        input_file=req.input_file or None,
        extra_opts=req.extra_opts,
    )


@app.post("/memoryAnalyze")
def memory_analyze(req: MemoryAnalyzeRequest) -> dict:
    _check_command(req.command, get_tool_commands("memoryAnalyze"))
    return adapter.run(
        req.command,
        duration=req.duration if req.duration > 0 else None,
        interval=req.interval,
        target_pid=req.target or None,
        extra_opts=req.extra_opts,
    )


@app.post("/visualize")
def visualize(req: VisualizeRequest) -> dict:
    _check_command(req.command, get_tool_commands("visualize"))
    if not req.input_file:
        raise HTTPException(status_code=400, detail="input_file is required for visualize commands")
    return adapter.run(
        req.command,
        input_file=req.input_file,
        extra_opts=req.extra_opts,
        json_output=False,
    )


@app.post("/logAnalyze")
def log_analyze(req: LogAnalyzeRequest) -> dict:
    _check_command(req.command, get_tool_commands("logAnalyze"))
    return adapter.run(
        req.command,
        duration=req.duration,
        input_file=req.input_file or None,
        extra_opts=req.extra_opts,
        json_output=False,
    )


@app.post("/runCommand")
def run_command(req: RunCommandRequest) -> dict:
    from guider_catalog import BLOCKED_COMMANDS
    if req.command in BLOCKED_COMMANDS:
        raise HTTPException(status_code=403, detail=f"command '{req.command}' is blocked")
    if req.command not in CATALOG:
        raise HTTPException(status_code=400, detail=f"unknown command '{req.command}'")
    meta = CATALOG[req.command]
    return adapter.run(
        req.command,
        duration=req.duration if (req.duration > 0 and meta.get("streaming")) else None,
        interval=req.interval,
        target_pid=req.target or None,
        input_file=req.input_file or None,
        device_id=req.device_id or None,
        extra_opts=req.extra_opts,
        json_output=req.json_output,
    )


@app.get("/guiderHelp")
def guider_help(
    query: str = Query("", description="keyword filter"),
    tool_name: str = Query("", description="MCP tool name to list"),
) -> dict:
    valid_tools = [
        "systemMonitor", "bpfTrace", "ftraceProfile", "networkTrace",
        "androidPerf", "memoryAnalyze", "visualize", "logAnalyze",
        "runCommand", "guiderHelp",
    ]
    if tool_name:
        if tool_name not in valid_tools:
            raise HTTPException(status_code=400, detail=f"unknown tool '{tool_name}'")
        cmds = get_tool_commands(tool_name)
        results = {cmd: CATALOG[cmd] for cmd in cmds}
    elif query:
        q = query.lower()
        results = {
            cmd: meta
            for cmd, meta in CATALOG.items()
            if q in cmd or q in meta.get("description", "").lower()
        }
        return {"ok": True, "count": len(results), "commands": results}
    else:
        grouped: dict[str, list[str]] = {}
        for cmd, meta in CATALOG.items():
            t = meta["mcp_tool"]
            grouped.setdefault(t, []).append(cmd)
        return {
            "ok": True,
            "total_commands": len(CATALOG),
            "mcp_tools": grouped,
        }
    return {
        "ok": True,
        "count": len(results),
        "commands": {
            cmd: {
                "description": m["description"],
                "requires_root": m["requires_root"],
                "streaming": m["streaming"],
                "mcp_tool": m["mcp_tool"],
                "examples": m.get("examples", []),
            }
            for cmd, m in results.items()
        },
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Guider REST API server")
    parser.add_argument("--host", default="127.0.0.1", help="bind host (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="bind port (default 8080)")
    parser.add_argument("--reload", action="store_true", help="auto-reload on file changes")
    args = parser.parse_args()

    print(f"Starting Guider REST API on http://{args.host}:{args.port}")
    print(f"OpenAPI spec: http://{args.host}:{args.port}/openapi.json")
    uvicorn.run(
        "guider-rest:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
