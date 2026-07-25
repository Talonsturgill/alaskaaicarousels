# SELECTION — 2026-07-25 — Carousel No. 17

## THE STORY (chosen)

**Scout D1.** Campaign finance reports made public the week of July 20, 2026 show
Democrat Jonathan Kreiss-Tomkins with the largest reported haul in Alaska's
17-candidate governor field, 1.8 million dollars since February, most of it from
donors in the Lower 48 (per ADN). Inside that total, six employees of the AI
company Anthropic gave 372,000 dollars, and the single largest contribution,
100,000 dollars, came from an Anthropic employee who grew up in Soldotna and now
lives in Berkeley. The same candidate campaigns on pausing data center
construction until Alaska has a process and a policy, and on six named AI
regulations. Alaska's primary is August 18, 2026, 24 days out from this run.

## WHY THIS ONE (criteria in order)

1. **Concrete Alaska impact.** Alaska has an unusually dense stack of pending
   AI-infrastructure decisions and the next governor inherits the whole stack.
   This is the one story in the window where the DECIDER is being chosen rather
   than the decision being made, and where every Alaskan holds a vote.
2. **Visual potential.** Money has scale, a field has rank, a ballot has 17
   lines, a policy list has six items, a calendar has 24 days. Every one of
   those is drawable, and the honest tension (money pointing one way, stated
   platform pointing the other) is a two-column composition waiting to happen.
3. **Tangibility.** A filing, a named dollar figure, a named person, a dated
   election. Nothing speculative.
4. **Would an Alaskan send this to a coworker?** Yes, and to a legislator. It is
   the first time AI-industry money is a measurable presence in an Alaska
   statewide race, and it is 24 days before people vote.

## DEDUPE GATE

`python scripts/dedupe_check.py` exit 0. **No LIKELY DUPLICATE.** Full output read
(never tailed, per instinct 0.95). Strongest match was No.14 (2026-07-22) at
token_jaccard 0.022 with **zero shared entities**, and the only shared keyword was
"center", which comes from my candidate keyword "data center moratorium". Six soft
overlaps, all on that same single word.

Read in full as required: No.14 is a DNR land conveyance to AIDEA near Houston.
This deck is a campaign-finance and AI-policy story about who gets elected. No
shared entity, no shared decider, no shared decision, no shared frame. Genuinely
distinct. Nothing in the 90-day window touches elections, campaign money,
candidates, or AI policy platforms. Clean.

## WHAT THE FACT-CHECKER TOOK AWAY (and how the story changed)

The intended centerpiece is DEAD. I had planned the comparison "six people at one
AI company gave more than every Alaska donor to that campaign combined." The
in-state total ($365,808) came only from a partisan outlet whose page now 404s,
and APOC plus the state notice system both returned 503. **REJECTED.** The deck
uses the attributed "majority from wealthy donors in the Lower 48" instead.

Also removed: a second named donor who does not exist in the sourcing at all; the
80/20 split; the APOC attribution; the top-four primary rule; any claim that
Alaska has no AI statute; HCR 3 and HB 259 status; and the AIDEA and STAK docket
items I wanted for the stakes beat (both 503-blocked this run). The verified
stakes anchor is the Air Force lease instead, 4,700 acres at three Alaska
installations, offers due June 29, no award announced.

And the fact-checker found the thing that reshapes the deck: the candidate is on
record saying **"Most of our national donors, I think, actually, their only agenda
is, 'can you win?'"** That is a direct rebuttal of a causation reading, it is
mandatory on the deck, and it makes the deck better rather than worse.

## THE HONEST THESIS

Not "AI money bought an AI platform." That is unprovable, the donors' motives are
nowhere on record, and the candidate denies it.

The defensible and more interesting argument: **Alaska is choosing the person who
will write its AI rules, and the money in that choice is already national. Follow
it and you find six people at one AI company holding about a fifth of the biggest
haul in the field, a self-funding candidate who wrote a bigger check than all six
of them, and four candidates who would not answer a survey about AI at all. No
one has alleged anything improper. The point is not a scandal. The point is that
Alaskans can still ask, and they have until August 18.**

The deck's job is to give a busy Alaskan the receipts and the counter-receipts on
one screen, and to make the missing answers as visible as the money.

## RUNNER-UP (and why not)

**Scout A1, the Bradley Lake Expansion.** Strong and primary-sourced (a 5,600-page
FERC filing announced July 20, an AEA board financing framework July 23, $400M
total, 167,000 MWh added, five Railbelt utilities next). Not chosen because the AEA
releases never say "AI" or "data center", so the AI framing would be entirely the
studio's analysis, and because the power-and-data-center beat has already carried
six of sixteen decks. Parked as a strong near-term candidate, especially once the
five utilities act on the financing before the fall 2026 deadline.

Also parked: the ONR Arctic autonomous observing system (comment closes Aug 21,
but it is autonomy not AI), the NSF GAIA AI geohazard award to UAF (out of window,
no release, and adjacent to decks No.3 and No.11), and Alaska's $272M Rural Health
Transformation award (the AI and drone shortlist is real but no award list was ever
published).

## DIRECTORS ROOM SETUP

Three lenses, chosen to rotate off the recent cartographic and systems trios:
**data-journalist**, **editorial-essayist**, **field-documentarian**.

Variance dials: DESIGN_VARIANCE 5, VISUAL_DENSITY 2, TYPE_TEMPERATURE 5.

The light-register allowance (once per 8 runs, brand.yaml) is UNSPENT: runs 9
through 16 were all dark-base. This story's material world is paper and civic
objects (a filing, a ballot, a questionnaire, a mailed disclosure), so light is
motivated here rather than a stunt. Price of admission per this run's craft
refresh: the cover must carry an unusually large near-black display headline plus
one saturated accent mass, and it must be judged at 432px before anything else
gets built.

One extra design problem handed to the room: this deck needs a **designed
conflict-of-interest disclosure**, because the routine runs on a Claude model built
by Anthropic and six Anthropic employees are the donors in the story. Buried fine
print is not acceptable. It should be a deliberate element.

---

## SYNTHESIS (after the directors room)

Three strong, genuinely different pitches. All three independently chose a light
ground, all three independently landed on Fraunces plus Bricolage Grotesque plus
JetBrains Mono, and two independently chose an ORTHOGRAPHIC camera. That
convergence is a signal, not a coincidence, and I am taking all three.

**WINNER, on thesis: the editorial-essayist's THE UNCUT SIDE.** It is the only
pitch that found something better than the corruption frame instead of merely
avoiding it. Its insight is that the record WORKED. Every number in this story
exists because a law compelled it, down to one 100,000 dollar gift and one man's
1.4 million dollar check to himself. What is missing beside it is policy, because
nothing compelled any of the 17 candidates to state an AI position, so what little
we know exists only because reporters volunteered to ask and four candidates did
not answer. **The money is compulsory and legible. The policy is optional and
blank.** That reframe does three things at once: it is the sharpest available
argument, it refuses causation on principle rather than on a technicality, and it
turns the fact-checker's demolition of my in-state-split centerpiece from a wound
into the deck's actual subject. Its second-best line is the craft argument for
going light, and it is unanswerable: you cannot draw an absence on a black field.

**ORGANS GRAFTED FROM THE OTHER TWO:**

From the **data-journalist**: (1) the ORTHOGRAPHIC PBR rule, which is the run's
real technical unlock. Doctrine forbids perspective on quantities, so a rendered
object whose dimension encodes dollars is only legal under a parallel projection.
An OrthographicCamera inside the akthree rig gives real PBR materials, real
shadows and real IBL while keeping quantities honest, and it makes the Canvas
fallback geometrically identical rather than merely similar. (2) The UNMEASURED
BRACE for the rejected in-state split, merged into the milled language as a
dimension call with a missing extension line and a NOT DISCLOSED value field.
(3) Its evidence-class-by-SHAPE idea, kept small.
REJECTED from it: money as stacks of physical sheets. Its own self-critique names
the reason, and the reason is fatal. Stacks of paper money read as stacks of cash
at 432px, and a cash-pile read smuggles in exactly the corruption causation the
claims forbid. The metaphor argues the thing we may not argue.

From the **field-documentarian**: (1) the camera-arithmetic-derived ZONE SYSTEM,
which is the structural fix for the dead-lower-third defect that has capped
artwork craft at 7 for four straight runs. Deriving the text bands and the art
band from the projection means no slide has a dead band by construction, because
the object lives down there and the shadowed front band is a real inhabited
surface. (2) The light-angle arc as the calendar, one key light rotating so cast
shadows lengthen toward the vote. (3) Its disclosure placement instinct, that the
conflict must be visible where the name appears and not only at the back.
REJECTED from it: the counter-of-objects chassis, on its own self-critique. Four
printed sheets in a row would read as four cousins on the contact sheet.

**THE DISCLOSURE, resolved.** The essayist's answer is the right one and it is
better than either alternative: set "WHO IS TELLING YOU THIS" at the SAME size and
weight as every other headline in the deck. A shrunk gray disclosure is a
confession; an equal one is a position. Two milled plates, sourcing on the left
(one reporter, one article, republished, not two independent outlets) and the
conflict on the right (this deck was produced with a Claude model built by
Anthropic; six Anthropic employees are the donors; no source reports any
involvement by Anthropic the company; this deck asserts no causation and no
wrongdoing). Plus the field-documentarian's pointer, a compact conflict chip on
the slide where Anthropic is first named, so no reader meets the name before they
meet the disclosure.

**FAIRNESS, resolved as geometry rather than as a courtesy line.** The receipts
slide and the counter slide are TWINS: same slab, same orthographic camera, same
light, same well depth, wells cut to the same dollars-per-pixel scale. On the
contact sheet they are architecturally equal, so the counter-argument cannot read
as a concession. The deepest single cut anywhere in the deck is one candidate's
own checkbook, and the largest quotation in the deck is the subject's own sentence
undoing the easy reading.

**HERO TECHNIQUE, one deliberate change from the winning pitch.** The essayist
specified aksdf CPU raymarch for the carved hero. I am overruling that to akthree
GPU PBR under the same orthographic camera. Reasons: akthree is proven in this
container and produced what the scorer called the strongest artwork the series has
shipped one run ago; aksdf is D4, 5 to 15 seconds, and its documented failure mode
is exactly ours (carved recesses going near-black); and using one technique across
the receipts, counter and hero slides is what makes the twins argument literally
true. Depth is distributed across four slides (three akthree sharing one scene and
one camera, plus akrelief relit rows on the keepable), which is the fix for the
recurring flat-deck ceiling.

**SLIDE COUNT: 10.** All three directors independently arrived at 10, the arc
genuinely has ten beats, and it sits inside the 8 to 10 house default. At
VISUAL_DENSITY 2 compressing to 9 would force two argued beats onto one slide,
which is the exact crowding the dial exists to prevent.

**PALETTE, from the essayist:** bone-dominant with FIREWEED #C0246B as the single
saturated accent, meaning "the compulsory record" and nothing else, plus navy
inset wells as the pocket where dark and gold can survive on a light deck. Gold
never sets type on bone. Fireweed is also honestly seasonal, it is what the
roadsides this campaign is happening on actually look like in late July, and the
series has never used the hue.

**CUT for honesty and tightness:** nothing. The Air Force in-tray beat stays, but
its copy is disciplined down to the verified facts plus "Alaska's next governor
takes office with this already in motion", because the governor does not sign a
federal lease and the deck must not imply otherwise.
