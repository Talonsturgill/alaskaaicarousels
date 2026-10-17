# PLAN, run 2026-10-16, Alaska.Ai carousel No.88

Run date 2026-10-16 (America/Anchorage; session woke 22:14 AKDT). Effort in effect: high (CLAUDE_EFFORT=high, as the settings intend).
No prompts/NEXT_RUN.md queued. run_guard CLEAR. machine_due: weekly pass DUE today (repeat offender queued, last pass 2026-10-11).

## Top 5 instincts (confidence >= 0.7), injected into every subagent brief
1. A generated block pasted into a run record goes stale the moment another round runs; re-sync gate_status after every round.
2. AK.grainTile returns a DATA URL, not a canvas; grain is a DOM layer (CSS background, overlay, opacity 0.05 to 0.12), never createPattern.
3. A constraint you can't point at is one you invented; there is no context or token budget. Finish the deck.
4. A machine_qa PASS is not composition approval; critics judge composition, hierarchy and collision at full size and thumb.
5. A repair can land a bigger defect than the one it fixed; re-render and re-read every frame you touched with fresh eyes.

## Variety constraints (ledger/artwork.json)
Forbidden hero structures (last 4): THE PAINT LAW (10-11), THE ROOM AND THREE ADDRESSES (10-12), THE EXHIBITS (10-14), THE FRAME IS THE RULER (10-15).
Forbidden atmospheres (last 3): projector spill/lowland west light (10-12), sea smoke at the rail (10-14), the south window at twenty degrees (10-15).
Forbidden continuity devices (last 2): camera move, palette arc, edge-tease (10-14); panorama spine ruler, gold/ice motif, one-sun light (10-15).
Forbidden hook archetypes (last 3): THE ADDRESS, BETTER EYES SAME BILL, THE DECK AS MEASURE.
Forbidden palette families (last 3): projector spill/slate velvet, galvanized zinc/tarred groundline/sea smoke, cutting mat/museum board/vellum/gold leaf.
Forbidden type pairings (last 2): Fraunces display+text + JetBrains Mono; Unbounded 560 + Archivo + JetBrains Mono.
=> Candidate continuity for today: motif evolution of a NEW kind + weather/time arc or a split-frame device; not a panorama spine, not a camera move.
=> Candidate type: Instrument Serif or Bricolage Grotesque or Space Grotesk display + Manrope + JetBrains Mono (not Fraunces-only, not Unbounded/Archivo).

## Variance dials (chosen to differ from 10-15's 5/2/2)
design_variance 3, visual_density 4, type_temperature 4 (warmer serif display, denser information frames).

## Seasonal Alaska context (mid October)
- Legislature out of session (34th Legislature's second session ended in May; next convenes January 2027). Interim hearings only.
- November 3rd general election: governor's race, ballot measures; early voting starts about October 19th.
- Alaska Day, October 18th (Sitka). AFN Convention in mid to late October (Anchorage).
- PFD payments in October.
- Freeze-up under way on the Interior rivers; Cook Inlet gas moving from injection to withdrawal; GVEA's first Energy Emergency Alert (October 12th) is fresh.
- Fall Bering Sea crab and pollock B season; NPFMC met October 9th.
- Federal fiscal year began October 1st; grant cycles and DOE/DPA announcements.

## Standing weakness (trend_check --window 10)
```
REPEAT OFFENDERS
  weakest  7/10  mean 6.98   last 7.5    Artwork craft and genuine detail   worked 2026-10-04  STALE
  weakest  2/10  mean 7.03   last 7.0    Variety vs ledger                  worked 2026-08-15  STALE
  weakest  1/10  mean 7.77   last 7.5    Thumb-stop cover                   worked 2026-09-02  STALE
HARD FAILS: none in window
DEFECT CLASSES THAT KEEP SHIPPING: contact shadow (4 runs), busy art under text (3), art touching glyphs (3), top-loaded composition (2), outside safe zone (2)
SCORES: 10-07 8.74, 10-08 8.41, 10-09 8.20, 10-10 8.60, 10-11 8.26, 10-12 8.62, 10-14 8.51, 10-15 8.66
```
THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft, specifically "the largest object on the frame is the least modelled" (flow critic cause b, the week's most persistent). How: the CRAFT PLAN names each frame's largest object FIRST and its modelling, the masterful depth frame is BUILT FIRST, and no frame relies on a texture as its largest mass. Fewer, larger, better-modelled objects (visual_density 4 means information, not clutter). Text reserves are designed into the ground before the first render (busy art under text, art touching glyphs).
