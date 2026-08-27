# PHASE 3.6 — SITE SIGN-OFF — 2026-08-27

SITE SIGN-OFF: PASS, 86 pages, 18 checks
GAS WATCH: PASS, read August 26th, 2026, 22 days on record, chart present

## The checkers

`python scripts/site_signoff.py --out docs` exited 0, 18 of 18 clean, 86 pages
plus 2 foreign directories skipped (docs/videos/ and docs/awesomeproposal/,
neither of which is this repo's to sign off). Every cron-written ledger reaches
the page that publishes it: gaswatch.jsonl at August 26th, power.json at May
2026 and 28.23, power_utility.json at 2024 and 21.24, docket.json at 22 items,
watch.json 1 day old.

`python scripts/gaswatch_pagecheck.py --out docs` exited 0, 15 of 15 clean.
The reading is current, the headline figure of 56.0 percent of design reaches
the page, the series is continuous over 22 verified days, the modeled peak of
133 MMcf per day is reproducible from the published formula, and the page still
refuses to say whether supply is adequate.

## What a person actually looked at

Rendered `docs/index.html`, `docs/docket/index.html` and
`docs/gas-watch/index.html` in Chromium at 1440 wide and at 390 wide, the phone
case, and read them.

- No page scrolls horizontally at either width. Measured scrollWidth against
  viewport width on all six renders and every one matched.
- The gas watch meter reads instantly and the big figure agrees with the tiles.
  56.0 percent of design against 7.29 of 13.0 Bcf, 28.4 MMcf per day going in,
  154.8 MMcf per day of withdrawal capacity, 133 MMcf per day modeled peak, 22
  days on record. Nothing is cut off or overlapping on a phone, and the three
  stacked series render cleanly at 390 wide with their own axes.
- Nothing on that page asserts a state the data could flip, and no sentence
  contradicts a number beside it. The three series carry separate scales with
  the reason printed, which is that they are different in kind.
- The retail price sparkline was checked specifically for the finger case,
  because a mouse-only version of it shipped once. Its 120 monthly rects are 1
  to 6 px wide at phone width, which would be dead under a thumb, and they are
  not the touch mechanism. `power_panel.py` hit tests the x position from one
  listener on the svg, and `.pwtouch` swaps the instruction line on
  `hover:none`. Working as designed, nothing to fix.
- Counted nouns agree with their counts on the pages read.

## One thing that looks like a defect and is not

`Our Latest Video` does not render when the homepage is opened from the local
filesystem. The section skeleton is baked with `hidden` and the newest entry is
pulled live from `videos/videos.json`, which a `file://` page can't fetch, so
the section stays hidden in a local render and appears over HTTPS. The
passthrough file itself is intact and is another repo's to own, so nothing here
was touched. Confirmed the same way `site_signoff.py` does, by reading the
bytes rather than the builder.

## SITE FIXES

None. Nothing was found that needed repair, so nothing was changed. Both
checkers were clean before the run touched anything and the reader-level pass
turned up no layout, wording or link defect on the three pages read.

## UNFIXED

None.
