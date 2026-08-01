# SELECTION — 2026-08-01 — Carousel No. 22

## THE DECISION

**The automated screen that moved 3,048 Alaskans to inactive voter status 27 days
before a primary, and what it says about the verification standard Alaska applies
to an automated decision about a person.**

Anchor development, in window: Elections Director Carol Beecher disclosed at a
2026-07-22 legislative hearing that the quarterly cross-match of the voter file
against Division of Motor Vehicles records returned roughly 3,500 flagged names
against a normal quarterly yield of about 200, and that 3,048 registered voters
were moved to inactive status. On 2026-07-29 and 07-30 a bipartisan group of
legislators, including Senate Majority Leader Cathy Giessel and House Speaker
Bryce Edgmon, demanded immediate restoration and called the action illegal. The
primary is 2026-08-18.

## WHY THIS ONE, against the four criteria in order

**(1) Strongest concrete Alaska impact.** 3,048 named-by-the-state Alaskans have
had their registration status changed weeks before they vote, and the fix is a
burden the state placed on them rather than on itself. Nothing else in the sweep
touches individual Alaskans this directly this week.

**(2) Visual potential.** The quantity is a count of PEOPLE, and the counts are
large enough against the usual baseline that three bars on one shared scale draw
the gap without the page asserting a ratio. (This paragraph originally claimed a
"seventeen-fold spike"; all three directors independently refused to print any
multiplier, and they were right. See the CUTS section below.)
The place is the strongest thing here and it is the argument.
The state has not published which boroughs or census areas the 3,048 live in, so
the honest map is a true-projection Alaska with its 29 boroughs and census areas
drawn and UNFILLED. Drawing the map the state has not drawn is both a real
geographic anchor and the thesis in one object. This directly serves the standing
weakness this run is attacking (see plan.md).

**(3) Tangibility.** A person, a letter, a box to check, a questioned ballot.

**(4) Would an Alaskan send this to a coworker?** Yes, and specifically to a
coworker who is naturalized, or who works in elections, or who is about to vote.
It is useful, not just interesting, which is what makes a deck get saved.

## THE HONESTY FIREWALL, and why it is the deck rather than a caveat

**This was not artificial intelligence. It was a records cross-match, and no
fetched source describes a model.** That fact is not a problem to be managed
around, it is the deck's spine. (Placement changed in the directors room. The
cover does NOT say "this wasn't AI", because a cover that corrects the reader's
assumption is the DEFINITIONAL CORRECTION archetype the ledger forbids. The
cover names the missing map; the mechanism is stated plainly on slide 2; the
governance standard lands at the close.)

The argument: Alaska is currently being asked to decide how much authority to
give AI systems. It has 4,700 acres at three military installations on offer for
AI data centers. A candidate for governor wants a moratorium. Its schools are
writing classroom AI policy. Meanwhile the one time this summer that an automated
system made a consequential decision about thousands of Alaskans at once, the
system was the simplest thing in computing, a comparison of two lists, and it
still returned far more than its usual quarterly yield, still changed 3,048
people's status on data the state itself calls probably very old, and still put
the burden of proof on the person rather than on the state. The governance gap is
not in the future. It is measurable now, at 3,048.

A deck that dressed a database join up as AI would violate non-negotiable 1 and
would deserve to be caught. A deck that refuses to, and makes the refusal the
argument, is the honest version and the stronger one. The series has run this
move before and it scores well (No. 8's "the AI is a single unbuilt sentence",
No. 9's "the only real ML is two models").

## DEDUPE GATE — PASSED

`python scripts/dedupe_check.py` returned **EXIT 0, soft overlaps only**, on the
candidate entities and keywords. Strongest match No.21 (2026-07-31) at token
jaccard 0.02, sharing only the word "primary"; No.17 (2026-07-25) at 0.015 on
"election, primary". Both of those decks are about campaign MONEY and the
contribution RULEBOOK. This deck is about voter list maintenance and automated
decision-making, which shares neither subject nor entity set beyond the election
date they happen to sit before. No reframe as an UPDATE is needed; this is a
net-new topic.

Every LIKELY DUPLICATE printed for the runner-up was read in full (below).

## RUNNER-UP, AND WHY IT WAS REJECTED

**Enstar closes the queue to new large customers.** Genuinely the biggest energy
news of the window, and it names data-center interest explicitly.

Rejected on the dedupe gate. `dedupe_check.py` returned **EXIT 1 with SEVEN
LIKELY DUPLICATE matches**, all read in full:

- **No.6 (2026-07-13, 19 days), jaccard 0.143, 5 shared entities.** GVEA's $120M
  turbine vote set explicitly against the Air Force AI data-center land leases.
  Same entity spine (Air Force, Clear, Eielson, JBER, Cook Inlet), same argument
  shape (a power decision framed against AI load).
- **No.4 (2026-07-11), shares Enstar, Hilcorp, John Sims, Cook Inlet.** The Cook
  Inlet gas storage crisis, RCA denying Enstar's Kenai Loop prudency request. The
  storage-shortfall material is the same material.
- **No.10 (2026-07-18).** "Will an Alaska data center raise your power bill",
  on-grid vs off-grid cost allocation. The ratepayer question, already answered.
- **No.20 (2026-07-30, two days ago).** Shares Enstar, Sims, MEA, Izzo AND the
  rolling-blackouts keyword; its own ledger entry cites the blackout warning.
- Plus No.1, No.16 (STAK), No.18 (ratepayer pledge), and soft overlap on No.14
  (AIDEA land).

The Cook Inlet gas and data-center lane has carried **eight of the last 21
decks**. The strongest available reframe was land supply outrunning energy supply
("Alaska keeps offering ground, the gas ran out first"), and even that sits
directly on No.4's and No.10's entities and would have been a ninth deck in the
same lane inside 30 days. The rubric hard-fails a topic repeat without a material
new development framed as an update, and while the Enstar new-customer line IS
new, it is a one-sentence development inside a story this page has told four
times. Held as supporting context; it is genuinely useful as the "what Alaska is
being asked to decide" beat, and one claim from it may appear in the deck.

## OTHER CANDIDATES CONSIDERED AND SET ASIDE

- **Alaska DOT&PF's robot fleet** (Aurora the Spot quadruped at Fairbanks
  International, Archimedes the underwater dock inspector, drone-triggered
  avalanches at Thompson Pass). Primary-sourced, hard numbers, four real
  coordinates, and the best pure-geography story the sweep produced. OUT OF
  WINDOW (2026-06-29) with no news peg. **Queued for a future run** and written
  into scout_merge.md so it is not lost.
- **XPRIZE Wildfire autonomous finals at Nenana** — shipped as No.5 twenty days
  ago; the September verdict is the real peg. Blocked.
- **Bristol Bay drone salmon counting** — shipped as No.2. Blocked.
- **ReconCraft / UForce Magura USVs** — the Alaska tie is contested between
  fetched sources and the Navy award figure could not be fetched. Not shippable.
- **Northrim / Narmi**, **UAF Aug 5 lecture**, **Claude Impact Lab at APU** — too
  thin, single-sourced, or self-referential for this brand.

## GATE STATUS AT SELECTION
Claims gate pending (fact-checker running). Story ships only if it clears
>= 3 verified claims and `scripts/claims_check.py` exits 0.

---

# PHASE 5 — DIRECTORS ROOM, THE SYNTHESIS

Three directors pitched blind under three lenses: **cartographer**, **systems
illustrator**, **cinematographer**. (Run 21 used editorial-essayist,
historian-of-the-future and data-journalist, so the trio is fully rotated. The
cartographer is in the room deliberately, because this run's standing weakness
is the missing geographic anchor and run 21's own retro said a cartographer's
pitch would have beaten its winner on exactly that axis.)

## THE CONVERGENCE, and it is the headline again

All three independently arrived at the same four decisions without seeing each
other's work:

1. **A true-projection Alaska with all 29 boroughs drawn and NOT ONE FILLED**,
   because the state has not published where the 3,048 live. Three directors,
   three lenses, one image.
2. **Unbounded + Manrope + JetBrains Mono**, each verifying independently
   against the full 21-deck ledger audit.
3. **Swiss-manner Imhof relief through `AK.reliefShade`**, three value bands
   keyed to elevation, generalised with a MEDIAN filter and faded back about 50
   percent. Today's craft refresh, implemented three times over.
4. **No fog layer anywhere**, all three reasoning that Imhof's aerial
   perspective is a value rule and not a haze plate.

When a room converges that hard the material is right and the argument is over
(the lesson written down on 2026-07-31). Judgement goes to WHICH organs graft.

## THE WINNER: the cartographer's THE UNFILLED SHEET

Chosen on two grounds, and feasibility is the first of them.

**Feasibility.** The cinematographer's pitch is the most beautiful of the three
and it rests on a per-scanline cartographic ground-plane sampler that exists
nowhere in the library and has never rendered in this container, on its four
most important slides. Its own self-critique says so plainly. Artwork craft has
been the weakest criterion in 8 of the last 10 runs; betting this run's entire
attack on an unproven renderer is how it becomes 9 of 11. The cartographer's
chassis uses `AKGeo.zoomTo` and `AK.reliefShade` exactly as they are documented.

**Honesty.** The systems illustrator's COMPARATOR BED is the richest concept in
the room, and it admits that its platen and time-height record stacks are "my
model of what a join is, not the Division of Elections' process." On a deck
whose entire spine is refusing to overclaim what the machinery did, drawing a
machine the state does not have is the one exposure this deck can least afford.

The cartographer's hero also carries the argument with zero words, which is what
the wordless-claim field exists to force: one located gold point, and everything
else drawn, authoritative and blank.

## GRAFTS ADOPTED

From the **systems illustrator**:
- **The unit-mismatch guard line**, printed on the data slide. Its phrasing is
  better than mine. Shipped as "Three different counts. Don't add them."
- **3,048 stipple marks with nowhere to land**, on the synthesis slide.
- **Density 2 as the deck mean with two declared density-3 data slides**, on the
  argument that a keepable slide's furniture is what makes it savable. Accepted.
- **Giving the counterargument the most generous frame in the deck.** "A page
  that gives its opponent the widest frame is a page that gets believed."

From the **cinematographer**:
- **The equality encoding on the fairness pair.** The two readings are staged at
  identical scale, identical position logic and identical light, so fairness is
  argued by the lighting rather than asserted in copy. Best single idea in the
  room for this deck's credibility.
- **Holding meaning-gold out entirely until it lands**, so its arrival means
  something.
- **Recomputing every `data-encodes` region from the projection and the measured
  boxes at build time**, never shipping a typed constant.

## CUTS, including one the winner asked for

- **CUT: the ghost-coast misregistration** on slides 3 to 5. The cartographer
  named this as its own most-likely-to-be-over-read element and offered the exact
  fallback. On 2026-07-31 a director's accurate self-critique was overridden and
  the scorer later found precisely that weakness. Taking the note this time.
  Slide 3 becomes a clean push to Southcentral with C24 set as type over water.
- **CUT: any multiplier.** All three directors independently refused to print
  "seventeen times". The 200 is names returned (C01), the 3,500 is letters sent
  (C02), the 3,048 is registrations moved (C04), and claims.json warns they are
  different quantities. The showrunner's brief asked for the ratio and the room
  was right to refuse it. Three bars on one shared scale, no ratio asserted.
- **FIXED: station-A repetition.** Slides 1, 5 and 9 all sat at the wide station.
  Per the winner's own recommendation, slide 9 gets a different value key rather
  than a new object, because adding objects is how a density-2 deck becomes a
  density-4 deck with none of the craft.
- **NOT USED:** C14 and C15 appear only as attributed allegation with a printed
  tag; C25 (imputed motive) is dropped entirely; C20 is dropped because it would
  read as evidence of a review step no source establishes.

## VARIANCE DIALS, CONFIRMED
design_variance 4, visual_density 2 (deck mean, with S2 and S9 declared at 3),
type_temperature 2. Zero serif in the deck, which is itself a divergence: twelve
of the last 21 decks led with a serif display.
