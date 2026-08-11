#!/usr/bin/env python3
"""What each Alaska utility charges, from Form EIA-861, annually.

WHY THIS EXISTS. power_collect.py answers "is my power bill going up" with a
state average, and a state average is the wrong shape for the question. Alaska
is not one grid. A Chugach customer in Anchorage and a village on the Alaska
Village Electric Coop system are both inside that one number and it is nobody's
bill. The page said so honestly and then had nothing better to offer, which is
a caveat standing in for an answer.

This is the better answer. Form EIA-861 carries retail revenue, sales and
customer counts PER UTILITY, and the companion service territory file says
which boroughs each one serves, so both the price and the place come out of the
record rather than out of anyone's head. Divide revenue by sales and you have
what that utility's residential customers actually paid, on average, across the
year.

WHAT IT COSTS TO GET THAT. Time. The bulk file behind the state series is
monthly and current to within about two months. This one is ANNUAL, and the
newest year EIA has published is usually the one before last. That trade is
worth making and it is not worth hiding, so the data year is a field, the page
prints it beside every figure, and the two numbers are never blended.

WHAT THIS PUBLISHES AND WHAT IT REFUSES TO. Revenue divided by sales, as filed,
per utility, per sector. Nothing else.

  It is not a tariff and it is not a bill. It is a year of revenue over a year
  of sales, so it carries whatever mix of rate classes, seasons, fuel surcharges
  and Power Cost Equalization credits that utility actually billed. A customer
  looking up their own rate should read their own bill.

  It does not forecast and it does not attribute, which are power_collect.py's
  rules and not this file's to relax. A price is a measurement. A price BECAUSE
  of anything is a claim, and Form EIA-861 does not carry causes.

  It shows the long form filers only. Alaska's smallest utilities file a short
  form that reports one revenue figure across all sectors, and a household rate
  and an all customers rate are different measurements. Publishing them in one
  column would be a made-up number wearing a real one's clothes. The count left
  out is published instead, so the gap is stated rather than implied.

A failed fetch writes nothing and says so, the same rule every collector here
follows.
"""

import argparse
import io
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import date, datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "ledger", "power_utility.json")

UA = "AlaskaAI-PowerWatch/1.0 (+https://alaskaaihq.com; docket@alaskaaihq.com)"
BULK = "https://www.eia.gov/electricity/data/eia861/zip/f861{year}.zip"
TIMEOUT = 180
STATE = "AK"

# EIA answers a missing year with 200 and a small HTML page rather than a 404,
# so "did it download" is not the question. "Is it a zip" is.
MIN_ARCHIVE = 500_000

# Balancing rows EIA inserts to reconcile state totals. They carry a price and
# they are not a utility anybody buys power from.
NOT_A_UTILITY = re.compile(r"^\s*adjustment\b", re.I)

# Column letters in Sales_Ult_Cust. Revenue in thousand dollars, sales in
# megawatthours, customers a count, three columns per sector in that order.
SECTORS = {"residential": "JKL", "commercial": "MNO", "industrial": "PQR"}

XL = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


# ------------------------------------------------------------------ xlsx

def sheet_rows(xlsx_bytes):
    """Rows of an xlsx as {column letter: text}, using the standard library.

    openpyxl would be one line and one more dependency, and every collector in
    this repo runs on a bare Python so that a workflow cannot fail on an
    install. An xlsx is a zip of XML and the part needed here is small.
    """
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")):
            shared.append("".join(t.text or "" for t in si.iter(XL + "t")))
    names = sorted(n for n in z.namelist()
                   if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))
    if not names:
        raise LookupError("workbook carries no worksheet")
    out = []
    for row in ET.fromstring(z.read(names[0])).iter(XL + "row"):
        cells = {}
        for c in row.iter(XL + "c"):
            col = re.match(r"([A-Z]+)", c.get("r") or "A").group(1)
            kind, v = c.get("t"), c.find(XL + "v")
            if kind == "s" and v is not None:
                cells[col] = shared[int(v.text)]
            elif kind == "inlineStr":
                cells[col] = "".join(x.text or "" for x in c.iter(XL + "t"))
            elif v is not None:
                cells[col] = v.text
        out.append(cells)
    return out


def num(x):
    """A figure, or None. EIA writes a withheld cell as a full stop."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ fetch

def fetch(year):
    req = urllib.request.Request(BULK.format(year=year), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read()
    if len(raw) < MIN_ARCHIVE or not raw.startswith(b"PK"):
        raise LookupError(f"EIA has not published {year} yet")
    return raw


def newest(today=None, back=4):
    """The most recent published year, found by asking rather than by assuming.

    EIA-861 for a year lands the following autumn, so the newest year is
    sometimes last year and sometimes the year before, depending on the month.
    Hard coding either one means this file silently serves stale data for
    months, so it walks back from last year until an archive answers.
    """
    today = today or date.today()
    tried = []
    for year in range(today.year - 1, today.year - 1 - back, -1):
        try:
            return year, fetch(year)
        except Exception as exc:
            tried.append(f"{year} ({exc.__class__.__name__})")
    raise LookupError("no EIA-861 archive answered for " + ", ".join(tried))


# ------------------------------------------------------------------ build

def territories(raw, state=STATE):
    """Utility name to the boroughs it serves, straight out of EIA's file.

    The alternative was writing down that Chugach serves Anchorage, which is
    true and which is still an assertion this record would be carrying without
    a source. EIA publishes it, so it is data.
    """
    out = {}
    for r in sheet_rows(raw):
        if r.get("E") != state:
            continue
        area = (r.get("F") or "").strip()
        if not area or area == "Not Applicable":
            continue
        out.setdefault((r.get("C") or "").strip(), []).append(area)
    return {k: sorted(set(v)) for k, v in out.items()}


def build(archive, year):
    z = zipfile.ZipFile(io.BytesIO(archive))
    need = [f"Sales_Ult_Cust_{year}.xlsx", f"Service_Territory_{year}.xlsx",
            f"Short_Form_{year}.xlsx"]
    missing = [n for n in need if n not in z.namelist()]
    if missing:
        raise LookupError(f"EIA no longer packs {missing}")
    areas = territories(z.read(need[1]))

    utilities = []
    for r in sheet_rows(z.read(need[0])):
        if r.get("G") != STATE or r.get("D") != "A":
            continue
        name = (r.get("C") or "").strip()
        if not name or NOT_A_UTILITY.match(name):
            continue
        row = {"name": name, "utility_id": r.get("B"),
               "ownership": (r.get("H") or "").strip(),
               "areas": areas.get(name, []), "sectors": {}}
        for label, cols in SECTORS.items():
            rev, sales, cust = (num(r.get(c)) for c in cols)
            if not rev or not sales:
                continue
            # Thousand dollars over megawatthours is already cents per
            # kilowatthour. Both factors of a thousand cancel and the hundred
            # turns dollars into cents.
            row["sectors"][label] = {
                "cents_per_kwh": round(rev * 100 / sales, 2),
                "customers": int(cust) if cust else None,
                "megawatthours": int(sales),
            }
        if row["sectors"]:
            utilities.append(row)
    if not utilities:
        raise LookupError(f"no {STATE} utilities in Sales_Ult_Cust_{year}")

    # Biggest first, by households served, because a reader looking for their
    # own utility is most likely to be with one of the large ones and a reader
    # looking for the spread wants both ends visible without sorting anything.
    utilities.sort(key=lambda u: -(u["sectors"].get("residential", {}).get(
        "customers") or 0))

    short = [r for r in sheet_rows(z.read(need[2]))
             if r.get("E") == STATE and not NOT_A_UTILITY.match(
                 (r.get("C") or "").strip())]
    res = [u for u in utilities if "residential" in u["sectors"]]
    prices = [u["sectors"]["residential"]["cents_per_kwh"] for u in res]
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "US Energy Information Administration, Form EIA-861",
        "source_url": BULK.format(year=year),
        "data_year": year,
        "geography": "Alaska, one row per utility, boroughs served as filed",
        "units": "cents per kilowatthour",
        "basis": ("retail revenue divided by retail sales for the year, as "
                  "filed. An average of what was billed, not a tariff"),
        "utilities": utilities,
        "residential_low": min(prices) if prices else None,
        "residential_high": max(prices) if prices else None,
        "not_shown": {
            "short_form_filers": len(short),
            "why": ("Alaska's smallest utilities file a short form that reports "
                    "one revenue figure across all sectors. A household rate "
                    "and an all customers rate are different measurements and "
                    "this record does not put them in one column."),
        },
    }


# --------------------------------------------------------------- self test

def _fixture(year=2024):
    """An archive shaped exactly like EIA's, so the parser is tested on the
    format rather than on a dictionary someone typed."""
    def book(header, body):
        strings, index = [], {}

        def sid(s):
            if s not in index:
                index[s] = len(strings)
                strings.append(s)
            return index[s]

        xml = ['<?xml version="1.0"?><worksheetData xmlns="' + XL[1:-1] + '">',
               "<sheetData>"]
        for n, row in enumerate([header] + body, 1):
            cells = []
            for col, val in zip("ABCDEFGHIJKLMNOPQRSTUVWX", row):
                if val is None or val == "":
                    continue
                cells.append(f'<c r="{col}{n}" t="s"><v>{sid(str(val))}</v></c>')
            xml.append(f'<row r="{n}">{"".join(cells)}</row>')
        xml.append("</sheetData></worksheetData>")
        ss = ('<?xml version="1.0"?><sst xmlns="' + XL[1:-1] + '">'
              + "".join(f"<si><t>{s}</t></si>" for s in strings) + "</sst>")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("xl/worksheets/sheet1.xml", "\n".join(xml))
            z.writestr("xl/sharedStrings.xml", ss)
        return buf.getvalue()

    sales = book(
        ["Data Year", "Utility Number", "Utility Name", "Part", "Service Type",
         "Data Type", "State", "Ownership", "BA Code"] + ["Revenues", "Sales",
         "Customers"] * 5,
        [[year, "55", "Chugach Electric Assn Inc", "A", "Bundled", "O", "AK",
          "Cooperative", "CEA", "125500", "590921", "97048",
          "62000", "367000", "12000", "9000", "63000", "40"],
         [year, "12345", "Matanuska Electric Assn Inc", "A", "Bundled", "O",
          "AK", "Cooperative", "CEA", "109100", "466931", "64205",
          "50000", "247000", "9000", "", "", ""],
         # A balancing row, which is not a utility and must not be published.
         [year, "99999", "Adjustment 2024", "A", "Bundled", "O", "AK", "", "",
          "54800", "178666", "25316", "1", "1", "1"],
         # Another state, and a non Part A row. Neither is ours.
         [year, "77", "Some Texas Co", "A", "Bundled", "O", "TX", "Municipal",
          "ERCO", "1000", "10000", "500", "", "", ""],
         [year, "55", "Chugach Electric Assn Inc", "B", "Delivery", "O", "AK",
          "Cooperative", "CEA", "999999", "1", "1", "", "", ""]])
    terr = book(["Data Year", "Utility Number", "Utility Name", "Short Form",
                 "State", "County"],
                [[year, "55", "Chugach Electric Assn Inc", "N", "AK", "Anchorage"],
                 [year, "55", "Chugach Electric Assn Inc", "N", "AK",
                  "Kenai Peninsula"],
                 [year, "12345", "Matanuska Electric Assn Inc", "N", "AK",
                  "Matanuska Susitna"],
                 [year, "12345", "Matanuska Electric Assn Inc", "N", "AK",
                  "Not Applicable"],
                 [year, "77", "Some Texas Co", "N", "TX", "Travis"]])
    short = book(["Data Year", "Utility Number", "Utility Name", "Ownership",
                  "State", "BA Code", "Total Revenue (Thousand Dollars)",
                  "Total Sales (MWh)", "Total Customers"],
                 [[year, "192", "Akiachak Native Community Electric",
                   "Cooperative", "AK", "NA", "1269.4", "1976", "254"],
                  [year, "878", "Atmautluak Tribal Utilities", "Municipal",
                   "AK", "NA", "618.4", "937", "104"]])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"Sales_Ult_Cust_{year}.xlsx", sales)
        z.writestr(f"Service_Territory_{year}.xlsx", terr)
        z.writestr(f"Short_Form_{year}.xlsx", short)
    return buf.getvalue()


def self_test():
    print("what each Alaska utility charges")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    out = build(_fixture(), 2024)
    ut = {u["name"]: u for u in out["utilities"]}

    print("it reads the format EIA actually publishes")
    check("only Alaska utilities came back", set(ut) == {
        "Chugach Electric Assn Inc", "Matanuska Electric Assn Inc"},
        str(sorted(ut)))
    ch = ut["Chugach Electric Assn Inc"]["sectors"]["residential"]
    # 125500 thousand dollars over 590921 MWh is 21.24 cents per kWh.
    check("revenue over sales is cents per kilowatthour",
          ch["cents_per_kwh"] == 21.24, str(ch["cents_per_kwh"]))
    check("the customer count comes with it", ch["customers"] == 97048)
    check("a sector nobody filed is absent rather than zero",
          "industrial" not in ut["Matanuska Electric Assn Inc"]["sectors"],
          str(sorted(ut["Matanuska Electric Assn Inc"]["sectors"])))

    print("the place a utility serves is read, never assumed")
    check("boroughs come from EIA's own file",
          ut["Chugach Electric Assn Inc"]["areas"] == ["Anchorage",
                                                       "Kenai Peninsula"],
          str(ut["Chugach Electric Assn Inc"]["areas"]))
    check("'Not Applicable' is not a place",
          ut["Matanuska Electric Assn Inc"]["areas"] == ["Matanuska Susitna"],
          str(ut["Matanuska Electric Assn Inc"]["areas"]))

    print("what is not a utility does not get published as one")
    check("EIA's balancing row is dropped",
          not any("Adjustment" in n for n in ut), str(sorted(ut)))
    check("another state's utility is not mistaken for ours",
          "Some Texas Co" not in ut)
    check("a delivery only row cannot outrank the bundled one",
          ch["cents_per_kwh"] == 21.24)

    print("the biggest utilities lead, so a reader finds their own")
    check("sorted by households served",
          [u["name"] for u in out["utilities"]][0] == "Chugach Electric Assn Inc")
    check("the spread is stated on the record",
          out["residential_low"] == 21.24 and out["residential_high"] == 23.37,
          f"{out['residential_low']} to {out['residential_high']}")

    print("the gap is published rather than implied")
    check("short form filers are counted, not silently dropped",
          out["not_shown"]["short_form_filers"] == 2,
          str(out["not_shown"]["short_form_filers"]))
    check("and the reason is on the record",
          "different measurements" in out["not_shown"]["why"])

    print("it publishes a measurement and refuses everything else")
    blob = json.dumps(out).lower()
    for word in ("forecast", "predict", "expected", "will rise", "will fall",
                 "projection", "outlook"):
        check(f"nothing in the output claims to {word}", word not in blob)
    check("no field names a cause", not any(
        k in blob for k in ("because of", "caused by", "driven by", "due to")))
    check("the year is on the record, because it is not this year",
          out["data_year"] == 2024)
    check("it says the figure is an average of what was billed",
          "not a tariff" in out["basis"])

    print("a bad day writes nothing")
    for label, bad in (("a corrupt archive", b"not a zip"),
                       ("EIA's soft 404 page", b"<html>Page not found</html>")):
        try:
            build(bad, 2024)
            check(f"{label} raises rather than publishing", False)
        except Exception:
            check(f"{label} raises rather than publishing", True)
    thin = io.BytesIO()
    with zipfile.ZipFile(thin, "w") as z:
        z.writestr("Sales_Ult_Cust_2024.xlsx", b"x")
    try:
        build(thin.getvalue(), 2024)
        check("a file EIA stopped packing is a failure, not a gap", False)
    except LookupError as exc:
        check("a file EIA stopped packing is a failure, not a gap", True,
              str(exc)[:52])

    print("and a year EIA has not published is not silently served")
    check("a short body is refused before it is parsed",
          len(b"<html>404</html>") < MIN_ARCHIVE)

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--year", type=int, help="pin a data year instead of "
                    "asking EIA which one is newest")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    try:
        if args.year:
            year, archive = args.year, fetch(args.year)
        else:
            year, archive = newest()
    except Exception as exc:
        print(f"FAILED to fetch Form EIA-861: {exc}", file=sys.stderr)
        print("nothing written; yesterday's file is left exactly as it was",
              file=sys.stderr)
        return 1
    out = build(archive, year)
    if args.write:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1)
            fh.write("\n")
        print(f"wrote {OUT}  ({os.path.getsize(OUT) // 1024} KB)")
    print(f"Form EIA-861, data year {year}, "
          f"{len(out['utilities'])} Alaska utilities")
    for u in out["utilities"]:
        r = u["sectors"].get("residential")
        if not r:
            continue
        print(f"  {u['name'][:33]:<35}{r['cents_per_kwh']:>6} cents/kWh  "
              f"{r['customers'] or 0:>7} households  {', '.join(u['areas'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
