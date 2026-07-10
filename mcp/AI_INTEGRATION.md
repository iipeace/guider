# Guider AI Coding Tool Integration Guide

This document explains how to connect Guider performance analysis to three AI coding tools:
**Claude Code**, **Google Gemini Code Assist**, and **OpenAI Codex**.

---

## How It Works — The Complete Flow

**Yes, just type a natural language prompt.** No special syntax is needed.

When you type a prompt like *"show me the top CPU-consuming threads right now"*, the following
happens automatically:

```
1. You type a natural language prompt
         │
         ▼
2. Claude Code reads tool schemas on startup
   (from guider-mcp.py via .mcp.json — done once per session)
         │
         ▼
3. Claude decides which MCP tool to call
   e.g. systemMonitor("top", duration=3)              # process-level overview
        systemMonitor("top", duration=3, target="bd")   # root: + per-device I/O & disk usage
         │
         ▼
4. guider-mcp.py receives the tool call over stdio
         │
         ▼
5. GuiderAdapter builds a subprocess command list
   e.g. ["python3", "guider.py", "ttop", "-i", "1", "-R", "5s", "-J"]
         │
         ▼
6. guider.py runs as a subprocess (shell=False, isolated process group)
         │
         ▼
7. JSON output is parsed and wrapped in a result envelope:
   { "ok": true, "command": "ttop", "data": [...], "duration_sec": 5.1, ... }
         │
         ▼
8. Claude reads the envelope and interprets the data
         │
         ▼
9. Claude answers in natural language with analysis and recommendations
```

The MCP server (`guider-mcp.py`) is **started automatically** by Claude Code when a session
begins (via `.mcp.json`), and stays alive for the entire session. You do not start or stop it
manually.

---

## Architecture Overview

```
Claude Code (MCP native) │ Gemini CLI (MCP) │ OpenAI Codex (REST)
         stdio           │    stdio/SSE      │    HTTP REST
─────────────────────────┼───────────────────┼──────────────────────
        mcp/guider-mcp.py  (MCP Server — 10 tools)
─────────────────────────┴───────────────────┴──────────────────────
        mcp/guider_adapter.py  (subprocess engine, security, cleanup)
────────────────────────────────────────────────────────────────────
        guider/guider.py  (core — NOT modified)
```

The adapter runs guider via subprocess using standard flags:
- `-J` — JSON output
- `-R Ns` — duration limit (prevents infinite loops)
- `-i N` — sampling interval
- `-e target` — process filter
- `-q KEY[:VALUE]` — feature options

---

## MCP Server Lifecycle

| Event | What Happens |
|-------|-------------|
| Claude Code starts | Reads `.mcp.json`, launches `python3 mcp/guider-mcp.py` as a child process |
| First tool call | MCP server imports catalog + adapter, locates guider.py |
| Each tool call | GuiderAdapter spawns a guider subprocess, waits, returns JSON envelope |
| Subprocess timeout | SIGTERM → 2s → SIGKILL sent to the process group |
| Claude Code exits | SIGTERM sent to MCP server → `atexit` kills all active guider subprocesses |
| Ctrl+C | SIGINT handler cleans up children and exits |

The MCP server process is completely transparent — you never interact with it directly.

---

## 10 MCP Tools

| Tool | Purpose | Key Commands |
|------|---------|-------------|
| `systemMonitor` | CPU/memory/IO/thread monitoring | top, ttop, mtop, vtop, disktop |
| `bpfTrace` | eBPF kernel/user tracing | bpfstacktop, bpfsyscalltop, bpfbinderlat |
| `ftraceProfile` | ftrace/perf profiling | trtop, btop, ktop, funcrec |
| `networkTrace` | TCP/packet tracing | bpftcpretrans, bpftcplife, bpfdroptop |
| `androidPerf` | Android Perfetto/Binder/ATrace | perfetto, bdtop, bpfbinderlat, logand |
| `memoryAnalyze` | Memory leak/dup detection | checkdup, leaktop, oomtop, vtop |
| `visualize` | Flame graphs, charts, histograms | drawflame, drawcpu, drawscatter |
| `logAnalyze` | Log streaming/analysis | logkmsg, logdlt, logjrl, convlog |
| `runCommand` | Generic whitelisted runner | any non-blocked command |
| `guiderHelp` | Command catalog (no subprocess) | always available |

---

## 1. Claude Code (Recommended — MCP Native)

Claude Code natively supports MCP via stdio. The `.mcp.json` at the project root
configures automatic connection.

### Setup

```bash
cd <GUIDER_ROOT>    # e.g. $HOME/guider

# Install MCP SDK (one-time)
pip install mcp

# Optional: verify the MCP server starts without error
python3 mcp/guider-mcp.py
# (waits for stdio — press Ctrl+C to exit)
```

The `.mcp.json` is pre-configured at the project root:
```json
{
  "mcpServers": {
    "guider": {
      "command": "python3",
      "args": ["<GUIDER_ROOT>/mcp/guider-mcp.py"],
      "env": {
        "GUIDER_PATH": "<GUIDER_ROOT>/guider/guider.py"
      }
    }
  }
}
```
Replace `<GUIDER_ROOT>` with the absolute path to your guider checkout
(e.g. `/home/user/guider`). If your `mcp` package lives in a virtualenv,
set `command` to that virtualenv's `python3` instead.

**After placing `.mcp.json`, restart Claude Code.** The 10 tools appear automatically.
Verify with `/mcp` in the Claude Code prompt — you should see `guider` listed.

### Example Prompts (just type these)

```
List all available BPF tracing commands
Show me the hottest CPU threads right now
Find on-CPU kernel hotspots over the next 10 seconds
Check for duplicate memory mappings
Capture Android performance trace on device <YOUR_DEVICE_SERIAL> with jank analysis
Stream kernel messages for 5 seconds
Generate a flame graph from stacks.out
What is using the most memory?
```

Claude will automatically choose the right tool and command for each prompt.

### Troubleshooting

| Problem | Fix |
|---------|-----|
| Tools not appearing in `/mcp` | Restart Claude Code; check `.mcp.json` is at project root |
| `ModuleNotFoundError: mcp` | Run `pip install mcp` |
| `guider.py not found` | Set `GUIDER_PATH` in `.mcp.json` env or run from the guider repo root |
| `too many concurrent calls` | Wait for previous calls to finish (max 3 concurrent) |
| `tracefs busy` | Another ftrace command is running; wait for it to finish |
| `ok: false, error: "exit code 1"` | Most BPF/ftrace commands require root (`sudo`) |

---

## 2. Google Gemini Code Assist

### Option A: Gemini CLI (MCP)

```bash
# Install Gemini CLI
pip install gemini-cli
# or: npm install -g @google/gemini-cli

# Register guider MCP server
gemini mcp add guider python3 <GUIDER_ROOT>/mcp/guider-mcp.py

# Verify
gemini mcp list
```

Once registered, type natural language prompts in Gemini CLI — it calls the guider tools
the same way Claude Code does.

### Option B: Gemini API with Function Definitions

```python
import json
import google.generativeai as genai

# Load pre-built function definitions (OpenAI format)
with open("openapi/function_definitions_openai.json") as f:
    openai_defs = json.load(f)

# Convert to Gemini format
def to_gemini(d: dict) -> dict:
    fn = d["function"]
    return {"name": fn["name"], "description": fn["description"],
            "parameters": fn["parameters"]}

gemini_tools = [to_gemini(d) for d in openai_defs]

# Configure model
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-pro", tools=gemini_tools)

# Start the REST server first: python3 openapi/guider-rest.py --port 8080
import requests

def handle_gemini_call(function_call) -> str:
    name = function_call.name
    args = dict(function_call.args)
    result = requests.post(f"http://localhost:8080/{name}", json=args, timeout=60)
    return json.dumps(result.json())
```

---

## 3. OpenAI Codex / GPT-4 Function Calling

### Static Function Definitions

```python
import json
import openai
import requests

# Load pre-built definitions
with open("openapi/function_definitions_openai.json") as f:
    tools = json.load(f)

client = openai.OpenAI(api_key="YOUR_KEY")
REST_BASE = "http://localhost:8080"  # start guider-rest.py first

def call_guider(name: str, args: dict) -> str:
    resp = requests.post(f"{REST_BASE}/{name}", json=args, timeout=120)
    return json.dumps(resp.json(), ensure_ascii=False)

messages = [{"role": "user", "content": "What are the hottest CPU threads right now?"}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

msg = response.choices[0].message
messages.append(msg)

for tc in msg.tool_calls or []:
    result = call_guider(tc.function.name, json.loads(tc.function.arguments))
    messages.append({
        "role": "tool",
        "tool_call_id": tc.id,
        "content": result,
    })

# Continue conversation with tool results
final = client.chat.completions.create(model="gpt-4o", messages=messages)
print(final.choices[0].message.content)
```

### Dynamic Definitions from OpenAPI

```python
import requests
# FastAPI auto-generates OpenAPI 3.1 compatible spec
spec = requests.get("http://localhost:8080/openapi.json").json()
```

---

## REST Server Setup (Required for Gemini/OpenAI)

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Start server (localhost only by default)
python3 <GUIDER_ROOT>/openapi/guider-rest.py --port 8080

# Endpoints:
# GET  /health                    health check
# GET  /guiderHelp?tool_name=X    command catalog
# GET  /openapi.json              OpenAPI 3.1 spec
# POST /systemMonitor             system monitoring
# POST /bpfTrace                  BPF tracing
# POST /ftraceProfile             ftrace profiling
# POST /networkTrace              network tracing
# POST /androidPerf               Android performance
# POST /memoryAnalyze             memory analysis
# POST /visualize                 visualization
# POST /logAnalyze                log analysis
# POST /runCommand                generic runner

# Test
curl -s http://localhost:8080/health
curl -s "http://localhost:8080/guiderHelp?tool_name=bpfTrace" | python3 -m json.tool
```

---

## Security Notes

### Blocked Commands (MCP/REST refuse these)
```
# System control / destructive
kill, tkill, freeze, pause, hook, cgroup, swapout
limitcpu, limitcpuset, limitmem, limitread, limitwrite
setafnt, setcpu, setsched, setprop, sysrq, exec

# LLM loop prevention
ask, chat, embed, rag, askai, askrun, aiperiodic
```

### Blocked -q Options
`ASKAI`, `ASKRUN`, `AIPERIODIC`, `LLMPROVIDER`, `LLMMODEL`,
`EXITCMD`, `PRINTCMD`, `DUPOUTPATH`, `OUTFILEUSER`, `OUTFILEPERM`

### Concurrency Limits
- Max 3 concurrent guider calls (`threading.Semaphore(3)`)
- ftrace commands: max 1 concurrent (tracefs semaphore)
- All subprocesses: `start_new_session=True` → process group kill on timeout

### Output Limits
- Responses truncated at 500 KB; `"truncated": true` flag set

---

## Result Envelope

Every tool call returns a JSON envelope:

```json
{
  "ok": true,
  "command": "ttop",
  "timestamp": 1720000000.0,
  "duration_sec": 5.1,
  "data": [ { /* one guider JSON object per sampling interval */ } ],
  "truncated": false,
  "warnings": [],
  "error": null
}
```

- `ok: false` — check `error` field for the reason
- `truncated: true` — output exceeded 500 KB; only the first 500 KB is in `data`
- `warnings` — non-fatal issues (e.g. blocked options, stderr output)

---

## Verification

```bash
cd <GUIDER_ROOT>    # e.g. $HOME/guider

# 1. Syntax check all MCP files
python3 -m py_compile mcp/guider-mcp.py     && echo 'guider-mcp.py: OK'
python3 -m py_compile mcp/guider_adapter.py && echo 'guider_adapter.py: OK'
python3 -m py_compile mcp/guider_catalog.py && echo 'guider_catalog.py: OK'

# 2. Catalog check
python3 -c "
import sys; sys.path.insert(0, 'mcp')
from guider_catalog import CATALOG, get_tool_commands
print('Total commands:', len(CATALOG))
for tool in ['systemMonitor','bpfTrace','ftraceProfile','networkTrace',
             'androidPerf','memoryAnalyze','visualize','logAnalyze']:
    print(f'  {tool}: {len(get_tool_commands(tool))} commands')
"

# 3. Adapter functional test (requires guider.py + python3)
python3 -c "
import sys; sys.path.insert(0, 'mcp')
from guider_adapter import GuiderAdapter
r = GuiderAdapter().run('ttop', duration=2)
print('ok:', r['ok'], '| duration_sec:', r['duration_sec'])
"

# 4. MCP server start test (requires pip install mcp)
python3 mcp/guider-mcp.py &
sleep 1 && kill %1 && echo 'MCP server: OK'

# 5. REST server check (requires fastapi)
python3 -m py_compile openapi/guider-rest.py && echo 'guider-rest.py: OK'
```
