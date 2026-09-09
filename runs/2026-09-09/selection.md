# SELECTION — Carousel No. 54 — 2026-09-09

## THE PICK

**Executive Order 14421 and the DOE scope docket that closes October 9th.**

A national emergency was declared on August 26th, 2026 over foreign-made
bulk-power system equipment. The order's stated reason is demand, and it names
artificial intelligence and data centers in its own words. It then defines its
own reach, in its own Section 5(a), around an "interconnected electric energy
transmission network" and transmission rated at 69,000 volts or more, and it
never once says Alaska, Hawaii, islanded or non-contiguous. Today, September
9th, DOE published the Request for Information that will settle what equipment
is actually covered. It asks respondents to name the voltage, capacity and
connectivity thresholds that should draw the line. It also never says Alaska.
Comments close October 9th, 2026, docket DOE-HQ-2026-1123.

## WHY THIS ONE, against the four criteria in order

**1. Strongest concrete Alaska impact.** The Railbelt is not connected to any
grid outside Alaska, so the hinge word in the order's own definition,
"interconnected", is a live question here and settled everywhere else. The
equipment the order names is the equipment Alaska utilities buy, and the
threshold it sets is a number Alaska transmission is on the wrong side of. If
the rule reaches the Railbelt, five utilities inherit a federal procurement
regime designed for a continental grid. If it does not, an emergency justified
by AI electricity demand skips the state where AI electricity demand is the
loudest argument in local politics. Nobody has said which, and there are thirty
days to ask.

**2. Visual potential.** Very high, and in a register this deck has not used.
The story has a threshold (69,000 volts, a hard horizontal line), a topology
(a closed loop that connects to nothing, against a continent that connects to
everything), an inventory (transformers, inverters, storage, relays, breakers,
turbines, control systems, drawn as the physical objects they are), a calendar
(signed the 26th, published the 31st, docketed the 9th, closes the 9th of
October, rules at 120 days), and an absence (a word count of zero, which is a
drawable quantity). The material world is a substation, which is a world this
studio has never drawn.

**3. Tangibility.** Every element is a thing. A transformer is a thing. A
comment deadline is a thing. A voltage is a number on a nameplate.

**4. Would an Alaskan send this to a coworker?** A utility engineer, a
legislative staffer, an RCA practitioner and a data-centre developer would each
send it to a different person, and all four for the same reason, which is that
the answer is not published and the window is open.

## THE DEDUPE GATE

`python scripts/dedupe_check.py` run before the directors room, on the
candidate's entities and keywords. Exit 0, SOFT OVERLAP only, strongest match
No.31 on 2026-08-12 at jaccard 0.043.

The one entry that needed reading in full is No.46, 2026-08-31, the FCC
Universal Service Fund deck, nine days ago. Read in full. It is a different
story and, more importantly, the opposite shape, and this run states the
distinction rather than assuming it.

No.46's angle was that **Alaska is named and treated wrongly**. The FCC's
programs carry Alaska-specific mechanisms, the deck's own line was "Alaska is
the place where the FCC's preferred method does not fit, by design, because
Alaska is not standard", and the argument was about a formula that has an
Alaska carve-out and still misfits.

No.54's angle is that **Alaska is not named at all, in either direction**. There
is no carve-out to critique and no misfit to measure. There are two federal
documents, one of them an emergency declaration, that reach every state with
transmission above 69 kV and are silent about the two states whose grids are not
part of any interconnection. The deck is about a silence and the thirty days
available to break it, not about a formula.

Entities share nothing. FCC, USAC, Rural Health Care Program and Healthcare
Connect Fund against the Executive Office of the President, DOE, CESER, the FAR
Council and the Railbelt utilities. Mechanism shares nothing. A subsidy
administration proceeding against a procurement prohibition under IEEPA.

VERDICT: not a duplicate, and the deck must not reach for No.46's sentence.

## RUNNER-UP

**FERC dockets DeepGreen's Cook Inlet subsea data center, P-15423-000.**

Three of six scouts found it independently, which is the sweep's strongest
confidence signal. FERC accepted the preliminary permit application for filing
and published at 91 FR 56879 on September 4th, putting the first hard
specification on the federal record, 330 to 350 marine hydrokinetic turbines, 66
modular subsea-compute hives, an approximately 3.5-mile 115 kV hybrid power and
fiber-optic armored subsea cable landing at Nikiski, and 100 MW of estimated
annual generation. Comments, motions to intervene and competing applications
close 5:00 p.m. Eastern November 2nd, 2026.

It is a genuinely strong deck and it is the fallback if the claims gate guts the
pick. It loses on two counts. The topic ran on 2026-08-21, nineteen days ago, so
it would have to ship as an explicit UPDATE and spend a slide saying so. And its
newest fact is five days old against a pick whose second document published this
morning.

The runner-up is not wasted. Its 115 kV cable is the single most concrete Alaska
object standing above the order's 69 kV threshold, and it earns a slide inside
the pick as evidence rather than as its own deck.

## WHAT WAS CONSIDERED AND SET DOWN

Eight further candidates are laid out in `scout_merge.md` with the reason each
lost. The three worth naming here, because they are queued rather than dead.

- The Census and NTIA survey notices, both published today, which decide whether
  the only official state-level measurement of AI adoption keeps being taken.
  Fresh, uncovered, quieter. Held for a near run.
- The Alaska Tribal Health System's own published AI governance framework, from
  the International Journal of Circumpolar Health in May. Out of window, and the
  strongest standing lead in the sweep.
- NSF's EPSCoR Graduate Fellowship Program, eighteen awards and no Alaska one.
  Not run, because the scout was honest that this is an absence in a database
  rather than a decision anyone has confirmed, and an absence claim needs a
  source that says no.

## THE FRAME THIS DECK MUST NOT TAKE

It is not an accusation and it must not read as one. Nobody has said Alaska is
out. Nobody has said Alaska is in. The order is nine business days old, the
scope docket opened this morning, and DOE has 120 days to write the rule. The
honest statement is that the question exists, that it has one venue and one
deadline, and that the venue is asking the exact question that would answer it.
A deck that implies bad faith will be wrong within a month and will deserve it.

The counterweight slide is not optional.

---

## WHAT THE CLAIMS GATE CHANGED, appended after Phase 3

The fact-checker returned 41 verified claims, 39 of them primary, and
`claims_check.py` passes. It also killed thirteen things, and four of those
kills change what this deck may say. They are recorded here because the
selection was made on a reading that was partly wrong.

**THE STORY GOT BETTER, and by a lot.** The hinge is no longer a word. It is a
sentence of statute. `16 U.S.C. 824o(k)`, the Federal Power Act's electric
reliability section, carries a subsection headed Alaska and Hawaii whose entire
text is "The provisions of this section do not apply to Alaska or Hawaii." C22
then establishes that the same statute defines the bulk-power system in nearly
the words the order uses. So the order borrows the definition, adds a 69,000
volt sentence the statute does not have, and drops the Alaska sentence the
statute does have. That was verified on two hosts because it carries the deck.

**FOUR CORRECTIONS THIS RUN MUST OBEY.**

1. The DOE docket string is NOT safe to print. The document prints it two ways,
   as `DOE-2026-HQ-2026-1123` in its bracketed header and on regulations.gov,
   and as `DOE-HQ-2026-1123` in its own ADDRESSES prose. The deck cites
   `RIN 1901-AB79`, which is unambiguous, and nothing else.
2. The FERC docket is `Project No. 15423-000`, with no P- prefix. The scouts and
   the earlier commit message both carried `P-15423-000`.
3. The RFI does NOT set the covered scope, and the deck may not say it does. DOE
   says it is seeking information "to inform DOE actions to implement the
   Executive order". The 120 day rulemaking is what sets scope. The window still
   matters, and it is the only published invitation to speak before that rule.
4. The word "interconnected" DOES appear in the order, in the very phrase the
   story turns on. The absence claim is limited to Alaska, Hawaii, islanded and
   non-contiguous, and it may never be widened.

**AND THE COUNTERWEIGHT IS NOW A FACT RATHER THAN A POSTURE.** C31 has the
Alaska Energy Authority describing its own Alaska Intertie as "an integral part
of the interconnected Bulk Electrical System (BES) for the railbelt region",
which is the order's exact term of art applied to the Railbelt by the state
agency that owns the line. Read plainly, that points toward the order reaching
Alaska rather than skipping it. The deck says so. What is missing from the
record is not a carve-out, it is any statement either way, and one window is
open to ask for one.

Two things the sourcing would not carry, and the deck goes without them. There
is no verified statement that the Railbelt is unconnected to any grid outside
Alaska, so the deck uses the Railbelt Reliability Council's own word "islanded"
and its own footprint, which terminates at Alaska communities in all four
directions. And there is no reachable figure for Railbelt peak load, so no peak
load appears anywhere.

---

## THE DIRECTORS ROOM, and the synthesis

Three lenses, rotated off No.53's cartographer, data-journalist and
historian-of-the-future trio: SYSTEMS-ILLUSTRATOR, EDITORIAL-ESSAYIST,
FIELD-DOCUMENTARIAN. All three returned complete treatments. All three
independently converged on the same key, sodium at az 118 el 34 with a 6 to 1
fill, which is the key the run's own prototype proved before any of them read
the plan, and all three converged on a nameplate as the modelled surface the
type sits on. That convergence is a signal, not a coincidence, and it is taken.

**THE WINNER IS THE ESSAYIST'S ARGUMENT, and the room's best idea belongs to it.**
The thesis is a sentence, not a word. Federal law contains thirteen words that
exempt Alaska from the grid reliability regime, the order rebuilds that regime's
definition almost verbatim without carrying them, and one venue is open until
October 9th. The essayist's slide 04, the two definitions set side by side at
identical size, measure, leading and colour, sharing a clause for thirteen words
and then diverging, is the strongest single frame any of the three proposed. The
geometry is the argument and a pixel critic can measure it.

**THE 69 KV DATUM IS THE ROOM'S BEST DEVICE AND IT IS TAKEN WHOLE.** A gold
hairline at a fixed y on all ten slides, above which the order reaches and below
which sits local distribution, which the order excludes and which this deck
always draws as a lit, textured, modelled apron. It makes the frame's own
geometry say what the order says, and it points the deck's craft at the band the
frame-balance gate measures. One correction, computed rather than assumed. The
gate's bottom band is design y 837 to 1269, not 900 to 1350, because it drops a
three-cell safe margin ring first. A datum at 900 sits inside the band and is
legitimate. A dossier claiming it IS the boundary would be wrong.

**THE DOCUMENTARIAN FOUND THE CRACK IN ALL THREE TREATMENTS, INCLUDING ITS OWN.**
Every director built the hinge as two engraved metal plates, and its self
critique says so plainly. There is no engraved Federal Power Act nameplate on any
transformer in Alaska. It is a metaphor rendered in documentary language, and a
deck whose whole authority is that its objects are real can't afford one. So the
hinge reverts to the essayist's version, which was always the honest one, two
columns of type on the document material each speaker actually uses. The statute
is a page. The order is a page. The equipment is steel. Nothing is invented.

**FOUR SELF CRITIQUES ACCEPTED, all four from the directors themselves.**

1. The essayist's, that four materials are four greys at 432px and the palette
   was being asked to carry a distinction the copy already states. Cut to THREE.
   Struck steel for equipment, printed page for the order and the docket and the
   statute, and Alaska's own institutional voice as forget-me-not engraved on the
   same steel. Phenolic is gone.
2. The essayist's, that a four-row ladder is thin for a slide claiming to be the
   save. Fixed by the documentarian's own remedy below.
3. The documentarian's, that ten frames of metal and paper leave the state
   itself undrawn, and that a deck arguing about 700 miles of grid without ever
   drawing the 700 miles is asking a placard to do a map's job. Accepted, and its
   own cheapest fix is taken. Slide 07's gauge board carries a printed Railbelt
   strip from Fairbanks and Delta Junction to Homer and Seldovia beside the
   voltage ladder. That buys the geography back on the one slide people
   screenshot and fixes the thin ladder in the same move.
4. The systems-illustrator's, that three of its ten frames were one frame
   repeated. Three materials and a hard register shift between the yard and the
   bench answer it, and the contact sheet is where it gets checked.

**WHAT EACH LENS CONTRIBUTED TO THE SHIPPED PLAN.**

- ESSAYIST: the thesis, the title, the hook archetype, every on-slide string, the
  69 kV datum and its state table, slide 04, the counterweight drawn as a balance
  at equal weight and equal rule length, and the DeepGreen row drawn phantom
  dashed because a preliminary permit is a study permit and solid would lie.
- SYSTEMS-ILLUSTRATOR: the material discipline. One reliefShade pass per spatial
  frequency, every rib and fastener drawn after as a lit stroke pair on the one
  declared key, and the explicit written exclusion of every notes-only fact.
- FIELD-DOCUMENTARIAN: the object inventory, the three-register camera walk, the
  strip map, and the best hedge list of the three, which goes into the storyboard
  verbatim because it is what keeps this deck from becoming an accusation.

Type is Fraunces at opsz 144 with SOFT and WONK, over Space Grotesk, over
JetBrains Mono. Two of three directors picked it. It is neither forbidden pairing
and it is the warm display voice a type_temperature of 5 asks for.
