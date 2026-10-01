#!/usr/bin/env python3
"""akengrave_lathe_verify.py -- the reconstruction behind AKENGRAVE's lathe()
ring engraver (2026-10-01, run No.74, technique 112).

WHAT IT RECONSTRUCTS. surface() seeds every stroke on one raster through the
region's centre and walks the direction field. On a turned form the iso-lines
are rings, and the rings of a fillet or a flare arch away from that raster, so
no seed lands on them and those bands print as black holes. No.74 met it on a
standard weight (slide 04) and an hourglass (slide 09) and wrote an inline
"ringEngrave" twice. lathe() is that function, promoted.

  python3 tests/akengrave_lathe_verify.py      # exit 0 = every check holds

Node only, no browser, no new dependency: the REAL akengrave.js and noise.js
draw into a stub 2D context that records every filled polygon, and a small
even-odd scanline fill turns those polygons into a coverage grid.

  holes     slide 04's weight profile through surface() vs lathe(): the share
            of 12 px cells inside the silhouette that receive no ink at all.
            surface() must leave a real share empty (the defect), lathe() none.
  parity    lathe() with slide 04's options reproduces No.74's inline
            ringEngrave op for op (same fills, same vertices), on the weight
            AND on a gold ballot sphere, so the promotion changes no pixel.
  lee       on a cylinder every lee crossline sits on the shadow side of the
            axis, and none is drawn when the option is off.
  reserve   a reserved box receives no ink on a 1x offscreen canvas, on the
            2x slide canvas, and under a translated 2x transform (the mask is
            asked in design px); without the reservation the box is inked.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROBE = r"""
const fs = require('fs');
const ROOT = process.argv[process.argv.length - 1];
const scope = {};
global.window = scope;
const load = f => (new Function('window', 'globalThis',
  fs.readFileSync(ROOT + '/assets/js/' + f, 'utf8'))).call(scope, scope, scope);
load('noise.js');
scope.AKC = {mixOklab: (a, b, t) => 'mix(' + a + ',' + b + ',' + t.toFixed(3) + ')'};
global.AK = scope.AK; global.AKC = scope.AKC;
load('akengrave.js');
const AKENGRAVE = scope.AKENGRAVE;

function stub(m, canvas) {
  const ops = []; let cur = null, fs = null;
  const cx = {
    canvas: canvas || {width: 2160, clientWidth: 1080},
    save(){}, restore(){}, clip(){}, rect(){}, arc(){}, stroke(){},
    beginPath(){ cur = []; }, closePath(){},
    moveTo(x, y){ cur.push([x, y]); }, lineTo(x, y){ cur.push([x, y]); },
    fill(){ if (cur && cur.length > 2) ops.push({fs, pts: cur}); cur = []; },
    set fillStyle(v){ fs = v; }, get fillStyle(){ return fs; },
    set strokeStyle(v){}, set lineWidth(v){}, set lineJoin(v){}, set lineCap(v){},
    set globalAlpha(v){},
    getTransform(){ return m || {a: 1, b: 0, c: 0, d: 1, e: 0, f: 0}; }
  };
  return {cx, ops};
}

/* even-odd scanline coverage of the recorded polygons, 1 px rows */
function coverage(ops, X0, Y0, W, H, skip) {
  const g = new Uint8Array(W * H);
  for (const op of ops) {
    if (skip && skip(op)) continue;
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

/* ---- No.74 slide 04's weight, verbatim geometry */
const AX = 770, YB = 1150, HH = 440, YT = YB - HH, TOP = 0.205;
const rOf = y => { const t = (y - YT) / HH;
  if (t < 0) return 0;
  if (t < 0.10) { const u = (t - 0.05) / 0.05; return 30 * Math.sqrt(Math.max(0, 1 - u * u)); }
  if (t < 0.15) return 13;
  if (t < 0.18) return 21;
  if (t < TOP) return 0;
  if (t < 0.25) { const u = (t - TOP) / (0.25 - TOP); return 100 + 18 * Math.sin(u * Math.PI / 2); }
  if (t < 0.88) { let r = 118; [0.56, 0.61].forEach(c => { r -= 5 * Math.exp(-Math.pow((t - c) / 0.007, 2)); }); return r; }
  if (t < 0.93) { const u = (t - 0.88) / 0.05; return 118 + 10 * Math.sin(u * Math.PI / 2); }
  if (t <= 1.0) return 128;
  return 0; };
const LS = [0.52, 0.44, 0.74];
const ramp = ['#2E363E', '#46505A', '#66717B', '#8A949D', '#AEB6BD', '#CDD3D8', '#E4E8EB', '#F4F7F9'];
const gold = ['#9A6E12', '#B88716', '#D69E1C', '#F0B624', '#FFC72C', '#FFD24D', '#FFE07A', '#FFEFB8'];

/* ---- No.74 slide 04's inline ringEngrave, verbatim, as the parity reference */
function inline(cx, axis, y0, y1, rFn, o = {}) {
  const gap = o.gap || 4.2, ell = o.ell == null ? 0.10 : o.ell, wMax = o.wMax || 2.9, inks = o.ramp || ramp;
  let st = 0;
  for (let y = y0 + gap / 2; y < y1; y += gap) {
    const r = rFn(y); if (r < 1.2) continue;
    const slope = (rFn(Math.min(y1, y + 1.5)) - rFn(Math.max(y0, y - 1.5))) / 3, phi = Math.atan(slope);
    const n = Math.max(8, Math.round(2 * r / 2.5)), up = [], dn = [], cols = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n, x = -r + 2 * r * t, th = Math.asin(Math.max(-1, Math.min(1, x / r)));
      const nr = [Math.sin(th), 0, Math.cos(th)], nv = [Math.cos(phi) * nr[0], Math.sin(phi), Math.cos(phi) * nr[2]];
      const lam = Math.max(0, nv[0] * LS[0] + nv[1] * LS[1] + nv[2] * LS[2]);
      const spec = o.spec === false ? 0 : Math.max(0, (lam - 0.9) / 0.1);
      const w = Math.min(gap * 1.02, (0.25 + (wMax - 0.25) * Math.pow(lam, 1.35)) * Math.pow(Math.sin(Math.PI * t), 0.35) * (0.9 + 0.2 * AK.simplex2(y * 0.05, t * 3)) + gap * spec);
      const yy = y + ell * r * Math.cos(th);
      up.push([axis + x, yy - w / 2]); dn.push([axis + x, yy + w / 2]); cols.push(inks[Math.max(0, Math.min(7, Math.round(lam * 7)))]);
    }
    for (let i = 0; i < n; i++) { cx.fillStyle = cols[i]; cx.beginPath(); cx.moveTo(up[i][0], up[i][1]); cx.lineTo(up[i + 1][0], up[i + 1][1]); cx.lineTo(dn[i + 1][0], dn[i + 1][1]); cx.lineTo(dn[i][0], dn[i][1]); cx.closePath(); cx.fill(); }
    st++;
  }
  return st;
}

const out = {};
const light = {azDeg: Math.atan2(LS[1], LS[0]) * 180 / Math.PI, elDeg: Math.asin(LS[2] / Math.hypot(...LS)) * 180 / Math.PI};

/* holes: cells inside the body band (below the flat top) with no ink */
const X0 = AX - 140, Y0 = YT + TOP * HH + 4, W = 280, H = Math.round(YB - Y0);
function holes(ops) {
  const g = coverage(ops, X0, Y0, W, H), C = 12; let inside = 0, empty = 0;
  for (let cy = 0; cy + C <= H; cy += C) for (let cxp = 0; cxp + C <= W; cxp += C) {
    let all = true, ink = 0;
    for (let j = 0; j < C; j++) for (let i = 0; i < C; i++) {
      const x = X0 + cxp + i + 0.5, y = Y0 + cy + j + 0.5;
      if (Math.abs(x - AX) > rOf(y) - 3) all = false;
      ink += g[(cy + j) * W + cxp + i];
    }
    if (!all) continue;
    inside++; if (ink === 0) empty++;
  }
  return {inside, empty, share: inside ? empty / inside : 1};
}
{
  const e = AKENGRAVE.create({seed: 2026100104, light});
  const s = stub();
  const form = (x, y) => { const r = rOf(Math.min(y, YB)), dx = x - AX; return Math.sqrt(Math.max(0, r * r - dx * dx)); };
  e.surface(s.cx, {region: [AX - 140, YT, 280, HH + 20], form, tone: () => 0.5,
                   budget: {main: 4.2}, inkLo: '#2E363E', inkHi: '#F4F7F9'});
  out.surface = holes(s.ops);
  const e2 = AKENGRAVE.create({seed: 2026100104, light});
  const s2 = stub();
  e2.lathe(s2.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, gap: 4.2, ell: 0.10, ramp, L: LS});
  out.lathe = holes(s2.ops);
}

/* parity: the weight and one gold ballot, inline vs lathe() */
function same(a, b) {
  if (a.length !== b.length) return 'op count ' + a.length + ' vs ' + b.length;
  for (let i = 0; i < a.length; i++) {
    if (a[i].fs !== b[i].fs) return 'fill ' + i + ': ' + a[i].fs + ' vs ' + b[i].fs;
    if (a[i].pts.length !== b[i].pts.length) return 'vertex count at op ' + i;
    for (let k = 0; k < a[i].pts.length; k++)
      for (let c = 0; c < 2; c++)
        if (Math.abs(a[i].pts[k][c] - b[i].pts[k][c]) > 1e-9) return 'vertex at op ' + i;
  }
  return 'same';
}
{
  const ball = y => Math.sqrt(Math.max(0, 900 - (y - 1088) * (y - 1088)));
  const A = stub(), B = stub(), e = AKENGRAVE.create({light});
  inline(A.cx, AX, YT, YB + 1, rOf, {gap: 4.2, ell: 0.10});
  e.lathe(B.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, gap: 4.2, ell: 0.10, ramp, L: LS});
  out.parity_weight = same(A.ops, B.ops); out.parity_weight_ops = A.ops.length;
  const C = stub(), D = stub();
  inline(C.cx, 462, 1058, 1118, ball, {gap: 2.5, ell: 0.0, wMax: 2.6, ramp: gold});
  e.lathe(D.cx, {axis: 462, y0: 1058, y1: 1118, r: ball, gap: 2.5, ell: 0.0, wMax: 2.6, ramp: gold, L: LS});
  out.parity_ball = same(C.ops, D.ops); out.parity_ball_ops = C.ops.length;
}

/* lee: only on the shadow side, and only when asked. On a plain cylinder the
 * shadow side is simply the half away from the key; on a profile with slope a
 * bulge's underside is lee too, which is correct, so the side test uses r = 118 */
{
  const e = AKENGRAVE.create({light});
  const s = stub();
  const cyl = y => 118;
  const r1 = e.lathe(s.cx, {axis: AX, y0: YT, y1: YB + 1, r: cyl, ramp, L: LS,
                            lee: {gate: 0.32, gap: 9, wMax: 1.4, ink: '#101418'}});
  const lee = s.ops.filter(o => o.fs === '#101418');
  let pts = 0, shadow = 0;
  lee.forEach(o => o.pts.forEach(p => { pts++; if (p[0] < AX) shadow++; }));
  out.lee = {count: r1.lee, polys: lee.length, shadow_share: pts ? shadow / pts : 0};
  const s0 = stub();
  out.lee_off = e.lathe(s0.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, ramp, L: LS}).lee;
}

/* reserve: no ink in a reserved box, at identity and under translate + 2x */
function inkIn(ops, box) {
  const g = coverage(ops, box[0], box[1], box[2], box[3]);
  let n = 0; for (const v of g) n += v; return n;
}
{
  const box = [700, 900, 60, 50];
  /* a 1x offscreen canvas (drawOffscreen), identity transform */
  const e = AKENGRAVE.create({light}); e.reserve([box]);
  const s = stub(null, {width: 1080, clientWidth: 0});
  e.lathe(s.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, ramp, L: LS});
  out.reserve_identity = inkIn(s.ops, box);
  /* the slide canvas itself: 2160 backing, setTransform(2,0,0,2,0,0) */
  const e1 = AKENGRAVE.create({light}); e1.reserve([box]);
  const s1 = stub({a: 2, b: 0, c: 0, d: 2, e: 0, f: 0});
  e1.lathe(s1.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, ramp, L: LS});
  out.reserve_slide = inkIn(s1.ops, box);
  const e0 = AKENGRAVE.create({light}); const s0 = stub();
  e0.lathe(s0.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, ramp, L: LS});
  out.reserve_control = inkIn(s0.ops, box);
  /* user space shifted 100 px left of design space, canvas backed at 2x */
  const e2 = AKENGRAVE.create({light}); e2.reserve([[box[0] + 100, box[1], box[2], box[3]]]);
  const s2 = stub({a: 2, b: 0, c: 0, d: 2, e: 200, f: 0});
  e2.lathe(s2.cx, {axis: AX, y0: YT, y1: YB + 1, r: rOf, ramp, L: LS});
  out.reserve_transformed = inkIn(s2.ops, box);
}
console.log(JSON.stringify(out));
"""


def main():
    p = subprocess.run(["node", "-", str(ROOT)], input=PROBE,
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("  BAD  node failed\n" + p.stderr[-1200:])
        return 1
    r = json.loads(p.stdout.strip().splitlines()[-1])
    checks = [
        ("holes, surface() on the lathe form (the defect)",
         r["surface"]["share"] >= 0.05,
         "%d of %d cells empty (%.0f%%), want a real share"
         % (r["surface"]["empty"], r["surface"]["inside"], 100 * r["surface"]["share"])),
        ("holes, lathe() on the same form",
         r["lathe"]["empty"] == 0,
         "%d of %d cells empty" % (r["lathe"]["empty"], r["lathe"]["inside"])),
        ("parity with No.74's inline ringEngrave, weight",
         r["parity_weight"] == "same", "%s over %d ops" % (r["parity_weight"], r["parity_weight_ops"])),
        ("parity with No.74's inline ringEngrave, gold ballot",
         r["parity_ball"] == "same", "%s over %d ops" % (r["parity_ball"], r["parity_ball_ops"])),
        ("lee crosslines drawn, all on a cylinder's shadow side",
         r["lee"]["count"] > 0 and r["lee"]["shadow_share"] == 1.0,
         "%d crosslines, %.3f of vertices left of the axis" % (r["lee"]["count"], r["lee"]["shadow_share"])),
        ("no lee crosslines unless asked", r["lee_off"] == 0, "%d" % r["lee_off"]),
        ("reserved box, control (no reservation) carries ink",
         r["reserve_control"] > 100, "%d px" % r["reserve_control"]),
        ("reserved box, 1x offscreen canvas", r["reserve_identity"] == 0, "%d px of ink" % r["reserve_identity"]),
        ("reserved box, the 2x slide canvas", r["reserve_slide"] == 0, "%d px of ink" % r["reserve_slide"]),
        ("reserved box, translated 2x transform", r["reserve_transformed"] == 0,
         "%d px of ink" % r["reserve_transformed"]),
    ]
    ok = True
    for name, good, detail in checks:
        print("  %s  %-52s %s" % ("ok  " if good else "BAD ", name, detail))
        ok = ok and good
    print("LATHE ENGRAVE: " + ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
