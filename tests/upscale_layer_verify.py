#!/usr/bin/env python3
"""upscale_layer_verify.py -- the reconstruction behind qa.py's 2026-10-25
per-pixel-layer-magnified check (render.py UPSCALE_HOOK_JS).

THE DEFECT. Run No.96's deck helper shaded its North Slope relief per pixel
into a 1080 x 1350 ImageData, put it on a 1x offscreen canvas and drew that
into the 2x frame canvas at (0, 0, 1080, 1350). Every computed pixel printed as
a smoothed 2 x 2 block, and pixel rounds 1 to 3 named upscale blur and
stair-steps on six terrain frames. qa.py FAILs a canvas ELEMENT under 1.5x
backing; a 1x layer drawn into a 2x element passed everything.

THE FIXTURES, one per slide:

  1. hillshade at 1x, drawn up to the 2x canvas          -> WARNS
  2. the same hillshade computed per device pixel         -> clean
  3. a smooth fog ramp at 1x, drawn up                     -> clean (nothing to lose)
  4. hillshade at 1x, copied 1:1 to a second 1x canvas,
     and that one drawn up                                 -> WARNS (mark carried)
  5. hillshade at 1x drawn up into a small inset (6%)      -> clean (below the share floor)

The clean variants prove the check is not firing on every putImageData or on
every magnified draw; 2 is the repair No.96 shipped.

Usage: python tests/upscale_layer_verify.py   (exit 0 = all five hold)
Renders with the engine's own render.py and judges with its own qa.py. No
network. Writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENGINE = REPO / ".claude" / "skills" / "carousel-engine"
NEEDLE = "per-pixel layer drawn up"

HEAD = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; background:#0A1018; }
  canvas { position:absolute; left:0; top:0; width:1080px; height:1350px; }
  h1 { position:absolute; left:80px; top:1150px; font:600 64px sans-serif; color:#F4F8FF; }
</style></head><body>
<canvas id="c" width="2160" height="2700"></canvas>
<h1>Relief fixture</h1>
<script>
function hh(a, b) { var q = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return q - Math.floor(q); }
function vn(x, y) {
  var i = Math.floor(x), j = Math.floor(y), u = x - i, v = y - j;
  u = u * u * (3 - 2 * u); v = v * v * (3 - 2 * v);
  return (hh(i, j) * (1 - u) + hh(i + 1, j) * u) * (1 - v) + (hh(i, j + 1) * (1 - u) + hh(i + 1, j + 1) * u) * v;
}
function height(x, y) {            /* design px in, metres-ish out */
  var s = 0, a = 1, f = 1 / 90;
  for (var o = 0; o < 6; o++) { s += a * vn(x * f, y * f); a *= 0.5; f *= 2.03; }
  return s * 900;
}
/* a hillshade into a W x H ImageData, k device px per design px */
function shade(W, H, k, smooth) {
  var g = document.createElement('canvas'); g.width = W; g.height = H;
  var x = g.getContext('2d'), img = x.createImageData(W, H), d = img.data;
  for (var j = 0; j < H; j++) for (var i = 0; i < W; i++) {
    var px = i / k, py = j / k, l;
    if (smooth) l = 40 + 60 * Math.exp(-((px - 540) * (px - 540) + (py - 500) * (py - 500)) / 2.2e5);
    else {
      var e = 0.5 / k, dx = (height(px + e, py) - height(px - e, py)) / (2 * e);
      var dy = (height(px, py + e) - height(px, py - e)) / (2 * e);
      var n = 1 / Math.hypot(dx, dy, 1), lit = Math.max(0, (-dx * -0.5 + -dy * -0.6 + 0.62) * n);
      l = 20 + 200 * lit;
    }
    var q = (j * W + i) * 4; d[q] = l * 0.8; d[q + 1] = l * 0.9; d[q + 2] = l; d[q + 3] = 255;
  }
  x.putImageData(img, 0, 0);
  return g;
}
var cx = document.getElementById('c').getContext('2d');
cx.scale(2, 2);
"""

TAIL = "</script></body></html>\n"

CASES = [
    ("hillshade at 1x drawn up to 2x", True,
     "cx.drawImage(shade(1080, 1350, 1), 0, 0, 1080, 1350);\n"),
    ("hillshade per device pixel (the repair)", False,
     "cx.setTransform(1, 0, 0, 1, 0, 0); cx.drawImage(shade(2160, 2700, 2), 0, 0);\n"),
    ("smooth fog ramp at 1x drawn up", False,
     "cx.drawImage(shade(1080, 1350, 1, true), 0, 0, 1080, 1350);\n"),
    ("hillshade at 1x, copied 1:1, then drawn up", True,
     "var a = shade(1080, 1350, 1), b = document.createElement('canvas');\n"
     "b.width = 1080; b.height = 1350; b.getContext('2d').drawImage(a, 0, 0);\n"
     "cx.drawImage(b, 0, 0, 1080, 1350);\n"),
    ("hillshade at 1x in a 6 percent inset", False,
     "cx.fillStyle = '#26303A'; cx.fillRect(0, 0, 1080, 1350);\n"
     "cx.drawImage(shade(1080, 1350, 1), 0, 0, 1080, 1350, 700, 120, 260, 325);\n"),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="upscale_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, _w, body) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(HEAD + body + TAIL)
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, should_warn, _b) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None:
            ok = False
            print("[BROKE] %-46s -> slide never rendered" % name)
            continue
        hits = [w for w in s["warns"] + s["fails"] if NEEDLE in w]
        good = bool(hits) if should_warn else not hits
        ok &= good
        print("[%s] %-46s -> %s" % ("HOLD" if good else "BROKE", name,
                                    hits[0][:150] if hits else "clean"))
    print("upscale_layer_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
