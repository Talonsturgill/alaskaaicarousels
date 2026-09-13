#!/usr/bin/env python3
"""overprint_verify.py -- the reconstruction behind qa.py's 2026-09-07
same-line overprint check, on both surfaces.

THE DEFECT. Run No.53's slide 05 set a register of four rows as a name at the
left margin and a value column right-aligned to the gutter. That is a constant,
and a constant cannot be right for four names of different lengths: the longest
name ran under its own value and the frame printed

    LEISNOI PROFESSIONAL SERVICESHQ003425CE092

on the slide whose job is exact figures. It was the round-2 capping defect, and
the round-2 REPAIR had introduced it while fixing four other collisions of the
same shape in round 1 (a label's last glyphs inside the rail's mono column,
twice). qa.py's text_collisions() could not see any of them: it needs the
intersection to cover 30 percent of the smaller line box, and these are a few
characters of overprint worth a few per cent. Five pixel critics found them by
eye, a round apart, twice. The repair that held placed the value column from a
MEASURED width.

THE FIXTURES. Four slides, the same register drawn twice on each surface:

  1. DOM, value column at a constant x        -> FAILS, names both strings
  2. DOM, value column at measured width + 30 -> clean
  3. canvas, value column at a constant x     -> FAILS
  4. canvas, value column at measured width   -> clean

Both broken variants print the same shredded string the run shipped. The two
clean variants are the same register with the one repair applied, so the test
also proves the check is not simply firing on a dense register.

Usage: python tests/overprint_verify.py   (exit 0 = all four hold)
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

ROWS = [("TUKNIK GOVERNMENT SERVICES", "140D0419C0047"),
        ("KONIAG IT SYSTEMS", "HQ003425CE012"),
        ("LEISNOI PROFESSIONAL SERVICES", "HQ003425CE092"),
        ("KONIAG EMERGING TECHNOLOGIES", "W519TC26CA019")]

HEAD = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#081426; font-family:"JetBrains Mono", monospace;
         position:relative; color:#E7EFF8; }
  canvas { position:absolute; inset:0; }
  .row { position:absolute; font-size:26px; white-space:nowrap; }
</style></head><body>
"""

TEXTURE = """
<canvas id="tex" width="2160" height="2700" style="width:1080px;height:1350px"></canvas>
<script type="module">
  const cx = document.getElementById('tex').getContext('2d');
  cx.scale(2, 2);
  let s = 20260907;
  const rnd = () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  for (let i = 0; i < 9000; i++) {
    cx.fillStyle = 'rgba(150,190,235,' + (0.02 + 0.10 * rnd()).toFixed(3) + ')';
    cx.fillRect(rnd() * 1080, rnd() * 1350, 2 + 4 * rnd(), 2 + 4 * rnd());
  }
"""


def dom_slide(broken):
    """The register as DOM rows. Broken: the value column is a constant."""
    out = [HEAD, TEXTURE, "</script>\n"]
    for i, (name, piid) in enumerate(ROWS):
        y = 420 + i * 70
        out.append(f'<div class="row" style="left:96px; top:{y}px">{name}</div>\n')
        # BROKEN: one x for four names. REPAIRED: the longest name plus a gap.
        vx = 520 if broken else 96 + 30 + max(len(n) for n, _ in ROWS) * 15.62
        out.append(f'<div class="row" style="left:{vx:.0f}px; top:{y}px">{piid}</div>\n')
    out.append("</body></html>\n")
    return "".join(out)


def canvas_slide(broken):
    """The same register drawn with fillText."""
    rows = json.dumps(ROWS)
    place = ("520" if broken
             else "96 + 30 + Math.max(...ROWS.map(r => cx.measureText(r[0]).width))")
    return (HEAD + TEXTURE + f"""
  const ROWS = {rows};
  cx.font = '26px "JetBrains Mono", monospace';
  cx.textAlign = 'left';
  cx.fillStyle = '#E7EFF8';
  const vx = {place};
  ROWS.forEach((r, i) => {{
    const y = 440 + i * 70;
    cx.fillText(r[0], 96, y);
    cx.fillText(r[1], vx, y);
  }});
</script>
</body></html>
""")


def mixed_slide(broken):
    """A ROTATED canvas axis label and a DOM block of copy (2026-09-13).

    Run No.58's slide 02 scribed a megawatt rail, drew '100 MW' up the side of
    it with a 90-degree rotation, and set a DOM unit guard in the same 60px of
    x. The deck's one load-bearing number was destroyed and every machine gate
    passed the frame: canvas ink is not a DOM node, so no line box existed to
    intersect, and the rotated string recorded a degenerate box that even the
    canvas-against-canvas test skipped. The scorer caught it by eye and capped
    the round at 6.9. Broken: the guard in the label's column. Repaired: the
    same guard clear of it, everything else identical.
    """
    left = 120 if broken else 420
    return (HEAD + TEXTURE + f"""
  cx.save();
  cx.translate(150, 1140);
  cx.rotate(-Math.PI / 2);
  cx.font = '500 22px "JetBrains Mono", monospace';
  cx.textAlign = 'left';
  cx.fillStyle = '#FFC72C';
  cx.fillText('100 MW', 0, 0);
  cx.restore();
</script>
<div class="row" style="left:{left}px; top:1040px; font-size:24px;
     line-height:1.4; white-space:normal; width:420px">PEAK DEMAND, WHICH IS
     POWER. NOT ANNUAL ENERGY.</div>
</body></html>
""")


CASES = [("DOM register, value column at a constant", dom_slide(True), False,
          "LEISNOI PROFESSIONAL SERVICES"),
         ("DOM register, value column measured", dom_slide(False), True, None),
         ("canvas register, value column at a constant", canvas_slide(True), False,
          "LEISNOI PROFESSIONAL SERVICES"),
         ("canvas register, value column measured", canvas_slide(False), True, None),
         ("rotated canvas label under a DOM block", mixed_slide(True), False,
          "100 MW"),
         ("rotated canvas label, DOM block clear", mixed_slide(False), True, None)]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="overprint_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, html, _ok, _names) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(html)
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
    for i, (name, _html, should_pass, names) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html", {"fails": ["slide never rendered"]})
        hits = [f for f in s["fails"] if "sharing a column" in f
                or "canvas text collision" in f
                or "canvas type through DOM type" in f]
        good = (not hits) if should_pass else bool(hits)
        # a broken variant must name the string that got shredded
        if good and hits and names:
            good = names in hits[0]
        ok &= good
        print("[%s] %-44s -> %s" % ("HOLD" if good else "BROKE", name,
                                    "clean" if not hits else hits[0][:120]))
    print("overprint_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
