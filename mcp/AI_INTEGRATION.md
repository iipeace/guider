# Guider AI Coding Tool Integration Guide

This document explains how to connect Guider performance analysis to three AI coding tools:
**Claude Code**, **Google Gemini Code Assist**, and **OpenAI Codex**.

> Note: The existing `docs/` directory is root-owned. This file lives in `mcp/` instead.
> A symlink or copy can be placed in `docs/` once root access is available.

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

Claude Code natively supports MCP via stdio. The `.mcp.json` at project root
configures automatic connection.

### Setup

```bash
cd /home/iipeace/work/guider

# Install MCP SDK
pip install mcp

# Verify MCP server starts
python3 mcp/guider-mcp.py
# (press Ctrl+C — it waits for stdio input)
```

The `.mcp.json` is pre-configured:
```json
{
  "mcpServers": {
    "guider": {
      "command": "python3",
      "args": ["/home/iipeace/work/guider/mcp/guider-mcp.py"],
      "env": {
        "GUIDER_PATH": "/home/iipeace/work/guider/guider/guider.py"
      }
    }
  }
}
```

Restart Claude Code after placing `.mcp.json` — the 10 tools become available automatically.

### Example Prompts

```
"Use guiderHelp to list all BPF tracing commands"
"Run systemMonitor ttop for 5 seconds and identify the hottest threads"
"Use bpfTrace bpfstacktop for 10 seconds to find on-CPU kernel hotspots"
"Use memoryAnalyze checkdup with SKIPEXMAPPED option"
"Run androidPerf perfetto with ANALYZEJANK on device 5af877f6"
"Use logAnalyze logkmsg for 5 seconds to show recent kernel messages"
```

---

## 2. Google Gemini Code Assist

### Option A: Gemini CLI (MCP)

```bash
# Install Gemini CLI
pip install gemini-cli
# or: npm install -g @google/gemini-cli

# Register guider MCP server
gemini mcp add guider python3 /home/iipeace/work/guider/mcp/guider-mcp.py

# Verify
gemini mcp list
```

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

# The REST server dispatches Gemini function calls to guider
# python3 openapi/guider-rest.py --port 8080

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

# Continue conversation with tool results...
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
python3 /home/iipeace/work/guider/openapi/guider-rest.py --port 8080

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

## Verification

```bash
cd /home/iipeace/work/guider

# 1. Catalog check
python3 -c "
import sys; sys.path.insert(0, 'mcp')
from guider_catalog import CATALOG
print('Total commands:', len(CATALOG))
print('First 5:', list(CATALOG.keys())[:5])
"

# 2. Adapter test (2-second ttop run)
python3 -c "
import sys; sys.path.insert(0, 'mcp')
from guider_adapter import GuiderAdapter
r = GuiderAdapter().run('ttop', duration=2)
print('ok:', r['ok'], '| duration_sec:', r['duration_sec'])
if isinstance(r.get('data'), dict):
    print('data keys:', list(r['data'].keys())[:5])
"

# 3. MCP server syntax check
python3 -m py_compile mcp/guider-mcp.py && echo 'guider-mcp.py: OK'
python3 -m py_compile mcp/guider_adapter.py && echo 'guider_adapter.py: OK'
python3 -m py_compile mcp/guider_catalog.py && echo 'guider_catalog.py: OK'

# 4. REST server check (requires fastapi)
# python3 -m py_compile openapi/guider-rest.py && echo 'guider-rest.py: OK'
```
