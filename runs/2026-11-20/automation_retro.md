# Automation retro, 2026-11-20 (No.120)

## Trend check (window 10)
Top repeat offender: Artwork craft and genuine detail, weakest on 8 of 10 runs, mean 7.15, last worked 2026-11-11 (STALE). This run scored art 6.5 and it was again the weakest criterion. DEFERRED to the weekly pass (machine_due exit 1: last pass 2026-11-17, due at seven days). What would make it tractable there: this run's round 1 sent all ten frames back for flat large faces (press body, plat sheet, calendar leaf, envelope, snow), the same cause the week digest keeps counting; a doctrine or helper change that gives every per-pixel and canvas ground a default lamp falloff, tooth and contact cast would remove a round of work on most decks.

## Deviations, phase by phase
- Wake: woke 2026-11-21 06:04Z for run date 2026-11-20 (21:04 AKST). run_guard CLEAR. $CLAUDE_EFFORT recorded medium though settings carry high; noted by the scorer, not a gate.
- Phase 3.6: gaswatch_health FAILED on late_post at wake, the same signature as No.118 and No.119; dispatched gaswatch.yml and Pages, re-audit PASS at 06:18Z. The queued 2026-11-18 item already carries this.
- Phase 7 to 8: aggregate_check could not verify a from_claim declaration on word numerals; slide 04 reworded. QUEUED.
- Phase 8: copy_sync_check and qa.py were first run with the wrong arguments (qa.py has no --slides-dir; copy_sync_check needs --copy and --render-report). Cost two invocations, no change needed.
- Phase 8: caption_check run without --deck-summary wrote FAIL over a passing caption_report.json because out/<date>/deck_summary.txt did not exist; re-run with the line and the file written. The 2026-11-08 fallback works only when that file exists; no queue item, the run should write it in Phase 6.
- Phase 8: round 1 verdicted all ten frames revise; four pixel rounds were used, 06 and 07 held out to round 4, and the flow round was the fifth. Slide 07's relief was asked for across the sheet four times while the DEM covers only the hills. QUEUED (DEM coverage check).
- Phase 8: assemble.py exceeded the 120 s tool timeout twice (30.7 MB vector PDF); run with a longer timeout. shrink_pdfs declined the PDF (its guards), so it ships at 29.3 MB, above the rubric's 25 MB band.
- Phase 10: scored 8.075 against 7.7 (5 of 5 rounds), art 6.5 under the 8.5 craft floor, exempt at the cap. No hard fails.
- Phase 11: docket_alerts sent one subscriber email for the new Alaska LNG comment window (its own ledger-deduped sender).

## Queue
2 new items in knowledge/MACHINE_QUEUE.md. The weekly pass is not due today (machine_due exit 1, last pass 2026-11-17), so there are no upgrades this run.
