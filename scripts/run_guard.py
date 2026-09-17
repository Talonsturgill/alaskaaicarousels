#!/usr/bin/env python3
"""Phase 0 guard: has this date's carousel already shipped?

The trigger fires daily, but a firing is not always a new day. On 2026-09-17
the schedule delivered its stored prompt a second time, minutes after the first
run had merged to main and created its Gmail draft, because the first firing
was interrupted mid wrap. The prompt says "execute it end to end, beginning at
Phase 0", and Phase 0 had nothing that could tell a fresh day from a re-fire.
Obeying it literally would have produced a second deck dated 2026-09-17: a
second entry in topics.json for one day, a collision on runs/2026-09-17, and a
second draft in a mailbox whose whole job is to hold one postable deck per day.

A duplicate is not the same failure as an empty run and must not be confused
with one. NO EMPTY RUNS is about a day with no deck. This is a day that already
HAS its deck, and the honest move is to finish the outstanding work rather than
draw the same day twice.

Exit codes are distinct on purpose, so a run can branch on them:
  0  nothing shipped for this date. Proceed with Phase 0.
  3  this date already shipped. Do NOT start a new deck.
  1  the evidence disagrees with itself. A human should look.

Usage:
  python3 scripts/run_guard.py                       (today, UTC)
  python3 scripts/run_guard.py --run-date 2026-09-17
  python3 scripts/run_guard.py --json
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def evidence(run_date):
    """Three independent records of a shipped run. They should agree."""
    ev = {"run_date": run_date}

    state_path = REPO / "runs" / run_date / "run_state.json"
    state = {}
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text())
        except json.JSONDecodeError:
            state = {"status": "unreadable"}
    ev["run_state_status"] = state.get("status")
    ev["gmail_draft_id"] = state.get("gmail_draft_id")
    ev["merged_to_main"] = state.get("merged_to_main")
    ev["shipped_artifacts"] = (
        sorted(p.name for p in (REPO / "runs" / run_date).glob("slide-*.webp"))
        if (REPO / "runs" / run_date).is_dir() else [])

    topics_path = REPO / "ledger" / "topics.json"
    entries = []
    if topics_path.is_file():
        raw = json.loads(topics_path.read_text())
        entries = raw if isinstance(raw, list) else raw.get(
            "topics", raw.get("entries", []))
    ev["topics_entries"] = len(entries)
    ev["next_carousel_no"] = len(entries) + 1

    return ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-date",
                    default=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    ev = evidence(args.run_date)
    complete = ev["run_state_status"] == "complete"
    n_slides = len(ev["shipped_artifacts"])

    # The slides under runs/ are the primary evidence, because runs/ IS the
    # shipped location and a deck only lands there at Phase 11. status and
    # gmail_draft_id corroborate, but they are recent fields: runs before
    # 2026-09-17 carry neither, so requiring them would report every historical
    # date as half-finished. The floor is 5 because the degradation ladder's
    # reduced deck never goes below 5 slides.
    if n_slides >= 5:
        verdict, code = "ALREADY_SHIPPED", 3
    elif n_slides == 0 and not complete:
        verdict, code = "CLEAR", 0
    else:
        verdict, code = "PARTIAL", 1

    ev["verdict"] = verdict
    if args.json:
        print(json.dumps(ev, indent=2))
    else:
        print(f"run_guard: {args.run_date} -> {verdict}")
        print(f"  run_state status   {ev['run_state_status']}")
        print(f"  shipped slides     {len(ev['shipped_artifacts'])}")
        print(f"  gmail draft        {ev['gmail_draft_id']}")
        print(f"  merged to main     {str(ev['merged_to_main'])[:8] or None}")
        print(f"  topics entries     {ev['topics_entries']}"
              f" (next No. {ev['next_carousel_no']})")
        if verdict == "ALREADY_SHIPPED":
            print("  DO NOT start a new deck for this date. This firing is a "
                  "re-fire, not a new day. Finish any outstanding work "
                  "(open PRs, gas watch, docket) and stop.")
        elif verdict == "PARTIAL":
            print("  Evidence disagrees. Some of the run landed and some did "
                  "not. Resume the unfinished phases; do not start over.")
    sys.exit(code)


if __name__ == "__main__":
    main()
