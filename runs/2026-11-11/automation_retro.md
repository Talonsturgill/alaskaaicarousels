# Automation retro, 2026-11-11 (No.112)

## Trend check, top repeat offender

`trend_check.py --window 10` names Insight density and factual weight as the STALE weakest criterion (last worked 2026-09-06). This run's scorer gave it 7.5 for 04 being thin and for printing no yardstick for $0.40/MWh. Handed to today's weekly machine pass, which works the week's recurring themes first. Recurring QA warns in the window: tiny-text, contact shadow, axis census (4 runs each).

## Deviations, phase by phase

- Phase 3.5 docket: the STAK decision refresh pushed the inline ask payload over its 190,000-byte ceiling. Fixed in-run by packing each date slot to [day, label] in `scripts/ask_answers.py` ship(), because the page reads only those two fields. Headroom is now 2,147 bytes. The queue item is at repeat 2, so the weekly pass is due today.
- Phase 3.6 cron: a ghost queued `gaswatch.yml` run that GitHub refuses to cancel (409). Collection is fine. Recorded in cron_incidents.json and the gate shows WARN. Re-check next run.
- Phase 7/8 art: the column-march renderer (AKP.march) printed a staircase along every crest on 02, 04 and 08 for three critic rounds, and machine QA never flagged it. Root cause: the rows under a crest silhouette were blended from the crest in front. Fixed in the helper by interpolating from the bisected emergence point, plus sub-column supersampling. Queued: a qa probe for it.
- Phase 8: akhaul's GPU sky canvas is half resolution, so the 09 aurora smeared and a sky blur left a light rim at the frame edges. Worked around on the frame. Queued.
- Phase 8: moving 04 to the GPU plain tripped dossier_check's cap on primary marks ("gpu render" on four frames). The gate was right; 04 moved to the column march.
- Phase 8: the critics, the flow critic and both scorers repeatedly asked to seat 03's Base Rate level on the snow crust. That would draw a sum, and C30 says the rent is the larger of the two. Declined on the honesty guard every round, with the reason in BUILD RECONCILIATION.
- Phase 10: scored 8.49 with art 7. The craft floor cycle on 07, 03, 04, 02 and 09 brought art to 7.5 and the total to 8.57. That used 4 of the 5 rounds.
- Phase 11: `docket_alerts.py` sent one subscriber alert (Enstar's Cook Inlet gas storage, deadline in 2 days). The key was set under the `Buttondown` name, not `BUTTONDOWN_API_KEY`, which the script also reads. `prune_runs.py --apply` was blocked by the session's permission classifier as a delete under runs/. It was not retried, and nothing old was pruned this run.
- Rubric weights still sum to 1.10 (queued earlier, an owner decision). 8.57 by the formula is 7.79 normalized.

## Machine pass

machine_due exit 0, so the weekly pass ran today. Its changes are the separate `upgrade(2026-11-11)` commit, logged in ledger/upgrades.json.

Weekly pass result (upgrade-engineer, commit d747a24e):
- Ask pack: passed key dates are retired from the model pack by rule (the first, the newest three, every upcoming). 31,894 tokens became 30,928, and the 32,000 ceiling is untouched. The inline ask payload sits at 187,958 of 190,000 bytes; that one is the owner's call.
- caption_check writes its report atomically.
- akhaul's GPU sky draws at full device resolution.
- Phase 8 names one five-round budget shared by the pixel, flow and craft rounds.
- Deferred, with reasons in ledger/upgrades.json: artwork craft (no shared machine cause), the recurring soft QA warns, insight density (weakest on 1 of 7 runs). Escalated: the rubric weights summing to 1.10.
- Frontier, parked: carousel PDFs ship untagged because the per-slide merge drops Chromium's structure tree.
