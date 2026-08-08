# SELECTION — 2026-08-08 — Carousel No. 29

## THE DECISION

**The Sitka Tribe of Alaska's AI escapement counter at Redoubt Falls, and the
funding structure that will not pay for it because it works.**

The queued brief in `prompts/NEXT_RUN.md` handed this forward as the default.
It is being run, but not because it was handed forward. This run's own Beat B
found the two primary documents the brief said were missing, and they change the
story from a good one into the strongest candidate in the sweep.

### The thesis, and it belongs to neither neighbour

**The system is not broken, and that is the problem.**

Redoubt Lake is the largest subsistence sockeye fishery in Southeast Alaska,
roughly 35 percent of the region's whole subsistence sockeye harvest. The weir
count there is not a statistic, it is a rationing instrument. It sets how many
sockeye a Sitka household may legally take, it opens the commercial seine
fishery, and it is what lets the Tribe run its community harvest permit. That
count is now produced by a machine vision model in a plastic chute, moving over
solar-powered Starlink to an office 15 miles away, and the man who runs it says
there is no funding for the weir right now.

The reason is the deck. Grant money exists to remediate damaged systems. This
one is not damaged, so it does not qualify. A working instrument that doubled a
household's legal harvest has no funding line precisely because it works.

That is not No.2's thesis and not No.9's. It is about the shape of the money.

### Why it beat the runner-up

The runner-up was strong and lost on one specific thing. See below.

## CRITERIA, IN THE ROUTINE'S ORDER

1. **Concrete Alaska impact.** A household's legal sockeye limit doubled from 50
   to 100 a year, on the record in an ADF&G news release, attributed by the
   Tribe's own resource protection director to the data the weir produces.
   Roughly 35 percent of all Southeast subsistence sockeye passes this one site.
2. **Visual potential.** Three independent geometries, which is rare. The CHUTE,
   a single aperture every fish in a run must pass through one at a time. The
   ESCAPEMENT STAIRCASE, about 800 fish in the early 1980s to about 229,000 in
   2025. The FUNDING LEDGER, a two-column comparison with money on the broken
   side and one $200,000 bar on the working side.
3. **Tangibility.** Fish, a chute, a household freezer, a bear at a weir pool.
4. **Would an Alaskan send this to a coworker.** Yes, and to a tribal council.

## DEDUPE GATE

`python scripts/dedupe_check.py` run with the candidate's entities and keywords.
**Exit 0. No LIKELY DUPLICATE.** Full output read, never tailed. Soft overlaps,
all read:

- **No.2, 2026-07-09, "One river. Two ways to count it. Only one is proven."**
  jaccard 0.081, the strongest. Wood River drone-in-a-box AI salmon counting
  tested against Bristol Bay's human towers. Its thesis was VALIDATION, whether
  the machine can be trusted against a 70-year human baseline. This deck does
  not argue accuracy at all, and deliberately refuses to (see the hard rule
  below). Different river, different agency posture, different question.
- **No.9, 2026-07-17, "No Road Out. Quinhagak Flies Its Own Eyes."**
  jaccard 0.038. Nalaquq, Yup'ik-owned machine vision. Thesis was OWNERSHIP of
  the sensing layer, own the eye rather than rent it. Sitka Tribe is in fact
  RENTING the eye, a British Columbia-built system from the Pacific Salmon
  Foundation, which is the opposite posture and would make writing No.9's thesis
  here factually wrong as well as repetitive.
- **No.19, 2026-07-29, "Not a better fish. More hours."** jaccard 0.033.
  Shinkei's harvesting robot on Cook Inlet boats. Harvest side, not escapement.
- **No.15, 2026-07-23, "Governed First."** jaccard 0.028. Tribal health data
  sovereignty. Shares only the word tribal.

## RUNNER-UP, AND WHY IT LOST

**The University of Alaska Fairbanks $499,000,000 nuclear-proliferation
detection award**, contract W911NF-26-D-A013, announced on war.gov **yesterday,
August 7th**. A cost-no-fee, cost-plus-fixed-fee, firm-fixed-price IDIQ from
Army Contracting Command at Aberdeen Proving Ground, running to August 6th,
2031, **one bid solicited and one received**. UAF's Geophysical Institute holds
the only University Affiliated Research Center in the country charged with the
geophysical detection of nuclear proliferation, and its Wilson Alaska Technical
Center runs nearly two dozen seismic and infrasound arrays worldwide.

It is fresher, larger and more novel against the ledger than the winner, and it
lost on the AI hook.

The contract face does not contain the words artificial intelligence or machine
learning. Beat E flagged this itself and was right to. There IS documented ML at
that centre, and it is remarkable: Alex Witsil generated **28,000 synthetic
infrasound signals** to train explosion-detection models, published in
Geophysical Research Letters (doi 10.1029/2022GL097785), because real large
explosions are too rare to train on. That is a 2022 paper funded by the Defense
Threat Reduction Agency, a different program from the award announced yesterday.

So the honest deck would have to place a half-billion-dollar contract beside a
four-year-old paper and refuse to connect them, and the connection is the only
reason the story is on this page. That is a deck built around a hole. Better to
hold it until either the contract's own statement of work is readable or the
centre publishes something current, and run it properly.

It is queued in `prompts/NEXT_RUN.md` for a later run with exactly that note.

## ALSO CONSIDERED AND RULED OUT

- **Anthropic employees' $372,000 to a candidate for governor.** Lead finding of
  Beat A, Beat D, Beat E and Beat F, so plainly the loudest AI story in Alaska
  this week. `dedupe_check` exit 1, two LIKELY DUPLICATEs, both read in full:
  No.17 (2026-07-25) and No.21 (2026-07-31). No.21's own ledger entry records
  that it disclosed on its cover that it was the second deck on these donors in
  seven days. A third inside fourteen days is a fixation rather than an update,
  and the new material since is reaction to a story this page told twice.
  There is a second reason and it is written into the working notes rather than
  buried. This routine runs on a Claude model built by Anthropic. No.17 and
  No.21 both handled that with disclosure on slide 09 at full headline scale, on
  the cover chip, in the caption and atop the first comment, and that protocol
  works. What it cannot address is a page returning to its own maker's story a
  third time in a fortnight, which is a judgement for the maintainer and not for
  an unattended run. Flagged in the Gmail draft.
- **AIDEA's 19,950 acres near Houston.** Beat A and Beat D lead. Direct
  collision with No.27, two days ago, whose keyword list already carries
  "19,950 acres" and "August 19th comment window". Nothing material has moved.
  The August 13th Houston council vote and the August 19th deadline are both
  carried on the public docket, which is the right surface.
- **STAK Energy's North Slope lease, ADL 422741.** `dedupe_check` exit 1
  against No.16 (2026-07-24), which its own outcome note records was already a
  revisit of No.1. No Final Finding and Decision has issued, so there is no
  third development to report.
- **Kenai Peninsula school AI policy.** LIKELY DUPLICATE of No.12
  (2026-07-20) at jaccard 0.213 with four shared entities. The August 3rd
  screen-time caps are new, but they are a screen-time story rather than an AI
  story.
- **FCC E-Rate cuts, docket 26-133.** Real, fresh and consequential, more than
  $200 million a year to Alaska schools and libraries. It is a connectivity
  story, and putting an AI frame on it would be the frame doing work the facts
  do not support.
- **NSF's $4.74 million rare-earth bioprocessing award to UAA and UAF**
  (August 5th) and **GAIA** (August 1st). Both genuinely AI, both primary
  sourced through the NSF award API, both strong. Held back because No.8
  (2026-07-15) already ran a UAF critical-minerals AI award and No.20
  (2026-07-30) already ran a federal-AI-award-list deck. Two award decks in
  three weeks is enough. Queued as future material.

## HARD RULES THIS DECK INHERITS

1. **THE TWO ACCURACY NUMBERS NEVER MEET.** Jeff Feldpausch's "about a 95%
   confidence interval" is a director speaking loosely in a radio interview and
   is not a published validation result. SalmonVision's 80.2 percent mean
   average precision is a different metric measuring a different thing across 17
   species. No slide may average them, compare them, or let either validate the
   other. Nobody has published a head to head against hand counts at Redoubt,
   and saying so plainly is this deck's honesty beat.
2. **THE GRANT AMOUNT IS NOW KNOWN AND MUST BE USED EXACTLY.** The brief said it
   was unknown. Beat B found it: a U.S. Fish and Wildlife Service FY2024 Tribal
   Wildlife Grant of **$200,000**, titled "Artificial Intelligence for
   Subsistence Salmon Monitoring and Management". That title is a primary
   document with the technology named in it, and it is the single best claim in
   the package. It does not follow that this grant is the weir's operating
   funding, and the deck may not imply it is. Feldpausch says there is no
   funding for the weir NOW; the grant was for installing the system.
3. **THE 229,000 FIGURE IS A 2025 NUMBER, NOT A 2026 ONE.** The brief banned it
   because it looked like an unsourced 2026 count. Beat B read it in full on the
   Ketchikan Daily News reprint of Anna Laffrey's Daily Sitka Sentinel
   reporting, where it is the 2025 weir count. The Sentinel blocks direct
   fetching, so the reprint is the path. If the fact-checker cannot re-verify
   the year, the number does not ship.
4. **THE FISH ARE NOT THE ARGUMENT, THE MONEY IS.** A run this large is a good
   news story and the deck must not become one. The escapement staircase exists
   to make the instrument's value legible, not to celebrate a big year.

## VARIETY DIVERGENCE STATED

Water, motion and a counted stream. The last four heroes were the Head Sheet,
the Open Block, the Traverse and the Unbounded Population, and four of the last
five were a rigid manufactured object under a fixed or near-fixed camera. The
brief flagged the same risk independently. Nothing recent has used flowing
water, a moving population, or a single aperture. Fraunces is out, having run in
both of the last two decks.
