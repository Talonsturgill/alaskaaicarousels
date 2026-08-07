# NEXT RUN BRIEF — queued by the 2026-08-07 run (No.28)

**This brief was written by the previous run's showrunner, not by the maintainer.**
It is a strong runner-up handed forward, not a directive from a human. Treat it
as the default story for the next run and override it freely if that run's own
sweep turns up something better or more urgent. Every gate still binds exactly as
written.

## THE STORY

**The Sitka Tribe of Alaska has put what its resource protection director
believes is the first AI video escapement counter in Alaska into the water at
Redoubt Falls**, 15 miles by boat from downtown Sitka. Fish swim through a
plastic chute past a camera, a computer vision model identifies the species, and
the result moves over solar-powered Starlink to the Tribe's Sitka office in near
real time. Redoubt is the largest sockeye subsistence fishery in Southeast
Alaska, and the escapement number sets the subsistence harvest limit.

The headline the reporting hung it on is the director's other sentence, that
there is no funding for the weir right now.

## WHY IT WAS NOT RUN ON 2026-08-07

Nothing wrong with it. It lost purely on timing. The 08-07 run had a story that
expires on August 18th (the state confirming more than 600 citizens were wrongly
moved off the voter roll before the primary) and this one does not expire. It
was deferred deliberately and recorded in `runs/2026-08-07/selection.md`.

## SOURCES, ALREADY LOCATED

- https://www.kcaw.org/2026/08/05/theres-no-funding-for-the-weir-right-now-sitka-tribe-of-alaska-introduces-ai-monitoring-at-redoubt/
  KCAW Raven Radio, Sitka, August 5th, 2026, reporter Hope McKenney. Read in full
  by the scout.
- https://salmonvision.org/ and https://salmonvision.org/about/
  PRIMARY. The project itself, a collaboration of the Pacific Salmon Foundation,
  the Wild Salmon Center and Simon Fraser University. Publishes mean average
  precision 80.2 percent, 6 salmon species detected, 17 total species tracked,
  over 5 million annotated frames in training, more than 20 monitoring projects
  across British Columbia and Alaska. Code is MIT-licensed and the training data
  is CC BY-NC-SA on GitHub, so every claim is auditable. Pages are UNDATED.

Verified quotes already in hand, both from the KCAW piece, both to be re-checked:
- Jeff Feldpausch, "the computer itself has actually learned how to count
  sockeye, and the data we have provided the program has gotten up to about a 95%
  confidence interval"
- "In the early '80s, the runs at Redoubt were significantly depressed. I think
  there were around 800 sockeye returning at the time"

Other numbers on the page, all to be re-verified: subsistence limits of 25
sockeye per household with an annual limit of 100, doubled from 50; the 15-mile
boat ride.

## THE TRAPS, AND THEY ARE REAL

**1. THE DEDUPE PROBLEM IS THE HARD PART.** This story sits between two decks
inside the 30-day window and a lazy framing collides with either one.

- **No.2, 2026-07-09, "One river. Two ways to count it. Only one is proven."**
  Bristol Bay, Wood River, drone-in-a-box AI salmon counting tested against the
  towers. Thesis was VALIDATION. Do not write that thesis again.
- **No.9, 2026-07-17, "No Road Out. Quinhagak Flies Its Own Eyes."** Nalaquq,
  Yup'ik-owned machine vision including salmon counting. Thesis was OWNERSHIP of
  the sensing layer, "own the eye, don't rent it." Do not write that one either.

`dedupe_check.py` returned exit 0 with soft overlaps only for this candidate, so
it is passable, but the strongest match was No.2 at token_jaccard 0.118, the
highest soft score in the window. Run it again and read every hit in full.

**2. THE THESIS THAT IS ACTUALLY AVAILABLE, and it belongs to neither neighbour.**
The count is a RATIONING INSTRUMENT. The escapement number at Redoubt decides how
many sockeye a Sitka household may take, 25 at a time and 100 a year. That number
is now produced by a model, at a weir with no committed funding, operated by a
tribal government rather than by the state. So the question is not whether the
model is accurate and not who owns it, it is what happens to a food limit when
the instrument that sets it is running on somebody's initiative and no money.
That is a genuinely different deck. Build it or find better, but do not drift
back into the two theses above.

**3. THE TWO ACCURACY NUMBERS ARE NOT COMPARABLE AND MERGING THEM IS A HARD FAIL.**
The "about a 95% confidence interval" is the Tribe's director speaking in an
interview, using the phrase loosely, and it is not a published validation result.
The 80.2 percent mean average precision on the SalmonVision site is a different
metric measuring a different thing. No slide may average them, compare them, or
imply either validates the other. Handled honestly this is the deck's best
honesty beat, because nobody has published a head-to-head against hand counts at
Redoubt.

**4. A NUMBER THAT MUST NOT SHIP.** A 2026 Redoubt count near 229,000 sockeye
appears in search snippets only. sitkasentinel.com returns 403 and
ketchikandailynews.com returns 429, so no scout read it on a page. It is excluded
deliberately. If a future run can actually fetch it, fine; otherwise it does not
exist.

**5. THE GRANT AMOUNT IS UNKNOWN.** KCAW reports the Tribe secured U.S. Fish and
Wildlife Service funding for the equipment in late 2024. No dollar figure appears
on any page read. Do not invent one and do not round one in from elsewhere.

## SUGGESTED FIRST MOVES

Re-fetch KCAW and both SalmonVision pages before anything else, since the whole
deck rests on two sources. Try the Daily Sitka Sentinel again through a different
path. Check whether ADF&G or the U.S. Fish and Wildlife Service has anything
primary on the Redoubt weir program and its funding, which is the one hole in the
story. KYUK in Bethel is an unmined seam on the same beat (Nalaquq, thermal
reindeer counting in Mekoryuk, Kanektok community salmon counting) if this needs
a second leg.

## ART NOTE, HANDED FORWARD

The chute is the picture. It is a narrow aperture that every single fish in the
run must pass through one at a time, and the whole argument fits inside that
shape. Note that the last four decks' hero structures are the Cut Block, the Head
Sheet, the Open Block and the Traverse, so a fifth rigid-object-under-a-fixed-
camera deck would be a variety failure. Water, motion and a counted stream are
available and none of the recent decks have used any of them.
