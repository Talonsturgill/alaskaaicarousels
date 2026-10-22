# Plan, run 2026-10-21 (No.92)

Woke 22:05 AKDT October 21st (2026-10-22 05:05 UTC). runs/2026-10-21 absent, run_guard CLEAR for
2026-10-21, so the run takes the Anchorage date. No prompts/NEXT_RUN.md. Effort in effect: high
(`$CLAUDE_EFFORT=high`, as the repo settings intend). Branch: the session's designated branch
`tsturg/clever-mayer-d3poy8` (the harness pins it; CLAUDE.md's delivery policy still governs the
ready PR and the merge).

## Top 5 instincts (confidence >= 0.7), injected into every subagent brief

1. (0.99) A generated block pasted into a run record goes stale the moment another round runs.
   Regenerate gate_status --sync at the LAST render.
2. (0.99) AK.grainTile returns a data URL, not a canvas. Grain is a DOM layer over the art canvas,
   never a createPattern fill.
3. (0.99) A machine_qa PASS is not composition approval; critics judge composition at full and
   thumb size.
4. (0.99) Sanity-check long body copy line counts against fixed-position labels and plates before
   rendering; DOM overlaps pass machine QA and fail the eye.
5. (0.99) Grain is a small repeating tile, never a full-frame feTurbulence rect.

## Variety constraints (ledger/artwork.json)

Forbidden hero structures (last 4): THE TRANSCRIPT WITHOUT A WITNESS (Q and A pages, plate
registers), THE ANALYSIS LATTICE (true-geography world with a forecast grid and descending
camera), THE SPLIT SPECIMEN (sawn anatomical specimen), THE PINNED RELIEF SHEET (pin map on a
plaster relief model).
Forbidden atmospheres (last 3): THE BREAK UNDER THE CEILING (low stratus), RUNWAY NIGHT OVER THE
CORE, THE MAP-TABLE LAMP (raking NW key on plaster).
Forbidden continuity devices (last 2): a pinned gold motif that becomes the Polaris; a hand-laid
palette-arc wash; a three-frame shared projection registration; the kerf motif; an orbit camera
with no readout; a 01-to-02 half-cut edge tease.
Forbidden hook archetypes (last 3): THE BLANK ON THE MAP, THE TWO READINGS, THE WRONG ADDRESS.
Forbidden palette families (last 3): silt/stratus/sedge rust; core box/Tyonek sandstone/coal on
subsurface navy; chart night/plaster/salmonberry wash/gold/instrument steel.
Forbidden type pairings (last 2): Archivo + JetBrains Mono; Fraunces + JetBrains Mono.

## Variance dials (chosen)

Last four: (3,4,4), (4,3,1), (4,5,3), (3,3,5). This run: design_variance 5, visual_density 2,
type_temperature 2. Density drops to 2 because the last two decks sat at 5 and 3 and the scorer
has charged busy art under text on three of the last ten; temperature goes cool after a 5.
Final dial justification is restated in the storyboard header once the story is known.

## Seasonal Alaska context (for scouts)

Late October. Legislature out of session (interim; Senate Resources subpoena hearings on DNR
continue). General election November 3rd (governor, US House, legislature, ballot measures),
early voting open. AFN convention season. PFD paid in October. Freeze-up starting on the
Interior rivers; fall storms on the west coast (one year after Halong). Cook Inlet gas winter
draw beginning; GVEA issued its first Energy Emergency Alert October 12th. Bering Sea red king
crab and snow crab seasons opened October 15th. NPFMC met in October (280th meeting). UA Board
of Regents November meeting ahead. Military: Arctic training season and JBER/Eielson F-35 ops.

## Standing weakness (trend_check --window 10)

```
weakest  6/10  mean 7.05   last 7.0    Artwork craft and genuine detail        worked 2026-10-04 (14 run(s) ago)  <-- STALE
weakest  3/10  mean 7.05   last 6.5    Variety vs ledger                       worked 2026-08-15 (57 run(s) ago)  <-- STALE
weakest  1/10  mean 7.6    last 7.0    Legibility and platform fitness         worked never (never)  <-- STALE
HARD FAILS none in this window
DEFECT CLASSES THAT KEEP SHIPPING: outside safe zone (5 runs), contact shadow (4), art touching
glyphs (3), busy art under text (3), tiny-text (3), ragged display line (3)
SCORES 10-11 8.26  10-12 8.62  10-14 8.51  10-15 8.66  10-16 8.79  10-17 8.74  10-19 8.60  10-20 8.44
```

THE ONE WEAKNESS THIS RUN ATTACKS: Artwork craft. How: fewer, larger objects per frame (visual
density 2), each frame's largest object modelled first and named in the CRAFT PLAN with its
light, lee and contact; the masterful depth frame built and critic-checked first; and type set
on composed quiet ground (no veils or plates over busy art), which also attacks the "busy art
under text" and "art touching glyphs" warns. Secondary: every text block inside the 80 px safe
zone from the first build (the outside-safe-zone warn shipped on five of ten runs).
