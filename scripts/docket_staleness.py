#!/usr/bin/env python3
"""Name the docket items that MUST be re-verified today, and refuse to let one rot silently.

WHY THIS EXISTS (2026-08-06, maintainer: "I am afraid that it is not checking each item
daily to see if any updates ... it might not be looking hard enough for updates or
updating items frequently enough").

They were right, and the measurement is worse than the worry. Phase 3.5 step 2 said:

    Refresh tracked items whose next key date is within 7 days or has passed.
    Bounded work, a handful of fetches at most.

That selects on `key_dates`, and on 2026-08-06 NINE of the seventeen live items had no
future key date at all. Every one of them fell through to the "or has passed" clause,
which nominates all nine at once, against a budget of "a handful", with no priority
order and no record of which ones lost. So whichever items a run happened to notice got
checked and the rest silently aged:

    hb-259-data-center-utility-standards    pending-decision, 19 days unchecked
    ratepayer-protection-pledge             watching,         11 days unchecked

The blind spot is worst exactly where the stakes are highest. adl-422741, STAK Energy's
North Slope lease, is a 50-year lease on 715.4 acres for a campus its developer pegs
above $10 billion. Its comment window closed July 17th and DNR is now weighing a final
best-interest decision. Because that decision has no published date, the item has NO
future key date, so the selector that is supposed to catch breaking changes is
structurally least able to see the item most likely to break. An awaiting-an-unscheduled-
decision item is not a quiet item. It is the loudest one.

WHAT THIS DOES. It replaces "a handful, whichever ones you notice" with a deterministic,
ranked, reasoned worklist:

  - every live item carries a MAX AGE by status (see SLA), so a live item cannot age out
    of attention just because nobody scheduled its next event
  - an item whose events have all passed while its status is still live is scored as
    AWAITING AN UNSCHEDULED EVENT, the STAK case, and is treated as urgent rather than
    invisible
  - the worklist is ranked and capped by --budget, and it ALWAYS PRINTS WHAT IT DEFERRED.
    A silent cap reads as "everything is covered" when it is not, which is the whole bug.

STALENESS NEVER FAILS A RUN, and the first draft of this file got that wrong (maintainer,
2026-08-06: "huh? fail? the routine is to update items if they are not updated, not fail
the run"). A stale item is an INSTRUCTION TO GO AND LOOK, not a defect in the run that
finds it. Failing on it is backwards twice over: it punishes today's run for yesterday's
omission, and because a failed run does not merge, the docket would end up updated LESS
often the staler it got. That is a loop that runs the wrong way.

So this follows the convention gaswatch_pagecheck.py already sets in this repo: rot exits
2, which a run records and carries on from. Only a genuinely broken CHECK exits 1, which
here means an unreadable or malformed ledger. Nothing this file measures about the docket
can abort a run.

It does not fetch anything and it has no opinion about what a refresh finds. It decides
WHAT TO LOOK AT, which is the part that was being decided by accident.
"""
import argparse
import datetime as dt
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEDGER = os.path.join(REPO, "ledger", "docket.json")

# Maximum days a live item may go without a re-verified primary source.
#
# These are graded by what a stale entry COSTS THE READER, not by how interesting the item
# is. open-for-comment is the tightest because the page is telling somebody they can still
# act, and being wrong about that is the worst thing this tracker can do.
SLA = {
    "open-for-comment": 2,
    "pending-decision": 3,
    "watching": 7,
}
# Terminal states. Still checked, far more slowly, because a decided item can be appealed,
# rescinded or superseded and the page would keep saying "decided" forever.
SLA_TERMINAL = {"decided": 30, "closed": 30, "dead": 60}
LIVE = set(SLA)


def parse_date(s):
    return dt.date.fromisoformat(str(s)[:10])


def assess(item, today):
    status = item.get("status", "unknown")
    sla = SLA.get(status, SLA_TERMINAL.get(status, 14))
    last = item.get("last_updated")
    age = (today - parse_date(last)).days if last else 9999

    dates = sorted(parse_date(k["date"]) for k in (item.get("key_dates") or []))
    future = [d for d in dates if d >= today]
    next_key = future[0] if future else None
    days_to_next = (next_key - today).days if next_key else None

    unscheduled = status in LIVE and not future
    # THE STAK CASE tightens the limit rather than standing on its own as a reason. An
    # item whose next event has no announced date can change on any morning, so it earns
    # a shorter leash. It does NOT earn being listed as due on a day it was just verified:
    # a worklist that names things the run did an hour ago is a worklist the run learns to
    # skim, and then the one real entry goes past with the noise.
    if unscheduled:
        sla = min(sla, 3)

    reasons, urgency = [], 0.0
    if age > sla:
        reasons.append(f"{age}d since last verified, over its {sla}d limit")
        urgency += (age - sla) / max(1.0, sla)
        if unscheduled:
            reasons.append("no scheduled event, so any change arrives unannounced")
            urgency += 2.0
        if status == "open-for-comment":
            reasons.append("the page is telling a reader they can still act")
            urgency += 1.0
    # A near key date is its own trigger, because the day a window closes is the day the
    # page must be right, whatever its last-verified stamp says. Still not on the same day
    # it was checked.
    if days_to_next is not None and days_to_next <= 7 and age >= 1:
        reasons.append(f"key date in {days_to_next}d")
        urgency += 2.5 - (days_to_next * 0.2)

    return {
        "id": item.get("id"), "title": item.get("title", "")[:60], "status": status,
        "age_days": age, "sla_days": sla, "over_sla": age > sla,
        "rotten": age > sla * 2 and status in LIVE,
        "days_to_next_key": days_to_next,
        "no_scheduled_event": unscheduled,
        "urgency": round(urgency, 2), "reasons": reasons,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--today", default=None, help="ISO date; defaults to today")
    ap.add_argument("--budget", type=int, default=6,
                    help="how many items the run will actually re-fetch this pass")
    ap.add_argument("--json", action="store_true", help="emit the worklist as JSON")
    # No --strict, deliberately. See the module docstring: a stale item is work to do,
    # not a reason to stop, and there is no flag that turns that into a failure.
    a = ap.parse_args()

    today = parse_date(a.today) if a.today else dt.date.today()
    items = json.load(open(a.ledger))["items"]
    rows = [assess(i, today) for i in items]
    rows.sort(key=lambda r: (-r["urgency"], -r["age_days"]))

    due = [r for r in rows if r["reasons"]]
    work, deferred = due[:a.budget], due[a.budget:]
    rotten = [r for r in rows if r["rotten"]]

    if a.json:
        print(json.dumps({"today": today.isoformat(), "must_refresh": work,
                          "deferred": deferred, "rotten": rotten}, indent=1))
        return 2 if rotten else 0

    print(f"DOCKET REFRESH WORKLIST for {today}   ({len(items)} tracked, "
          f"{sum(1 for r in rows if r['status'] in LIVE)} live)\n")
    if not work:
        print("  nothing is due. Every item is inside its limit.")
    for n, r in enumerate(work, 1):
        print(f"  {n}. {r['id']}")
        print(f"     {r['status']}, last verified {r['age_days']}d ago "
              f"(limit {r['sla_days']}d)")
        for why in r["reasons"]:
            print(f"     - {why}")

    if deferred:
        # NEVER SILENT. A cap that does not announce itself is indistinguishable from
        # full coverage, and that indistinguishability is the defect this file exists for.
        print(f"\n  DEFERRED past the --budget of {a.budget}, and these are NOT covered "
              f"today:")
        for r in deferred:
            print(f"     {r['id']}  ({r['age_days']}d old, {r['reasons'][0]})")
        print("     Raise --budget or carry them at the top of tomorrow's list.")

    if rotten:
        print(f"\n  ROTTEN, past TWICE the limit while still live:")
        for r in rotten:
            print(f"     {r['id']}  {r['status']}, {r['age_days']}d "
                  f"(limit {r['sla_days']}d)")
        print("     The docket is publishing a status nobody has confirmed in that long.")
        print("     Re-verify these FIRST, before writing anything new. This is work to")
        print("     do, not a reason to stop: exit 2 means attention, and a run records")
        print("     it and carries on.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
