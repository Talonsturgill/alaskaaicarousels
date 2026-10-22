#!/usr/bin/env python3
"""akpost_reserve_verify.py -- AKPOST.reserve and the bitmap-px blur it exists for
(2026-10-21, weekly machine pass).

WHAT IT RECONSTRUCTS. Four decks running (No.89 to No.92) printed their type
reserves as slabs: blurred rectangles whose edge read as a box on textured art.
Every one of them typed its blur as design px. Chromium applies ctx.filter's
blur in BITMAP px and ignores the transform, so on the house's 2x canvas each
of those feathers was half its stated width. AKPOST.reserve takes its feather
as a design px sigma, converts it through the context's own scale, pads each
rect so the type box sits at the 90 percent contour, and blurs one opaque union.

    python3 tests/akpost_reserve_verify.py      # exit 0 = every check holds

  trap      ctx.filter blur(10px) under scale(2, 2) has the SAME 10-to-90 edge in
            device px as at scale 1, so half the width in design px. If a future
            Chromium scales filters by the transform this FAILS, and the helper's
            conversion must be revisited before anything else.
  feather   AKPOST.reserve feather 20 has a 10-to-90 edge of about 51 design px
            (2.563 sigma) at scale 2 AND at scale 1, within 3 px of each other.
  pad       the type box's own edge sits at 0.85 or more of full strength, and
            the half-strength contour lies about 1.28 sigma outside it.
  union     two overlapping rects never stack past the requested strength.
  erase     erase: true punches the same profile out of a filled canvas.
  contract  a paint reserve with no colour, an unknown option or a bad rect throws.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

JS = r"""
() => {
  const out = {};
  const edge = (row, from) => {         // first index where alpha passes 10 and 90 percent of max
    let mx = 0; for (const v of row) mx = Math.max(mx, v);
    let a = -1, b = -1;
    for (let i = from; i < row.length; i++) {
      if (a < 0 && row[i] >= 0.1 * mx) a = i;
      if (b < 0 && row[i] >= 0.9 * mx) { b = i; break; }
    }
    return [a, b, mx];
  };
  const alphaRow = (cv, y) => {
    const d = cv.getContext('2d').getImageData(0, y, cv.width, 1).data, r = [];
    for (let x = 0; x < cv.width; x++) r.push(d[4 * x + 3] / 255);
    return r;
  };
  // trap: the raw filter under each scale
  for (const sc of [1, 2]) {
    const c = document.createElement('canvas'); c.width = 800; c.height = 40;
    const g = c.getContext('2d'); g.scale(sc, sc);
    g.filter = 'blur(10px)'; g.fillStyle = '#fff'; g.fillRect(400 / sc, -200, 2000, 2000);
    const [a, b] = edge(alphaRow(c, 20), 0);
    out['raw' + sc] = { device: b - a, design: (b - a) / sc };
  }
  // feather: AKPOST.reserve on a transparent canvas, a rect from x 300 (design) rightwards
  for (const sc of [1, 2]) {
    const c = document.createElement('canvas'); c.width = 900 * sc; c.height = 200 * sc;
    const g = c.getContext('2d'); g.scale(sc, sc);
    const ret = AKPOST.reserve(g, [[300, -400, 2000, 1200]], { color: '#000000', strength: 1 });
    const row = alphaRow(c, 100 * sc);
    const [a, b, mx] = edge(row, 0);
    const at = (x) => row[Math.round(x * sc)];
    let half = -1; for (let i = 0; i < row.length; i++) if (row[i] >= 0.5 * mx) { half = i / sc; break; }
    out['res' + sc] = { design: (b - a) / sc, max: mx, atBoxEdge: at(300), half: half, ret: ret };
  }
  // union: two overlapping rects at strength 0.9
  {
    const c = document.createElement('canvas'); c.width = 1200; c.height = 400;
    const g = c.getContext('2d'); g.scale(2, 2);
    AKPOST.reserve(g, [[100, 80, 300, 40], [250, 90, 250, 40]], { color: '#070B11', strength: 0.9 });
    const d = g.getImageData(0, 0, 1200, 400).data; let mx = 0;
    for (let i = 3; i < d.length; i += 4) mx = Math.max(mx, d[i]);
    out.union = mx / 255;
  }
  // erase: punch out of an opaque field
  {
    const c = document.createElement('canvas'); c.width = 1800; c.height = 400;
    const g = c.getContext('2d'); g.fillStyle = '#123'; g.fillRect(0, 0, 1800, 400); g.scale(2, 2);
    AKPOST.reserve(g, [[300, -400, 2000, 1200]], { erase: true, strength: 1 });
    const row = alphaRow(c, 200).map((v) => 1 - v);
    const [a, b] = edge(row, 0);
    out.erase = { design: (b - a) / 2, inside: 1 - row[1200] };
  }
  // contract
  const throws = (f) => { try { f(); return false; } catch (e) { return e instanceof TypeError; } };
  const g = document.createElement('canvas').getContext('2d');
  out.contract = {
    noColour: throws(() => AKPOST.reserve(g, [[0, 0, 10, 10]], {})),
    unknown: throws(() => AKPOST.reserve(g, [[0, 0, 10, 10]], { color: '#000', blur: 9 })),
    badRect: throws(() => AKPOST.reserve(g, [[0, 0, 10]], { color: '#000' })),
  };
  return out;
}
"""


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium
    with sync_playwright() as p:
        b = launch_chromium(p)
        pg = b.new_page()
        pg.set_content("<html><body></body></html>")
        pg.add_script_tag(path=str(ROOT / "assets" / "js" / "akpost.js"))
        r = pg.evaluate(JS)
        ver = b.version
        b.close()
    bad = 0

    def ok(label, cond, extra):
        nonlocal bad
        print("  %s  %s  %s" % ("ok  " if cond else "FAIL", label, json.dumps(extra)))
        bad += 0 if cond else 1

    print("Chromium", ver)
    ok("trap: a raw blur(10px) keeps its device width under scale(2,2), half in design px",
       abs(r["raw1"]["device"] - r["raw2"]["device"]) <= 2 and r["raw2"]["design"] < 0.6 * r["raw1"]["design"],
       [r["raw1"], r["raw2"]])
    w1, w2 = r["res1"]["design"], r["res2"]["design"]
    ok("feather: sigma 20 gives a 10-to-90 edge of about 51 design px at scale 2",
       46 <= w2 <= 56, r["res2"])
    ok("feather: the same edge at scale 1 (the helper converts through the transform)",
       abs(w1 - w2) <= 3, [w1, w2])
    s2 = r["res2"]
    ok("pad: the type box's own edge sits at 0.85 of full strength or more",
       s2["atBoxEdge"] >= 0.85, s2["atBoxEdge"])
    ok("pad: the half-strength contour lies about 1.28 sigma (25.6 px) outside the box",
       20 <= 300 - s2["half"] <= 31, 300 - s2["half"])
    ok("pad: the bitmap blur the helper asked for is sigma times scale",
       abs(s2["ret"]["blurBitmapPx"] - 40) < 1e-6 and abs(r["res1"]["ret"]["blurBitmapPx"] - 20) < 1e-6,
       [s2["ret"], r["res1"]["ret"]])
    ok("union: overlapping rects never pass the requested strength",
       r["union"] <= 0.9 + 2 / 255, r["union"])
    ok("erase: the punch has the same profile and clears the inside",
       46 <= r["erase"]["design"] <= 56 and r["erase"]["inside"] <= 0.01, r["erase"])
    ok("contract: no colour, an unknown option and a bad rect each throw",
       all(r["contract"].values()), r["contract"])
    print("\nakpost_reserve_verify: " + ("all passed" if not bad else "%d FAILED" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
