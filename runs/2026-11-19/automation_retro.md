# Automation retro, 2026-11-19 (No.119)

## Trend check (window 10)
Top repeat offender: Artwork craft and genuine detail, weakest on 7 of 10 runs, mean 7.15, last worked 2026-11-11. This run's craft cycle lifted art from 7.0 to 7.5 on frames 03, 06, 09 and 08. The machine work on it is DEFERRED to the weekly pass (machine_due exit 1: last pass 2026-11-17, due at seven days). What would make it tractable there: the week digest's flow-critic causes, which keep naming large flat faces drawn with uniform texture (this run's 03 door, No.118's plate). That is a doctrine or helper change, and it belongs in the weekly pass, not in a daily fix.

## Deviations, phase by phase
- Wake: woke 2026-11-20 06:04Z for run date 2026-11-19. run_guard CLEAR.
- Phase 3.5 docket: the AIDEA note's sources were appended as bare URL strings, and the ask_answers self-test crashed with a TypeError inside site_build. Fixed in-run by rewriting them as {url, outlet, date} dicts. QUEUED: docket schema validation should reject that shape with a named remedy.
- Phase 3.6: gaswatch_health FAILED at wake on late_post, the same signature as No.118. Dispatched gaswatch.yml (run 44685887939) and Pages (run 44686193005), and the re-audit PASSED at 06:15Z. Raised the queued 2026-11-18 item to repeat 1.
- Phase 8 build: AKT.setup threw "existing context of a different type" on 01 and 05 when the slide took a 2D context first. Fixed in-run with supersample: 2. QUEUED.
- Phase 8: render.py --only-exact is a flag that takes --only. Cost one wasted invocation, and no change is needed.
- Phase 8: bespoke_check FAILED 01 against 05 (99 percent the same door staging). 05 was rebuilt as a wall clock. The gate did its job.
- Phase 9: qa caught an undeclared dateline-strip mark three times on 01 (a foreground jamb, a DOF edge and a floor pool peak). Each fix was real.
- Phase 10: the score report's criteria were first persisted as a dict keyed by name. ship_gate's _art_score reads a list of {name, score}, so the CRAFT FLOOR row failed closed until the report was rewritten as a list. Cycle 1 used the dict shape too, but it was never gated. The gate is right to fail closed, and the fix was to persist the scorer's list shape. No queue item: it was the showrunner's transcription, not the machine.
- Scores: cycle 1 8.59 (art 7.0), craft cycle (round 4), cycle 2 8.67 against 7.7 (art 7.5), no hard fails.

## Queue
2 new items and 1 repeat raised in knowledge/MACHINE_QUEUE.md. The weekly pass is not due today (machine_due exit 1), so there are no upgrades this run.
