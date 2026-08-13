# SELECTION — carousel No.32 — 2026-08-13

## The story

**A synthetic "Anchorage local news" site published more than 500 stories in 19
days, told readers on each one that no journalist had read it, then stopped
dead. The pages are still live.**

dailyanchorage.news. Tagline "Local News, Anchorage. Every Day." Articles dated
July 8th through July 26th, 2026 and nothing since, checked August 13th. Every
article we opened carries the sentence "This article was written by AI from the
linked sources and was not reviewed by a journalist before publishing." Its
editorial standards page says the opposite-sounding thing, "Our articles are
produced with AI-assisted research and drafting under human oversight," and
resolves it in the next line, "A human editor reviews flagged content before
publication." Flagged content. Not all content.

It is bylined to desks, Anchorage Tech Desk, Anchorage News Desk, Anchorage
Policy Desk, and no named human reporter appears anywhere on it. It carries the
full furniture of a local paper, politics, property, schools, transport, things
to do, a corrections page and a legal notices page. Its parent, dailynetwork.news,
calls itself "The Daily World, a daily paper for every city," says it is "in a
hyperscale phase," and lists 18 mastheads, every one of them an Australian city.
Anchorage is not on the list.

## Why this one

1. **Concrete Alaska impact.** More than 500 pages branded as Anchorage local
   news are live and indexed right now, in the week Alaskans vote in an August
   18th top four primary. They sit in the same search results as ADN, the Alaska
   Beacon and KDLL. That is a real thing happening to Alaska's information
   supply, and no Alaska outlet has written it up.
2. **Visual potential.** The story is about FORM WITHOUT LABOR, which is a gift
   to an art department. A newspaper's furniture is one of the deepest engraving
   traditions there is, scotch rules, cut rules, section heads, halftone screens,
   correction boxes, dateline slugs. The deck can draw all of it at full fidelity
   and let the absence be the argument.
3. **Tangibility.** Every load-bearing fact is the publisher's own printed
   words, fetched and quoted. Nothing rests on an inference.
4. **Would an Alaskan send this to a coworker?** Yes, and specifically the
   audience this page has, journalists, comms people, civic professionals, all
   of whom are about to have to explain to someone why a plausible Anchorage
   article isn't reporting.

## Dedupe

`dedupe_check` on the candidate fingerprint returns **soft overlaps only**, zero
shared entities, strongest match jaccard 0.008 against No.9 (2026-07-17,
Quinhagak drone training) on the single token "search". No topic in the 30 day
window is remotely this. This is a clean new story, not an update.

It is also a deliberate break from the beat mix. The last 30 days ran heavily on
land, power and elections. This is the first deck in the window about what
Alaskans READ.

## Runner-up, and why it lost

**UAF's $499,000,000 Army contract, announced August 7th** (C30 to C34). The
money is real, primary and rock solid. It lost on the claims gate rather than on
taste. The fact-checker was told to make a genuine attempt to establish an AI or
machine-learning link and could not (C35, C36): the war.gov announcement contains
none of the words artificial intelligence, machine learning, algorithm or data
science; UAF's own newsroom carries no story on the contract at all; and
uarc.gi.alaska.edu returned 503 on both attempts. A half billion dollar defense
story with an unverified AI link can't anchor an Alaska AI deck. It goes to the
docket instead.

Third was the Eielson microreactor town hall of August 26th (C37, C38). The town
hall is verified. Everything that would have made it an AI story is not: the 5
megawatt figure, the 30 year power purchase agreement and the Oklo notice of
intent all died on a page that returned 503, and the link tying Eielson to
AFCEC-26-R-0006 could not be confirmed either.

**AIDEA's Houston conveyance** was ruled out before the fact-checker ran.
`dedupe_check` returns LIKELY DUPLICATE against No.14 (2026-07-22) with four
shared entities and jaccard 0.196, and Beat A independently flagged it as the
spine of No.27 as well. Its August 19th deadline is live and stays on the
docket, where it belongs.

## What the adversarial pass killed, and what that costs the deck

The scouts offered a second leg, a doctored image of a gubernatorial candidate
circulating twelve days before the primary. **It does not survive.** The
fact-checker searched the outlet twice; a site search returned 61 results in
strict date order running August 11th, July 20th, July 3rd, with a clean gap
across the claimed August 6th publication date, and a separate search for
"deepfake" returned four articles, none about a doctored image of any candidate.
Nothing about that image appears anywhere in this deck.

Two counts also died and their replacements are hedged on purpose. The sitemap
would not count the same way twice (1,064 / 501 / 1,012 across three reads), so
the deck says **more than 500** and never a precise figure. The states-with-laws
count would not either (33 / 23), so the deck says **more than 20 states,
according to Public Citizen's tracker as of August 3rd, 2026** and never the
op-ed's "roughly 30".

## Three things the deck must not do

1. **It must not say the site lied.** It disclosed. The disclosure is real, it
   is on the articles, and the about page's claim to disclose on every page is
   true. The story is that full disclosure changed nothing about how the pages
   look in a search result. C11 is in the deck for exactly this reason.
2. **It must not assert the site influenced the election.** The August 18th
   primary is TIMING and nothing more. There is no evidence of any link and the
   deck may not imply one.
3. **It must not repeat the site's own unverified numbers as true.** The $1.6
   billion and the 220 to 205 vote appear only as examples of what the site
   published, never as facts.

A fourth, on judgement rather than evidence. The ownership page names an
individual. The deck's target is a publishing method, not a person, and the
slide-worthy fact there is the ABSENCE of any registered legal entity, not the
name. Leave the name off the slides.

## Dials, carried from plan.md and amended by the Phase 1 refresh

design_variance 4, visual_density 4, type_temperature 2. Density 4 is spent as a
HIERARCHY rather than as uniform coverage, per today's FIELD_NOTES entry: two
declared focal clusters per slide, deliberate quiet elsewhere.
