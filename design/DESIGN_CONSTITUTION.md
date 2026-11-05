# DESIGN CONSTITUTION — CageCheck on QNX ("Timing Console")

Status: PREP — describes the intended restyle of `app/index.html`
for the QNX port. The upstream UI (paper/ink/stamp) is NOT reused;
this is a distinct identity. Nothing here is built yet; the build
happens in Phase 2 on the target (BUILD_PLAN.md).

## 1. Product personality and emotional tone

A real-time timing console, not a stamp desk and not a SaaS
dashboard. Precise, quiet, metronomic. Every decision is shown with
its timing: how long the policy scan took, how much CPU the runner
was allowed, how much it used. The product's argument is visible in
the chrome itself: *a check that cannot be starved by the code it
checks*.

## 2. Target user and context of use

A developer about to paste AI-suggested code into a safety-critical
 codebase, and a judge watching a screen share of a QEMU target.
 Primary viewing context: host browser pointed at the QNX guest.
 The whole decision — paste → scan → stamp → receipt → partition
 evidence — must be readable in one scroll, with no tab hunting.

## 3. Visual metaphor — timing trace + partition

- **Timing trace:** a horizontal trace line (oscilloscope-style)
  runs under the hero; each check drops a marker on it with its
  verdict colour and its milliseconds. Time is the product's
  subject, so time is drawn.
- **Partition:** the cage is drawn as a bounded lane — a 5% slice of
  a 100% CPU bar — labelled with the APS budget. The snippet runner
  lives inside that lane; the server lives outside it. The boundary
  is a visible bar, not just a word.
- **Stamp:** kept from upstream (PASSED / HELD / BLOCKED) but
  restyled: a squared-off, technical stamp, not a rubber stamp —
  the decision is an instrument reading.

## 4. Colour palette (semantic roles)

| Token | Value | Role |
|---|---|---|
| Paper | `#F4F1EA` | Page background — light schematic paper, NOT CageCheck's warm paper (different hue temp + blueprint grid) |
| Ink | `#14213D` | Primary text, deep blueprint navy |
| Trace blue | `#1D4ED8` | Links, active states, trace line |
| Signal amber | `#D97706` | HELD, warnings, budget markers |
| Block red | `#B91C1C` | BLOCKED, errors |
| Pass green | `#15803D` | PASSED, healthy |
| Grid line | `#D8DEE9` | Blueprint grid, hairlines |

Light theme, deliberately: the three most recent projects are
paper-warm (CageCheck), dark slate console (Digest Room) and
haunted-house dark (Spec Ghost). A light blueprint schematic is
recognisably different from all three.

## 5. Typography

- Display/headings: monospace with wide tracking for labels
  ("CAGECHECK / QNX" eyebrow, section numbers) — instrument-panel
  labelling, not marketing type.
- Body: system sans, short lines, one idea per paragraph.
- Receipts: monospace, as upstream (a receipt you can quote back).

## 6. Layout

Single column, max ~880px. Order: header (product + target line
"QNX 8.0 · QEMU x86_64 · APS 5%") → timing trace → paste box +
Check button → stamp + receipt → partition bar with live budget →
audit list. No sidebar, no dashboard grid — the console is the page.

## 7. 3D experience (meaningful, not decoration)

**Microkernel message-passing view:** a small 3D scene (Three.js,
lazy-loaded, with a static 2D fallback) showing the QNX microkernel
at the centre, the server process and the snippet-runner process as
nodes, and the checked snippet's messages as pulses travelling
server → policy → runner → receipt. The user can rotate it and click
a node to see what that process is allowed to do. It teaches the
architecture the port is selling: isolation is the message passing,
not a slogan. Keyboard alternative: a labelled list of the same
nodes. Respects `prefers-reduced-motion` (static diagram).

## 8. Motion language

Restrained: the trace marker draws in (fast, 150 ms), the stamp
lands with a single 120 ms scale settle, nothing pulses, nothing
floats. Motion marks cause-and-effect (check → marker → stamp), not
decoration.

## 9. Responsive / accessibility

Desktop first (judge screen share), but no horizontal overflow at
360 px; the 3D scene collapses to the static diagram under 640 px
or without WebGL. All controls keyboard-reachable with visible
focus; forms labelled; reduced-motion honoured.

## 10. Design research status (honest)

Inspected in this pass (5 Nov 2026): the QNX Devpost page
(structure, categories, evidence rules) and the upstream CageCheck
constitution + UI (what NOT to repeat). NOT yet inspected: five
external design references per rulebook §1.1 — the research pass
for this track is PARTIAL. Before the Phase 2 restyle, inspect and
record: two real-time/embedded console UIs, one exceptional motion
system, one strong typographic hierarchy, one 3D/spatial data
visualisation. Gate A is NOT passed until that is done.
