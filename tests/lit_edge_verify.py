#!/usr/bin/env python3
"""Is a layer of light that ends in mid-air caught? (2026-09-26, run No.69)

No.69's CRAFT FLOOR cycle drew slide 08's lamp glow on an offscreen canvas 760
px wide and composited it in `screen`. The halo still carried a few levels of
light at the layer's left edge, so the picture got a hard vertical edge at
x 492, visible in the 432 px thumb. render, qa and every gate passed it, and
the re-scorer found it after the last card.

render.py's LIT_EDGE_HOOK_JS measures the light each additive drawImage
actually painted and records where it stops on a straight row or column
(`lit_edges`); qa.py confirms each line in the shipped render before it WARNs,
and names anything the hook could not measure or place. Every fixture goes
through the REAL render.py and qa.py:

  01 RED    the run's own shape: a 760 px glow layer at x 492, screen
  02 GREEN  the repair: the same glow on a full-frame layer
  03 GREEN  a 760 px layer feathered to zero on its in-frame edges
  04 GREEN  the RED layer with an opaque canvas plate over its edge
            (recorded, silent in qa: nothing visible is left)
  05 GREEN  the RED layer drawn in source-over (a panel, not light)
  06 GREEN  the RED layer under an opaque DOM plate (recorded, silent)
  07 RED    twelve 30 px additive sprites, then the RED layer
  08 RED    the glow filling a 588 px canvas element placed at x 492
  09 RED    a layer drawn at x -100 on a canvas that starts at x 500
  10 RED    the RED layer at globalAlpha 0.12 under brightness(300%)
  11 RED    the RED layer drawn with a negative destination width
  12 RED    canvases reordered by z-index, the seam canvas on top
  13 RED    a source rect that starts past its source canvas
  14 RED    a full-frame glow drawn through ctx.clip() from x 492
  15 RED    ancestor stacking contexts that reverse DOM order
  16 RED    a full-strength additive panel on a 2 percent canvas
  17 RED    a full-width layer starting at y 700: a TOP edge
  18 RED    the nested glow, painted before its canvas is appended
  19 RED    one glow through a clip of two rects on the same line: BOTH
            stretches of x 492 are reported, not only the longer (and the
            rects' ends at y 500 and y 800, which are real seams too)
  20 RED    a second translucent white layer on a translucent canvas
            (the draw raises only alpha; the delta is premultiplied)
  21 RED    a 20 px seam on a canvas shown at 3x (40 px applies in design px)
  22 GREEN  the nested glow on a canvas under transform: rotate(20deg)
  23 GREEN  the same under transform: scaleX(-1), a mirror
  24 GREEN  the same under the separate CSS `rotate: 20deg` property
            (22 to 24: nothing recorded, and qa says it could not place it)
  25 RED    a full-width layer ending at y 700: a BOTTOM edge
  26 RED    a full-height layer ending at x 588: a RIGHT edge
  27 GREEN  twenty 30 px additive sprites, then the RED layer: the seam is
            past the on-page budget, and qa says the check was capped
  28 GREEN  thirty additive sprites onto a detached canvas that is then
            appended: past the off-page budget, and qa says so

Then the report path for what the hook could not read: no route to a tainted
canvas exists under render.py's flags (--allow-file-access-from-files, and a
foreignObject SVG image stays readable, measured 2026-09-26), so the fixture
feeds qa.py a record with lit_edges_readback set and checks it is named.

OUT OF SCOPE, deliberately: a seam at any angle other than a row or column
(a draw through a rotation, a diagonal clip). The hook does not look for one
and nothing here claims it does.

    python3 tests/lit_edge_verify.py

Exit 0 HOLDS, exit 1 BROKEN. A fixture missing from either report is BROKEN,
so a GREEN case can never pass by absence.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#000;width:1080px;height:1350px}
canvas{display:block}</style></head><body>
<canvas id="c" width="1080" height="1350"></canvas>
<script>
const W = 1080, H = 1350, cx = document.getElementById('c').getContext('2d');
const bg = cx.createLinearGradient(0, 0, 0, H);
bg.addColorStop(0, '#0B1422'); bg.addColorStop(1, '#1A2436');
cx.fillStyle = bg; cx.fillRect(0, 0, W, H);
// a lamp at (872, 760): core, two exp halos and a squashed pool, per pixel
function glow(gx0, gy0, GW, GH, feather) {
  const gl = document.createElement('canvas'); gl.width = GW; gl.height = GH;
  const gc = gl.getContext('2d'), im = gc.createImageData(GW, GH), d = im.data;
  for (let j = 0; j < GH; j++) for (let i = 0; i < GW; i++) {
    const x = gx0 + i - 872, y = gy0 + j - 760, r = Math.hypot(x, y);
    let v = Math.exp(-r / 7) * 0.9 + Math.exp(-r / 60) * 0.34 + Math.exp(-r / 170) * 0.12;
    // the pool fades in over 40 px below the lamp, so the light itself has no
    // edge of its own (a hard `y > 12` start is a real seam, and the measured
    // hook rightly records it)
    v += Math.exp(-Math.hypot(x / 220, (y - 16) / 44)) * 0.3 * Math.min(1, Math.max(0, (y - 12) / 40));
    if (feather) {
      const e = Math.min(i, GW - 1 - i, j, GH - 1 - j) / 150, f = Math.min(1, e);
      v *= f * f * (3 - 2 * f);
    }
    v = Math.min(1, v); const o = (j * GW + i) * 4;
    d[o] = 255 * v * 0.953; d[o + 1] = 255 * v * 0.702; d[o + 2] = 255 * v * 0.416; d[o + 3] = 255;
  }
  gc.putImageData(im, 0, 0);
  return gl;
}
%s
window.renderReady = Promise.resolve(true);
</script></body></html>
"""

RED = """
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
"""

GREEN_SPAN = """
const g = glow(0, 0, 1080, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 0, 0, 1080, 1350); cx.restore();
"""

GREEN_FEATHER = """
const g = glow(492, 0, 760, 1350, true);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
"""

GREEN_OCCLUDED = """
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
cx.fillStyle = '#3A2A1E'; cx.fillRect(440, 0, 120, 1350);
"""

GREEN_DOM_PLATE = """
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
const plate = document.createElement('div');
plate.style.cssText = 'position:absolute;left:440px;top:0;width:120px;height:1350px;background:#3A2A1E';
document.body.appendChild(plate);
"""

RED_AFTER_SPRITES = """
for (let q = 0; q < 12; q++) {
  const sp = document.createElement('canvas'); sp.width = 30; sp.height = 30;
  const sg = sp.getContext('2d'); sg.fillStyle = 'rgb(200,160,90)'; sg.fillRect(0, 0, 30, 30);
  cx.save(); cx.globalCompositeOperation = 'screen'; cx.globalAlpha = 0.3;
  cx.drawImage(sp, 60 + q * 30, 200 + (q % 3) * 60); cx.restore();
}
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
"""

RED_NESTED = """
const nc = document.createElement('canvas'); nc.width = 588; nc.height = 1350;
nc.style.cssText = 'position:absolute;left:492px;top:0;width:588px;height:1350px';
document.body.appendChild(nc);
const n2 = nc.getContext('2d'), gn = glow(492, 0, 588, 1350, false);
const nb = n2.createLinearGradient(0, 0, 0, H);   // the page's own ground, so only the light differs
nb.addColorStop(0, '#0B1422'); nb.addColorStop(1, '#1A2436');
n2.fillStyle = nb; n2.fillRect(0, 0, 588, 1350);
n2.globalCompositeOperation = 'screen'; n2.drawImage(gn, 0, 0);
"""

RED_CLIPPED = """
const nc = document.createElement('canvas'); nc.width = 580; nc.height = 1350;
nc.style.cssText = 'position:absolute;left:500px;top:0;width:580px;height:1350px';
document.body.appendChild(nc);
const n2 = nc.getContext('2d'), gn = glow(400, 0, 760, 1350, false);
const nb = n2.createLinearGradient(0, 0, 0, H);
nb.addColorStop(0, '#0B1422'); nb.addColorStop(1, '#1A2436');
n2.fillStyle = nb; n2.fillRect(0, 0, 580, 1350);
n2.globalCompositeOperation = 'screen'; n2.drawImage(gn, -100, 0);
"""

RED_FILTERED = """
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.globalAlpha = 0.12; cx.filter = 'brightness(300%)';
cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
"""

RED_NEGATIVE = """
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen';
cx.drawImage(g, 0, 0, 760, 1350, 1252, 0, -760, 1350); cx.restore();
"""

RED_ZORDER = """
// the seam-bearing canvas is FIRST in the DOM but painted on top (z-index 2);
// a later canvas, painted underneath (z-index 1), is opaque over the seam's
// line. The shipped render shows the seam, so it must WARN: the verdict reads
// the shipped render and needs no model of paint order (Codex, PR #402)
const c = document.getElementById('c'); c.style.cssText = 'position:absolute;left:0;top:0;z-index:2';
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
const back = document.createElement('canvas'); back.width = 1080; back.height = 1350;
back.style.cssText = 'position:absolute;left:0;top:0;z-index:1';
document.body.appendChild(back);
const bctx = back.getContext('2d'); bctx.fillStyle = '#3A2A1E'; bctx.fillRect(440, 0, 120, 1350);
"""

RED_SRC_BOUNDS = """
// the source rect starts 100 px LEFT of the source canvas: that part is
// transparent, so the light begins at x 492, inside the destination rect
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen';
cx.drawImage(g, -100, 0, 860, 1350, 392, 0, 860, 1350); cx.restore();
"""

RED_CTX_CLIP = """
// a full-frame glow drawn through a clip that starts at x 492
const g = glow(0, 0, 1080, 1350, false);
cx.save(); cx.beginPath(); cx.rect(492, 0, 588, 1350); cx.clip();
cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 0, 0); cx.restore();
"""

RED_ANCESTOR_Z = """
// canvases with z-index auto inside positioned parents whose stacking order
// is the reverse of DOM order: the seam canvas is painted on top
const c = document.getElementById('c');
const upper = document.createElement('div'); upper.style.cssText = 'position:absolute;left:0;top:0;z-index:2';
const lower = document.createElement('div'); lower.style.cssText = 'position:absolute;left:0;top:0;z-index:1';
document.body.appendChild(upper); upper.appendChild(c); document.body.appendChild(lower);
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
const back = document.createElement('canvas'); back.width = 1080; back.height = 1350; lower.appendChild(back);
const bctx = back.getContext('2d'); bctx.fillStyle = '#3A2A1E'; bctx.fillRect(440, 0, 120, 1350);
"""

RED_FAINT_CANVAS = """
// a full-strength additive panel on a canvas shown at 2 percent opacity: a
// five-level step in the shipped render
const nc = document.createElement('canvas'); nc.width = 588; nc.height = 1350;
nc.style.cssText = 'position:absolute;left:492px;top:0;width:588px;height:1350px;opacity:0.02';
document.body.appendChild(nc);
const n2 = nc.getContext('2d'), wl = document.createElement('canvas'); wl.width = 588; wl.height = 1350;
const wg = wl.getContext('2d'); wg.fillStyle = '#FFFFFF'; wg.fillRect(0, 0, 588, 1350);
n2.globalCompositeOperation = 'screen'; n2.drawImage(wl, 0, 0);
"""

RED_HORIZONTAL = """
// a full-width glow layer that starts at y 700: its top edge is a HORIZONTAL
// seam, which must be recorded as a top edge and measured as a row
const g = glow(0, 700, 1080, 650, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 0, 700, 1080, 650); cx.restore();
"""

RED_APPENDED_LATE = """
// the visible canvas is painted while detached and appended afterwards
const nc = document.createElement('canvas'); nc.width = 588; nc.height = 1350;
nc.style.cssText = 'position:absolute;left:492px;top:0;width:588px;height:1350px';
const n2 = nc.getContext('2d'), gn = glow(492, 0, 588, 1350, false);
const nb = n2.createLinearGradient(0, 0, 0, H);
nb.addColorStop(0, '#0B1422'); nb.addColorStop(1, '#1A2436');
n2.fillStyle = nb; n2.fillRect(0, 0, 588, 1350);
n2.globalCompositeOperation = 'screen'; n2.drawImage(gn, 0, 0);
document.body.appendChild(nc);
"""

RED_TRANSLUCENT = """
// a translucent white overlay canvas; a second translucent white layer added
// with 'lighter' from x 492 raises only the ALPHA (unpremultiplied RGB stays
// 255), yet the page sees a brighter band from x 492 (Codex, PR #402)
const oc = document.createElement('canvas'); oc.width = 1080; oc.height = 1350;
oc.style.cssText = 'position:absolute;left:0;top:0;width:1080px;height:1350px';
document.body.appendChild(oc);
const o2 = oc.getContext('2d'); o2.fillStyle = 'rgba(255,255,255,0.08)'; o2.fillRect(0, 0, 1080, 1350);
const sp = document.createElement('canvas'); sp.width = 588; sp.height = 1350;
const s2 = sp.getContext('2d'); s2.fillStyle = 'rgba(255,255,255,0.08)'; s2.fillRect(0, 0, 588, 1350);
o2.globalCompositeOperation = 'lighter'; o2.drawImage(sp, 492, 0);
"""

RED_CSS_SCALED = """
// a 20 px tall canvas shown at 3x: its 20 px seam is 60 design px on the page
const sc = document.createElement('canvas'); sc.width = 200; sc.height = 20;
sc.style.cssText = 'position:absolute;left:480px;top:600px;width:600px;height:60px';
document.body.appendChild(sc);
const c2 = sc.getContext('2d'); c2.fillStyle = '#101826'; c2.fillRect(0, 0, 200, 20);
const sp = document.createElement('canvas'); sp.width = 196; sp.height = 20;
const s2 = sp.getContext('2d'); s2.fillStyle = 'rgb(60,50,30)'; s2.fillRect(0, 0, 196, 20);
c2.globalCompositeOperation = 'screen'; c2.drawImage(sp, 4, 0);
"""

GREEN_PANEL = """
const g = glow(492, 0, 760, 1350, false);
cx.drawImage(g, 492, 0, 760, 1350);
"""

RED_TWO_RUNS = """
// one full-frame glow through a clip of two rects that share the line x 492;
// the rects' own ends at y 500 and y 800 are real seams too, and are reported
const g = glow(0, 0, 1080, 1350, false);
cx.save(); cx.beginPath(); cx.rect(492, 0, 588, 500); cx.rect(492, 800, 588, 550); cx.clip();
cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 0, 0); cx.restore();
"""

def placed_canvas(css):
    return """
const nc = document.createElement('canvas'); nc.width = 588; nc.height = 1350;
nc.style.cssText = 'position:absolute;left:492px;top:0;width:588px;height:1350px;%s';
document.body.appendChild(nc);
const n2 = nc.getContext('2d'), gn = glow(492, 0, 588, 1350, false);
n2.globalCompositeOperation = 'screen'; n2.drawImage(gn, 0, 0);
""" % css

GREEN_CSS_ROTATED = placed_canvas("transform:rotate(20deg)")
GREEN_CSS_MIRRORED = placed_canvas("transform:scaleX(-1)")
GREEN_ROTATE_PROP = placed_canvas("rotate:20deg")

RED_BOTTOM = """
// a full-width glow layer that ends at y 700: a BOTTOM edge
const g = glow(0, 0, 1080, 700, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 0, 0, 1080, 700); cx.restore();
"""

RED_RIGHT = """
// a full-height glow layer that ends at x 588: a RIGHT edge
const g = glow(0, 0, 588, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 0, 0, 588, 1350); cx.restore();
"""

def sprites(n, target):
    return """
for (let q = 0; q < %d; q++) {
  const sp = document.createElement('canvas'); sp.width = 30; sp.height = 30;
  const sg = sp.getContext('2d'); sg.fillStyle = 'rgb(200,160,90)'; sg.fillRect(0, 0, 30, 30);
  %s.save(); %s.globalCompositeOperation = 'screen'; %s.globalAlpha = 0.3;
  %s.drawImage(sp, 60 + (q %% 12) * 30, 200 + (q %% 3) * 60); %s.restore();
}
""" % ((n,) + (target,) * 5)

GREEN_BUDGET_ON = sprites(20, "cx") + """
const g = glow(492, 0, 760, 1350, false);
cx.save(); cx.globalCompositeOperation = 'screen'; cx.drawImage(g, 492, 0, 760, 1350); cx.restore();
"""

GREEN_BUDGET_OFF = """
const dc = document.createElement('canvas'); dc.width = 1080; dc.height = 1350;
dc.style.cssText = 'position:absolute;left:0;top:0';
const d2 = dc.getContext('2d');
""" + sprites(30, "d2") + """
document.body.appendChild(dc);
"""

# (name, body, records that must exist as (side, at), qa warnings that must
#  name each line as "x 492 (its left edge)", the exact lit-edge warn count,
#  and a phrase another warning must carry)
LEFT = ("left", 492)
CASES = [
    ("slide-01", RED, [LEFT], 1, None),
    ("slide-02", GREEN_SPAN, [], 0, None),
    ("slide-03", GREEN_FEATHER, [], 0, None),
    ("slide-04", GREEN_OCCLUDED, [LEFT], 0, None),
    ("slide-05", GREEN_PANEL, [], 0, None),
    ("slide-06", GREEN_DOM_PLATE, [LEFT], 0, None),
    ("slide-07", RED_AFTER_SPRITES, [LEFT], 1, None),
    ("slide-08", RED_NESTED, [LEFT], 1, None),
    ("slide-09", RED_CLIPPED, [("left", 500)], 1, None),
    ("slide-10", RED_FILTERED, [LEFT], 1, None),
    ("slide-11", RED_NEGATIVE, [LEFT], 1, None),
    ("slide-12", RED_ZORDER, [LEFT], 1, None),
    ("slide-13", RED_SRC_BOUNDS, [LEFT], 1, None),
    ("slide-14", RED_CTX_CLIP, [LEFT], 1, None),
    ("slide-15", RED_ANCESTOR_Z, [LEFT], 1, None),
    ("slide-16", RED_FAINT_CANVAS, [LEFT], 1, None),
    ("slide-17", RED_HORIZONTAL, [("top", 700)], 1, None),
    ("slide-18", RED_APPENDED_LATE, [LEFT], 1, None),
    ("slide-19", RED_TWO_RUNS, [LEFT, LEFT, ("bottom", 500), ("top", 800)], 4, None),
    ("slide-20", RED_TRANSLUCENT, [LEFT], 1, None),
    ("slide-21", RED_CSS_SCALED, [("left", 492)], None, None),
    ("slide-22", GREEN_CSS_ROTATED, [], 0, "can't place"),
    ("slide-23", GREEN_CSS_MIRRORED, [], 0, "can't place"),
    ("slide-24", GREEN_ROTATE_PROP, [], 0, "can't place"),
    ("slide-25", RED_BOTTOM, [("bottom", 700)], 1, None),
    ("slide-26", RED_RIGHT, [("right", 588)], 1, None),
    ("slide-27", GREEN_BUDGET_ON, [], 0, "past its budget"),
    ("slide-28", GREEN_BUDGET_OFF, [], 0, "past its budget"),
]
NEEDLE = "a layer of light ends in mid-air"


def named(side, at):
    return "%s %d (its %s edge)" % ("y" if side in ("top", "bottom") else "x", at, side)


def run_qa(rdir):
    subprocess.run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(rdir)],
                   capture_output=True, text=True)
    qa = json.loads((rdir / "machine_qa.json").read_text())
    return {s["file"]: s for s in qa["slides"]}


def main():
    bad = []
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        sdir, rdir = root / "slides", root / "render"
        sdir.mkdir()
        for name, body, _, _, _ in CASES:
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
        missing = [n for n, _, _, _, _ in CASES if n + ".html" not in byfile]
        if missing:
            bad.append("render report omits fixtures: %s" % missing)

        for name, _, want, _, _ in CASES:
            rec = byfile.get(name + ".html", {})
            if rec.get("page_errors"):
                bad.append("%s: the hook broke the page: %s" % (name, rec["page_errors"]))
            edges = list(rec.get("lit_edges", []))
            if not want and edges:
                bad.append("%s: recorded an edge that carries no light: %s"
                           % (name, json.dumps(edges)))
            for side, at in want:
                got = [e for e in edges if e.get("side") == side and abs(e["at"] - at) <= 1
                       and e.get("lit_max", 0) >= 0.004]
                if not got:
                    bad.append("%s: the lit %s edge at %d was NOT recorded: %s"
                               % (name, side, at, json.dumps(edges)))
                else:
                    edges.remove(got[0])

        q = run_qa(rdir)
        if set(n + ".html" for n, _, _, _, _ in CASES) - set(q):
            bad.append("qa report omits fixtures: %s"
                       % sorted(set(n + ".html" for n, _, _, _, _ in CASES) - set(q)))
        for name, _, want, count, other in CASES:
            s = q.get(name + ".html", {})
            warns = s.get("warns", [])
            hits = [w for w in warns if NEEDLE in w]
            if count is not None and len(hits) != count:
                bad.append("%s: qa.py reported %d lit-edge warnings, expected %d: %s"
                           % (name, len(hits), count, hits))
            if count:
                for side, at in want:
                    if not any(named(side, at) in h for h in hits):
                        bad.append("%s: no warning names %s: %s" % (name, named(side, at), hits))
            if count is None and not any(named(*want[0]) in h for h in hits):
                bad.append("%s: no warning names %s: %s" % (name, named(*want[0]), hits))
            if other and not any(other in w for w in warns):
                bad.append("%s: qa.py did not say %r: %s" % (name, other, warns))
            if not other and any(w.startswith("lit-edge check") for w in warns):
                bad.append("%s: qa.py reported a gap that is not there: %s" % (name, warns))
            if any("lit-edge record unreadable" in w for w in warns):
                bad.append("%s: qa.py could not read its own record" % name)

        # what the hook could not read back is named, never dropped
        rep2 = json.loads((rdir / "render_report.json").read_text())
        for s in rep2["slides"]:
            if s["file"] == "slide-02.html":
                s["lit_edges_readback"] = 3
            if s["file"] == "slide-05.html":
                s["lit_edges_readback"] = -1
        (rdir / "render_report.json").write_text(json.dumps(rep2))
        q2 = run_qa(rdir)
        if not any("could not read back 3" in w for w in q2.get("slide-02.html", {}).get("warns", [])):
            bad.append("slide-02 (readback 3): qa.py did not name the unread draws")
        if not any("could not collect its records" in w
                   for w in q2.get("slide-05.html", {}).get("warns", [])):
            bad.append("slide-05 (collection failed): qa.py did not say so")

    if bad:
        print("BROKEN")
        for b in bad:
            print(" - " + b)
        return 1
    print("HOLDS: %d fixtures. Every RED seam is recorded on its line and reported once "
          "per stretch; the repaired, feathered, occluded and source-over layers are "
          "silent; the rotated, mirrored and budget cases say what was not examined."
          % len(CASES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
