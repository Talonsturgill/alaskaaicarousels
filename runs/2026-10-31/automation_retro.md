# Automation retro, run No.101, October 31st

The machine pass is weekly. `machine_due.py --date 2026-10-31` returned exit 1: the last pass was 2026-10-25, six days ago, and it falls due at seven. No upgrade-engineer ran and no upgrade commit was made. The queue now holds 45 open items, four of them bumped and four added by this run.

## trend_check reading (window 10, 2026-10-21 to 2026-10-31)

- Top repeat offender: Artwork craft, the weakest criterion on 7 of the last 10 runs (mean 7.21, this run 7.5). Its last upgrade was 2026-10-04 and trend_check marks it STALE.
- Decision: it is DEFERRED to the weekly pass, which falls due tomorrow. That pass should take the recurring theme from this run and the last two: the largest object is drawn with a helper that fails at the deck's scale, and the deck rebuilds the drawing inline mid-review. This run's 04, Tanaka contours in place of scribed hachure, is the newest instance and is queued as `akscribe: scribeRelief at state scale ... reads as fur`.
- What would have to be true to work it today: nothing here prevents it except the weekly rule, and it is not this run's job to make the machine change.
- Defect classes that keep shipping: busy art under text (5 runs) and art touching glyphs (4 runs) both shipped again as WARNs on 03 and 04.
- The weekly pass should also look at the label knockouts this run hand-built on 04, a third instance of the same fix.

## Deviations, phase by phase

- Wake: the run woke at 22:04 AKDT on October 31st (06:04Z November 1st). `run_guard` needs `--run-date` passed by hand or it guards tomorrow; the queue item is bumped to repeat 3.
- Phase 3.6, Gas Watch: the first live audit FAILED "source reading published". The evening slot had not been collected. I fixed it by dispatching `gaswatch.yml` on main (run 41279655464); the re-audit PASSED at 06:14:32Z and no incident was needed. This is repeat 17 of the queued evening-slot item.
- Phase 3.5 and the site: the docket commit adding the FCC GCI-Quintillion item landed without a site rebuild. `site_fresh` caught it at Phase 8 and the rebuild was committed separately (3f43deca). The gate worked as designed.
- Phase 6 and 8, subagent output: the fact-checker and copywriter returned their JSON only in their transcripts. I extracted it with Python from the subagent JSONL, which worked but is fragile.
- Phase 8, review: the pixel critics scored round 1 at 4.6 to 7.0, every slide a revise, and round 2 at 6.2 to 7.6. The flow critic came in at 7.2 after round 2. Round 3 worked its order. Round 4 was the craft-floor cycle. All four rounds were used and the cap was never reached.
- The site line idiom: critics named alaskaaihq.com illegible on seven frames, because the house colour #46545F only works on near black. I fixed it once across the deck. No gate measures fixture contrast; that queue item is bumped.
- Tooling papercuts, both queued:
  - `caption_check.py --copy` with no caption path blocked on stdin until the tool timeout.
  - A re-run without `--deck-summary` overwrote the passing caption_report.json with FAIL. I restored it immediately.
- New aggregate: adding a strip unit label on 05, "ONE CELL, ONE MONTH", tripped `aggregate_check` as an undeclared duration. I declared it as `design`. The gate behaved correctly.
- Copy drift: split SVG tspans on 05 render as two strings, so copy.json was updated to match. copy_sync caught it.
- Ledger: I wrote two beat slugs that do not exist and caught them by hand before the final build. That queue item is bumped.
- Phase 10, scoring:
  - First score: 8.355 with art at 7.0.
  - Craft cycle on frames 05, 04, 07, 03, 06 and 08.
  - Re-score: 8.485 with art at 7.5.
  - Three of the six repairs did not fully land in the pixels, according to the re-scorer: 03's top arc, 06's far cable fin and 07's glint shape. The cap on scoring cycles was reached, so they ship as known shortfalls and are named in the email.
- Subscriber alert: `docket_alerts.py` sent one Buttondown email, the DeepGreen Cook Inlet near-deadline alert for November 2nd, deduped in ledger/alerts.json.

## Queued this run

1. caption_check blocks on stdin without a caption path (new).
2. caption_check overwrites a passing report on an argument error (new).
3. akscribe needs a Tanaka contour helper; scribeRelief reads as fur at state scale (new).
4. A contre-jour sun under about 6 degrees behind a tall object floods the foreground with shadow (new).
5. Bumped: unknown beat slugs, run_guard's UTC date, no gate on fixture contrast, and the gas watch evening slot.
