/* akcorridor.js — the Railbelt corridor bench (added 2026-10-07, No.80).
 *
 * Shared furniture for a deck about the Alaska Intertie and the proposed
 * Beluga-Healy line: committed DEM sampling with a bicubic (Catmull-Rom)
 * reader in lon/lat, the AEA transmission geometry with the Intertie picked
 * out, the named stops of the proposed line, the gazetteer's military
 * installations, and the deck fixtures (locator strip, counter, watermark,
 * wordmark). Classic script, global AKCOR. Requires d3 for the locator strip.
 *
 * HONESTY: the proposed line has no published route. `stops` are the places
 * the Alaska delegation named, in order; nothing here interpolates between
 * them, and West Susitna has no coordinates on purpose.
 */
(function (global) {
  "use strict";
  const AKCOR = {};

  /* ---- DEM ------------------------------------------------------------- */
  // name: 'ak-corridor149-dem' | 'ak-denali-dem' | 'ak-cookinlet-dem' ...
  // Returns {meta, raw, at(i,j), sample(lon,lat) -> metres (monotone bicubic)}.
  AKCOR.loadDEM = async function (assets, name) {
    const meta = await (await fetch(assets + '/geo/' + name + '.json')).json();
    const raw = new Int16Array(await (await fetch(assets + '/geo/' + name + '.bin')).arrayBuffer());
    const C = meta.cols, R = meta.rows;
    // a truncated or mismatched pair would read undefined past the tail and put NaN into the terrain quietly
    if (raw.length !== C * R) throw new Error('AK CONTRACT: DEM ' + name + ' has ' + raw.length + ' cells, meta says ' + C * R);
    const at = (i, j) => raw[Math.min(R - 1, Math.max(0, j)) * C + Math.min(C - 1, Math.max(0, i))];
    // Steffen's monotone cubic (Steffen 1990, A&A 239, 443), as in akscribe.js and akblock.js: it never leaves
    // the cell's own posts, so it can't invent peaks or pits between DEM samples the way Catmull-Rom does.
    const stTan = (a, b, c) => { const s0 = b - a, s1 = c - b; return (Math.sign(s0) + Math.sign(s1)) * Math.min(Math.abs(s0), Math.abs(s1), Math.abs(s0 + s1) / 4); };
    const st = (y0, y1, y2, y3, t) => { const d1 = stTan(y0, y1, y2), d2 = stTan(y1, y2, y3), t2 = t * t, t3 = t2 * t;
      return (2 * t3 - 3 * t2 + 1) * y1 + (t3 - 2 * t2 + t) * d1 + (-2 * t3 + 3 * t2) * y2 + (t3 - t2) * d2; };
    const atF = (fi, fj) => {
      const i = Math.floor(fi), j = Math.floor(fj), tx = fi - i, ty = fj - j, r = [];
      for (let m = -1; m < 3; m++) r.push(st(at(i - 1, j + m), at(i, j + m), at(i + 1, j + m), at(i + 2, j + m), tx));
      return st(r[0], r[1], r[2], r[3], ty);
    };
    const inside = (lon, lat) => lon >= meta.west && lon <= meta.east && lat >= meta.south && lat <= meta.north;
    const sample = (lon, lat) => atF((lon - meta.west) / meta.dlon, (meta.north - lat) / meta.dlat);
    return { meta, raw, at, atF, sample, inside };
  };

  /* ---- lines, stops, bases --------------------------------------------- */
  // AEA layer 15 (>= 69 kV). The Alaska Intertie is the 138 kV segment from
  // Willow (-150.042, 61.7369) to Healy (-148.6994, 63.8345); it is returned
  // Willow first. Everything else is context.
  AKCOR.loadLines = async function (assets) {
    const t = await (await fetch(assets + '/geo/ak-transmission-69kv.geo.json')).json();
    const lines = t.lines;
    const isIntertie = l => l.kv === 138 && l.pts.length > 20 &&
      l.pts.some(p => Math.abs(p[0] + 150.042) < 1e-3 && Math.abs(p[1] - 61.7369) < 1e-3) &&
      l.pts.some(p => Math.abs(p[0] + 148.6994) < 1e-3 && Math.abs(p[1] - 63.8345) < 1e-3);
    let intertie = null;
    for (const l of lines) if (isIntertie(l)) { intertie = l.pts.slice(); break; }
    if (!intertie) throw new Error('AK CONTRACT: akcorridor: Intertie segment not found in the AEA layer');
    if (intertie[0][1] > intertie[intertie.length - 1][1]) intertie.reverse();
    const railbelt = lines.filter(l => l.pts.every(p => p[0] > -152 && p[0] < -145.2 && p[1] > 59.4 && p[1] < 65.2));
    return { lines, railbelt, intertie };
  };
  // The named stops of the proposed Beluga-Healy line, in order (C12).
  // West Susitna is a region with no point; it is carried as a name only.
  AKCOR.stops = [
    { name: 'BELUGA', at: [-150.9859, 61.19] },
    { name: 'WEST SUSITNA', at: null },
    { name: 'WILLOW', at: [-150.042, 61.7369] },
    { name: 'HEALY', at: [-148.6994, 63.8345] },
  ];
  AKCOR.bases = [
    { name: 'JBER', at: [-149.7458, 61.2536] },
    { name: 'CLEAR', at: [-149.1875, 64.2903] },
    { name: 'EIELSON', at: [-147.1017, 64.6658] }   // assets/geo/alaska-places.json,
  ];
  // Great-circle-ish length in km along a lon/lat polyline (small spans).
  AKCOR.lengthKm = function (pts) {
    let s = 0;
    for (let k = 1; k < pts.length; k++) {
      const a = pts[k - 1], b = pts[k], la = (a[1] + b[1]) / 2 * Math.PI / 180;
      s += Math.hypot((b[0] - a[0]) * 111.32 * Math.cos(la), (b[1] - a[1]) * 110.57);
    }
    return s;
  };
  // Point at fraction f (0..1) of a polyline's length, and the cumulative list.
  AKCOR.along = function (pts) {
    const cum = [0];
    for (let k = 1; k < pts.length; k++) cum.push(cum[k - 1] + AKCOR.lengthKm([pts[k - 1], pts[k]]));
    const L = cum[cum.length - 1];
    function at(f) {
      const d = Math.max(0, Math.min(1, f)) * L;
      let k = 1; while (k < cum.length - 1 && cum[k] < d) k++;
      const t = (d - cum[k - 1]) / Math.max(1e-9, cum[k] - cum[k - 1]);
      return [pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * t, pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * t];
    }
    function fractionOf(lonlat) {   // nearest vertex fraction
      let best = 0, bd = 1e9;
      pts.forEach((p, k) => { const dd = Math.hypot(p[0] - lonlat[0], p[1] - lonlat[1]); if (dd < bd) { bd = dd; best = k; } });
      return cum[best] / L;
    }
    return { cum, L, at, fractionOf };
  };

  /* ---- fixtures -------------------------------------------------------- */
  // Every frame: wordmark top right, counter bottom right, the site watermark
  // bottom centre, coordinates beside it, and the locator strip (device D1).
  // state.bracket: 'all' | 'willow-healy' | 'beluga-healy' | 'bases' | 'crest'
  //                | 'healy-eielson'.  state.light: type colour set for a light frame.
  // state.wordmark === false: the frame carries its own (the close).
  AKCOR.fixtures = function (rail, no, total, state) {
    state = state || {};
    const light = !!state.light;
    const ink = light ? '#24323F' : '#C9D6E2';
    const dim = light ? '#5B6874' : '#5E6E7C';
    const root = document.createElement('div');
    root.className = 'akcor-fixtures';
    root.innerHTML = (state.wordmark === false ? '' :
      '<div class="akcor-wordmark" style="position:absolute;right:80px;top:84px;font:400 26px \'Instrument Serif\';letter-spacing:0.06em;color:' + ink + '">ALASKA.AI</div>') +
      '<div class="akcor-counter" style="position:absolute;right:80px;top:1234px;font:500 24px \'JetBrains Mono\';letter-spacing:0.08em;color:' + ink + ';font-variant-numeric:tabular-nums">' +
      '<span style="color:#FFC72C' + (light ? ';background:#24323F;padding:0 6px;border-radius:3px' : '') + '">' + String(no).padStart(2, '0') + '</span> / ' + String(total).padStart(2, '0') + '</div>' +
      '<div data-decorative class="akcor-site" style="position:absolute;left:0;right:0;top:1296px;text-align:center;font:400 19px \'JetBrains Mono\';letter-spacing:0.06em;color:' + dim + '">alaskaaihq.com' +
      (state.coords ? '&nbsp;&nbsp;·&nbsp;&nbsp;' + state.coords : '') + '</div>';
    document.body.appendChild(root);
    // locator strip: the corridor oriented to the line, south left, north right
    const W = 232, H = 56, X0 = 80, Y0 = 1252;
    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('data-decorative', '');
    svg.setAttribute('width', W); svg.setAttribute('height', H);
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.style.cssText = 'position:absolute;left:' + X0 + 'px;top:' + Y0 + 'px;overflow:visible';
    // canonical projection, then rotated by hand so the Intertie runs left
    // (Willow, south) to right (Healy, north), then fitted to the strip.
    const base = d3.geoConicEqualArea().parallels([55, 65]).rotate([154, 0]).scale(1000).translate([0, 0]);
    const ib = rail.intertie[0], ie = rail.intertie[rail.intertie.length - 1];
    const pa = base(ib), pb = base(ie), ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]);
    const ca = Math.cos(-ang), sa = Math.sin(-ang);
    const rot = ll => { const q = base(ll); return [q[0] * ca - q[1] * sa, q[0] * sa + q[1] * ca]; };
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    const keep = rail.railbelt.filter(l => l.pts.every(p => p[0] < -146.5));   // the Railbelt proper, not Copper Valley
    for (const l of keep) for (const p of l.pts) { const q = rot(p); x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); }
    for (const b of AKCOR.bases) { const q = rot(b.at); x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); }
    const k = Math.min((W - 8) / (x1 - x0), (H - 12) / (y1 - y0));
    const ox = (W - (x1 - x0) * k) / 2 - x0 * k, oy = (H - (y1 - y0) * k) / 2 - y0 * k;
    const proj = ll => { const q = rot(ll); return [q[0] * k + ox, q[1] * k + oy]; };
    const path = { };
    const d = pts => pts.map((p, i) => (i ? 'L' : 'M') + proj(p)[0].toFixed(1) + ' ' + proj(p)[1].toFixed(1)).join('');
    const add = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); return e; };
    for (const l of keep) add('path', { d: d(l.pts), fill: 'none', stroke: light ? '#8A96A2' : '#3A4B5E', 'stroke-width': 1 });
    add('path', { d: d(rail.intertie), fill: 'none', stroke: '#FFC72C', 'stroke-width': 1.8, 'stroke-linecap': 'round' });
    // the bases take the military ink only where the frame's own ink law admits it
    let mil = true;
    try { mil = !JSON.parse(document.body.dataset.ink || '[]').some(k => k.hex.toUpperCase() === '#6EA5FF' && k.state === 'absent'); } catch (e) { mil = true; }
    for (const b of AKCOR.bases) { const p = proj(b.at);
      if (mil) add('circle', { cx: p[0], cy: p[1], r: 2.6, fill: '#6EA5FF' });
      else add('circle', { cx: p[0], cy: p[1], r: 2.4, fill: 'none', stroke: light ? '#5B6874' : '#7F8FA0', 'stroke-width': 1.1 }); }
    if (state.stops) for (const s of AKCOR.stops) if (s.at) { const p = proj(s.at); add('circle', { cx: p[0], cy: p[1], r: 3.2, fill: 'none', stroke: light ? '#24323F' : '#F4F8FF', 'stroke-width': 1 }); }
    // the bracket: what this frame covers
    const bx = { all: [0, W], 'willow-healy': [proj(ib)[0], proj(ie)[0]], 'beluga-healy': [proj(AKCOR.stops[0].at)[0], proj(ie)[0]],
      bases: [proj(AKCOR.bases[0].at)[0], proj(AKCOR.bases[2].at)[0]], 'healy-eielson': [proj(ie)[0], proj(AKCOR.bases[2].at)[0]] }[state.bracket || 'all'];
    const by = H + 6;
    if (state.bracket === 'crest') {
      const c = proj([-149.2, 63.35]);
      // the crest as a small caret pointing down at the baseline
      add('path', { d: 'M' + (c[0] - 6) + ' ' + (by - 9) + 'L' + (c[0] + 6) + ' ' + (by - 9) + 'L' + c[0] + ' ' + (by + 1) + 'Z', fill: light ? '#24323F' : '#F4F8FF' });
    } else {
      const a = Math.min(bx[0], bx[1]), b = Math.max(bx[0], bx[1]);
      add('path', { d: 'M' + a + ' ' + (by - 4) + 'V' + by + 'H' + b + 'V' + (by - 4), fill: 'none', stroke: light ? '#24323F' : '#F4F8FF', 'stroke-width': 1.2,
        'stroke-dasharray': state.bracket === 'beluga-healy' ? '4 3' : 'none' });
    }
    document.body.appendChild(svg);
    return { root, svg };
  };

  global.AKCOR = AKCOR;
})(typeof window !== 'undefined' ? window : this);
