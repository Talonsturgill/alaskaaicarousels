#!/usr/bin/env python3
"""Is a circular ramp poured into an ellipse caught while the slide draws?
(2026-08-26)

Run No.41 added a type reserve to six slides as
`createRadialGradient(0,0,24, 0,0,r)` filled into `ctx.ellipse(cx,cy,r,ry)`
with ry well under r. The ramp is circular, the fill is elliptical, so the
paint stopped on the short axis while the ramp still carried about 0.30 alpha
and every one of the six slides got a hard arc across its ground. Four pixel
critics reported it, no machine gate saw it, and it cost a full editing round
under a five-round cap.

Four fixtures through the REAL render.py and qa.py:

  RED   the run's own idiom, rebuilt from its numbers   -> must WARN
  GREEN the scaled-circle idiom the lit pools use       -> must be silent
  GREEN a deliberately hard-edged ellipse (opaque tail) -> must be silent
  GREEN a circular ramp in a circular fill              -> must be silent

The two green ellipse cases are the false-positive guard: the check must not
fire on a fill that was MEANT to have an edge, nor on the correct idiom, or it
becomes noise a run learns to scroll past.

    python3 tests/gradient_clip_verify.py

Exit 0 HOLDS, exit 1 BROKEN.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#123;width:1080px;height:1350px}
canvas{display:block}</style></head><body>
<canvas id="c" width="1080" height="1350"></canvas>
<script>
const cx = document.getElementById('c').getContext('2d');
cx.fillStyle = '#2A3A4A'; cx.fillRect(0, 0, 1080, 1350);
%s
window.renderReady = Promise.resolve(true);
</script></body></html>
"""

# The defect, with run No.41's own shape: a ramp built to fade to nothing at
# r=104, poured into an ellipse only 31 tall.
RED = """
const g = cx.createRadialGradient(540, 900, 24, 540, 900, 104);
g.addColorStop(0, 'rgba(8,10,14,0.44)');
g.addColorStop(0.54, 'rgba(8,10,14,0.18)');
g.addColorStop(1, 'rgba(8,10,14,0)');
cx.fillStyle = g;
cx.beginPath(); cx.ellipse(540, 900, 104, 31, 0, 0, Math.PI * 2); cx.fill();
"""

# The idiom this deck's lit pools already use: a CIRCLE inside a transform.
GREEN_SCALED = """
cx.save(); cx.translate(540, 900); cx.scale(1, 31 / 104);
const g = cx.createRadialGradient(0, 0, 1, 0, 0, 104);
g.addColorStop(0, 'rgba(8,10,14,0.44)');
g.addColorStop(0.54, 'rgba(8,10,14,0.18)');
g.addColorStop(1, 'rgba(8,10,14,0)');
cx.fillStyle = g;
cx.beginPath(); cx.arc(0, 0, 104, 0, Math.PI * 2); cx.fill();
cx.restore();
"""

# An ellipse that is SUPPOSED to have an edge: the ramp ends opaque, so the
# author asked for a hard boundary and gets one on both axes.
GREEN_HARD = """
const g = cx.createRadialGradient(540, 900, 24, 540, 900, 104);
g.addColorStop(0, 'rgba(240,230,200,0.90)');
g.addColorStop(1, 'rgba(180,170,140,0.85)');
cx.fillStyle = g;
cx.beginPath(); cx.ellipse(540, 900, 104, 31, 0, 0, Math.PI * 2); cx.fill();
"""

# A circular ramp in a circular fill: nothing is clipped, nothing to say.
GREEN_ROUND = """
const g = cx.createRadialGradient(540, 900, 1, 540, 900, 104);
g.addColorStop(0, 'rgba(255,248,224,0.44)');
g.addColorStop(1, 'rgba(255,248,224,0)');
cx.fillStyle = g;
cx.beginPath(); cx.ellipse(540, 900, 104, 104, 0, 0, Math.PI * 2); cx.fill();
"""

CASES = [("slide-01", RED, True), ("slide-02", GREEN_SCALED, False),
         ("slide-03", GREEN_HARD, False), ("slide-04", GREEN_ROUND, False)]
NEEDLE = "circular gradient poured into an ellipse"


def main():
    bad = []
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        sdir, rdir = root / "slides", root / "render"
        sdir.mkdir()
        for name, body, _ in CASES:
            (sdir / (name + ".html")).write_text(PAGE % body)
        r = subprocess.run(
            [sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sdir),
             "--out-dir", str(rdir), "--scale", "1"],
            capture_output=True, text=True)
        if not (rdir / "render_report.json").exists():
            print("BROKEN: render produced no report\n" + r.stdout + r.stderr)
            return 1
        rep = json.loads((rdir / "render_report.json").read_text())
        byfile = {s["file"]: s for s in rep["slides"]}

        for name, _, should in CASES:
            rec = byfile.get(name + ".html", {})
            if rec.get("page_errors"):
                bad.append("%s: the hook broke the page: %s"
                           % (name, rec["page_errors"]))
            clips = rec.get("gradient_clips", [])
            if should and not clips:
                bad.append("%s: the run's own defect was NOT detected" % name)
            if not should and clips:
                bad.append("%s: false positive on honest drawing: %s"
                           % (name, json.dumps(clips)))
            if should and clips:
                c = clips[0]
                if not (c["a_short"] > 0.2 and c["a_long"] < 0.02):
                    bad.append("%s: measured the wrong thing: %s" % (name, json.dumps(c)))

        # ... and the finding must reach a human through qa.py, once per fill.
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(rdir)], capture_output=True, text=True)
        qa = json.loads((rdir / "machine_qa.json").read_text())
        for s in qa["slides"]:
            hits = [w for w in s.get("warns", []) if NEEDLE in w]
            want = dict((n + ".html", sh) for n, _, sh in CASES)[s["file"]]
            if want and len(hits) != 1:
                bad.append("%s: qa.py reported %d warnings, expected 1" % (s["file"], len(hits)))
            if not want and hits:
                bad.append("%s: qa.py warned about honest drawing: %s" % (s["file"], hits))
            if want and hits and "scale(1.000,0.298)" not in hits[0]:
                bad.append("%s: the remedy does not name the right scale: %s"
                           % (s["file"], hits[0]))

    if bad:
        print("BROKEN")
        for b in bad:
            print(" - " + b)
        return 1
    print("HOLDS: the circular-ramp-in-an-ellipse defect is detected as it is "
          "drawn and reported once with its remedy; the scaled-circle idiom, a "
          "deliberately hard-edged ellipse and a circular fill are all silent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
