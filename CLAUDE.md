# Guider MCP Tools (AI Coding Tool Integration)

10 MCP tools are implemented in `mcp/guider-mcp.py`.
Claude Code connects automatically via `.mcp.json`.

## How to Use — Just Type a Prompt

**No special syntax is needed.** Type a natural language request and Claude will
automatically call the right guider tool.

Examples:
```
"Show me current system performance overview"
"Show me the hottest CPU threads right now"
"Find kernel-level on-CPU hotspots for 10 seconds"
"Check for duplicate memory mappings"
"Stream kernel messages for 5 seconds"
"List all BPF tracing commands"
"Capture a perfetto trace on Android device <YOUR_DEVICE_SERIAL>"
```

The MCP server starts automatically when Claude Code opens this project (via `.mcp.json`)
and stays alive for the whole session. You never start or stop it manually.

## Analysis Guidelines

When analyzing `top` output, always report in this order:

**1. PSI — identifies the bottleneck resource**
```
PSI cpu.some    > 10%  → CPU contention
PSI memory.some >  1%  → memory pressure
PSI io.some     >  5%  → I/O bottleneck
```

**2. CPU** — total%, user%, kernel%, idle%

**3. Memory** — available, anon(used), cache, swap usage

**4. I/O & Disk** — block read/write MB, iowait%, per-process I/O
- With root: pass `target="bd"` (maps to `-e bd`) to see per-storage-device
  availability and per-process I/O sizes
  ```
  systemMonitor("top", duration=3)               # basic (no root needed)
  systemMonitor("top", duration=3, target="bd")  # root: per-device + per-process I/O
  ```

**5. Top processes** — by CPU%, then by RSS

## What Happens Under the Hood

```
Your prompt
  → Claude picks the right tool (e.g. systemMonitor, bpfTrace)
  → guider-mcp.py receives the call
  → GuiderAdapter runs: python3 guider.py CMD -i 1 -R 5s -J
  → JSON envelope returned: { "ok": true, "data": [...], ... }
  → Claude interprets data and answers in natural language
```

## Quick Tool Reference

```
guiderHelp(query="tcp")                    # search commands by keyword
guiderHelp(tool_name="bpfTrace")           # list commands for a tool
systemMonitor("top", duration=3)           # process-level overview
systemMonitor("ttop", duration=3)          # thread-level drill-down
bpfTrace("bpfstacktop", duration=10)       # on-CPU kernel stack sampling
bpfTrace("bpftop", func_name="do_sys_open", duration=5)  # per-function call count
memoryAnalyze("checkdup")                  # detect duplicate memory mappings
androidPerf("perfetto", device_id="<YOUR_DEVICE_SERIAL>", extra_opts=["PERF:5s"])
logAnalyze("logkmsg", duration=5)          # kernel message streaming
visualize("drawflame", input_file="stacks.out")  # flame graph
```

## 10 MCP Tools

| Tool | Key Commands | Notes |
|------|-------------|-------|
| `systemMonitor` | top/ttop/mtop/vtop/disktop/irqtop/oomtop | no root required |
| `bpfTrace` | bpfstacktop/bpfsyscalltop/bpfbinderlat/bpfrunqtop | root/CAP_BPF, kernel≥5.8 |
| `ftraceProfile` | trtop/btop/ktop/funcrec | root, kernel≥4.4, max 1 concurrent |
| `networkTrace` | bpftcpretrans/bpftcplife/bpfdroptop/bpftcplat | root required |
| `androidPerf` | perfetto/bdtop/bpfbinderlat/logand/cantop | adb required |
| `memoryAnalyze` | checkdup/leaktop/oomtop/vtop/dump | - |
| `visualize` | drawflame/drawcpu/drawscatter/drawhist | -I file required |
| `logAnalyze` | logkmsg/logdlt/logjrl/convlog | - |
| `runCommand` | any whitelisted command | blocked: kill/exec/LLM-loop |
| `guiderHelp` | command catalog | no subprocess |

## Blocked Commands

```
kill, tkill, freeze, exec, swapout, sysrq        # system control
ask, chat, embed, rag, askai, askrun, aiperiodic  # LLM loop prevention
```

## First-Time Setup

```bash
pip install mcp               # required for guider-mcp.py
# Restart Claude Code after installing
# Verify: type /mcp — "guider" should appear in the list
```

## File Layout

- MCP server: `mcp/guider-mcp.py`
- Adapter: `mcp/guider_adapter.py`
- Command catalog: `mcp/guider_catalog.py`
- Claude Code config: `.mcp.json`
- REST API: `openapi/guider-rest.py`
- OpenAI function definitions: `openapi/function_definitions_openai.json`
- Full integration guide: `mcp/AI_INTEGRATION.md`
