# SELECTION — 2026-07-30 — Carousel No. 20

## THE STORY

**Alaska appears exactly once on the federal government's flagship AI project
list, and its one entry is not about hosting AI. It is about keeping Alaska's
own power on.**

On July 22 the Department of Energy posted the Genesis Mission awards list. It
runs 278 rows. Exactly one is Alaska's:

    Wies, Richard | AURORA-AI: Alaska Utility Resilience & Optimization
    using Real-time AI | University of Alaska Fairbanks | Fairbanks | AK

Six days later, Southcentral utility executives said publicly that a winter
like last year's would likely bring rolling blackouts, and that one of them
can no longer guarantee reliable power during normal operation.

## WHY THIS ONE

**1. It inverts the month.** Ten of the last nineteen decks have been some
version of "AI wants Alaska's land, power or water." That framing is correct
and it is also now the only frame in the feed. This story is the same subject
from the opposite end, and it is verified rather than contrarian-for-effect.
The federal AI money that actually landed in Alaska this month is not a data
center. It is one engineering grant about grid reliability.

**2. The sourcing is unusually hard.** The primary document was downloaded and
parsed rather than read off a search result. The row count, the state
distribution and the single Alaska entry were all derived from the PDF itself.
The stakes claims were verified verbatim by the fact-checker on pages it
actually fetched.

**3. It clears the dedupe gate cleanly** (soft overlaps only, no shared
entities with any in-window entry), which the leading alternative did not.

**4. It fits the run's artwork brief exactly.** The subject is a place at
night in winter, which is a FIELD hero with foreground, midground and
background, not another single modelled object. See the art note below.

## WHY NOT THE ALTERNATIVES

**Gas curtailment and Enstar weighing new customers.** RULED OUT at the dedupe
gate. `dedupe_check.py` exited 1 with five LIKELY DUPLICATES. No.4
(2026-07-11) is the same axis and the same thesis shape, 19 days ago. Its
July 28 facts are excellent and they survive here as this deck's STAKES rather
than as its subject, which is the honest use for them.

**The RTO closed subcommittee rooms.** This was the leading candidate going
into the fact-check and it lost its spine there. The fact-checker verified the
three notices and the closed-meeting language verbatim, and verified that the
RTO must file a nondiscriminatory open access transmission tariff. It then
KILLED the connective claim, that the tariff governs large new loads such as
data centers, because no fetched page says it. It also killed SB 250 and
HB 259 entirely, because akleg.gov returned 403 on every path, and those two
bills were the whole "statutory vacuum" leg.

What was left was a true and interesting civic story with no verified AI teeth.
Building the deck anyway would have meant asserting the link the fact-checker
had just refused. Held for a future run, when akleg.gov is reachable and the
bill record can be read. The three notices are logged in scout_merge.md.

**GAIA, the UAF landslide digital twin.** Fully verified, eight primary claims,
and a genuinely good story that will keep. Passed over for ADJACENCY. No single
ledger entry duplicates it, but the neighbourhood has been visited three times
in twenty days: No.3 (07-10) UAF AI volcano monitoring on seismic and InSAR,
No.8 (07-15) an NSF UAF award, No.11 (07-19) a geophysical digital twin whose
angle was "a forecast the ground itself keeps correcting." A fourth
machine-reads-the-Alaska-ground deck inside three weeks is the editorial
repetition the dedupe rule exists to prevent, even though no single entry trips
it. RUNNER-UP, and a strong candidate for a run about ten days out.

**The aviation weather station outage.** Vivid and completely unworked, but it
is an automation and sensing story, not an AI story, and the news core rests on
a single newsroom. The fact-checker verified five claims and flagged the
single-source problem itself.

## THE DEDUPE GATE

`python scripts/dedupe_check.py` on this candidate returned SOFT OVERLAPS ONLY.
Strongest match No.8 (2026-07-15, NSF minerals engine), jaccard 0.05, one
shared entity, and that entity is "University of Alaska Fairbanks". Read in
full. No.8 is a mineral exploration Engine under NSF; this is a DOE grid
resilience award. Different funder, different program, different PI, different
subject. Not a duplicate. No UPDATE reframe needed.

## THE ARTWORK ARGUMENT (carried into the directors room)

Phase 0 named the standing weakness this run attacks: artwork craft, weakest in
8 of the last 10 runs, stuck at 6.90 for three runs running, all three of which
concentrated their craft in one precisely modelled object. This story hands the
deck a way out that is motivated rather than imposed.

- The hero is a PLACE, not an object. The Railbelt at night in winter, seen at
  three camera stations. Foreground ridge in full value range and sharpest
  edges, midground line and town as the one tack sharp focal plane, background
  range fading into cold haze at minimal contrast. That is three value groups
  by construction, which is what the craft refresh said depth actually needs.
- The line voice is NOT drafting instrument. Three consecutive decks used
  dimension calls, leader discipline, phantom dash kits and datum triangles.
  Retired for this run.
- The deck's own subject is light in the dark, which means the artwork can
  carry the thesis without a diagram.

## VARIETY LEDGER CHECK

- Hero structure: THE LIT CORRIDOR, a place hero. NOT the adjudicated margin
  (16), the milled bone register (17), the dead end insulator string (18), or
  the hour column (19). Deliberately a field rather than an object, which
  breaks all four at once.
- Atmosphere: arctic night under a working sky, cold and high chroma with snow
  as a major surface. NOT gallery lit bone (17), sea fog on wet steel (18), or
  sodium on silt (19). Dark ground, since the one light deck per eight runs was
  spent on 07-25.
- Continuity: (A) THE LIST, a register of 278 marks with exactly one gold,
  changing state across the deck until the single mark becomes Fairbanks and
  then becomes the ask. (B) PALETTE ARC, cold blue toward warm interior light
  as the deck turns. NOT the span state machine (18), NOT the hour marker (19).
- Type pairing: Fraunces display, Space Grotesk body, JetBrains Mono
  instrument. Never shipped. NOT Archivo alone plus mono (18), NOT Unbounded
  plus Fraunces body plus mono (19).
- Hook archetype: to be set by the directors room. NOT asymmetry couplet about
  the record (17), NOT locator paradox (18), NOT definitional correction (19).

## VARIANCE DIALS

design_variance 3, visual_density 3, type_temperature 3, as set in plan.md and
deliberately centred against four consecutive runs that reached for a 4 or a 5
and three of which scored 6.90. The difference this run has to make is craft
per square inch across nine slides, not one loud idea.

## RUNNER-UP

GAIA (NSF award 2608510, UAF, starts 2026-08-01). Claims already verified and
carried in claims.json under candidate B so a later run can pick them up
without re-fetching.
