#!/usr/bin/env python3
"""gaswatch_eia.py, the monthly external check on the Cook Inlet Gas Watch model.

The build brief listed Hilcorp storage inventory and Enstar sendout as not
public, and the page said so. Two of those three are wrong. EIA publishes
Alaska underground storage and Alaska gas deliveries by sector every month,
keyless, in a bulk file, and that is enough to do two things the project could
not do before.

  Storage. Alaska statewide working gas less the CINGSA volume we measure
  daily leaves non CINGSA storage, which is overwhelmingly Hilcorp. Alaska
  working capacity is several times CINGSA's design volume, so the field this
  project watches daily is the minority of the state's storage.

  Demand. Deliveries to residential, commercial and electric power consumers
  are observed consumption. The demand model can be checked against them, which
  the brief said was impossible. It is not a refit, and it must not be
  mistaken for one, because the geography and the period do not line up.

WHAT THIS DATA IS NOT. It is monthly, not daily. It is Alaska statewide, not
Southcentral. It lags about two months. So it is a lagging, wider geography
check on the model and never a substitute for the daily series, and nothing
here closes the daily gap the page describes.

Run:
  python3 scripts/gaswatch_eia.py --self-test    # hermetic, no network
  python3 scripts/gaswatch_eia.py --dry-run
  python3 scripts/gaswatch_eia.py
"""

import argparse
import io
import json
import os
import sys
import traceback
import zipfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gaswatch_collect as gc  # noqa: E402  probes, retry and the model live there

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "ledger", "gaswatch_eia.json")

# The whole natural gas dataset, no API key. The v2 API refuses without one,
# so this is the path that can run unattended.
BULK_URL = "https://api.eia.gov/bulk/NG.zip"

# Only what the cross check uses. Pulling the whole file and keeping eight
# series is deliberate; a narrower fetch would need the keyed API.
SERIES = {
    "NG.NGM_EPG0_SAO_SAK_MMCF.M": "ak_working_gas_mmcf",
    "NG.NGA_EPG0_SACW0_SAK_MMCF.M": "ak_working_gas_capacity_mmcf",
    "NG.NGM_EPG0_SAD_SAL_COUNT.M": "ak_storage_field_count",
    "NG.NGM_EPG0_SAI_SAK_MMCF.M": "ak_injections_mmcf",
    "NG.NGM_EPG0_SAW_SAK_MMCF.M": "ak_withdrawals_mmcf",
    "NG.N3010AK2.M": "residential_mmcf",
    "NG.N3020AK2.M": "commercial_mmcf",
    "NG.N3045AK2.M": "electric_power_mmcf",
    "NG.N3035AK2.M": "industrial_mmcf",
    "NG.N3060AK2.M": "delivered_total_mmcf",
}

# Keep a decade. Enough to fit a season against, small enough to commit.
KEEP_MONTHS = 132


def parse_bulk(raw_bytes):
    """Pull the wanted series out of the bulk archive.

    The file is one JSON object per line, about 24 MB unpacked, so it is
    streamed and filtered by a cheap substring test before any JSON parsing.
    """
    with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
        names = [n for n in zf.namelist() if n.endswith(".txt")]
        if not names:
            raise ValueError(f"EIA bulk archive has no .txt member, got {zf.namelist()}")
        out = {}
        with zf.open(names[0]) as fh:
            for line in io.TextIOWrapper(fh, encoding="utf-8", errors="ignore"):
                sid = None
                for want in SERIES:
                    if want in line:
                        sid = want
                        break
                if sid is None:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("series_id") != sid or not isinstance(obj.get("data"), list):
                    continue
                pairs = {str(d[0]): d[1] for d in obj["data"]
                         if isinstance(d, list) and len(d) == 2 and d[1] is not None}
                out[SERIES[sid]] = dict(sorted(pairs.items())[-KEEP_MONTHS:])
    missing = [v for v in SERIES.values() if v not in out]
    if missing:
        raise ValueError(
            f"EIA bulk file no longer carries {missing}. The series ids moved or "
            f"the file changed shape, so report it rather than publishing a "
            f"cross check built on a partial pull.")
    return out


def build(now):
    probe = gc.Probe("eia_bulk_natural_gas", BULK_URL)
    raw = gc.http_bytes(probe)
    series = parse_bulk(raw)
    months = sorted(series["delivered_total_mmcf"])
    return {
        "_spec": {
            "purpose": "Monthly external check on the Cook Inlet Gas Watch demand "
                       "model and on storage outside CINGSA. Written by "
                       "scripts/gaswatch_eia.py, never by a routine run.",
            "limits": "Monthly, not daily. Alaska statewide, not Southcentral. "
                      "Lags about two months. It checks the model and never "
                      "replaces the daily series.",
        },
        "source": BULK_URL,
        "source_label": "US Energy Information Administration, bulk natural gas dataset",
        "documentation": "https://www.eia.gov/opendata/",
        "collected_utc": gc.iso_z(now),
        "collector_version": "1.0",
        "latest_month": months[-1] if months else None,
        "months": len(months),
        "series_ids": {v: k for k, v in SERIES.items()},
        "series": series,
        "provenance": probe.as_dict(),
    }


# ------------------------------------------------------------------ self test

FIXTURE_LINES = [
    json.dumps({"series_id": "NG.NGM_EPG0_SAO_SAK_MMCF.M",
                "name": "Alaska Natural Gas in Underground Storage (Working Gas), Monthly",
                "f": "M", "units": "Million Cubic Feet",
                "data": [["202605", 29994], ["202604", 28047], ["202603", 26651]]}),
    json.dumps({"series_id": "NG.NGA_EPG0_SACW0_SAK_MMCF.M", "f": "M",
                "data": [["202605", 69905], ["202604", 69905]]}),
    json.dumps({"series_id": "NG.NGM_EPG0_SAD_SAL_COUNT.M", "f": "M",
                "data": [["202605", 5], ["202604", 5]]}),
    json.dumps({"series_id": "NG.NGM_EPG0_SAI_SAK_MMCF.M", "f": "M",
                "data": [["202605", 1947], ["202604", 1500]]}),
    json.dumps({"series_id": "NG.NGM_EPG0_SAW_SAK_MMCF.M", "f": "M",
                "data": [["202605", 278], ["202604", 400]]}),
    json.dumps({"series_id": "NG.N3010AK2.M", "f": "M",
                "data": [["202605", 1248], ["202604", 1600]]}),
    json.dumps({"series_id": "NG.N3020AK2.M", "f": "M",
                "data": [["202605", 1081], ["202604", 1300]]}),
    json.dumps({"series_id": "NG.N3045AK2.M", "f": "M",
                "data": [["202605", 1703], ["202604", 1767]]}),
    json.dumps({"series_id": "NG.N3035AK2.M", "f": "M",
                "data": [["202605", 2795], ["202604", 3158]]}),
    json.dumps({"series_id": "NG.N3060AK2.M", "f": "M",
                "data": [["202605", 6828], ["202604", 7827]]}),
]


def _fixture_zip(lines=None):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("NG.txt", "\n".join(lines if lines is not None else FIXTURE_LINES))
    return buf.getvalue()


def self_test():
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    print("bulk archive parser")
    got = parse_bulk(_fixture_zip())
    check("every wanted series is pulled", len(got) == len(SERIES),
          f"{len(got)} of {len(SERIES)}")
    check("storage working gas parses",
          got["ak_working_gas_mmcf"]["202605"] == 29994,
          str(got["ak_working_gas_mmcf"]["202605"]))
    check("consumption by sector parses",
          got["residential_mmcf"]["202605"] == 1248
          and got["electric_power_mmcf"]["202605"] == 1703)
    check("months come back sorted",
          list(got["ak_working_gas_mmcf"]) == sorted(got["ak_working_gas_mmcf"]))

    print("the gate can still go red")
    dropped = [l for l in FIXTURE_LINES if "N3045AK2" not in l]
    try:
        parse_bulk(_fixture_zip(dropped))
        check("a series disappearing is reported, not published around", False,
              "parsed anyway")
    except ValueError:
        check("a series disappearing is reported, not published around", True)
    try:
        parse_bulk(_fixture_zip([]) )
        # An empty member still parses to nothing, which the missing check
        # catches; reaching here means it did not.
        check("an empty dataset is reported", False, "parsed anyway")
    except ValueError:
        check("an empty dataset is reported", True)
    try:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("README.md", "no data here")
        parse_bulk(buf.getvalue())
        check("an archive with no data member is reported", False, "parsed anyway")
    except ValueError:
        check("an archive with no data member is reported", True)

    print()
    if not ok[0]:
        print("self-test FAILED")
        return 1
    print("self-test clean")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Monthly EIA cross check for the gas watch")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    now = datetime.now(timezone.utc)
    rec = build(now)

    # Idempotent on the data, not the clock. EIA publishes once a month, so a
    # scheduled run that finds the same latest month rewrites nothing and the
    # commit step sees no diff.
    if os.path.exists(args.out):
        try:
            prev = json.loads(open(args.out, encoding="utf-8").read())
            if prev.get("latest_month") == rec["latest_month"]:
                print(f"EIA still publishes through {rec['latest_month']}, nothing new.")
                return 0
        except Exception:
            pass

    if args.dry_run:
        print(json.dumps({k: v for k, v in rec.items() if k != "series"}, indent=2))
        return 0
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=False)
        fh.write("\n")
    s = rec["series"]
    m = rec["latest_month"]
    print(f"EIA through {m}, {rec['months']} months on file")

    # latest_month comes from the DELIVERY series alone, and EIA-191 storage
    # routinely lags it. Indexing every series at that month raised a KeyError
    # here, after the ledger had already been written, so a pull that worked
    # ended in a traceback and a red job. A series that has not caught up says
    # so and the summary carries on.
    def line(label, key, unit=""):
        val = s.get(key, {}).get(m)
        if val is None:
            print(f"  {label:32s}not published for {m} yet")
        else:
            print(f"  {label:32s}{val:,}{unit}")

    line("Alaska working gas in storage", "ak_working_gas_mmcf", " MMcf")
    line("Alaska working gas capacity", "ak_working_gas_capacity_mmcf", " MMcf")
    line("storage fields in Alaska", "ak_storage_field_count")
    line("delivered to consumers", "delivered_total_mmcf", " MMcf")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
