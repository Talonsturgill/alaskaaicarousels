# WORKLOG: docket dates have roles (2026-07-29)

## The defect, confirmed

`ledger/docket.json` entry `aidea-houston-industrial-park` carries three
key_dates: JUL 13 milestone, AUG 13 `vote` (Houston City Council, a different
body, on a different question), AUG 19 `deadline` (the DNR public comment
close). `docket_build.next_date()` returns the soonest UPCOMING date of ANY
kind, so AUG 13 wins, and four surfaces then render another body's vote as
this entry's comment deadline, including a gold call to action reading
`COMMENT NOW · CLOSES AUG 13`.

Ground truth, Alaska DNR Online Public Notices id=224431, ADL 234762:
comment closes **5:00 PM, Wednesday, August 19, 2026**, Alaska time, not
extended. The entry's prose, timeline rail and change notes are all correct
and sourced. Only the chrome is wrong.

Live from 2026-07-21 (when the AUG 13 vote was added to the ledger, per the
entry's own history note) through 2026-08-12. Subscriber alerts on 2026-07-17
predate that and were NOT affected.

## Approved scope

Fix the mechanism, not the entry. Five invariants: dates have roles; an
action CTA renders only its own action's deadline; absent or ambiguous means
render no date; status follows the deadline automatically; one resolved
value per role per entry, read by every surface.

## Decisions and the measured reason

- **`kind` already is the role.** The schema has deadline | vote | decision |
  milestone. No schema change is needed and none is made: the bug is that
  `next_date()` ignored `kind` entirely.
- **Deadline PASSED degrades, deadline ABSENT does not.** Rule 3 says a CTA
  with no date is fine; rule 7c says OPEN implies a future deadline. Those
  conflict only if "no deadline recorded" and "deadline expired" are treated
  alike. Unknown close date keeps the CTA and shows no date. Expired close
  date degrades access to closed and status to pending-decision.
- **Degrade in the renderer, assert in the gate.** A build that hard-fails
  the morning after a deadline passes would break an autonomous daily run.
  The renderer degrades with no human intervention (rule 4) and the gate
  fails if the rendered output ever shows OPEN without a future deadline
  (7c/7d). Both rules are satisfied, neither breaks the routine.
- **The degraded shape reproduces what humans already did by hand** for
  entry 02 (STAK): status pending-decision, access closed, once its window
  closed. That is the confirmation the shape is right.
- **Header NEXT DATE binds to the headline date, not the raw next event.**
  It understates by 6 days today (AUG 19 not AUG 13) and can never again
  present another body's vote as the marquee item's deadline. The AUG 13
  vote stays fully visible on entry 01's timeline rail.

## File map

| File | Change |
|---|---|
| `scripts/docket_build.py` | roles, `resolve()`, role-aware chip/CTA/card, degradation |
| `scripts/site_build.py` | header stat + homepage line read the resolver |
| `scripts/docket_alerts.py` | window-open alert reads the action deadline |
| `scripts/gmail_draft.py` | daily draft reads the resolver, not its own min() |
| `scripts/docket_dates_check.py` | NEW: fixtures 6a-6f + real-build cross-surface gate |
| `.github/workflows/docket-dates.yml` | NEW: CI wiring |
| `scripts/gate_status.py` | new gate row |
| `prompts/routine_instructions.md` | Phase 11 wiring |
| `ledger/docket.json` | dated correction note on entry 01 |

## Status

| # | Task | Status |
|---|---|---|
| 1 | Reproduce symptom string by string | DONE |
| 2 | Ground truth from DNR primary source | DONE |
| 3 | Mechanism with file/line refs | DONE |
| 4 | Blast radius across entries and surfaces | DONE |
| 5 | Roles + resolver in docket_build.py | DONE |
| 6 | Surfaces read the resolver | DONE |
| 7 | docket_dates_check.py with fixtures 6a-6f | DONE |
| 8 | Prove the guard fails on a broken fixture | DONE |
| 9 | CI + gate_status + routine wiring | DONE |
| 10 | Rebuild docs/, correction note on entry 01 | DONE |
| 11 | Commit, push, PR, merge per delivery policy | TODO |

## Wrap

All tasks DONE except the push/PR/merge, which is task 11. Delete this file
once that lands.

Incidental, called out in the PR: the previously committed `docs/site.css`
carried `background-image:url(none)`, so the last build ran without Pillow and
the live site lost its grain texture. Rebuilding with Pillow restored it. No
code change, no hand edit; it is what `site_build.py` emits.
