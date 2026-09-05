# SELECTION — Carousel No. 50 — 2026-09-04

## THE DECK

**ADL 234762. Roughly 19,950 acres of state land, about two miles north of
Houston in the Mat-Su, conveyed to AIDEA at no charge under a noncompetitive
public and charitable use conveyance, with a Draft Land Classification Order
that would move about 15,100 of those acres into Settlement. Written comment
closes at 5:00 p.m. Monday, September 14th, 2026.**

### The angle, and it comes from the primary documents rather than from a frame

Three DNR notices govern this conveyance. The original of July 10th, 2026, the
extension of August 19th, 2026, and the meeting notice of August 24th, 2026.
**None of the three contains the phrase data center.** The state's own July
notice does not state an intended use at all beyond the conveyance category.
The August meeting notice gets as far as "to create a multi-use industrial and
energy development district".

The words scalable data centers live in AIDEA's own development plan and in
the reporting about it, not in the document Alaskans are being asked to
comment on. AIDEA has named no tenant, no firm job number, no energy need, no
water use and no buildout plan.

So the deck's argument is about WHAT IS ACTUALLY ON THE TABLE. The thing that
closes on September 14th is a land transfer and a classification order, and
the classification order is the quiet half. Reclassifying about 15,100 acres
from forestry, habitat and water resources to Settlement is the decision that
outlives whichever tenant does or does not arrive, and it is the part nobody
is arguing about, because the argument is about a phrase that is not in the
notice.

This is a position and it is fair. It does not say the district is bad. It
says the document is thin, the classification is the durable part, and the
window is ten days from the run date.

### Why this story

1. **Concrete Alaska impact.** 19,950 acres, roughly 31 square miles, of
   public land, at no charge, two miles north of a town of about 2,000 people,
   on the Parks Highway and the Alaska Railroad, about 60 road miles north of
   Anchorage. Houston, Willow, Meadow Lakes and Big Lake have all objected to
   the process.
2. **Visual potential is the best on the board.** Real ground, in a real
   survey framework (Township 18 North and Township 19 North, Seward
   Meridian), whose CATEGORY is what changes. Land classification is
   inherently a drawable system, a field of named uses being overwritten by
   one. Quantity, geometry and place all present. Note that the claims give
   the parcel's AREA and the townships it lies within, and NOT its boundary,
   so no slide draws one. That constraint turned out to be a gift rather than
   a limit, because it is what pushed the deck toward drawing the ground
   itself instead of a shape on a map.
3. **Tangibility.** A reader can act. Comments to the Division of Mining, Land
   and Water by 5:00 p.m. Monday, September 14th, and DNR's own notice ties
   appeal standing on the Final Finding and Decision to having filed timely
   written comment.
4. **Would an Alaskan send it to a coworker?** More than 2,000 written
   comments have already arrived, per the state's own August 24th notice. The
   answer is measurably yes.

### THE DEDUPE GATE

`python scripts/dedupe_check.py` on this candidate's entities and keywords
exits 0. No LIKELY DUPLICATE. The strongest soft overlap is No.27, 2026-08-06,
"The Land Is On Offer. The Power Is Not.", sharing only the token aidea and the
words acres and comment at a jaccard of 0.051. That deck was about two private
landholders marketing ground and the power they can't supply. This one is
about the state giving public land away and the classification that goes with
it. Different actor, different mechanism, different document.

### CORRECTION, and it matters (caught in the directors room, not by a gate)

An earlier draft of this file said this story has never been a deck. **That was
wrong.** No.14, run date 2026-07-22, was "The Giveaway, Surveyed", on ADL
234762, the same 19,950 acres, the same conveyance, with the hook "31 square
miles of public land. Free." It scored 8.86. The cartographer flagged it out of
`ledger/artwork.json` while I was reading the same ledger for variety
constraints and did not connect it.

The dedupe gate is right to pass. 2026-07-22 is 44 days before this run date,
well outside the 30 day window, so no hard fail fires. The gate is calendar
based and it did its job. The error was mine, in a sentence I wrote from
`ledger/topics.json`'s 30 day slice without reading past it.

**What it changes, and this is why the correction is worth more than the
embarrassment.**

THE ANGLE HAS TO BE, AND IS, GENUINELY DIFFERENT. No.14's angle was the
SUBSIDY. Free ground as pre-payment for AI infrastructure, the giveaway IS the
subsidy, the comment window is the last price control. Its hook was a big
number monument and its motif was a gold cadastral parcel that changed state
every slide.

This deck's angle is the opposite end of the same document. It is about what
the record ACTUALLY SAYS, that none of the three notices contains the phrase
data center (C08), that the state's own words go no further than a multi-use
industrial and energy development district (C09), and that the durable half is
a classification order moving about 15,100 acres out of Forestry, Habitat and
Water Resources into Settlement (C07, C12).

Read against No.14 this deck is in part a CORRECTION of the frame No.14
shipped. That run's own topic line says the district "includes scalable data
centers". Six weeks of verification later, the honest version is that AIDEA's
plan calls its uses "possibilities, not commitments" and that the state's
notices name no use at all. Saying so 44 days on, with a live window, is
better journalism than repeating it.

THE VARIETY COST IS REAL AND IS PAID DELIBERATELY. No.14 used a PLSS section
grid plat register, a section line edge tease, a boreal spruce green palette,
drafting dimension calls, Archivo with JetBrains Mono, and gold RESERVED FOR
THE PARCEL. Any treatment reaching for the survey grid re-runs that deck's
visual system, which is precisely why the cartographer's pitch lost despite
being the sharpest on geography. The winning treatment diverges on every one of
those axes, and gold is deliberately INVERTED, so that in this deck gold never
touches ground and means only the window that is still open.

It IS also tracked on the public docket as `aidea-houston-industrial-park`,
daily since July 17th, which is the tracker doing its job and is not a topic
ledger entry.

## THE RUNNER-UP, and why it lost

**Anchorage funded its police Real Time Crime Center 8 to 4 and postponed the
privacy rules to September 15th.** Fresh, dramatic, named, and the payoff of a
thesis this page already published.

It lost on the dedupe gate, which returned a LIKELY DUPLICATE at jaccard 0.165
with seven shared entities against No.40, 2026-08-25, eleven days ago. No.40's
title was "750 feeds funded. About 15 running. Hearing September 1st." Its
angle was THE ORDER OF OPERATIONS, that a rule is cheap to write while the
machine is still small. The September vote is the answer to that deck's own
question, so it is a legitimate UPDATE and could ship as one.

It is not shipping as one today for two reasons. A second Anchorage
surveillance deck inside eleven days spends the variety budget on the same
subject, the same entities and the same argument, and the reader who saw No.40
gets a rerun with a new final slide. And the outcome is already published,
dated and public on the docket item `anchorage-rtcc-surveillance-ordinance`,
whose September 3rd history note opens "The money passed and the rules did
not." The record is kept. The deck slot is better spent on the door that is
still open.

Held for a future run if the September 15th ordinance produces a real
decision, which would be a genuinely new development rather than the same one
told twice.

## ALSO CONSIDERED

- **FERC accepts the DeepGreen Cook Inlet subsea filing, comments to November
  2nd.** Rich and primary sourced, and it is an update to the 2026-08-21 deck
  fourteen days ago. The November 2nd window is eight weeks out, so there is
  no urgency cost to holding it, and holding it avoids a second data centre
  siting deck in three days.
- **NSF puts $4.7 million into AI for rare earth recovery from coal waste.**
  Clean, primary, and genuinely new. It is a grant story, and the last thirty
  days already carry three of those. Held as a strong candidate for a run that
  needs one.
- **The Cook Inlet gas shortfall as the ceiling on AI load.** This publication
  already runs a daily numeric instrument on exactly that question at
  /gas-watch/, and a deck restating the instrument is weaker than the
  instrument.

## VARIETY DIVERGENCE, stated

Hero structure, atmosphere, continuity device, hook archetype, palette family
and type pairing all diverge from the forbidden windows recorded in plan.md.
The divergence is written in full in the storyboard header. Dials are
design_variance 4, visual_density 3, type_temperature 2, with density
deliberately DOWN from the last four runs so the standing weakness, artwork
craft and genuine detail, gets fewer objects each more completely drawn.

---

# THE DIRECTORS ROOM, and the synthesis

Three lenses, cartographer, field documentarian, historian of the future. All
three came back complete and all three came back with an honest self critique,
which is what made the judging easy.

## What each one won and what each one lost

**THE CARTOGRAPHER** had the sharpest geography on the board and lost on
variety. Its system is a PLSS section grid register, a section line edge tease,
a drafting line voice, a boreal palette and cabinet oblique blocks. That is
No.14's system, on No.14's story, six weeks later. Its own self critique said
so before anyone asked. It also flagged the No.14 collision that this file had
wrong, which is the most valuable single thing any agent did this run.

Kept from it. The GOLD DISCIPLINE, and it is kept in an inverted form. In No.14
gold WAS the parcel, the land at stake. Here gold means only the window that is
still open and it NEVER TOUCHES GROUND, which is both a deliberate divergence
from the earlier deck and a structural guard, because land that is never marked
as a prize can't be drawn as one. Also kept, the SOURCED versus REPORTED
provenance stamps on the data slide, and the LEGEND THAT LOSES ITS NAMES, whose
empty SETTLEMENT swatch argues the whole story with no words at all.

**THE FIELD DOCUMENTARIAN** had the best answer to the standing weakness and
the best accuracy architecture. Its per slide middle ground population table
and its build order rule, draw at full contrast THEN compress toward the far
value, are the most directly useful things produced this run. Its solid versus
phantom line grammar, where a solid stroke means the statement is in a state
notice and a chalk phantom dash means it is proposed or quoted or not yet
stated, carries the deck's whole accuracy structure in the drawing rather than
in a caveat, and it reads at thumb size without a word.

It lost the hero on its own self critique. The ground column it stands in the
left margin is a drawn stratigraphic core, and a drawn core implies somebody
went and pulled one. Nothing in claims.json supports that. Inventing evidence
is worse than being dull, so the device survives as a CLASSIFICATION KEY, which
is what it was always actually doing, and the sampling implication is gone.

Its atmosphere was also declined. A civil twilight sky dome at 3.5 to 1 with
almost no cast shadows is physically right and it removes the strongest craft
lever this bench has, which its own risk section admitted.

**THE HISTORIAN OF THE FUTURE** had the sharpest thesis and the best continuity
device, and it wins both.

THE PAPER GEOMETRY. The only straight lines anywhere in the deck belong to the
state's instrument, and their SHARE OF THE FRAME is the story's own ratio. It
goes 0.1 percent, 1, 6, 0.2, then 76 percent when the classification arrives,
then 9, 14, 78, and back to 0.4 on the close. That column is legible as a
filmstrip on the contact sheet and on every single frame at 432 pixels, and it
is the argument, not an illustration of it.

THE CAMERA THAT PULLS UP. The camera climbs until the tenant is out of frame
and only the category is left, then comes back to the ground for the ask. A
time argument made with a lens.

Its hero lost, and for the same reason the ground column lost. A frost split
erratic is invented. Nothing in the claims puts one on that ground and seven of
nine slides leaned on it.

## THE SYNTHESIS, and what it is

**The historian's argument and devices, built on the field documentarian's
ground, disciplined by the cartographer's gold rule.**

The hero is not an object at all. It is a RELATIONSHIP, and it is the one thing
all three treatments were circling. **The ground carries no strokes anywhere in
this deck, only modelled tone. Every straight line in nine slides belongs to
the document.** The land is drawn and the instrument is ruled, and a reader can
tell them apart from across a room.

That single rule does four jobs at once. It makes the argument without a word.
It forces the middle distance to be BUILT rather than outlined, which is the
standing weakness attacked at its root rather than patched at Phase 9. It makes
the parcel boundary undrawable, because a boundary would need a closed polygon
and the ground has no strokes to make one from. And it makes a data centre
undrawable, because the vocabulary contains no enclosure of any kind.

The ground itself is generic boreal lowland, black spruce on muskeg, kettle
hollows with no outlet, tussock, birch on the drained rises, in the first week
of September. It is drawn from the notice's own township description and it is
NOT a survey, and the deck says so in a provenance line rather than leaving a
reader to assume. That is the historian's own recommended repair, taken.
