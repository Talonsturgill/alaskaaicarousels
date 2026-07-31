# NEXT RUN ASSIGNMENT — for the run dated 2026-07-31

**Status: ACTIVE. Written 2026-07-30 on maintainer instruction.**

Phase 0 reads this file. It is a MAINTAINER DIRECTIVE and it overrides the
run's own story selection. Everything else in the master routine still binds,
including every gate, and specifically including the dedupe gate, which this
assignment does NOT waive. See "The dedupe problem" below, because it is the
first thing this run has to deal with honestly.

Archive this file at ship time (`git mv prompts/NEXT_RUN.md
runs/2026-07-31/next_run_brief.md`) so it cannot silently steer a later run.

---

## THE ASSIGNMENT

Cover the Anthropic employees' donations to Jonathan Kreiss-Tomkins' campaign
for Alaska governor.

The maintainer's words: "cover the anthropic employees donations to the Alaska
guys campaign ... I want it on that story tmrw, that's huge."

## THE DEDUPE PROBLEM, AND IT IS REAL

**This story already ran, six days ago, as No. 17 (2026-07-25), "On File, Off
Record. Alaska's AI Governor Race."** With the dedupe window now at 30 days,
`dedupe_check.py` will flag it as a LIKELY DUPLICATE and it will be right.

The assignment stands, but the routine's own rule for this case stands too, so
this run ships as an EXPLICIT UPDATE and says so on the cover. Do not pretend
it is a new story. The scoring rubric hard-fails "topic repeats a ledger entry
within 30 days WITHOUT a material new development framed as an update", and the
material new development is real and specific:

> No. 17's stated angle was, verbatim from the ledger, "The asymmetry of the
> public record ... Alaska knows to the dollar who paid for this race and almost
> nothing about what any of the 17 candidates would do with AI ... **no donor
> motive on record**."
>
> On 2026-07-29, four days after that deck shipped, the largest donor put his
> motive on the record himself, in a signed first-person op-ed in the Anchorage
> Daily News.

So the update is not "here is that story again with a fresh number". It is
**the missing half of the earlier deck arriving**. That is a genuinely strong
reason to return to a story and it should be stated plainly on the cover and in
the caption.

Run `dedupe_check.py` anyway, read every LIKELY DUPLICATE in full as always,
and write the UPDATE framing into selection.md.

## WHAT IS ACTUALLY NEW SINCE No. 17

Leads, not verified claims. The fact-checker re-verifies everything from the
page, as always.

1. **The op-ed. This is the peg.** Drake Thomas, "Opinion: Why this Anthropic
   employee gave $100K to a candidate for Alaska governor", Anchorage Daily
   News, 2026-07-29, labelled Opinion.
   https://www.adn.com/opinions/2026/07/29/opinion-why-this-anthropic-employee-gave-100k-to-a-candidate-for-alaska-governor/
   Reported content, all to be re-verified: he works on Anthropic's safety
   team writing risk reports and running pre-release safety testing; he grew up
   in Kenai and now lives in California; "I'm terrified by the extremely rapid
   pace of AI development, and I wish it were slower"; he wants Dunleavy
   replaced; he backs the candidate's data-center moratorium plank; he claims
   the campaign has 1,569 Alaska donors, more than any other campaign for
   governor; and the piece carries the disclaimer "The views in this op-ed are
   his alone and do not represent Anthropic."

2. **NOTE A DISCREPANCY AND RESOLVE IT.** ADN's NEWS story (2026-07-23) says
   Thomas grew up in **Soldotna**. His own op-ed says **Kenai**. No. 17 shipped
   "Soldotna". Use the self-description, and if the deck says anything about it,
   say which source said which. This is exactly the kind of small thing a Kenai
   Peninsula reader notices.

3. **The connector fact.** Kreiss-Tomkins reportedly said Thomas connected him
   with the other Anthropic employees who gave. If that verifies, it explains
   how a six-person, $372,000 cluster forms without any coordination by the
   company, which is a structurally different thing from "an AI company gave
   money" and is worth drawing precisely.

4. **The denominator.** The Juneau Independent has published a chart putting
   all 17 candidates at nearly $9 million raised in total.
   https://www.juneauindependent.com/post/alaska-s-17-governor-candidates-have-raised-nearly-9-million-this-chart-shows-who-gave-it
   If it verifies, $372,000 against roughly $9 million is the honest proportion
   and it belongs in the deck. No. 17 built fairness in at full depth and this
   run must not regress on that.

5. **National pickup and its framing.** PJ Media and RedState both ran it as
   California Democrats trying to flip a red state. Alaska Watchman ran a piece
   on low turnout, ranked choice voting and unlimited donations. Salience and
   framing input only, never sourcing.

## THE ANGLE I RECOMMEND, AND THE ONE I RECOMMEND AGAINST

**RECOMMENDED SPINE: the record filled itself in.** No. 17 said the money was on
file and the motive was not. Six days later the motive is on file too, and what
it says is not what either side of the argument predicted: an AI safety
researcher spending $100,000 to help elect a candidate who wants to STOP data
centre construction, because he is, in his own word, terrified of how fast his
industry is moving. Reader takeaway: the loudest AI money in this race is
arguing for less AI infrastructure in Alaska, not more.

**THE STRUCTURAL TURN, and this is the brand voice doing its job:** ask why a
single $100,000 personal donation is legal at all. Alaska currently has no
individual contribution limits, and there is a measure on the August ballot
about reinstating them. VERIFY THIS PROPERLY, from the Alaska Public Offices
Commission and the Division of Elections, not from a news summary. If it holds,
the deck's real subject is not six donors, it is the rulebook that makes six
donors decisive, which is the structural framing brand.yaml asks for and is
also a fresh angle against No. 17.

**RECOMMEND AGAINST, and treat as a landmine:** Alaska Story has published an
"investigation" tying the candidate to a consulting firm in a Nebraska
campaign-finance corruption probe. It is a partisan outlet making a serious
allegation about a named person. Do NOT carry it, in any form, unless it is
independently verified against primary records, and even then it is a different
story from this one. Repeating an unverified corruption allegation about a
named candidate is the single worst thing this run could do.

## THE CONFLICT OF INTEREST, WHICH IS NOW SHARPER THAN LAST TIME

This routine runs on a Claude model built by Anthropic, and the story is about
Anthropic employees' political donations. No. 17 disclosed this on slide 09 at
full headline scale, in a pointer chip on slide 02, in the caption, and at the
top of the first comment. That is the floor, not the ceiling.

**This run must disclose at least as prominently, and must additionally say
that this is the second deck on these donors.** A second visit to a story that
touches the model-maker's own employees, without saying it is a second visit,
would look like emphasis chosen for the maker's benefit. Say it plainly.

Two things that are true and both belong: the op-ed's own disclaimer that
Thomas speaks for himself and not for Anthropic, and the fact that this deck's
publisher runs on that company's model.

## PROCESS NOTES FOR THIS RUN

- **Variety.** No. 17 was the series' first elections deck. Its hero was THE
  MILLED REGISTER (bone limestone slab), its atmosphere gallery-lit bone, its
  hook an asymmetry couplet. Those are all outside the forbidden window by
  2026-07-31 EXCEPT that returning to the same story with a similar look would
  read as a re-skin. Go somewhere visually distant from No. 17 deliberately,
  and note the choice in the storyboard's variety check.
- **Caption.** The two new gates apply: a declared deck-summary line passed to
  `caption_check.py --deck-summary`, and no use of the word "cannot".
- **Artwork.** `assets/js/aksnow.js` exists now if the deck wants snow, but do
  not reach for it just because it is new. The standing weakness is still
  artwork craft, and the lesson from No. 20 is to spend the detail budget on a
  few surfaces built properly rather than spreading a uniform texture
  everywhere. Read the 2026-07-30 addendum in FIELD_NOTES before Phase 5.
- **Election proximity.** The primary is 2026-08-18. Anything that reads as
  advocacy for or against a candidate is out of bounds. No. 17 asserted no
  causation, no donor motive and no wrongdoing; motive is now on the record in
  the donor's own words, so it can be QUOTED, but causation and wrongdoing stay
  unasserted.
