# SELECTION — Carousel No. 44 — 2026-08-29

## THE STORY

**A machine has been listening off northwest Alaska since July 24th, and one of
the eight things it listens for is not an animal.**

Slocum glider unit 595 is an autonomous underwater glider working a small box in
the Chukchi Sea at roughly 68.63 north, 166.89 west, off the northwest Alaska
coast. It is operated by Oregon State University, the University of Alaska
Fairbanks and Woods Hole Oceanographic Institution, with support from the Alaska
Ocean Observing System and the North Pacific Research Board. It carries a DMON
digital acoustic monitor running the Low Frequency Detection and Classification
System, which tallies classified calls every 15 minutes and transmits them
ashore, where they are posted publicly and reviewed by an analyst each day.

The classifier sorts what it hears into columns defined BEFORE the glider went
in the water. Fin whale, beluga whale, killer whale, bearded seal, bowhead
whale, walrus, AIR GUN, other. Six animals, one industrial sound source, and a
catch all the page defines as "all calls/sounds not found in the call library".

## CORRECTION FROM THE CLAIMS GATE, and it made the deck better

The first read of this selection said "seven animals and a seismic survey". That
is wrong and the fact-checker killed it. Six of the eight are animals (C03). Any
copy asserting seven animals is a hard fail.

It also found something the scout missed and that is now the spine of the deck.
**The project's two published surfaces do not agree on how many things the
machine listens for.** The deployment landing page's daily grid carries eight
class headings including Killer whale (C03). The near real time detection table,
the live one, carries seven and has NO Killer whale column at all (C05). Both
were verified across multiple independent fetches in both directions.

## THE THESIS

**A classifier can only ever report what it was taught to name, and the Arctic
is not obliged to stay inside the list.**

Three beats in the record carry it, and they escalate.

**The list is fixed before the water is listened to.** The call library is
"defined prior to deployment" (C24), and "Other" is by definition everything not
in it (C07). The method is discriminant function analysis published in 2011
(C22, C23), gated at 11 dB above background (C09) and a Mahalanobis distance
under 3 (C10). This is not a learning system. It is a 2016 hull (C20) carrying a
2011 method against a list somebody finished writing before July 24th.

**The list does not even agree with itself.** Eight columns on the project page,
seven in the live table, killer whale present on one and absent from the other.

**So the humans write in the margin.** "check p13-16" on the first day (C36).
"poss single fin whale pulse p3" (C38). "Can't be sure of species" (C37). "odd
PTs. Not walrus. A bit high for KWs but perhaps" (C39). And across 45 minutes on
August 27th, "likely mn" at 19:39 becoming a flat "Mn" at 20:24 (C33, C34), a
code that is not a column on either surface (C30).

The margin is where the Arctic actually gets recorded.

## TWO HONESTY RULES THIS DECK SHIPS WITH

**The deck will NOT name a species for "Mn".** It prints the verbatim code and
says it is not one of the standing columns. Standard cetacean shorthand makes Mn
the humpback, and that is exactly the kind of inference this page does not
publish on someone else's field notes. The honesty is part of the argument.

**The deck will NOT gloss "Air gun" as seismic survey noise.** No fetched page
defines it that way and the fact-checker killed the gloss explicitly. The column
is called Air gun and the deck calls it Air gun. That it sits in the same table
as the bowhead needs no editorial help.

Bowhead, beluga and bearded seal are sourced subsistence species (C40 to C42).
**Walrus is not** and was killed for lack of a source, so the deck names the
three that survived and leaves walrus out of any subsistence sentence, even
though walrus is one of the classifier's own columns.

## WHY THIS ONE, against the four criteria in order

1. **Concrete Alaska impact.** Bowhead, beluga, walrus and bearded seal are
   subsistence species for Point Hope, Point Lay, Kivalina and Kotzebue. This is
   a machine counting the animals those communities eat, and counting the
   industrial noise in the same water, on a page anyone can open the same day.
2. **Visual potential.** Very high, and unusually literal. There is a real
   object (a glider), a real box of ocean about 5 km on a side, a real coast, a
   36 by 8 grid of days against classes, a 15 minute cadence, a sawtooth dive
   profile, and an amplitude threshold at 11 dB that is itself a drawn line.
   The eighth column being an air gun is a WORDLESS visual claim if the deck
   draws seven of something and one of something else.
3. **Tangibility.** A yellow torpedo with wings, holding station in the Chukchi,
   phoning home every 15 minutes. It is the least abstract AI story in the sweep.
4. **Would an Alaskan send it to a coworker?** North Slope Borough and Northwest
   Arctic Borough wildlife staff, subsistence users, marine mammal researchers,
   and anyone who has argued about seismic survey noise. Yes.

## DEDUPE GATE

`python scripts/dedupe_check.py` run with the full entity and keyword set before
the directors room. **Exit 0, soft overlaps only, no LIKELY DUPLICATE.** Every
soft overlap is either the bare token "University of Alaska Fairbanks" or a
generic word (real, time, arctic, minute, tally). Strongest match was No.43 at
jaccard 0.029.

The two entries worth reading in full were read in full.

- **No.43, 2026-08-28**, the Permafrost Discovery Gateway lake drainage tracker.
  Shares only UAF and the words arctic and real time. Different medium (aerial
  and satellite imagery against underwater acoustics), different subject
  (thawing ground against marine mammals), different thesis (a drained lake as a
  receipt for ice already gone). Not a duplicate.
- **No.29, 2026-08-08**, the Sitka Tribe's AI video escapement counter at
  Redoubt Lake. The real thematic cousin, since both are machine counters whose
  output touches a subsistence resource, and the only shared keyword is
  "subsistence". Still clearly distinct. No.29's thesis is THE SHAPE OF THE
  MONEY, a working instrument disqualified from funding by working, and it
  deliberately refuses the accuracy argument. This deck's thesis is about the
  SCHEMA, what a classifier was built to be able to see. Different animal,
  different sensing modality, different region, different operator, different
  argument. Not a duplicate.

No UPDATE framing is needed. This is a new story.

## RUNNERS UP, and why not

- **FAA BEYOND Phase 2** (announced August 27th, 2026, up to eight new lead
  participants on top of the original eight, UAF among the incumbents,
  proposals reported due September 10th). Genuinely strong, in window, with a
  real forward date a reader can act on. Held as the fallback story and being
  verified alongside the primary. It loses on visual potential, since it is a
  program structure rather than a physical thing in a real place, and this run
  is deliberately spending its effort on artwork craft.
- **UAF's Arctic and Homeland Defense Center**, renamed under a five-year
  agreement announced August 19th. Institutionally important, but the scout
  found the announcement names no AI, autonomy or uncrewed system, so it would
  be an Alaska plus institutions story rather than Alaska plus AI. Third
  fallback only.
- **The Mat-Su AIDEA land conveyance** and **DeepGreen's Cook Inlet filing** are
  both live and both loud in community discussion, and both are already shipped
  decks (No.37 and No.39) and tracked docket items. Not eligible.
- **Rural Health Transformation Program technology awards** would be an update
  to No.35 and the scout's own confidence is low, with the drone and AI line
  items resting on a single outlet the department's own release does not carry.
  Not shippable at that sourcing.

## WHAT THE ART HAS TO DO, handed to the directors room

The binding design law for this deck is in `plan.md` and is not negotiable,
because it is this run's attack on the standing weakness. In one line, the type
reserve is a MODELLED NEAR SURFACE at the BOTTOM of the frame, never a plate.

For this story the near surface has an obvious and honest candidate, which the
directors should treat as a strong default rather than a requirement. The
Chukchi shelf is shallow, so a lit silt bed in the near field, with real
material detail, carrying the type, with the water column and the machine above
it receding into dark, satisfies the law and is literally where this story
happens.

One caution the directors must respect. No.42 was THE SOUNDING COLUMN, a
to-scale vertical section of one night's atmosphere with the camera inside the
medium. A vertical water column section is the obvious move here and it is TOO
CLOSE to that. Diverge.
