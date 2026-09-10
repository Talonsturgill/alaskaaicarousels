#!/usr/bin/env python3
"""reserve_punch_verify.py -- the reconstruction behind AKENGRAVE.punchReserves
and qa.py's 2026-09-10 radial-punch fingerprint. One defect from run No.55, two
fixtures, one drawing.

THE DEFECT. The house reserves type out of a field by drawing the field
offscreen and punching the measured boxes back out with destination-out. The
idiom shipped with a RADIAL gradient, and a radial punch cannot reserve a long
box: its outer radius is half the box's longest side, so on a 900px line of type
the circle has faded to nothing well before the ends of the line. The middle of
the headline is cleanly reserved and the field stays over the first and last
words. qa.py measured it correctly, as a worst-point contrast failure against a
healthy box mean, and described it as a graded ground -- "give it a reserve or
move it", which is the repair that was already there. Run No.55's slide 08
carried two of these findings and both died on one change.

THE FIXTURES, the same field and the same headline in both:

  1. punched with a radial gradient   -> FAILS, and now names the radial punch
  2. punched with AKENGRAVE.punchReserves -> clean, the whole line is reserved

Fixture 2 is also the helper's own proof: it runs the committed asset in
Chromium against measured [data-reserve] boxes.

Usage: python tests/reserve_punch_verify.py   (exit 0 = both hold)
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

SLIDE = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#10141A; font-family:"Space Grotesk", sans-serif;
         position:relative; }
  canvas { position:absolute; inset:0; z-index:0; }
  h1 { position:absolute; left:90px; top:600px; width:900px; z-index:1;
       font-size:54px; font-weight:640; line-height:1.05; color:#F2ECDF; }
</style></head><body>
<canvas id="c" width="2160" height="2700" style="width:1080px;height:1350px"></canvas>
<h1 data-reserve>One agenda, two items, one vote at the end of it</h1>
<script src="@@ASSETS@@/js/akengrave.js"></script>
<script>
window.renderReady = (async () => {
  await document.fonts.ready;
  const cx = document.getElementById('c').getContext('2d');
  cx.scale(2, 2);
  const W = 1080, H = 1350;
  const boxes = AKENGRAVE.boxesFor('[data-reserve]', {padBody: 8});

  /* the field: a bright lay across the headline's band, drawn offscreen */
  const off = AKENGRAVE.drawOffscreen(2160, 2700, (g) => {
    g.save(); g.scale(2, 2);          /* restored below: the punch re-scales */
    g.fillStyle = 'rgba(236,229,208,0.92)';
    g.fillRect(60, 560, 960, 200);
    g.strokeStyle = 'rgba(120,108,84,0.5)';
    g.lineWidth = 1.5;
    for (let y = 566; y < 760; y += 7) {
      g.beginPath(); g.moveTo(60, y); g.lineTo(1020, y); g.stroke();
    }
    g.restore();
  });
  const og = off.getContext('2d');
  og.save(); og.scale(2, 2);
  %s
  og.restore();
  cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
  cx.drawImage(off, 0, 0); cx.restore();
  return true;
})();
</script>
</body></html>
"""

RADIAL = """
  /* THE DEFECT: a radial punch, outer radius half the box's longest side */
  og.globalCompositeOperation = 'destination-out';
  boxes.forEach(function (b) {
    const g2 = og.createRadialGradient(b[0]+b[2]/2, b[1]+b[3]/2, 0,
                                       b[0]+b[2]/2, b[1]+b[3]/2,
                                       Math.max(b[2], b[3])/2 + 22);
    g2.addColorStop(0, 'rgba(0,0,0,1)');
    g2.addColorStop(0.74, 'rgba(0,0,0,1)');
    g2.addColorStop(1, 'rgba(0,0,0,0)');
    og.fillStyle = g2;
    og.fillRect(b[0]-26, b[1]-26, b[2]+52, b[3]+52);
  });
"""

REPAIRED = """
  /* THE REPAIR: blurred rectangles, which follow the shape of the box */
  AKENGRAVE.punchReserves(og, boxes, {blur: 9});
"""

NEEDLE = "fingerprint of a RADIAL destination-out reserve"

CASES = [
    ("punched with a radial gradient", RADIAL, False),
    ("punched with AKENGRAVE.punchReserves", REPAIRED, True),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="reservepunch_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, punch, _ok) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(SLIDE % punch)
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=600)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=600)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, _punch, should_pass) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html", {"fails": ["slide never rendered"],
                                        "warns": []})
        found = [f for f in s.get("fails", []) + s.get("warns", [])
                 if "WORST POINT" in f or "worst-point" in f]
        named = [f for f in found if NEEDLE in f]
        if should_pass:
            good = not found            # the helper reserves the whole line
        else:
            good = bool(found) and bool(named)
        ok &= good
        print("[%s] %-38s -> %s" % ("HOLD" if good else "BROKE", name,
                                    "clean" if not found else found[0][:230]))
    print("reserve_punch_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
