# ARCHITECTURE — CageCheck-on-QNX

## System shape (QNX target, QEMU)

```
Host browser ──(QEMU net, guest IP:8766)──► QNX 8.0 (QEMU)
                                              │
                                   ┌────────────┴────────────┐
                                   │ CageCheck server (Python)
                                   │  ThreadingHTTPServer
                                   │  GET /  /health  /receipts
                                   │  POST /api/check  /api/approve
                                   └────────────┬────────────┘
                                              │ policy scan (ast, pure)
                                              │ BLOCKED → receipt, no run
                                              │ CLEAN/HELD → run in cage
                                              ▼
                                   ┌─────────────────────────┐
                                   │ Snippet runner (Python) │
                                   │  separate process       │
                                   │  APS partition          │
                                   │  "cagecheck_snippet"    │
                                   │  5% CPU budget, 0 crit  │
                                   │  + POSIX rlimits if the │
                                   │    QNX Python port has  │
                                   │    the `resource` module│
                                   └─────────────────────────┘
                                              │
                                   receipts → runs/audit.jsonl
```

## Module map

| File | Origin | QNX change |
|---|---|---|
| app/policy.py | upstream, untouched | none — pure `ast`, portable as-is |
| app/receipts.py | upstream, untouched | none — stdlib only |
| app/llm.py | upstream + patch 003 | QNX-aware local explanation text |
| app/server.py | upstream + patch 002 | HOST default 0.0.0.0 on QNX; QNX tier label |
| app/cage.py | upstream + patch 001 | `resource` import guard; `_launch_prefix()` → `on -Xaps=<partition>` |
| app/index.html | upstream, restyled | new "timing console" identity (see design/) |
| src/qnx_cage/platform_detect.py | NEW (this scaffold) | `is_qnx()` via uname; summary for receipts |
| src/qnx_cage/aps.py | NEW (this scaffold) | APS command builders (setup/launch/show/destroy) |
| src/qnx_cage/qnx_limits.py | NEW (this scaffold) | LinuxRlimitBackend (verified) + QnxApsBackend (on-target) |
| src/qnx_cage/verify_upstream.py | NEW (this scaffold) | baseline check, read-only import of upstream |
| qnx/cagecheck-qnx.build | NEW (this scaffold) | mkifs buildfile — DRAFT, verify on target |
| qnx/Makefile | NEW (this scaffold) | stage/install/check packaging |
| qnx/run-on-qnx.sh | NEW (this scaffold) | target startup: APS setup + server |

## Enforcement layers on QNX (strongest first)

1. **Microkernel process isolation** — runner and server are
   separate processes; a runner crash cannot take the server down.
2. **Adaptive Partitioning** — runner launched with
   `on -Xaps=cagecheck_snippet` into a 5% CPU budget partition
   (`aps modify -s recommended` locks scheduler changes to the
   System partition). A runaway snippet gets 5% and no more.
3. **POSIX rlimits** — RLIMIT_CPU 5 s / AS 256 MiB / FSIZE 1 MiB,
   applied when the QNX Python port provides `resource` (UNVERIFIED).
4. **Static policy first** — the deterministic `ast` scan still runs
   before any execution; BLOCKED never reaches the runner.
5. **Runner-internal patching** — restricted import hook, cage-only
   `open()`, blocked socket/subprocess, scrubbed env (unchanged
   from upstream).

## What the Linux sandbox verified vs what needs the target

VERIFIED HERE (5 Nov 2026, Python 3.12.3):
- Upstream suite 10/10; patched tree 10/10; policy vectors 7/7;
  live patched-server smoke test (BLOCKED receipt for SSH read);
  port suite 13/13 (APS strings, rlimit child enforcement,
  QNX backend refuses off-target, patches apply cleanly).
VERIFY ON TARGET (first QNX boot):
- Python version, `resource` module, `subprocess`+`preexec_fn`;
  `ap`/`aps`/`on` flags on SDP 8.0; QEMU networking; mkifs build;
  the restyled UI served from the target; the <3 min video.

## Stretch (only after the core port runs on QEMU)

- **procmgr abilities:** a tiny C helper (or ctypes, if the QNX
  Python port ships it) that drops the runner's abilities after
  startup — e.g. deny creating further executable mappings
  (`procmgr_ability()`). This is the second QNX-specific-technology
  story; it is NOT in the core path because it needs a compiled
  helper and target verification.
- **Codelab** for the $3,500 bonus, written from the real port log.
