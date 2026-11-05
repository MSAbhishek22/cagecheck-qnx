# Patches — what changes in upstream CageCheck, and why

Upstream: https://github.com/MSAbhishek22/cagecheck (public, 13 files,
commit a5588ef, 3 Nov 2026). These patches are the porting layer's
other half: the minimal changes the upstream files need to run on QNX.
They are generated as real unified diffs and verified: each applies
cleanly with `patch -p1` to a fresh copy of upstream, and the upstream
test suite still passes 10/10 afterwards (see
tests/test_qnx_port.py::TestPatchesApplyAndPass, and the manual run
on 5 Nov 2026: patched tree 10/10 OK, 7/7 policy vectors OK, live
server smoke test OK).

Rule compliance: the Ports category requires "a new repository,
created during the Submission Period, containing your porting or
contribution work: the patches or porting layer, the QNX build files,
build and run instructions, and your documentation" and to
"reference the upstream project by URL rather than copying its
history" and "Do not submit a fork of the upstream project." This
scaffold follows exactly that shape: patches + layer + build files,
no upstream history copied.

| Patch | File | What it does |
|---|---|---|
| 001-cage-qnx-limits-and-aps-launch.patch | app/cage.py | Guards `import resource` (module presence on the QNX Python port is UNVERIFIED); `_limits()` returns None when unavailable; adds `_launch_prefix()` — `on -Xaps=<partition>` on QNX, empty on Linux. Linux behaviour unchanged. |
| 002-server-qnx-host-and-tier.patch | app/server.py | On QNX, default host becomes `0.0.0.0` (host browser reaches the QEMU target) and the default CAGE_TIER label becomes the honest QNX APS tier. Linux defaults unchanged. |
| 003-llm-qnx-local-explanation.patch | app/llm.py | On QNX with no inference keys, the explanation states it is a local explanation (no outbound call from the target). No behaviour change on Linux or when keys are set. |

QNX-only code paths in these patches are NOT runnable in this Linux
sandbox — they are code-reviewed, not executed. First QNX boot is the
verification point (BUILD_PLAN.md, Day 1 spike).
