# SELECTION + DEDUPE — carousel No. 21, run date 2026-07-31

## 1. THE STORY

**Alaska's campaign contribution limit is a number that no longer exists, and on
August 18 Alaskans vote on whether to write a new one in.**

The statute, AS 15.13.070(b), still says $500 an individual may give a candidate
in a year. It has never been repealed. It is also not the rule. The Ninth
Circuit struck it in July 2021, APOC deadlocked three to two on a replacement in
February 2022, the Legislature's fix was vetoed on July 9 this year, and APOC's
own published table, date-stamped two days before this run, says Unlimited for
an Alaska resident and a non-resident alike.

That is why a single personal check for $100,000 could arrive in Alaska's
governor's race from Berkeley, California, and why six employees of one AI
company could put in $372,000 between them. And on 2026-08-18, on the same
ballot as that race, Ballot Measure 1 asks whether to write $2,000 back in.

The turn: even if it passes, it can't touch this race. An initiated law takes
effect ninety days after certification.

## 2. THE ASSIGNMENT, AND WHY THE SPINE MOVED

`prompts/NEXT_RUN.md` is an ACTIVE maintainer directive and it overrides story
selection. Its assignment was "the Anthropic employees' donations to Jonathan
Kreiss-Tomkins' campaign". That is covered here and it is the deck's exhibit.

The brief also RECOMMENDED a spine ("the record filled itself in") and, in the
same document, flagged a structural turn it wanted verified from primary
sources: "ask why a single $100,000 personal donation is legal at all ... If it
holds, the deck's real subject is not six donors, it is the rulebook that makes
six donors decisive."

It holds. S2 verified it out of APOC's own table, the official Division of
Elections sample ballot, the Ninth Circuit's opinion and the Alaska
Constitution. So this run takes the brief's own second option, which the brief
itself called "the structural framing brand.yaml asks for and is also a fresh
angle against No. 17". Showrunner's call, made on the evidence, and recorded
here as the brief instructed.

Two independent findings pushed the same way:

- **S2, from the documents.** The rulebook is not background to this story, it
  is a decision with a date on it, and Alaskans are the deciders.
- **S6, from the community.** It read every pro-reform letter and op-ed in the
  window and found that NONE of them mentions AI. Four independent reform
  advocates, zero AI mentions. Its conclusion is a design constraint: "If the
  deck opens on 'AI money enters Alaska politics' it is opening on the national
  frame. If it opens on ... 'you vote on whether that stays legal in eighteen
  days' it is opening on the Alaskan one."

The AI framing of this donation is being supplied almost entirely by two
national conservative blogs, one Alaska conservative site, and ADN's news desk
via one legislator. Opening on it would be importing an Outside frame into a
page written for Alaskans.

## 3. DEDUPE GATE

`python scripts/dedupe_check.py` exited **1**, exactly as the brief predicted.

```
  [LIKELY DUPLICATE] No.17 2026-07-25 ()
    shared entities: alaska governor race 2026, anchorage daily news, anthropic,
                     august 18 2026 primary, drake thomas, jonathan kreiss tomkins,
                     matt heilala, soldotna
    shared keywords: campaign, disclosure, donations, election, elections,
                     finance, governor, money, out, political, primary, race
    token jaccard: 0.161
  STRONGEST MATCH: No.17 2026-07-25 (6 days ago) -- LIKELY DUPLICATE -- 8 shared
  entities, jaccard 0.161
```

Full output read, never tailed (instinct at 0.95). The one LIKELY DUPLICATE,
No. 17, was read IN FULL from the ledger before the directors room. Nine SOFT
OVERLAP entries were also read; all are incidental ("center", "kenai") and none
is a topic collision.

**RULING: this is a repeat, and it ships as an EXPLICIT UPDATE, stated on the
cover.** The rubric hard-fails "topic repeats a ledger entry within 30 days
WITHOUT a material new development framed as an update". Both halves are
satisfied, and here is the material new development, stated precisely.

No. 17's ledger angle, verbatim: "The asymmetry of the public record, NOT
corruption ... Alaska knows to the dollar who paid for this race and almost
nothing about what any of the 17 candidates would do with AI ... no donor motive
on record, no wrongdoing alleged."

Since that deck shipped, three things happened, and only the first was
foreseeable:
1. **2026-07-29.** The largest donor put his motive on the record himself, in a
   signed first-person ADN op-ed. No. 17's stated gap closed.
2. **2026-07-30.** ADN reported that Ballot Measure 1 is on the August 18
   primary ballot and cited these same six-figure contributions by name as its
   illustrative example. The donation stopped being a campaign story and became
   an exhibit in a ballot question.
3. **Verified this run, and not previously published anywhere in this form:**
   the statute still says $500; a passed Measure 1 can't govern the race it
   shares a ballot with; and the measure does not restore any out-of-state
   limit, because the sponsors' earlier petition carried that clause and the one
   that reached the ballot dropped it.

**No. 17 was a deck about a RECORD. No. 21 is a deck about a RULE.** Different
subject, different verb, different decider. No. 17's decider was nobody, which
was its point. This deck's decider is the reader, and the deadline is eighteen
days out with early voting in three.

The deck says all of this on the cover and again in the caption. It does not
pretend to be new.

## 4. THE RUNNER-UP

**S5's docket sweep, specifically the AIDEA Houston conveyance (ADL 234762),
whose comment deadline is 5:00 PM on 2026-08-19** and which carries a fact this
page has never drawn: the notice says only people who file timely written
comment are eligible to appeal the Final Finding and Decision. Commenting is not
just being heard, it is buying standing. About 19,950 acres, four concurrent
actions bundled into one notice.

Rejected for THIS run for two reasons, both honest. First, No. 14 (2026-07-22)
already told the AIDEA conveyance as its own deck, "31 square miles of public
land. Free.", so it is the same dedupe problem without the same quality of new
development. Second, the standing point is genuinely good and deserves better
than a runner-up slot; it goes to the docket this run and is queued as a
candidate for a deck of its own before August 19.

Also considered and rejected: the Houston City Council's August 13 vote on a
municipal data-center ban, which is real but small and whose most interesting
feature (the AIDEA parcel sits outside city limits, so the ban would not reach
it) is a docket line, not a deck.

## 5. WHAT THIS DECK WILL NOT DO

- **No advocacy.** The primary is eighteen days out and early voting opens in
  three. The deck takes no position on any candidate and no position on how to
  vote on Ballot Measure 1. It reports what the rule is, what the ballot asks,
  and what a YES would and would not do.
- **No causation, no wrongdoing.** Same standard as No. 17. Motive is now on the
  record in the donor's own words and can be QUOTED. Nothing is inferred from it.
- **The company did not give.** Six employees gave personally. Anthropic has
  issued no statement and the op-ed carries its own disclaimer. The deck holds
  that line, because collapsing it is the single most common error in the
  circulating coverage.
- **The excluded allegation stays excluded.** A partisan outlet has published an
  unverified serious allegation about a named person. It does not appear in this
  deck in any form, including as an example of a framing that exists. All six
  scouts were instructed accordingly and all six complied.
- **No 80 percent.** Pending the fact-checker's ruling, the out-of-state share
  is "a majority", which is ADN's own qualitative wording, because no permitted
  source publishes a percentage.

## 6. THE CONFLICT OF INTEREST, DISCLOSED HARDER THAN LAST TIME

This routine runs on a Claude model built by Anthropic, and the deck concerns
donations by Anthropic employees. **This is also the second deck this page has
published on these donors in seven days.** Both facts ship.

No. 17's disclosure floor was slide 09 at full headline scale, a pointer chip on
slide 02, the caption, and the top of the first comment. The brief requires this
run to meet that floor AND to additionally say it is a second visit. It does,
and the second-visit line is not buried with the model disclosure; it is on the
cover, because a reader who saw No. 17 should know inside one second that this
is a return.

Two true things ride together: the op-ed's own disclaimer that Thomas speaks for
himself and not for Anthropic, and the fact that this deck's publisher runs on
that company's model.

## 7. THE OBJECTION THIS DECK HAS TO SURVIVE

S6 wrote it at full strength and it is the right test: a deck built on a sincere
signed op-ed picks the one artifact in the story that is pure self-report, and
publishes it during early voting, so it functions as earned media whether or not
that is the intent.

The rulebook spine is the answer, and it has to be visible in the artwork rather
than asserted in a disclaimer. The donor is not the subject. The op-ed is quoted
for essentially one line, the line where he argues against the rule that let him
give. The concentration ratio, the ballot math and the counterweights ride on
the same slides as the exhibit, not in a fairness annex at the back.

If the deck can't hold all of that, S6 is right that the objection wins.

## 8. WHY AN ALASKAN SENDS THIS TO A COWORKER

Because it answers a question a lot of people have half-asked this month and
nobody has answered in one place. Why is a $100,000 check from California legal
here at all, what is actually on my August ballot about it, and would passing it
have changed anything about the race I am voting in? The answer to the last one
is no, and that is genuinely surprising.
