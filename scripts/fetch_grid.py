#!/usr/bin/env python3
"""fetch_grid.py -- rebuild assets/geo/ak-transmission-69kv.geo.json from the
Alaska Energy Authority's published transmission layer.

WHY THIS IS A SCRIPT AND NOT A ONE-OFF DOWNLOAD
    The docket map draws Alaska's transmission backbone under the pins, because
    almost every decision on the docket is really a decision about that grid.
    The line has to be reproducible and its provenance has to be checkable, so
    the fetch, the filter and the simplification all live here rather than in
    somebody's shell history.

THE FILTER, WHICH IS AN EDITORIAL DECISION AND IS STATED OUT LOUD
    The source layer is 1478 features and it is NOT a statewide transmission
    map. 1383 of those features come from one utility, Homer Electric, and 1309
    of them are at 24.9 kV or below, which is local distribution, not
    transmission. Drawn whole it would say "there is a dense grid on the Kenai
    Peninsula and almost nothing anywhere else", which is an artifact of who
    submitted data rather than a fact about Alaska.

    So this keeps 69 kV and above. That subset is 64 features and 2386 km, and
    it does form the real backbone: it passes Anchorage, Willow, Healy,
    Fairbanks, Delta Junction and Kenai, which is the Railbelt, plus the
    islanded Southeast and Kodiak systems.

    69 kV is the conventional floor for transmission as opposed to distribution.
    Anything at or above it is kept, whatever utility filed it.

WHAT THIS IS NOT
    Not authoritative and not complete. AEA publishes it with an explicit
    no-warranty use constraint, and the sibling layers in the same service carry
    2013 and 2015 vintages. It is good enough to show where the backbone runs.
    It is not good enough to assert that any particular line does or does not
    exist, and the page says so.

Usage:
    python scripts/fetch_grid.py            # rewrite the asset
    python scripts/fetch_grid.py --report   # show what changed, write nothing
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
OUT = REPO / "assets" / "geo" / "ak-transmission-69kv.geo.json"

SERVICE = ("https://services2.arcgis.com/0DjevcWawQ1dy3il/arcgis/rest/services/"
           "AlaskaEnergyAuthority_Vectors/FeatureServer/15/query")
SOURCE_ITEM = "Alaska Energy Authority Library, layer 15, Electric Transmission Lines"
MIN_KV = 69.0
# About 1.1 km. The map is 1000px across for a state 3700 km wide, so one pixel
# is roughly 3.7 km. Simplifying under a third of a pixel cannot move a line
# anywhere a reader could see.
TOLERANCE_DEG = 0.01


def fetch():
    feats, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "where": "1=1", "outFields": "Name,Voltage,Source,Type",
            "outSR": "4326", "f": "geojson",
            "resultOffset": offset, "resultRecordCount": 1000,
        })
        with urllib.request.urlopen(SERVICE + "?" + q, timeout=180) as r:
            d = json.load(r)
        got = d.get("features", [])
        feats.extend(got)
        if len(got) < 1000:
            break
        offset += 1000
        if offset > 20000:
            raise SystemExit("fetch_grid: refusing to page past 20000, the service changed")
    return feats


def kv_of(props):
    """Voltage as a number. The column mixes '138KV', '230 KV' and bare '14.4'."""
    v = str(props.get("Voltage") or "").upper().replace(" ", "")
    m = re.match(r"^(\d+(?:\.\d+)?)", v)
    return float(m.group(1)) if m else None


def lines_of(feat):
    g = feat.get("geometry") or {}
    cs = g.get("coordinates")
    if not cs:
        return []
    return cs if g.get("type") == "MultiLineString" else [cs]


def simplify(pts, tol):
    """Douglas-Peucker. Iterative, because an Alaska line can be long enough to
    blow a recursion limit on a bad day."""
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
            if den == 0:
                d = math.hypot(px - ax, py - ay)
            else:
                d = abs(dy * px - dx * py + bx * ay - by * ax) / den
            if d > worst:
                worst, wi = d, i
        if worst > tol:
            keep[wi] = True
            stack.append((a, wi))
            stack.append((wi, b))
    return [p for p, k in zip(pts, keep) if k]


def build(feats):
    out, dropped_lowv, dropped_nogeom = [], 0, 0
    for f in feats:
        kv = kv_of(f.get("properties") or {})
        if kv is None or kv < MIN_KV:
            dropped_lowv += 1
            continue
        segs = lines_of(f)
        if not segs:
            dropped_nogeom += 1
            continue
        for seg in segs:
            pts = [(round(float(x), 4), round(float(y), 4)) for x, y in seg]
            pts = simplify(pts, TOLERANCE_DEG)
            if len(pts) >= 2:
                out.append({"kv": kv, "pts": [[x, y] for x, y in pts]})
    return out, dropped_lowv, dropped_nogeom


def stats(lines):
    km = 0.0
    for L in lines:
        for a, b in zip(L["pts"], L["pts"][1:]):
            km += math.hypot((b[0] - a[0]) * 55.6, (b[1] - a[1]) * 111.3)
    return km, sum(len(L["pts"]) for L in lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--report", action="store_true", help="print, write nothing")
    args = ap.parse_args()

    print("fetching %s" % SOURCE_ITEM)
    feats = fetch()
    print("  %d features from the service" % len(feats))
    lines, low, nogeom = build(feats)
    km, verts = stats(lines)
    print("  kept %d segments at %g kV and above" % (len(lines), MIN_KV))
    print("  dropped %d below the floor, %d with no geometry" % (low, nogeom))
    print("  %.0f km, %d vertices after simplifying at %g degrees" % (km, verts, TOLERANCE_DEG))

    doc = {
        "_source": SOURCE_ITEM,
        "_service": SERVICE.rsplit("/query", 1)[0],
        "_attribution": "Alaska Energy Authority via Alaska DCCED, no warranty",
        "_filter": "voltage >= %g kV, which is transmission rather than distribution" % MIN_KV,
        "_simplified_deg": TOLERANCE_DEG,
        "_rebuild": "python scripts/fetch_grid.py",
        "lines": lines,
    }
    body = json.dumps(doc, separators=(",", ":"))
    if args.report:
        print("\n--report, nothing written. Would be %.0f KB" % (len(body) / 1024))
        return 0
    OUT.write_text(body)
    print("\nwrote %s  %.0f KB" % (OUT.relative_to(REPO), OUT.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
