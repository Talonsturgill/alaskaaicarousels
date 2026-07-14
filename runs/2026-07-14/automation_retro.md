# Automation retro — 2026-07-14 — Carousel No. 7

## Diff: what happened vs what the routine says should happen

Walked run_state.json phase by phase.

- **Phase 2 research (deviation, root cause of the whole run's shape).** The
  routine spawns SIX scout subagents in parallel. All six died on the same
  hard error: "Agent terminated early due to an API error: You've hit your
  weekly limit, resets 5pm (UTC)." This is an account-level usage cap, not a
  transient failure. By inference every other subagent (fact-checker,
  treatment-directors, copywriter, pixel-critics, flow-critic, scorer,
  upgrade-engineer) would fail identically. Spawning all six at once burned
  budget on six doomed calls before the signal was clear.
- **Phases 3, 5, 6, 8, 10, 12 (degraded to solo).** Per the FAILURE PROTOCOL
  and the Phase-12 "if subagents are unavailable, the showrunner executes the
  same steps" clause, the showrunner ran research, fact-check, treatment,
  copy, pixel review (by reading every render PNG and the contact sheet), and
  scoring directly in the main loop. Main-loop WebSearch/WebFetch and the
  Gmail/GitHub MCP tools were unaffected throughout.
- **Engine (no breakage).** render.py, qa.py, assemble.py, site_build.py,
  caption_check.py, style_lint.py, docket_alerts.py all behaved exactly as
  documented. machine QA PASSed with zero warnings on the first full render
  after two cosmetic fix passes. Vector PDF at 2.63 MB. No environment
  breakage, no installs failing, no 403/429 on the primary tools. The 07-13
  font-style QA probe upgrade held (Fraunces/Space Grotesk/JetBrains Mono all
  loaded clean).
- **Date boundary (handled).** Trigger fired at Anchorage 2026-07-13 20:10
  (UTC 07-14 04:10) after the 07-13 edition had already shipped; dated this
  run 2026-07-14 to avoid a same-date collision. Not a defect, a boundary
  case worth a FIELD_NOTES line (added).

## Frontier scan

Focus rotation (last: editorial-dataviz 07-10, procedural-art + 3D 07-11,
accessibility/PDF 07-12, headless-Chromium/Playwright 07-13). This run's
natural focus is **self-improving-pipeline resilience / graceful degradation**,
surfaced directly by the weekly-limit incident.

HELD TO ZERO SEARCHES this run, deliberately. The account weekly usage limit
that killed the subagents is the same pool the main loop draws from; the run's
one irreplaceable deliverable is the Gmail draft, and spending discretionary
search budget on a frontier scan risked that deliverable. The reactive lesson
was captured from this run's own evidence instead of an external scan. The
"canary-first fan-out" idea (spawn one subagent, read its error before fanning
out) is PARKED as a candidate rather than forced in, because serializing a
canary adds latency to every healthy run to save budget only on the rare
limit-hit run; the codified FAILURE-PROTOCOL clause below is the safer,
zero-latency version of the same fix.

## Upgrades implemented this run: 1 (reactive fix)

1. **FAILURE PROTOCOL clause: usage/weekly-limit errors are terminal for the
   subagent layer.** Codifies exactly what this run did: on an account usage
   or weekly-limit API error from any subagent, do not respawn or fan out
   further (it only burns the shared budget), switch immediately to solo
   showrunner execution, hold the score conservatively for the missing
   independent critic pass, and disclose the degraded pass in the Gmail draft.
   Area: prompt (prompts/routine_instructions.md). Kind: fix. Weakens no gate,
   threshold, or hard-fail rule; it only removes wasted retries and makes the
   already-correct fallback explicit. Verified by review (prose clause, no
   engine/script change, so no render/qa re-run applies).

No engine or script code changed this run, so the render.py + qa.py
verification bar (which applies to engine/script upgrades) is satisfied
vacuously; the demo-deck and this run's slides both rendered and QA-passed
cleanly during the normal pipeline.
