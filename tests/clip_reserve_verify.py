#!/usr/bin/env python3
"""clip_reserve_verify.py -- the reconstruction behind qa.py's 2026-09-09
even-odd clip checks. Two defects from run No.54, four fixtures.

THE FIRST DEFECT. The house draws an ATTACHED CAST by reserving everything
except the object:

    cx.beginPath(); cx.rect(0, 0, W, H); <the object's outline>;
    cx.clip('evenodd');                  // the object is now a HOLE

No.54 refactored the cockled sheet outline of four slides onto a shared
sheetPath(), and that helper opened with cx.beginPath(). Canvas throws the
current path away on beginPath, so the full-frame rect vanished, the clip became
the object rather than everything-but-the-object, and the casts of slides 02,
03, 04 and 08 were drawn INSIDE their own sheets where the sheet's fill covered
them. Every render succeeded and every frame looked plausible: a missing shadow
is an absence, not an artefact. qa.py's contact gate caught two of the four,
and only because their declared rects happened to sample the right band.

THE SECOND DEFECT. The same run reserved type out of a band field by adding one
rect per element to an even-odd clip. Two elements overlapped by 25px, and a
region covered by the outer shape plus TWO rects has three crossings, which is
odd, which is inside again, so the set lines painted straight back into the gap
between the two elements and read as a broken glyph at the slide's own declared
focal point. qa.py reported it as "busy art under text", the right flag with the
wrong cause, which would never have led anyone to the fix.

THE FIXTURES. Two pairs, each the same drawing broken and repaired:

  1. cast through a helper that calls beginPath()   -> FAILS, full-frame discard
  2. the same helper contributing a subpath          -> clean
  3. two reserved boxes that overlap by 30px         -> WARNS, names both boxes
  4. the same two elements reserved as one box       -> clean

The overlap finding is a WARN and not a FAIL on purpose; qa.py's constants block
carries the corpus that decided it (run No.53 shipped five slides doing this,
some of them real unreserved regions and some of them padding slivers, with no
gap between the two populations to put a threshold in).

The repaired variants are the same pictures with the one-line repair applied, so
the test also proves neither check simply fires on the idiom itself: both clean
fixtures build a full-frame even-odd reserve and clip through it.

Usage: python tests/clip_reserve_verify.py   (exit 0 = all four hold)
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

HEAD = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#1B1712; font-family:"JetBrains Mono", monospace;
         position:relative; color:#EDE3D2; }
  canvas { position:absolute; inset:0; }
</style></head><body>
<canvas id="c" width="2160" height="2700" style="width:1080px;height:1350px"></canvas>
<script type="module">
  const cx = document.getElementById('c').getContext('2d');
  cx.scale(2, 2);
  const W = 1080, H = 1350;
  let s = 20260909;
  const rnd = () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  cx.fillStyle = '#2A231A';
  cx.fillRect(0, 0, W, H);
  for (let i = 0; i < 4000; i++) {
    cx.fillStyle = 'rgba(220,200,170,' + (0.02 + 0.06 * rnd()).toFixed(3) + ')';
    cx.fillRect(rnd() * W, rnd() * H, 2 + 3 * rnd(), 2 + 3 * rnd());
  }
"""

TAIL = """
</script>
</body></html>
"""

# The sheet's cockled outline. BROKEN opens its own path, which is the whole
# defect; REPAIRED contributes a subpath to whatever path is already open.
SHEET = """
  const sheetPath = (cx) => {
    %s
    cx.moveTo(180, 300);
    for (let x = 180; x <= 900; x += 30) cx.lineTo(x, 300 + 6 * Math.sin(x / 70));
    for (let y = 300; y <= 1000; y += 30) cx.lineTo(900 + 5 * Math.sin(y / 60), y);
    for (let x = 900; x >= 180; x -= 30) cx.lineTo(x, 1000 + 6 * Math.sin(x / 55));
    cx.closePath();
  };
"""


def cast_slide(broken):
    """A sheet on a table with an attached cast reserved out of the frame."""
    return HEAD + (SHEET % ("cx.beginPath();" if broken else "")) + """
  /* the lit bench under the sheet */
  const pool = cx.createRadialGradient(540, 700, 0, 540, 700, 620);
  pool.addColorStop(0, 'rgba(255,232,190,0.30)');
  pool.addColorStop(1, 'rgba(255,232,190,0)');
  cx.fillStyle = pool;
  cx.fillRect(0, 0, W, H);

  /* THE ATTACHED CAST: reserve everything except the sheet, then throw the
     cast along the lee. With the outer rect present the cast lands on the
     bench; without it the clip is the sheet and the cast lands under the
     sheet's own fill, where nothing can see it. */
  cx.save();
  cx.beginPath();
  cx.rect(0, 0, W, H);
  sheetPath(cx);
  cx.clip('evenodd');
  const cast = cx.createLinearGradient(0, 1000, 0, 1090);
  cast.addColorStop(0, 'rgba(20,14,8,0.62)');
  cast.addColorStop(1, 'rgba(20,14,8,0)');
  cx.fillStyle = cast;
  cx.fillRect(120, 990, 800, 100);
  cx.restore();

  /* the sheet itself, painted after the cast */
  cx.beginPath();
  sheetPath(cx);
  cx.fillStyle = '#E9DFC9';
  cx.fill();
""" + TAIL


def reserve_slide(broken):
    """A band field with type reserved out of it. Broken: two boxes overlap."""
    boxes = ("""
    cx.rect(150, 640, 620, 96);      /* the hanging subsection letter's box */
    cx.rect(170, 706, 560, 96);      /* the quotation beside it, 30px into the first */
""" if broken else """
    cx.rect(150, 640, 620, 162);     /* both elements reserved as ONE box */
""")
    return HEAD + """
  /* the ruled band field */
  cx.save();
  cx.beginPath();
  cx.rect(90, 560, 900, 420);
""" + boxes + """
  cx.clip('evenodd');
  cx.strokeStyle = 'rgba(90,70,45,0.55)';
  cx.lineWidth = 2;
  for (let y = 570; y < 980; y += 14) {
    cx.beginPath();
    cx.moveTo(90, y);
    cx.lineTo(990, y);
    cx.stroke();
  }
  cx.restore();
""" + TAIL


# (name, html, should_be_clean, needle, which list the finding lands in)
CASES = [
    ("cast through a helper that opens its own path", cast_slide(True), False,
     "thrown away before anything painted it", "fails"),
    ("cast through a helper that contributes a subpath", cast_slide(False), True,
     "thrown away before anything painted it", "fails"),
    ("two reserved boxes overlapping by 30px", reserve_slide(True), False,
     "overlap, so the reserve is not reserved", "warns"),
    ("the same two elements reserved as one box", reserve_slide(False), True,
     "overlap, so the reserve is not reserved", "warns"),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="clipreserve_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, html, _ok, _n, _w) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(html)
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
    for i, (name, _html, should_pass, needle, where) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html", {"fails": ["slide never rendered"],
                                        "warns": ["slide never rendered"]})
        hits = [f for f in s.get(where, []) if needle in f]
        good = (not hits) if should_pass else bool(hits)
        # the overlap finding has to name the geometry, not just the class
        if good and hits and i == 3:
            good = "(150,640) 620x96" in hits[0] and "(170,706) 560x96" in hits[0]
        ok &= good
        print("[%s] %-48s -> %s" % ("HOLD" if good else "BROKE", name,
                                    "clean" if not hits else hits[0][:150]))
    print("clip_reserve_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
