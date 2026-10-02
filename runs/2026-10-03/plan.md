# PLAN, run 2026-10-03, Carousel No.76

## Date
Woke 22:14 AKDT on October 1st, the regular daily slot. runs/2026-10-01 (No.74) and runs/2026-10-02 (No.75) were both taken by off-schedule firings earlier on Anchorage October 1st, and No.75 completed cleanly, so this is a new daily firing (2026-09-25 precedent) and the run date is the first free date, 2026-10-03. run_guard --run-date 2026-10-03 CLEAR.

## Queued assignment
prompts/NEXT_RUN.md (NPFMC 2027 ADP) is dated not before October 14th. Left parked; the ship note says so.

## Top instincts (confidence >= 0.7), injected into every subagent prompt
1. Apply grain as a small repeating tile (AK.grainTile, which returns a DATA URL for a CSS background, never a canvas pattern), never a full-frame feTurbulence rect.
2. Never treat a machine_qa PASS as composition approval; the pixel critics judge composition, hierarchy and collision at full size and thumb size.
3. Before rendering, sanity-check long serif/body copy line counts against any fixed-position labels, bars or plates; qa.py's collision check is DOM-only, so labels against canvas/SVG geometry need an eye.
4. A generated block pasted into a run record goes stale the moment another round runs; re-sync after every round.
5. A constraint you cannot point at is a constraint you invented: no context, token or time budget exists; do not cut work for one.

## Variety constraints (forbidden this run)
- Hero structures (last 4): the cut-and-paste notice (72); one strait at five scales (73); the long table of the record, counted exhibits on one table (74); the inspection bench, precision instruments in one metrology room (75).
- Atmospheres (last 3): marine ceiling west-bright overcast (73); the long window, linear source front right (74); the inspection softbox, overhead top-centre (75).
- Continuity devices (last 2): three gold ballots, warm-to-cool split-tone arc, edge-tease, one lit nosing (74); the gold reading cursor hairline, the uncut field drawn as an absence, one camera moving through one room (75).
- Hooks (last 3): the majority answer (73); the matched count (74); the year already open (75).
- Palettes (last 3): Pasagshak sedge under a marine ceiling (73); Senate mahogany and ballot ivory (74); surface plate and layout blue (75).
- Type pairings (last 2): Archivo condensed over Archivo with Instrument Serif (74); Fraunces display over Fraunces text (75).

## Variance dials (moving off the last five: (5?,..) 71, (4,3,3) 72, (3,4,4) 73, (3,3,2) 74, (4,2,5) 75)
DESIGN_VARIANCE 5, VISUAL_DENSITY 4, TYPE_TEMPERATURE 1. Far from house centre in composition, dense, and cool grotesk-led type: the opposite of yesterday's sparse warm serif deck. Dark register (the last light deck was No.72's paper frames, four runs ago, so no light deck).

## Seasonal context, October 3rd
- PFD: 2026 dividend payments go out in October; the amount and energy relief share are live talk.
- Municipal elections October 6th (Fairbanks North Star Borough incl. Proposition 3 hand count; Juneau, Mat-Su, Kenai Peninsula boroughs).
- AFN Convention mid-October; Alaska Day October 18th; general election November 3rd, early voting from October 19th.
- North Pacific Fishery Management Council meets October 5th to 13th in Anchorage (the parked brief); Bering Sea crab openers October 15th.
- Freeze-up on the North Slope and western rivers; aurora season; first snow in the Interior; moose season closing.
- Legislature in interim (convenes January 19th, 2027); Congress out until after the election.
- Federal fiscal year 2027 began October 1st: new grants, rules and comment windows; possible appropriations lapse questions.
- Railbelt winter gas position (Cook Inlet Gas Watch) and utility rate filings are live.

## STANDING WEAKNESS this run attacks
TREND -- scripts/trend_check.py --window 10, 2026-09-23 to 2026-10-02.
  weakest  7/10  mean 7.25   last 6.5    Artwork craft and genuine detail        worked 2026-09-28 (4 runs ago)  <-- STALE
  weakest  1/10  mean 7.35   last 7.0    Variety vs ledger
  weakest  1/10  mean 7.5    last 8.0    Legibility and platform fitness
  weakest  1/10  mean 7.75   last 8.0    Deliverable completeness
  HARD FAILS: none in window.
  DEFECT CLASSES THAT KEEP SHIPPING: outside safe zone (4 runs), ragged display line (4), art touching glyphs (3), busy art under text (2), canvas mark near reserved text (2).
  SCORES: 09-25 8.69, 09-26 8.16, 09-27 8.47, 09-28 8.23, 09-29 8.79, 09-30 8.76, 10-01 8.51, 10-02 8.14.

Attacking ARTWORK CRAFT (weakest in 7 of the last 10, last 6.5). Planned at altitude:
1. The lower third is a SURFACE in the CRAFT PLAN, named per frame (No.75's four flat black bands below a datum were one cross-frame defect).
2. Each frame's largest object gets its own modelling named and built first; the masterful depth frame is built and critic-checked before the rest.
3. Text reserves are designed in from the first build (art touching glyphs and canvas-near-reserved-text are the two shipping warns): every headline block gets a measured reserve rect the art routes around.
4. From No.75's retro: put Alaska's own number on the cover or slide 02 (thumb-stop and arc held at 7 when the first state figure arrived on slide 05).

## Effort
CLAUDE_EFFORT=high
