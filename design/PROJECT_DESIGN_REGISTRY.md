# PROJECT DESIGN REGISTRY — QNX track (comparison)

Rulebook §1.3: compare with at least the three most recent projects
before approving a new design. Inspected 5 Nov 2026 from the local
design constitutions.

## The three most recent projects

| Project | Metaphor | Palette | Layout | Signature interaction |
|---|---|---|---|---|
| **CageCheck** (3 Nov 2026) | Border inspector's stamp desk — cage + rubber stamp + paper receipt | Warm paper/ink, stamp red | Single column, paste → stamp → receipt | Circular rotated rubber stamp (PASSED/HELD/BLOCKED) |
| **Digest Room** (Flip the Switch, 5 Nov 2026) | "The room is the desk" — chat timeline IS the workflow | Deep slate `#0F1419`, night-shift console, dark | Chat timeline hero + slim right rail of claimed tasks | Reaction claim → task card in-thread |
| **Spec Ghost** (Kiroween, 3 Nov 2026) | Haunted house as information architecture — rooms are scan categories | Dark haunted-house (per constitution) | House sections in scan order | Room cards = covered specs |

## This project — CageCheck on QNX

| Aspect | Choice | Distinct from the three above how |
|---|---|---|
| Metaphor | Timing console — trace line + APS partition lane | Time/budget as the visual subject; none of the three is about timing |
| Palette | Light blueprint schematic: paper `#F4F1EA`, navy ink `#14213D`, trace blue, amber/red/green signals | Light theme vs Digest Room + Spec Ghost dark; cooler/bluer than CageCheck's warm paper |
| Layout | Single column, trace → paste → stamp → receipt → partition bar | No sidebar (unlike Digest Room's rail), no house sections, no stamp-desk framing |
| Signature interaction | Timing-trace markers per check + 5% CPU partition bar | Neither a rubber stamp, nor a chat claim, nor room cards |
| 3D | Microkernel message-passing scene (server/policy/runner nodes, pulses) | None of the three has a message-passing 3D model; the 3D explains the architecture |

Verdict: recognisably different in concept, palette, layout and
interaction — not a recolour. Approved in principle; final approval
after the 5-reference research pass (constitution §10) and the
Phase 2 build.
