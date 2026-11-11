/* aksand.js -- the sand table under ADL 234762 (Alaska.Ai, run No.111, 2026-11-10). Classic script.
 *
 * One world for every frame of the deck: the real Houston DEM shaped in damp sand inside an oak tray,
 * the July outline and the survey grid as PROJECTED light, and the conveyed 6,800 acres as a gold
 * cord on steel tacks. This module holds the world (geometry, heights, the record's lines, the sand's
 * own texture fields); each slide draws it its own way (GPU, plan relief, column march, raymarch).
 *
 *   const W = await AKSAND.load('@@ASSETS@@');
 *   W.toTable(lon, lat) -> [x, z] metres on the table (x east, z south, origin at the table centre)
 *   W.toLL(x, z)        -> [lon, lat]
 *   W.h(x, z)           -> sand surface height in metres (DEM x RELIEF at the table scale, smoothed)
 *   W.outline           -> the cord path: 28 corners of the conveyed parcel, table metres, closed ring
 *   W.cells             -> 170 quarter-quarter cells [[x0,z0,x1,z1], part] in table metres
 *   W.july              -> the July outline (traced from DNR's map), table metres
 *   W.sections          -> PLSS section rings, table metres
 *   W.grain(x, z)       -> 0..1 fine sand grain field (deterministic)
 *   W.ripple(x, z)      -> -1..1 combed-ripple field, crests running across the lamp
 *
 * SCALE. 1 km of ground = 0.1 m of table (1:10,000). The table window is TABLE_LON x TABLE_LAT below,
 * about 21.7 km by 14.5 km, so the sand bed is about 2.17 m by 1.45 m. Heights are the DEM times
 * RELIEF at the same 1:10,000, so RELIEF 2.5 means the sand stands 2.5 times taller than true scale.
 * Every frame that shows relief prints that number.
 *
 * GEOMETRY SOURCE. ak-houston-ffd-6800.geo.json (the FFD's legal description as 40-acre cells; the
 * R2W Tract A portion traced from DNR's vicinity map) and ak-houston-adl234762.geo.json (the July
 * outline, traced). The cord's 28 corners are the snapped outer boundary of the 170 cells.
 */
(function (global) {
  "use strict";
  const S = {};
  const KM_LAT = 111.32;
  S.TABLE_LON = [-149.93, -149.52];
  S.TABLE_LAT = [61.615, 61.745];
  S.SCALE = 0.1;          // metres of table per km of ground
  S.RELIEF = 2.5;         // vertical exaggeration
  S.LAT0 = 61.68;
  const COS = Math.cos(S.LAT0 * Math.PI / 180);

  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  // value noise on a hashed lattice (Math.imul, never a float product past 2^53: No.107)
  function hash(ix, iy, s) { let h = Math.imul(ix, 374761393) ^ Math.imul(iy, 668265263) ^ Math.imul(s, 1442695041);
    h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
  function vnoise(x, y, s) { const ix = Math.floor(x), iy = Math.floor(y), fx = x - ix, fy = y - iy;
    const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy);
    const a = hash(ix, iy, s), b = hash(ix + 1, iy, s), c = hash(ix, iy + 1, s), d = hash(ix + 1, iy + 1, s);
    return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v; }
  function fbm(x, y, s, o) { let f = 0, a = 0.5, n = 0; for (let i = 0; i < (o || 4); i++) { f += a * vnoise(x, y, s + i * 17); n += a; x *= 2.03; y *= 2.03; a *= 0.5; } return f / n; }
  S.fbm = fbm; S.vnoise = vnoise; S.rng = mulberry;

  S.load = async function (assets) {
    const meta = await (await fetch(assets + '/geo/ak-houston-dem.json')).json();
    const dem = new Int16Array(await (await fetch(assets + '/geo/ak-houston-dem.bin')).arrayBuffer());
    const ffd = await (await fetch(assets + '/geo/ak-houston-ffd-6800.geo.json')).json();
    const july = await (await fetch(assets + '/geo/ak-houston-adl234762.geo.json')).json();
    const plss = await (await fetch(assets + '/geo/ak-houston-plss.geo.json')).json();
    const lon0 = (S.TABLE_LON[0] + S.TABLE_LON[1]) / 2, lat0 = (S.TABLE_LAT[0] + S.TABLE_LAT[1]) / 2;
    const W = { meta, lon0, lat0, scale: S.SCALE, relief: S.RELIEF };
    W.width = (S.TABLE_LON[1] - S.TABLE_LON[0]) * KM_LAT * COS * S.SCALE;
    W.depth = (S.TABLE_LAT[1] - S.TABLE_LAT[0]) * KM_LAT * S.SCALE;
    W.toTable = (lon, lat) => [(lon - lon0) * KM_LAT * COS * S.SCALE, -(lat - lat0) * KM_LAT * S.SCALE];
    W.toLL = (x, z) => [lon0 + x / (KM_LAT * COS * S.SCALE), lat0 - z / (KM_LAT * S.SCALE)];
    // DEM, bicubic-free: bilinear on a pre-smoothed copy (a 3x3 box) so the lattice never prints in the sand
    const C = meta.cols, Rr = meta.rows, sm = new Float32Array(C * Rr);
    for (let j = 0; j < Rr; j++) for (let i = 0; i < C; i++) { let s = 0, n = 0;
      for (let dj = -2; dj <= 2; dj++) for (let di = -2; di <= 2; di++) { const jj = j + dj, ii = i + di;
        if (jj >= 0 && jj < Rr && ii >= 0 && ii < C) { const w = (3 - Math.abs(di)) * (3 - Math.abs(dj)); s += dem[jj * C + ii] * w; n += w; } }
      sm[j * C + i] = s / n; }
    // Catmull-Rom bicubic (2026-11-10 round 1): bilinear gave heights that were continuous but normals
    // that jumped at every 53 m cell edge, so every per-pixel hillshade printed the DEM lattice as blocks.
    const cr = (p0, p1, p2, p3, t) => p1 + 0.5 * t * (p2 - p0 + t * (2 * p0 - 5 * p1 + 4 * p2 - p3 + t * (3 * (p1 - p2) + p3 - p0)));
    const at = (i, j) => sm[Math.max(0, Math.min(Rr - 1, j)) * C + Math.max(0, Math.min(C - 1, i))];
    W.demAt = function (lon, lat) {
      const fx = (lon - meta.west) / meta.dlon - 0.5, fy = (meta.north - lat) / meta.dlat - 0.5;
      const i = Math.max(0, Math.min(C - 2, Math.floor(fx))), j = Math.max(0, Math.min(Rr - 2, Math.floor(fy)));
      const tx = Math.max(0, Math.min(1, fx - i)), ty = Math.max(0, Math.min(1, fy - j));
      const row = (jj) => cr(at(i - 1, jj), at(i, jj), at(i + 1, jj), at(i + 2, jj), tx);
      return cr(row(j - 1), row(j), row(j + 1), row(j + 2), ty);
    };
    const BASE = 60;   // metres; the lowest ground in the window sits a little above the bed
    W.h = function (x, z) { const ll = W.toLL(x, z); return (W.demAt(ll[0], ll[1]) - BASE) / 1000 * S.SCALE * S.RELIEF; };
    W.grain = (x, z) => vnoise(x * 2600, z * 2600, 11) * 0.6 + vnoise(x * 900, z * 900, 12) * 0.4;
    W.ripple = function (x, z) {   // combed ripples, crests running roughly north-south, wavelength 9 mm
      const warp = fbm(x * 9, z * 9, 21, 3) * 0.02;
      return Math.sin((x + warp + 0.004 * Math.sin(z * 40)) / 0.009 * 2 * Math.PI);
    };
    // sinuous ripples for the GPU texture frames (2026-11-10 round 1): a straight sine at 9 mm read as a
    // pinstripe moire at 4-6 px on 01 and 09. Longer wavelength, crests that bend, amplitude in patches.
    W.ripple2 = function (x, z) {
      const th = 0.55 * (fbm(x * 1.4, z * 1.4, 27, 2) - 0.5);
      const u = x * Math.cos(th) + z * Math.sin(th);
      const ph = u / 0.015 + 2.2 * fbm(x * 11, z * 11, 23, 3);
      const s = Math.sin(ph * 2 * Math.PI) + 0.28 * Math.sin(ph * 4 * Math.PI + 0.9);
      const m = 0.25 + 0.75 * Math.max(0, Math.min(1, (fbm(x * 3.2, z * 3.2, 29, 3) - 0.32) / 0.3));
      return s * m / 1.2;
    };
    // the record
    const outF = ffd.features.find(f => f.properties.part === 'outline');
    W.outline = outF.geometry.coordinates[0].map(p => W.toTable(p[0], p[1]));
    W.lattice = outF.properties.lattice;
    W.cells = [];
    ffd.features.forEach((f, k) => { if (f.properties.part === 'outline') return;
      for (const poly of f.geometry.coordinates) { const r = poly[0].map(p => W.toTable(p[0], p[1]));
        const xs = r.map(p => p[0]), zs = r.map(p => p[1]);
        W.cells.push({ x0: Math.min(...xs), x1: Math.max(...xs), z0: Math.min(...zs), z1: Math.max(...zs), part: k, plat: f.properties.plat, acres: f.properties.stated_acres }); } });
    W.parts = ffd.features.filter(f => f.properties.part !== 'outline').map(f => f.properties);
    W.july = july.features[0].geometry.coordinates.map(r => r.map(p => W.toTable(p[0], p[1])));
    W.sections = plss.features.map(f => ({ id: f.properties.plss + ':' + f.properties.sec, ring: f.geometry.coordinates[0].map(p => W.toTable(p[0], p[1])) }));
    W.HOUSTON = W.toTable(-149.773719, 61.608309);
    // point in conveyed parcel (cells) and in July outline
    W.inParcel = (x, z) => W.cells.some(c => x >= c.x0 && x <= c.x1 && z >= c.z0 && z <= c.z1);
    W.inJuly = function (x, z) { const r = W.july[0]; let c = false;
      for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, zi] = r[i], [xj, zj] = r[j];
        if ((zi > z) !== (zj > z) && x < (xj - xi) * (z - zi) / (zj - zi) + xi) c = !c; } return c; };
    // the cord: tacks at the 28 corners, cord height above the sand
    W.tackHeight = 0.012;
    W.tacks = W.outline.slice(0, -1).map(p => [p[0], W.h(p[0], p[1]), p[1]]);
    return W;
  };

  /* Sand texture canvases for the GPU frames: albedo (damp low ground darker, grain), bump (ripples
   * + grain), emissive (the projected record). size in px for the full table. */
  S.textures = function (W, o) {
    o = o || {};
    const N = o.size || 2048, M = Math.round(N * W.depth / W.width);
    function mk() { const c = document.createElement('canvas'); c.width = N; c.height = M; return c; }
    const alb = mk(), bmp = mk(), ax = alb.getContext('2d'), bx = bmp.getContext('2d');
    const ai = ax.createImageData(N, M), bi = bx.createImageData(N, M);
    const lit = o.sand || [205, 187, 151], damp = o.damp || [128, 116, 92];
    for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) {
      const x = (i / N - 0.5) * W.width, z = (j / M - 0.5) * W.depth;
      const hh = W.h(x, z), g = W.grain(x, z), wet = Math.max(0, Math.min(1, 1 - hh / 0.012)) * (0.55 + 0.45 * fbm(x * 6, z * 6, 31, 3));
      const k = (j * N + i) * 4, t = 0.9 + 0.2 * g;
      for (let ch = 0; ch < 3; ch++) ai.data[k + ch] = Math.min(255, (lit[ch] * (1 - wet * 0.55) + damp[ch] * wet * 0.55) * t);
      ai.data[k + 3] = 255;
      const b = 128 + 50 * W.ripple2(x, z) + 22 * (g - 0.5);
      bi.data[k] = bi.data[k + 1] = bi.data[k + 2] = Math.max(0, Math.min(255, b)); bi.data[k + 3] = 255;
    }
    ax.putImageData(ai, 0, 0); bx.putImageData(bi, 0, 0);
    return { albedo: alb, bump: bmp, px: (x, z) => [(x / W.width + 0.5) * N, (z / W.depth + 0.5) * M], N, M };
  };

  /* A projector canvas the same size as the textures: the caller draws lines into it with px(). */
  S.projectorCanvas = function (W, T) { const c = document.createElement('canvas'); c.width = T.N; c.height = T.M; return c; };

  global.AKSAND = S;
})(window);
