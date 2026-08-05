# WORKLOG — code review remediation, 2026-08-05

Fifteen findings from a full-repo review (repo, site, all crons). Four
reproduced by execution before any fix was written. Branch:
`claude/master-prompt-task-fcgu4x`, restarted from `main` at f803688.

## Approved scope

Fix all fifteen. Ship as one PR, ready not draft, merged same session per
CLAUDE.md delivery policy.

## The measured reason behind the ordering

Findings 1, 2, 4 and 11 can each cost a day of the Cook Inlet series, which
CLAUDE.md names as the one irreversible failure this project has. They go
first regardless of how small the diff is. Efficiency work (15) goes last
because it changes no behaviour.

Reproduced before fixing:
- F1 `gaswatch_pagecheck.py --self-test` exits 1 on a stale `docs/`, and it
  runs BEFORE the collector, so the day's CINGSA reading never gets written.
  A refit commit from `gaswatch-eia.yml` arms it, since that workflow writes
  the model and does not rebuild the page.
- F2 EIA-191 storage lagging deliveries leaves `eia_months_checked` set with
  `eia_ak_working_gas_bcf` absent. Confirmed absent.
- F6 `stale_model_output` compares the model against itself. With the model
  moved +7, figures said 111, the page said 104, verdict was None.
- F11 A model with no `fit` block crashes `page_body` with KeyError.

## Task table

| # | Finding | Severity | Status |
|---|---------|----------|--------|
| 1 | pagecheck self-test not hermetic, blocks collection | series loss | DONE |
| 2 | EIA storage lag -> page KeyError -> build dies | series loss | DONE |
| 4 | rebase of generated docs discards ledger append | series loss | DONE |
| 11 | None-valued figures indexed unguarded | build crash | DONE |
| 8 | gaswatch_eia summary KeyError after a good pull | false red | DONE |
| 5 | HDD history never extended, refit freezes | false claim | DONE |
| 6 | page check cannot fail on a stale page | toothless gate | DONE |
| 3 | GITHUB_TOKEN push does not trigger pages.yml | page not live | DONE |
| 9 | `date -u` used where Anchorage date is required | wrong day | DONE |
| 7 | JSON-LD still says two point calibration | false claim | DONE |
| 10 | 28 days accepted as a whole month | fit skew | DONE |
| 12 | docket_alerts --dry-run writes the ledger | contract break | DONE |
| 13 | assemble.py finally block masks the raster fallback | no PDF | DONE |
| 14 | docket_alerts emits bare "August 10" | house rule | DONE |
| 15 | figures() recomputed 4x, load_hdd_history 9x | efficiency | DONE |

## Measured outcome

- Site build 1.02s to 0.30s. figures 4 to 1 real computation, backtest_facts
  4 to 1, eia_crosscheck 4 to 1, load_hdd_history 9 calls to 1 parse. Output
  byte-identical apart from the two intended copy fixes.
- 128 of 128 model shapes (every anchor subset, with and without a fit block)
  now build. Four crashed before.
- docket_alerts.py had NO self-test, which is how both of its bugs survived.
  It has one now, and it goes red on the bare-date bug it was written for.

## Corrections to the review

- Finding 13 claimed the early `return False` in vector_pdf leaks the two
  directories. It does not; that return runs before they are created. The
  finally-block half of that finding was right and is fixed.

## File map

- `.github/workflows/gaswatch.yml` — hermetic gates, collect before page work,
  ledger commit split from docs commit, Anchorage date
- `.github/workflows/gaswatch-eia.yml` — HDD extend step before the refit
- `.github/workflows/pages.yml` — workflow_run trigger so bot pushes deploy
- `scripts/gaswatch_pagecheck.py` — hermetic self-test, page-reading peak check
- `scripts/gaswatch_build.py` — optional-key guards, whole-month test, one
  figures() threaded through
- `scripts/gaswatch_eia.py` — summary guards
- `scripts/gaswatch_fit.py` — calendar whole-month test
- `scripts/gaswatch_hdd.py` — NEW, extends the observed HDD record
- `scripts/site_build.py` — measurementTechnique from config, threaded figures
- `scripts/docket_alerts.py` — dry run writes nothing, ordinal dates
- `.claude/skills/carousel-engine/assemble.py` — defensive cleanup

## Wrap

- [x] all four self-tests clean
- [x] site rebuild + pagecheck PASS
- [x] pushed, PR ready, merged
- [x] delete this file
