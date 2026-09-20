#!/usr/bin/env python3
"""ribbon_taper_verify.py -- the reconstructions behind two AKSECT geometry
fixes, the ribbon resample guard and the per-segment lip (2026-09-20, run
No.64, Codex rounds two and four on PR #391).

WHAT IT RECONSTRUCTS. `ribbon()` draws a line across air as a TAPERED cased
polygon, and `widthAt()` is `sin(pi * t)`, which is zero at t = 0 and t = 1 by
construction. A polyline that arrives with only two points is sampled at
exactly those two values, so both the body and the casing polygon have ZERO
AREA and the mark renders as nothing. That is what emptied the locator ticks on
run No.64 and why the resample block exists.

The block then guarded itself with `total / (pts.length - 1) > DENSE`, so a
SHORT two point path -- 6 design px or less -- skipped the resample and fell
straight back into the zero-area case the block was written to remove. The
comment promised an interior sample whatever the caller passed; the code
delivered one only for long enough inputs.

  python tests/ribbon_taper_verify.py            # exit 0 = the guard holds

The fixtures drive the REAL AKSECT.ribbon through a stub 2D context that
records the polygon vertices, and measure the shoelace area of what was
filled. Node only, no browser, no dependency.

  short2   a two point ribbon 4 px long        -> 30.7 px2 (4e-12 before)
  tiny2    a two point ribbon 1 px long        -> 7.7 px2  (2e-12 before)
  long2    a two point ribbon 40 px long, the
           size the locator ticks actually are -> area > 0, and IDENTICAL
                                                  before and after, so no
                                                  shipped frame moves
  many     a five point path already denser
           than DENSE                          -> area > 0, and IDENTICAL
                                                  before and after

AND THE PER-SEGMENT LIP (Codex round four). `incise()` draws a groove as a dark
trough plus a bright lip on the UP-LIGHT shoulder, and it chose that shoulder
once for the whole path, from the mean of the vertex normals. locator() passes
a CLOSED RECTANGLE for the window, whose normals sum to roughly zero: the mean
is meaningless there, opposite edges were bevelled with opposing normals, and
half the window's lip sat on the shadowed side. The fixtures measure, for every
lip vertex, whether its displacement from the path runs WITH the key.

  rect     a closed rectangle, the locator window -> 100% of lip vertices
                                                     up-light (50% before)
  open     an open diagonal groove, which the mean
           always got right                        -> 100%, before AND after
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROBE = r"""
const fs = require('fs');
global.window = global;
/* The library ends `})(this)`, so it publishes onto whatever `this` is at
 * load time. Under CommonJS that is module.exports, not global, so it is
 * loaded into a scope object of our own and read back from there. */
const scope = {};
(new Function(fs.readFileSync(process.argv[2], 'utf8'))).call(scope);
const AKSECT = scope.AKSECT;

function measure(pts) {
  let polys = [], cur = null;
  const cx = {
    save(){}, restore(){}, beginPath(){ cur = []; }, closePath(){},
    moveTo(x, y){ cur.push([x, y]); }, lineTo(x, y){ cur.push([x, y]); },
    fill(){ if (cur) polys.push(cur); cur = []; }, stroke(){},
    set fillStyle(v){}, set strokeStyle(v){}, set lineWidth(v){},
    set lineJoin(v){}, set lineCap(v){}, set globalAlpha(v){},
    set globalCompositeOperation(v){}, set shadowBlur(v){},
    set shadowColor(v){}, set filter(v){},
    createLinearGradient(){ return { addColorStop(){} }; },
    getTransform(){ return { a: 1 }; }
  };
  const S = AKSECT.create({ seed: 1, light: { azDeg: 205, elDeg: 23 }, datumY: 960 });
  S.ribbon(cx, pts, { wMax: 6, colour: '#C8A45A', casing: '#101010' });
  let best = 0;
  for (const p of polys) {
    let a = 0;
    for (let i = 0; i < p.length; i++) {
      const q = p[(i + 1) % p.length];
      a += p[i][0] * q[1] - q[0] * p[i][1];
    }
    best = Math.max(best, Math.abs(a) / 2);
  }
  return best;
}

function lipUplight(pts) {
  /* Every vertex of the LIP band (the second fill), scored on whether it sits
   * on the up-light side of the path point it belongs to. */
  let polys = [], cur = null;
  const cx = {
    save(){}, restore(){}, beginPath(){ cur = []; }, closePath(){},
    moveTo(x, y){ cur.push([x, y]); }, lineTo(x, y){ cur.push([x, y]); },
    fill(){ if (cur) polys.push(cur); cur = []; }, stroke(){},
    set fillStyle(v){}, set strokeStyle(v){}, set lineWidth(v){},
    set globalAlpha(v){}, set globalCompositeOperation(v){},
    createLinearGradient(){ return { addColorStop(){} }; },
    getTransform(){ return { a: 1 }; }
  };
  const S = AKSECT.create({ seed: 1, light: { azDeg: 205, elDeg: 23 }, datumY: 960 });
  S.incise(cx, pts, { w: 6 });
  const lip = polys[1];                     /* trough first, then the lip */
  let up = 0, n = 0;
  for (let k = 0; k < pts.length; k++) {
    const dx = lip[k][0] - pts[k][0], dy = lip[k][1] - pts[k][1];
    if (dx * S.lightX + dy * S.lightY >= 0) up++;
    n++;
  }
  return up / n;
}

const RECT = [[100, 100], [200, 100], [200, 180], [100, 180], [100, 100]];
const OPEN = [[100, 100], [140, 130], [180, 160], [220, 190]];

const CASES = {
  short2: [[100, 100], [104, 100]],
  tiny2:  [[100, 100], [101, 100]],
  long2:  [[100, 100], [140, 100]],
  many:   [[100, 100], [110, 102], [120, 100], [130, 98], [140, 100]]
};
const out = {};
for (const k of Object.keys(CASES)) out[k] = measure(CASES[k]);
out.lip_rect = lipUplight(RECT);
out.lip_open = lipUplight(OPEN);
console.log(JSON.stringify(out));
"""


def areas(lib_path, probe):
    p = subprocess.run(["node", str(probe), str(lib_path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("  BAD  node failed on %s\n%s" % (lib_path, p.stderr[-600:]))
        return None
    return json.loads(p.stdout.strip().splitlines()[-1])


MEAN_LIP = """var mnx = 0, mny = 0;
    for (var s0 = 0; s0 < pts.length; s0++) {
      var pp = pts[s0 - 1] || pts[s0], nn = pts[s0 + 1] || pts[s0];
      var sx = nn[0] - pp[0], sy = nn[1] - pp[1];
      var sl = Math.sqrt(sx * sx + sy * sy) || 1;
      mnx += -sy / sl; mny += sx / sl;
    }
    var ml = Math.sqrt(mnx * mnx + mny * mny) || 1;
    mnx /= ml; mny /= ml;
    var upSign = (mnx * lx + mny * ly) >= 0 ? 1 : -1;
    band(upSign * w * 0.5, Math.max(1.2, w * 0.36), lip, 0.95);"""


def main():
    tmp = Path(tempfile.mkdtemp(prefix="ribbon-taper-"))
    probe = tmp / "probe.js"
    probe.write_text(PROBE)

    now = ROOT / "assets" / "js" / "aksection.js"
    before = tmp / "aksection_before.js"
    # The pre-fix library is this one with the guard put back, which is the
    # single condition the fix changed. Reconstructing it from the shipped
    # file keeps the two versions identical in every other respect.
    src = now.read_text()
    old = src.replace("if (wasTwo || total / (pts.length - 1) > DENSE) {",
                      "if (total / (pts.length - 1) > DENSE) {")
    old = old.replace("Math.max(wasTwo ? MIN2 : 1, Math.ceil(segLen / DENSE))",
                      "Math.max(1, Math.ceil(segLen / DENSE))")
    # ...and with the per-segment lip put back to the path's mean normal,
    # which is the one line Codex's fourth round changed.
    old = old.replace("band(w * 0.5, Math.max(1.2, w * 0.36), lip, 0.95, true);",
                      MEAN_LIP)
    if old == src:
        print("  BAD  could not reconstruct the pre-fix guard; the code moved")
        return 1
    before.write_text(old)

    a_before = areas(before, probe)
    a_after = areas(now, probe)
    if a_before is None or a_after is None:
        return 1

    ok = True
    for name, want_zero_before in (("short2", True), ("tiny2", True),
                                   ("long2", False), ("many", False)):
        b, a = a_before[name], a_after[name]
        if want_zero_before:
            # "Zero" is floating-point zero: the degenerate polygon measures
            # about 4e-12 px squared, which is nothing on any raster.
            good = b < 1e-6 and a > 1.0
            expect = "no area before the fix (under 1e-6 px2) and a real mark after"
        else:
            good = b > 0 and abs(a - b) < 1e-9
            expect = "real area, unchanged by the fix"
        print("  %s   %-7s before=%.4g px2  after=%.4g px2   (%s)"
              % ("ok  " if good else "BAD ", name, b, a, expect))
        ok = ok and good

    for name, want_half_before in (("lip_rect", True), ("lip_open", False)):
        b, a = a_before[name], a_after[name]
        if want_half_before:
            good = b < 0.99 and a == 1.0
            expect = "not all lip vertices up-light before, all of them after"
        else:
            good = b == 1.0 and a == 1.0
            expect = "all lip vertices up-light before AND after"
        print("  %s   %-7s before=%.0f%%  after=%.0f%%   (%s)"
              % ("ok  " if good else "BAD ", name.replace("lip_", ""),
                 b * 100, a * 100, expect))
        ok = ok and good

    print("\ntwo-point ribbon taper and per-segment lip: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
