# Caption Craft — the variety engine for post copy

The caption is a bespoke piece of writing, conceived fresh per run, not a
template filled with today's nouns. This doc is the craft library the caption
room draws from and the laws the caption-critic enforces. The ledger at
`ledger/captions.json` is the memory that makes repetition impossible.

## The anti-template law (the whole point)

If today's caption could be produced by swapping the nouns into yesterday's
caption, it fails. The shape itself must be a choice. Every run the room picks
a named OPENING MOVE, a STRUCTURE, and a CLOSING MOVE, and the recent ledger
entries are excluded from the menu. Form serves the story: pick the move the
material actually rewards, never a gimmick for variety's own sake. Same-y and
safe loses to specific and alive, but clarity beats cleverness when they fight.

## Banned furniture (mechanically enforced, caption_check fails these)

Recurring connective tissue that made the old captions read like a mail merge.
Never write:
- "The deck walks through..." / "walks you through" / any "N slides walk" line
- "These 9 slides..." or any slide-count-does-X sentence used as furniture
- A closing question bolted on in the same breath every day

Pointing at the deck is allowed, but earn it fresh each time or skip it: fold
the pointer into the argument ("Slide 6 is the one the council member will
bring to the meeting"), make it a dare ("The deed map alone is worth the
swipe"), or let the deck sell itself with no pointer at all.

## Opening moves (pick one; last 6 runs' moves are off the menu)

- COLD NUMBER — one verified figure, alone, before any context. "31 square
  miles. Zero dollars."
- SCENE — put the reader somewhere physical at a time. Freeze-up, a dock, a
  hearing room at 5 p.m.
- CONTRADICTION — two true things that can't both be comfortable, side by
  side.
- QUOTE FIRST — a verified human sentence opens, attribution after.
- SECOND PERSON STAKE — what this decision does to the reader's bill, land,
  or job. Use sparingly and only when literally true.
- TIMELINE COLLAPSE — then vs now in two beats. "In 1979 there were 1,300.
  Today, 331."
- DEFINITION SUBVERSION — take a word everyone uses and show what it actually
  means here.
- THE ABSURD DETAIL — the one small verified fact that sounds made up and is
  not.
- LEDGER TALLY — a running count or scoreboard framing, receipts up front.
- QUESTION FIRST — open on the genuine question the story turns on. Not
  clickbait, the real fork.
- LETTER FRAME — addressed to a named decision-maker or body, respectful and
  blunt.
- MAP MOVE — geography does the arguing. Name the places, walk the line.

The menu is not closed. A director may invent a move and name it NEW:<name>;
the critic judges it, and if it ships it joins this list.

## Structures (pick one; last 3 runs' structures are off the menu)

- INVERTED PYRAMID — hardest fact first, context widening beneath it.
- BRAID — two threads alternating (the deal and the person fighting it),
  meeting in the last line.
- COUNTDOWN — organized around a real deadline, time pressure explicit.
- PUNCH THEN PROOF — one-sentence claim, then the receipts, one per line.
- Q AND A — the story as the three questions an owner would actually ask,
  answered straight.
- ZOOM — one household or block, then the borough, then the state. Or the
  reverse.
- COLD OPEN, WARM CLOSE — data-forward top, human consequence last.

## Closing moves (rotate; never the same phrasing two runs straight)

The close is still a real, debatable question (caption_check requires it),
but the KIND of question rotates: a fork ("fair trade or giveaway?"), a
stake ("would you take that deal for your block?"), a prediction ("what
lands first, the tenants or the lawsuits?"), a who-decides ("should the
neighbors get a vote before the deed moves?"), a price ("what is the honest
number?").

## Voice, unchanged and non-negotiable

Everything in config/brand.yaml still binds: analytical, position-taking,
plain English, grade 8-10. No em or en dashes, NO COLONS EVER (clock times
excepted), no semicolons, straight quotes, no emojis, exactly 3 niche
hashtags as the final line, hook under 140 chars, 300-900 chars total, no
links, no sources, no credits, no AI-tells, close on a real question. The
variety engine changes the shape, never the standards.

## Two rules the machine now enforces, so they stop lapsing

**THE DECK SUMMARY LINE IS MANDATORY.** brand.yaml has set
`deck_summary_line: true` since the beginning and the room quietly stopped
writing one for three consecutive runs (2026-07-26, 07-29, 07-30) because
nothing checked. The reason it matters is not style. A LinkedIn DOCUMENT post
carries no alt text at all, so for a screen-reader user the caption is the
entire deck. One or two plain lines saying what the deck actually contains is
the only accessible description that exists, and it doubles as ranker signal
because the ranker reads text and not hashtags.

Write it as its own line. It may not be the hook and it may not be the closing
question. It is not the banned deck-pointer furniture either, and the
difference is that furniture points at the artifact ("the deck walks through
five slides") while a summary names the CONTENTS ("the award row as published,
what two utility chiefs said, and the blanks in both"). `caption_check.py`
requires the line to be declared with `--deck-summary` and to appear in the
caption verbatim; whether it is any good is the critic's call.

**NEVER WRITE "CANNOT".** Always "can't" (maintainer rule, 2026-07-30). This
holds in the caption, in the first comment and on every slide. "Cannot" is the
register of a press release; the house voice is a person talking.
`caption_check.py` fails it.

**DATES ARE MONTH FIRST.** "August 10th", never "10 August" (maintainer rule,
2026-08-05). The day-then-month form reads as a dateline or a filing header,
and this page is a person talking. Use the ordinal when no year follows. With
a year, use the plain form, "August 27, 2026", which is also what the federal
documents this page quotes actually print, so a quoted date and our own date
look like the same language. Eleven of the first 26 shipped captions broke
this. `caption_check.py` fails both the day-first form and a bare "August 27"
with no ordinal and no year.

**NO FIRST PERSON. EVER.** (maintainer rule, 2026-08-05). No I, we, us, our, my
or me anywhere in the caption, outside a straight-quoted source. The page is an
analyst describing the world, never a narrator describing their own work.

**THIS RULE NEEDS TWO CHECKS AND THAT IS THE WHOLE LESSON.** A pronoun grep
over all 26 shipped captions returns ZERO bare hits, so by that measure the
page never had a first-person problem. It had one anyway, and it wore no
pronoun. No.26 shipped "No page anyone could reach shows what SEDS-AK was
worth" and opened a paragraph with "Enclosed,". Both are the studio narrating
its own search and its own envelope, and the first is literally the
de-pronouned rewrite of a slide that says "any page we could reach". Ban the
pronouns and the posture together, or the posture just drops the pronoun and
carries on.

The fix is always the same move. Convert a claim about the SEARCH into a claim
about the RECORD. "No page anyone could reach shows the figure" becomes "No
published page shows the figure." "Enclosed, the objection and the reply"
becomes "The objection and the reply, as printed." What the studio tried is
never the story; what is true is.

`caption_check.py` fails both the pronouns and the named postures. Two
deliberate holes in the pronoun list, so the gate does not cry wolf: "mine" is
omitted because this page covers Graphite Creek, Red Dog and Ambler and "the
mine" is a noun here far more often than a possessive, and an all-caps match
longer than one character is skipped so "the US Air Force" reads as a country.

**NEVER OPEN A SENTENCE WITH "AND" OR "BUT"** (maintainer rule, 2026-08-05).
They are conjunctions that join clauses, so a sentence starting on one is a
fragment wearing a full stop. Join it to the sentence before with a comma, or
drop the word entirely, which usually reads better than either. Currently clean
across all 26 shipped captions, so this gate is preventive: it exists because
the habit is all over the run records and the retros and it would eventually
leak into the copy.

**SPEND FEWER COMMAS.** Budget is **1.05 commas per 100 characters** of caption
body, hashtag line excluded (maintainer rule, 2026-08-05). The number is not a
guess: every shipped caption was measured, 26 of them, and the mean was 1.17
per 100 with a median of 1.12. The budget is ten percent under that mean, which
is what was asked for.

Fifteen of those 26 would fail it, so this is a real constraint and not a
formality. When you are over, the fix is to cut a comma or split the sentence.
It is NOT to reach for a semicolon, which is already banned, and it is not to
run two clauses together without one. A comma splice is worse than a comma.
The rule exists because the house voice is short declarative sentences and a
comma is usually the seam where a sentence should have ended.
`caption_check.py` fails it and prints the count, the density and how many to
cut.

## The ledger contract

After every shipped run the showrunner appends to `ledger/captions.json`:
run_date, opening_move, structure, closing_move, first_words (the caption's
first 8 words), and hook_type. Before writing, the room reads the ledger and
excludes: opening_move used in the last 6 entries, structure in the last 3,
closing phrasing in the last 1. caption_check additionally hard-fails any
caption whose first 4 words match any of the last 12 entries.
