# PLAN — Alaska.Ai carousel No. 64, run 2026-09-20

## Wake

run_guard: CLEAR. `runs/2026-09-19` holds No.63, so 2026-09-20 is the first
date with no shipped run directory. Anchorage read 23:08 on September 19th at
wake, which is the hour the date-collision clause was written for; the run
takes the date Anchorage rolls into and `run_state.json` carries the note.

carousel_no = 63 entries in ledger/topics.json + 1 = **64**.

`prompts/NEXT_RUN.md` does not exist. No queued assignment, so story selection
is this run's own.

## Top 5 instincts (confidence >= 0.7), injected into every subagent this run

1. **0.99 machine-qa-is-not-taste** A machine_qa PASS is never composition
   approval. The pixel critics judge composition, hierarchy and collision at
   full size AND at thumb size.
2. **0.99 verify-body-line-count** Sanity-check long body copy line counts
   against fixed-position labels, bars and plates BEFORE rendering. DOM text
   overlaps pass machine QA and fail the eye.
3. **0.98 qa.py's text-collision check is DOM-ONLY.** Any label positioned
   against Canvas or SVG geometry can collide freely and the gate still
   returns green. Anything set against drawn geometry is checked by eye.
4. **0.98 screen-the-light-attach-the-cast** A lit ground is SCREENED over the
   surface, never painted on it, and the cast is an ATTACHED subtraction from
   that lit ground thrown down-light. A painted radial pool centred on the
   object reads as a spotlight with a hole in it.
5. **0.98 a repair can land a bigger defect than the one it fixed**, and only
   a fresh adversarial read catches it. Re-render and re-read every frame that
   was touched, before moving on.

Carried alongside: grain is a small repeating tile (AK.grainTile) and it
returns a DATA URL, not a canvas; `lerpHex` returns `rgb()`, so never nest a
colour helper inside itself; re-run the dedupe gate whenever the candidate
story changes.

## Variety constraints (derived from ledger/artwork.json)

FORBIDDEN this run:

- **Hero structures, last 4.** No.60 nine nadir plan views on one shared areal
  mapping with quantities as cut plates. No.61 the drift line, a continuous
  receding snow-fence structure seen from nine places. No.62 the returned
  apron, a 9720px lateral panorama at constant camera height. No.63 the season
  disc, one machined instrument on a bench in parallel oblique.
- **Atmospheres, last 3.** Lichen plaster and open shadow. Interior August,
  low sun and haze. Nilas, black water and milled ice under a studio key.
- **Continuity devices, last 2.** The tyre track crossing its own impression.
  The disc returning rotated to its agreement face plus a phantom dashed ring.
- **Hook archetypes, last 3.** The center and the remainder. The completed
  contradiction. The quoted absence.
- **Palette families, last 3.** Lichen plaster; interior August; nilas.
- **Type pairings, last 2.** Archivo over Instrument Serif over JetBrains
  Mono. Space Grotesk over Manrope over JetBrains Mono.

The binding observation is not any single entry, it is the SHAPE of all four:
every one of the last four decks is a physical object or surface under a
camera, lit by one key, drawn from a station. A fifth would read as a house
style however new the object was. This run's divergence has to be structural
rather than material.

## Variance dials

- DESIGN_VARIANCE **4**. No.62 ran 4 and No.63 ran high; the correction is not
  to pull toward house centre, because house centre is currently "an object on
  a bench". Four, spent on STRUCTURE rather than on subject matter.
- VISUAL_DENSITY **4**. Deliberately up from No.62's 3. The standing weakness
  is artwork craft and the cheapest read of a low craft score is a thin frame.
  Density here means drawn incident per region, not more elements.
- TYPE_TEMPERATURE **3**. Between No.62's warm serif body (2) and No.63's
  all-grotesk (cool). A serif returns, but as display rather than as body.

## Seasonal Alaska context (September 20th)

Freeze-up is beginning in the north and termination dust is on the Chugach.
The Legislature is OUT of session until January, so `ledger/watch.json` will
normally report zero hearings and that is not a collector failure. The
Fairbanks North Star Borough municipal election is October 6th, which No.48
already covered as Proposition 3. PFD distribution runs early October. Fall
subsistence and moose seasons are open; the commercial salmon season is
closed and the season totals are being published now, which is when
fisheries-model stories become checkable. Wildfire season is over and the
season's acreage figures are final. University semesters are in week five.
Utility and borough budget cycles are opening for the calendar year.

## STANDING WEAKNESS this run deliberately attacks

`python scripts/trend_check.py --window 10`, 2026-09-09 to 2026-09-19:

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  7/10  mean 6.7    last 6.0    Artwork craft and genuine detail        worked 2026-09-14 (4 runs ago)  <-- STALE
  weakest  1/10  mean 6.9    last 6.0    Legibility and platform fitness         worked never (never)  <-- STALE
  weakest  1/10  mean 8.1    last 9.0    Alaska authenticity and local relevance worked 2026-08-05 (37 runs ago)  <-- STALE
  weakest  1/10  mean -      last -      {'name'                                 worked 2026-09-15 (3 runs ago)  <-- STALE

HARD FAILS (0 of 10 runs carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   3 runs  warns:contact shadow                                  latest 2026-09-14
   2 runs  warns:canvas mark near reserved text                  latest 2026-09-11
   2 runs  warns:art touching glyphs                             latest 2026-09-11
   2 runs  warns:top-loaded composition                          latest 2026-09-15

SCORE, most recent runs
  09-11 8.47  09-12 8.72  09-13 8.39  09-14 8.76  09-15 8.61  09-17 8.79  09-18 8.76  09-19 8.36
```

**THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft and genuine detail.**

Read as a design brief rather than a report, this says the deck shipping
tonight will score 6 on artwork craft unless something changes at planning
altitude. Yesterday's scorer named the mechanism precisely enough to act on,
which is rare and should not be wasted: slide 04 "stroked hairlines onto a
gradient" where its own dossier had specified incising the datum and the
markers into a modelled substrate with lit lips and shadowed shoulders. The
plan was right and the build was cheap. The defect is not a taste gap, it is
a BUILD gap between what the dossier described and what the drawing code did.

So the attack is three commitments, made here and enforced in Phase 5:

1. **The hero climbs the rendered ladder.** akthree GPU PBR, or an aksdf
   raymarched panel, finished with the akpost film grade and akcolor OKLCH
   ramps, with a designed Canvas fallback and the snapshot sentinel checked.
   The doctrine already makes this the craft floor for hero slides and the
   last several runs have argued flat instead. Not this run.
2. **No frame is hairlines on a gradient.** Every drawn feature that stands
   for a physical thing is MODELED: a surface with a lit edge and a shadowed
   shoulder, an incision with a bright lip and a dark trough, material with
   tooth. A 1px stroke may be annotation furniture; it may never be the
   object. This is the sentence from yesterday's report, turned into a rule.
3. **Every dossier's field 4a carries modeled tone**, and no frame gets a
   flat plate or a floating hairline as its lower-third answer. The
   `data-breather` escape is spent at most once, declared in the dossier.

Verification that it worked is objective and already in the harness:
`bespoke_check.py` drawn share well clear of its 45 percent floor, zero
`frame_balance` fails, and the scorer's artwork-craft number read back at
Phase 10 against the 6.7 mean it has to beat.

**SECOND TARGET, cheap and measurable.** No.63's second-weakest was
Legibility at 6 of 10, for a reason that is a build slip rather than a
judgement: six content-bearing strings shipped at 17px, half the 24px mobile
floor. This run sets a house floor of **24px for every content-bearing
string and 32px for body**, with sub-24 reserved for `data-decorative`
fixtures. It costs nothing and it is worth 0.07 weight.

## Slide-count and shape intention (pre-story)

Default 9: HOOK, context, point, big-visual breather, point, data slide,
point, synthesis, close. The keepable element and the single ask are planned
from the start rather than discovered. Final count is the directors room's
call once the story is known.
