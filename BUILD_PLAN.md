# BUILD PLAN — CageCheck-on-QNX (5 Nov → 15 Dec 2026)

**Deadline: Wed 16 Dec 2026 00:30 IST** (15 Dec 2026 14:00 ET).
**Safe internal target: Sun 14 Dec 2026 20:00 IST** (submit a day
early; Devpost edits are allowed until the deadline, but a day of
slack is worth more than a day of polish).
**Winners: on/around Fri 5 Feb 2027 00:30 IST** — AFTER the Dec 2026
goal window. This track is a long-tail entry, not December cash.

## Done (5 Nov 2026, this scaffold)

- [x] Rules/categories/prizes/deadline/eligibility verified from
      official Devpost pages (RESEARCH.md).
- [x] Port-path research: QNX Everywhere, SDP 8.0, QEMU QSTI,
      Developer Desktop, APS/procmgr, mkifs buildfile format.
- [x] Upstream baseline verified: 10/10 tests on Linux.
- [x] Porting layer `src/qnx_cage/` (detection, APS builders,
      limit backends, upstream verifier) — 13/13 port tests pass.
- [x] Three real patches (001/002/003) — apply cleanly, patched
      tree stays 10/10 + live smoke test green.
- [x] QNX build files (Makefile, mkifs buildfile DRAFT, run script),
      QEMU notes, design constitution + registry, submission draft.

## Phase 1 — QNX access + first boot (user's taps; ~1 day)

Owner: user (account creation is his tap; agents do prep only).
1. myQNX account + free QNX Everywhere licence (qnx.software).
2. Install SDP 8.0 on the host (Windows/Linux; ~30–60 min).
3. Install "QNX SDP 8.0 Quick Start Target Image for QEMU" via
   Software Center; boot the QEMU image per its docs.
   - Prefer the Self-Hosted Developer Desktop QEMU image if
     available — Python + git preloaded, native iteration.
4. **Day-1 spike (stop/go gate):** on the target, answer the 8 open
   questions in RESEARCH.md §5 (Python version, `resource` module,
   `subprocess`+`preexec_fn`, `ap`/`aps` flags, networking,
   buildfile). If Python is missing or `ap` differs, adapt the
   porting layer — do not force it.

## Phase 2 — Port on target (~2–3 days)

5. `scp` staged tree to /opt/cagecheck-qnx; apply patches/ to
   app/*.py; run upstream suite ON QNX (must be 10/10 on target).
6. Run `run-on-qnx.sh`; verify `ap show cagecheck_snippet` and
   `curl <guest-ip>:8766/health` from the host.
7. Run the check flow end-to-end from the host browser: clean
   snippet → PASSED; SSH read → BLOCKED; runaway snippet
   (`while True: pass`) → killed/limited by the APS budget — record
   the evidence (partition CPU time before/after).
8. Restyle index.html to the "timing console" identity
   (design/DESIGN_CONSTITUTION.md) + 3D microkernel message view;
   interaction inventory (qa/) with no dead controls.

## Phase 3 — Release evidence (~2 days)

9. Create the NEW submission repo (user's tap — repo creation is
   his, or via his saved GitHub session): patches + qnx_cage +
   qnx/ + qemu/ + docs + MIT licence. Upstream referenced by URL
   only. No fork.
10. Record the demo video FROM the live QEMU target URL (<3 min,
    public YouTube): problem → paste → BLOCKED stamp → receipt →
    APS evidence → closing. Never from screenshots.
11. Devpost: register (user's tap), fill submission form (category:
    Open-Source Contribution & Ports; upstream URL; build/run
    instructions with QNX version + QEMU target + toolchain),
    attach video. Submit by **Sun 14 Dec 20:00 IST** safe target.
12. Stretch only if 5–11 are green: procmgr-ability helper, codelab
    for the $3,500 bonus.

## Critical path

myQNX account → SDP 8.0 install → QEMU boot → Day-1 spike answers →
port runs on target → video from live target → repo → submit.
The bottleneck is Phase 1 (user's account + install + first boot).
Everything after it is 2–4 days of focused work. Start Phase 1 by
**Fri 7 Nov** — the later it slips, the more the Dec crunch collides
with the other tracks (SPECS/BharatCode 10 Nov, Founding.dev 10 Nov,
SLAY/AI-Driven India 14 Nov).

## If QEMU fails

Fall back to labelled host-side build verification (qemu/QEMU_NOTES.md
fallback). Do NOT claim a QNX run that did not happen; do NOT submit
a screenshot video. A weaker honest entry beats a disqualified one.
