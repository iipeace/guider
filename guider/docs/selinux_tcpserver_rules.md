# SELinux Rules for guider ctop TCPSERVER Full Command Support

This document maps everything required to expose all guider commands through the
TCPSERVER socket (port 55555) that the `ctop` service opens on boot. Two distinct
layers must both be cleared, so the document is structured in that order.

1. **Section A — Application layer**: guider.py's own TCPSERVER command allowlist.
   Commands absent from this list are rejected immediately, regardless of SELinux
   or root privileges.
2. **Section B — OS layer**: SELinux rules the `guider` domain needs when allowlisted
   commands access kernel resources (BPF, tracefs, ptrace, AF_CAN, etc.).
3. **Section C**: Items that cannot be fixed by SELinux rules alone (kernel config,
   hardware absence, etc.). Note: neverallow constraints are not a barrier on this
   device — see Section F.
4. **Section D**: Verification procedure using an adb-connected device, no build required.
5. **Section E**: Actual AVC denial data collected from a live device (2026-09-11).
6. **Section F**: D step 5 — static policy vs. live denial cross-check; final
   classification of each requirement as (a)/(b)/(c).

> **Bottom line first**: Even with a perfectly open SELinux policy, `top`, `ttop`,
> `mtop`, `vtop`, `disktop`, `irqtop`, `oomtop`, `trtop`, `btop`, `ktop`,
> `funcrec`, `perfetto`, `andtop`, `checkdup`, `leaktop`, `logkmsg`, `logdlt`,
> `logjrl`, `convlog`, and `bpfbinderlat` cannot be invoked via TCPSERVER.
> Enabling them requires a **code change** — adding the command literal to the
> `_handleCmd` allowlist tuple at `guider.py:81691-81780`. That is outside the
> scope of this SELinux analysis.

## 0. Current State

- `guider.rc` (repo root):
  ```
  service guider /vendor/bin/guider ctop -i 3 -o /data/guider \
      -q TEXTREPORT,NOSOCKPROF,LIMITREPDIR:200M,TCPSERVER:55555,OPSLOG:a,NOTEMPER,NOUSBINFO \
      -b 10M -e dC -C /vendor/etc/guider/guider.conf
  class main
  user root
  group system log readproc
  disabled
  ```
  TCPSERVER is **already enabled**. There is no `seclabel` line, so the SELinux
  domain is determined by the `file_contexts` mapping for `/vendor/bin/guider` in
  the device vendor tree.
- `guider/boot.json` (boot capture): records `Security: u:r:vendor_guider:s0`.
- ⚠️ **Domain mismatch confirmed on live device (see Section E)**: On device
  5af877f6, the running process (pid 8906) shows context **`u:r:guider:s0`** —
  not `vendor_guider`. Furthermore, static policy analysis (Section F) confirms
  `vendor_guider` is **not defined** in this compiled policy at all. **All allow
  rules in Section B and the `.te` file use the domain name `guider`.**
- Because guider runs as `root`, DAC (traditional UNIX permissions) is already
  bypassed, but SELinux MAC is a separate layer — resources not permitted in the
  `guider` domain are still blocked with `avc: denied`.
- TCPSERVER authentication (`runServerTask`, `guider.py:94382`) uses
  `AUTHCOMM`/`AUTHCMDLINE`/`AUTHUSER`/`AUTHGROUP`/`AUTHGROUPS` options at the
  application layer and is unrelated to SELinux. If none of these options are set,
  the default is "anyone who connects is authenticated." `AUTHKEY` (shared secret)
  exists in code as a TODO and is not implemented.
- **Note**: The 10 MCP tools supported by `mcp/guider_catalog.py` and
  `mcp/guider-mcp.py` (Claude Code integration) fork a **new process** per call
  via `adb shell ... python3 guider.py <CMD>` — a completely separate path from
  the persistent TCPSERVER socket that ctop holds open. The MCP layer's
  `BLOCKED_COMMANDS`/`BLOCKED_OPTS` (`mcp/guider_catalog.py`) do not apply to
  the TCPSERVER path this document covers.

## A. TCPSERVER Command Allowlist (independent of SELinux)

`_handleCmd` (`guider.py:81494`) checks whether the command is in the hardcoded
tuple at `guider.py:81691-81780`, or matches `isDrawMode` (visualization commands),
before executing anything. Commands not in this list are rejected with
`"no support '%s' command"` followed by `sys.exit(-1)`.

```python
# guider.py:81694-81777 (actual literals)
andcmd, bdmon, bdtop, bgkill, bpfblktop, bpfdroptop, bpfnetlat, bpfpktsnoop,
bpfpkttop, bpfrunqtop, bpfstacktop, bpfsyscalltop, bpftcplat, bpftcplife,
bpftcpretrans, bpfwaittop, bugrec, bugrep, cantop, cansnoop, control, cpuprof,
cputest, dir, dirlist, disablepkglist, download, dump, dumpfile, enablepkglist,
event, funcall, funcschema, getactlist, getappstat, getconf, getdumplist,
getpeak, getpermlist, getpkg, getpkgattr, getpkginfo, getpkglist,
getpkglistinfo, getprop, getsettings, gfxmon, gfxtop, iotest, jobs, kill,
logcat, logmon, memmon, memprof, memtest, memtop, ntop, overlay, printboot,
ps, pslist, remove, resmon, ressum, restop, restopsum, run, runpkglist, save,
savemin, saveraw, scrcap, screeninfo, scrrec, setprop, setsettings,
stoppkglist, sysdump, sysinfo, syslist, taskresmon, tkill, updateconf
```

Two commands are aliased internally (`guider.py:82462-82464`):
`memprof` → runs `hprof` internally; `cpuprof` → runs `sperf` internally.

Cross-referencing against `mcp/guider_catalog.py` (canonical command names):
(The table covers CLAUDE.md Quick Tool Reference commands; the catalog also contains
`atop`, `wtop`, `bpftop`, `bpfsnoop`, `bpfexectop`, `bpflocktop`,
`bpfbindersnoop`, `irqlattop`, `tptop`, `utop`, `strace`, `logsys`, `dlttop`
and dozens more — all equally absent from the allowlist and therefore unreachable
via TCPSERVER.)

| CLAUDE.md Category | Commands | TCPSERVER Support |
|---|---|---|
| systemMonitor | top, ttop, mtop, vtop, disktop, irqtop, oomtop | ❌ none |
| bpfTrace | bpfstacktop, bpfsyscalltop, bpfrunqtop | ✅ present |
| bpfTrace | bpfbinderlat | ❌ absent |
| ftraceProfile | trtop, btop, ktop, funcrec | ❌ none |
| networkTrace | bpftcpretrans, bpftcplife, bpfdroptop, bpftcplat | ✅ present |
| networkTrace | ntop | ✅ present |
| androidPerf | bdtop, cantop | ✅ present |
| androidPerf | hprof | 🟡 reachable via `memprof` alias |
| androidPerf | perfetto, andtop | ❌ absent |
| memoryAnalyze | dump, sysdump | ✅ present |
| memoryAnalyze | checkdup, leaktop | ❌ absent |
| visualize | drawflame, drawcpu, drawscatter, drawhist, etc. | ✅ all pass via `isDrawMode` |
| logAnalyze | logkmsg, logdlt, logjrl, convlog | ❌ none |

`resmon`/`restop`/`ressum`/`restopsum`/`taskresmon` are in the allowlist and
internally reuse top-style display logic (code contains `main("top" + addOpt)`
calls), but they are not full replacements for the ❌ commands above.

**Items marked ❌ are not subject to the SELinux discussion in Sections B/C** —
they are blocked before SELinux is ever consulted, and unlocking them requires a
code change to `guider.py:81691-81780`.

## B. SELinux Rule Matrix for Allowlisted Commands

> Rules in this table were initially estimated from guider.py syscall/file-path
> analysis and AOSP sepolicy conventions. Section F (D step 5) cross-checks them
> against the compiled policy from device 5af877f6 and updates each row's
> classification.
>
> Key finding from static analysis: this device's compiled policy has **no
> neverallow rules** covering `capability2:bpf`, `can_socket`, `perf_event`, or
> `debugfs_tracing` for the `guider` domain. All of these are therefore in class
> (a) — addable. See Section F for the full classification table.

| Category (in allowlist) | Required resources (code reference) | `guider` rules needed | Classification |
|---|---|---|---|
| bpfblktop / bpfdroptop / bpfnetlat / bpfpkttop·pktsnoop / bpfrunqtop / bpfstacktop / bpfsyscalltop / bpftcplat·life·retrans / bpfwaittop | `bpf()` syscall (`BpfMgr.bpfSyscall`, `guider.py:122132`; `BPF_MAP_CREATE` L122163, `BPF_PROG_LOAD` L122210), kprobe/tracefs access, CAP_BPF or CAP_SYS_ADMIN, kernel ≥5.8 | `allow guider self:capability2 { bpf perfmon };`<br>`allow guider fs_bpf:dir { read search write add_name };`<br>`allow guider fs_bpf:file { read write open getattr map };`<br>`allow guider debugfs_tracing:dir { read open search };`<br>`allow guider debugfs_tracing:file { read open write };` | **(a)** No neverallow; live denial not yet collected (see Section E) |
| cantop / cansnoop | `AF_CAN` (=29) raw socket, `SOCK_RAW`/`CAN_RAW` (`guider.py:155893` cantop, `156502` cansnoop) | `allow guider self:can_socket { create bind read write setopt };` | **(a)** No neverallow; hardware/kernel prerequisite remains (Section C #3) |
| dump / dumpfile / sysdump | Standard `/proc/<pid>/maps,smaps`, filesystem stat | See Section F — several denials confirmed (E절) | **(a)** All confirmed denials are addable |
| memprof(→hprof) / cpuprof(→sperf) | perf profiling, `perf_event_open()` wrapper (`SysMgr.openPerfEvent`, `guider.py:79302`). Also: `traced_perf_socket` path already permitted (see below) | `allow guider self:perf_event { open cpu kernel };` (new-style); or `allow guider self:capability { sys_admin };` (old-style) | **(a)** No neverallow. Note: `traced_perf_socket:sock_file write` + `traced_perf:unix_stream_socket connectto` already allowed — perfetto-based perf path is usable without extra rules |
| bdmon / bdtop | Block device I/O stats (`/proc/diskstats` already allowed, `/sys/block/*`) | `allow guider sysfs_block:dir { read search };`<br>`allow guider sysfs_block:file { read open getattr };` | **(a)** No neverallow; `proc_diskstats` already permitted |
| scrrec / scrcap / bugrec / bugrep | Screen capture / bug report trigger | Likely needs SurfaceFlinger socket/binder permissions. Note: `surfaceflinger:binder { call transfer }` and `surfaceflinger_service:service_manager find` already allowed — may reduce extra rules needed | **(a)** Enumerate remaining denials via Section D |
| gfxmon / gfxtop | Graphics performance stats | `surfaceflinger:binder { call transfer }` + `surfaceflinger_service:service_manager find` already allowed — may be sufficient | **(a)** Enumerate remaining denials via Section D |
| resmon / restop / ressum / restopsum / taskresmon | Reuses top-style logic internally, `/proc` reads | Mostly covered by existing root domain grants | **(a)** Likely no additional rules needed |
| Visualization (`isDrawMode`: drawflame, etc.) | Local file I/O (`-I` input file) | No additional rules likely needed unless the input file is owned by another domain | **(a)** No additional rules expected |

## C. Items That Cannot Be Fixed by SELinux Rules Alone

> **Correction from initial draft**: The original Section C #1 claimed BPF
> `capability2` permissions were blocked by `neverallow` and structurally
> impossible to add. Static analysis of the compiled policy from device 5af877f6
> found **no such neverallow**. All BPF-related rules are in class (a) — addable
> on this device. The caveat below about other devices remains valid.

1. **BPF commands — device-dependent**: On this device (5af877f6), there are no
   neverallow constraints on `capability2:{bpf, perfmon}` or `fs_bpf`, so rules
   can be added. On other devices or stock AOSP builds, these permissions are often
   restricted to `bpfloader`/`netd` and protected by `neverallow` — adding them
   to `guider` would fail at policy compile time on those devices. Always run
   `sesearch --neverallow` on the target device's compiled policy first.
2. **ftrace/tracefs, debugfs** — `user` builds frequently disable `CONFIG_DEBUG_FS`
   or omit a tracefs mount entirely. The filesystem not being present makes SELinux
   rules irrelevant.
3. **CAN bus (cantop/cansnoop)** — Requires SocketCAN kernel support
   (`CONFIG_CAN`) and a physical CAN transceiver/interface. SELinux can only permit
   access to an interface that already exists.
4. **perf_event_open family** — Depends on the `kernel.perf_event_paranoid` sysctl
   and `CONFIG_PERF_EVENTS`. Even with SELinux permission, a disabled kernel
   feature means nothing works.
5. **`/proc` hidepid mount option** — A mount-namespace-level control, separate from
   SELinux. Currently not a problem because guider runs as root (euid 0), but
   shrinking capabilities in the future could expose this.
6. **(Non-SELinux risk, noted for completeness) TCPSERVER has no default
   authentication** — Without `AUTHCOMM`/`AUTHUSER` options set, anyone who can
   reach port 55555 can invoke allowlisted commands. Broadening SELinux access
   amplifies this risk. Configuring at least `AUTHCOMM` or `AUTHUSER` is
   recommended alongside any SELinux expansion (out of scope for this document).

## D. Verification Procedure (no device build required)

Because the vendor sepolicy source tree was unavailable via opengrok, the primary
verification source is the **compiled policy pulled directly from the adb device**.

### Steps that require no device modification

1. `adb devices`, then `adb shell getprop ro.build.type` / `ro.debuggable`,
   `adb shell getenforce` — confirm device type and SELinux enforcement mode.
2. Validate Section A: send allowlisted commands (e.g. `bpfstacktop`, `cantop`,
   `bdtop`, `dump`) to TCPSERVER and confirm ACK; send an absent command (e.g.
   `top`) and confirm `"no support"` rejection — verify the code analysis against
   the live device.
3. Pull the compiled policy:
   `adb pull /vendor/etc/selinux/precompiled_sepolicy` (adjust path if needed —
   try `plat_sepolicy.cil`/`vendor_sepolicy.cil`). On the host, run
   `sesearch`/`sepolicy-analyze` (setools package: `apt install setools`) to query
   existing allow rules and relevant `neverallow` constraints for the `guider`
   domain. This cross-validates Sections B/C without any build or device change.
4. Execute commands from the Section B matrix one at a time, then collect:
   `adb shell logcat -b all -d | grep avc:` (or `adb shell dmesg | grep avc:` if
   logd drops entries). Even in Enforcing mode, denials are always logged.
5. Map step-3 (static policy) against step-4 (live denial) to classify each
   requirement as:
   - (a) fixable by adding an allow rule
   - (b) structurally blocked by `neverallow` — cannot be fixed in this domain
   - (c) irrelevant due to missing kernel feature or hardware
   
   **Status**: Completed for device 5af877f6. Results in Section F.

### Steps that modify device state — confirm separately before running

6. On userdebug/eng builds, to force-collect BPF/CAN/perf denials:
   `adb root` → (if needed) `adb disable-verity && adb reboot` → `adb root &&
   adb remount` → `adb shell setenforce 0` (global permissive). Run the full
   Section B matrix and treat the remaining avc audit entries as the "final
   required rule list." **This step involves disable-verity and reboot — confirm
   before executing.**
7. To permanently embed rules, a partial build (`m selinux_policy`) is sufficient
   without a full image rebuild — much faster than a complete AOSP build.

## E. Live Device AVC Denial Collection (2026-09-11)

### Test environment

| Field | Value |
|---|---|
| Device serial | 5af877f6 |
| Build type | userdebug |
| SELinux mode | Enforcing |
| guider pid | 8906 |
| Actual SELinux context | **`u:r:guider:s0`** (differs from boot.json `vendor_guider`) |

### Domain mismatch root cause

`boot.json` was captured on an earlier build. Static policy analysis (Section F)
confirms `vendor_guider` is **not defined** in the current compiled policy —
`sesearch --allow -s vendor_guider` returns "vendor_guider is not a valid type
attribute." The device's `file_contexts` has been updated to map
`/vendor/bin/guider` to the `guider` type. All rules in this document and in
`sepolicy/vendor_guider_tcpserver.te` use `guider`.

### Confirmed blocking denials (permissive=0, collected via logcat + dmesg)

```
# audit2allow format — scontext=u:r:guider:s0

# TCPSERVER nc connection (GuiderTCPReceiv thread)
allow guider fwmarkd_socket:sock_file { write };

# ctop continuous /proc/<pid> scan for processes owned by other vendor domains
allow guider vendor_hal_keymint_qti:dir { search getattr };
allow guider tee:dir { search getattr };
allow guider vendor_agmservice_qti:dir { search getattr };

# dump/sysdump command — filesystem metadata access
allow guider bt_firmware_file:filesystem { getattr };
allow guider mnt_product_file:dir { search };
allow guider mnt_vendor_file:filesystem { getattr };
allow guider dropbox_data_file:dir { getattr };
allow guider anr_data_file:dir { getattr };
```

The `/proc` scan entries above represent only the vendor processes running during
the short collection window. Long-term operation or additional command runs will
surface more vendor domain `dir { search getattr }` denials.

### Denials NOT observed (BPF / AF_CAN / perf_event)

Commands `bpfstacktop`, `cantop`, `bdtop`, and `memprof` were sent via TCPSERVER
and received ACK, but **no `capability2:bpf`, `can_socket`, or `perf_event`
denials appeared in the `guider:s0` domain.** Two plausible explanations:

1. **Internal software check**: guider.py checks BPF/CAN/perf availability at the
   Python level before making the syscall. If the check fails, the syscall is never
   issued and SELinux is never reached. ACK means the command was received, not
   that it executed successfully.
2. **`su` subprocess path**: A `capability2:bpf` denial was observed from
   `u:r:su:s0 permissive=1` — suggesting bpfstacktop may spawn a child process in
   the `su` context for the actual BPF syscalls.

Section D step 6 (`setenforce 0`) is needed to force-collect these denials.

### nc command format caveat

The TCPSERVER parser does not strip newlines before comparing the received bytes
to the allowlist tuple. Sending `printf 'cantop\n'` delivered `cantop` followed by
an actual newline byte (0x0A); the server reported `"no support 'cantop\n'"` —
showing the newline as a literal in the error — and rejected the command that is
otherwise present in the allowlist.

```bash
# printf sends a real newline (0x0A) after the command
printf 'bpfstacktop\n' | nc -w 5 127.0.0.1 55555
```

If the server does not strip 0x0A on input, the guider.py `_handleCmd` parser
needs a `.strip()` call on the received command string to behave correctly.

## F. D Step 5 — Static Policy vs. Live Denial Cross-Check (2026-09-11)

Source: `sesearch` against `/tmp/precompiled_sepolicy` (pulled from device 5af877f6).

### Key static findings

- `vendor_guider` type: **not defined** in this policy.
- `guider` domain: 381 direct allow rules. Already permitted notably:
  - `traced_perf_socket:sock_file write` + `traced_perf:unix_stream_socket connectto`
  - `heapprofd_socket:sock_file write` + `heapprofd:unix_stream_socket connectto`
  - `surfaceflinger:binder { call transfer }` + `surfaceflinger_service:service_manager find`
  - `proc_diskstats`, `proc_meminfo`, `proc_stat`, `proc_net_tcp_udp`
  - `sysfs_thermal:dir/file/lnk_file { read ... }`
  - `cgroup`/`cgroup_v2:dir/file { read write ... }`
- **No neverallow** covering `capability2:bpf`, `can_socket`, `perf_event`,
  `debugfs_tracing`, or `fs_bpf` for the `guider` domain.

### Classification table

| Requirement | Static policy | Live denial (Section E) | Class | Rule to add |
|---|---|---|---|---|
| `fwmarkd_socket:sock_file write` | absent; many similar domains allowed | ✅ confirmed permissive=0 | **(a)** | `allow guider fwmarkd_socket:sock_file { write };` |
| `vendor_hal_keymint_qti:dir { search getattr }` | `file read` present; `dir` absent | ✅ confirmed | **(a)** | `allow guider vendor_hal_keymint_qti:dir { search getattr };` |
| `tee:dir { search getattr }` | `file read` present; `dir` absent | ✅ confirmed | **(a)** | `allow guider tee:dir { search getattr };` |
| `vendor_agmservice_qti:dir { search getattr }` | `file read` present; `dir` absent | ✅ confirmed | **(a)** | `allow guider vendor_agmservice_qti:dir { search getattr };` |
| `bt_firmware_file:filesystem getattr` | `firmware_file:filesystem getattr` present; `bt_firmware_file` absent | ✅ confirmed | **(a)** | `allow guider bt_firmware_file:filesystem { getattr };` |
| `mnt_product_file:dir search` | absent | ✅ confirmed | **(a)** | `allow guider mnt_product_file:dir { search };` |
| `mnt_vendor_file:filesystem getattr` | `dir { getattr search }` present; `filesystem` absent | ✅ confirmed | **(a)** | `allow guider mnt_vendor_file:filesystem { getattr };` |
| `dropbox_data_file:dir getattr` | absent | ✅ confirmed | **(a)** | `allow guider dropbox_data_file:dir { getattr };` |
| `anr_data_file:dir getattr` | absent | ✅ confirmed | **(a)** | `allow guider anr_data_file:dir { getattr };` |
| `capability2 { bpf perfmon }` | absent; **no neverallow** | ⬜ not yet collected | **(a)** | `allow guider self:capability2 { bpf perfmon };` |
| `fs_bpf:dir/file` | absent; bpfloader/gpuservice allowed; **no neverallow** | ⬜ not yet collected | **(a)** | `allow guider fs_bpf:dir { read search write add_name };`<br>`allow guider fs_bpf:file { read write open getattr map };` |
| `debugfs_tracing:dir/file` | absent; atrace/shell/profcollectd allowed; **no neverallow** | ⬜ not yet collected | **(a)** | `allow guider debugfs_tracing:dir { read open search };`<br>`allow guider debugfs_tracing:file { read open write };` |
| `self:can_socket` | absent; **no neverallow** | ⬜ not yet collected | **(a)** + **(c)** HW | `allow guider self:can_socket { create bind read write setopt };` |
| `self:perf_event` | absent; **no neverallow**; `traced_perf` path already open | ⬜ not yet collected | **(a)** | `allow guider self:perf_event { open cpu kernel };` |
| `sysfs_block:dir/file` | absent (general `sysfs` present); **no neverallow** | ⬜ not yet collected | **(a)** | `allow guider sysfs_block:dir { read search };`<br>`allow guider sysfs_block:file { read open getattr };` |

**Legend**: ✅ confirmed by live avc denial · ⬜ static analysis only, live denial pending · **(a)** addable rule · **(c)** additional kernel/HW prerequisite

All items are class **(a)**. No class **(b)** (neverallow-blocked) items were found on this device.

> **Action item**: Run Section D step 6 (`setenforce 0`) to collect BPF/CAN/perf
> live denials and confirm the ⬜ rows above.

## Related Files

- `guider.rc` — current ctop/TCPSERVER boot configuration
- `guider/boot.json` — original domain capture (`u:r:vendor_guider:s0`)
- `guider/guider.py`
  - `runServerTask` (L94382) — TCPSERVER accept / application-layer auth
  - `_handleCmd` (L81494, allowlist L81691-81780, aliases L82462-82464)
  - `class BpfMgr` (L121991), `BpfMgr.bpfSyscall` (L122132),
    `BPF_MAP_CREATE` (L122163), `BPF_PROG_LOAD` (L122210)
  - `SysMgr.mountFsCmd` (L90713), `SysMgr.getTracefsPath` (L111651)
  - AF_CAN socket (L155893 cantop, L156502 cansnoop)
  - PTRACE constants (`PTRACE_PEEKTEXT` L6249, `PTRACE_ATTACH` L6262)
  - `/dev/kmsg` access (`SysMgr.kmsgPath` L49640)
  - `SysMgr.getEnforce` (L38796), `AndroidMgr.getSelinuxEnforce` (L40469)
  - `SysMgr.openPerfEvent` (L79302)
- `mcp/guider_catalog.py` — canonical command name list (allowlist cross-reference)
- `sepolicy/vendor_guider_tcpserver.te` (same directory) — allow-rule draft
  updated to reflect Section F classification
