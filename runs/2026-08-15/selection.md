# SELECTION — 2026-08-15 — Carousel No. 34

## The story

On August 5th, 2026 the Senate Commerce Committee held Executive Session 24 in
room SR-253. Five bills were on the agenda and three of the five carry
artificial intelligence or chatbot subject matter in their titles. One of those
three is S. 5171, the Children's Artificial Intelligence Toy Safety Act of
2026, and Alaska's Lisa Murkowski is the Republican cosponsor named in the
sponsor's announcement that it cleared committee that day.

What the bill asks for is the story. Per Senator Duckworth's release, it
requires the Federal Trade Commission and the Consumer Product Safety
Commission to give Congress a coordinated plan on AI-enabled toy products, and
it directs the National Academies to conduct a study. A plan and a study.
Nothing in the release describes a rule, a ban or a standard.

## Why this one, over the two that lost

**The NSF critical minerals award was the strongest story on the table and it
lost on dedupe freshness, not on quality.** Two scouts converged independently
on NSF awards 2614749, 2614750 and 2614751, dated August 5th, obligating
$3,824,575 to UAA, $913,037 to UAF and $1,260,800 to Montana Tech through 2030
to pull rare earth elements out of coal mining waste with bioprocessing and AI,
led out of Anchorage. Verified against the NSF Award API, which is primary. It
is held back because No.33 shipped yesterday on an NSF AI funding rule and
No.24 shipped twelve days ago on critical minerals and AI, and this story sits
at the intersection of both. It goes first in the queue when the window clears.

**The FAA's $875 million SMART award** rests on one NPR story carried by Alaska
Public Media, its fuel and flight-hour figures are airline and vendor claims
with no published method, and the carrier is headquartered in Seattle.

**The AI-donation and data-center-moratorium thread** is No.21's and No.17's
material. Every named entity in it is already in the ledger inside the window.

The selected story wins on all four criteria in order. Concrete Alaska impact,
because an Alaskan senator is the actor rather than the recipient and the thing
being decided is what arrives in an Alaskan house. Visual potential, because
the subject is a physical object that can be rendered, opened and examined.
Tangibility, because a toy on a shelf is the least abstract thing this page has
covered in a month. And an Alaskan sends this to a coworker who has a
four-year-old.

## The dedupe gate

`python scripts/dedupe_check.py` with the candidate entities and keywords
returned exit 0, SOFT OVERLAP only, against every entry in the 30 day window.
The strongest match is No.28 at token jaccard 0.006 on the single shared entity
"alaska legislature". Read in full: No.28 is the voter roll citizenship flags
and shares nothing but the name of the body. No.24 shares the word "executive"
at 0.031 and is a graphite mine. Nothing here needs an UPDATE framing.

## THE THESIS WAS REBUILT AT THE CLAIMS GATE, AND THIS IS THE HONEST ACCOUNT

The story was selected on a thesis the fact-checker then killed. The original
frame was that Alaska's own statute book on AI systems that talk to children is
empty, so whatever Congress writes is the only rule an Alaskan family gets.
That is probably true. It is not verifiable. BASIS, LegiScan and the NCSL state
AI legislation tracker all returned HTTP 403 to automated fetch this run, so no
source was reached that enumerates Alaska statutes on AI or companion chatbot
disclosure, and an unverified absence is not a claim.

So the deck argues something narrower and harder, entirely from what the record
does support.

**THESIS. The first federal answer to the machines that talk to children is a
request for a plan and a study, and no page anyone can reach says when either
one is due.**

That is not a complaint about Congress. It is a description of the shape of the
answer, and the deck is deliberately fair about it. A plan and a study are the
normal opening move for a technology nobody has measured yet, and the deck says
so. What the deck refuses is the pretence that anything has been decided.

The absence is architectural rather than a caveat, and every part of it is
itself verified. The committee's own page publishes no tally, so nobody can say
by what margin it advanced (C11). The bill text is unreachable, so nobody can
print a deadline for the plan or for the study (C15, C16). The FTC's and the
CPSC's own release indexes carried nothing on AI toys on the day this deck was
built (C27, C28). The testing the release leans on could not be read directly
(C24). Five separate things are not knowable today, and the deck prints that as
the record rather than as an excuse.

## What the deck refuses to say

- It never states a vote margin. C11 records that no tally is published.
- It never prints a deadline for the plan or the study, because the bill text
  can't be read.
- It never says the bill contains no rule. It says the sponsor's release
  describes a plan and a study and describes no rule, which is C17 exactly.
- It never says Alaska has no law on this. It says the sources reachable this
  run do not settle it, and it attributes the Alaska policy record to an
  Anchorage Daily News opinion column by name.
- It never converts "by the thousands" into a number. That is Senator
  Duckworth's characterization and carries no cited count (C21).
- It never states the PIRG findings as established. They are attributed to the
  sponsor's office citing the U.S. PIRG Education Fund (C24).
- It never names a state that requires companion chatbot disclosure. The column
  names none (C35).

## The docket

S. 5171 is deliberately NOT added to `ledger/docket.json`. The docket's written
promise is every AI infrastructure decision in Alaska, and a consumer product
safety bill is not infrastructure. Widening that promise is the maintainer's
call, not a run's. It is raised as a proposal in the ship note instead.

## Runner-up, for the record

NSF awards 2614749, 2614751 and 2614750, the $4.74 million to UAA and UAF for
AI and bioprocessing recovery of rare earth elements from coal mining waste.
Held for freshness, not for quality. Everything needed to build it is in
`out/2026-08-15/scout_merge.md`.
