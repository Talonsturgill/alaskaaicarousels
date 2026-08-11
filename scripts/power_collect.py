#!/usr/bin/env python3
"""What Alaskans pay for electricity, from EIA, monthly, back to 2001.

WHY THIS EXISTS. "Is my power bill going up" is the question an ordinary
Alaskan brings to a site about data centres and the grid, and this record had
no answer to it at all. The body that would know is the Regulatory Commission
of Alaska, and rca.alaska.gov sits behind a bot wall that answers 403, so the
obvious route is shut.

EIA is the way around it. The bulk electricity file is keyless, it carries
Alaska retail price and sales by sector monthly, and it goes back to January
2001, which is long enough that a reader can see whether this year is unusual
rather than being told it is.

WHAT THIS PUBLISHES AND WHAT IT REFUSES TO. Measured average retail price, the
sales volume behind it, and the change against a year ago. Nothing else.

  It does not forecast. There is no next month on this page, in either
  direction, for the same reason the gas watch publishes no shortfall call. A
  rate case can move a number more than a decade of trend, and a published
  prediction would be a credibility loss the data cannot carry.

  It does not attribute. The price went up is a measurement. The price went up
  BECAUSE of data centres is a claim, and this file cannot support it, because
  EIA does not break out who used the power or why the rate moved. The docket
  tracks the decisions; this tracks the number; joining them is a reader's
  judgement and an editor's job, not a collector's.

  It is a STATE average. Alaska is not one grid and a Railbelt customer and a
  village on diesel are not on the same tariff. The page says so, because an
  average presented as a bill is a wrong answer to the question actually asked.

A failed fetch writes nothing and says so, the same rule the gas watch follows.
"""

import argparse
import io
import json
import os
import sys
import urllib.request
import zipfile
from datetime import date, datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "ledger", "power.json")

UA = "AlaskaAI-PowerWatch/1.0 (+https://alaskaaihq.com; docket@alaskaaihq.com)"
BULK = "https://api.eia.gov/bulk/ELEC.zip"
TIMEOUT = 180

# Sector by sector, because "my bill" is the residential number and the
# commercial and industrial ones are what a data centre would actually pay.
# Publishing all three is what lets a reader see the gap themselves.
SERIES = {
    "residential": "ELEC.PRICE.AK-RES.M",
    "commercial": "ELEC.PRICE.AK-COM.M",
    "industrial": "ELEC.PRICE.AK-IND.M",
    "all": "ELEC.PRICE.AK-ALL.M",
}
SALES = {"residential": "ELEC.SALES.AK-RES.M", "all": "ELEC.SALES.AK-ALL.M"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def fetch_bulk(url=BULK):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def parse(raw, wanted):
    """Pull only the series asked for out of a 292 MB archive.

    Streamed line by line and filtered on a substring before any JSON parsing,
    because decoding the whole file to find twenty thousand characters of it
    would cost a minute and a gigabyte for nothing.
    """
    found = {}
    z = zipfile.ZipFile(io.BytesIO(raw))
    name = z.namelist()[0]
    with z.open(name) as f:
        for line in io.TextIOWrapper(f, encoding="utf-8", errors="replace"):
            if '"ELEC.PRICE.AK' not in line and '"ELEC.SALES.AK' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            sid = d.get("series_id")
            if sid in wanted:
                found[sid] = d
            if len(found) == len(wanted):
                break
    return found


def ym(period):
    """202605 becomes May 2026, which is how a person says it."""
    return f"{MONTHS[int(period[4:6]) - 1]} {period[:4]}"


def build(raw):
    wanted = set(SERIES.values()) | set(SALES.values())
    found = parse(raw, wanted)
    missing = sorted(wanted - set(found))
    if missing:
        raise LookupError(f"EIA no longer carries {missing}")

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "US Energy Information Administration, bulk electricity file",
        "source_url": BULK,
        "geography": "Alaska, all utilities, state average",
        "units": "cents per kilowatthour",
        "sectors": {},
    }
    for label, sid in SERIES.items():
        d = found[sid]
        # EIA hands these back newest first. Kept that way, because every
        # reader of this file wants the latest month and none of them want to
        # scan to the end for it.
        pts = [[p, v] for p, v in d["data"] if v is not None]
        latest_p, latest_v = pts[0]
        year_ago = next((v for p, v in pts if p == str(int(latest_p) - 100)), None)
        out["sectors"][label] = {
            "series_id": sid,
            "eia_updated": (d.get("last_updated") or "")[:10],
            "latest_period": latest_p,
            "latest_label": ym(latest_p),
            "latest": latest_v,
            "year_ago": year_ago,
            # Stated as a change, never as a trend and never as a projection.
            "change_year": (round(latest_v - year_ago, 2)
                            if year_ago is not None else None),
            "points": len(pts),
            "first_period": pts[-1][0],
            "data": pts,
        }
    for label, sid in SALES.items():
        d = found[sid]
        pts = [[p, v] for p, v in d["data"] if v is not None]
        out.setdefault("sales", {})[label] = {
            "series_id": sid, "units": d.get("units", ""),
            "latest_period": pts[0][0], "latest": pts[0][1], "data": pts,
        }
    return out


# --------------------------------------------------------------- self test

def _fixture():
    """A tiny archive shaped exactly like EIA's, so the parser is tested on
    the format rather than on a dictionary someone typed."""
    lines = []
    for sid in list(SERIES.values()) + list(SALES.values()):
        lines.append(json.dumps({
            "series_id": sid, "name": sid, "units": "cents per kilowatthour",
            "last_updated": "2026-07-22T10:00:00-04:00",
            "data": [["202605", 28.23], ["202604", 27.35], ["202512", 25.54],
                     ["202505", 26.10], ["200101", 11.5]],
        }))
    lines.append(json.dumps({"series_id": "ELEC.PRICE.TX-RES.M", "data": [["202605", 1]]}))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("ELEC.txt", "\n".join(lines))
    return buf.getvalue()


def self_test():
    print("what Alaskans pay for power")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    out = build(_fixture())
    print("it reads the format EIA actually publishes")
    check("every sector asked for came back",
          set(out["sectors"]) == set(SERIES), str(sorted(out["sectors"])))
    res = out["sectors"]["residential"]
    check("the latest month is the newest one", res["latest_period"] == "202605",
          res["latest_period"])
    check("said the way a person says it", res["latest_label"] == "May 2026",
          res["latest_label"])
    check("the year-ago comparison is the same month last year",
          res["year_ago"] == 26.10, str(res["year_ago"]))
    check("the change is stated, not projected",
          res["change_year"] == round(28.23 - 26.10, 2), str(res["change_year"]))
    check("another state's series is not mistaken for ours",
          all("AK" in s["series_id"] for s in out["sectors"].values()))
    check("sales volume comes with it", "sales" in out and out["sales"]["all"]["latest"])

    print("it publishes a measurement and refuses everything else")
    src = open(os.path.abspath(__file__)).read()
    body = src.split("def self_test", 1)[0]
    blob = json.dumps(out).lower()
    for word in ("forecast", "predict", "expected", "will rise", "will fall",
                 "projection", "outlook"):
        check(f"nothing in the output claims to {word}", word not in blob)
    check("no field names a cause", not any(
        k in blob for k in ("because", "caused", "driven by", "due to")))
    # The state average is the honest shape of this number and the file has to
    # say so, or a reader in Bethel reads a Railbelt figure as their bill.
    check("the geography is stated on the record",
          "state average" in out["geography"].lower(), out["geography"])

    print("a bad day writes nothing")
    try:
        build(b"not a zip")
        check("a corrupt archive raises rather than publishing", False)
    except Exception:
        check("a corrupt archive raises rather than publishing", True)
    short = io.BytesIO()
    with zipfile.ZipFile(short, "w") as z:
        z.writestr("ELEC.txt", json.dumps(
            {"series_id": "ELEC.PRICE.AK-RES.M", "data": [["202605", 1]]}))
    try:
        build(short.getvalue())
        check("a series EIA dropped is a failure, not a gap", False)
    except LookupError as e:
        check("a series EIA dropped is a failure, not a gap", True, str(e)[:60])

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    try:
        raw = fetch_bulk()
    except Exception as e:
        print(f"FAILED to fetch the EIA bulk file: {e}", file=sys.stderr)
        print("nothing written; yesterday's file is left exactly as it was",
              file=sys.stderr)
        return 1
    out = build(raw)
    if args.write:
        with open(OUT, "w") as f:
            json.dump(out, f, indent=1)
            f.write("\n")
        print(f"wrote {OUT}  ({os.path.getsize(OUT) // 1024} KB)")
    for label in ("residential", "commercial", "industrial"):
        s = out["sectors"][label]
        ch = s["change_year"]
        move = ("level with a year ago" if not ch else
                f"{'up' if ch > 0 else 'down'} {abs(ch)} cents from a year ago")
        print(f"  {label:<12} {s['latest']:>6} cents/kWh  {s['latest_label']:<14}{move}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
