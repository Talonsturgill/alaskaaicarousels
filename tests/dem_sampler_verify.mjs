#!/usr/bin/env node
/* Does a hillshade taken off the house DEM samplers print the cell lattice?
 * (2026-09-27, run No.70)
 *
 * No.70's slide 02 shaded the Kachemak DEM per device pixel at 8.1 device px
 * per DEM cell. With a 3 x 3 presmooth it scored well; the craft cycle dropped
 * the presmooth and the frame REGRESSED to a visible grid, because the gradient
 * of a bilinear surface is constant along each cell edge and jumps across it.
 * The repair in the engine is a C1 sampler (a monotone Steffen bicubic, which
 * replaced Catmull-Rom after Codex's review of PR #404): AKS.loadDEM(...)
 * .sampleCubic and AKBLOCK.sampler(dem, 'cubic').
 *
 * This measures the lattice directly on the real DEM, on slide 02's own
 * geometry, and holds four things:
 *   1. INTERPOLATING. Both cubic samplers return every DEM value exactly at the
 *      cell centres (no height invented or flattened), and agree with each other.
 *   2. C1. Across a cell edge the cubic gradient is continuous; bilinear jumps.
 *   3. THE RED CASE. Bilinear shading at 8.1 px per cell carries a strong
 *      cell-period component in its shade (the regression, reconstructed).
 *   4. THE REPAIR. Cubic shading, with NO presmooth, carries less lattice than
 *      the shipped bilinear-plus-presmooth version, and keeps more real relief.
 *
 *    node tests/dem_sampler_verify.mjs          exit 0 HOLDS, exit 1 BROKEN
 */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const base = path.join(ROOT, 'assets/geo/ak-kachemak-dem');
const meta = JSON.parse(fs.readFileSync(base + '.json', 'utf8'));
const raw = fs.readFileSync(base + '.bin');
const z = new Int16Array(raw.buffer, raw.byteOffset, raw.length / 2);

/* akblock.js, as a slide imports it */
const AKBLOCK = (await import(path.join(ROOT, 'assets/js/akblock.js'))).init(null);
const demB = { meta, z };
const bil = AKBLOCK.sampler(demB), cubB = AKBLOCK.sampler(demB, 'cubic');

/* akscribe.js, as a slide loads it: a classic script on window */
const win = {};
const fakeFetch = async (u) => ({
  json: async () => meta,
  arrayBuffer: async () => raw.buffer.slice(raw.byteOffset, raw.byteOffset + raw.length),
});
vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'assets/js/akscribe.js'), 'utf8'),
  { window: win, fetch: fakeFetch, console, Math, Float32Array, Int16Array });
const demS = await win.AKS.loadDEM('ignored');
const cubS = demS.sampleCubic;

let fails = 0;
const check = (name, ok, detail) => { console.log(`[${ok ? 'HOLD' : 'BROKEN'}] ${name}: ${detail}`); if (!ok) fails++; };

/* 1. interpolating at nodes, and the two implementations agree */
let nodeErr = 0, agree = 0;
for (let q = 0; q < 4000; q++) {
  const i = 2 + Math.floor((q * 7919) % (meta.cols - 4)), j = 2 + Math.floor((q * 104729) % (meta.rows - 4));
  const lon = meta.west + i * meta.dlon, lat = meta.north - j * meta.dlat;
  nodeErr = Math.max(nodeErr, Math.abs(cubB(lon, lat) - z[j * meta.cols + i]), Math.abs(cubS(lon, lat) - z[j * meta.cols + i]));
  const lo2 = lon + 0.37 * meta.dlon, la2 = lat - 0.61 * meta.dlat;
  agree = Math.max(agree, Math.abs(cubB(lo2, la2) - cubS(lo2, la2)));
}
check('interpolating', nodeErr < 1e-6 && agree < 1e-6,
  `max |cubic - DEM| at 4000 nodes ${nodeErr.toExponential(1)} m, akblock vs akscribe ${agree.toExponential(1)} m`);
check('outside is NaN', Number.isNaN(cubB(meta.west - 1, meta.north)) && Number.isNaN(cubS(meta.west - 1, meta.north)),
  'both cubic samplers return NaN off the grid');
let threw = false; try { AKBLOCK.sampler(demB, 'bicubic'); } catch (e) { threw = /AK CONTRACT/.test(e.message); }
check('unknown mode refused', threw, "AKBLOCK.sampler(dem, 'bicubic') throws an AK CONTRACT error");

/* 2. C1: slope just either side of a cell edge, over the lake basin's ridges */
function edgeJump(S) {
  let jump = 0, mag = 0; const h = 1e-4 * meta.dlon;
  for (let q = 0; q < 2000; q++) {
    const i = 400 + (q % 200), j = 250 + Math.floor(q / 200) * 13;
    const lonE = meta.west + i * meta.dlon, lat = meta.north - (j + 0.5) * meta.dlat;
    const gL = (S(lonE - h, lat) - S(lonE - 2 * h, lat)) / h, gR = (S(lonE + 2 * h, lat) - S(lonE + h, lat)) / h;
    jump += Math.abs(gR - gL); mag += Math.abs(gR) + Math.abs(gL);
  }
  return jump / (mag / 2);
}
const jb = edgeJump(bil), jc = edgeJump(cubB);
/* Why monotone and not Catmull-Rom (Codex on PR #404, measured on this DEM):
 * Catmull-Rom overshot in 11 percent of random samples, by up to 46 m, and 629
 * in 400,000 dipped below 0 m between posts all at or above it (a fake
 * shoreline). Clamping it to each cell's four posts cost C1 (jump 0.06) and
 * tore the surface at cell edges (246 m against 293 m across row 617).
 * Clamping each pass to its two central posts was continuous but flattened
 * every sampled peak (jump 0.18). Steffen keeps all three properties. */
check('C1 at cell edges', jc < 0.02 && jb > 0.2,
  `relative slope jump across an edge: bilinear ${jb.toFixed(3)}, cubic ${jc.toFixed(4)}`);

/* monotone: a cubic sample never leaves the range of its own cell's four posts */
let worst = 0;
for (let q = 0; q < 20000; q++) {
  const x = 1 + ((q * 0.61803398875) % 1) * (meta.cols - 3), y = 1 + ((q * 0.41421356237) % 1) * (meta.rows - 3);
  const i = Math.floor(x), j = Math.floor(y), k = j * meta.cols + i;
  const posts = [z[k], z[k + 1], z[k + meta.cols], z[k + meta.cols + 1]];
  const lon = meta.west + x * meta.dlon, lat = meta.north - y * meta.dlat;
  for (const v of [cubB(lon, lat), cubS(lon, lat)]) worst = Math.max(worst, Math.min(...posts) - v, v - Math.max(...posts));
}
check('no overshoot', worst < 1e-6, `worst excursion outside the cell's posts ${worst.toExponential(1)} m over 20000 samples`);

/* 3 and 4. slide 02's own geometry and shading, on a 1200 x 360 device-px strip over the relief */
const W = 1080, H = 1350, MAPY = 560, KM = 45, LAT0 = 59.725;
const KX = Math.cos(LAT0 * Math.PI / 180) * 111.32, KY = 111.2, CLON = -150.872, CLAT = 59.712;
const LON = (x) => CLON + (x - W / 2) / (KX * KM), LAT = (y) => CLAT - (y - MAPY - (H - MAPY) / 2) / (KY * KM);
const PX0 = 400, PY0 = 300, PW = 1200, PH = 360;          // device px, inside the relief
const lights = [[315, 38, 0.6], [345, 38, 0.22], [285, 38, 0.18]].map(([az, el, w]) => {
  const a = az * Math.PI / 180, e = el * Math.PI / 180;
  return [Math.sin(a) * Math.cos(e), Math.cos(a) * Math.cos(e), Math.sin(e), w];
});
function shade(height) {
  const hg = new Float64Array((PW + 2) * (PH + 2));
  for (let y = -1; y <= PH; y++) for (let x = -1; x <= PW; x++) {
    const v = height(LON((PX0 + x) / 2), LAT(MAPY + (PY0 + y) / 2));
    hg[(y + 1) * (PW + 2) + x + 1] = Number.isFinite(v) ? v : 0;
  }
  const Hh = (x, y) => hg[(y + 1) * (PW + 2) + x + 1], cellM = 1000 / (KM * 2), out = new Float64Array(PW * PH);
  for (let y = 0; y < PH; y++) for (let x = 0; x < PW; x++) {
    const dzdx = (Hh(x + 1, y) - Hh(x - 1, y)) / (2 * cellM), dzdy = (Hh(x, y - 1) - Hh(x, y + 1)) / (2 * cellM);
    let nx = -dzdx, ny = -dzdy, nz = 1; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
    let sh = 0; for (const L of lights) sh += Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]) * L[3];
    out[y * PW + x] = sh;
  }
  return out;
}
/* slide 02's shipped presmooth: 3 x 3 taps at 0.0012 by 0.0006 degrees, centre weight 2 */
const presmooth = (S) => (lo, la) => {
  let e = 0, n = 0;
  for (const a of [-1, 0, 1]) for (const b of [-1, 0, 1]) {
    const v = S(lo + a * 0.0012, la + b * 0.0006); if (Number.isFinite(v)) { const w = a || b ? 1 : 2; e += v * w; n += w; }
  }
  return n ? e / n : 0;
};
/* The lattice, measured: the shade's column-to-column change, folded by the
 * DEM cell's phase along x. A surface with no lattice folds flat (ratio ~1);
 * a bilinear gradient jump piles up at one phase. Reported as the folded
 * profile's max over its mean. Detail is the mean |change| itself: real relief. */
const cellPx = meta.dlon * KX * KM * 2;
function lattice(sh) {
  const BINS = 16, acc = new Float64Array(BINS), cnt = new Float64Array(BINS); let tot = 0, n = 0;
  for (let y = 0; y < PH; y++) for (let x = 1; x < PW; x++) {
    const d = Math.abs(sh[y * PW + x] - sh[y * PW + x - 1]);
    const lonMid = LON((PX0 + x - 0.5) / 2), ph = ((lonMid - meta.west) / meta.dlon) % 1;
    const b = Math.min(BINS - 1, Math.floor(ph * BINS)); acc[b] += d; cnt[b]++; tot += d; n++;
  }
  const prof = [...acc].map((a, k) => a / cnt[k]), mean = tot / n;
  return { ratio: Math.max(...prof) / mean, detail: mean };
}
const L_bil = lattice(shade(bil)), L_pre = lattice(shade(presmooth(bil))), L_cub = lattice(shade(cubB));
const L_cubS = lattice(shade(cubS));
console.log(`  cell = ${cellPx.toFixed(2)} device px; lattice ratio (1.0 = none) / detail (mean |d shade| per px)`);
console.log(`  bilinear, no presmooth   ${L_bil.ratio.toFixed(2)} / ${L_bil.detail.toFixed(5)}   (the craft-cycle regression)`);
console.log(`  bilinear + 3x3 presmooth ${L_pre.ratio.toFixed(2)} / ${L_pre.detail.toFixed(5)}   (what shipped)`);
console.log(`  cubic, no presmooth      ${L_cub.ratio.toFixed(2)} / ${L_cub.detail.toFixed(5)}   (akblock)`);
console.log(`  cubic, no presmooth      ${L_cubS.ratio.toFixed(2)} / ${L_cubS.detail.toFixed(5)}   (akscribe)`);
check('red case: bilinear prints the lattice', L_bil.ratio > 2.0,
  `bilinear lattice ratio ${L_bil.ratio.toFixed(2)} at ${cellPx.toFixed(1)} px per cell`);
check('repair: cubic carries less lattice than the shipped presmooth', L_cub.ratio < L_pre.ratio && L_cub.ratio < 1.5,
  `cubic ${L_cub.ratio.toFixed(2)} vs bilinear+presmooth ${L_pre.ratio.toFixed(2)}`);
check('repair keeps real relief', L_cub.detail > L_pre.detail,
  `detail cubic ${L_cub.detail.toFixed(5)} vs presmooth ${L_pre.detail.toFixed(5)}`);
check('akscribe cubic matches akblock cubic', Math.abs(L_cubS.ratio - L_cub.ratio) < 1e-9, 'same lattice reading');

/* continuous across every cell edge (Codex round 4 on PR #404): a single clamp to
 * each cell's own four posts jumped 246 m to 293 m across row 617 at column
 * 505.6367, within 2e-7 of a cell. Probe that exact spot, then 20000 edges. */
const eps = 2e-7;
let seam = 0, seamAt = '';
const probe = (S, x, y, dx, dy) => {
  const at = (xx, yy) => S(meta.west + xx * meta.dlon, meta.north - yy * meta.dlat);
  const d = Math.abs(at(x - dx, y - dy) - at(x + dx, y + dy));
  if (d > seam) { seam = d; seamAt = `col ${x.toFixed(4)} row ${y.toFixed(4)}`; }
};
for (const S of [cubB, cubS]) {
  probe(S, 505.6367, 617, 0, eps);
  for (let q = 0; q < 10000; q++) {
    const e = 2 + (q * 7919) % (meta.rows - 4), f = 2 + ((q * 0.7548776662) % 1) * (meta.cols - 4);
    probe(S, f, e, 0, eps);                                   // across a row edge
    probe(S, 2 + (q * 104729) % (meta.cols - 4), 2 + ((q * 0.5698402910) % 1) * (meta.rows - 4), eps, 0);  // across a column edge
  }
}
check('continuous across cell edges', seam < 0.01, `worst jump across an edge ${seam.toExponential(1)} m (${seamAt})`);

/* every committed DEM's bounds are its outermost SAMPLE CENTRES (Codex on PR #404):
 * east = west + (cols - 1) dlon, south = north - (rows - 1) dlat. Bounds one cell
 * out sent AKS.relief's edge clamp to a NaN, which it drew as sea level. */
const geo = path.join(ROOT, 'assets/geo');
const badBounds = [];
for (const f of fs.readdirSync(geo).filter(f => /dem\.json$/.test(f))) {
  const mm = JSON.parse(fs.readFileSync(path.join(geo, f), 'utf8'));
  if (mm.dlon == null || mm.east == null) continue;
  const eE = mm.west + (mm.cols - 1) * mm.dlon, eS = mm.north - (mm.rows - 1) * mm.dlat;
  if (Math.abs(mm.east - eE) > mm.dlon / 100 || Math.abs(mm.south - eS) > mm.dlat / 100) badBounds.push(`${f} east ${mm.east} vs ${eE.toFixed(6)}, south ${mm.south} vs ${eS.toFixed(6)}`);
}
check('DEM bounds are sample centres', !badBounds.length, badBounds.length ? badBounds.join('; ') : 'every assets/geo/*dem.json');

console.log(fails ? `DEM SAMPLER: BROKEN (${fails})` : 'DEM SAMPLER: HOLDS');
process.exit(fails ? 1 : 0);
