#!/usr/bin/env python3
"""akengrave_even_verify.py -- the reconstruction behind AKENGRAVE surface()'s
opt-in `seed: "even"` lay (2026-10-06, weekly machine pass).

WHAT IT RECONSTRUCTS. surface() seeds every stroke on one raster line through
the region's centre and walks the form's iso-lines from there. On a RADIAL
face the iso-lines are rings, and any ring the centre raster does not cross
is never seeded: with the bore off the region's centre the inner rings print
as a hole, and No.78's flange face printed patches and holes. On a SINUOUS form (No.77's river
channel) the lay collapsed onto a few iso-lines. Both frames were rebuilt by
hand. `seed: "even"` seeds from the strokes already drawn, Jobard and Lefer
(1997), so the lay covers any form at one spacing.

  python3 tests/akengrave_even_verify.py      # exit 0 = every check holds

Node only, no browser, no new dependency: the REAL akengrave.js and noise.js
draw into a stub 2D context that records every filled polygon, and an even-odd
scanline fill turns those polygons into a coverage grid.

  holes     the share of (3 x spacing) px cells inside the form that receive no
            ink, on a radial flange face and on a meandering channel. The
            raster lay must leave a real share empty on both (the defect);
            the even lay must leave under 2 percent on all three.
  wraps     on the flange every even stroke runs along a ring: the mean
            |cos| between a segment and the radius is under 0.1 (rule 1).
  spacing   no sample of one even stroke sits closer than dtest (0.5 x spacing,
            less a tolerance) to a sample of another.
  parity    without the option, surface() draws op for op what git HEAD's
            akengrave.js draws, on all three forms, so no slide changes.
  determ    two even runs draw identical ops.
  reserve   a reserved box receives no ink from the even lay.
  contract  seed: "random" throws.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROBE = r"""
const fs = require('fs');
const ROOT = process.argv[process.argv.length - 2];
const HEAD = process.argv[process.argv.length - 1];
function engrave(src) {
  const scope = {};
  global.window = scope;
  (new Function('window', 'globalThis', fs.readFileSync(ROOT + '/assets/js/noise.js', 'utf8'))).call(scope, scope, scope);
  scope.AKC = {mixOklab: (a, b, t) => 'mix(' + a + ',' + b + ',' + t.toFixed(3) + ')'};
  global.AK = scope.AK; global.AKC = scope.AKC;
  (new Function('window', 'globalThis', src)).call(scope, scope, scope);
  return scope.AKENGRAVE;
}
const NEW = engrave(fs.readFileSync(ROOT + '/assets/js/akengrave.js', 'utf8'));
const OLD = engrave(fs.readFileSync(HEAD, 'utf8'));

function stub() {
  const ops = []; let cur = null, fsty = null;
  const cx = {
    canvas: {width: 2160, clientWidth: 1080},
    save(){}, restore(){}, clip(){}, rect(){}, arc(){}, stroke(){},
    beginPath(){ cur = []; }, closePath(){},
    moveTo(x, y){ cur.push([x, y]); }, lineTo(x, y){ cur.push([x, y]); },
    fill(){ if (cur && cur.length > 2) ops.push({fs: fsty, pts: cur}); cur = []; },
    set fillStyle(v){ fsty = v; }, get fillStyle(){ return fsty; },
    set globalAlpha(v){}
  };
  return {cx, ops};
}
function coverage(ops, X0, Y0, W, H) {
  const g = new Uint8Array(W * H);
  for (const op of ops) {
    const p = op.pts; let ymin = 1e9, ymax = -1e9;
    for (const q of p) { ymin = Math.min(ymin, q[1]); ymax = Math.max(ymax, q[1]); }
    for (let yi = Math.max(0, Math.floor(ymin - Y0)); yi <= Math.min(H - 1, Math.ceil(ymax - Y0)); yi++) {
      const yc = Y0 + yi + 0.5, xs = [];
      for (let i = 0; i < p.length; i++) {
        const a = p[i], b = p[(i + 1) % p.length];
        if ((a[1] <= yc) !== (b[1] <= yc)) xs.push(a[0] + (yc - a[1]) / (b[1] - a[1]) * (b[0] - a[0]));
      }
      xs.sort((u, v) => u - v);
      for (let k = 0; k + 1 < xs.length; k += 2)
        for (let xi = Math.max(0, Math.ceil(xs[k] - X0 - 0.5)); xi <= Math.min(W - 1, Math.floor(xs[k + 1] - X0 - 0.5)); xi++)
          g[yi * W + xi] = 1;
    }
  }
  return g;
}
const PITCH = 5, C = 3 * PITCH;
function holes(ops, region, insideFn) {
  const [X0, Y0, W, H] = region, g = coverage(ops, X0, Y0, W, H);
  let inside = 0, empty = 0;
  for (let cy = 0; cy + C <= H; cy += C) for (let cxp = 0; cxp + C <= W; cxp += C) {
    let all = true, ink = 0;
    for (let j = 0; j < C; j++) for (let i = 0; i < C; i++) {
      if (!insideFn(X0 + cxp + i + 0.5, Y0 + cy + j + 0.5)) all = false;
      ink += g[(cy + j) * W + cxp + i];
    }
    if (!all) continue;
    inside++; if (ink === 0) empty++;
  }
  return {inside, empty, share: inside ? empty / inside : 1};
}

/* the forms. tone 0.5 everywhere, so only the lay decides where ink goes */
/* the flange's bore sits 110 px left of its region's centre, as a face does
 * when the region is boxed round the whole fitting and not round the bore:
 * the raster through the region's centre then never meets the rings smaller
 * than 110 px, which is the "arch away from the raster" hole lathe() was
 * written for (2026-10-01) and the holes No.78 rebuilt by hand */
const FX = 430, FY = 700, R0 = 40, R1 = 280, RX = 540;
const forms = {
  /* a turned flange face, height falling off the bore, rings for iso-lines */
  flange: {region: [RX - 300, FY - 300, 600, 600],
           form: (x, y) => 0.6 * Math.hypot(x - FX, y - FY) + 8 * Math.sin(Math.hypot(x - FX, y - FY) / 40),
           inside: (x, y) => { const r = Math.hypot(x - FX, y - FY); return r > R0 && r < R1 && x > RX - 300; }},
  /* a meandering channel, depth by distance from a sine centreline */
  channel: {region: [140, 400, 800, 600],
            form: (x, y) => { const d = y - (700 + 150 * Math.sin((x - 140) / 110)); return -Math.abs(d) * 0.8 - 0.002 * d * d; },
            inside: (x, y) => x > 150 && x < 930 && y > 410 && y < 990},
  /* the control: a plain fall in y, which the raster lay already covers */
  ramp: {region: [140, 400, 800, 400],
         form: (x, y) => 0.5 * y,
         inside: (x, y) => x > 150 && x < 930 && y > 410 && y < 790}
};
const light = {azDeg: 118, elDeg: 34};
const out = {};
for (const [name, F] of Object.entries(forms)) {
  const opts = {region: F.region, form: F.form, tone: () => 0.5, budget: {main: PITCH},
                inkLo: '#2E363E', inkHi: '#F4F7F9', landformIntended: true};
  const a = stub(), b = stub(), c = stub(), d = stub(), e = stub();
  NEW.create({seed: 7, light}).surface(a.cx, opts);
  OLD.create({seed: 7, light}).surface(b.cx, opts);
  const st = NEW.create({seed: 7, light}).surface(c.cx, Object.assign({seed: 'even'}, opts));
  NEW.create({seed: 7, light}).surface(d.cx, Object.assign({seed: 'even'}, opts));
  out[name] = {raster: holes(a.ops, F.region, F.inside), even: holes(c.ops, F.region, F.inside),
               lines: st.main, parity: JSON.stringify(a.ops) === JSON.stringify(b.ops),
               parity_ops: a.ops.length, determ: JSON.stringify(c.ops) === JSON.stringify(d.ops)};
  if (name === 'flange') {
    /* wraps: segment direction against the radius, over every even stroke centre */
    const eng = NEW.create({seed: 7, light});
    let tot = 0, n = 0, minD = 1e9;
    const lines = [];
    const orig = eng._ribbon;
    eng._ribbon = function (cx, poly, p) { lines.push(poly); return orig.call(this, cx, poly, p); };
    eng.surface(stub().cx, Object.assign({seed: 'even'}, opts));
    for (const L of lines) for (let i = 1; i < L.length; i++) {
      const mx = (L[i][0] + L[i - 1][0]) / 2 - FX, my = (L[i][1] + L[i - 1][1]) / 2 - FY;
      const r = Math.hypot(mx, my); if (r < R0) continue;
      const sx = L[i][0] - L[i - 1][0], sy = L[i][1] - L[i - 1][1], sl = Math.hypot(sx, sy) || 1;
      tot += Math.abs((sx * mx + sy * my) / (sl * r)); n++;
    }
    /* spacing: nearest sample of a DIFFERENT stroke, on a coarse grid */
    const cell = PITCH, grid = new Map();
    lines.forEach((L, id) => L.forEach(q => { const k = Math.floor(q[0] / cell) + ',' + Math.floor(q[1] / cell);
      (grid.get(k) || grid.set(k, []).get(k)).push([q[0], q[1], id]); }));
    lines.forEach((L, id) => L.forEach(q => {
      const i = Math.floor(q[0] / cell), j = Math.floor(q[1] / cell);
      for (let jj = j - 1; jj <= j + 1; jj++) for (let ii = i - 1; ii <= i + 1; ii++) {
        const a = grid.get(ii + ',' + jj); if (!a) continue;
        for (const o of a) if (o[2] !== id) minD = Math.min(minD, Math.hypot(o[0] - q[0], o[1] - q[1]));
      }
    }));
    out.wraps = n ? tot / n : 1; out.min_sep = minD; out.flange_strokes = lines.length;
  }
}
/* reserve */
{
  const box = [380, 520, 120, 60], F = forms.flange;
  const e = NEW.create({seed: 7, light}); e.reserve([box]);
  const s = stub();
  e.surface(s.cx, {region: F.region, form: F.form, tone: () => 0.5, budget: {main: PITCH}, seed: 'even', feather: 6});
  const g = coverage(s.ops, box[0], box[1], box[2], box[3]); let n = 0; for (const v of g) n += v;
  const e0 = NEW.create({seed: 7, light}), s0 = stub();
  e0.surface(s0.cx, {region: F.region, form: F.form, tone: () => 0.5, budget: {main: PITCH}, seed: 'even'});
  const g0 = coverage(s0.ops, box[0], box[1], box[2], box[3]); let n0 = 0; for (const v of g0) n0 += v;
  out.reserve = n; out.reserve_control = n0;
}
try { NEW.create({}).surface(stub().cx, {region: [0, 0, 10, 10], seed: 'random'}); out.contract = 'no throw'; }
catch (err) { out.contract = String(err.message); }
console.log(JSON.stringify(out));
"""


def main():
    head = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:assets/js/akengrave.js"],
                          capture_output=True, text=True, check=True).stdout
    with tempfile.TemporaryDirectory() as td:
        hp = Path(td) / "akengrave_head.js"
        hp.write_text(head)
        p = subprocess.run(["node", "-", str(ROOT), str(hp)], input=PROBE,
                           capture_output=True, text=True)
    if p.returncode != 0:
        print("  BAD  node failed\n" + p.stderr[-1500:])
        return 1
    r = json.loads(p.stdout.strip().splitlines()[-1])
    f, c, m = r["flange"], r["channel"], r["ramp"]
    pct = lambda h: "%d of %d cells empty (%.1f%%)" % (h["empty"], h["inside"], 100 * h["share"])
    checks = [
        ("holes, raster lay on the radial flange (the defect)", f["raster"]["share"] >= 0.10, pct(f["raster"])),
        ("holes, raster lay on the meandering channel (the defect)", c["raster"]["share"] >= 0.05, pct(c["raster"])),
        ("holes, even lay on the radial flange", f["even"]["share"] < 0.02,
         pct(f["even"]) + ", %d strokes" % f["lines"]),
        ("holes, even lay on the meandering channel", c["even"]["share"] < 0.02,
         pct(c["even"]) + ", %d strokes" % c["lines"]),
        ("holes, even lay on the plain ramp (control)", m["even"]["share"] < 0.02,
         pct(m["even"]) + " (raster: %s)" % pct(m["raster"])),
        ("wraps: even strokes run along the flange's rings", r["wraps"] < 0.1,
         "mean |cos| to the radius %.3f" % r["wraps"]),
        ("spacing: no two even strokes closer than dtest", r["min_sep"] >= 0.5 * 5 - 0.6,
         "nearest samples of different strokes %.2f px (dtest 2.5)" % r["min_sep"]),
        ("parity: no option draws what git HEAD draws, all three forms",
         f["parity"] and c["parity"] and m["parity"],
         "%d / %d / %d ops" % (f["parity_ops"], c["parity_ops"], m["parity_ops"])),
        ("determinism: two even runs identical", f["determ"] and c["determ"] and m["determ"], ""),
        ("reserved box: control carries ink", r["reserve_control"] > 200, "%d px" % r["reserve_control"]),
        ("reserved box: no ink from the even lay", r["reserve"] == 0, "%d px" % r["reserve"]),
        ("contract: an unknown seed mode throws", r["contract"].startswith("AKENGRAVE: seed"), r["contract"][:60]),
    ]
    bad = 0
    for name, ok, detail in checks:
        print(("  ok   " if ok else "  BAD  ") + name + (": " + detail if detail else ""))
        bad += 0 if ok else 1
    print("%d/%d checks hold" % (len(checks) - bad, len(checks)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
