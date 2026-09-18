# RUN PLAN, 2026-09-18, carousel No. 62

## Wake

`scripts/run_guard.py` returned CLEAR. `runs/2026-09-18/` does not exist, no
run_state was on disk, nothing merged for this date, 61 entries in
`ledger/topics.json`. So this is a new day and the carousel number is 62.

Bootstrap installed playwright, pypdf, img2pdf, pillow and numpy, repaired the
pypdf import, confirmed chromium and mirrored `.claude/settings.json` to the
local scope.

## Cadence and window

The trigger fires daily. Research window is the last 10 days, September 8th to
September 18th. The 30 day topic dedupe is the binding editorial constraint and
every run-based window (variety over the last 4 decks, instincts over 8 runs)
is counted in runs rather than calendar days.

## Seasonal Alaska context handed to every scout

The Legislature is out of session until January, so state activity is interim
committee work, prefiled bills and agency regulation. The federal fiscal year
ends September 30th, which is the dominant fact of this window and puts a heavy
wave of awards, obligations, solicitation closings and contract actions inside
it. Arctic sea ice hit its annual minimum in mid September. Freeze-up is coming
and winter gas planning is live, with CINGSA in its announced semiannual
maintenance shut-in from September 14th to 21st. AFN convention is next month.
The general election is about six weeks out.

## Top instincts injected into every subagent this run

1. A constraint you can't point at is a constraint you invented. This routine
   has no context budget and no token budget, and nothing measures one.
2. Never treat a machine QA pass as composition approval. The gates are blind
   to everything a reader sees first.
3. Any label positioned against canvas or SVG geometry can collide freely and
   the gate still returns PASS with zero warns. Text collision checking is DOM
   only.
4. Before rendering, sanity-check long body copy line counts against every
   fixed-position label, bar and plate. DOM overlaps pass machine QA and fail
   the eye.
5. A generated block pasted into a run record goes stale the moment another
   round runs, so re-sync after every round rather than once.

## Variety constraints derived from ledger/artwork.json

FORBIDDEN HERO STRUCTURES, last 4 decks:
- No.58, the unset benchmark, a green concrete service pad with a bare bronze
  monument disc.
- No.59, the hold at altitude, a cargo floor with one crate as the unit.
- No.60, the model and the plates, nine nadir plan views on one shared conic
  equal area mapping of Alaska with cut plates whose area is the count.
- No.61, the drift line, a Wyoming-pattern snow fence as a continuous receding
  structure seen from nine places.

FORBIDDEN ATMOSPHERES, last 3: the hold at altitude near black under one cargo
door key; lichen plaster and open shadow; blue hour civil twilight on tundra.

FORBIDDEN PALETTE FAMILIES, last 3: the hold at altitude, lichen plaster and
open shadow, blue hour.

FORBIDDEN TYPE PAIRINGS, last 2: Bricolage Grotesque over Fraunces over
JetBrains Mono, and Space Grotesk over Manrope over JetBrains Mono.

FORBIDDEN HOOK ARCHETYPES, last 3: the two sums; the center and the remainder;
and No.61's second-person binding.

Read together, the last four decks are a NIGHT DECK, a NIGHT DECK, a daylight
plan view and a TWILIGHT DECK, and three of the four are one object or one
structure lit by a single hard key. The divergence this run owes the ledger is
therefore a genuinely different LIGHT, not another single-key night scene with
a different prop.

## VARIANCE DIALS

design_variance 4, visual_density 3, type_temperature 2.

Reasoning. No.61 ran dense and cold and No.60 ran dense and warm, so density
comes down a step to leave the artwork room to be looked at rather than
inventoried. Design variance goes up because the standing weakness below is
artwork craft and a cautious deck has never once fixed it. Type temperature
stays cool, because the last two type pairings are both burned and the pairing
this deck picks has to be chosen on the story rather than on temperature.

## THE ONE STANDING WEAKNESS THIS RUN ATTACKS

`scripts/trend_check.py --window 10`, 2026-09-06 to 2026-09-17:

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  6/10  mean 6.8    last 7.0    Artwork craft and genuine detail        worked 2026-09-14 (2 run(s) ago)
  weakest  2/10  mean 6.8    last 7.0    Legibility and platform fitness         worked never (never)  <-- STALE
  weakest  1/10  mean 8.1    last 8.0    Alaska authenticity and local relevanc  worked 2026-08-05 (35 run(s) ago)  <-- STALE
  weakest  1/10  mean -      last -      {'name'                                 worked 2026-09-15 (1 run(s) ago)

HARD FAILS (0 of 10 run(s) carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   4 run(s)  warns:art touching glyphs                             latest 2026-09-11
   3 run(s)  warns:canvas mark near reserved text                  latest 2026-09-11
   3 run(s)  warns:busy art under text                             latest 2026-09-09
   3 run(s)  warns:top-loaded composition                          latest 2026-09-15
   3 run(s)  warns:contact shadow                                  latest 2026-09-14

SCORE, most recent runs
  09-09 8.47  09-10 8.20  09-11 8.47  09-12 8.72  09-13 8.39  09-14 8.76  09-15 8.61  09-17 8.79
```

ARTWORK CRAFT AND GENUINE DETAIL is the target, for the sixth time in ten runs.
Read as a prediction rather than a report, it says this deck will also be
capped there unless something changes in the PLAN, and the four surviving
defect classes say exactly where it goes wrong. Three of the five are one
defect wearing three names. Art touching glyphs, canvas mark near reserved
text and busy art under text are all the same failure, which is TYPE AND ART
COMPETING FOR THE SAME PIXELS, patched after a gate complains instead of
composed from the start.

So the attack is specific and it happens in the Phase 5 dossiers, not in a
Phase 9 repair pass:

1. EVERY DOSSIER DESIGNS ITS TYPE GROUND BEFORE ITS ART. Each slide's layout
   map names the region type occupies and what the art does UNDERNEATH it, as
   a modeled thing (a lit pool, a fall of light, a planed surface, a shadow
   side) and never as a plate, scrim or caption bar. If the art under a
   headline can't be described as a lit surface, the composition is wrong and
   it gets fixed on paper where it is free.
2. THE BOTTOM THIRD CARRIES THE DECK. `dossier_check` already enforces field
   4a and this run treats it as the main event rather than a field to fill.
   Top-loaded composition has shipped in three of ten runs, most recently two
   runs ago, and a deck whose weight sits low fixes that and the dead lower
   zone in one move.
3. DRAWN, NOT BOXED. `bespoke_check` fails a drawn share under 45 percent. This
   deck aims well past that, with a named bench from TECHNIQUE_LIBRARY doing
   the work rather than gradients inside rectangles.
4. CONTACT SHADOWS ARE MEASURED, NEVER COMPUTED. `scripts/contact_probe.py`
   against the render, with the object's own base point, and a LIT GROUND under
   anything that sits on something. The floor is not a target, and a detached
   core reads as a hole.
5. ONE HERO CLIMBS THE RENDERED LADDER, with a designed Canvas fallback and
   the snapshot sentinel checked.

The second row deserves naming even though it is not this run's target.
LEGIBILITY AND PLATFORM FITNESS has been the weakest criterion twice in ten
runs and has NEVER been worked on by any upgrade. That is a Phase 12 candidate
and it goes to the upgrade engineer as one, rather than being quietly carried
into an eleventh run.

## Phases already complete at the time of writing

- Phase 1, craft refresh, done. Two searches, LinkedIn document post
  performance and editorial cartographic shading.
- Phase 2, six scouts out in parallel, each capped at 25 WebSearch calls.
- Phase 3.5, the docket, done and committed. Seven items refreshed, one real
  change, the Kenai Peninsula board adopting both academic honesty documents on
  September 14th, 9 to 0 on the consent agenda.
- Phase 3.6, site sign-off, done and committed. 115 pages, 18 checks, one WARN.
