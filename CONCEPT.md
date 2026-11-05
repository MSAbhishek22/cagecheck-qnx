# CONCEPT — CageCheck on QNX: the secret-leak guard, caged by a real-time OS

## The idea in one line

Port CageCheck (agent-code secret-leak guard) to QNX 8.0, and replace
its weakest link — a Linux process with `resource` rlimits — with the
thing QNX is actually for: **microkernel process isolation plus an
Adaptive Partitioning CPU budget**, so a malicious snippet physically
cannot starve the guard itself.

## Why this port, why this category

- **Category: Open-Source Contribution & Ports.** Upstream is the
  user's own public repo (https://github.com/MSAbhishek22/cagecheck,
  built 3 Nov 2026 for Vultr Agent Rush). The submission is a NEW
  repo created in the submission period holding only the patches,
  the porting layer, QNX build files, instructions and docs — exactly
  what the rules require. No fork, upstream referenced by URL.
- **The fit is real, not a relabel.** On Linux/Vultr the cage's
  honest limit is "process + patch isolation, NOT a container
  boundary". On QNX the boundary is the OS architecture itself:
  the snippet runner and the server are separate processes under a
  microkernel; a crashing runner restarts without taking the server
  down; APS guarantees the runner 5% CPU and no more. The port
  makes the product's core promise *stronger*, which is what a port
  should do — and it is a genuine entry for the "Best use of
  QNX-specific Technologies" $3,500 bonus.
- **Why QNX is the right foundation (judging: Potential Impact).**
  The exact places that run untrusted agent-written code — software-
  defined vehicles, medical devices, factory robots — are the places
  QNX already runs. A secret-leak guard that lives on the same RTOS
  as the system it protects, with deterministic timing (a check
  cannot be starved by the code it is checking), is a credible story
  for those markets. Timing determinism is the product reason QNX
  is chosen, not a logo.

## What the user gets

1. **CageCheck web UI served from QNX 8.0 in QEMU** — paste a
   snippet, get a PASSED / HELD / BLOCKED stamp + receipt, same as
   the Linux version. The host browser reaches it over QEMU
   networking; the demo video records that live session.
2. **QNX-native cage tier** — receipts say `qnx-aps-partition`
   instead of `local-process-patch`, and the receipt can cite the
   partition (`ap show cagecheck_snippet`) as evidence.
3. **A codelab** (stretch, for the $3,500 Best Codelab bonus):
   "Port a Python security tool to QNX 8.0 in an afternoon" — the
   porting layer + patches + QEMU notes, written as a runnable
   tutorial. Only if the core port lands first.

## What it is NOT

- Not a rewrite: ~460 lines of upstream Python, 3 small patches,
  one new package. The deterministic policy (`policy.py`) is
  untouched — it is pure `ast` and already portable.
- Not a fake QNX run: if QEMU cannot be booted, the submission
  says so and falls back to a labelled host-side build verification
  (see qemu/QEMU_NOTES.md). No screenshot video, ever.
- Not a Vultr resubmission: the Vultr track keeps its Docker
  boundary; this track's boundary is QNX APS. Different product
  claim, different evidence.

## Judging-criteria mapping

| Criterion | How this entry answers it |
|---|---|
| Technological Implementation | Real port: patches apply, tests pass, server runs on QNX 8.0 QEMU; APS + abilities are QNX-native, not a README mention. |
| Design | Distinct "timing console" identity (see design/DESIGN_CONSTITUTION.md); 3D microkernel message-passing view of the cage. |
| Potential Impact | Secret-leak guard for agent-written code on safety-critical QNX systems (auto/medical/robotics) — QNX's actual markets. |
| Innovation & AI Creativity | The guard that cannot be starved by what it guards: APS budget + microkernel isolation as the enforcement mechanism. |
