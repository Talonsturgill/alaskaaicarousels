#!/usr/bin/env python3
"""strobe_focus_cells_verify.py -- AKSTROBE.focus reads its near-field map
smoothly (2026-10-11, weekly machine pass).

WHAT IT RECONSTRUCTS. AKSTROBE.focus max-pools the foreground circle of
confusion into 4 x 4 backing-pixel cells, blurs that small map, and used to read
it back by NEAREST cell (x >> 2). Where a defocused foreground bleeds over the
sharp plane behind it, the bleed radius then stepped every 4 px and the
gathered blur printed a 4 px cell grid. No.84 slide 07 used it, and after the
grain tile was fixed one critic still named a regular lattice there. The read
is now bilinear between cell centres; the cells themselves are unchanged.

    python3 tests/strobe_focus_cells_verify.py     # exit 0 = every check holds

The fixture: a source of horizontal 1 px stripes (so the local blur radius is
read straight off the stripe contrast of each column), a near object over the
left of the frame, and the sharp plane to its right. Across the bleed band the
stripe contrast must fall SMOOTHLY: the share of its column-to-column change
that lands on a 4 px cell boundary is about 1 for a stepped read and about 0.25
for a smooth one.

  defect    the committed (git HEAD) akstrobe.js, if it still reads by nearest
            cell, puts 0.8 or more of the change on cell boundaries.
  smooth    the working akstrobe.js puts under 0.5 there.
  same      outside the bleed band (deep in the near object, and far into the
            sharp plane) the two versions agree within 1 level.
"""

import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

STEPPED_MIN = 0.8
SMOOTH_MAX = 0.5
N = 512            # backing px, square
EDGE = 200         # the near object covers x < EDGE

PAGE = """<!doctype html><html><body style="margin:0">
<canvas id="d" width="512" height="512"></canvas>
<script src="@@STROBE_SRC@@"></script>
<script>
window.renderReady = (async () => {
  const N = 512, EDGE = 200;
  const src = document.createElement("canvas"); src.width = N; src.height = N;
  const sx = src.getContext("2d");
  for (let y = 0; y < N; y++) { sx.fillStyle = (y % 2) ? "#e0e0e0" : "#202020"; sx.fillRect(0, y, N, 1); }
  const d = new Float32Array(N * N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) d[y * N + x] = x < EDGE ? 1.0 : 6.0;
  const dst = document.getElementById("d").getContext("2d");
  AKSTROBE.focus(dst, src, {w: N, h: N, d: d}, {focus: 6.0, k: 13, maxR: 16, scale: 2});
  const px = dst.getImageData(0, 0, N, N).data, g = [];
  for (let i = 0; i < px.length; i += 4) g.push(px[i]);
  return JSON.stringify(g);
})();
</script></body></html>"""


def head_copy(rel, dest):
    out = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:" + rel],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    dest.write_text(out.stdout)
    return dest


def contrast_profile(g):
    """Per column, the mean absolute difference between neighbouring rows:
    the stripes' surviving contrast, which falls as the blur radius rises."""
    a = np.asarray(g, dtype=np.float64).reshape(N, N)
    return np.abs(np.diff(a[16:N - 16], axis=0)).mean(axis=0), a


def boundary_share(c):
    """Share of the bleed band's total column-to-column change that falls
    between two 4 px cells (x = 4k-1 to 4k)."""
    lo, hi = EDGE + 2, EDGE + 60
    dx = np.abs(np.diff(c[lo:hi]))
    xs = np.arange(lo, hi - 1)
    at = (xs + 1) % 4 == 0
    tot = dx.sum()
    return (float(dx[at].sum() / tot) if tot > 0 else 0.0), float(tot)


def run(browser, tmp, strobe):
    f = tmp / ("focus_%s.html" % strobe.stem)
    f.write_text(PAGE.replace("@@STROBE_SRC@@", strobe.as_uri()))
    page = browser.new_page(viewport={"width": 512, "height": 512})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(f.as_uri(), wait_until="load", timeout=60000)
    res = json.loads(page.evaluate("() => window.renderReady"))
    page.close()
    return res, errs


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium

    bad = []
    with tempfile.TemporaryDirectory() as d, sync_playwright() as p:
        tmp = Path(d)
        old = head_copy("assets/js/akstrobe.js", tmp / "akstrobe_head.js")
        b = launch_chromium(p)
        try:
            new_g, e1 = run(b, tmp, ROOT / "assets" / "js" / "akstrobe.js")
            c_new, a_new = contrast_profile(new_g)
            s_new, t_new = boundary_share(c_new)
            print("working akstrobe.js: %.2f of the bleed band's change on cell "
                  "boundaries (total %.1f)" % (s_new, t_new))
            if t_new < 5:
                bad.append("the fixture shows no bleed band (total change %.1f)" % t_new)
            if s_new >= SMOOTH_MAX:
                bad.append("the near-field read is still stepped: %.2f of the change "
                           "on 4 px cell boundaries" % s_new)
            if e1:
                bad.append("page error: %s" % e1[0][:200])
            if old:
                old_g, e2 = run(b, tmp, old)
                c_old, a_old = contrast_profile(old_g)
                s_old, _ = boundary_share(c_old)
                stepped = "(y >> 2) * nb.width) + (x >> 2)" in old.read_text()
                print("committed akstrobe.js: %.2f on cell boundaries%s"
                      % (s_old, " (nearest-cell read)" if stepped else ""))
                if stepped and s_old < STEPPED_MIN:
                    bad.append("the committed nearest-cell read measures %.2f: the "
                               "fixture would not catch the defect" % s_old)
                for lo, hi, where in ((8, EDGE - 40, "deep in the near object"),
                                      (EDGE + 120, N - 8, "far into the sharp plane")):
                    dmax = np.abs(a_new[:, lo:hi] - a_old[:, lo:hi]).max()
                    if dmax > 1:
                        bad.append("%s the two versions differ by %.0f levels" % (where, dmax))
        finally:
            b.close()

    if bad:
        print("BROKEN")
        for x in bad:
            print(" - " + x)
        return 1
    print("HOLDS: the near-field bleed falls smoothly across the 4 px cells, and "
          "away from the bleed band nothing moved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
