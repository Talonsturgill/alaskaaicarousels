# SELECTION — Carousel No. 37 — 2026-08-19

## THE STORY

**A poll measures what people want. A vote decides what they get. Both happened
in Alaska this month, nine days apart, and they disagree.**

REVISED AFTER THE FACT-CHECK. The thesis this section originally carried was
"73 percent want a pause and there is no pause anywhere in Alaska." The
fact-checker killed the second half of that sentence, correctly, as an
unbounded negative nobody had established: two jurisdictions were checked out
of one state, nineteen organised boroughs, the unorganised borough and every
incorporated city. What survives is better, because it is an argument rather
than an absence.

Between July 28th and August 4th, Data for Progress asked 605 Alaska likely
voters about pausing new data center development until the state passes a law
regulating it. 73 percent said pause. 63 percent of Republicans said pause
(C01, C02). That is a majority that refuses to split by party on a beat where
everything else in Alaska splits hard.

On August 13th the Houston city council in the Mat-Su had an actual pause in
front of it, an ordinance that would have blocked data center construction
inside city limits. It FAILED, 4 to 2 (C20). The same council the same night
unanimously passed two resolutions objecting to the state's land transfer
PROCESS (C23).

**And the deck's argument is that this is neither hypocrisy nor betrayal.** It
is the difference between a preference and an instrument. A poll aggregates
what people would like. A vote allocates a specific power over a specific
thing, and the room holding one reached for the general tool instead of the
blunt one. Only a small section of the land in question even crosses into
Houston city limits (C30), so the ban would never have reached most of it.
Kent Mitchell said it out loud, that zoning laws stopping anyone doing whatever
they want "solves a problem in the future for multiple industries" (C26).

## WHY THIS ONE

**(1) Strongest concrete Alaska impact.** Not a proposal, not a lease, not a
grant. A measurement of what Alaskans themselves say, statewide, with an N and
a margin of error, in the week they voted. Everything else on the beat this
week is a document about a thing that might happen. This is a number about
what people want.

**(2) Visual potential.** Unusually high and unusually MEASURED, which is what
this run needs:
- a partisan pair that refuses to split, 73 against 63, on a beat where every
  other Alaska number splits hard
- borough crosstabs that are literally the geography of the Railbelt grid a
  data center would plug into (Fairbanks North Star 55, Kenai 51, Mat-Su 46)
- a two point trend on utility worry, 54 to 66, in ten months
- a 4 to 2 tally and two 7 to 0 tallies from one room on one night
- an empty policy shelf, one filled cell against six blank ones
Every one of those is a quantity that can drive a drawn line-density field
rather than a bar chart, which is exactly the standing weakness this run is
attacking (plan.md section 3).

**(3) Tangibility.** A utility bill, a ballot, a council chamber with six
people in it.

**(4) Would an Alaskan send this to a coworker?** Yes, and specifically an
Alaskan of either party, because the 63 percent Republican number is the one
nobody expects.

## DEDUPE GATE

Ran `scripts/dedupe_check.py` TWICE, on two different fingerprints, because
the first fingerprint was wrong and the script told me so.

**First pass**, with the AIDEA parcel in the entity list, returned **2 LIKELY
DUPLICATES**, No.14 at jaccard 0.126 and No.27 at 0.034. Both read in full.

- **No.14 (2026-07-22), "31 square miles of public land. Free."** DNR's
  preliminary decision (ADL 234762) to convey about 19,950 acres north of
  Houston to AIDEA at no cost. Its angle was the giveaway itself, the state
  pre-paying for AI infrastructure with public land.
- **No.27 (2026-08-06), "The Land Is On Offer. The Power Is Not."** Two
  landholders advertising ground for data centers, each listing the power as
  something the site lacks.

The script was right to flag it, and the flag was diagnostic rather than
fatal. It was telling me my own candidate was drifting onto the parcel. So the
candidate got narrowed to what the deck is actually about, the electorate and
the missing instrument, and the parcel came out of the fingerprint.

**Second pass** returned **1 LIKELY DUPLICATE**, No.14 at jaccard 0.081, on
two shared entities (Lisa Johansen, Matanuska-Susitna Borough) and one shared
word ("ban").

**THE SEMANTIC CALL, which is mine and not the script's, is NOT A DUPLICATE.**
No.14's subject is a land conveyance. This deck's subject is a measured public
majority and the absence of any mechanism that answers it. They share a town
and a councilmember's name because Houston is where both happen to sit, the
way DNR and AIDEA appear in nearly every deck on this beat. Jaccard 0.081 is
low and the shared tokens are cast, not thesis.

**THE BINDING CONSTRAINT THIS PUTS ON THE BUILD, and it is a real one.** The
deck does NOT re-tell the parcel. No acreage, no free price, no conveyance
mechanics, no comment window as a subject. Houston enters this deck ONLY
through its August 13th VOTES, which are new, dated inside the window, and are
the sharpest available counter-fact to the 73 percent. The moment a slide
starts explaining 19,950 acres, this deck has become No.14 and the storyboard
gate should kill that slide.

## THE RUNNER-UP, and why it lost

**Every NSF award tagged artificial intelligence that Alaska won in 2026 was
signed inside one 27 day stretch this summer, $8,097,929 across four awards,
all starting between August 1st and September 1st, and neither campus has
announced any of them.** Pulled by Beat B straight off the NSF award API,
which is the kind of unread primary record this studio likes best, with award
numbers, PI names, obligated dollars and abstracts.

It lost on ONE thing, and it is the thing that binds hardest at daily cadence.
Federal AI money landing in Alaska has been the subject of No.20 (Genesis
Mission), No.26 (Administration for Native Americans), No.31 (AURORA-AI's
amount and mechanism), No.33 (NSF 26-513 hubs) and No.35 (Rural Health
Transformation). FIVE decks in three weeks. A sixth is a lane, not an
editorial choice, however good the primary record is. The finding is real and
it keeps; it is logged in scout_merge.md and it should be the first thing a
future run looks at once the money lane has cooled.

Also considered and set aside:
- **The ENSTAR and HEX emergency arbitration** over discretionary gas that
  stopped flowing July 26th. Genuinely new, genuinely numeric, and its AI link
  is contextual rather than direct. Beat A flagged that honestly. A deck built
  on it would have to admit in its own copy that this is not an AI story, and
  that is a bad trade at nine slides.
- **The AKLNG third special session collapse.** Same problem one step further
  out.
- **The Anthropic donations and Ballot Measure 1.** Loudest thing in the local
  conversation and the thing No.17 and No.21 already covered. Beat F's read
  was that the money frame buries the more useful fact, and that is right. The
  primary result enters this deck as ONE supporting beat, on the moratorium
  position rather than on the donors, and the money is not mentioned.

## THE HONESTY THE DECK OWES

Three things, and they are not footnotes, they are slides or they are lines on
slides.

1. **Data for Progress is a progressive polling organisation.** The deck says
   so, on the slide that prints the number. Naming the house is what makes the
   63 percent Republican crosstab load-bearing rather than convenient, because
   it is the number a progressive pollster had the least reason to find.
2. **The primary numbers are preliminary.** About 70 percent of precincts, the
   count runs to August 28th, certification is August 31st (C39, C43). Any
   slide printing 21.8 percent prints "preliminary" beside it. The "283 of 402
   precincts" figure this section originally carried was killed as a back
   calculation neither outlet published.
3. **THE NEGATIVE WAS KILLED AND THE DECK OBEYS IT.** No slide may say a pause
   exists nowhere in Alaska. What the evidence carries is that Alaska has
   adopted no statewide pause, and that no pause has been adopted in the places
   that have voted on one. Slide 08's headline is scoped to the two instruments
   it actually draws.
4. **The Houston vote is single sourced**, to the Mat-Su Sentinel and reporter
   Amy Bushatz. Alaska Public Media and ADN republished it with permission, so
   they are syndication and not corroboration (C20). The slide says so, and the
   deck's tolerance stamp carries SINGLE SOURCED on that sheet.
5. **Three facts the scouts believed are gone.** HB 47 and HCR 3 were killed
   outright for lack of any reachable source, so the deck makes NO claim about
   how many AI laws Alaska has. "About 30 states" is gone; the hedged
   replacement is at least 27 by a count of Public Citizen's own tracker (C33),
   and the solid half is the Alaska half, that no Alaska election deepfake law
   is enacted and SB 64 passed the House with its provision removed (C31, C32).

## VARIANCE DIALS AND THE STANDING WEAKNESS

Dials 4 / 3 / 4 as set in plan.md. The standing weakness under attack is
artwork craft (weakest in 7 of the last 10 runs, mean 6.6), and the method is
line-density as a data channel applied deck-wide rather than one rendered
hero, because two rendered heroes yesterday still scored 7. This story is
unusually well suited to it, since almost every quantity in it is a
PROPORTION, and a proportion is exactly what a hachure or streamline field can
carry honestly in the spacing of its own marks.

---

# PHASE 5 — THE DIRECTORS ROOM, AND THE SYNTHESIS

Three lenses, three complete treatments, judged against the rubric's eyes.

## WHAT EACH ONE BROUGHT

**A, DATA-JOURNALIST, "A Poll Is Not a Ballot", NEW: THE FEATHERED PLATE.**
One idea in this pitch is better than anything else in the room and it is a
DRAWING CONVENTION rather than a picture:

    A poll has a feathered end. A vote has a hard end.

Every polled quantity terminates in a feather whose span IS the margin of
error. Every decided thing (a roll call, an adopted ordinance, a certification
date) has a butt cap at full weight and does not fade. The reader learns it
once, on slide 3, and every later slide is legible in half a second. It is
thesis-as-grammar, it costs zero words, and it survives the 432px downsample.
Its mappings are the most checkable of the three: 605 hairlines, one per
respondent, with the outer 24 at each end fading to nothing because 4 percent
of 605 is 24.2; slide 9's bar with its trailing 30 percent phantom-dashed
because 70 percent of precincts had reported.

**B, SYSTEMS-ILLUSTRATOR, "Six Tools, Six Grips, One Empty Socket".**
Gave the thesis a physical verb, GRIP, and correctly identified that the six
things people call "doing something about data centers" are six different tools
with six different reaches. Also invented the best piece of FURNITURE in the
room, a fixed drafting title block on every sheet carrying the source and its
tolerance (SELF PUBLISHED, PROGRESSIVE. SINGLE SOURCED, MAT-SU SENTINEL.
PRELIMINARY, 70 PERCENT OF PRECINCTS). Honesty as furniture rather than as a
footnote, and it composes the lower-left corner on all nine slides, which is a
free hit on the four-run top-loaded-composition defect.

**C, EDITORIAL-ESSAYIST, "A Poll Is Not an Instrument".**
Two beats nobody else had. First, the single best honesty move of the run: on
the slide that draws 605 respondents as 605 marks, the REPUBLICAN BLOCK REFUSES
TO RESOLVE INTO MARKS and is drawn as a plain bar, because no subgroup n was
published. The drawing declines to draw what the source did not publish, and
says so. Second, and more important editorially, C is the only director who
gave the Houston councillors the best version of their own argument as a WHOLE
SLIDE. The ban reached almost none of the land (C30), so voting it down was a
judgement about instruments rather than a capitulation. Without that beat this
deck is a sneer, and a sneer is not this page's voice.

## THE DECISION

**WINNER, A's FEATHERED PLATE**, as hero structure and as the deck's drawing
grammar, on three counts. It diverges hardest from the four forbidden heroes
(nine discrete plates, each beginning and ending inside its own frame, no
continuous surface and no camera anywhere). It gives every slide a measurable
line system, which is this run's standing-weakness attack. And it is the only
one of the three whose central idea a reader absorbs without accepting a
metaphor first.

**GRAFTED FROM C, two organs, both load-bearing.**
1. The Republican block declining to become marks. Kept exactly, and married to
   A's feather grammar as a double-wide phantom feather.
2. Slide 04, the fairness beat, promoted from an inset in A's slide 2 to a
   slide of its own, which costs A's methods-register slide. C is right that
   this is the beat that earns the thesis, and A's register facts survive on
   slide 3 where they belong anyway.

**GRAFTED FROM B, one organ.** The tolerance title block as fixed furniture on
all nine sheets.

**DECLINED FROM B**, and the reason matters. The six-instrument metaphor is a
translation layer the reader must accept before the deck works, and B named
that risk itself. Six brass objects modelled well is also six chances to ship
clip art. A's slide 08 already makes the same argument in the feather grammar
with no metaphor to buy, by setting three instruments at three heights, one
raised and adopted, one hard-capped and cut, one flush with the ground and
blank.

**UNANIMOUS ACROSS ALL THREE**, which settles it: the keepable slide is the
crossing slope chart, energy affordability at 17 percent on first choice alone
against 39 percent on first or second combined. Three directors reached for the
same frame independently.

## PALETTE, WHERE THE ROOM WAS OVERRULED

A proposed CARBON CROSSTAB, a dark navy with forget-me-not and snow. Read
against the ledger that is a THIRD consecutive dark-blue deck after No.35's
radiograph bone and state blue and No.36's tropopause dusk. C's PROOF PRESS is
the divergent one, warm kraft ink on cool slate with an oxide red, and it suits
type_temperature 4 in a way a cool navy does not. So the deck takes C's palette
and A's SEMANTIC SPLIT, which is the better idea inside it: one ink means
measured, another means decided.

    KRAFT is what was decided. FORGET-ME-NOT is what was measured.
    OXIDE RED is what failed or was removed. GOLD is the one thing to look at.
