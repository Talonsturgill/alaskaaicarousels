# Automation retro, 2026-11-17 (No.117)

## What broke in this run and was fixed in it
- news.yml (and four other Playwright workflows) failed on the ubuntu-latest runner image; maintenance PR #502 pinned them to ubuntu-24.04 and added tests/workflow_runners.py. Merged, news.yml re-dispatched and green; cron_health PASS.
- cron_health's git fetch timed out and left .git/shallow.lock, failing its own retries. Removed by hand in-run, then fixed at the root in the weekly pass.
- render.py crashed under memory pressure on nine heavy frames when not batched; renders were done in threes in-run, then fixed in the weekly pass (recycle every 3 slides, one crash retry).

## Weekly machine pass (due today), upgrade(2026-11-17) 7cf0cdd64
- render.py recycles the browser every 3 slides and retries a slide once after a browser or renderer crash; per-slide memory in the report.
- dedupe_check adds an earlier-coverage tier to 120 days and exits 1 on a likely repeat inside the topics ledger's 90-day rule (it would have caught No.77 at 44 days).
- cron_health gets a 600 s fetch, process-group kill on timeout and safe removal of its own stale shallow.lock.
- akthree audit warns on ground_edge and fog_seam; qa.py surfaces both.
- Escalated to the owner: rubric weights sum to 1.10.

## Queued (knowledge/MACHINE_QUEUE.md)
- Nothing new beyond the items the weekly pass closed or annotated.
