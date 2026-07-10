# Guider MCP Tools (AI Coding Tool Integration)

10 MCP tools are implemented in `mcp/guider-mcp.py`.
Claude Code connects automatically via `.mcp.json`.

## Quick Usage

```
guiderHelp(query="tcp")                    # search commands by keyword
guiderHelp(tool_name="bpfTrace")           # list commands for a tool
systemMonitor("ttop", duration=5)          # thread-level CPU monitor
bpfTrace("bpfstacktop", duration=10)       # on-CPU kernel stack sampling
memoryAnalyze("checkdup")                  # detect duplicate memory mappings
androidPerf("perfetto", device_id="5af877f6", extra_opts=["PERF:5s"])
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

## File Layout

- MCP server: `mcp/guider-mcp.py`
- Adapter: `mcp/guider_adapter.py`
- Command catalog: `mcp/guider_catalog.py`
- Claude Code config: `.mcp.json`
- REST API: `openapi/guider-rest.py`
- OpenAI function definitions: `openapi/function_definitions_openai.json`
- Integration guide: `mcp/AI_INTEGRATION.md`
