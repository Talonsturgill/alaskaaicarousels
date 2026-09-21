# SELECTION — Carousel No. 65 — 2026-09-21

## THE PICK

**FERC docket P-15423-000. DeepGreen Cook Inlet SPV, LLC has a live federal
permit application for a 100 megawatt subsea data center on the floor of Cook
Inlet off Nikiski, and the State of Alaska's own energy authority says it was
never contacted and will file to oppose it. Comments, protests and motions to
intervene are due at 5:00 p.m. Eastern on November 2nd.**

## Why this one, against the four criteria in order

**1. Strongest concrete Alaska impact.** A 100 MW load is a large fraction of
Railbelt peak demand, and this one proposes to make its own power from the
tide, cool itself in water that carries salmon, and sell the surplus back into
the grid at Nikiski. It sits in the same inlet whose gas position is tight
enough that Enstar could not supply customers for 18 days this winter at
current delivery rates. Every other data center story in Alaska right now is
about land that might hold one. This is about a specific seabed with a
specific docket number and a specific date.

**2. Visual potential.** The best in weeks, and that matters more than usual
because artwork craft has been the weakest scored criterion in 7 of the last
10 runs. The story is natively a CROSS SECTION: a shoreline at Nikiski, water
from 45 to 166 feet deep, 66 pods on the floor, 330 to 350 turbine rotors in
the column above them, one 3.5-mile cable climbing to the beach. It has a
real geometry, a real quantity and a real place, which is exactly what the
Reuters standard in DESIGN_DOCTRINE section 6 asks for, and it is a MATERIAL
subject (water, sediment, steel in cold salt water) rather than another
drafted instrument on a bench. That is the standing weakness this run said in
plan.md it would attack, and the story hands it to us.

**3. Tangibility.** A reader can picture 66 boxes on the bottom of Cook Inlet.
They can picture a turbine field. They have driven past Nikiski.

**4. Would an Alaskan send this to a coworker?** Yes, and the reason is the
conflict at the centre of it. The Alaska Energy Authority is a state entity
whose own Cook Inlet PowerLink was cited in the applicant's filing, and its
chief executive says the applicant never spoke to them. That is not a
process complaint, it is a state agency saying it was used as a reference
without being asked.

## THE DOOR IS OPEN, AND THAT IS THE DECIDING FACTOR

The docket's four-rooms model asks whether the public has a way in. Today
there are three Alaska compute stories and only one of them has an open door:

| story | the reader's move | status |
|---|---|---|
| ADL 234762, AIDEA's 19,950 acres near Houston | comment to DNR | CLOSED September 14th |
| the governor's race positions | vote | November, and No.51 already took the money angle on September 5th |
| **FERC P-15423-000** | **comment, protest or move to intervene** | **OPEN until November 2nd** |

A publication whose whole product is when a decision lands and whether you
get a say does not lead on the two rooms that are shut.

## THE CANDIDATE THAT NEARLY WON, AND WHY IT DID NOT

**Beat C's NPFMC finding was the strongest single piece of research of the
day and it is killed by the dedupe rule.**

On September 15th the North Pacific Fishery Management Council's partial
coverage committee reviewed NMFS's Draft 2027 Annual Deployment Plan, and
the same agenda carried a machine-learning presentation reporting 96 of 97
Pacific sleeper sharks detected on longline electronic-monitoring video. The
plan's own numbers are excellent deck material: a preliminary budget rising
from $4.75 million to $5.45 million while expected monitored days fall from
22,110 to 20,782, and coverage of retained catch running from 99.96 percent
for Bering trawl down to 14.25 percent for Gulf fixed gear. The scout read
all four primary PDFs. The Council decides October 5th to 13th and the
electronic-monitoring opt-in closes November 1st.

Every one of those is a reason to want it. `dedupe_check.py` returned it at
a token jaccard of 0.168, four shared entities and seven shared keywords,
against **No.52 of September 6th, "Two Instruments, One Line"**, which I read
in full. That deck's own topic line reads, verbatim: "Twelve days later the
North Pacific Council's partial coverage committee reviews the draft 2027
Annual Deployment Plan." The meeting Beat C found IS the meeting No.52
pointed forward to, and No.52's angle was "who pays to watch". A deck built
on the budget going up while the days go down is that same argument with
fresher numbers, which is what the 30-day rule exists to stop.

It could ship as an explicit UPDATE. It should not, for a second reason
No.52 wrote down itself: the fisheries-monitoring well is visibly saturated,
with No.44 on August 29th, No.52 on September 6th and No.57 on September
12th all drawing from it. Three in four weeks is enough.

**It is queued instead.** The Council meets October 5th to 13th and will act
on the plan. That is the moment the story has a DECISION rather than a
committee review, it will be well outside the 30-day window by then, and the
numbers will be final rather than draft. A `prompts/NEXT_RUN.md` brief is
being written for the run that wakes after the Council acts.

## RUNNER-UP

**The AIDEA Houston conveyance.** Genuinely the bigger story by acreage and by
political weight: 19,950 acres, no cost, no appraisal, the reversionary
interest waived, more than 2,100 comments, five Senate Resources Committee
members saying it may fail the public-and-charitable-use test in
AS 38.05.810, and unanimous votes against it from both the Houston City
Council and the Mat-Su Borough Assembly. It loses on one thing only, and it
is the thing that matters most here: the window closed on September 14th, so
the deck would be reporting a fight the reader can no longer join. It stays
tracked on the docket as `aidea-houston-industrial-park`, refreshed this run,
and it is the obvious deck the day DNR issues its final decision.

Second runner-up: the University of Alaska's draft system AI policy, taken to
the Board of Regents in September with no vote and sent back for listening
sessions before a November decision. Cut because No.61 on September 17th was
the UA Generative AI Security Standard, twelve days ago, and a second UA
policy deck inside a fortnight is the dedupe rule's whole point.

## DEDUPE GATE

`python scripts/dedupe_check.py` returned exit 0 with two LIKELY DUPLICATE
flags, both of which I read in full before proceeding, and both of which are
shared-entity artifacts rather than topic collisions:

- **No.54, 2026-09-09**, shares Alaska Energy Authority, Cook Inlet and FERC.
  Its topic is the sentence Executive Order 14421 borrows from 16 U.S.C.
  824o(a)(1) and what it leaves out. Different subject entirely; the three
  shared entities are the vocabulary of Alaska energy, not the story.
- **No.56, 2026-09-11**, shares Cook Inlet and Nikiski. Its topic is gas
  storage reading 7,648,351 Mcf and the Section 1200 interruption clause.
  Same water, different question.

Nothing in the 30-day window covers a subsea data center, a marine
hydrokinetic project, or FERC docket P-15423. The semantic call is mine and
it is CLEAR: this is a new story.

One live constraint the dedupe run surfaced and the deck must respect: **the
Cook Inlet gas position was deck No.56 ten days ago**, so the gas arithmetic
that makes this load matter is allowed ONE slide of context and may not
become the deck's argument.

And **No.51 on September 5th already told the Anthropic donation story**, so
the governor's race is off limits as a frame here even though three scouts
brought it back independently.

## THE WINDOW QUESTION, ANSWERED HONESTLY

The FERC notice published September 4th, which is 17 days back against a
stated 10-day research window. The deck's news peg is not the notice. It is
the September 14th development that the Alaska Energy Authority will file to
intervene and oppose, that ORPC has disclaimed any affiliation, and that the
Kenai Peninsula Borough and two other parties have moved to intervene. That
is inside the window, and the forward date is November 2nd. The cover will
not imply the docket opened this week.

## WHAT THE FACT-CHECKER MUST SETTLE BEFORE ANY OF THIS IS DRAWN

1. The Federal Register notice says "Annual generation: 100 megawatts." A
   megawatt is power and not annual generation, so the deck must print what
   the document prints and must not silently convert it into a
   megawatt-hours figure. If the notice's own units are odd, the deck quotes
   rather than corrects.
2. Whether the turbine count is "approximately 330 to 350" in the notice's
   own words, and whether 66 pods is the notice's figure or a reporter's.
3. The seabed acreage, the depth range and the cable specification, each
   against the notice rather than against coverage.
4. Curtis W. Thayer's quotation verbatim and its attribution.
5. Whether the intervenor list is confirmable. FERC's eLibrary is a
   JavaScript shell that no route reached today, so the motions to intervene
   are currently sourced only to an advocacy tracker and MUST NOT be printed
   as fact unless a second route is found.
6. What a preliminary permit does and does not authorize, which the notice
   states outright and which is the single most important honesty guard in
   this deck. A permit is a study priority, not a construction approval, and
   a deck that lets a reader think a data center is being built would be the
   failure mode here.
