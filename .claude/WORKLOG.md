# WORKLOG: site audit remediation (T1 to T7)

Maintainer-supplied audit, 2026-08-04. Verify-first protocol: every claim was
probed before any edit. Two PRs. T1 to T4 are correctness and ship together;
T5 to T7 are business surface and ship second.

## Verification results (all probes run on main @ 2026-08-04)

| task | claim reproduced | evidence |
|---|---|---|
| T1 | YES | line 4957 "six beats", line 2563 "seven standing beats", TOPICS=7 |
| T2 | YES | home sums to 47 citations, data/sources count 43 distinct URLs, same label |
| T3 | YES | exactly one drift, gvea-lm6000-turbine-purchase, 2026-07-30 vs 2026-08-01 |
| T4 | PARTIAL | hist=2 srcs=2 and both news, YES. "thinnest on the board" NO, six items have hist=1. Proposed fix of adding the 2026-08-23 date is unnecessary, it already exists with kind=decision |
| T5 | YES | SOCIALS X entry is https://x.com/Microvestapp, all others alaskaai |
| T6 | YES | docket_page 0, archive_page 0, topic_page 1, sources_page 1, questions_page 1 |
| T7 | YES | grep count is 0 |

T0 false findings were NOT acted on. Confirmed each is working as described.

## T4 root cause (answers the PR question)

Neither a missing date nor a trigger bug. Phase 3.5 step 2 refreshes items
whose next key date is "within 7 days or has passed". Enstar's next key date
is 2026-08-23, which is 19 days out from 2026-08-04, so the near-date trigger
correctly has not fired. air-force-eul carries a 2026-08-10 milestone, 6 days
out and inside the window, which is why it gets near-daily notes.

The real gap is that the window is blind to STAKES. A 19-day-out RCA decision
on the Cook Inlet gas shortage deserves primary filings on file well before
day 7. Fix is the primary documents plus a proposal, not a trigger change,
because widening the window for everything would multiply fetches across all
12 items for no gain on the quiet ones.

## Status

| task | status |
|---|---|
| T1 beat count interpolated | DONE |
| T2 one source_doc_count helper + aggregate_check --site assertion | DONE |
| T3 repair data + append_history + docket_dates_check gate | DONE |
| T4 sources + date correction + root cause report | DONE |
| PR 1 (T1-T4) | open |
| T5 X handle | not started, needs maintainer answer |
| T6 civic page CTAs | not started |
| T7 public sector proposal | not started, proposal only |
| PR 2 (T5-T7) | not started |

Delete this file when all rows are DONE.
