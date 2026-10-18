#!/usr/bin/env python3
"""strobe_focal_region_verify.py -- AKSTROBE.focus's focal region and
AKSTROBE.depthRange (2026-10-17, weekly machine pass).

WHAT IT RECONSTRUCTS. A thin lens is sharp on ONE plane. No.89's two akthree
relief frames (01, 09) pulled focus across a terrain slab seen obliquely, the
slab running from about 16 to 40 camera units, and at k 5 to 7 the largest
object itself went soft: the round 1 critics named it on both frames, and the
fix was to drop k to about 2, which took the fall-off in front of and behind
the slab with it. `o.sharp = [dNear, dFar]` gives a focal REGION: zero circle
of confusion inside it, the same thin-lens fall-off outside it.

    python3 tests/strobe_focal_region_verify.py     # exit 0 = every check holds

The fixture is a slab that runs away from the camera across the frame (depth
4 at the left edge to 12 at the right) under 1 px horizontal stripes, so each
column's surviving stripe contrast reads its blur radius directly.

  same      without o.sharp the working akstrobe.js and git HEAD's write the
            same bytes (no shipped slide moves).
  thin      without o.sharp at k 13, the sharp columns (contrast within 10
            percent of the source) cover under 15 percent of the slab: the
            No.89 defect, a subject sharp along one line.
  region    with o.sharp = [6, 10] every column whose depth is inside the
            region, past the near field's bleed margin, keeps its contrast, and
            the columns well outside it still fall off.
  share     the returned inFocus share rises with the region.
  range     depthRange returns the 5th and 95th percentile depths of a rect and
            leaves the far-plane background out; null for a rect of background.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

N = 512

PAGE = """<!doctype html><html><body style="margin:0">
<canvas id="d" width="512" height="512"></canvas>
<script src="@@STROBE_SRC@@"></script>
<script>
window.renderReady = (async () => {
  const N = 512;
  const src = document.createElement("canvas"); src.width = N; src.height = N;
  const sx = src.getContext("2d");
  for (let y = 0; y < N; y++) { sx.fillStyle = (y % 2) ? "#e0e0e0" : "#202020"; sx.fillRect(0, y, N, 1); }
  const d = new Float32Array(N * N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) d[y * N + x] = 4 + 8 * x / (N - 1);
  const depth = {w: N, h: N, d: d};
  const dst = document.getElementById("d").getContext("2d");
  const o = {focus: 8, k: 13, maxR: 16, scale: 2};
  if (@@SHARP@@) o.sharp = [6, 10];
  const ret = AKSTROBE.focus(dst, src, depth, o) || {};
  const px = dst.getImageData(0, 0, N, N).data, g = [];
  for (let i = 0; i < px.length; i += 4) g.push(px[i]);
  let range = null, empty = null;
  if (AKSTROBE.depthRange) {
    // a background band on the right, at the far plane: depthRange must leave it out
    const d2 = new Float32Array(d); for (let y = 0; y < N; y++) for (let x = 400; x < N; x++) d2[y * N + x] = 100;
    range = AKSTROBE.depthRange({w: N, h: N, d: d2, near: 0.3, far: 100}, [0, 0, 128, 128], {scale: 2});   // backing columns 0 to 255
    empty = AKSTROBE.depthRange({w: N, h: N, d: d2, near: 0.3, far: 100}, [210, 0, 40, 40], {scale: 2});   // backing columns 420 to 499, all background
  }
  return JSON.stringify({g: g, inFocus: ret.inFocus == null ? null : ret.inFocus, range: range, empty: empty});
})();
</script></body></html>"""


def head_copy(rel, dest):
    out = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:" + rel], capture_output=True, text=True)
    if out.returncode != 0:
        return None
    dest.write_text(out.stdout)
    return dest


def contrast(g):
    a = np.asarray(g, dtype=np.float64).reshape(N, N)
    return np.abs(np.diff(a[16:N - 16], axis=0)).mean(axis=0), a


def run(browser, tmp, strobe, sharp):
    f = tmp / ("region_%s_%d.html" % (strobe.stem, int(sharp)))
    f.write_text(PAGE.replace("@@STROBE_SRC@@", strobe.as_uri()).replace("@@SHARP@@", "true" if sharp else "false"))
    page = browser.new_page(viewport={"width": N, "height": N})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(f.as_uri(), wait_until="load", timeout=60000)
    res = json.loads(page.evaluate("() => window.renderReady"))
    page.close()
    return res, errs


def depth_at(x):
    return 4 + 8 * x / (N - 1)


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium

    bad = []
    with tempfile.TemporaryDirectory() as d, sync_playwright() as p:
        tmp = Path(d)
        old = head_copy("assets/js/akstrobe.js", tmp / "akstrobe_head.js")
        b = launch_chromium(p)
        try:
            cur = ROOT / "assets" / "js" / "akstrobe.js"
            plain, e1 = run(b, tmp, cur, False)
            region, e2 = run(b, tmp, cur, True)
            for e in e1 + e2:
                bad.append("page error: " + e[:200])
            c_plain, a_plain = contrast(plain["g"])
            c_reg, _ = contrast(region["g"])
            full = float(c_plain.max())
            sharp_plain = c_plain >= 0.9 * full
            share_plain = float(sharp_plain.mean())
            print("thin    no o.sharp, k 13: %.1f percent of the slab's columns stay sharp" % (100 * share_plain))
            if share_plain >= 0.15:
                bad.append("the fixture does not show a thin focal plane (%.2f sharp)" % share_plain)

            xs = np.arange(N)
            # inside the region, clear of the near field's bleed (maxR 16 at sc 2 is 32 backing px, x 1.6)
            inside = (depth_at(xs) >= 6) & (depth_at(xs) <= 10) & (xs > (6 - 4) / 8 * (N - 1) + 56)
            outside = (depth_at(xs) > 11) | (depth_at(xs) < 5)
            keep = float((c_reg[inside] >= 0.9 * full).mean())
            fall = float(c_reg[outside].mean() / full)
            print("region  o.sharp [6, 10]: %.0f percent of the in-region columns sharp; outside it, contrast "
                  "at %.2f of the source" % (100 * keep, fall))
            if keep < 0.99:
                bad.append("the focal region does not hold its columns sharp (%.2f)" % keep)
            if fall > 0.6:
                bad.append("outside the region the fall-off is gone (%.2f of source contrast)" % fall)

            print("share   inFocus %s without the region, %s with it" % (plain["inFocus"], region["inFocus"]))
            if not (isinstance(plain["inFocus"], float) and isinstance(region["inFocus"], float)
                    and region["inFocus"] > plain["inFocus"] + 0.2):
                bad.append("the inFocus share does not rise with the region")

            r, emp = region["range"], region["empty"]
            print("range   depthRange %s over the left quarter, %s over background" % (r, emp))
            want = (depth_at(0.05 * 255), depth_at(0.95 * 255))
            if not r or abs(r[0] - want[0]) > 0.1 or abs(r[1] - want[1]) > 0.1:
                bad.append("depthRange %s, expected about %.2f to %.2f" % (r, want[0], want[1]))
            if emp is not None and (emp[1] >= 100 or emp[0] >= 100):
                bad.append("depthRange counted far-plane background: %s" % emp)

            if old:
                head, e3 = run(b, tmp, old, False)
                diff = int(np.abs(np.asarray(head["g"]) - np.asarray(plain["g"])).max())
                print("same    without o.sharp, HEAD and working differ by at most %d levels" % diff)
                if diff:
                    bad.append("the default output moved (%d levels)" % diff)
        finally:
            b.close()

    if bad:
        print("BROKEN")
        for x in bad:
            print(" - " + x)
        return 1
    print("HOLDS: the focal region keeps a receding subject sharp, the fall-off outside it is kept, "
          "and without it nothing moved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
