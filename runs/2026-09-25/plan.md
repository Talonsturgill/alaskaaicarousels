# RUN PLAN — Alaska.Ai Carousel No. 68 — September 25th

## Wake state

- run_guard: CLEAR for 2026-09-25. Woke 2026-09-24 23:15 AKDT; `runs/2026-09-24/` already
  holds No.67, shipped and merged, so the run date is the first date with no `runs/<date>/`,
  which is 2026-09-25 (recorded in run_state.json `date_note`).
- carousel_no = 67 topics entries + 1 = **68**.
- effort: `$CLAUDE_EFFORT` = high. The setting took.
- `prompts/NEXT_RUN.md` is **PARKED** (DO NOT USE BEFORE OCTOBER 14TH; the North Pacific
  Council acts on the 2027 Annual Deployment Plan at its October 5th to 13th meeting). It stays
  in place, is not archived, and this run selects its own story. Beat C is told the ADP is off
  limits today.
- Branch: the harness-designated `tsturg/zen-goodall-yg68mm` (prior runs shipped from harness
  branches too).

## Standing weakness, and what this run does about it

`trend_check.py --window 10` (2026-09-13 to 2026-09-24):

```
REPEAT OFFENDERS
  weakest  8/10  mean 7.0  last 7.0  Artwork craft and genuine detail   worked 2026-09-14 (8 runs ago)  <-- STALE
  weakest  1/10  mean 7.5  last 8.0  Deliverable completeness           worked never  <-- STALE
  weakest  1/10  mean 8.2  last 8.0  Alaska authenticity and local relevance  worked 2026-09-20  <-- STALE
HARD FAILS: none in this window
DEFECT CLASSES THAT KEEP SHIPPING: none recurring
SCORE: 09-15 8.61  09-17 8.79  09-18 8.76  09-19 8.36  09-20 8.50  09-21 7.98  09-23 8.67  09-24 8.34
```

**Attacking: artwork craft, 8 of 10 runs weakest.** No.67's lesson is that the defect is usually
chosen at PLANNING, not rendered: its slide 08 failed five rounds because the station had nothing
real to draw. So this run's move is in Phase 5, not Phase 8: every frame's dossier must name the
real MATERIAL the frame draws (a surface, a mass, a field with measured texture) and the one
modelled-tone structure in its lower third, and the deck plans FEWER distinct subsystems executed
more deeply (one shared bench, per-frame compositions). Critics diagnose; the plan changes when two
rounds name the same defect on the same slide (the No.67 parked rule, applied by hand).

## Variety constraints (from ledger/artwork.json)

- Hero structures FORBIDDEN (last 4): No.64 orthographic jurisdiction section; No.65 waterline hold
  (survey camera at a boundary inside a medium); No.66 reading frame plate (frontal engraved
  document, no camera); No.67 aerial unit over real DEM ground (perspective camera over terrain).
- Atmospheres FORBIDDEN (last 3): flood tide under high overcast; interior plate light (raking key
  az 118); blank sky by rule (cartographer's key az 315).
- Continuity devices FORBIDDEN (last 2): reading frame / engraved ground / struck slot / scale
  ladder (No.66); camera stations around one valley / gold square shape-state / station card (No.67).
- Hook archetypes FORBIDDEN (last 3): THE STATE OF MATTER; THE ENACTED LIMIT; THE THREE DATELINES.
- Palette families FORBIDDEN (last 3): turbid water column browns/greens; ink-and-plate
  #0A1014 to #C9DCD2; spruce-black/sphagnum/river ice.
- Type pairings FORBIDDEN (last 2): Fraunces + Manrope + Mono; Archivo condensed + Archivo + Mono.
  Recently heavy: Fraunces (64, 66), Archivo (64, 67). Open and unrun lately: Instrument Serif as
  display, Bricolage Grotesque, Space Grotesk.

## Variance dials (chosen to move, not to sit)

Last two: 5/4/4 and 3/4/2. This run: **design_variance 4, visual_density 3, type_temperature 4**
(pending the story; density drops to give the one material room to be deep rather than busy).

## Seasonal Alaska context for the scouts (late September 2026)

- General election November 3rd (governor race; primary was August 18th). Fairbanks North Star
  Borough Proposition 3 (hand count) is on the October 6th municipal ballot; Anchorage and Mat-Su
  borough elections early October.
- PFD amount announced in September, paid in October. AFN Convention in October.
- Legislature out of session (zero BASIS hearings is normal until January).
- Fall storm season on the west coast (Typhoon Merbok anniversary, September 2022); sea ice minimum
  just past; freeze-up begins; termination dust on the Chugach.
- Fisheries: salmon season closed; Bering Sea crab opener mid October; North Pacific Council meets
  October 5th to 13th in Anchorage (the ADP is parked for October 14th, do not take it early).
- Fall moose season closes; wildfire season over (XPRIZE Wildfire covered yesterday).
- Cook Inlet gas: storage heading into winter; CINGSA dashboard stale since September 13th (an
  upstream incident carried by the last two runs).
- Federal fiscal year ends September 30th: obligations, grant awards and contract actions cluster
  this week.

## Top instincts (confidence >= 0.7), injected into every subagent brief

1. grain-as-tile (0.99): grain as a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect.
2. machine-qa-is-not-taste (0.99): a machine_qa PASS is not composition approval.
3. verify-body-line-count (0.99): check long body copy line counts against fixed-position labels
   before rendering; DOM overlaps pass QA and fail the eye.
4. A constraint you can't point at is one you invented: there is no context or token budget.
5. fitextent-fits-the-smaller-dimension (0.99): d3 fitExtent preserves aspect; set a one-axis
   extent explicitly.
