# PLAN, 2026-10-24, Carousel No.95

Woke 22:04 AKDT October 24th (06:04 UTC October 25th). Run date is the Anchorage
date, 2026-10-24; runs/2026-10-24 does not exist. run_guard --run-date 2026-10-24
CLEAR (run_guard with no argument reads the UTC date, 2026-10-25, which is not the
run date). Effort: high (CLAUDE_EFFORT=high, as the repo settings intend). No
prompts/NEXT_RUN.md queued.

Environment at wake: the Bash auto-mode classifier returned no verdict for about ten
minutes (06:05Z to 06:15Z); Read and Write kept working and the run read the knowledge
base meanwhile. bootstrap.sh printed "no chromium found" again (open MACHINE_QUEUE item,
the chrome-linux64 glob); /opt/pw-browsers/chromium-1243 is present.

## Top 5 instincts (confidence >= 0.7, injected into every subagent prompt)

1. (0.99) Apply grain as a small repeating tile (AK.grainTile / AK.grainOn), never a
   full-frame feTurbulence rect.
2. (0.99) Never treat a machine_qa PASS as composition approval; the pixel critics judge
   composition, hierarchy and collision at full size and thumb size.
3. (0.99) Before rendering, check long serif/body copy line counts against any
   fixed-position labels, bars or plates; DOM overlaps pass machine QA but fail the eye.
4. (0.99) A generated block pasted into a run record goes stale the moment another round
   runs. Regenerate gate_status --sync after the LAST render, every round.
5. (0.99) d3's fitExtent preserves aspect; a projection onto one axis needs that axis
   remapped explicitly after a normal fit.

## Variety constraints (from ledger/artwork.json)

Forbidden hero structures (last 4): THE PINNED RELIEF SHEET (10-20), THE FLOWN LINE
(10-21), THE COMPOSING STONE (10-22), THE REGISTERED LAYER (10-23).
Forbidden atmospheres (last 3): THE OCTOBER NOON OVER MAGNETITE, THE NORTH SKYLIGHT AT
FOUR, THE FIRST ICE FOG.
Forbidden continuity devices (last 2): the ink law as a device, a brass line motif, an
accession stamp ticker, one skylight, edge tease 03 to 04 (10-22); a registered-layer
camera move, a gold line migrating between media, a survey staff planted then graduated
(10-23).
Forbidden hook archetypes (last 3): THE ODOMETER, THE NAMED PARTY ANSWERS, THE ONE-WORD
AUDIT.
Forbidden palette families (last 3): caesius and magnetite; type metal, oak and proof
bond; inversion season (night slate, jade, hoarfrost, rust, alpenglow).
Forbidden type pairings (last 2): Instrument Serif + Archivo + JetBrains Mono; Fraunces +
JetBrains Mono.

## Variance dials (vary the dials themselves)

Last six: (4,3,1) (4,5,3) (3,3,5) (5,2,2) (2,4,3) (4,2,4).
This run: DESIGN_VARIANCE 3, VISUAL_DENSITY 4, TYPE_TEMPERATURE 2. Revisit at the
directors room if the story argues otherwise.

## Seasonal Alaska context (late October)

- November 3rd general election, governor's race on the ballot; early voting under way
  since October 19th. Legislature out of session (zero hearings normal June to December).
- Senate Resources' subpoenaed DNR Commissioner John Crowther appears October 26th,
  10 a.m., Anchorage LIO (covered No.88; only material news would justify an update).
- PFD paid in October. AFN convention season just past. Freeze-up on Interior rivers,
  first snow in Anchorage. Cook Inlet gas in winter withdrawal (Gas Watch 7.67 Bcf on
  October 24th, injection restriction active, inventory declining).
- FERC P-15423 (DeepGreen) comment and intervention window closes November 2nd (covered
  No.65, No.68, No.93). Daylight saving ends November 1st.
- Bering Sea crab openers mid October; NPFMC December meeting ahead; UA Regents in November;
  RCA winter dockets.

## Standing weakness (trend_check --window 10)

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  7/10  mean 7.18   last 7.3    Artwork craft and genuine detail        worked 2026-10-04 (17 run(s) ago)  <-- STALE
  weakest  2/10  mean 7.3    last 7.0    Variety vs ledger                       worked 2026-08-15 (60 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.7    last 7.5    Legibility and platform fitness         worked never (never)  <-- STALE

HARD FAILS (0 of 10 run(s) carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   6 run(s)  warns:outside safe zone                               latest 2026-10-22
   5 run(s)  warns:busy art under text                             latest 2026-10-23
   4 run(s)  warns:contact shadow                                  latest 2026-10-22
   4 run(s)  warns:ragged display line                             latest 2026-10-22
   3 run(s)  warns:top-loaded composition                          latest 2026-10-21
   3 run(s)  warns:art touching glyphs                             latest 2026-10-22

SCORE, most recent runs
  10-15 8.66  10-16 8.79  10-17 8.74  10-19 8.60  10-20 8.44  10-21 8.66  10-22 8.42  10-23 8.63
```

THE ONE WEAKNESS THIS RUN ATTACKS: Artwork craft, weakest on 7 of 10. The retros say
how it is lost: the largest object stalls (No.84, No.85, No.86 rebuilt nothing and
touched six frames), and the cover and depth frame are closed late. This run (1) builds
the masterful depth frame and the cover FIRST and closes both by round 3; (2) plans one
lit EVENT per lower third (not a texture) and names it in field 4a; (3) keeps type over
quiet ground by routing the art, with AKPOST.reserve at a 20 design px feather only where
routing fails; (4) draws the flag gold after the grade or ends with AKPOST.holdInk; (5)
spends any craft cycle rebuilding the largest object of the two named frames rather than
touching six.

Secondary: "outside safe zone" and "busy art under text" warns have shipped on 6 and 5 of
10 runs. Every dossier's layout map keeps primary type inside 80 to 1000 x 80 to 1270
and names the quiet ground under each text block.

## Phase 1 craft refresh

Two searches (LinkedIn document posts in October 2026; editorial night cartography). The
only concrete platform item, LinkedIn's compact carousel display, is already in
FIELD_NOTES (line ~8993). Nothing new; nothing appended.
