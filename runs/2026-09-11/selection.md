# SELECTION — 2026-09-11 — Carousel No. 56

## THE STORY, AS THE FACT-CHECK LEFT IT

**THE THESIS CHANGED AT THE CLAIMS GATE, AND IT GOT BETTER.** The version that
went into the fact-checker said the published curtailment tariff puts large
commercial and industrial ahead of residential. That did not survive. What
survived is sharper.

**There is a rulebook for who loses gas first. It is Section 1200 of Enstar's
tariff, titled Interruption, and it is on Enstar's own website. What it says
about the order reaches the public as a mayor's summary of a meeting.**

Three verified pieces make that argument and the deck needs all three together:

- **C40, primary.** Enstar's own tariff page lists Section 1200, Interruption.
  The section exists. The fact-checker fetched the PDF and it returned as 2.4 MB
  of binary that would not extract to text, so nobody read the priority
  language, and the deck must not pretend anyone did.
- **C20.** Enstar says reductions "would be phased by customer class under the
  utility's tariff, with service to facilities serving human needs and occupancy
  given the highest priority." That establishes the instrument and the principle
  and stops there.
- **C19.** The only public account of WHERE large commercial and industrial sits
  in that order is Kenai Mayor Henry Knackstedt, telling his city council what
  Enstar described to a room of Southcentral mayors on August 21st. Attributed
  to him, not to the tariff.

A data center is a large commercial and industrial customer. Anyone proposing to
site one on Railbelt gas is being placed in an order they can't read, and
neither can the households in the same order.

## THE STORY AS ORIGINALLY FRAMED, kept for the record

**Southcentral Alaska enters the heating season with less gas in the ground than
it wants, and the rulebook for what happens if it runs short is already
written. Large commercial and industrial load is curtailed before households.**

Enstar told a Kenai Peninsula meeting, reported September 10th, 2026, that
regional storage sits roughly 3 Bcf below ideal going into the winter, which the
utility characterises as about 18 days of winter demand at normal to slightly
cold temperatures. The relief is not close. BlueCrest's Cosmopolitan gas, once
expected in early September, has slipped to the first quarter of 2027 at the
earliest, and an LNG import project near Nikiski would not be ready before the
fourth quarter of 2029. If conditions turn extreme the stated sequence is
conservation to 65 degrees, then curtailment of large commercial and industrial
users, then residential.

That sequence is the whole reason this is an AI story rather than only an energy
story. Alaska is being marketed to AI data center developers on the promise of
cheap industrial power, and the published order of cuts already ranks a large
industrial load ahead of a house. Nobody has put those two facts on the same
page.

## WHY THIS ONE

**1. It is the only candidate that cleared the dedupe gate.** Five candidates
were screened with `scripts/dedupe_check.py` and four came back LIKELY
DUPLICATE against entries inside the 30-day window. This one returned soft
overlaps only, strongest No.42 at 15 days with one shared entity and jaccard
0.025. At daily cadence the 30-day rule is the binding editorial constraint and
this run it did most of the selecting.

**2. This page owns a primary measurement nobody else has.** Cook Inlet Gas
Watch has been reading CINGSA's dashboard every morning and keeping the history
CINGSA does not keep. The September 10th reading is 7,648,351 Mcf against a
13,000,000 Mcf design capacity, 58.8 percent, and the published demand model
(version 2.0, MMcf/d = 80.868 + 3.439 x HDD65) puts the modeled peak in the
forecast window at 120 MMcf/d. A story about how much gas Southcentral has is a
story this publication can anchor on its own instrument rather than on a
spokesperson's characterisation, and that is exactly what the Gas Watch was
built for.

**3. It is physical, seasonal and lands today.** Freeze-up is starting. Every
other candidate was a document about a future decision; this is the fuel in the
ground under a region of 400,000 people as the furnaces come on.

**4. The art has real geometry.** A reservoir with a measured level in it, a
calendar of the heating season, an order of cuts that is literally a ladder, and
a relief timeline that runs three winters long.

## THE HONESTY CONSTRAINT, WRITTEN DOWN BEFORE THE DECK IS PLANNED

**This deck does not predict a shortage and must not read as though it does.**
Enstar itself says so and the sentence goes on a slide, not in a footnote. The
published characterisation is a measure of cushion, not a forecast, and a
compressor failure or a warm January can move it either way. CLAUDE.md's Gas
Watch rules forbid the page publishing a safety verdict for precisely this
reason, and while a carousel is a different surface, the discipline is the same
one and the run adopts it voluntarily here.

What the deck asserts is narrower and fully supportable. There is a published
order of cuts. Large commercial and industrial sits above residential in it.
Relief is three winters out. Those are facts about a rulebook and a calendar,
not predictions about weather.

## RUNNER-UP, and why it lost

**FERC opened the comment and intervention window on DeepGreen's 100 MW subsea
data center in Cook Inlet.** Notice published September 4th, 2026, Project No.
P-15423-000, comments and motions to intervene due 5:00 p.m. Eastern on November
2nd, 2026. Primary-sourced from the Federal Register text, a live deadline a
reader can act on, and genuinely new since the last time this page covered it.

It lost on lane exhaustion rather than on quality. No.39 ran DeepGreen's filing
on August 21st and No.54 cited the same FERC permit number on September 9th,
which would make this the third appearance in 22 days, and No.47's own ledger
note already recorded that the data-centre siting lane had carried three decks
in fourteen days and told the next run to change beat.

**It is not being dropped, it is being routed.** The November 2nd deadline is
already tracked in `ledger/docket.json` under
`deepgreen-cook-inlet-subsea-data-center`, carried as a `deadline`-kind key date
and published on the public tracker, which is the surface built for exactly this
and which reaches the reader without spending the day's deck on a third helping.

## OTHER CANDIDATES CONSIDERED AND KILLED

- **GVEA's 34.55 cents a kilowatt-hour and the 4 to 3 turbine vote.** LIKELY
  DUPLICATE against No.47 at 10 days, three shared entities. The rate number
  survives as supporting material here.
- **The gubernatorial forum's data centre split, September 8th.** LIKELY
  DUPLICATE against No.51 at 6 days, four shared entities. Same race, same
  cast, same month.
- **UAA's AI@UAA launch and the 48 GPUs that are the state's whole academic AI
  compute.** LIKELY DUPLICATE against No.41 at 16 days. The 48-GPU figure is
  also 2024 background, not news.
- **The Rural Health Transformation technology slice**, an AI imaging network
  across 21 hospitals, the first robotic surgery in southern Southeast, and a
  94,000 square mile drone pharmacy framework. The richest find of the day and
  burned twice inside the window, No.36 on August 16th and No.45 on August 30th.
  Today's $207 million across 217 projects is an increment on No.45's own
  $181,871,366 across 185.
- **The Navy's Year 9 Arctic acoustic navigation grid.** LIKELY DUPLICATE twice
  over, strongest No.44 at 13 days. Genuinely a different question from No.44's
  classifier story, and still the same sea, the same regulator and the same
  subject matter a fortnight apart.
- **The Railbelt Transmission Organization's closed subcommittees.** Primary,
  in-window, and the scout was honest that No.20 already killed this angle at
  fact-check because nothing connects the tariff to data centres. Nothing found
  this week fixes that. Parked, not used.

## DECK SHAPE, going into the directors room

Nine slides. The arc runs from the measured level, to what the level means as
time, to the rulebook nobody has read aloud, to who is above whom in it, to the
three winters before relief, to the single ask.

The cover carries the measurement, not the alarm.
