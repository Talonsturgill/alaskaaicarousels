#!/usr/bin/env python3
"""aksnow_verify.py -- the verification behind assets/js/aksnow.js.

Renders tests/aksnow_probe.html, which draws the OLD uniform-weight contour
hatch on the left half and AKSNOW.surface on the right half over the identical
contour, palette and region, then measures whether the new surface actually
beats the defect it replaces.

WHY MEASURE AT ALL. Run 2026-07-30 shipped a deck whose artwork-craft score was
6.0 for the ninth time in eleven runs, and the complaint from four pixel critics
and the scorer was that the snow read as "topographic contour lines" with "no
visible fall-line spacing variation, no two-part contact shadow and no specular
crest". A helper that only proved "something was drawn" would have passed the
thing it was written to fix.

WHICH FEATURES, AND WHY NOT detail_ratio.
The obvious move is to assert the new surface carries more fine detail than the
old one. That bar was tried first and it is WRONG, for two independent reasons,
and the wrongness is worth recording because it will look like an omission
otherwise.

  1. This repo already tested detail_ratio. scripts/craft_corpus.py measured it
     over 171 shipped slides against scorer-derived labels and got AUC 0.653
     with a Bonferroni-corrected p of 0.147, i.e. noise. Gating a craft upgrade
     on a feature the corpus says does not predict craft would be theatre.
  2. Mechanically, the old hatch WINS on ink. It draws ~50 full-width level
     strokes; the new surface draws tapered marks that stop. Requiring the
     replacement to out-ink the defect would push it back toward being a dense
     line field, which is precisely the thing being removed.

So this asserts the three things the design claim actually says, each of which
distinguishes carved snow from contour lines:

  edge_var        variance of gradient magnitude among edge pixels. The old
                  hatch uses two fixed line widths; the new marks taper along
                  their own length and scale with depth. This is the direct
                  measure of the rubric's own descriptor-4 phrase, "uniform
                  line weights".

  orient_spread   circular spread of local gradient ORIENTATION among edge
                  pixels. Every stroke in the old hatch is level, so its
                  gradients all point the same way. Sastrugi ridges here carry
                  +-9 degrees of per-ridge tilt about the fall line.

  low_band_range  the tonal RANGE surviving in the bottom third of the region.
                  This one was not planned; it fell out of the first calibration
                  and it turned out to measure the series' longest-running
                  defect directly. The old hatch's value ladder SATURATES at
                  about 60 percent depth and is then flat at L 0.145 for the
                  entire bottom third, which is precisely the "dead lower zone"
                  the scorer named in six consecutive runs. The replacement is
                  still descending at the frame edge. A surface that stops
                  having values before it stops being visible is the defect.

  pair_rate       the file's central claim, measured. A ridge is supposed to be
                  a LIT windward edge with a DARK lee edge just beneath it. For
                  each edge pixel this counts how often a bright sample sits a
                  few pixels above a darker one, normalised by edge count. A
                  single-stroke hatch produces these only by accident.

detail_ratio is still COMPUTED AND PRINTED, because it is informative even
though it does not gate. Reporting a number and refusing to threshold it is the
lesson the 2026-07-29 corpus study wrote down.

  python tests/aksnow_verify.py            # render + measure + assert
  python tests/aksnow_verify.py --keep     # leave the render for inspection

Exit 0 = the new surface wins on all four gated features. Exit 1 = it does not
and the upgrade should not ship. Exit 2 = the check could not look, which is a
failure too, not a pass.
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBE = ROOT / "tests" / "aksnow_probe.html"
RENDER = ROOT / ".claude" / "skills" / "carousel-engine" / "render.py"

# Margins set from the measured first calibration with room to spare, so
# ordinary seed noise cannot flip a verdict but a real regression will.
GATES = {"edge_var": 1.8, "orient_spread": 1.10, "pair_rate": 1.30,
         "low_band_range": 3.0}

# When the OLD value is essentially zero a ratio is meaningless (the first run
# printed a 74,000,000x "gain", which is a divide-by-zero dressed as a result).
# For those features the gate falls back to an absolute floor on the new value.
ABS_FLOOR = {"low_band_range": 0.03, "pair_rate": 0.05}
NEAR_ZERO = 1e-4


def _grads(a):
    gy, gx = np.gradient(a.astype(float))
    return gx, gy, np.hypot(gx, gy)


def _box(a, k):
    h, w = a.shape
    h, w = h - h % k, w - w % k
    return a[:h, :w].reshape(h // k, k, w // k, k).mean(axis=(1, 3))


def features(img, box):
    x0, y0, x1, y1 = box
    a = np.asarray(img.convert("L")).astype(float)[y0:y1, x0:x1] / 255.0
    gx, gy, mag = _grads(a)

    thr = np.percentile(mag, 88)
    m = mag > thr
    edges = mag[m]

    # gradient orientation is pi-periodic (an edge has no sign), so double the
    # angle before taking the circular mean, the standard axial-data treatment.
    ang2 = 2 * np.arctan2(gy[m], gx[m])
    R = np.hypot(np.cos(ang2).mean(), np.sin(ang2).mean()) if edges.size else 1.0
    orient_spread = float(1.0 - R)          # 0 = all one direction, 1 = isotropic

    # lit-above-dark pairing at ridge scale, the two-edge claim
    d = 5
    upper, lower = a[:-2 * d], a[2 * d:]
    band = mag[d:-d]
    sel = band > thr
    pair_rate = float((((upper - lower) > 0.045) & sel).sum() / max(1, sel.sum()))

    low = a[int(a.shape[0] * 0.66):]
    low_band_range = float(np.percentile(low, 92) - np.percentile(low, 8))

    coarse = _grads(_box(a, 4))[2]
    return {"low_band_range": low_band_range,
            "edge_var": float(edges.var()) if edges.size else 0.0,
            "orient_spread": orient_spread,
            "pair_rate": pair_rate,
            "detail_ratio": float(mag.mean() / max(1e-6, coarse.mean())),
            "mean_grad": float(mag.mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()

    if not PROBE.exists():
        print("aksnow_verify: missing", PROBE)
        return 2

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="aksnow-"))
    slides, out = tmp / "slides", tmp / "render"
    slides.mkdir()
    shutil.copy(PROBE, slides / "slide-01.html")
    r = subprocess.run([sys.executable, str(RENDER), "--slides-dir", str(slides),
                        "--out-dir", str(out)], capture_output=True, text=True)
    png = out / "slide-01.png"
    if r.returncode != 0 or not png.exists():
        print("aksnow_verify: render failed\n", r.stdout[-2000:], r.stderr[-1500:])
        return 2

    img = Image.open(png)
    W, H = img.size
    old = features(img, (int(W * 0.06), int(H * 0.32), int(W * 0.44), int(H * 0.95)))
    new = features(img, (int(W * 0.56), int(H * 0.32), int(W * 0.94), int(H * 0.95)))

    print("aksnow_verify -- old uniform hatch vs AKSNOW.surface, same contour\n")
    ok = True
    for k, need in GATES.items():
        if old[k] < NEAR_ZERO and k in ABS_FLOOR:
            floor = ABS_FLOOR[k]
            good = new[k] >= floor
            print("  %-14s old ~0 (%.6f)  new %.6f   floor %.3f  %s"
                  % (k, old[k], new[k], floor, "OK" if good else "FAIL"))
        else:
            gain = new[k] / max(1e-9, old[k])
            good = gain >= need
            print("  %-14s old %.6f   new %.6f   gain %5.2fx  need %.2fx  %s"
                  % (k, old[k], new[k], gain, need, "OK" if good else "FAIL"))
        ok = ok and good
    print("\n  reported, NOT gated (corpus AUC 0.653, see module docstring):")
    print("  %-14s old %.4f   new %.4f" % ("detail_ratio", old["detail_ratio"],
                                           new["detail_ratio"]))
    print("  %-14s old %.5f   new %.5f" % ("mean_grad", old["mean_grad"],
                                           new["mean_grad"]))

    if args.keep:
        keep = ROOT / "out" / "aksnow_probe.png"
        keep.parent.mkdir(exist_ok=True)
        shutil.copy(png, keep)
        print("  kept ->", keep)
    else:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nverdict:", "PASS" if ok else "FAIL")
    print(json.dumps({"old": old, "new": new}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
