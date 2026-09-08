# SELECTION — 2026-09-07 — Carousel No. 53

## THE DECISION

**The federal AI money with an Alaska name on it is not a data centre. It is an
8(a) contract, and the public's own search for those contracts can't reliably
find them.**

The queued brief in `prompts/NEXT_RUN.md` set this story and made completeness a
PRECONDITION rather than a suggestion. That precondition was tested and it
FAILED, exactly as the brief allowed for, and the failure is a better deck than
the success would have been.

### What the brief asked for and what came back

The brief wanted the pattern proved complete before any total, rank or share
could ship. Beat D re-pulled FPDS with real pagination and returned
**NOT ESTABLISHED, with a proof rather than a suspicion.**

Two findings, and the second is the deck.

**One.** Run No. 52's "implausibly short result sets" were never an FPDS defect.
The feed pages by 10 and the fetch layer's summariser reports only the first 5
or 6 of them. Stepping `start` by 5 recovers the hidden half. That was a reading
artifact and it is now a documented method.

**Two, and this is the spine.** FPDS phrase search is not internally consistent.

| query, vendor state Alaska | records |
|---|---|
| `DESCRIPTION_OF_REQUIREMENT:"ARTIFICIAL INTELLIGENCE"` | 24 |
| `DESCRIPTION_OF_REQUIREMENT:"ARTIFICIAL INTELLIGENCE, AND MACHINE LEARNING"` | 25 |

The second phrase is a strict superset of the first, so its result set must be a
subset. It is not. The narrower query returns more, and it surfaces three
contracts the broad query never shows, the largest of them a **$20,632,119.41**
Pentagon artificial intelligence contract held by a Kodiak village corporation.
Apparent mechanism, fitting four independent cases, a comma immediately after
"ARTIFICIAL INTELLIGENCE" breaks the phrase match.

So the deck publishes no total, no rank, no share and no "most of", precisely as
instructed. It publishes the thing the brief itself named as the honest
fallback, that the full picture is not public, and it can now show WHY with two
reproducible queries.

## WHY THIS STORY, against the criteria in order

**1. Concrete Alaska impact.** A $20.6 million federal AI contract with a Kodiak
village corporation's name on it, a $5.27 million Army CDAO contract performed
in an Anchorage office park, and 30 Koniag-family contract actions signed in
fourteen days across twelve agencies. Money that reaches about 4,700 Alutiiq
shareholders through a $33 dividend, a $1,200 Elder Benefit, a $46 million
settlement trust and a foundation that has written more than 4,000 scholarships.

**2. Visual potential.** Unusually strong and unusually literal. Two places
3,000 miles apart. A seven-year chain of identical contract sentences handed
between corporations with a one-day seam. A fourteen-day calendar with 30 dots
piling against a September 30th wall. And the comma itself, which is a
typographic object, on a deck whose subject is a search that fails on
punctuation. The art can encode the argument with almost no metaphor.

**3. Tangibility.** A comma. A contract that expires two days from now. A
dividend a person receives.

**4. Would an Alaskan send this to a coworker?** This is the strongest yes of
the runner-ups. Beat F established that in the same ten days the Fairbanks
assembly put an AI data centre moratorium on two separate legislative priority
lists, and the opinion pages of the ADN, the News-Miner and Must Read Alaska
carried ZERO data centre or AI items. Nobody in Alaska said anything publicly
about ANCSA federal contracting in the entire window. The deck tells a reader
something about their own state that nobody has told them.

## DEDUPE GATE

`dedupe_check.py` exit 0, soft overlaps only, strongest match jaccard 0.031.
Read in full, that is No.31 (2026-08-12), the AURORA-AI research award, sharing
only the entity "Department of Energy". Koniag, Leisnoi, ANCSA contracting and
8(a) appear nowhere in the 30-day window. **Ships as a new story, not an
update.** No material from the last 30 days is reused.

## THE FAIRNESS, decided here rather than left to the copy room

The brief was explicit and it is right. This goes EARLY and on the face of the
deck, not as a hedge at the end.

All of this is lawful. 8(a) is the mechanism Congress built. ANCSA corporation
profits reach Alaska Native shareholders by design. The deck's question is not
whether any of it is proper. **The question is what "Alaska AI" means**, and
whether a public record that fails on a comma can answer it.

Two things make that fairness precise rather than sentimental, and both ship.

- **The statutory point.** 43 U.S.C. 1606(i) shares 70 percent of timber and
  subsurface revenue across all twelve regional corporations. Services and
  government contracting revenue are NOT covered. Technology earnings are not
  7(i) money, so the return path is narrower and more specific than the
  revenue-sharing story people half remember. Sent to the fact-checker as a
  legal claim to be verified exactly or narrowed.
- **The counterweight, which ships in the deck.** Koniag Government Services
  took a roughly $63 million DHS contract effective August 6th, 2026 to run a
  national ICE call center in Adams, Tennessee. And the register in which
  Alaskans actually litigate this is the Bering Straits shareholder petition,
  102 signatures against roughly $587 million in ICE and Homeland Security
  revenue. A deck that shows only the flattering side of 8(a) revenue reads as a
  brochure, and this audience would notice.

## RUNNER-UP, and why it lost

**The FERC comment room on DeepGreen's Cook Inlet subsea data centre.** Project
P-15423-000, comments due 5:00 p.m. Eastern November 2nd, 2026, roughly 330 to
350 tidal turbines and 66 subsea compute pods. It is actionable, primary, and
genuinely striking.

It lost for two reasons. It is already a docket item and was refreshed against
the Federal Register notice earlier in this same run, so it is a docket update
rather than a fresh carousel topic. And it is another megawatt argument, which
is the exact thing the queued brief exists to step away from after seven of the
last thirty days went to land, grid and data centre capacity.

Also considered and not taken: Rainmaker's cloud seeding over the Kenai (this
page already shipped the 374.3 grams figure), the September 1st NSF and ONR
funding cohort, the Permafrost Discovery Gateway watching 4 million Arctic
lakes, and MIT Lincoln Laboratory's through-ice link at Utqiagvik.

## HARD CONSTRAINTS CARRIED INTO THE DIRECTORS ROOM

1. **No total, no rank, no share, no "most of", no "the largest".** Counts of
   what a NAMED QUERY RETURNS are allowed and must be labelled as that.
2. **The Leisnoi parent link is the softest fact in the deck.** If the
   fact-checker can't source Leisnoi Professional Services LLC to Leisnoi, Inc.
   of Woody Island, the deck says "an Anchorage-registered firm named Leisnoi"
   and drops the village corporation frame from every slide.
3. **Nothing may imply any specific contract has been reviewed** under the
   Pentagon's 8(a) threshold. The arithmetic of $632,119.41 above a line is
   fair; a suggestion of consequence is not.
4. **No claim that the Fairbanks ballot carries a data centre measure.** It does
   not. Proposition 3 is a ballot hand count measure.
5. The deck is about a RECORD, so every number on every slide carries a
   claim-id, and the two FPDS queries appear on the slide that makes the
   inconsistency argument so a reader can run them.
