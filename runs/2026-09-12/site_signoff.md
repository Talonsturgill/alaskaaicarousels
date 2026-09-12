# PHASE 3.6 — SITE SIGN-OFF — 2026-09-12

SITE SIGN-OFF: PASS, 103 pages, 18 checks
GAS WATCH: WARN, read September 11th, 2026, 37 days on record, chart present
SITE FIXES: none needed. Nothing was found that presentation could repair.

## THE CHECKERS

`python scripts/site_signoff.py --out docs` exited 0, 18 of 18 clean, 103 pages,
2 foreign directories skipped and not this repo's to sign off. Every page is on
disk and titled, nothing rendered empty, no machine spill, the house voice holds
in the shipped bytes, 4344 internal links resolve, 101 sitemap entries have
pages, every asset a page asks for is present, and every cron-written ledger's
CURRENT value reaches the page that publishes it: gaswatch.jsonl at September
11th on the gas watch page, power.json at May 2026 and 28.23, power_utility.json
at 2024 and 21.24, docket.json at 24 items on the docket page, watch.json one day
old. The videos passthrough is intact and was not read.

`python scripts/gaswatch_pagecheck.py --out docs` exited 2, which is attention
and never an abort. Fourteen checks pass, one warns.

## THE ONE FINDING, AND IT IS A REPORT CASE

    [WARN] no gap in the series   1 missing, first 2026-09-08

The Cook Inlet Gas Watch series carries 89 records over 37 distinct days from
August 5th to September 11th, and **no record carries the date September 8th**.
That is one hole in a series CINGSA keeps no archive to rebuild from.

WHY IT IS NOT MINE TO FIX. `ledger/gaswatch.jsonl` is cron-written and
append-only, and non-negotiable 19 puts it and its collector off limits to a
routine run. A run that writes it is corrupting a published time series. So this
is reported in the draft and nothing was touched.

WHAT THE RUN FOUND OUT ABOUT IT, so the report is useful rather than a
restatement of the warning. The hole sits immediately after a collector outage.
The `gas watch` workflow failed on seven consecutive scheduled runs, run numbers
224 through 230, from September 6th at 16:26 UTC through September 7th at 18:25
UTC. Run 229 on branch `codex/gaswatch-recovery-2026-09-07` and run 231 on the
merge of PR #347, "Fix Cook Inlet Gas Watch outage and delayed true-ups", both
succeeded, and every scheduled run since has succeeded, runs 232 through 253.
So the collector is healthy now and has been for five days.

The repair left one day behind it. September 8th's three collections all
succeeded and one of them committed "gaswatch(page): rebuilt from 2026-09-08's
reading", yet the ledger holds no record dated September 8th and instead holds
two dated September 7th. The most likely reading is that the source still
published September 7th's figure when the recovered collector first looked, so
the day resolved as a second September 7th record rather than a new one. That is
a question about the collector's date resolution and it belongs to the
maintainer, not to this run.

## THE READ, because a checker cannot judge whether a page reads well

`/gas-watch/`. The meter reads instantly and the big figure agrees with the tiles
and with the gauge: 59.0 percent of design, 7.67 of 13.0 Bcf, flag at 7.67. The
four stat tiles agree with the chart axes. Nothing is cut off or crowded. The
page still refuses to say whether supply is adequate, and says so in its own
section, naming a compressor failure and a sanded well as the reason a
comfortable-looking day can still produce curtailment. Counted nouns agree with
their counts throughout; a scan for the "1 days" class found nothing.

One thing was checked and is NOT a defect. The gauge prints "Since the last
reading, 22.5 MMcf into storage" and a tile prints "22.5 MMcf/d injection rate
now". Those are two different measured quantities that coincide today because the
reading gap was one day. `inventory_delta_mmcf` is the change in inventory
between readings and `injection_in_progress_mmcfd` is the rate the field
publishes, and their labels already carry the distinction. No change.

`/` and `/docket/`. Both read clean. The homepage section order is as the
routine fixes it, hero then the scanner then Our Latest Video then Our Latest
Article then the docket then the beats. The docket header stat reads SEP 14 as
the next date, which is the AIDEA comment deadline and is a `deadline` kind, so
the role and the slot agree. Three items show open to the public and the ledger
holds three.

A SECOND JUDGMENT CALL, recorded so it is not mistaken for an oversight. Archive
and deck cards stamp their date in mono caps as "SEPTEMBER 11, 2026", which is
neither the ordinal form the house rule prescribes for a sentence nor ISO. It is
used uniformly on all 56 cards, and prose on the same pages correctly reads
"September 11th, 2026", so the site runs two registers rather than one register
inconsistently. brand.yaml's own scope note exempts a provenance stamp where the
date is a citation rather than a sentence, and a card's date stamp is that. Left
alone deliberately. If the owner wants the card stamps in the ordinal form too,
it is one change in `site_build.py` and it touches every card at once, which
makes it the owner's call and not a run's.
