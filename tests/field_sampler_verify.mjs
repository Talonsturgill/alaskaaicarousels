#!/usr/bin/env node
/* Does AKPOST.field shade a coarse hand-built field without printing its cells?
 * (2026-11-24, weekly machine pass)
 *
 * The house's C1 samplers all read a DEM's lon/lat meta, so a slide that shaded
 * a grid it built itself hand-rolled bilinear or a smoothstep blend, and the
 * shade printed the cell lattice: No.121 slides 07, 08 and 09 (striations,
 * terraces, zebra columns, two critic rounds each), No.100 slide 07 (a
 * smoothstep-bilinear h() whose slope is zero at every cell centre, three
 * rounds), No.96 (every terrain frame). AKPOST.field is the committed sampler.
 *
 * This reconstructs both hand-rolled interpolants on a seeded coarse field drawn
 * up 18 device px per cell, shades all four per device pixel under a raking key,
 * and holds:
 *   1. THE RED CASES. Bilinear and smoothstep shading carry a strong cell-period
 *      component (the defect, reconstructed) and their slope jumps (bilinear) or
 *      collapses (smoothstep) at cell edges.
 *   2. THE REPAIR. The default (bspline) carries no lattice; monotone carries far
 *      less than either hand-rolled case; both keep a continuous slope across
 *      cell edges, and neither overshoots its posts.
 *   3. THE CONTRACT. monotone passes through every post; the bspline analytic
 *      gradient matches a finite difference; an unknown mode and a short array
 *      throw; outside the grid the edge is held, never NaN.
 *
 *    node tests/field_sampler_verify.mjs        exit 0 HOLDS, exit 1 BROKEN
 */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ctx = { console, Math, Float32Array, Float64Array, Array, Number, Error };
ctx.globalThis = ctx;
vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'assets/js/akpost.js'), 'utf8'), ctx);
const AKPOST = ctx.AKPOST;

let fails = 0;
const check = (name, ok, detail) => { console.log(`[${ok ? 'HOLD' : 'BROKEN'}] ${name}: ${detail}`); if (!ok) fails++; };

/* a seeded coarse field: 24 x 20 posts of smooth-ish noise, the kind a slide builds */
const C = 24, R = 20;
let s = 20261124 >>> 0;
const rnd = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
const z = new Float64Array(C * R);
for (let j = 0; j < R; j++) for (let i = 0; i < C; i++) {
  z[j * C + i] = 40 * Math.sin(i * 0.45 + 0.3 * j) + 25 * Math.cos(j * 0.6 - 0.2 * i) + 18 * rnd();
}
const post = (i, j) => z[Math.max(0, Math.min(R - 1, j)) * C + Math.max(0, Math.min(C - 1, i))];

/* the two interpolants slides hand-rolled */
function lerp2(x, y, ease) {
  const i = Math.min(C - 2, Math.floor(x)), j = Math.min(R - 2, Math.floor(y));
  let u = x - i, v = y - j;
  if (ease) { u = u * u * (3 - 2 * u); v = v * v * (3 - 2 * v); }
  return post(i, j) * (1 - u) * (1 - v) + post(i + 1, j) * u * (1 - v) + post(i, j + 1) * (1 - u) * v + post(i + 1, j + 1) * u * v;
}
const bil = (x, y) => lerp2(x, y, false);
const smo = (x, y) => lerp2(x, y, true);
const mono = AKPOST.field(z, C, R, { mode: 'monotone' });
const bsp = AKPOST.field(z, C, R);

/* shade per device pixel at 18 px per cell under a raking key, then fold the
 * column-to-column change by cell phase: no lattice folds flat (ratio ~1). */
const PPC = 18, X0 = 2, Y0 = 2, W = 18 * PPC, H = 14 * PPC;
const L = (() => { const a = 300 * Math.PI / 180, e = 30 * Math.PI / 180; return [Math.sin(a) * Math.cos(e), -Math.cos(a) * Math.cos(e), Math.sin(e)]; })();
function shade(S) {
  const out = new Float64Array(W * H), d = 0.5 / PPC;
  for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) {
    const x = X0 + px / PPC, y = Y0 + py / PPC;
    const gx = (S(x + d, y) - S(x - d, y)) / (2 * d) / 12, gy = (S(x, y + d) - S(x, y - d)) / (2 * d) / 12;
    const nl = Math.hypot(gx, gy, 1);
    out[py * W + px] = Math.max(0, (-gx * L[0] - gy * L[1] + L[2]) / nl);
  }
  return out;
}
function lattice(sh) {
  const BINS = 18, acc = new Float64Array(BINS), cnt = new Float64Array(BINS); let tot = 0, n = 0;
  for (let py = 0; py < H; py++) for (let px = 1; px < W; px++) {
    const dd = Math.abs(sh[py * W + px] - sh[py * W + px - 1]);
    const b = px % PPC; acc[b] += dd; cnt[b]++; tot += dd; n++;
  }
  const prof = [...acc].map((a, k) => a / cnt[k]), mean = tot / n;
  return Math.max(...prof) / mean;
}
/* slope continuity across a column edge: |slope just right - just left| over |slope| */
function edgeJump(S) {
  let jump = 0, mag = 0; const h = 1e-4;
  for (let q = 0; q < 2000; q++) {
    const xe = 2 + (q % 19), y = 2.5 + ((q * 0.61803398875) % 1) * 15;
    const gl = (S(xe - h, y) - S(xe - 2 * h, y)) / h, gr = (S(xe + 2 * h, y) - S(xe + h, y)) / h;
    jump += Math.abs(gr - gl); mag += (Math.abs(gr) + Math.abs(gl)) / 2;
  }
  return jump / mag;
}
/* smoothstep's own defect: slope at the cell edge against the cell's mean slope */
function edgeFlat(S) {
  let edge = 0, mid = 0; const h = 1e-4;
  for (let q = 0; q < 2000; q++) {
    const i = 2 + (q % 19), y = 2.5 + ((q * 0.61803398875) % 1) * 15;
    edge += Math.abs((S(i + h, y) - S(i - h, y)) / (2 * h));
    mid += Math.abs(S(i + 1, y) - S(i, y));
  }
  return edge / mid;
}

const lat = { bil: lattice(shade(bil)), smo: lattice(shade(smo)), mono: lattice(shade(mono.at)), bsp: lattice(shade(bsp.at)) };
console.log(`  ${PPC} device px per cell; lattice ratio (1.0 = none): bilinear ${lat.bil.toFixed(2)}, smoothstep ${lat.smo.toFixed(2)}, ` +
  `field monotone ${lat.mono.toFixed(2)}, field bspline ${lat.bsp.toFixed(2)}`);
check('red case: bilinear prints the lattice', lat.bil > 2.0, `ratio ${lat.bil.toFixed(2)}`);
check('red case: smoothstep prints the lattice', lat.smo > 2.0, `ratio ${lat.smo.toFixed(2)}`);
/* monotone is C1, not C2: its curvature steps at each edge, which is the residual
 * technique 103 measured on a DEM (1.29). So it must beat both hand-rolled cases
 * clearly, and the default (bspline) must clear the lattice outright. */
check('repair: the default (bspline) carries no lattice', bsp.mode === 'bspline' && lat.bsp < 1.3, `ratio ${lat.bsp.toFixed(2)}`);
check('repair: monotone carries far less lattice than either hand-rolled case', lat.mono < lat.bil / 3 && lat.mono < lat.smo / 2, `ratio ${lat.mono.toFixed(2)}`);

const jb = edgeJump(bil), jm = edgeJump(mono.at), jp = edgeJump(bsp.at), fs_ = edgeFlat(smo), fm = edgeFlat(mono.at);
check('red case: bilinear slope jumps at a cell edge', jb > 0.2, `relative jump ${jb.toFixed(3)}`);
check('red case: smoothstep slope collapses at a cell edge', fs_ < 0.05, `edge slope / cell slope ${fs_.toFixed(4)}`);
check('C1 at cell edges', jm < 0.02 && jp < 0.02, `relative jump monotone ${jm.toFixed(4)}, bspline ${jp.toFixed(4)}`);
check('monotone keeps slope at cell edges', fm > 0.5, `edge slope / cell slope ${fm.toFixed(3)}`);

/* contract */
let nodeErr = 0;
for (let j = 0; j < R; j++) for (let i = 0; i < C; i++) nodeErr = Math.max(nodeErr, Math.abs(mono.at(i, j) - z[j * C + i]));
check('monotone is interpolating', nodeErr < 1e-9, `max |field - post| over ${C * R} posts ${nodeErr.toExponential(1)}`);
let worstM = 0, worstB = 0, gErr = 0, gMag = 0;
for (let q = 0; q < 20000; q++) {
  const x = 1 + ((q * 0.61803398875) % 1) * (C - 3), y = 1 + ((q * 0.41421356237) % 1) * (R - 3);
  const i = Math.floor(x), j = Math.floor(y);
  const p4 = [post(i, j), post(i + 1, j), post(i, j + 1), post(i + 1, j + 1)];
  const p16 = []; for (let b = -1; b <= 2; b++) for (let a = -1; a <= 2; a++) p16.push(post(i + a, j + b));
  const vm_ = mono.at(x, y), vb = bsp.at(x, y);
  worstM = Math.max(worstM, Math.min(...p4) - vm_, vm_ - Math.max(...p4));
  worstB = Math.max(worstB, Math.min(...p16) - vb, vb - Math.max(...p16));
  const g = bsp.grad(x, y), h = 1e-5;
  const fx = (bsp.at(x + h, y) - bsp.at(x - h, y)) / (2 * h), fy = (bsp.at(x, y + h) - bsp.at(x, y - h)) / (2 * h);
  gErr = Math.max(gErr, Math.abs(g[0] - fx), Math.abs(g[1] - fy)); gMag = Math.max(gMag, Math.abs(fx), Math.abs(fy));
}
check('no overshoot', worstM < 1e-9 && worstB < 1e-9,
  `monotone outside its cell's posts ${worstM.toExponential(1)}, bspline outside its 4x4 posts ${worstB.toExponential(1)}`);
check('bspline gradient is analytic and right', gErr < 1e-4 * gMag, `max |analytic - finite difference| ${gErr.toExponential(1)} (slopes to ${gMag.toFixed(1)})`);
const gm = mono.grad(5.3, 7.7), h = 1e-5;
const fxm = (mono.at(5.3 + h, 7.7) - mono.at(5.3 - h, 7.7)) / (2 * h);
check('monotone gradient', Math.abs(gm[0] - fxm) < 1e-3 * Math.max(1, Math.abs(fxm)), `grad ${gm[0].toFixed(4)} vs ${fxm.toFixed(4)}`);
let t1 = false, t2 = false;
try { AKPOST.field(z, C, R, { mode: 'cubic' }); } catch (e) { t1 = /mode must be/.test(e.message); }
try { AKPOST.field(z.subarray(0, 10), C, R); } catch (e) { t2 = /needs cols \* rows/.test(e.message); }
check('bad calls refused', t1 && t2, "an unknown mode and a short array both throw");
const edge = [mono.at(-3, -3), mono.at(C + 4, R + 4), bsp.at(-1, R + 2)];
check('outside is held, never NaN', edge.every(Number.isFinite) && Math.abs(edge[0] - z[0]) < 1e-9 && Math.abs(edge[1] - z[C * R - 1]) < 1e-9,
  `corners ${edge[0].toFixed(2)} = ${z[0].toFixed(2)}, ${edge[1].toFixed(2)} = ${z[C * R - 1].toFixed(2)}`);

console.log(fails ? `FIELD SAMPLER: BROKEN (${fails})` : 'FIELD SAMPLER: HOLDS');
process.exit(fails ? 1 : 0);
