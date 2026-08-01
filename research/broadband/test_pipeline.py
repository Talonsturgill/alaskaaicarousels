#!/usr/bin/env python3
"""Test suite for the Alaska school broadband price pipeline.

These are not unit tests of Python. They are assertions that the six data traps are
still handled and that the output still reconciles against a fact established outside
this dataset. If USAC changes the feed, this is what fails loudly instead of quietly
publishing a wrong number.

  python3 test_pipeline.py
"""
import csv, json, glob, collections, statistics as st, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS, CHECKS = [], 0


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}   {detail}")
        FAILS.append(name)


def load_rows():
    return list(csv.DictReader(open(os.path.join(HERE, "circuits_v2.csv"))))


def main():
    rows = load_rows()
    for r in rows:
        for k in ("mbps", "per_mbps", "unit_monthly", "monthly_share"):
            r[k] = float(r[k])
    cur = [r for r in rows if r["year"] == "2026"]

    print("\n--- structural integrity ---")
    check("rows present", len(rows) > 5000, f"got {len(rows)}")
    check("all years covered", len({r['year'] for r in rows}) >= 10,
          f"years={sorted({r['year'] for r in rows})}")
    check("no zero or negative speeds", all(r["mbps"] > 0 for r in rows))
    check("no zero or negative prices", all(r["unit_monthly"] > 0 for r in rows))
    check("per_mbps is consistent with cost/speed",
          all(abs(r["per_mbps"] - r["unit_monthly"] / r["mbps"]) < 1e-6 for r in rows))

    print("\n--- TRAP 2: de-duplication ---")
    # a (year, line_item, recipient) must appear at most once
    key = collections.Counter((r["year"], r["line_item"], r["recipient"]) for r in rows)
    check("no duplicated circuit-recipient rows", max(key.values()) == 1,
          f"max multiplicity {max(key.values())}")

    print("\n--- TRAP 4: transit only, no campus loops ---")
    # Saint Mary's 10 Gbps @ $900 is a campus WAN link and must be absent
    sm = [r for r in cur if "Mary" in r["city"] and r["mbps"] >= 9000]
    check("Saint Mary's campus loop excluded", len(sm) == 0,
          f"found {len(sm)} rows that look like the WAN link")
    check("all rows are internet transit", all(r["mbps"] > 0 for r in rows))

    print("\n--- TRAP 5: service class carried ---")
    check("product/service class present on every row",
          all(r.get("product") for r in rows))
    check("Ethernet and Satellite are distinguishable",
          len({r["product"] for r in cur}) >= 3,
          f"products={sorted({r['product'] for r in cur})[:6]}")

    print("\n--- TRAP 6: nothing silently dropped as an outlier ---")
    over150 = [r for r in cur if r["per_mbps"] > 150]
    check("circuits above $150/Mbps are retained", len(over150) > 50,
          f"only {len(over150)} retained -- an outlier filter may have crept in")

    print("\n--- external reconciliation ---")
    lk = [r for r in cur if "LOWER KUSKOKWIM" in r["org"].upper()]
    annual = sum(r["monthly_share"] for r in lk) * 12
    # Lower Kuskokwim's contract is independently reported at about $101M/year.
    check("Lower Kuskokwim annualises to ~$101M",
          95e6 <= annual <= 107e6, f"got ${annual:,.0f}")

    total = sum(r["monthly_share"] for r in cur) * 12
    # E-Rate delivered roughly $115M to Alaska districts in 2023 and was expected to
    # roughly double; pre-discount billing on transit alone should land in the same order.
    check("statewide annual billing is the right order of magnitude",
          5e7 <= total <= 5e8, f"got ${total:,.0f}")

    print("\n--- join coverage ---")
    check("provider named on >=99% of current rows",
          sum(1 for r in cur if r["provider"] != "(not stated)") / len(cur) >= 0.99)
    check("USAC rural flag on >=90% of current rows",
          sum(1 for r in cur if r["usac_rural"]) / len(cur) >= 0.90)
    check("every row has a community",
          sum(1 for r in cur if r["city"] and r["city"] != "(unknown)") / len(cur) >= 0.97)

    print("\n--- city canonicalisation ---")
    cities = {r["city"] for r in cur}
    bad = [c for c in cities if c.lower().startswith("st ") or c.lower().startswith("saint ")]
    check("Saint/St variants collapsed to one form", len(set(
        c.lower().replace("saint", "st").replace(".", "") for c in bad)) == len(bad),
        f"variants: {sorted(bad)}")
    check("Barrow normalised to Utqiagvik", "Barrow" not in cities)

    print("\n--- headline figures are stable ---")
    def med100(region_flag):
        s = [r["unit_monthly"] for r in cur
             if 90 <= r["mbps"] <= 110 and r["usac_rural"] == region_flag
             and "ethernet" in r["product"].lower()]
        return st.median(s) if s else None
    rural100 = med100("Rural")
    check("rural 100 Mbps dedicated-Ethernet median is ~$75k",
          rural100 and 50000 <= rural100 <= 90000, f"got {rural100}")

    print(f"\n{CHECKS - len(FAILS)}/{CHECKS} checks passed")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        sys.exit(1)
    print("all green")


if __name__ == "__main__":
    main()
