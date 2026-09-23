# RUN PLAN — Alaska.Ai Carousel No. 66 — September 23rd

## Wake state

- run_guard: CLEAR. New day, not a re-fire. `runs/2026-09-23/` does not exist.
- `runs/2026-09-22/` is absent, so no run fired yesterday. Today is not a duplicate
  of anything and takes its own calendar date.
- carousel_no = 65 topics entries + 1 = **66**.
- `prompts/NEXT_RUN.md` exists and is **PARKED**. Its first instruction is DO NOT USE
  BEFORE OCTOBER 14TH, because the North Pacific Council does not act on the 2027
  Annual Deployment Plan until its October 5th to 13th meeting. The file stays in
  place, is NOT archived this run, and this run selects its own story. Beat C was
  told the Annual Deployment Plan is off limits today.

## Standing weakness, and what this run does about it

`trend_check.py --window 10` (2026-09-11 to 2026-09-21):

```
REPEAT OFFENDERS (criterion, times weakest, mean, last worked on)
  weakest  7/10  mean 6.9  last 7.0  Artwork craft and genuine detail   worked 2026-09-14 (6 runs ago)  <-- STALE
  weakest  1/10  mean 6.9  last 7.0  Legibility and platform fitness    worked never  <-- STALE
  weakest  1/10  mean 8.1  last 8.0  Alaska authenticity and relevance  worked 2026-09-20 (1 run ago)
HARD FAILS: none in this window
DEFECT CLASSES THAT KEEP SHIPPING
   2 runs  warns:contact shadow            latest 2026-09-14
   2 runs  warns:top-loaded composition    latest 2026-09-15
SCORE: 09-13 8.39  09-14 8.76  09-15 8.61  09-17 8.79  09-18 8.76  09-19 8.36  09-20 8.50  09-21 7.98
```

**THE ONE STANDING WEAKNESS THIS RUN ATTACKS: artwork craft and genuine detail.**
Weakest in 7 of the last 10 runs, mean 6.9, and the last run scored 7.98, the lowest
in the window. It is not an incident, it is the house defect.

How, concretely, and decided here in the plan rather than in a Phase 9 repair pass:

1. **The deck's shading idiom is drawn line, not filled rectangle.** Phase 1's craft
   pass landed on CONTOUR HATCHING, where the hatch lines follow the three-dimensional
   contour of the surface rather than running straight, so the line work itself carries
   the form. That is a drawn mark per unit of tone, which is exactly the quantity
   `bespoke_check.py` measures as drawn share. Target a drawn share well clear of the
   45 percent floor, toward the reference deck's 82.
2. **Every frame gets its own drawing function.** No shared `drawTheWholeSlide()`.
   A shared projection or hatch helper is house furniture and is allowed; nine calls
   to one composer is the template failure the gate exists to catch.
3. **Detail at zoom in every region.** The zoom test is the acceptance criterion in
   each dossier, not a global note.
4. **The two recurring machine defects are designed out at build time, not fixed after
   a gate fails.** Contact shadows get a LIT GROUND first and are MEASURED with
   `contact_probe.py` off a real render, never computed off camera arithmetic.
   Composition is deliberately bottom-weighted against the top-loaded warn, and every
   dossier's field 4a names what the lower third CARRIES with modeled tone.

## Variety constraints, derived from ledger/artwork.json

FORBIDDEN this run:

- **hero structures (last 4)**: the returned apron panorama (No.62), the season disc
  (No.63), the jurisdiction section (No.64), the waterline hold (No.65).
- **atmospheres (last 3)**: nilas / black water / milled ice studio (No.63),
  Kachemak stratus at low sun (No.64), flood tide under high overcast (No.65).
- **continuity devices (last 2)**: No.64's notice-path ribbon plus its dated sealing
  ring; No.65's docket staff, its four-level render state, and its edge tease.
- **hook archetypes (last 3)**: the quoted absence (No.63), the vector (No.64),
  the state of matter (No.65).
- **palette families (last 3)**: nilas and milled ice; cold navy over warm cut earth
  with one gold; extinction-to-specular through water, silt and flour.
- **type pairings (last 2)**: Fraunces / Archivo / JetBrains Mono (No.64);
  Unbounded / Instrument Serif / JetBrains Mono (No.65).

Edge tease has now run on three consecutive decks as a continuity device. Treat it as
burned even though the window technically clears it.

## Variance dials, chosen deliberately

- design_variance **5** (No.62 ran 4; the standing weakness is craft, and the answer
  to a craft deficit is not a safe deck)
- visual_density **4** (No.62 ran 3; contour hatching is a dense idiom by nature)
- type_temperature **4** (No.62 ran 2; a warmer, more expressive display face)

## Caption room, burns carried forward

Forbidden right now by the ledger's own divergence windows:

- opening move, differs from last 6, so not: COUNTED THINGS THEN A COUNTED ABSENCE,
  NEW: THE DIRECTIONAL QUESTION, DEFINITION SUBVERSION, CONTRADICTION,
  SECOND PERSON STAKE, THE ABSURD DETAIL.
- structure, differs from last 3, so not: three specifications then the absence then
  the flat correction then the record then one debatable question; Q AND A then three
  beats of record then the ask; Q AND A.
- closing move, differs from last 1, so not: A QUESTION THE DECK ITSELF DOES NOT ANSWER.
- first 4 words, differ from the last 12 entries.
- Every closing-move name in the burn table is spent. A close named NEW: has to BE new.

## Seasonal Alaska context handed to every scout

Freeze-up approaching in the Interior and Arctic, termination dust on the Chugach, the
Legislature out of session and running interim hearings only, fall subsistence and
moose and caribou hunts, Bering Sea crab decisions ahead of October 15 openers, the
2026 Permanent Fund Dividend distributed in early October, the Alaska Federation of
Natives convention mid October, the North Pacific Council meeting October 5th to 13th,
the Arctic sea ice annual minimum announced around now, winter gas supply planning in
Cook Inlet, utility rate cases at the RCA, and **federal fiscal year end on September
30th**, which is when agencies obligate awards and post solicitations. That last one
was flagged hard to Beats B, D and E because it is primary-source rich in this window.

## Research sweep

Six scouts, one per beat, each capped at 25 WebSearch calls with the reason for the cap
stated in the brief, each given `scripts/fetch_pdf_text.py` so a primary-source PDF is
not mistaken for a dead end, each given the 403 host list and the route around it, and
each given the last 30 days of shipped topics for its own beat as an explicit avoid list.
Beat F was given the three reachable community routes in order, since Reddit is not
reachable from this environment.

## Phase 3.6 state at plan time

- CRON HEALTH: FAIL on `gaswatch.yml:completion` and `gaswatch.yml:steps`. Diagnosed
  below. Every other scheduled workflow passed every check.
- GAS WATCH LIVE: FAIL on source freshness and on the collector job.

Both trace to one upstream cause. CINGSA's public dashboard still reads
`09/13/2026 21:00`, and its own operational note announced a semiannual shut-in from
September 14th until September 21st. The dashboard is two days past its announced
return date carrying the same stamp and no extension. Verified live twice today, once
through WebFetch and once by fetching the raw HTML directly, so the staleness is in
the published bytes and not in our parser or a cache. The collector fetched fine,
archived the snapshot, carried NO number forward, wrote an explicit unverified record
and failed loudly, which is the designed behavior. There is no repair on this side.
`gaswatch_incident.json` and `cron_incidents.json` are written with blocker `upstream`;
both gate rows are WARN, the deck ships, and the check resumes tomorrow.
