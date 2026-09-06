# SELECTION. 2026-09-05. Carousel No. 51.

## THE STORY

**Six people who list one AI company as their employer put $372,000 into
Alaska's governor's race. On the same August 18th ballot that ranked that
candidate first, 117,962 Alaskans voted to cap an individual gift at $2,000.
The cap starts after the November 3rd election.**

Every load-bearing number comes from a State of Alaska record. The money comes
from the Alaska Public Offices Commission's own Campaign Disclosure Income
database, pulled in full this run, 4,604 rows. The votes come from the Division
of Elections' certified official results PDF, timestamped August 31st, 2026.

## WHY THIS ONE, against the criteria in order

**1. Strongest concrete Alaska impact.** The next governor inherits every live
AI infrastructure decision in the state, and there are a lot of them on this
studio's own docket right now. Twenty four tracked decisions, three open for
comment. The Air Force is offering land at JBER, Eielson and Clear. DNR is
weighing a North Slope campus lease and a Mat-Su conveyance. Fairbanks has
asked the Legislature for a moratorium. Whoever wins on November 3rd decides
how the state answers all of it, and the money deciding that race is mostly not
Alaskan.

**2. Visual potential.** This is the best-shaped data this beat has produced in
weeks. Six marks against 125 marks is a countable hook that the frame itself
can verify through `__akAssert` with declared points. $372,000 against $632,036
is one comparison. 58.8 percent of the gifts carrying 26.6 percent of the money
is a second, and it is the more interesting one, because it is the shape of the
whole problem in two numbers. A median Alaska gift of $50 against a single gift
of $100,000 is a ratio of two thousand to one and it is drawable.

**3. Tangibility.** A dollar figure, six names, a date, a cap, a ballot already
counted. Nothing here is a forecast.

**4. Would an Alaskan send this to a coworker?** Yes, and to a legislator. It
is the rare AI story that is not about a machine at all.

## THE HONEST FRAME, and this is the whole editorial decision

This deck is NOT an accusation and must never read as one. Three disciplines
bind every slide.

**Every one of those six gifts was legal when it was made.** Alaska has had no
individual contribution limit since the Ninth Circuit struck the $500 cap in
Thompson v. Hebdon and the Legislature declined to write a new one. The donors
followed a rule Alaska's own government left in place for five years. If the
deck lets a reader think a law was broken, the deck is wrong.

**The company did not give. Six people did, with their own money.** Anthropic
appears in this record only as the string those six typed into the employer
field on a disclosure form. Writing "Anthropic gave" would be false. The deck
says employees, every time.

**No evidence of any exchange exists, and the deck says so out loud rather than
leaving the shape of an insinuation.** The candidate's own answer runs on a
slide, verbatim, in his words and not in a summary of them.

What is left after all three disciplines is still a real story, and it is
structural rather than personal. **Alaska fixed this problem itself and set the
fix to arrive one election late.** That is nobody's scandal and everybody's
problem, and it is the kind of thing this page exists to name. The runner-up
frame, "candidate takes AI money", is the one every other outlet already ran
and it is the weaker story.

## THE MISSING OPTION, which is what the house voice is for

The debate on the ground is moratorium against build. The thing nobody is
arguing about is that the rule Alaskans wrote for exactly this situation was
written to start after the situation. A cap that arrives in December governs
the next race. It does not govern the one that decides who the state's AI
policy belongs to.

## DEDUPE GATE

`python scripts/dedupe_check.py` exit 0. Soft overlaps only, the strongest
being No.28 on August 7th at a token jaccard of 0.036, sharing exactly one
entity, the Division of Elections, on a completely different subject, the voter
list purge. No.48 on September 2nd shares the word "ballot" and is about hand
counting in one borough. No topic in the 30 day window is about campaign
finance, donors, or the governor's race. This is a genuinely new story, not an
update.

## RUNNER UP, and why not

**The Anchorage Real Time Crime Center vote of September 1st.** The Assembly
funded it 8 to 4 at $600,000 and held off the privacy ordinance, and Chief Sean
Case put a real AI boundary on the record for the first time, excluding facial
recognition and including weapons and vehicles. That last part is genuinely
new and genuinely interesting.

It loses on the dedupe clock rather than on merit. No.40 shipped the RTCC
ordinance on August 25th, eleven days ago, and this would have to ship as an
update inside the 30 day window. The code-versus-policy distinction is worth a
deck on its own later, when it is not a fortnight behind its predecessor. Held
as a candidate for `prompts/NEXT_RUN.md` if the ordinance comes back.

Third place, the FAA doubling its BEYOND drone programme with UAF ACUASI
continuing as a lead site. In window and real, but the scout could not reach a
primary source, faa.gov answered with a 403, and the Alaska-specific content
was institutional naming with no operational detail. Thin.

## WHAT THE DECK MUST NOT DO

- Must not say Anthropic gave money. Six named people did.
- Must not imply illegality. Nothing here was against any rule.
- Must not imply an exchange. State the absence of evidence explicitly.
- Must not be about one candidate's character. It is about a rule's start date.
- Must not print the November ballot field unless the fact-checker confirms it.
  One source suggested a withdrawal after the primary and it is not verified.

## PHASE 3.5 STEP 1, and why nothing new reached the docket

This run's verified claims add NO item to `ledger/docket.json`, and that is a
decision rather than an omission.

The docket tracks AI infrastructure DECISIONS in Alaska, and its kinds are a
lease, a comment window, a vote, a regulatory docket, a solicitation or a
procurement. Ballot Measure 1 is a campaign finance rule and is not AI
infrastructure. A governor's race is not a decision before a body. C33, the
candidate's proposal to ban data centre construction until the Legislature
regulates, is a campaign position rather than a filed instrument, and putting a
candidate's platform on a tracker of filed decisions would be the first step
toward the docket becoming an opinion page.

The two candidates in `ledger/watch.json` were triaged and dropped. Both are
FERC hydropower notices, Juneau Hydropower's extension of time and an Alaska
Energy Authority non-capacity licence amendment, and neither carries an AI or
compute connection that a primary source supports.

`watch.json` carried one FAILED source today, `basis-bills`, HTTP 503. The
Legislature's BASIS did not answer the sweep, so today's bill observations are
absent rather than empty, and the ship note says so.
