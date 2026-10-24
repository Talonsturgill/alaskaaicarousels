# PLAN, 2026-10-23, Carousel No.94

Woke 22:06 AKDT October 23rd (06:06 UTC October 24th). Run date is the Anchorage
date, 2026-10-23; runs/2026-10-23 does not exist. run_guard CLEAR. Effort: high
(CLAUDE_EFFORT=high, as the repo settings intend). No prompts/NEXT_RUN.md queued.

## Top 5 instincts (confidence >= 0.7, injected into every subagent prompt)

1. (0.99) A generated block pasted into a run record goes stale the moment another
   round runs. Regenerate gate_status --sync after the LAST render, every round.
2. (0.99) AK.grainTile returns a data URL, not a canvas. Grain is a DOM layer over
   the graded art canvas (mix-blend overlay, opacity 0.05 to 0.12), never a canvas fill.
3. (0.99) A machine_qa PASS is not composition approval; the pixel critics judge
   composition, hierarchy and collision at full size and thumb size.
4. (0.99) Before rendering, check long serif/body copy line counts against any
   fixed-position labels, bars or plates; DOM overlaps pass machine QA but fail the eye.
5. (0.99) A constraint you can't point at is one you invented. There is no context
   or token budget in this routine. Write the next slide.

## Variety constraints (from ledger/artwork.json)

Forbidden hero structures (last 4): THE SPLIT SPECIMEN (10-19), THE PINNED RELIEF
SHEET (10-20), THE FLOWN LINE (10-21), THE COMPOSING STONE (10-22).
Forbidden atmospheres (last 3): THE MAP-TABLE LAMP, THE OCTOBER NOON OVER MAGNETITE,
THE NORTH SKYLIGHT AT FOUR.
Forbidden continuity devices (last 2): panorama rail with an aircraft tick, gold
meaning the flown line, tonal arc as a named device (10-21); the ink law as a
device, a brass line motif, an accession stamp ticker, one skylight, edge tease
03 to 04 (10-22).
Forbidden hook archetypes (last 3): THE WRONG ADDRESS, THE ODOMETER, THE NAMED
PARTY ANSWERS.
Forbidden palette families (last 3): chart night/plaster/salmonberry; caesius and
magnetite; type metal/oak/proof bond.
Forbidden type pairings (last 2): Space Grotesk + JetBrains Mono; Instrument Serif +
Archivo + JetBrains Mono.

## Variance dials (vary the dials themselves)

Last five: (4,3,1) (4,5,3) (3,3,5) (5,2,2) (2,4,3).
This run: DESIGN_VARIANCE 4, VISUAL_DENSITY 2, TYPE_TEMPERATURE 4. Revisit at the
directors room if the story argues otherwise.

## Seasonal Alaska context (late October)

- November 3rd general election, governor's race on the ballot; early and absentee
  voting under way. Legislature out of session (hearings normally zero June to December).
- PFD payments land in October. AFN convention season (mid to late October).
- Freeze-up begins on the Interior rivers; first snow in Anchorage; Cook Inlet gas
  enters winter withdrawal (Gas Watch shows injection restriction active, inventory
  declining at 7.68 Bcf on October 23rd).
- FERC P-15423 (DeepGreen) comment, intervention and competing-application window
  closes November 2nd (covered No.65, No.68, No.93; do not repeat without material news).
- Daylight saving time ends November 1st. Fishing seasons closed; NPFMC December meeting ahead.
- Board of Fisheries cycle, University of Alaska Regents (November), RCA winter dockets.

## Standing weakness (trend_check --window 10)

```
REPEAT OFFENDERS
  weakest  7/10  mean 7.1    last 7.0    Artwork craft and genuine detail        worked 2026-10-04 (16 run(s) ago)  <-- STALE
  weakest  2/10  mean 7.3    last 7.5    Variety vs ledger                       worked 2026-08-15 (59 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.7    last 8.0    Legibility and platform fitness         worked never (never)  <-- STALE
HARD FAILS: none in this window
DEFECT CLASSES THAT KEEP SHIPPING
   6 run(s)  warns:outside safe zone
   5 run(s)  warns:busy art under text
   5 run(s)  warns:contact shadow
   4 run(s)  warns:ragged display line
   3 run(s)  warns:top-loaded composition
   3 run(s)  warns:art touching glyphs
SCORE  10-14 8.51  10-15 8.66  10-16 8.79  10-17 8.74  10-19 8.60  10-20 8.44  10-21 8.66  10-22 8.42
```

THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft, through FEWER, BETTER-MODELLED
objects. Visual density is set to 2 so each frame carries one large object that is
the best-modelled thing on it (flow-critic cause b, named on every deck of the
first weekly digest). Concretely: the masterful depth frame is built FIRST and
reviewed before the rest; every frame's largest object gets a named light
(key azimuth and elevation stated in the dossier), a lit ground under its foot
before any contact shadow, and no type reserve box (route the art around the
type; AKPOST.reserve only where unavoidable, feathered in design px). Flag gold is
drawn AFTER the grade or held with AKPOST.holdInk. Second target, the "outside
safe zone" warn that shipped on six runs: every text block placed inside the
80px margins by construction, and the warn list read before review.
