/* akkusko.js — THE FLOWN LINE bench (No.92, 2026-10-21).
 *
 * WHAT IT OWNS. The data and the furniture the nine frames of No.92 share, and
 * no composition: loading the DGGS Kuskokwim survey assets, sampling the 500 m
 * residual magnetic and terrain grids, the one real flight line every frame
 * carries as its rail (the panorama spine), the field colour ramp, a feathered
 * reserve punch for type, and the fixtures. Each slide draws its own picture.
 *
 * DATA. assets/geo/ak-kuskokwim-mag.{bin,json}: residual magnetic intensity
 * (nT) then terrain (m), int16, 500 m UTM zone 4N, from DGGS GPR 2026-1 and
 * 2026-2. assets/geo/ak-kuskokwim-surveys.json: the five 2026 survey outlines
 * and every flown line in UTM km. Nothing here invents a value: a cell with no
 * data is NaN and draws nothing.
 *
 * THE FLOWN LINE. McGrath line index 1003 in the surveys asset: a straight east
 * to west line at northing 6,917.8 km, easting 659.211 to 463.751 km, 195.46 km
 * long, about 62.4 N. km 0 is its east end. Frame n of 9 shows km
 * (n - 1) L / 9 to n L / 9 across the full frame width at 9720 / L px per km, so
 * global x = (n - 1) * 1080 + local x and every seam is exact by construction.
 *
 * USAGE
 *   <script src="@@ASSETS@@/js/akcolor.js"></script>
 *   <script src="@@ASSETS@@/js/akkusko.js"></script>
 *   const G = await AKK.load('@@ASSETS@@');
 *   AKK.rail(cx, G, 3);            // frame 3's ninth of the line, in its band
 *   AKK.fixtures(3);               // wordmark, counter, site, coordinates
 */
(function (global) {
  "use strict";
  var AKK = global.AKK || (global.AKK = {});

  AKK.KEY = { azDeg: 180, elDeg: 16 };   // the late October noon sun at McGrath, a drawing property
  AKK.MOTIF = { xE: 659.211, xW: 463.751, y: 6917.8, L: 195.46 };
  AKK.RAIL = { top: 1080, base: 1222, bottom: 1236, pxPerNT: 0.10, floorNT: -150,
               tickTop: 1240, tickBottom: 1254 };
  AKK.PLACES_UTM = { bethel: [350.01, 6742.79], galena: [598.69, 7180.35] };  // pyproj EPSG 32604
  AKK.COORDS = "62°23'N · 157°49'W";                         // the line's midpoint

  AKK.load = async function (assets) {
    var hj = await (await fetch(assets + '/geo/ak-kuskokwim-mag.json')).json();
    var buf = await (await fetch(assets + '/geo/ak-kuskokwim-mag.bin')).arrayBuffer();
    var raw = new Int16Array(buf), n = hj.cols * hj.rows;
    var mag = new Float32Array(n), dtm = new Float32Array(n);
    for (var i = 0; i < n; i++) {
      mag[i] = raw[i] === -32768 ? NaN : raw[i];
      dtm[i] = raw[n + i] === -32768 ? NaN : raw[n + i];
    }
    var surveys = await (await fetch(assets + '/geo/ak-kuskokwim-surveys.json')).json();
    var by = {};
    surveys.surveys.forEach(function (s) { by[s.id] = s; });
    var line = await (await fetch(assets + '/geo/ak-kuskokwim-line.json')).json();
    return { h: hj, mag: mag, dtm: dtm, surveys: surveys.surveys, by: by, line: line };
  };

  /* Bilinear sample of a grid at UTM km; NaN where any corner is missing. */
  AKK.sample = function (G, grid, xkm, ykm) {
    var h = G.h, i = (xkm * 1000 - h.x0) / h.cell - 0.5, j = (h.y1 - ykm * 1000) / h.cell - 0.5;
    var i0 = Math.floor(i), j0 = Math.floor(j);
    if (i0 < 0 || j0 < 0 || i0 + 1 >= h.cols || j0 + 1 >= h.rows) return NaN;
    var fx = i - i0, fy = j - j0, c = h.cols, k = j0 * c + i0;
    return grid[k] * (1 - fx) * (1 - fy) + grid[k + 1] * fx * (1 - fy) +
           grid[k + c] * (1 - fx) * fy + grid[k + c + 1] * fx * fy;
  };

  /* The flown line's field at km from its east end: linear between the 0.1 km
   * samples of ak-kuskokwim-line.json (100 m DGGS grids). NaN off the line. */
  AKK.lineAt = function (G, km) {
    var v = G.line.nT, f = km / G.line.step_km, i = Math.floor(f);
    if (i < 0 || i >= v.length - 1) return (i === v.length - 1 && v[i] != null) ? v[i] : NaN;
    if (v[i] == null || v[i + 1] == null) return NaN;
    return v[i] + (v[i + 1] - v[i]) * (f - i);
  };
  /* The flown line's profile from km a to km b, every step km. */
  AKK.profile = function (G, a, b, step) {
    var out = [];
    for (var km = a; km <= b + 1e-9; km += step) out.push([km, AKK.lineAt(G, km)]);
    return out;
  };

  /* Field colour: the deck ramp in OKLab, deep caesius to slate to glacier ice. */
  AKK.LUT = null;
  AKK.ramp = function (t) {
    if (!AKK.LUT) AKK.LUT = AKC.gradientMapLUT(['#1B3550', '#5C7488', '#BFD9EE'], [0, 0.45, 1]);
    var v = Math.max(0, Math.min(255, Math.round(t * 255))) * 3, L = AKK.LUT;
    return [L[v], L[v + 1], L[v + 2]];
  };
  /* Map nT to 0..1 with the grid's own spread (p1 -203, p50 -25, p99 502). */
  AKK.nt01 = function (v) {
    var s = v < -25 ? 0.45 * (v + 203) / 178 : 0.45 + 0.55 * (v + 25) / 527;
    return Math.max(0, Math.min(1, s));
  };

  /* THE RAIL. Frame n (1..9) draws its ninth of the flown line in the band
   * y RAIL.top to RAIL.bottom: a ground-filled ridge, a lit lip under the crest,
   * the gold crest as ONE stroke, and the gold aircraft tick at local x 540 in
   * the tick strip below. Returns the km window and the tick's km so the slide
   * can declare the tick on data-scale. */
  AKK.rail = function (cx, G, n, o) {
    o = o || {};
    var R = AKK.RAIL, L = AKK.MOTIF.L, a = (n - 1) * L / 9, b = n * L / 9, pxkm = 1080 / (L / 9);
    var step = o.step || 0.1, pts = AKK.profile(G, a - 0.2, b + 0.2, step);
    function X(km) { return (km - a) * pxkm; }
    function Y(v) { return R.base - (v - R.floorNT) * R.pxPerNT; }
    var P = pts.filter(function (p) { return isFinite(p[1]); }).map(function (p) { return [X(p[0]), Y(p[1])]; });
    cx.save();
    // body: ground fill from the crest down to the band floor
    var g = cx.createLinearGradient(0, R.top, 0, R.bottom);
    g.addColorStop(0, '#1C2B3C'); g.addColorStop(0.55, '#0E1722'); g.addColorStop(1, '#070B11');
    cx.beginPath(); cx.moveTo(P[0][0], R.bottom);
    P.forEach(function (p) { cx.lineTo(p[0], p[1]); });
    cx.lineTo(P[P.length - 1][0], R.bottom); cx.closePath();
    cx.fillStyle = g; cx.fill();
    // lit lip: the face just under the crest catches the key, brighter where it faces it
    // ONE continuous path, round joins: a lip stroked segment by segment beads at every sample
    cx.lineJoin = 'round'; cx.lineCap = 'round';
    cx.beginPath(); cx.moveTo(P[0][0], P[0][1] + 3);
    for (var i = 1; i < P.length; i++) cx.lineTo(P[i][0], P[i][1] + 3);
    cx.strokeStyle = 'rgba(191,217,238,0.26)'; cx.lineWidth = 5; cx.stroke();
    cx.strokeStyle = 'rgba(191,217,238,0.12)'; cx.lineWidth = 11; cx.stroke();
    // the gold crest, one path, one stroke
    cx.beginPath(); cx.moveTo(P[0][0], P[0][1]);
    for (var k = 1; k < P.length; k++) cx.lineTo(P[k][0], P[k][1]);
    cx.strokeStyle = '#FFC72C'; cx.lineWidth = o.crest || 2.2; cx.stroke();
    cx.strokeStyle = '#FFDA6E'; cx.lineWidth = 0.8; cx.stroke();
    // the aircraft tick
    var tx = o.tickX != null ? o.tickX : 540;
    if (tx !== false) {
      cx.beginPath(); cx.moveTo(tx, R.tickTop); cx.lineTo(tx + 7, R.tickBottom); cx.lineTo(tx - 7, R.tickBottom);
      cx.closePath(); cx.fillStyle = '#FFC72C'; cx.fill();
    }
    cx.restore();
    return { kmFrom: a, kmTo: b, pxPerKm: pxkm, tickKm: a + tx / pxkm, tickX: tx,
             crestY: function (x) { return Y(AKK.lineAt(G, a + x / pxkm)); } };
  };

  /* data-scale entry for the tick strip, so qa.py audits the one mark in it. */
  AKK.railScale = function (r) {
    return { what: "the flown line, km from its east end", axis: "x", unit: "km",
             from: [0, +r.kmFrom.toFixed(2)], to: [1080, +r.kmTo.toFixed(2)],
             band: [AKK.RAIL.tickTop - 2, AKK.RAIL.tickBottom + 2],  // [1238, 1256]
             marks: [{ at: r.tickX, means: "the survey aircraft on the flown line, km " + r.tickKm.toFixed(1) }] };
  };

  /* A feathered reserve: blurred rectangles of the ground colour painted over a
   * finished art layer, so type sits on quiet ground. It PAINTS rather than
   * erases: an erased reserve shows the page background, and once the frame is
   * graded the lifted ground around it no longer matches, which prints the
   * reserve as a box. Painting before the grade keeps one tone. */
  AKK.punch = function (cx, rects, o) {
    o = o || {};
    var W = 1080, H = 1350, s = 2, off = document.createElement('canvas');
    off.width = W * s; off.height = H * s;
    var g = off.getContext('2d'); g.scale(s, s);
    // never sharper than 40 px: a tighter falloff prints the reserve as a slab on textured art
    g.filter = 'blur(' + Math.max(40, o.blur || 28) + 'px)';
    g.fillStyle = o.color || '#070B11';
    g.globalAlpha = o.strength != null ? o.strength : 0.92;
    rects.forEach(function (r) { g.fillRect(r[0], r[1], r[2], r[3]); });
    g.filter = 'none';
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
    cx.globalCompositeOperation = 'source-over';
    cx.drawImage(off, 0, 0); cx.restore();
  };

  /* Fixtures, at z-index 9 above every canvas. */
  AKK.fixtures = function (n, o) {
    o = o || {};
    var css = 'position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;';
    function add(html, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', css + style); d.textContent = html;
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    add('ALASKA.AI', 'left:80px;top:76px;font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:24px;letter-spacing:0.06em;color:#F4F8FF;');
    add((n < 10 ? '0' : '') + n + ' / 09', 'right:80px;top:78px;font-size:24px;letter-spacing:0.04em;color:#8C9DAB;font-variant-numeric:tabular-nums;');
    add('alaskaaihq.com', 'left:80px;top:1281px;font-size:19px;letter-spacing:0.04em;color:#66788A;', true);
    if (o.coords !== false)
      add(AKK.COORDS, 'right:80px;top:1281px;font-size:19px;letter-spacing:0.04em;color:#66788A;', true);
  };

  /* Grain as a DOM tile, one cell per device pixel. */
  AKK.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.05));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 280, strength: o.strength || 44, seed: o.seed || 92 });
    return d;
  };

  /* UTM km to screen for a plan view: s px per km, (ox, oy) the screen point of (x0, y0) km. */
  AKK.plan = function (x0, y0, s, ox, oy) {
    return function (x, y) { return [ox + (x - x0) * s, oy - (y - y0) * s]; };
  };
})(typeof window !== "undefined" ? window : this);
