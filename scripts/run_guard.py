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

THE ANCHORAGE DATE IS PRINTED BESIDE IT (2026-11-08, weekly pass). The
routine's run date is the America/Anchorage date, and the trigger wakes at
about 06:05Z, which is the previous evening in Anchorage all winter. So the UTC
default named tomorrow on every November run, and a re-fire of a deck that had
just shipped would have read CLEAR for tomorrow. With no --run-date this now
also reads the Anchorage date when the two differ and prints its verdict and
the command to run, and --json carries utc_date, anchorage_date and
anchorage_verdict. The default and the exit code are unchanged: which date
governs a late wake against a re-fire is the owner's call
(knowledge/MACHINE_QUEUE.md, escalated 2026-10-25).

Usage:
  python3 scripts/run_guard.py                       (today, UTC; Anchorage's printed too)
  python3 scripts/run_guard.py --run-date 2026-09-17
  python3 scripts/run_guard.py --json
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:          # pragma: no cover, py < 3.9
    ZoneInfo = None

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


def verdict_of(ev):
    """(verdict, exit code) from one date's evidence."""
    complete = ev["run_state_status"] == "complete"
    n_slides = len(ev["shipped_artifacts"])
    if n_slides >= 5:
        return "ALREADY_SHIPPED", 3
    if n_slides == 0 and not complete:
        return "CLEAR", 0
    return "PARTIAL", 1


def anchorage_today(now=None):
    """The America/Anchorage calendar date, or None without a tz database."""
    if ZoneInfo is None:
        return None
    try:
        now = now or dt.datetime.now(dt.timezone.utc)
        return now.astimezone(ZoneInfo("America/Anchorage")).strftime("%Y-%m-%d")
    except Exception:
        return None


def main(argv=None, now=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-date", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    now = now or dt.datetime.now(dt.timezone.utc)
    defaulted = args.run_date is None
    if defaulted:
        args.run_date = now.strftime("%Y-%m-%d")

    ev = evidence(args.run_date)
    ak = anchorage_today(now) if defaulted else None
    if ak and ak != args.run_date:
        ev["utc_date"] = args.run_date
        ev["anchorage_date"] = ak
        ev["anchorage_verdict"] = verdict_of(evidence(ak))[0]

    # The slides under runs/ are the primary evidence, because runs/ IS the
    # shipped location and a deck only lands there at Phase 11. status and
    # gmail_draft_id corroborate, but they are recent fields: runs before
    # 2026-09-17 carry neither, so requiring them would report every historical
    # date as half-finished. The floor is 5 because the degradation ladder's
    # reduced deck never goes below 5 slides.
    verdict, code = verdict_of(ev)

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
        if ev.get("anchorage_date"):
            print(f"  NOTE: that is the UTC date. Anchorage is on "
                  f"{ev['anchorage_date']}, which reads "
                  f"{ev['anchorage_verdict']}; the routine's run date is the "
                  f"Anchorage date (taking the next free date only when it is "
                  f"taken). Run: python3 scripts/run_guard.py --run-date "
                  f"{ev['anchorage_date']}")
            if ev["anchorage_verdict"] != "CLEAR":
                print(f"  The Anchorage date already holds a deck. If it "
                      f"shipped tonight this firing is a RE-FIRE of it, not a "
                      f"new day; read runs/{ev['anchorage_date']}/run_state.json "
                      f"before starting anything.")
    sys.exit(code)


if __name__ == "__main__":
    main()
