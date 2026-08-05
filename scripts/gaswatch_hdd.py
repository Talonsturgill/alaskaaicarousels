#!/usr/bin/env python3
"""gaswatch_hdd.py, extend the observed Anchorage degree day record.

WHY THIS EXISTS. The demand model refits itself against observed EIA
consumption, and the page says so in as many words: refitted every time another
month is published, more accurate as the record grows. That promise had a floor
nobody had noticed. observations() only yields a month present in BOTH the EIA
ledger AND config/gaswatch_hdd_history.json, and nothing in the repo ever wrote
the second file. It was committed once, ending 2026-08-04, and referenced only
by readers.

So the fit could gain the two months EIA still owed it and then stop forever, at
which point every monthly run would recompute an identical fit, evaluate() would
answer "the fit does not beat the current model", and the model would quietly
stop tracking the record while the page kept claiming otherwise. On a page whose
entire argument is that its accuracy is checked rather than asserted, that is
the worst kind of bug: everything stays green and the claim goes false.

This closes the loop. It runs on the monthly EIA workflow, immediately before
the refit, so a refit always sees every day the weather record can offer.

WHAT IT GUARANTEES. The file's shape is a start date plus one value per day with
no gaps, which is what makes a missing day impossible to represent. So a partial
fetch is refused outright rather than written with a hole, and nothing is
appended unless the run can produce an unbroken chain from the existing
end_date. Same reasoning as the collector: a wrong record is worse than a short
one.

Run:
  python3 scripts/gaswatch_hdd.py --self-test   # hermetic
  python3 scripts/gaswatch_hdd.py --dry-run     # fetch, report, write nothing
  python3 scripts/gaswatch_hdd.py               # extend to yesterday
"""

import argparse
import json
import os
import sys
import traceback
from datetime import date, datetime, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gaswatch_collect as gc  # noqa: E402

HISTORY = os.path.join(REPO, "config", "gaswatch_hdd_history.json")

# ACIS returns M for missing and T for trace. A degree day cannot be a trace, so
# anything that is not a number is treated as absent and stops the append there.
MISSING = ("M", "T", "", None)


def parse_range(payload):
    """[(iso date, hdd)] from an ACIS StnData range response, missing dropped."""
    out = []
    for row in json.loads(payload).get("data", []):
        if len(row) < 2 or row[1] in MISSING:
            continue
        try:
            out.append((row[0], float(row[1])))
        except (TypeError, ValueError):
            continue
    return out


def contiguous_from(rows, first_needed):
    """The unbroken run starting exactly at first_needed, and nothing after a gap.

    The history file cannot represent a hole, so a gap is not something to
    tolerate and skip past. Everything up to the gap is usable and everything
    beyond it waits for a run that can fill it.
    """
    by_date = dict(rows)
    out, cur = [], date.fromisoformat(first_needed)
    while cur.isoformat() in by_date:
        out.append((cur.isoformat(), by_date[cur.isoformat()]))
        cur += timedelta(days=1)
    return out


def whole_days(vals):
    """Degree days are whole in this record. Keep them that way.

    load_hdd_history floats them on read, and every figure recomputed from them
    rounds at the end, so storing 23.0 instead of 23 would only put a float in
    a committed file and eventually on a page.
    """
    return [int(v) if float(v).is_integer() else v for v in vals]


def fetch(start, end, base_f):
    probe = gc.Probe("acis_panc_hdd_range", gc.ACIS_URL, method="POST")
    body = json.dumps({
        "sid": "PANC", "sdate": start, "edate": end,
        "elems": [{"name": "hdd", "interval": "dly", "base": base_f}],
    }).encode("utf-8")
    return parse_range(gc.http(probe, data=body,
                               headers={"Content-Type": "application/json"})), probe


def extend(hist, rows):
    """Return (updated history, appended count). Never leaves a gap behind."""
    first_needed = (date.fromisoformat(hist["end_date"]) + timedelta(days=1)).isoformat()
    run = contiguous_from(rows, first_needed)
    if not run:
        return hist, 0
    out = json.loads(json.dumps(hist))
    out["daily"] = list(out["daily"]) + whole_days(v for _, v in run)
    out["end_date"] = run[-1][0]
    out["days"] = len(out["daily"])
    out["fetched_utc"] = date.today().isoformat()
    return out, len(run)


def main():
    ap = argparse.ArgumentParser(description="Extend the observed HDD record")
    ap.add_argument("--history", default=HISTORY)
    ap.add_argument("--through", help="last date to fetch, default yesterday")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    with open(args.history, encoding="utf-8") as fh:
        hist = json.load(fh)
    start = (date.fromisoformat(hist["end_date"]) + timedelta(days=1)).isoformat()
    # Yesterday. ACIS publishes a day after it closes, so asking for today
    # returns M and the run would report a gap that is only the clock.
    through = args.through or (date.today() - timedelta(days=1)).isoformat()
    if start > through:
        print(f"Record already runs to {hist['end_date']}, nothing to add.")
        return 0

    rows, probe = fetch(start, through, hist["base_f"])
    if probe.status != "ok":
        print(f"ACIS fetch failed, {probe.error}. Record left alone.")
        return 1

    new, added = extend(hist, rows)
    if not added:
        print(f"ACIS returned nothing usable from {start}. Record left alone.")
        return 0
    gap = "" if added == len(rows) else (
        f"  {len(rows) - added} later day(s) held back behind a gap")
    print(f"Extending {hist['end_date']} to {new['end_date']}, {added} day(s)"
          f"{gap}")
    if args.dry_run:
        return 0
    with open(args.history, "w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=2)
        fh.write("\n")
    # The loader is the authority on whether the file is coherent, so it is
    # what confirms the write rather than a check written twice.
    model = gc.load_model(gc.MODEL_CONFIG)
    checked, _ = gc.load_hdd_history(model, REPO)
    print(f"Written. Loader agrees, {checked['days']} days to {checked['end_date']}.")
    return 0


# ------------------------------------------------------------------ self test

def self_test():
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    print("the ACIS range parser")
    payload = json.dumps({"data": [["2026-08-05", "12"], ["2026-08-06", "M"],
                                   ["2026-08-07", "9"], ["2026-08-08", "0"]]})
    rows = parse_range(payload)
    check("missing days are dropped, zero is kept",
          rows == [("2026-08-05", 12.0), ("2026-08-07", 9.0), ("2026-08-08", 0.0)],
          str(rows))
    check("a trace reading is not treated as a number",
          parse_range(json.dumps({"data": [["2026-08-05", "T"]]})) == [])

    print("a gap stops the append rather than being skipped")
    base = {"start_date": "2026-08-01", "end_date": "2026-08-04",
            "days": 4, "daily": [10, 11, 12, 13], "base_f": 65}
    new, added = extend(base, rows)
    check("only the unbroken run is appended", added == 1 and new["days"] == 5,
          f"{added} added, ends {new['end_date']}")
    check("the day after the gap is held back", new["end_date"] == "2026-08-05")
    check("the original is not mutated", base["days"] == 4)

    full = parse_range(json.dumps({"data": [["2026-08-05", "12"], ["2026-08-06", "8"],
                                            ["2026-08-07", "9"]]}))
    new, added = extend(base, full)
    check("a clean run appends whole", added == 3 and new["end_date"] == "2026-08-07",
          f"{added} added")
    check("degree days stay whole numbers",
          all(isinstance(v, int) for v in new["daily"]), str(new["daily"]))

    print("nothing is appended when there is nothing to append")
    _, added = extend(base, [("2026-08-09", 4.0)])
    check("a run that does not start at the next day is refused", added == 0)
    _, added = extend(base, [])
    check("an empty fetch is refused", added == 0)

    print("the committed record still loads")
    model = gc.load_model(gc.MODEL_CONFIG)
    hist, series = gc.load_hdd_history(model, REPO)
    check("the loader accepts the record on disk",
          len(series) == hist["days"],
          f"{hist['days']} days to {hist['end_date']}")
    # The whole point of this script, asserted rather than assumed.
    with open(HISTORY, encoding="utf-8") as fh:
        on_disk = json.load(fh)
    grown, added = extend(on_disk, [
        ((date.fromisoformat(on_disk["end_date"]) + timedelta(days=1)).isoformat(), 7.0)])
    check("the committed record can still be extended",
          added == 1 and grown["days"] == on_disk["days"] + 1,
          f"{on_disk['days']} to {grown['days']}")

    print()
    if not ok[0]:
        print("self-test FAILED")
        return 1
    print("self-test clean")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
