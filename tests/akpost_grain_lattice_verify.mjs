// akpost_grain_lattice_verify.mjs -- AKPOST.grade's grain has no fixed lattice at
// its default size (2026-11-08, weekly machine pass; queue item 2026-11-03).
//
//   node tests/akpost_grain_lattice_verify.mjs     # exit 0 = every check holds
//
// THE DEFECT. grade()'s grain is bilinear value noise on a cell of `size`
// DEVICE px. A pixel on a cell corner carries one random value at full
// variance; a pixel between corners carries an average of two or four values
// at a half or a quarter of it. At size 2 that is a fixed 2 px lattice of
// strong and weak pixels, and three critics named "a square cell lattice" in
// No.104's near-black fields (03, 04 and 09, round 2). Size 1 cured each frame.
// The header's example said size 2 and builders copied it.
//
// THE MEASURE. Grade a flat sRGB 60 plate with grain only (no dither, no tone
// curve), take the grain's change per pixel, and compare its variance across
// the phase classes (x mod p, y mod p): the largest class variance over the
// smallest. White grain reads about 1.0 at any p; a lattice of period p reads
// about 4 at p = 2.
//
// HELD:
//  1. grain with NO size (the default) measures under 1.25 at p = 2 and p = 3.
//  2. grain passed size 2 measures over 2.5 at p = 2 (the fixture sees the
//     lattice, so check 1 is not passing on a measure that can't see one).
//     Sizes 3 and 4 are printed too: each carries a lattice of its own period
//     (3.1 and 4.0 on 2026-11-08), which is why akpost's header says so.
//  3. the committed akpost.js before this pass (cdb8d61b), graded with no size,
//     measures over 2.5 at p = 2: the old default printed the lattice. Skipped
//     with a note when git history is not available.
// It runs the REAL assets/js/akpost.js in Node on a stub 2D context.
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(ROOT, "assets", "js", "akpost.js");
const BEFORE = "cdb8d61b";

function load(path) {
  delete require.cache[require.resolve(path)];
  delete globalThis.AKPOST;
  require(path);
  return globalThis.AKPOST;
}

function at(rev) {
  try {
    const text = execFileSync("git", ["-C", ROOT, "show", rev + ":assets/js/akpost.js"],
      { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
    const f = join(mkdtempSync(join(tmpdir(), "akpost-grain-")), "akpost.cjs");
    writeFileSync(f, text);
    return load(f);
  } catch (e) { return null; }
}

function plate(W, H, v) {
  const data = new Uint8ClampedArray(W * H * 4);
  for (let i = 0; i < W * H; i++) {
    data[i * 4] = data[i * 4 + 1] = data[i * 4 + 2] = v; data[i * 4 + 3] = 255;
  }
  const img = { data, width: W, height: H };
  return {
    canvas: { width: W, height: H }, img,
    getTransform: () => ({ a: 1 }), setTransform: () => {},
    getImageData: () => img, putImageData: () => {},
  };
}

const W = 384, H = 384, LEVEL = 60;
const PLAIN = { filmic: false, saturation: 1, contrast: 1, dither: false, sharpen: 0,
  vignette: 0 };

function lattice(P, grain, p) {
  const c = plate(W, H, LEVEL);
  P.grade(c, Object.assign({ w: W, h: H, grain }, PLAIN));
  const sum = new Float64Array(p * p), sq = new Float64Array(p * p), n = new Float64Array(p * p);
  for (let y = 4; y < H - 4; y++) {
    for (let x = 4; x < W - 4; x++) {
      const d = c.img.data[(y * W + x) * 4 + 1] - LEVEL;
      const k = (y % p) * p + (x % p);
      sum[k] += d; sq[k] += d * d; n[k] += 1;
    }
  }
  const v = [];
  for (let k = 0; k < p * p; k++) v.push(sq[k] / n[k] - (sum[k] / n[k]) ** 2);
  const lo = Math.min(...v), hi = Math.max(...v);
  return { ratio: lo > 0 ? hi / lo : Infinity, hi, lo };
}

const bad = [];
const P = load(SRC);
const g = { amount: 0.08, seed: 20261108 };

for (const p of [2, 3]) {
  const r = lattice(P, g, p);
  console.log(`default grain, period ${p}: phase variance ratio ${r.ratio.toFixed(2)} (${r.lo.toFixed(2)} to ${r.hi.toFixed(2)} levels^2)`);
  if (!(r.ratio < 1.25)) bad.push(`1. the default grain has a period-${p} lattice (ratio ${r.ratio.toFixed(2)})`);
  if (r.hi < 0.5) bad.push(`1. the fixture grain is too faint to measure (variance ${r.hi.toFixed(2)})`);
}
for (const s of [2, 3, 4]) {
  const r = lattice(P, Object.assign({ size: s }, g), s);
  console.log(`grain size ${s}, period ${s}: phase variance ratio ${r.ratio.toFixed(2)}`);
  if (s === 2 && !(r.ratio > 2.5)) bad.push(`2. size 2 measures ${r.ratio.toFixed(2)}: the fixture can't see the lattice`);
}
const old = at(BEFORE);
if (old) {
  const r = lattice(old, g, 2);
  console.log(`akpost.js at ${BEFORE}, no size, period 2: phase variance ratio ${r.ratio.toFixed(2)}`);
  if (!(r.ratio > 2.5)) bad.push(`3. the pre-pass default measures ${r.ratio.toFixed(2)}: the fixture would not catch it`);
} else {
  console.log(`(git history for ${BEFORE} not available: check 3 skipped)`);
}

if (bad.length) {
  console.log("BROKEN");
  for (const b of bad) console.log(" - " + b);
  process.exit(1);
}
console.log("HOLDS: the default grain is white, with no fixed lattice; size 2 still prints one and is now opt-in.");
