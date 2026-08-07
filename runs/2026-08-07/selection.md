# SELECTION — 2026-08-07 — Carousel No. 28

## THE STORY

**Alaska's Division of Elections has told legislators that more than 600 of the
roughly 3,000 people it moved off the active voter list were U.S. citizens, and
it has paused the DMV comparison that flagged them. The primary is August 18th.
About 1,900 of those people have not responded to the notice at all.**

Elections Director Carol Beecher's letter to lawmakers was posted August 6th,
2026. Alaska Beacon reported its contents August 7th.

## SHIPPED AS AN EXPLICIT UPDATE

This is an UPDATE to **No.22, 2026-08-01, "Where Are the 3,048? The Map Alaska
Hasn't Drawn."** That is six days ago and well inside the 30-day window, so the
update framing is mandatory and goes on the cover, exactly as No.21 did when it
updated No.17 seven days later.

No.22 asked where the 3,048 were and argued that the burden of proving the match
wrong had been placed on the person. **The state has now answered part of its own
question, and the answer is a number.** More than 600 were citizens. That is the
material new development, and it is the strongest kind, because it is the
deciding body correcting its own record rather than a critic alleging something.

### The thesis must NOT be No.22's thesis

No.22's spine was THE VERIFICATION BAR, that a comparison of two lists changed
3,048 people's status and left them to prove it wrong. This deck cannot repeat
that or it is the same deck twice.

**THIS DECK'S SPINE IS WHAT HAPPENS WHEN THE BURDEN LANDS ON THE PERSON AND THE
PERSON DOES NOT ANSWER.** The correction only found the people who wrote back.
About 685 contacted the Division and more than 600 of them turned out to be
citizens. About 350 notices came back undeliverable. Roughly 1,900 said nothing
at all, and nobody knows which of those are citizens because the only instrument
that would find out is a reply. The state has stopped running the match. It has
not, on the record so far, restored the silent ones.

Working title direction, the number that is NOT known is the subject.

## WHY THIS STORY, AGAINST THE FIELD

Criteria in the routine's order.

**(1) Strongest concrete Alaska impact.** Roughly 1,900 Alaskans may arrive at a
precinct on August 18th and find they are not on the register, eleven days from
this run. Nothing else in the six beats is actionable inside two weeks.

**(2) Visual potential.** Very high, and it is a QUANTITY story with a residual
shape rather than a map story. The fan of one population into four outcomes
(replied and vindicated, replied and cancelled, undeliverable, silent) with the
silent block dwarfing the rest. The scale jump from 2,000 records compared in
2024 to more than 580,000 this year is a single-glance graphic. The honest form
is the residual, not the coastline.

**(3) Tangibility.** Maximum. "You may not be registered and may not know."

**(4) Would an Alaskan send this to a coworker.** Yes, and they would send it
today rather than admire it.

## THE RUNNER-UP, AND IT IS QUEUED FOR TOMORROW

**The Sitka Tribe of Alaska has put what its resource director believes is the
first AI video escapement counter in Alaska into the water at Redoubt Falls**,
15 miles by boat from Sitka, over solar-powered Starlink, at the largest sockeye
subsistence fishery in Southeast, at a weir he says has no funding right now
(KCAW, August 5th, IN WINDOW, plus SalmonVision's own auditable project site).

It lost on timing, not on quality. It has no deadline attached and it will be
just as good tomorrow, while the voter story expires on August 18th. It is being
written into `prompts/NEXT_RUN.md` so it cannot be lost.

It also needs careful handling that this run has no budget for. It sits between
TWO decks inside the 30-day window, No.2 (2026-07-09, Wood River AI salmon
counting, thesis "only one is proven") and No.9 (2026-07-17, Quinhagak, thesis
"own the eye, don't rent it"). Its own distinct thesis is available and it is
neither of those, that the count is a RATIONING instrument (25 sockeye per
household, 100 a year) produced by a model at a weir with no money, but that
needs a directors room to build, not a paragraph here.

## WHAT WAS KILLED, AND WHY

**Shinkei's PSDN-S salmon robot (Beat E1).** HARD DEDUPE COLLISION. Already
shipped as No.19 on 2026-07-29, nine days ago, headline "Not a better fish. More
hours." The scout found it as fresh July 30th news; the ledger says otherwise.
Caught by reading the dedupe output in full rather than by luck.

**The Anthropic employee donations (Beats F1 and D2).** This is the loudest AI
story in Alaska right now, four outlets, bipartisan heat, and it is ALREADY
COVERED TWICE inside thirteen days, as No.17 (2026-07-25, "On File, Off Record")
and No.21 (2026-07-31, "$500 in the statute. Unlimited in the table."). A third
deck on the same donors would be a re-run, and both prior decks carry a formal
`conflict_of_interest` field in the topics ledger recording that a deck about
Anthropic donations is produced by a routine running on an Anthropic model, with
disclosure on slide 09, the cover chip, the caption and the first comment. That
practice is established and correct; it is simply not needed today, because the
story is spent for now. Beat D's scout independently raised the same flag, which
is worth recording.

**The altered Bernadette Wilson hat image (Beats F4 and E5).** Two scouts reached
it independently and both said kill. One openly partisan outlet, no
corroboration, and the piece itself hedges between "artificial intelligence or
digital manipulation," which is not a finding that a generative model was used.

**Enstar versus HEX (Beat A1).** Genuinely strong and genuinely fresh, 3 Bcf and
"18 days in the middle of winter where I cannot serve any customers." Killed for
this deck because its AI nexus is OUR framing rather than the record's, and the
publication's own rubric scores a local story with an AI sticker at 4 out of 10
on Alaska authenticity for exactly that move. Parked as a future energy deck.

**The NSF AI critical-minerals award (Beat B1).** $4.74 million across UAA and
UAF on August 5th, unreported anywhere, primary-sourced from the NSF Awards API.
Excellent and nearly selected. It lost because the work has not started (it
begins September 1st) and because `dedupe_check` returned it as a LIKELY
DUPLICATE against No.8 (2026-07-15, the NSF Critical Mineral Accelerator Engine,
"It isn't built yet."), which is the same institution, the same federal funder
and the same minerals. It would need an update framing of its own. Parked.

## DEDUPE GATE, EXECUTED

`python scripts/dedupe_check.py` was run for THREE candidates, not one, and every
LIKELY DUPLICATE was read in full from `ledger/topics.json` rather than tailed,
per the standing instinct at confidence 0.95.

- SELECTED candidate: **exit 1, 3 LIKELY DUPLICATES.** Strongest No.22
  (2026-08-01, six days) at token_jaccard 0.113 with 2 shared entities and 9
  shared keywords. Also No.23 (0.037) and No.21 (0.026). No.22, No.21 and No.17
  all read in full. **Resolution, ship as an explicit UPDATE with a material new
  development, stated on the cover.**
- Sitka salmon candidate: exit 0, soft overlaps only, strongest No.2 at 0.118.
  Read in full anyway. Genuinely distinct on place, actor, sensor, fishery and
  maturity, but it needs its own thesis and it is deferred to tomorrow.
- NSF candidate: exit 1, strongest No.8 at 0.069. Parked.

## HONESTY FIREWALL FOR THIS DECK, ARCHITECTURAL

These are not caveats to bolt on at the end. They are the spine, and they carry
forward the firewall No.22 built.

1. **THIS IS NOT AN AI SYSTEM AND THE DECK NEVER SAYS IT IS.** It is an automated
   comparison of two record sets. That is precisely why it belongs on this page,
   and No.22 already made the argument, so this deck states it plainly and does
   not re-argue it at length.
2. **NO ILLEGALITY IS ASSERTED.** That 23 legislators called the removals illegal
   is an allegation and is attributed as one if it appears at all.
3. **NO INTENT, NO MOTIVE, NO PARTISANSHIP.**
4. **THE 1,900 ARE NOT CLAIMED TO BE CITIZENS.** Nobody knows. That unknown is the
   deck's subject and it must be drawn as an unknown, never as a wronged group.
   The moment the art implies 1,900 wronged citizens the deck is asserting
   something no document supports.
5. **THE 3,048 VERSUS 3,058 QUESTION IS THE FACT-CHECKER'S TO RESOLVE** and the
   deck prints whichever it verifies, with the discrepancy acknowledged if both
   are real counts of different things.
6. **NO NUMBER SHIPS THAT THE FACT-CHECKER DID NOT VERIFY**, including anything
   inherited from No.22.

## CONFLICT OF INTEREST

None for this deck. Recorded because the two nearest neighbours in the ledger
both carry one and a reader of the run record should not have to infer its
absence.

## FACT-CHECKER SPAWNED

One `fact-checker`, adversarial, with the full source list, the 3,048 versus
3,058 problem flagged as the single most important item, and a required
`actionable` block establishing what a removed voter can actually do before
August 18th. The deck is worth little if it cannot tell an Alaskan the remedy.
