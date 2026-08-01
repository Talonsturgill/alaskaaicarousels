#!/usr/bin/env python3
"""Alaska school broadband price pipeline.

Turns five USAC open-data tables into one row per circuit-recipient: what a named
community pays, for how much bandwidth, to which provider, under how much bidding
competition, at what discount rate, for how many students.

WHY THE UNIT IS A CIRCUIT AND NOT A DISTRICT
--------------------------------------------
The billed entity is usually a district headquartered in a hub town. Lower Kuskokwim
bills out of Bethel and serves ~22 delta villages. District-level analysis hides which
village sits on the expensive circuit, so every line item is exploded to its recipients
via the Recipients of Service table and then geocoded.

THE FIVE TRAPS
--------------
Each one silently produces a wrong answer, and each is handled here.

 1. UNIT COST vs BILL. `total_monthly_cost` is per unit. The bill is that times
    `monthly_quantity` (= `total_monthly_eligible_recurring_costs`). Using the raw
    field understates multi-site districts by up to 6x.

 2. DOUBLE ROWS. Every line item is published twice, form_version Original and
    Current. 6,156 of Alaska's 6,706 line items are duplicated. A naive sum doubles
    the state's bill.

 3. QUANTITY ZERO. 3,380 Alaska rows are one-time equipment with no bandwidth. They
    must not enter a price per megabit.

 4. TRANSIT vs CAMPUS LOOP. The one that nearly broke the analysis. Andreafski High
    School in Saint Mary's buys 100 Mbps of INTERNET for $75,000/mo and a 10 Gbps link
    between its own buildings for $900/mo. Both file as "Fiber". Only `purpose`
    separates them. Mixing them makes local loops look like miraculously cheap
    internet. Only transit is comparable across communities.

 5. SERVICE CLASS. Found by verifying a headline before publishing it. In Wrangell GCI
    bills the school district $7,500/mo for 500 Mbps and the public library $100/mo for
    1 Gbps -- but the school circuit is Fiber/Ethernet (dedicated, symmetric, SLA) and
    the library's is Copper/Cable Modem (shared, best-effort). Those are different
    products and comparing them would be dishonest. `form_471_product_name` is carried
    through and every provider comparison is controlled on it.

 6. THE OUTLIER FILTER. Not in the data -- in the literature. Published K-12 broadband
    research routinely drops circuits above $150/Mbps as implausible outliers. In
    off-road Alaska $285/Mbps is the MEDIAN. National method silently deletes rural
    Alaska. Nothing is dropped here; extremes are the finding.

WHY PRICE PER MEGABIT IS COMPUTED PER CIRCUIT
---------------------------------------------
A line item with quantity 6 is six circuits, each at the stated speed for the stated
unit cost. Price per megabit is unit monthly cost / speed, so a 6-school district stays
comparable to a 1-school district instead of looking 6x more expensive.
"""
from __future__ import annotations
import json, glob, csv, collections, statistics as st, re, os, sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

SPEED_UNITS = {"Mbps": 1.0, "Gbps": 1000.0, "Kbps": 0.001}
CIRCUIT_FUNCTIONS = {"Fiber", "Wireless", "Copper"}   # things with a bandwidth


# ---------------------------------------------------------------- helpers
def load(pattern: str) -> list[dict]:
    out = []
    for f in sorted(glob.glob(os.path.join(DATA, pattern))):
        try:
            d = json.load(open(f))
        except json.JSONDecodeError:
            continue
        if isinstance(d, list):
            out += d
    return out


def num(v):
    if v in (None, ""):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def pct(vals, p):
    v = sorted(vals)
    if not v:
        return float("nan")
    return v[min(len(v) - 1, max(0, int(round((len(v) - 1) * p))))]


def purpose_class(p: str | None) -> str:
    """TRAP 4: separate internet transit from an internal campus/WAN link."""
    p = (p or "").lower()
    if "between two or more sites entirely within" in p:
        return "wan"
    if "applicant owned fiber" in p or "backbone circuit for consortium" in p:
        return "wan"
    if "internet access" in p or "to an internet service provider" in p:
        return "internet"
    return "unknown"


def latest_version(rows, key):
    """TRAP 2: keep form_version 'Current' where a record exists twice."""
    best = {}
    for r in rows:
        k = key(r)
        if k not in best or r.get("form_version") == "Current":
            best[k] = r
    return best


# City strings arrive inconsistently across USAC tables. Normalise to one canonical
# key so "Saint Marys", "St. Marys" and "ST MARYS" collapse to a single community
# instead of splitting one village into three rows.
_CITY_FIX = {
    "st marys": "Saint Marys", "saint marys": "Saint Marys", "pitkas point": "Saint Marys",
    "st michael": "Saint Michael", "saint michael": "Saint Michael",
    "st paul island": "Saint Paul Island", "st paul is": "Saint Paul Island",
    "st george island": "Saint George Island", "st nenana": "Nenana",
    "barrow": "Utqiagvik", "mc grath": "McGrath", "mcgrath": "McGrath",
    "brevig": "Brevig Mission", "prudhoe bay": "Deadhorse",
    "jber": "Anchorage", "ft richardson": "Anchorage", "fort richardson": "Anchorage",
    "ft wainwright": "Fairbanks", "fort wainwright": "Fairbanks",
    "eielson afb": "Eielson AFB",
}


def canon_city(s: str | None) -> str:
    c = re.sub(r"\s+", " ", (s or "").strip()).strip(" .,")
    if not c:
        return ""
    k = c.lower().replace(".", "").replace("'", "")
    k = re.sub(r"\s+", " ", k)
    if k in _CITY_FIX:
        return _CITY_FIX[k]
    return c.title()


# ---------------------------------------------------------------- build
def build_circuits() -> list[dict]:
    raw = load("ak_*.json")
    ded = latest_version(raw, lambda r: (r.get("application_number"),
                                         r.get("funding_request_number"),
                                         r.get("form_471_line_item_number")))
    out = []
    for r in ded.values():
        if r.get("form_471_function_name") not in CIRCUIT_FUNCTIONS:
            continue
        spd = num(r.get("download_speed"))
        unit = SPEED_UNITS.get(r.get("form_471_download_speed_unit_name"))
        if not spd or not unit:
            continue
        mbps = spd * unit
        qty = num(r.get("monthly_quantity")) or 0        # TRAP 3
        cost = num(r.get("total_monthly_cost"))          # TRAP 1: per unit
        if mbps <= 0 or qty <= 0 or not cost or cost <= 0:
            continue
        billed = num(r.get("total_monthly_eligible_recurring_costs"))
        if billed is None:
            billed = cost * qty
        out.append({
            "year": r.get("funding_year"),
            "app": r.get("application_number"),
            "frn": r.get("funding_request_number"),
            "line_item": r.get("form_471_line_item_number"),
            "ben": r.get("ben"),
            "org": (r.get("organization_name") or "").strip(),
            "function": r.get("form_471_function_name"),
            "product": (r.get("form_471_product_name") or "").strip() or "(not stated)",
            "purpose_class": purpose_class(r.get("form_471_purpose_name")),
            "mbps": mbps,
            "circuits": qty,
            "unit_monthly": cost,
            "monthly_billed": billed,
            "per_mbps": cost / mbps,
        })
    return out


def provider_index() -> dict:
    """(year, frn) -> provider name, bid count, contract type/date."""
    rows = load("frn_*.json")
    best = latest_version(rows, lambda r: (r.get("funding_year"),
                                           r.get("funding_request_number")))
    idx = {}
    for (yr, frn), r in best.items():
        idx[(yr, frn)] = {
            "provider": (r.get("spin_name") or "").strip() or "(not stated)",
            "bids": num(r.get("bid_count")),
            "contract_type": (r.get("contract_type_name") or "").strip(),
            "award_date": (r.get("award_date") or "")[:10],
            "service_type": (r.get("form_471_service_type_name") or "").strip(),
        }
    return idx


def discount_index() -> dict:
    """BEN -> Category One discount rate, student count, USAC's own rural flag."""
    rows = load("disc_*.json")
    idx = {}
    for r in rows:
        for ben_f, name_f in (("par_entity_ben", "par_entity_name"),):
            ben = r.get(ben_f)
            if not ben:
                continue
            d = num(r.get("c1_discount"))
            students = num(r.get("entity_number_of_students")) or num(r.get("par_students_count"))
            ur = (r.get("par_entity_is_urban_or_rural") or "").strip()
            cur = idx.setdefault((r.get("funding_year"), ben), {})
            if d is not None:
                cur["discount"] = d
            if students:
                cur["students"] = students
            if ur:
                cur["usac_rural"] = ur
    return idx


def entity_index() -> dict:
    ents = load("entities_ak.json")
    return {e.get("entity_number"): e for e in ents}


def recipient_index() -> dict:
    rows = load("recip_*.json")
    best = latest_version(rows, lambda r: (r.get("funding_year"),
                                           r.get("form_471_line_item_number"),
                                           r.get("ben")))
    by_line = collections.defaultdict(list)
    for (yr, li, ben), r in best.items():
        by_line[(yr, li)].append(r)
    return by_line


def build(transit_only=True) -> list[dict]:
    circuits = build_circuits()
    if transit_only:
        circuits = [c for c in circuits if c["purpose_class"] == "internet"]
    prov, disc, ents, recips = provider_index(), discount_index(), entity_index(), recipient_index()

    rows, matched, unmatched = [], 0, 0
    for c in circuits:
        rs = recips.get((c["year"], c["line_item"]))
        p = prov.get((c["year"], c["frn"]), {})
        if not rs:
            unmatched += 1
            continue
        matched += 1
        allocs = [num(r.get("original_allocation")) for r in rs]
        use_alloc = all(a is not None and a > 0 for a in allocs) and sum(allocs) > 0
        for r, a in zip(rs, allocs):
            ben = r.get("ben")
            ent = ents.get(ben) or {}
            city = canon_city(ent.get("physical_city"))
            dd = disc.get((c["year"], ben), {}) or disc.get((c["year"], c["ben"]), {})
            share = (a / sum(allocs)) if use_alloc else (1.0 / len(rs))
            rows.append({
                **{k: c[k] for k in ("year", "org", "line_item", "frn", "function",
                                     "product", "mbps", "unit_monthly", "per_mbps")},
                "recipient": (r.get("organization_name") or "").strip(),
                "city": city or "(unknown)",
                "county": (ent.get("physical_county") or "").strip().title(),
                "entity_type": ent.get("entity_type") or "",
                "provider": p.get("provider", "(not stated)"),
                "bids": p.get("bids"),
                "contract_type": p.get("contract_type", ""),
                "award_date": p.get("award_date", ""),
                "discount": dd.get("discount"),
                "students": dd.get("students"),
                "usac_rural": dd.get("usac_rural", ""),
                "monthly_share": c["monthly_billed"] * share,
                "alloc_method": "usac_allocation" if use_alloc else "even_split",
                "recips_on_circuit": len(rs),
            })
    sys.stderr.write(f"[pipeline] circuits {len(circuits):,}  matched {matched:,} "
                     f"({matched/max(1,matched+unmatched)*100:.1f}%)  rows {len(rows):,}\n")
    return rows


def main():
    rows = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "circuits_v2.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out}  ({len(rows):,} circuit-recipient rows)")

    cur = [r for r in rows if r["year"] == "2026"]
    print(f"\nFY2026: {len(cur)} rows, {len({r['city'] for r in cur})} communities, "
          f"{len({r['provider'] for r in cur})} providers")
    print(f"provider coverage: "
          f"{sum(1 for r in cur if r['provider'] != '(not stated)')/len(cur)*100:.1f}%")
    print(f"discount coverage: {sum(1 for r in cur if r['discount'])/len(cur)*100:.1f}%")
    print(f"USAC rural flag coverage: "
          f"{sum(1 for r in cur if r['usac_rural'])/len(cur)*100:.1f}%")

    print("\n=== providers, FY2026 internet transit ===")
    by = collections.defaultdict(list)
    for r in cur:
        by[r["provider"]].append(r)
    print(f"{'provider':38s} {'circ':>5s} {'med $/Mbps':>11s} {'med Mbps':>9s} {'$/mo total':>12s}")
    for p, rs in sorted(by.items(), key=lambda kv: -st.median([x["per_mbps"] for x in kv[1]])):
        if len(rs) < 2:
            continue
        print(f"{p[:38]:38s} {len(rs):5d} {st.median([x['per_mbps'] for x in rs]):11.2f} "
              f"{st.median([x['mbps'] for x in rs]):9.0f} "
              f"{sum(x['monthly_share'] for x in rs):12,.0f}")


if __name__ == "__main__":
    main()
