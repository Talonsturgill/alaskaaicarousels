#!/usr/bin/env python3
"""aksnow_recede_verify.py -- the verification behind AKSNOW.surface's
`nearEdge: 'bottom'` option (assets/js/aksnow.js, receding()).

THE DEFECT. AKSNOW.surface was written for a drift seen from above: its crest
(the `top` contour) is the NEAR edge, so the lit end of the value ladder, the
heaviest ridges and the specular glints all sit at the TOP of the region. Run
No.71 (2026-09-28) laid it on two floors that recede UP the frame to a horizon,
slides 04 and 05. There the top of the region is the FAR edge, so the floor lit
backwards, and the strobe's multiply falloff (brightest near the camera, at the
bottom) cancelled the ladder to flat grey. The slides were rescued by drawing
the surface offscreen and painting that canvas flipped (TECHNIQUE_LIBRARY 106).
This test holds the native option to the numbers that rescue produced.

It runs AKSNOW in the engine's own browser (render.launch_chromium) on four
canvases of one receding floor, 360 x 1020, each finished with the same
multiply falloff the slides use (white at the bottom, dark at the far edge):

  flip       the No.71 workaround: offscreen surface, painted scale(1, -1)
  native     AKSNOW.surface(..., nearEdge: 'bottom')
  default    AKSNOW.surface with no nearEdge: THE DEFECT, reconstructed
  top        AKSNOW.surface with nearEdge: 'top' said out loud

and asserts:

  1. native reproduces flip: mean |dL| under 0.004 over the floor and the
     row-mean luminance profiles correlate above 0.999.
  2. native reads near-lit: bottom third minus top third L above 0.25, and
     the floor's p92-p8 tonal range above 0.40.
  3. THE DEFECT FAILS assertion 2 (default near-far under 0.10 or range under
     0.40), so the test can tell the two apart. With the pre-upgrade aksnow.js,
     which ignores nearEdge, `native` IS `default` and this test FAILS.
  4. nearEdge 'top' is byte-identical to no nearEdge, so every existing caller
     is untouched.
  5. On a CURVED far edge the receding surface paints nothing above top(x)
     (the clip) and covers the region below it.
  6. Any other nearEdge value throws, rather than silently drawing a default.

  python3 tests/aksnow_recede_verify.py
  python3 tests/aksnow_recede_verify.py --aksnow /path/to/old/aksnow.js   # the red case

Exit 0 = all hold. Exit 1 = a claim failed. Exit 2 = could not look.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

PAGE_JS = r"""
() => {
  const W = 360, H = 1020;
  const OPT = {x0: 0, x1: W, lit: '#E4EAF1', shadow: '#1B2A36', seed: 20260928 + 4,
               bands: 60, gamma: 0.9, lightDeg: 60, windDeg: 190, ridges: 60,
               weightNear: 2.4, weightFar: 0.5, alphaScale: 0.55};
  function canvas() { const c = document.createElement('canvas'); c.width = W; c.height = H;
                      return [c, c.getContext('2d')]; }
  function opts(extra) { return Object.assign({}, OPT, extra); }
  function falloff(cx) {        /* the slides' strobe pool: brightest near, at the bottom */
    cx.save(); cx.globalCompositeOperation = 'multiply';
    const g = cx.createRadialGradient(W * 0.4, H * 1.1, 40, W * 0.4, H * 1.1, H * 0.95);
    g.addColorStop(0, '#FFFFFF'); g.addColorStop(0.4, '#A4B0BC');
    g.addColorStop(0.8, '#39434F'); g.addColorStop(1, '#10171F');
    cx.fillStyle = g; cx.fillRect(0, 0, W, H); cx.restore();
  }
  function lum(cx) {
    const d = cx.getImageData(0, 0, W, H).data, L = new Float32Array(W * H);
    for (let i = 0; i < W * H; i++) {
      L[i] = (0.299 * d[4 * i] + 0.587 * d[4 * i + 1] + 0.114 * d[4 * i + 2]) / 255;
    }
    return Array.from(L);
  }
  const out = {};
  let c, cx;
  /* flip: the No.71 workaround */
  [c, cx] = canvas();
  const [oc, ox] = canvas();
  AKSNOW.surface(ox, opts({top: x => 0, bottom: H}));
  cx.save(); cx.translate(0, H); cx.scale(1, -1); cx.drawImage(oc, 0, 0); cx.restore();
  falloff(cx); out.flip = lum(cx);
  /* native */
  [c, cx] = canvas();
  const sn = AKSNOW.surface(cx, opts({top: x => 0, bottom: H, nearEdge: 'bottom'}));
  falloff(cx); out.native = lum(cx); out.nativeStats = sn;
  /* default: the defect */
  [c, cx] = canvas();
  const sd = AKSNOW.surface(cx, opts({top: x => 0, bottom: H}));
  falloff(cx); out.default = lum(cx); out.defaultStats = sd;
  /* explicit 'top' vs absent, byte for byte */
  const [c1, x1] = canvas(), [c2, x2] = canvas();
  AKSNOW.surface(x1, opts({top: x => 40 + 20 * Math.sin(x * 0.02), bottom: H}));
  AKSNOW.surface(x2, opts({top: x => 40 + 20 * Math.sin(x * 0.02), bottom: H, nearEdge: 'top'}));
  const a = x1.getImageData(0, 0, W, H).data, b = x2.getImageData(0, 0, W, H).data;
  let diff = 0; for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) diff++;
  out.topBytesDiffer = diff;
  /* curved far edge: the clip */
  const crest = x => 300 + 90 * Math.sin(x * 0.017);
  [c, cx] = canvas();
  AKSNOW.surface(cx, opts({top: crest, bottom: H, nearEdge: 'bottom'}));
  const cd = cx.getImageData(0, 0, W, H).data;
  let above = 0, aboveN = 0, below = 0, belowN = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const al = cd[4 * (y * W + x) + 3], t = crest(x);
    if (y + 0.5 < t - 2) { aboveN++; if (al > 0) above++; }   /* pixel centre over 2 px above: past any AA fringe */
    else if (y + 0.5 > t + 2 && y < H - 2) { belowN++; if (al === 255) below++; }
  }
  out.clip = {paintedAbove: above, aboveN: aboveN, coveredBelow: below / Math.max(1, belowN)};
  /* curved far edge keeps the FAR treatment along its whole length (Codex, PR #407): the band just
     under the edge at the low columns must read like the band under the peaks, not partway to near */
  let lowS = 0, lowN = 0, peakS = 0, peakN = 0;
  for (let x = 0; x < W; x++) {
    const t = Math.ceil(crest(x)) + 3;
    for (let y = t; y < t + 14 && y < H; y++) {
      const i = 4 * (y * W + x), l = (0.2126 * cd[i] + 0.7152 * cd[i + 1] + 0.0722 * cd[i + 2]) / 255;
      if (crest(x) > 370) { lowS += l; lowN++; } else if (crest(x) < 230) { peakS += l; peakN++; }
    }
  }
  out.edgeBand = {low: lowS / Math.max(1, lowN), peak: peakS / Math.max(1, peakN), lowN: lowN, peakN: peakN};
  /* a STEEP contour, a large change inside one 4 px strip (Codex, PR #407): the band under the edge must
     still read as far, not start partway down the ladder where the contour climbs within a strip */
  const steep = x => 400 + 200 * Math.sin(x * 0.8);
  [c, cx] = canvas();
  AKSNOW.surface(cx, opts({top: steep, bottom: H, nearEdge: 'bottom'}));
  const sd2 = cx.getImageData(0, 0, W, H).data;
  let stS = 0, stN = 0;
  for (let x = 0; x < W; x++) {
    const t = Math.ceil(steep(x)) + 3;
    for (let y = t; y < t + 14 && y < H; y++) {
      const i = 4 * (y * W + x); stS += (0.2126 * sd2[i] + 0.7152 * sd2[i + 1] + 0.0722 * sd2[i + 2]) / 255; stN++;
    }
  }
  out.steepBand = stS / Math.max(1, stN);
  /* a contour that returns the SAME value at every `step` probe (Codex, PR #407) must still be warped */
  const hidden = x => 400 + 100 * Math.sin(2 * Math.PI * x / 4);
  [c, cx] = canvas();
  const hs = AKSNOW.surface(cx, opts({top: hidden, bottom: H, nearEdge: 'bottom'}));
  const hd = cx.getImageData(0, 0, W, H).data;
  let hAbove = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++)
    /* the pixel grid is the finest a canvas clip can trace: judge against the contour's pixel-resolution
       polyline (its value midway between the two integer columns), not between them */
    if (y + 0.5 < Math.min(hidden(x), hidden(x + 1)) - 2 && hd[4 * (y * W + x) + 3] > 0) hAbove++;
  out.hidden = {warped: !!hs.warped, paintedAbove: hAbove};
  /* a bad value throws */
  try { AKSNOW.surface(cx, opts({top: x => 0, bottom: H, nearEdge: 'left'})); out.badThrows = false; }
  catch (e) { out.badThrows = e instanceof TypeError; }
  out.W = W; out.H = H;
  return out;
}
"""


def measure(L, W, H):
    import numpy as np
    a = np.asarray(L, dtype=float).reshape(H, W)
    t = H // 3
    return a, {"far": float(a[:t].mean()), "near": float(a[-t:].mean()),
               "near_minus_far": float(a[-t:].mean() - a[:t].mean()),
               "range": float(np.percentile(a, 92) - np.percentile(a, 8))}


def near_lit(m):
    return m["near_minus_far"] > 0.25 and m["range"] > 0.40


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aksnow", default=str(ROOT / "assets" / "js" / "aksnow.js"))
    args = ap.parse_args()
    try:
        import numpy as np
        from playwright.sync_api import sync_playwright
        from render import launch_chromium
    except Exception as e:                                   # noqa: BLE001
        print("aksnow_recede_verify: could not load the harness:", e)
        return 2
    noise = (ROOT / "assets" / "js" / "noise.js").read_text()
    snow = Path(args.aksnow).read_text()
    try:
        with sync_playwright() as p:
            b = launch_chromium(p)
            pg = b.new_page()
            pg.set_content("<!doctype html><html><body></body></html>")
            pg.add_script_tag(content=noise)
            pg.add_script_tag(content=snow)
            r = pg.evaluate(PAGE_JS)
            b.close()
    except Exception as e:                                   # noqa: BLE001
        print("aksnow_recede_verify: could not look:", str(e)[:600])
        return 2

    W, H = r["W"], r["H"]
    fa, mf = measure(r["flip"], W, H)
    na, mn = measure(r["native"], W, H)
    da, md = measure(r["default"], W, H)
    dl = np.abs(fa - na)
    corr = float(np.corrcoef(fa.mean(1), na.mean(1))[0, 1])
    ok = True

    def row(name, good, detail):
        nonlocal ok
        ok = ok and good
        print("  %-4s %-44s %s" % ("OK" if good else "FAIL", name, detail))

    print("aksnow_recede_verify -- nearEdge 'bottom' against the No.71 flip, %dx%d floor\n" % (W, H))
    for k, m in (("flip", mf), ("native", mn), ("default", md)):
        print("  %-8s far L %.3f  near L %.3f  near-far %+.3f  range %.3f"
              % (k, m["far"], m["near"], m["near_minus_far"], m["range"]))
    print()
    row("1 native reproduces the flip", dl.mean() < 0.004 and corr > 0.999,
        "mean|dL| %.5f  max %.3f  row-profile corr %.5f" % (dl.mean(), dl.max(), corr))
    row("2 native reads near-lit", near_lit(mn),
        "near-far %+.3f (> 0.25)  range %.3f (> 0.40)" % (mn["near_minus_far"], mn["range"]))
    row("3 the defect (no nearEdge) fails check 2", not near_lit(md),
        "near-far %+.3f  range %.3f" % (md["near_minus_far"], md["range"]))
    row("4 nearEdge 'top' byte-identical to absent", r["topBytesDiffer"] == 0,
        "%d bytes differ" % r["topBytesDiffer"])
    c = r["clip"]
    row("5 curved far edge: clipped and covered",
        c["paintedAbove"] == 0 and c["coveredBelow"] > 0.99 and c["aboveN"] > 1000,
        "painted above top(x) %d of %d px; covered below %.4f"
        % (c["paintedAbove"], c["aboveN"], c["coveredBelow"]))
    e = r["edgeBand"]
    row("8 curved far edge keeps the far treatment", abs(e["low"] - e["peak"]) < 0.06 and e["lowN"] > 500 and e["peakN"] > 500,
        "L under the edge: low columns %.3f, peak columns %.3f" % (e["low"], e["peak"]))
    row("9 a steep contour keeps the far treatment", r["steepBand"] - e["peak"] < 0.06,
        "L under the steep edge %.3f vs %.3f under the gentle peaks" % (r["steepBand"], e["peak"]))
    hz = r["hidden"]
    row("10 a curve between step probes is still warped", hz["warped"] and hz["paintedAbove"] == 0,
        "warped %s, painted above top(x) %d px" % (hz["warped"], hz["paintedAbove"]))
    row("6 an unknown nearEdge throws", r["badThrows"] is True, str(r["badThrows"]))
    sn, sd = r["nativeStats"], r["defaultStats"]
    same = all(sn.get(k) == sd.get(k) for k in ("ridges", "weightMin", "weightMax", "weightVar"))
    row("7 same marks, mirrored (stats match default)", same and sn.get("nearEdge") == "bottom",
        json.dumps({k: sn.get(k) for k in ("ridges", "weightVar", "nearEdge")}))
    print("\nverdict:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
