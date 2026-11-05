# SUBMISSION DRAFT — QNX Global Hackathon (DO NOT SUBMIT — prep only)

Category: **Open-Source Contribution & Ports**
Upstream: https://github.com/MSAbhishek22/cagecheck
Submission repo: (TO BE CREATED — new repo in the submission period;
user's tap. Must contain: patches/, src/qnx_cage/, qnx/, qemu/,
docs, MIT LICENSE. Must NOT be a fork of upstream.)

## Title (draft)

CageCheck on QNX — the secret-leak guard, caged by a real-time OS

## Description (draft, < Devpost limits; finalise after the QNX run)

CageCheck checks AI-suggested code for secret leaks before it is
pasted into a repo: a deterministic policy scan (secret paths, secret
env, subprocess, network) plus a runtime cage, with a signed receipt
for every check. This port moves it to QNX 8.0 — and makes the cage
stronger than it was on Linux. On Linux the cage is a process with
rlimits; on QNX the snippet runner is a separate process under the
microkernel, launched into an Adaptive Partitioning partition with a
5% CPU budget (`on -Xaps=cagecheck_snippet`), so a malicious snippet
cannot starve the guard that is checking it. The policy engine is
pure Python `ast` and ports unchanged; the port is three small
patches plus a porting layer.

Evidence of QNX use (for reviewers): `src/qnx_cage/aps.py` (APS
command builders), `qnx/cagecheck-qnx.build` (mkifs buildfile),
`qnx/run-on-qnx.sh` (APS setup + server start), receipts stamped
with cage tier `qnx-aps-partition`, and the demo video showing the
server running on QNX 8.0 in QEMU with `ap show` output.

## Build & run instructions (draft — finalise after first QNX boot)

- QNX version: QNX SDP 8.0 (QNX Everywhere, free non-commercial).
- Target: QEMU x86_64 (Quick Start Target Image for QEMU).
- Toolchain: SDP 8.0 + Python on the target (version TBD on first
  boot — see RESEARCH.md open questions).
- Steps: apply patches/ → `make stage` → scp to /opt/cagecheck-qnx
  → `sh run-on-qnx.sh` → open http://<guest-ip>:8766/ from the host.

## Video

< 3 min, public YouTube, recorded from the live QEMU target URL.
NOT YET RECORDED — recording happens only after the port runs on
QEMU (rulebook Gate F). Never from screenshots.

## Checklist before submitting

- [ ] Port runs on QNX 8.0 QEMU (10/10 upstream tests on target)
- [ ] APS partition evidence captured (`ap show` output in video)
- [ ] New submission repo created + pushed (user's tap)
- [ ] Restyled UI + interaction inventory done (qa/)
- [ ] Video recorded from live target URL, uploaded Public
- [ ] Devpost registration + form (user's tap) by Sun 14 Dec 20:00 IST
- [ ] Optional: codelab URL for Best Codelab bonus; PR URL if opened
