const ctx2d = new Proxy({}, { get: (t, k) => (k in t ? t[k] : () => ({ addColorStop() {} })), set: (t, k, v) => { t[k] = v; return true; } });
globalThis.document = { createElement: () => ({ width: 0, height: 0, getContext: () => ctx2d }) };
/* tests/akblock_verify.mjs -- hermetic checks on assets/js/akblock.js (2026-09-27, the Codex review of
 * PR #404): an explicit bearing of 0 is honoured, each lake gets its own surface at its own level,
 * the documented `section` member is returned, and a block reaching outside the DEM throws instead
 * of rendering the missing ground as flat sea. Run: node tests/akblock_verify.mjs */
import * as THREE from '../assets/js/three.module.min.js';
import { init } from '../assets/js/akblock.js';
const B = init(THREE);
/* a synthetic 40x40 DEM: two flat lakes at 100 m and 300 m, land 500 m elsewhere */
const cols = 40, rows = 40, z = new Int16Array(cols * rows).fill(500);
for (let j = 5; j < 12; j++) for (let i = 5; i < 12; i++) z[j * cols + i] = 100;
for (let j = 25; j < 32; j++) for (let i = 25; i < 32; i++) z[j * cols + i] = 300;
const meta = { cols, rows, west: 0, north: 0.04, dlon: 0.001, dlat: 0.001 };
const dem = { meta, z };
const o = { origin: [0.002, 0.003], u: [0, 3.0], v: [0, 3.0], step: 0.02, ve: 1, lakes: [
  { level: 100, tol: 1, bbox: [0, 0, 1, 1] }, { level: 300, tol: 1, bbox: [0, 0, 1, 1] }] };
let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
const f0 = B.frame([0, 0], 0); ok(Math.abs(f0.ey - 1) < 1e-9, 'bearing 0 points u north');
const blk = B.build(dem, Object.assign({ bearing: 90, sectionEdge: 'v1', sectionMaterial: new THREE.MeshBasicMaterial() }, o));
const ys = blk.lakes.map(m => m.geometry.getAttribute('position').getY(0));
ok(blk.lakes.length === 2 && Math.abs(ys[0] - 0.102) < 1e-3 && Math.abs(ys[1] - 0.302) < 1e-3, 'each lake at its own level ' + ys.map(v => v.toFixed(3)));
ok(blk.section === blk.walls.v1, 'section is the named wall');
let threw = false; try { B.build(dem, Object.assign({ bearing: 90 }, o, { u: [0, 10] })); } catch (e) { threw = e instanceof RangeError; }
ok(threw, 'an extent outside the DEM throws instead of fabricating sea');
process.exit(fails ? 1 : 0);
