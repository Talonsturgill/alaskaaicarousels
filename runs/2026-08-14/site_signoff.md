# PHASE 3.6 — SITE SIGN-OFF, 2026-08-14

    SITE SIGN-OFF: PASS, 76 pages, 18 checks
    GAS WATCH: PASS, read 2026-08-14, 10 days on record, chart present

Both checkers exited 0. Re-run after the ship rebuild at --date 2026-08-14, now covering 76 pages including this run's own deck page. `site_signoff.py` cleared all 18 checks, including the
one no build gate can make, that the current value in each cron-written ledger
actually reaches the page that publishes it. gaswatch.jsonl reads August 14th,
2026 on the page, power.json reads May 2026 at 28.23, power_utility.json reads
2024 at 21.24, docket.json shows 20 tracked. `gaswatch_pagecheck.py` cleared all
15, including the two that matter most on that page, no safety verdict and no
claim about learning the page does not do.

## What the eye found that the checkers could not

The docket page's NEXT DATE stat was reading AUG 13, a date that had already
passed. That is not a builder defect and the fix is a rebuild, which is exactly
the failure this phase exists to catch. docs/ on main was generated on August
13th, so the live page has been advertising a spent date all day. Rebuilding
with today's date resolves it to AUG 19, the DNR comment close, which is the
correct next date. Confirmed by building into a scratch directory and reading
the stat row out of the emitted HTML before touching docs/.

Gas watch read at desktop and at 390 px. The meter reads instantly, 52.9 percent
of design capacity, and the big figure agrees with the tiles beside it, 6.88 of
13.0 Bcf and 42.4 MMcf into storage on the day. The utility price table lines up
at phone width with no wrapping collision, Kotzebue at 47.90 and Ketchikan at
12.48 both legible with their bars. No sentence contradicts a number beside it
and the page still refuses to say whether supply is adequate.

## Fixed this run

    SITE FIXES: rebuilt docs/ with the run date so the docket's NEXT DATE stat
    stops advertising August 13th, a date that has passed, and resolves to the
    August 19th DNR comment close.

## Report only, not this routine's to touch

Nothing. No collector has stopped and every cron-written ledger is inside its
cadence.
