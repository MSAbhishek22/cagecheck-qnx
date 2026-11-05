# QNX Global Hackathon — CageCheck on QNX

**Status: IN_PROGRESS — prep + verified scaffold. NOT submitted,
NOT registered, NOT run on QNX yet. Prep + build only; no account,
registration, submission or posting was done.**

## The track (verified 5 Nov 2026 from https://qnx.devpost.com/)

- **QNX Global Hackathon**, sponsor BlackBerry Ltd (QNX), via Devpost.
- **Deadline: Wed 16 Dec 2026 00:30 IST** (15 Dec 2026 14:00 ET).
  Safe internal target: **Sun 14 Dec 2026 20:00 IST**.
- **Prizes: $50,000+** — Grand $10,000; category Best $4,000;
  Runner-up $2,000; Honorable Mention $1,000 ×3; Best Codelab $3,500;
  Best use of QNX-specific Technologies $3,500; Community Choice
  (swag/feature).
- **Eligibility: 18+, solo OK, India eligible** (India is NOT in the
  rules' excluded-country list). Free — QNX SDP 8.0 via QNX Everywhere
  (non-commercial licence, myQNX account). No hardware needed — QEMU
  works (Quick Start Target Image for QEMU / Developer Desktop).
- **Category: Open-Source Contribution & Ports.** Requires a NEW repo
  created in the submission period with the patches/porting layer,
  QNX build files, instructions + docs; upstream referenced by URL,
  NOT a fork. Demo video < 3 min, public YouTube, showing the project
  functioning on the target.
- ⚠️ **Winners announced on/around Fri 5 Feb 2027 00:30 IST**
  (judging 15–29 Jan 2027) — **AFTER the Dec 2026 goal window.**
  This is a long-tail entry, not December cash. Flagged honestly;
  do not count it toward the $20,000-before-Dec-2026 goal.

## The concept

Port CageCheck (agent-code secret-leak guard) to QNX 8.0, and replace
its weakest link — a Linux process with rlimits — with what QNX is
for: microkernel process isolation + an Adaptive Partitioning 5% CPU
budget, so a malicious snippet cannot starve the guard checking it.
Full rationale: CONCEPT.md. Architecture: ARCHITECTURE.md.

## What is in this scaffold

| Path | What it is |
|---|---|
| RESEARCH.md | Verified rules/prizes/deadline/eligibility + QNX port-path research + 8 open questions for first boot |
| CONCEPT.md | Concept, why it wins, judging-criteria mapping |
| ARCHITECTURE.md | System shape, module map, enforcement layers |
| BUILD_PLAN.md | Dated plan 5 Nov → 15 Dec, critical path, QEMU-failure fallback |
| STATUS.md | Honest release card + gate status (IN_PROGRESS) |
| design/DESIGN_CONSTITUTION.md | "Timing console" identity — light blueprint schematic, distinct from CageCheck/Digest Room/Spec Ghost |
| design/PROJECT_DESIGN_REGISTRY.md | Comparison vs 3 most recent projects |
| src/qnx_cage/ | NEW porting layer: platform_detect, aps (APS command builders), qnx_limits (Linux rlimit backend verified + QNX APS backend), verify_upstream |
| patches/001–003 | Real unified diffs vs upstream cage.py/server.py/llm.py — apply cleanly, patched tree stays 10/10 |
| tests/test_qnx_port.py | 13/13 PASS in this sandbox |
| qnx/ | Makefile (stage/install/check), mkifs buildfile (DRAFT), run-on-qnx.sh |
| qemu/QEMU_NOTES.md | Official QSTI path, networking, fallback if QEMU fails |
| submission/SUBMISSION_DRAFT.md | Draft only — nothing submitted |

## What was verified here (Linux sandbox, Python 3.12.3, 5 Nov 2026)

- Upstream CageCheck suite 10/10; patched tree 10/10; policy
  vectors 7/7; live patched-server smoke test green.
- Port suite 13/13 (APS command strings, rlimit enforcement in a
  child, QNX backend refuses off-target, patches apply cleanly).
- No QEMU in this sandbox, no QNX image/SDP — **no QNX run is
  claimed anywhere in this scaffold.**

## What still needs the user's own taps (in order)

1. myQNX account + free QNX Everywhere licence (qnx.software).
2. Install SDP 8.0 on the host (Windows/Linux) + QSTI for QEMU;
   boot the QEMU image. Start by **Fri 7 Nov** — Phase 1 is the
   bottleneck.
3. Day-1 spike on target: answer RESEARCH.md §5 open questions.
4. Create the NEW submission repo + push (his GitHub session).
5. Devpost registration + submission (his browser tap) by
   Sun 14 Dec 20:00 IST; video from the live QEMU URL (< 3 min,
   public YouTube) — recorded only after the port runs on QEMU.
