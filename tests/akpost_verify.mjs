// akpost_verify.mjs -- AKPOST.grade's bloom and tone table, held on fixtures
// (2026-10-11, weekly machine pass).
//
//   node tests/akpost_verify.mjs        # exit 0 = every check holds
//
// It runs the REAL assets/js/akpost.js in Node on a stub 2D context (grade only
// reads and writes ImageData), and the committed versions it replaced from git,
// so each check is shown to fail on the code it guards against.
//
//  1. BLOOM OVER ONE-PIXEL EMITTERS (queued 2026-10-10, No.83 slide 05). A
//     dark plate with 1 px lights at a 3 px pitch, the shape of 15,141 lit
//     beads. Bloom took one pixel per 4 x 4 block and wrote each block back as
//     a flat square, so its light changed only at block edges and printed
//     4 to 6 px tiles. Held: of the bloom's column-to-column change on the
//     plate, the share that lands on a 4 px block edge is under 0.5 (smooth is
//     about 0.25; the old bloom measures about 1).
//  2. THE TONE TABLE IN THE SHADOWS (the in-run fix 02c6abf3, No.84 slide 08).
//     The table was indexed linearly in linear light, so every value under about
//     sRGB 10 fell in one bin and a dark gradient graded into hard steps. Held:
//     a ramp of sRGB 0 to 40 grades monotone, with no jump over 4 levels between
//     neighbouring inputs (the old table jumps about 15 at once).
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(ROOT, "assets", "js", "akpost.js");

function load(path) {
  delete require.cache[require.resolve(path)];
  delete globalThis.AKPOST;
  require(path);
  return globalThis.AKPOST;
}

function committed(rev) {
  try {
    const text = execFileSync("git", ["-C", ROOT, "show", rev + ":assets/js/akpost.js"],
      { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
    const f = join(mkdtempSync(join(tmpdir(), "akpost-")), "akpost.cjs");
    writeFileSync(f, text);
    return { text, P: load(f) };
  } catch (e) { return null; }
}

function ctxOf(W, H, fill) {
  const data = new Uint8ClampedArray(W * H * 4);
  for (let i = 0; i < W * H; i++) {
    const v = fill(i % W, (i / W) | 0);
    data[i * 4] = data[i * 4 + 1] = data[i * 4 + 2] = v; data[i * 4 + 3] = 255;
  }
  const img = { data, width: W, height: H };
  return {
    canvas: { width: W, height: H }, img,
    getTransform: () => ({ a: 1 }), setTransform: () => {},
    getImageData: () => img, putImageData: () => {},
  };
}

const PLAIN = { filmic: false, saturation: 1, contrast: 1, dither: false };
const W = 256, H = 96, PITCH = 3;
const isDot = (x, y) => x % PITCH === 1 && y % PITCH === 1;

function bloomEdgeShare(P) {
  const lit = (x, y) => (isDot(x, y) ? 255 : 12);
  const a = ctxOf(W, H, lit), b = ctxOf(W, H, lit);
  P.grade(a, Object.assign({ w: W, h: H }, PLAIN));
  P.grade(b, Object.assign({ w: W, h: H, bloom: { threshold: 0.7, strength: 0.6, radius: 8 } }, PLAIN));
  let at = 0, tot = 0;
  for (let y = 8; y < H - 8; y++) {
    if (y % PITCH === 1) continue;                     // rows of plate only
    for (let x = 8; x < W - 9; x++) {
      if (isDot(x, y) || isDot(x + 1, y)) continue;
      const i = (y * W + x) * 4, j = i + 4;
      const d = Math.abs((b.img.data[j] - a.img.data[j]) - (b.img.data[i] - a.img.data[i]));
      tot += d;
      if ((x + 1) % 4 === 0) at += d;
    }
  }
  let lift = 0, n = 0;
  for (let y = 8; y < H - 8; y++) for (let x = 8; x < W - 8; x++)
    if (!isDot(x, y)) { lift += b.img.data[(y * W + x) * 4] - a.img.data[(y * W + x) * 4]; n++; }
  return { share: tot > 0 ? at / tot : 0, tot, lift: lift / n };
}

function rampSteps(P) {
  const RW = 41;   // one column per input level, sRGB 0..40
  const c = ctxOf(RW, 4, (x) => x);
  P.grade(c, { w: RW, h: 4, dither: false });
  const out = [];
  for (let x = 0; x < RW; x++) out.push(c.img.data[(RW + x) * 4 + 1]);
  let maxJump = 0, monotone = true;
  for (let x = 1; x < RW; x++) {
    maxJump = Math.max(maxJump, out[x] - out[x - 1]);
    if (out[x] < out[x - 1]) monotone = false;
  }
  return { out, maxJump, monotone };
}

const bad = [];
const P = load(SRC);

const bl = bloomEdgeShare(P);
console.log(`bloom: ${bl.share.toFixed(2)} of its change on 4 px block edges, mean lift ${bl.lift.toFixed(2)} levels`);
if (bl.lift < 0.5) bad.push(`1. the fixture blooms nothing (mean lift ${bl.lift.toFixed(2)})`);
if (bl.share >= 0.5) bad.push(`1. bloom is still blocky: ${bl.share.toFixed(2)} of its change on block edges`);
const headP = committed("HEAD");
if (headP && /const si = \(\(y \* ds\) \* W \+ \(x \* ds\)\) \* 4;/.test(headP.text)) {
  const old = bloomEdgeShare(headP.P);
  console.log(`bloom at HEAD (point-sampled): ${old.share.toFixed(2)} on block edges`);
  if (old.share < 0.8) bad.push(`1. the point-sampled bloom measures ${old.share.toFixed(2)}: the fixture would not catch it`);
}

const rp = rampSteps(P);
console.log(`tone table: sRGB 0..40 grades to ${rp.out.slice(0, 16).join(",")}..., max jump ${rp.maxJump}`);
if (!rp.monotone) bad.push("2. the graded ramp is not monotone");
if (rp.maxJump > 4) bad.push(`2. the graded ramp jumps ${rp.maxJump} levels between neighbouring inputs`);
const preLut = committed("02c6abf3^");
if (preLut) {
  const old = rampSteps(preLut.P);
  console.log(`tone table before 02c6abf3: max jump ${old.maxJump}`);
  if (old.maxJump <= 4) bad.push(`2. the linear-indexed table jumps only ${old.maxJump}: the fixture would not catch it`);
}

if (bad.length) {
  console.log("BROKEN");
  for (const b of bad) console.log(" - " + b);
  process.exit(1);
}
console.log("HOLDS: bloom over one-pixel emitters is smooth across its blocks, and a dark ramp grades without steps.");
