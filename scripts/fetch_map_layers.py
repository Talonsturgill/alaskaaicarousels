#!/usr/bin/env python3
"""fetch_map_layers.py -- rebuild the docket map's context layers from public
state and federal data.

WHY THESE LAYERS EXIST
    The docket map used to be eight pins on an empty coastline, which made the
    pins look like a coincidence. They are not. Four of them cluster on the
    Railbelt because that is where the power is, the North Slope pin sits on the
    pipeline corridor, and the Cook Inlet items are about gas. The layers say
    the thing the pin list cannot.

EVERY LAYER IS FILTERED, AND EVERY FILTER IS AN EDITORIAL DECISION
    Published infrastructure data is not neutral. It reflects who bothered to
    file it. Drawn raw, two of these layers would tell the reader something
    false about Alaska, so each one states its cut on the page.

    GRID        AEA publishes 1478 "transmission" features. 1383 come from one
                utility, Homer Electric, and 1309 are at 24.9 kV or below, which
                is local distribution. Raw, the map would say "dense grid on the
                Kenai, nothing anywhere else", which is a fact about filing
                habits. Cut at 69 kV, the conventional transmission floor.

    GENERATION  152 Alaska plants in the EIA set, but 80 are under 5 MW and most
                of those are village diesel gensets. Raw, the map would be a
                rash of dots across rural Alaska that says nothing about where
                the load can actually go. Cut at 20 MW, which is 31 plants and
                79 percent of the state's capacity. That the number is 79 is
                itself the point: Alaska's capacity is concentrated.

    PIPELINES   TAPS and the gas lines, both carried whole, since neither has a
                submission bias worth correcting for.

WHAT NONE OF THIS IS
    Authoritative. AEA publishes with an explicit no-warranty use constraint and
    sibling layers in that service carry 2013 and 2015 vintages. Good enough to
    show where the backbone runs. Not good enough to assert that any particular
    line or plant does or does not exist, and the page says so.

Usage:
    python scripts/fetch_map_layers.py              # rebuild every layer
    python scripts/fetch_map_layers.py --only grid  # one layer
    python scripts/fetch_map_layers.py --report     # show sizes, write nothing
"""

import argparse
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GEO = REPO / "assets" / "geo"

AEA = ("https://services2.arcgis.com/0DjevcWawQ1dy3il/arcgis/rest/services/"
       "AlaskaEnergyAuthority_Vectors/FeatureServer")
EIA = ("https://services2.arcgis.com/FiaPA4ga0iQKduv3/arcgis/rest/services/"
       "Power_Plants_in_the_US/FeatureServer/0")

# About 1.1 km. The map is 1000px across for a state 3700 km wide, so one pixel
# is roughly 3.7 km. Simplifying under a third of a pixel cannot move a line
# anywhere a reader could see.
TOLERANCE_DEG = 0.01
MIN_KV = 69.0
MIN_MW = 20.0


def fetch(service, where, fields, timeout=180):
    feats, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "where": where, "outFields": fields, "outSR": "4326", "f": "geojson",
            "resultOffset": offset, "resultRecordCount": 1000})
        with urllib.request.urlopen(service + "/query?" + q, timeout=timeout) as r:
            d = json.load(r)
        got = d.get("features", [])
        feats.extend(got)
        if len(got) < 1000:
            return feats
        offset += 1000
        if offset > 30000:
            raise SystemExit("fetch_map_layers: refusing to page past 30000")


def simplify(pts, tol):
    """Douglas-Peucker, iterative so a long Alaska line cannot blow the stack."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        den = math.hypot(dx, dy)
        worst, wi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = (math.hypot(px - ax, py - ay) if den == 0 else
                 abs(dy * px - dx * py + bx * ay - by * ax) / den)
            if d > worst:
                worst, wi = d, i
        if worst > tol:
            keep[wi] = True
            stack.extend([(a, wi), (wi, b)])
    return [p for p, k in zip(pts, keep) if k]


def segments(feat):
    g = feat.get("geometry") or {}
    cs = g.get("coordinates")
    if not cs:
        return []
    return cs if g.get("type") == "MultiLineString" else [cs]


def lines_from(feats, keep=None):
    """Project nothing here. Just clean, simplify and round."""
    out = []
    for f in feats:
        if keep and not keep(f.get("properties") or {}):
            continue
        for seg in segments(f):
            pts = simplify([(round(float(x), 4), round(float(y), 4)) for x, y in seg],
                           TOLERANCE_DEG)
            if len(pts) >= 2:
                out.append([[x, y] for x, y in pts])
    return out


def km_of(lines):
    return sum(math.hypot((b[0] - a[0]) * 55.6, (b[1] - a[1]) * 111.3)
               for L in lines for a, b in zip(L, L[1:]))


def kv_of(props):
    """The column mixes '138KV', '230 KV' and bare '14.4'."""
    m = re.match(r"^(\d+(?:\.\d+)?)", str(props.get("Voltage") or "").upper().replace(" ", ""))
    return float(m.group(1)) if m else None


# ---------- the layers ----------

def build_grid():
    feats = fetch(AEA + "/15", "1=1", "Name,Voltage,Source,Type")
    lines = lines_from(feats, keep=lambda p: (kv_of(p) or 0) >= MIN_KV)
    # Voltage has to survive onto each segment, since weight carries it on the map.
    tagged = []
    for f in feats:
        kv = kv_of(f.get("properties") or {})
        if kv is None or kv < MIN_KV:
            continue
        for seg in segments(f):
            pts = simplify([(round(float(x), 4), round(float(y), 4)) for x, y in seg],
                           TOLERANCE_DEG)
            if len(pts) >= 2:
                tagged.append({"kv": kv, "pts": [[x, y] for x, y in pts]})
    return "ak-transmission-69kv.geo.json", {
        "_source": "Alaska Energy Authority Library, layer 15, Electric Transmission Lines",
        "_service": AEA + "/15",
        "_attribution": "Alaska Energy Authority via Alaska DCCED, no warranty",
        "_filter": "voltage >= %g kV, transmission rather than distribution. "
                   "The raw layer is 93 percent low voltage lines from one utility." % MIN_KV,
        "_kept": "%d segments, %.0f km" % (len(tagged), km_of([t["pts"] for t in tagged])),
        "lines": tagged,
    }, "%d segments, %.0f km" % (len(tagged), km_of([t["pts"] for t in tagged]))


def build_generation():
    feats = fetch(EIA, "State='Alaska'",
                  "Plant_Name,Utility_Na,PrimSource,tech_desc,Total_MW,City")
    total_all = sum((f["properties"].get("Total_MW") or 0) for f in feats)
    pts = []
    for f in feats:
        p = f["properties"]
        mw = p.get("Total_MW") or 0
        g = f.get("geometry") or {}
        if mw < MIN_MW or g.get("type") != "Point" or not g.get("coordinates"):
            continue
        lon, lat = g["coordinates"]
        pts.append({
            "n": (p.get("Plant_Name") or "").strip(),
            "mw": round(float(mw), 1),
            "src": (p.get("PrimSource") or "").strip(),
            "at": [round(float(lon), 4), round(float(lat), 4)],
        })
    pts.sort(key=lambda x: -x["mw"])
    kept = sum(x["mw"] for x in pts)
    share = 100.0 * kept / total_all if total_all else 0
    return "ak-generation-20mw.geo.json", {
        "_source": "EIA power plants, PowerPlants_US_EIA, Alaska subset",
        "_service": EIA,
        "_attribution": "US Energy Information Administration",
        "_filter": "nameplate >= %g MW. %d of %d Alaska plants, %.0f of %.0f MW, "
                   "%.0f percent of state capacity. The ones left out are mostly "
                   "village diesel." % (MIN_MW, len(pts), len(feats), kept, total_all, share),
        "plants": pts,
    }, "%d plants, %.0f MW, %.0f%% of state capacity" % (len(pts), kept, share)


def stitch(segs, tol=0.002):
    """Chain segments that share an endpoint into continuous runs.

    TAPS arrives as 801 milepost slivers of one pipeline. Simplifying them
    individually cannot remove a vertex that is somebody else's endpoint, so
    801 slivers stay 801 slivers and the layer weighs 60 KB for one line.
    Joined first, then simplified, it collapses to almost nothing."""
    remaining = [list(map(tuple, s)) for s in segs if len(s) >= 2]
    key = lambda p: (round(p[0] / tol), round(p[1] / tol))
    runs = []
    while remaining:
        run = remaining.pop()
        joined = True
        while joined:
            joined = False
            for i, s in enumerate(remaining):
                if key(s[0]) == key(run[-1]):
                    run += s[1:]
                elif key(s[-1]) == key(run[-1]):
                    run += s[::-1][1:]
                elif key(s[-1]) == key(run[0]):
                    run = s[:-1] + run
                elif key(s[0]) == key(run[0]):
                    run = s[::-1][:-1] + run
                else:
                    continue
                remaining.pop(i)
                joined = True
                break
        runs.append(run)
    return runs


def build_taps():
    """TAPS only.

    The Natural Gas Lines layer is deliberately NOT here. It is 2887 features
    whose median length is 0.31 km, 96 percent are under 1 km, and 2439 of them
    sit on the Kenai Peninsula. It carries no attributes at all beyond an id, so
    there is no way to tell a transmission main from a service line and no way
    to cut it honestly. Drawing it would repeat the exact mistake the 69 kV cut
    exists to avoid, and it would put 140 KB on a phone to do it.
    """
    feats = fetch(AEA + "/13", "1=1", "ROUTENAME,MILE_BEGIN")
    raw = [s for f in feats for s in segments(f)]
    runs = stitch(raw)
    lines = []
    for run in runs:
        pts = simplify([(round(float(x), 4), round(float(y), 4)) for x, y in run],
                       TOLERANCE_DEG)
        if len(pts) >= 2:
            lines.append([[x, y] for x, y in pts])
    return "ak-taps.geo.json", {
        "_source": "Alaska Energy Authority Library, layer 13, Trans Alaska Pipeline System",
        "_service": AEA + "/13",
        "_attribution": "Alaska Energy Authority via Alaska DCCED, no warranty",
        "_filter": "carried whole. %d milepost segments stitched into %d runs, "
                   "then simplified." % (len(raw), len(runs)),
        "_excluded": "The Natural Gas Lines layer is left out on purpose. 96 percent "
                     "of its 2887 features are under 1 km and 84 percent are on the "
                     "Kenai, and it has no attributes to cut it by, so it is "
                     "distribution clutter rather than a pipeline map.",
        "lines": lines,
    }, "%d segments stitched to %d runs, %.0f km" % (len(raw), len(lines), km_of(lines))


LAYERS = {"grid": build_grid, "generation": build_generation, "taps": build_taps}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", choices=sorted(LAYERS), help="rebuild one layer")
    ap.add_argument("--report", action="store_true", help="print sizes, write nothing")
    args = ap.parse_args()

    names = [args.only] if args.only else sorted(LAYERS)
    for name in names:
        print("building %s" % name)
        fn, doc, note = LAYERS[name]()
        doc["_rebuild"] = "python scripts/fetch_map_layers.py --only %s" % name
        body = json.dumps(doc, separators=(",", ":"))
        print("   %s" % note)
        print("   %s  %.0f KB%s" % (fn, len(body) / 1024, "  (not written)" if args.report else ""))
        if not args.report:
            (GEO / fn).write_text(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
