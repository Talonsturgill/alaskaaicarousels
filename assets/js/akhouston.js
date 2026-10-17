/* akhouston.js — the ground under ADL 234762, for No.88's land plates (Alaska.Ai, 2026-10-16). Classic script.
 *
 * Projection, terrain and the parcel outline; the drawing is each slide's own.
 *   const G = await AKHOUSTON.load('@@ASSETS@@');                      // DEM, parcel, PLSS sections
 *   const V = AKHOUSTON.view({lon0, lat0, kmPx, x0, y0});              // a local equirectangular view
 *   V.xy(lon, lat) -> [x, y] design px;  V.ll(x, y) -> [lon, lat]
 *   const hgt = AKHOUSTON.heightSampler(G, V, region, 4)              // metres, bilinear on a 4 px grid
 *   AKHOUSTON.parcelPath(ctx, G, V)                                    // adds every ring as a subpath, no beginPath
 *
 * The parcel outline is TRACED by eye from DNR's vicinity map onto the PLSS grid and georeferenced by an
 * affine fit to BLM section centroids; it encloses 19,733 acres against DNR's stated 19,950 (about 1 percent),
 * so every slide that draws it labels it as after DNR's map. The DEM is AWS terrain tiles at zoom 12.
 */
(function (global) {
  "use strict";
  const H = {};
  const KM_PER_DEG_LAT = 111.32;
  H.load = async function (assets) {
    const meta = await (await fetch(assets + '/geo/ak-houston-dem.json')).json();
    const buf = await (await fetch(assets + '/geo/ak-houston-dem.bin')).arrayBuffer();
    const parcel = await (await fetch(assets + '/geo/ak-houston-adl234762.geo.json')).json();
    const plss = await (await fetch(assets + '/geo/ak-houston-plss.geo.json')).json();
    return { meta, dem: new Int16Array(buf), parcel, plss };
  };
  H.demAt = function (G, lon, lat) {
    const m = G.meta, fx = (lon - m.west) / m.dlon - 0.5, fy = (m.north - lat) / m.dlat - 0.5;
    const i = Math.max(0, Math.min(m.cols - 2, Math.floor(fx))), j = Math.max(0, Math.min(m.rows - 2, Math.floor(fy)));
    const tx = Math.max(0, Math.min(1, fx - i)), ty = Math.max(0, Math.min(1, fy - j)), d = G.dem, c = m.cols;
    const a = d[j * c + i], b = d[j * c + i + 1], e = d[(j + 1) * c + i], f = d[(j + 1) * c + i + 1];
    return (a * (1 - tx) + b * tx) * (1 - ty) + (e * (1 - tx) + f * tx) * ty;
  };
  H.view = function (o) {
    const coslat = Math.cos(o.lat0 * Math.PI / 180), pxPerDegLat = KM_PER_DEG_LAT * o.kmPx, pxPerDegLon = pxPerDegLat * coslat;
    return {
      kmPx: o.kmPx, lon0: o.lon0, lat0: o.lat0, x0: o.x0, y0: o.y0,
      xy: (lon, lat) => [o.x0 + (lon - o.lon0) * pxPerDegLon, o.y0 - (lat - o.lat0) * pxPerDegLat],
      ll: (x, y) => [o.lon0 + (x - o.x0) / pxPerDegLon, o.lat0 - (y - o.y0) / pxPerDegLat],
      pxPerM: o.kmPx / 1000
    };
  };
  H.heightSampler = function (G, V, region, cell) {
    cell = cell || 4;
    const [rx, ry, rw, rh] = region, cols = Math.ceil(rw / cell) + 3, rows = Math.ceil(rh / cell) + 3, g = new Float32Array(cols * rows);
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { const [lon, lat] = V.ll(rx + (i - 1) * cell, ry + (j - 1) * cell); g[j * cols + i] = H.demAt(G, lon, lat); }
    return function (x, y) {
      const fx = (x - rx) / cell + 1, fy = (y - ry) / cell + 1;
      const i = Math.max(0, Math.min(cols - 2, Math.floor(fx))), j = Math.max(0, Math.min(rows - 2, Math.floor(fy))), tx = Math.max(0, Math.min(1, fx - i)), ty = Math.max(0, Math.min(1, fy - j));
      const a = g[j * cols + i], b = g[j * cols + i + 1], c = g[(j + 1) * cols + i], d = g[(j + 1) * cols + i + 1];
      return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty;
    };
  };
  H.rings = function (G, V) { return G.parcel.features[0].geometry.coordinates.map(r => r.map(p => V.xy(p[0], p[1]))); };
  H.parcelPath = function (ctx, G, V) { for (const r of H.rings(G, V)) { r.forEach((p, k) => k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); } };
  H.inParcel = function (G, V) {
    const rings = H.rings(G, V);
    function inRing(r, x, y) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; }
    return (x, y) => { if (!inRing(rings[0], x, y)) return false; for (let k = 1; k < rings.length; k++) if (inRing(rings[k], x, y)) return false; return true; };
  };
  H.HOUSTON = [-149.773719, 61.608309];   // the City of Houston (No.88 C86)
  global.AKHOUSTON = H;
})(window);
