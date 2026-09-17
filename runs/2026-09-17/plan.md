# RUN PLAN — 2026-09-17 — Carousel No. 61

## Wake state

- Run date: 2026-09-17 (America/Anchorage). `runs/2026-09-17/` does not exist,
  so the date is free. Note: there is no `runs/2026-09-16/`; yesterday's slot is
  a gap in the archive, not a collision.
- carousel_no: 61 (60 entries in ledger/topics.json + 1).
- Engine bootstrapped clean (playwright, pypdf repaired, chromium ok).
- `prompts/NEXT_RUN.md`: absent. No queued assignment; story selection is this
  run's own call.
- `ledger/watch.json` generated 2026-09-16T18:15:08Z. 1 bill observation,
  0 hearings (Legislature out of session, `note_hearings` explains it),
  29 candidates to triage, 0 failed sources.

## TOP 5 INSTINCTS (confidence >= 0.7, injected into every subagent prompt)

1. (0.99) Never treat a machine_qa PASS as composition approval. The pixel
   critics judge composition, hierarchy and collision at full size and at thumb
   size; the gate cannot.
2. (0.98) qa.py's text-collision check is DOM-ONLY. Any label positioned against
   Canvas or SVG geometry can collide freely and the gate still returns PASS.
   Every art-band label ships on an opaque knockout plate by default.
3. (0.98) A lit ground must be SCREENED over the surface, never painted on it,
   and the cast must be an ATTACHED subtraction from that lit ground thrown
   down-light. A painted radial pool centred on an object's own base puts the
   frame's brightest and darkest values concentrically, which reads as a hole in
   a spotlight.
4. (0.99) A generated block pasted into the run record goes stale the moment
   another round runs. Re-sync gate_status at the LAST render, every round.
5. (0.99) Before rendering, sanity-check long serif/body copy line counts against
   any fixed-position labels, bars or plates. DOM text overlaps pass machine QA
   and fail the eye.

Carried from No.60's retro, because both are one round each if missed:
- A halo is not a knockout. Against a ground uniformly brighter than the type,
  only an opaque plate clears "label crossed by art".
- An opaque label on a counted field erases the count. Place and measure the
  labels first, then reject-sample the marks around their rects.

## VARIETY CONSTRAINTS (derived from ledger/artwork.json)

FORBIDDEN hero structures (last 4, runs 57 to 60):
- the occupied station descended (one water column, nine frames on one shared
  depth-to-pixel mapping)
- the unset benchmark (concrete service pad, bronze monument disc, bare punched
  field)
- the hold at altitude (cargo floor, one crate as a $250,000 ISOTYPE unit)
- the model and the plates (nine nadir plan views, cut plates whose AREA is the
  count)

FORBIDDEN atmospheres (last 3): night pour under one work lamp; the hold at
altitude, near black, one key through the cargo door; lichen plaster and open
shadow.

FORBIDDEN continuity devices (last 2): the unit crate ISOTYPE + aperture/camera
station + lit wedge + strap state; the 500 mile geodesic ring + projection line
stamp + running plate tally.

FORBIDDEN hook archetypes (last 3): THE HALF VOTE; THE TWO SUMS; THE CENTER AND
THE REMAINDER.

FORBIDDEN palette families (last 3): night pour and struck bronze; the hold at
altitude; lichen plaster and open shadow.

FORBIDDEN type pairings (last 2): Bricolage Grotesque over Fraunces over
JetBrains Mono; Archivo over Archivo over JetBrains Mono.

Note on the shape of the last four: three of the four were an OBJECT under a
declared key light at low elevation, and the fourth was a nadir map. The
divergence this run owes the ledger is therefore structural and not only
cosmetic. A fifth staged object in raking light would be a re-skin even with a
new palette.

## VARIANCE DIALS (chosen deliberately)

- DESIGN_VARIANCE 3. Runs 53 and 55 sat at 4 and the last four decks have each
  invented a new chassis. A 3 spends the run's effort on execution rather than
  on a fifth novel chassis, which is where the standing weakness actually lives.
- VISUAL_DENSITY 4. The standing defect is a top-loaded composition with a thin
  bottom band. Density is the dial that directly buys modeled tone in the lower
  third.
- TYPE_TEMPERATURE 2. Cool grotesk-forward, diverging from No.60's warm
  Bricolage/Fraunces pairing and from No.58's Instrument Serif.

Base register: dark arctic (default). A light deck is a dial-5 move and No.55
(laid paper and burin) and No.60 (lichen plaster) already spent the light-ground
budget inside the last 8 runs.

## SEASONAL ALASKA CONTEXT (so scouts do not miss the obvious)

- FEDERAL FISCAL YEAR ENDS SEPTEMBER 30TH. Thirteen days out. Grant obligations,
  task orders, contract awards and solicitation closes all surge into this
  window, and an award that must obligate by the 30th is a real forward date.
- Alaska Legislature is OUT OF SESSION until January. Interim committee work and
  the RCA are where state action is.
- Arctic sea ice annual minimum falls in mid-September; the melt-season number
  lands about now.
- Winter heating season approaching, which is the Cook Inlet gas question's
  clock. Utility filings and RCA dockets cluster ahead of it.
- PFD distribution runs early October; the 2026 amount is public by now.
- AFN convention is in October, so Alaska Native organization announcements
  build through late September.
- Fall subsistence and hunting seasons; Bering Sea groundfish and crab
  determinations run into October.
- UAF and UAA fall semester underway, so university research awards and new
  center announcements are live.
- Wildfire season effectively closed; the season-total numbers are final.

## STANDING WEAKNESS — what this run attacks, and how

`python scripts/trend_check.py --window 10`, pasted:

```
TREND -- generated by scripts/trend_check.py over the last 10 scored run(s), 2026-09-05 to 2026-09-15.

REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  'worked' is a text match over ledger/upgrades.json prose, so it can UNDER-report:
  an upgrade that fixed a criterion without naming it reads as 'never'. Check before acting.
  weakest  5/10  mean 6.9    last 7.0    Artwork craft and genuine detail        worked 2026-09-14 (1 run(s) ago)
  weakest  2/10  mean 6.8    last 7.0    Legibility and platform fitness         worked never (never)  <-- STALE
  weakest  1/10  mean 7.4    last 7.0    Deliverable completeness                worked never (never)  <-- STALE
  weakest  1/10  mean 8.1    last 8.0    Alaska authenticity and local relevanc  worked 2026-08-05 (34 run(s) ago)  <-- STALE
  weakest  1/10  mean -      last -      {'name'                                 worked 2026-09-15 (0 run(s) ago)

HARD FAILS (0 of 10 run(s) carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   4 run(s)  warns:top-loaded composition                          latest 2026-09-15
   4 run(s)  warns:canvas mark near reserved text                  latest 2026-09-11
   4 run(s)  warns:art touching glyphs                             latest 2026-09-11
   3 run(s)  warns:busy art under text                             latest 2026-09-09
   3 run(s)  warns:contact shadow                                  latest 2026-09-14

SCORE, most recent runs
  09-07 9.07  09-09 8.47  09-10 8.20  09-11 8.47  09-12 8.72  09-13 8.39  09-14 8.61
```

THE ONE WEAKNESS THIS RUN IS DELIBERATELY ATTACKING: **top-loaded composition**,
the `frame_balance` warn that has shipped in 4 of the last 10 runs and was
present as recently as No.60, which is also the mechanism behind the
artwork-craft criterion being weakest 5 times in 10 at a mean of 6.9.

It is one defect, not two, and the cause is known and written down in
DESIGN_DOCTRINE 1. The bottom band gets composed last, so it gets whatever is
left, and what is left is flat: a hairline, a mono label, a plate. The dossier's
field 4a then legitimizes it, because naming the footer fixture satisfies a
reader of the field but not the rule behind it.

HOW THIS RUN ATTACKS IT, and all three are planning-time moves, not repair-time:

1. **The deck's chassis is chosen so the lower third is load-bearing before any
   copy is written.** Whatever the directors room returns, the winning treatment
   has to be one whose subject lives at the BOTTOM of the frame, so the modeled
   tone down there is the picture rather than a fix applied to it. A staged
   object on a table has its interest at eye level and its shadow at the
   bottom; that shape is exactly what produced four of these warns. The
   selection note will say which treatment wins this test.
2. **Field 4a is graded against the tone, not against the noun.** Every dossier
   names what the bottom band carries AND the value range it carries it in. A
   bullet that names furniture without a tone range gets rewritten at the
   storyboard gate, not at Phase 8.
3. **frame_balance is measured on the FIRST render of every slide, before any
   critic is spawned.** The five-round cap exists because critics were driving
   the run; a defect the machine can measure should never reach a critic. Any
   slide that warns top-loaded on render 1 is rebuilt in the same pass, and the
   rebuild is compositional (move the mass) rather than additive (put something
   down there).

Second target, free because it rides the same decisions: **Legibility and
platform fitness**, weakest 2 of 10, mean 6.8, and NEVER worked on. No.60's
retro measured the cheapest fix in the machine, a 24px mobile floor taking
machine QA from 150 warns to 6 in one pass. This run sets the floor at planning
time in every dossier's type spec rather than discovering it at scoring: no
rendered string below 24px anywhere, and every string that carries a reader
meaning at 26px or above.

## PHASE PLAN

Phase 1 craft refresh runs BEFORE the scouts, per the routine, so the search
budget is not already spent. Six scouts, each capped at 25 WebSearch calls,
with the cap and its reason stated in the brief.
