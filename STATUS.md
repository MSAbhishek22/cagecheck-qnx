# STATUS — CageCheck on QNX (5 Nov 2026)

**Overall: IN_PROGRESS — prep + verified scaffold. NOT a submission,
NOT deployed, NOT run on QNX yet.**

## Release card (rulebook §10)

| Deliverable | Evidence | Status |
|---|---|---|
| Project identity | CONCEPT.md — CageCheck-on-QNX port, timing-console design | DONE (prep) |
| Research | RESEARCH.md — official Devpost pages read 5 Nov 2026 | DONE |
| Live application | None — needs QNX 8.0 QEMU target (user's taps first) | BLOCKED (Phase 1) |
| GitHub | No submission repo yet — new repo in submission period, user's tap | NOT STARTED |
| Deployment | QNX QEMU target, not HTTPS — the "live" artifact is the QEMU run + video | BLOCKED (Phase 1) |
| UI quality | design/DESIGN_CONSTITUTION.md + registry comparison | PARTIAL — 5-reference research pass still open (§10) |
| 3D experience | Planned: microkernel message-passing scene | NOT BUILT |
| Functional controls | qa/INTERACTION_INVENTORY.md | NOT STARTED (UI restyle is Phase 2) |
| QA | Port tests 13/13 PASS; upstream 10/10; patched tree 10/10; policy vectors 7/7; live server smoke OK (all Linux sandbox) | PASS (sandbox only) |
| Demo video | Not recorded — only ever from the live QEMU URL, later | BLOCKED |
| Published video | None | BLOCKED |
| Submission | Draft only (submission/SUBMISSION_DRAFT.md) | PREP ONLY |

## Gate status (rulebook §9)

- GATE A (Research & design): PARTIAL — rules verified; 5-reference
  design research still open; constitution + registry done.
- GATE B (Functional product): IN PROGRESS — porting layer + patches
  verified on Linux; QNX run outstanding.
- GATE C (3D & visual quality): NOT STARTED.
- GATE D (QA): PARTIAL — sandbox tests green; on-target QA outstanding.
- GATE E (GitHub & deployment): NOT STARTED — repo + QEMU run outstanding.
- GATE F (Demo video): NOT STARTED — needs Gate E.
- GATE G (Final handoff): NOT STARTED.

## Status summary

- `LIVE_DEPLOYMENT`: BLOCKED (needs QNX QEMU target; user's myQNX/SDP taps)
- `GITHUB_COMMIT_MATCH`: BLOCKED (no repo yet)
- `ALL_VISIBLE_CONTROLS`: BLOCKED (UI restyle not built)
- `3D_EXPERIENCE`: BLOCKED (not built)
- `UI_DISTINCTIVENESS`: PASS (in principle — registry comparison done)
- `RESPONSIVE_AND_ACCESSIBLE`: BLOCKED (not built)
- `DEMO_VIDEO_RECORDED_FROM_LIVE`: BLOCKED
- `VIDEO_PUBLISHED_AND_URL_VERIFIED`: BLOCKED
- `HACKATHON_RULE_COMPLIANCE`: PASS (prep) — rules verified, Ports-category
  shape followed (new repo, patches not fork)
- `OVERALL_RELEASE`: IN_PROGRESS

## Test receipts (this sandbox, Linux, Python 3.12.3)

- Upstream CageCheck suite: 10/10 PASS (unittest, 0.24 s).
- Patched tree (patches applied): 10/10 PASS + 7/7 policy vectors +
  live server smoke test (BLOCKED receipt for SSH read, correct tier).
- Port suite (`python3 -m unittest discover -s tests`): 13/13 PASS.
- No QEMU installed in this sandbox; no QNX image/SDP — nothing
  here claims a QNX run.
