# RUN PLAN — 2026-08-02 — Carousel No. 23

## Run identity

- run_date: 2026-08-02
- carousel_no: 23 (ledger/topics.json holds 22 entries)
- Trigger fired at 2026-08-02 07:10 UTC, which is 2026-08-01 23:10 Anchorage.
  The Anchorage calendar date at wake was 2026-08-01, but `runs/2026-08-01/`
  is an already-shipped run and CLAUDE.md forbids overwriting shipped run
  artifacts. This firing is therefore the next daily run and takes the date
  2026-08-02, which is also the Anchorage date for nearly the whole of the
  run's execution window. Recorded here so the date is a decision and not an
  accident.
- Research window: 2026-07-23 to 2026-08-02 (last 10 days).

## Queued assignment

`prompts/NEXT_RUN.md` does not exist. No maintainer directive is in force.
Story selection is this run's own (Phase 4).

## Seasonal Alaska context (given to every scout)

- Alaska primary election 2026-08-18. Early voting opens about 2026-08-03.
  Ballot Measure 1 (campaign contribution limits) is on the same ballot.
- Legislature out of session since May. Interim committee hearings only.
- Peak Interior wildfire season, and peak smoke.
- Salmon season late-run. Bristol Bay winding down, Southeast pinks running,
  Cook Inlet late sockeye. In-season management decisions are live right now.
- Peak cruise and tourism season. Peak Arctic shipping season.
- Permafrost active layer at seasonal maximum. Arctic sea-ice minimum in
  September. Summer field season ending, so results and returns are seasonally
  likely.
- Federal fiscal year ends 2026-09-30, so obligations, solicitations and awards
  cluster now.
- Alaska DNR comment window on ADL 234762 (AIDEA, Houston) closes 5 p.m.
  2026-08-19.
- Summer military exercise season at JBER, Eielson, Fort Wainwright, Clear
  Space Force Station, Fort Greely.
- Alaska State Fair opens late August. PFD amount announcement season nears.

## Top instincts injected into every subagent (confidence >= 0.7)

1. Never treat a machine_qa PASS as composition approval. qa.py's text
   collision check is DOM-ONLY, so any label placed against Canvas or SVG
   geometry can collide freely and the gate still returns PASS with zero
   warns. Every art-band label ships on an opaque knockout by default.
2. Size every plate from the MEASURED string, never a guessed constant.
   JetBrains Mono at 24px with 0.10em tracking advances exactly 16.8 px per
   character and the eye estimates about 14, which costs roughly three
   characters per twenty.
3. Never nest a colour helper inside itself. lerpHex and its cousins return
   an `rgb()` string, feeding that into a hex parser returns NaN on every
   channel, and canvas silently keeps the previous fillStyle. A whole region
   renders the wrong colour with no console error and a clean machine gate.
4. Apply grain as a small repeating tile (AK.grainTile), never a full-frame
   feTurbulence rect.
5. Before rendering, sanity-check long serif and body copy line counts against
   any fixed-position labels, bars or plates. DOM text overlaps pass machine
   QA and fail the eye.

## Variety constraints derived from ledger/artwork.json

FORBIDDEN HERO STRUCTURES (last 4, No.19 to No.22)
- No.19 THE HOUR COLUMN. An orthographic two-material quantity column.
- No.20 THE INHABITED DARK. A multiplane winter valley as a PLACE, nine
  camera stations.
- No.21 THE ENGRAVED INSTRUMENT. A lit paper sheet on a copy stand carrying
  white-line intaglio, ten stations.
- No.22 THE UNFILLED SHEET. One true-projection Alaska as an Imhof relief
  sheet, eight stations, boroughs drawn and unfilled.
Note the shape those four share, which is itself now forbidden: ONE object or
sheet, revisited from N camera stations, carrying the whole deck. Three of the
last four decks are that shape and it has scored 6.90, 6.90 and 7.92. This run
does not build a single revisited object.

FORBIDDEN ATMOSPHERES (last 3)
- Ice fog at forty below (20). Copy-stand rake (21). High-altitude sheet
  light (22).
- ALSO BARRED BY THE SCORER, twice: the series' default cold arctic navy
  register. No.20 and No.22 both claimed a distinctive family and both were
  marked down for landing in the house default. A dark ground is required
  (the one-light-deck-per-8-runs allowance was spent at No.17, 2026-07-25,
  six runs ago, so it is not available until No.25), so this run needs a dark
  register that is NOT navy and NOT one of the three above.

FORBIDDEN CONTINUITY DEVICES (last 2)
- No.21 the cancel rule (one oxblood mark changing kind) plus the engraved
  oval.
- No.22 the camera move across one sheet, the registration pair at a fixed
  field, and the edge-tease.
So no registration-mark motif, no camera move across a single object, and
edge-tease is burned for this run.

FORBIDDEN HOOK ARCHETYPES (last 3)
- The direction reversal (20). The dead letter (21). The withheld map (22).

FORBIDDEN PALETTE FAMILIES (last 3)
- Deep-night navy with ice fog and snow (20). Security printing green-black
  (21). Graphite sheet and buff card (22).

FORBIDDEN TYPE PAIRINGS (last 2)
- Instrument Serif + Archivo + JetBrains Mono (21).
- Unbounded + Manrope + JetBrains Mono (22).
Audit any proposed trio against the FULL ledger, not the last four. Two
separate runs proposed trios that had already shipped and claimed novelty.

## Variance dials for this run

- design_variance: 5
- visual_density: 4
- type_temperature: 4

Recent dials were 3/3/3 (No.20) and 4/2/2 (No.22). This run moves all three
and moves density and type temperature in the opposite direction from the last
run on purpose. Density 4 is the dial that matters most against this run's
standing weakness (below): a sparse deck has fewer regions in which to put
craft, and No.22 at density 2 shipped a state that "shaded as one pale mass".

## STANDING WEAKNESS (scripts/trend_check.py --window 10, pasted verbatim)

```
TREND -- generated by scripts/trend_check.py over the last 10 scored run(s), 2026-07-21 to 2026-08-01.

REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  'worked' is a text match over ledger/upgrades.json prose, so it can UNDER-report:
  an upgrade that fixed a criterion without naming it reads as 'never'. Check before acting.
  weakest  8/10  mean 6.38   last 6.0    Artwork craft and genuine detail        worked 2026-07-31 (1 run(s) ago)
  weakest  1/10  mean 6.0    last 6.0    Legibility &amp; platform fitness       worked never (never)  <-- STALE
  weakest  1/10  mean 6.62   last 6.0    Legibility and platform fitness         worked never (never)  <-- STALE

HARD FAILS (3 of 10 run(s) carried one)
   3x  text against geometry       2026-07-25, 2026-07-29, 2026-07-31  <-- RECURRING
   1x  contrast                    2026-07-31

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   3 run(s)  warns:top-loaded composition                          latest 2026-08-01
   2 run(s)  warns:busy art under text                             latest 2026-08-01

SCORE, most recent runs
  07-23 8.90  07-24 8.66  07-25 6.90  07-26 6.90  07-29 6.90  07-30 8.09  07-31 6.90  08-01 7.92
```

### The ONE weakness this run attacks, and how

THE WEAKNESS: **artwork craft and genuine detail**, weakest in 8 of the last
10 runs at mean 6.38, and last at 6.0. Read as a prediction rather than a
report, it says this run's deck will also score 6.0 on craft unless the
mechanism changes.

THE DIAGNOSIS, from the last three retros in their own words:
- No.20: "what did not work was distributed detail: the same uniform-weight
  contour drift and the same knockout plates repeat across six slides, and the
  declared fall-line sastrugi, two-part contact shadows and specular crests are
  not in the pixels."
- No.21: budget was moved from subject count to one generative system, and the
  deck still scored 6.90 with a `text against geometry` hard fail.
- No.22: "the rule itself manufactured the dead lower third", raising the floor
  "traded a dead band for a flat one", and the deck's own signature element
  "does not read at any size".

The common failure is not that these decks have too little machinery. It is
that each builds ONE generative system and runs it at ONE weight across every
region of every slide. Uniform detail is wallpaper. The zoom test asks whether
there is craft in every region; a deck where every region looks like every
other region fails it even when the machinery is elaborate, because there is no
hierarchy for the eye to climb. Three of the last four decks are also literally
the same chassis (one object or sheet, N camera stations), which concentrates
the whole craft budget in one subject and leaves the other regions to a texture
pass.

THE MECHANISM THIS RUN CHANGES, stated now so Phase 5 is bound by it and Phase
9 never has to repair it:

1. **MATERIAL HIERARCHY, declared per region, not per slide.** The deck
   declares THREE distinct material registers with genuinely different detail
   FREQUENCIES (coarse, mid, fine) and different line weights, and every slide
   dossier must name which register carries its foreground, its midground and
   its lower band, and why. A region may not inherit the same register as its
   neighbour by default. This is the direct answer to "the same uniform-weight
   system repeats across six slides": uniformity becomes a thing a dossier has
   to argue for rather than a thing it gets for free.

2. **NOT a single revisited object.** The hero is forbidden from being the
   one-subject-N-stations chassis that carried No.19, No.21 and No.22. The
   craft budget must be spent in at least three genuinely different subjects
   across the deck so that detail is distributed rather than concentrated.

3. **MEASURED KNOCKOUTS OR GENERATIVE RESERVATION, no third option.** This is
   the answer to the recurring `text against geometry` hard fail, which has hit
   3 of the last 10 runs and which qa.py structurally CANNOT see, because its
   collision check is DOM-only. Every string that sits over Canvas or SVG art
   ships either on an opaque knockout sized from the MEASURED string metrics
   after `document.fonts.ready`, or inside a field where the generator's
   density was multiplied by zero with a feathered taper. No label is ever
   positioned by registration against art and hoped for. Phase 8 critics are
   told to check this explicitly because no machine gate can.

4. **The lower band is composed in the dossier, per field 4a**, and it carries
   modeled tone, not a plate or a hairline. `dossier_check.py` enforces the
   field exists; this plan additionally forbids the two cheap answers.

Reactive note carried to Phase 12: the `text against geometry` hard fail is now
3-in-10 and the only reason it keeps shipping is that no machine gate can see
it. That is a gate-shaped hole, and Phase 12 should price building one over any
frontier improvement.

## Phase order for this run

Standard. Phases 0 through 14 as written in prompts/routine_instructions.md.
Six scouts spawned in parallel at wake; craft refresh runs concurrently.
