#!/usr/bin/env python3
"""Build the published bundle: one lookup record per community, plus the aggregates.

The page is a LOOKUP TOOL first. A district technology director arrives asking one
question -- "am I overpaying?" -- so every community carries its own peer benchmark
and its own dollar gap, precomputed, rather than making the reader do arithmetic.

PEER DEFINITION (the honest part). A circuit's peers are circuits in the same
  * speed band (same tier boundaries used throughout)
  * service class (dedicated Ethernet is not compared against satellite or cable)
  * rurality, using USAC's own Rural/Urban flag rather than a hand-drawn list
in the same funding year. If a cell has fewer than 3 peers the benchmark is withheld
rather than computed on noise.
"""
import csv, json, collections, statistics as st, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = [(0, 50), (50, 150), (150, 600), (600, 1500), (1500, 10**9)]
TIER_NAMES = ["Under 50 Mbps", "50-150 Mbps", "150-600 Mbps", "600 Mbps-1.5 Gbps", "Over 1.5 Gbps"]
MIN_PEERS = 3


def tier_of(mbps):
    for i, (lo, hi) in enumerate(TIERS):
        if lo <= mbps < hi:
            return i
    return len(TIERS) - 1


def svc_class(product):
    p = (product or "").lower()
    if "satellite" in p:
        return "Satellite"
    if "microwave" in p:
        return "Microwave"
    if "cable modem" in p or "dsl" in p or "subscriber line" in p:
        return "Shared / best-effort"
    return "Dedicated"


def med(v):
    return round(st.median(v), 2) if v else None


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "circuits_v2.csv")))]
    for r in rows:
        for k in ("mbps", "per_mbps", "unit_monthly", "monthly_share"):
            r[k] = float(r[k])
        r["students"] = float(r["students"]) if r["students"] else None
        r["discount"] = float(r["discount"]) if r["discount"] else None
        r["bids"] = float(r["bids"]) if r["bids"] else None
        r["tier"] = tier_of(r["mbps"])
        r["svc"] = svc_class(r["product"])
    cur = [r for r in rows if r["year"] == "2026"]

    # ---- peer benchmark: (tier, svc, rural) -> median unit monthly cost
    cells = collections.defaultdict(list)
    for r in cur:
        if r["usac_rural"]:
            cells[(r["tier"], r["svc"], r["usac_rural"])].append(r["unit_monthly"])
    bench = {f"{k[0]}|{k[1]}|{k[2]}": med(v) for k, v in cells.items() if len(v) >= MIN_PEERS}
    bench_n = {f"{k[0]}|{k[1]}|{k[2]}": len(v) for k, v in cells.items() if len(v) >= MIN_PEERS}

    # A peer median is a WEAK benchmark where one provider holds the cell: if 40 of 44
    # comparable circuits are the same seller at the same price, the median simply IS
    # that price and nobody shows a gap. So also publish, per (tier, rural), what every
    # OTHER service class costs -- that is the number a district can actually act on,
    # clearly labelled, because a satellite link is not a dedicated circuit.
    alts = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in cur:
        if r["usac_rural"]:
            alts[(r["tier"], r["usac_rural"])][r["svc"]].append(r["unit_monthly"])
    alt_out = {}
    for (t, ru), d in alts.items():
        opts = [{"svc": s, "monthly": med(v), "n": len(v)} for s, v in d.items() if len(v) >= MIN_PEERS]
        if opts:
            alt_out[f"{t}|{ru}"] = sorted(opts, key=lambda o: o["monthly"])

    geo = {c["city"]: c for c in json.load(open(os.path.join(HERE, "communities_geo.json")))}

    # ---- per community
    byc = collections.defaultdict(list)
    for r in cur:
        byc[r["city"]].append(r)
    comms = []
    for city, rs in byc.items():
        if city == "(unknown)":
            continue
        g = geo.get(city) or {}
        gap = 0.0
        for r in rs:
            k = f"{r['tier']}|{r['svc']}|{r['usac_rural']}"
            b = bench.get(k)
            if b is not None and r["unit_monthly"] > b:
                gap += (r["unit_monthly"] - b) * 12
        provs = collections.Counter(r["provider"] for r in rs)
        students = [r["students"] for r in rs if r["students"]]
        disc = [r["discount"] for r in rs if r["discount"]]
        comms.append({
            "city": city,
            "lon": g.get("lon"), "lat": g.get("lat"),
            "region": g.get("region", ""),
            "rural": rs[0]["usac_rural"],
            "sites": len({r["recipient"] for r in rs}),
            "circuits": len(rs),
            "per_mbps": med([r["per_mbps"] for r in rs]),
            "mbps": med([r["mbps"] for r in rs]),
            "monthly": round(sum(r["monthly_share"] for r in rs)),
            "provider": provs.most_common(1)[0][0],
            "providers": [p for p, _ in provs.most_common()],
            "svc": collections.Counter(r["svc"] for r in rs).most_common(1)[0][0],
            "gap": round(gap),
            "students": int(max(students)) if students else None,
            "discount": med(disc),
            "bids": med([r["bids"] for r in rs if r["bids"] is not None]),
            "tier": collections.Counter(r["tier"] for r in rs).most_common(1)[0][0],
        })
    comms.sort(key=lambda c: -(c["per_mbps"] or 0))

    # ---- providers, controlled: rural + dedicated only
    prov = []
    ded = [r for r in cur if r["svc"] == "Dedicated" and r["usac_rural"] == "Rural"]
    for p, rs in collections.Counter(r["provider"] for r in ded).most_common():
        sub = [r for r in ded if r["provider"] == p]
        prov.append({"provider": p, "n": len(sub),
                     "per_mbps": med([r["per_mbps"] for r in sub]),
                     "mbps": med([r["mbps"] for r in sub]),
                     "monthly": round(sum(r["monthly_share"] for r in sub)),
                     "communities": len({r["city"] for r in sub})})
    prov.sort(key=lambda x: -x["monthly"])

    # ---- the controlled like-for-like cell that carries the headline
    cell = [r for r in cur if r["tier"] == 1 and r["svc"] == "Dedicated" and r["usac_rural"] == "Rural"]
    cellrows = []
    for p, rs in collections.Counter(r["provider"] for r in cell).most_common():
        sub = [r for r in cell if r["provider"] == p]
        cellrows.append({"provider": p, "n": len(sub),
                         "monthly": med([r["unit_monthly"] for r in sub]),
                         "mbps": med([r["mbps"] for r in sub])})

    # ---- headline: 100 Mbps dedicated, by rurality
    hero = {}
    for flag in ("Urban", "Rural"):
        s = [r["unit_monthly"] for r in cur
             if 90 <= r["mbps"] <= 110 and r["svc"] == "Dedicated" and r["usac_rural"] == flag]
        if s:
            hero[flag] = {"n": len(s), "monthly": med(s)}

    # ---- satellite substitute, same villages
    sat = [r for r in cur if r["svc"] == "Satellite" and r["usac_rural"] == "Rural" and r["tier"] == 1]
    substitute = {"n": len(sat), "communities": len({r["city"] for r in sat}),
                  "monthly": med([r["unit_monthly"] for r in sat]),
                  "mbps": med([r["mbps"] for r in sat])} if sat else None

    # ---- trend, all years, transit
    trend = []
    for y in sorted({r["year"] for r in rows}):
        ys = [r for r in rows if r["year"] == y]
        trend.append({"year": int(y), "n": len(ys),
                      "per_mbps": med([r["per_mbps"] for r in ys]),
                      "mbps": med([r["mbps"] for r in ys])})

    # ---- tier table by rurality
    tiers = []
    for i, nm in enumerate(TIER_NAMES):
        row = {"tier": nm}
        for flag in ("Urban", "Rural"):
            s = [r for r in cur if r["tier"] == i and r["svc"] == "Dedicated" and r["usac_rural"] == flag]
            row[flag] = {"n": len(s), "monthly": med([r["unit_monthly"] for r in s]),
                         "per_mbps": med([r["per_mbps"] for r in s])} if len(s) >= MIN_PEERS else None
        tiers.append(row)

    total_gap = sum(c["gap"] for c in comms)
    bundle = {
        "hero": hero, "substitute": substitute, "cell": cellrows,
        "communities": comms, "providers": prov, "trend": trend, "tiers": tiers,
        "bench": bench, "bench_n": bench_n, "alts": alt_out,
        "outline": json.load(open(os.path.join(HERE, "build/ak_outline.json"))),
        "totals": {
            "annual": round(sum(r["monthly_share"] for r in cur) * 12),
            "circuits": len(cur), "communities": len(comms),
            "providers": len({r["provider"] for r in cur}),
            "gap": round(total_gap),
            # NOTE: no student total. `entity_number_of_students` is a DISTRICT-level
            # count repeated on each of that district's communities, so summing it
            # across communities double-counts badly -- an early build produced 128,172,
            # more than Alaska's entire K-12 enrollment. Kept per-community only, where
            # it is at least interpretable, and never aggregated.
        },
        "tier_names": TIER_NAMES,
    }
    out = os.path.join(HERE, "build/bundle2.json")
    json.dump(bundle, open(out, "w"), separators=(",", ":"))
    print(f"wrote {out}  {len(json.dumps(bundle,separators=(',',':')))/1024:.1f} KB")
    print(json.dumps({k: bundle[k] for k in ("hero", "substitute", "totals")}, indent=1))
    print("\ncontrolled cell (rural, dedicated, 50-150 Mbps):")
    for r in cellrows:
        print(f"   {r['provider'][:44]:44s} ${r['monthly']:>10,.0f}/mo  n={r['n']}")


if __name__ == "__main__":
    main()
