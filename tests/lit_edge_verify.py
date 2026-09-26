#!/usr/bin/env python3
"""Is a layer of light that ends in mid-air caught? (2026-09-26, run No.69)

No.69's CRAFT FLOOR cycle rebuilt slide 08's lamp glow as one per-pixel
falloff, computed on an offscreen canvas 760 px wide and composited in
`screen`. The halo still carried a few levels of light at the layer's left
edge, so the picture got a hard vertical edge at x 492, visible in the 432 px
thumb. render, qa and every gate passed it, and the re-scorer found it after
the last card.

render.py's gradient hook records every ADDITIVE drawImage of a canvas whose
in-frame edge still carries light (`lit_edges`), and qa.py confirms the step on
the final canvas layer before it WARNs. Five fixtures through the REAL render.py
and qa.py:

  RED    the run's own shape: a 760 px glow layer at x 492, screen -> must WARN
  GREEN  the repair: the same glow on a full-frame layer            -> silent
  GREEN  a 760 px layer feathered to zero on its in-frame edges     -> silent
  GREEN  the RED layer with an opaque plate drawn over its edge     -> recorded,
         but silent in qa, because nothing visible is left to report
  GREEN  the RED layer drawn in source-over (a panel, not light)    -> silent
  RED    twelve 30 px additive sprites, then the RED layer          -> must WARN
         (short edges can't fill the census ahead of the seam; Codex, PR #402)
  RED    the glow filling a 588 px canvas element placed at x 492   -> must WARN
         (the layer ends at its canvas's own boundary; Codex, PR #402)
  RED    a layer drawn at x -100 on a canvas that starts at x 500   -> must WARN
         at x 500: the canvas clips the light at its own boundary, and the lit
         source there is inspected, not the clipped-away rect edge (Codex, PR #402)
  RED    the RED layer at globalAlpha 0.12 under brightness(300%)   -> must WARN
         (the raw border is under LIT_MIN; the filter makes it a seam)
  RED    the RED layer drawn with a negative destination width      -> must WARN
         (legal Canvas 2D, normalised, no flip; both Codex, PR #402)
  RED    canvases reordered by z-index, seam canvas on top            -> must WARN
         (the shipped render decides; no paint-order model)
  RED    a source rect that starts past its source canvas           -> must WARN
  RED    a full-frame glow drawn through ctx.clip() from x 492      -> must WARN
  RED    ancestor stacking contexts that reverse DOM order          -> must WARN
  RED    a full-strength additive panel on a 2 percent canvas       -> must WARN
         (all four Codex, PR #402: the hook reads what was painted and qa reads
         the shipped render, so none of them needs a model of its own)
  RED    a full-width layer starting at y 700                        -> must WARN
         as a TOP edge at y 700 (a horizontal seam is measured as a row)
  RED    the nested-canvas glow, painted before the canvas is appended -> must WARN
  RED    a bright panel drawn additively through a 30 degree rotation -> must WARN
         along its diagonal cut (all three Codex, PR #402)
  RED    a second translucent white layer on a translucent canvas  -> must WARN
         (the draw raises only alpha; the delta is premultiplied)
  RED    a 20 px seam on a canvas shown at 3x                       -> must WARN
         (the 40 px span is applied in design px, after CSS scale)
  GREEN  the nested glow on a CSS-rotated canvas                    -> nothing
         recorded, and qa says it couldn't place the seam (all Codex, PR #402)
  GREEN  the RED layer under an opaque DOM plate over its edge      -> recorded,
         but silent in qa: the canvas layer shows the seam and the shipped
         picture does not, and only the shipped picture counts (Codex, PR #402)

The occluded case is the reason the verdict lives on the pixels: the brush
knows a layer ended, only the final picture knows whether anyone can see it.
Every layer here runs the full frame height, so the left edge is the only line
inside the frame. The first draft of this file started the full-width GREEN
layer at y 340 with no feather, and the check reported that top edge as a
2.0-level step over 568 px: it was right, the fixture was wrong.

    python3 tests/lit_edge_verify.py

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

RED_ROTATED = """
// a bright panel drawn additively through a 30 degree rotation: a long
// diagonal cut that no row or column scan can see
const wl = document.createElement('canvas'); wl.width = 500; wl.height = 900;
const wg = wl.getContext('2d'); wg.fillStyle = 'rgb(90,70,40)'; wg.fillRect(0, 0, 500, 900);
cx.save(); cx.translate(540, 675); cx.rotate(Math.PI / 6); cx.globalCompositeOperation = 'screen';
cx.drawImage(wl, -250, -450); cx.restore();
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

GREEN_CSS_ROTATED = """
// the seam canvas is CSS-rotated: its bounding box can't place the line, so
// nothing is recorded and qa says it couldn't place it (Codex, PR #402)
const nc = document.createElement('canvas'); nc.width = 588; nc.height = 1350;
nc.style.cssText = 'position:absolute;left:492px;top:0;width:588px;height:1350px;transform:rotate(20deg)';
document.body.appendChild(nc);
const n2 = nc.getContext('2d'), gn = glow(492, 0, 588, 1350, false);
n2.globalCompositeOperation = 'screen'; n2.drawImage(gn, 0, 0);
"""

GREEN_PANEL = """
const g = glow(492, 0, 760, 1350, false);
cx.drawImage(g, 492, 0, 760, 1350);
"""

# (name, body, expect a lit_edges record, expect a qa warn)
CASES = [("slide-01", RED, True, True),
         ("slide-02", GREEN_SPAN, False, False),
         ("slide-03", GREEN_FEATHER, False, False),
         ("slide-04", GREEN_OCCLUDED, True, False),
         ("slide-05", GREEN_PANEL, False, False),
         ("slide-06", GREEN_DOM_PLATE, True, False),
         ("slide-07", RED_AFTER_SPRITES, True, True),
         ("slide-08", RED_NESTED, True, True),
         ("slide-09", RED_CLIPPED, True, True),
         ("slide-10", RED_FILTERED, True, True),
         ("slide-11", RED_NEGATIVE, True, True),
         ("slide-12", RED_ZORDER, True, True),
         ("slide-13", RED_SRC_BOUNDS, True, True),
         ("slide-14", RED_CTX_CLIP, True, True),
         ("slide-15", RED_ANCESTOR_Z, True, True),
         ("slide-16", RED_FAINT_CANVAS, True, True),
         ("slide-17", RED_HORIZONTAL, True, True),
         ("slide-18", RED_APPENDED_LATE, True, True),
         ("slide-19", RED_ROTATED, True, True),
         ("slide-20", RED_TRANSLUCENT, True, True),
         ("slide-21", RED_CSS_SCALED, True, True),
         ("slide-22", GREEN_CSS_ROTATED, False, False)]
EXPECT_X = {"slide-09": 500}
# what each RED case must record and name: (side, coordinate or None)
EXPECT = {"slide-17": ("top", 700), "slide-19": ("line", None)}
# a 20 px band has real top and bottom seams as well as the named left one
MULTI = {"slide-21"}
NEEDLE = "a layer of light ends in mid-air"


def main():
    bad = []
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        sdir, rdir = root / "slides", root / "render"
        sdir.mkdir()
        for name, body, _, _ in CASES:
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
        # every fixture must be in the report, or a GREEN case passes by absence
        missing = [n for n, _, _, _ in CASES if n + ".html" not in byfile]
        if missing:
            bad.append("render report omits fixtures: %s" % missing)

        for name, _, rec_want, _ in CASES:
            rec = byfile.get(name + ".html", {})
            if rec.get("page_errors"):
                bad.append("%s: the hook broke the page: %s" % (name, rec["page_errors"]))
            edges = rec.get("lit_edges", [])
            if rec_want:
                side, coord = EXPECT.get(name, ("left", EXPECT_X.get(name, 492)))
                got = [e for e in edges if e.get("side") == side]
                if not got:
                    bad.append("%s: the lit %s edge was NOT recorded: %s"
                               % (name, side, json.dumps(edges)))
                elif coord is not None and (abs(got[0]["at"] - coord) > 1 or got[0]["lit_max"] < 0.004):
                    bad.append("%s: recorded the wrong line or level: %s"
                               % (name, json.dumps(got[0])))
            elif edges:
                bad.append("%s: recorded an edge that carries no light: %s"
                           % (name, json.dumps(edges)))

        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(rdir)], capture_output=True, text=True)
        qa = json.loads((rdir / "machine_qa.json").read_text())
        want = dict((n + ".html", w) for n, _, _, w in CASES)
        qfiles = {s["file"] for s in qa["slides"]}
        if set(want) - qfiles:
            bad.append("qa report omits fixtures: %s" % sorted(set(want) - qfiles))
        for s in qa["slides"]:
            hits = [w for w in s.get("warns", []) if NEEDLE in w]
            name = s["file"][:-5]
            if want.get(s["file"]):
                side, coord = EXPECT.get(name, ("left", EXPECT_X.get(name, 492)))
                named = ("along a straight line" if side == "line" else
                         "%s %d (its %s edge)" % ("y" if side in ("top", "bottom") else "x", coord, side))
                if len(hits) < 1 or (side != "line" and name not in MULTI and len(hits) != 1):
                    bad.append("%s: qa.py reported %d lit-edge warnings, expected 1: %s"
                               % (s["file"], len(hits), hits))
                elif not any(named in h for h in hits):
                    bad.append("%s: the warning names the wrong line: %s" % (s["file"], hits))
            elif hits:
                bad.append("%s: qa.py warned about honest drawing: %s" % (s["file"], hits))
            if s["file"] == "slide-22.html" and not any("could not place" in w for w in s.get("warns", [])):
                bad.append("slide-22.html: qa.py did not say it couldn't place the rotated canvas's seam")
            if any("lit-edge record unreadable" in w for w in s.get("warns", [])):
                bad.append("%s: qa.py could not read its own record" % s["file"])

    if bad:
        print("BROKEN")
        for b in bad:
            print(" - " + b)
        return 1
    print("HOLDS: a 760 px screen-composited glow layer whose edge still carries light "
          "is recorded at x 492 and reported once; the full-frame layer, the feathered "
          "layer, the occluded edges (canvas and DOM) and the source-over panel are all silent in qa.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
