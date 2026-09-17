# WORKLOG — run 2026-09-17, carousel No.61, THE DRIFT LINE

Written at the start of Phase 8's first revision round, because the round is
large enough to cross a context boundary and a plan that lives only in context
does not survive compaction. Delete this file when the wrap tasks are DONE.

## Where the run is

Phases 0 to 7 are done and committed. The deck is nine slides, machine-green
(render 9/9 clean, qa.py PASS 0/0, dossier_check PASS 9/9, bespoke PASS,
claims 41/41, aggregate PASS, reconciled PASS, every frame clears
frame_balance at 1.00 to 1.18). BUILD RECONCILIATION is written and synced.
The deck is assembled: vector PDF, 9 pages, 11.55 MB.

Phase 8's pixel critics have reported and the MACHINE GREEN IS NOT THE DECK.
Five slides scored 4.5 to 6.0 against a ship threshold of 8.3. This is a work
order, not a verdict (CLAUDE.md): fix the named defects, re-render, re-gate,
re-score, repeat until it clears.

## The through-line of the critique

Three defects repeat across frames and each one is CHASSIS, not slide:

1. **D.veil renders as a hard rectangle.** A fixed 16 px blur on a wash that
   can be 400 x 240 leaves four straight edges. Slide 02's veil under MAY was
   called the single most damaging craft defect on the frame; slide 09's
   overruns its type by 195 px and reads as a third plate.
2. **The 2D law-bearing marks float.** D.gateMark and D.stakeMark were moved
   into 2D in Phase 7 to fix the ink census and the 432 px legibility, and
   they fixed both. But they are laid at hand-tuned constants, so on 01, 03,
   06 and 09 they sit on open snow attached to nothing and read as scratches
   or a stray legend key. They must be SEATED on the geometry they name.
3. **Hard seams where two passes meet.** Slide 01 has a full-width step at
   y 473 (the ground plane's far edge at 150 m, where fog #16304C meets the
   sky texture's bottom stop #20415F). Slide 06 has a vertical seam where the
   drift plane ends square. Slide 02 has a step under the headline.

## Task table

| # | Task | Status |
|---|---|---|
| C1 | D.drift end taper | DONE |
| C2 | D.veil feathered from the box, plus D.inkBoxes | DONE |
| C3 | Sky's last stop tied to the fog colour | DONE |
| C4 | D.camera + D.snapToSilhouette; marks projected, not placed | DONE |
| C5 | Volumetric shaft feathered across its width | DONE |
| C6 | Mesh rotation yaw minus 90 (the quarter turn) | DONE |
| C7 | Ground plane out to 2 km | DONE |
| C8 | Drift vertex-colour blend, with needsUpdate | DONE |
| S1..S9 | All nine slides through four revision rounds | DONE |
| X1 | Copywriter's three copy corrections | DONE |
| W1 | Render, qa, dossier, aggregate, bespoke, gate sync | DONE |
| W2 | Second and third critic rounds | DONE |
| W3 | copy.json gates: style_lint, copy_sync, plan_drift, caption_check | DONE |
| W4 | Flow critic (7.8) | DONE |
| W5 | Score: 8.79 vs threshold 7.70, ship=true | DONE |
| P11 | runs/2026-09-17, webp, PDF, site rebuild, ledgers, FIELD_NOTES | DONE |
| P11b | Push both branches, PR #373 ready, subscribed | DONE |
| P12 | Upgrade engineer, then merge to main | IN PROGRESS |
| P13 | Gmail draft (after the merge; image URLs point at main) | TODO |
| P14 | Retro, run_state complete, delete this file | TODO |

## Decisions already made, do not relitigate

- Slide 08 declares NO measured contact. Its gauge board hangs on the rail and
  its only post foot is behind the left plate. Struck in the dossier.
- Slide 05 carries NO data-breather. It never needed one.
- Slide 01 declares the bay 02 post foot as the deck's measured contact, at
  11.0 L*, painted by the new D.footAO.
- aggregate_check was taught calendar months so "TWENTY MONTHS OLD" could be
  declared as the duration it is instead of misfiled as artwork.
