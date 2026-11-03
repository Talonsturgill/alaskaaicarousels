/* aksawn.js -- deck furniture for No.103 (2026-11-02), THE SAWN INLET.
 *
 * Shared by the plan and section frames of the CIPLink / DeepGreen deck on
 * purpose: the fixtures, the palette, the grain tile, one cubic DEM reader for
 * ak-cookinlet-dem, one local plan projection so the coast never moves between
 * sheets, a water mask, the land film every plan sheet sits on, and AEA's own
 * transmission layer. None of it composes a slide; each frame owns its art
 * (bespoke_check strips <script src>, so this costs the variety budget nothing).
 *
 *   SAWN.fixtures(n, {dark})          wordmark, counter, site line, coordinates
 *   SAWN.canvas(id, z) / SAWN.layer() 2x-backed canvases, ctx scaled to design px
 *   SAWN.grain({opacity, seed})       AK.grainOn tile above art, below type
 *   SAWN.loadDEM(assets)              {meta, h, at(lon,lat) bilinear, atS(lon,lat) cubic}
 *   SAWN.plan({lon0, lat0, pxPerKm, cx, cy, rot})  xy(lon,lat) / ll(x,y)
 *   SAWN.landFilm(cx, P, dem, o)      device-pixel cubic hillshade of land, water left clear
 *   SAWN.waterMask(P, dem, rect)      1x Uint8Array, 1 where the DEM says sea
 *   SAWN.lines(assets)                AEA transmission lines (>= 69 kV) as [{kv, pts}]
 *   SAWN.cased(cx, pts, P, o)         a cased polyline in plan
 *   SAWN.lightVec(az, el)             az clockwise from up, screen space (+y down)
 *
 * ONE KEY for the deck: az 315, el 28 (upper left), the cartographer's light.
 * DATA HONESTY: heights are the DEM's (AWS terrain tiles, terrarium), sampled
 * with a cubic B-spline for shading only. No noise term touches a height.
 */
(function (global) {
  'use strict';
  var S = {};
  S.W = 1080; S.H = 1350;
  S.KEY = { az: 315, el: 28 };
  S.GOLD = '#FFC72C';
  S.MAGENTA = '#D0458A';
  S.MAGENTA_DIM = '#6B2848';
  S.FMN = '#6EA5FF';
  S.STEEL = '#8D99A3';
  S.COORDS = "60°56'N · 151°09'W";
  S.PAL = { night: '#050B10', elev: '#0A1720', elev2: '#11222E', type: '#F4F8FF', body: '#C9D1D6',
            label: '#A9B8C4', fixture: '#66788A', flourDeep: '#20262A', flour: '#3A3D36',
            flourLit: '#8A8574', foam: '#BDB6A0', sed0: '#2A2C28', sed1: '#3A342C', sed2: '#574D40',
            mud: '#4A3F33', mudLit: '#9A8B74', spruce: '#0F1B17', spruceLit: '#2A3A30',
            snow: '#DCE6EE', snowLee: '#6F8296', shadow: '#0A0F12', film: '#DDE4E8', ink: '#1B2530' };
  /* place names the frames label; positions are the shores the DEM itself draws */
  S.PLACES = { beluga: [-151.02, 61.17], nikiski: [-151.40, 60.70], soldotna: [-151.06, 60.488],
               kenai: [-151.258, 60.554], anchorage: [-149.90, 61.218], tyonek: [-151.137, 61.068] };

  S.lightVec = function (az, el) {
    var a = az * Math.PI / 180, e = el * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  S.layer = function (w, h) {
    var c = document.createElement('canvas');
    c.width = (w || S.W) * 2; c.height = (h || S.H) * 2;
    c.getContext('2d').scale(2, 2);
    return c;
  };

  S.canvas = function (id, z) {
    var c = document.createElement('canvas');
    c.id = id; c.width = S.W * 2; c.height = S.H * 2;
    c.setAttribute('style', 'position:absolute;left:0;top:0;width:' + S.W + 'px;height:' + S.H + 'px;z-index:' + (z || 1) + ';');
    document.body.insertBefore(c, document.body.firstChild);
    var x = c.getContext('2d'); x.scale(2, 2);
    return x;
  };

  function bs(t) {
    var t2 = t * t, t3 = t2 * t, m = 1 - t;
    return [m * m * m / 6, (3 * t3 - 6 * t2 + 4) / 6, (-3 * t3 + 3 * t2 + 3 * t + 1) / 6, t3 / 6];
  }

  S.loadDEM = async function (assets) {
    var base = assets + '/geo/ak-cookinlet-dem';
    var meta = await (await fetch(base + '.json')).json();
    var buf = await (await fetch(base + '.bin')).arrayBuffer();
    var h = new Int16Array(buf);
    if (h.length !== meta.cols * meta.rows) throw new Error('AK CONTRACT: DEM size mismatch');
    function at(lon, lat) {
      var fc = (lon - meta.west) / meta.dlon, fr = (meta.north - lat) / meta.dlat;
      var c0 = Math.max(0, Math.min(meta.cols - 2, Math.floor(fc)));
      var r0 = Math.max(0, Math.min(meta.rows - 2, Math.floor(fr)));
      var u = Math.max(0, Math.min(1, fc - c0)), v = Math.max(0, Math.min(1, fr - r0));
      var i = r0 * meta.cols + c0;
      return h[i] * (1 - u) * (1 - v) + h[i + 1] * u * (1 - v) + h[i + meta.cols] * (1 - u) * v + h[i + meta.cols + 1] * u * v;
    }
    /* cubic B-spline: smooth (C2) and slightly low-passed, so a hillshade of it
     * never prints the DEM's cell lattice (No.96). Shade with atS, mask with at. */
    function atS(lon, lat) {
      var fc = (lon - meta.west) / meta.dlon, fr = (meta.north - lat) / meta.dlat;
      var c0 = Math.floor(fc), r0 = Math.floor(fr), u = fc - c0, v = fr - r0, out = 0;
      var wu = bs(u), wv = bs(v);
      for (var j = -1; j <= 2; j++) {
        var rr = Math.max(0, Math.min(meta.rows - 1, r0 + j)), row = 0;
        for (var i = -1; i <= 2; i++) row += wu[i + 1] * h[rr * meta.cols + Math.max(0, Math.min(meta.cols - 1, c0 + i))];
        out += wv[j + 1] * row;
      }
      return out;
    }
    return { meta: meta, h: h, at: at, atS: atS };
  };

  /* A local plan: equirectangular about (lon0, lat0), pxPerKm, rotated by rot
   * degrees (positive turns the map clockwise on screen). */
  S.plan = function (o) {
    var kx = Math.cos(o.lat0 * Math.PI / 180) * 111.32, ky = 111.2;
    var r = (o.rot || 0) * Math.PI / 180, cr = Math.cos(r), sr = Math.sin(r), k = o.pxPerKm;
    return {
      pxPerKm: k,
      xy: function (lon, lat) {
        var E = (lon - o.lon0) * kx, N = (lat - o.lat0) * ky;
        /* rotate (E, -N) by r */
        var x = E * cr - (-N) * sr, y = E * sr + (-N) * cr;
        return [o.cx + x * k, o.cy + y * k];
      },
      ll: function (x, y) {
        var dx = (x - o.cx) / k, dy = (y - o.cy) / k;
        var E = dx * cr + dy * sr, Nm = -dx * sr + dy * cr;   /* inverse rotation */
        return [o.lon0 + E / kx, o.lat0 - Nm / ky];
      }
    };
  };

  /* 1x water mask over rect [x, y, w, h] (design px): 1 where the DEM is sea. */
  S.waterMask = function (P, dem, rect) {
    var x0 = rect[0], y0 = rect[1], W = rect[2], H = rect[3];
    var m = new Uint8Array(W * H);
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var ll = P.ll(x0 + x + 0.5, y0 + y + 0.5);
      m[y * W + x] = dem.at(ll[0], ll[1]) <= 0.5 ? 1 : 0;
    }
    return { m: m, x: x0, y: y0, w: W, h: H,
             at: function (X, Y) { var i = Math.floor(X - x0), j = Math.floor(Y - y0);
               return (i < 0 || j < 0 || i >= W || j >= H) ? 0 : m[j * W + i]; } };
  };

  /* Smooth coast rings over rect, contoured from the DEM's B-spline heights at
   * the shoreline level (linear-interpolated by d3.contours, then two Chaikin
   * passes), so a coast never steps on the pixel grid. Rings shorter than
   * minPts are dropped (sub-pixel islands and spurs). Needs d3. Design px. */
  S.coastRings = function (P, dem, rect, o) {
    o = o || {};
    var x0 = rect[0], y0 = rect[1], W = rect[2], H = rect[3], lvl = o.level != null ? o.level : 0.5;
    var f = new Float64Array(W * H), samp = dem.atS || dem.at;
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var ll = P.ll(x0 + x + 0.5, y0 + y + 0.5); f[y * W + x] = samp(ll[0], ll[1]);
    }
    var cs = d3.contours().size([W, H]).thresholds([lvl])(Array.from(f));
    var rings = [], minPts = o.minPts || 24, passes = o.passes != null ? o.passes : 2;
    cs[0].coordinates.forEach(function (poly) { poly.forEach(function (ring) {
      if (ring.length < minPts) return;
      var r = ring.map(function (q) { return [q[0] + x0, q[1] + y0]; });
      for (var k = 0; k < passes; k++) {
        var n = [];
        for (var i = 0; i < r.length - 1; i++) {
          var a = r[i], c = r[i + 1];
          n.push([a[0] * 0.75 + c[0] * 0.25, a[1] * 0.75 + c[1] * 0.25], [a[0] * 0.25 + c[0] * 0.75, a[1] * 0.25 + c[1] * 0.75]);
        }
        n.push(n[0]); r = n;
      }
      rings.push(r);
    }); });
    return rings;
  };
  /* Stroke rings as a cased line, casing then core, round joins. */
  S.strokeRings = function (cx, rings, o) {
    o = o || {};
    cx.save(); cx.lineJoin = 'round'; cx.lineCap = 'round';
    var R = o.rect, e = 2;
    function edge(q) { return R && (q[0] <= R[0] + e || q[0] >= R[0] + R[2] - e || q[1] <= R[1] + e || q[1] >= R[1] + R[3] - e); }
    /* a ring closed along the window frame is not coast: lift the pen there */
    function trace() { cx.beginPath(); rings.forEach(function (r) { r.forEach(function (q, i) {
      if (i && !(edge(q) && edge(r[i - 1]))) cx.lineTo(q[0], q[1]); else cx.moveTo(q[0], q[1]); }); }); }
    if (o.casing !== false) { trace(); cx.strokeStyle = o.casing || '#0A0F12'; cx.lineWidth = o.casingWidth || 3.4; cx.stroke(); }
    trace(); cx.strokeStyle = o.color || '#BDB6A0'; cx.lineWidth = o.width || 1.2; cx.stroke();
    cx.restore();
  };

  function hex(hx) { return [parseInt(hx.slice(1, 3), 16), parseInt(hx.slice(3, 5), 16), parseInt(hx.slice(5, 7), 16)]; }
  S.hex = hex;
  function rampAt(stops, t) {
    t = Math.max(0, Math.min(1, t));
    for (var i = 1; i < stops.length; i++) if (t <= stops[i][0]) {
      var a = stops[i - 1], b = stops[i], u = (t - a[0]) / (b[0] - a[0] || 1), ca = hex(a[1]), cb = hex(b[1]);
      return [ca[0] + (cb[0] - ca[0]) * u, ca[1] + (cb[1] - ca[1]) * u, ca[2] + (cb[2] - ca[2]) * u];
    }
    return hex(stops[stops.length - 1][1]);
  }
  S.rampAt = rampAt;

  /* The land film: a device-pixel hillshade of land only, written with
   * putImageData into rect (design px) of the context's canvas. Water pixels
   * are left transparent for the frame's own water treatment. Lambert from the
   * deck key plus a relief term (local height minus its neighbourhood mean,
   * lighting only), mudflats tinted where 0 to 6 m. o.ramp: [[t, hex]]. */
  S.landFilm = function (cx, P, dem, o) {
    o = o || {};
    var rect = o.rect || [0, 0, S.W, S.H];
    var DX = 2, W = rect[2] * DX, H = rect[3] * DX;
    var L = S.lightVec(S.KEY.az, S.KEY.el);
    var ve = o.ve || 6, step = 1 / (P.pxPerKm * DX);   /* km per device px */
    var ramp = o.ramp || [[0, '#0F1B17'], [0.5, '#22302A'], [0.8, '#3A4A3E'], [1, '#6A7868']];
    var img = cx.createImageData(W, H), d = img.data;
    var hcache = new Float32Array((W + 2) * (H + 2)), water = new Uint8Array((W + 2) * (H + 2));
    for (var y = -1; y <= H; y++) for (var x = -1; x <= W; x++) {
      var ll = P.ll(rect[0] + (x + 0.5) / DX, rect[1] + (y + 0.5) / DX);
      var e = dem.atS(ll[0], ll[1]), k = (y + 1) * (W + 2) + (x + 1);
      hcache[k] = e; water[k] = dem.at(ll[0], ll[1]) <= 0.5 ? 1 : 0;
    }
    var mlo = o.mudLo != null ? o.mudLo : 0.5, mhi = o.mudHi != null ? o.mudHi : 7;
    var mud = hex(S.PAL.mud), mudLit = hex(S.PAL.mudLit);
    var maxE = o.maxE || 400;
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) {
      k = (y + 1) * (W + 2) + (x + 1);
      var p = (y * W + x) * 4;
      if (water[k]) { d[p + 3] = 0; continue; }
      var gx = (hcache[k + 1] - hcache[k - 1]) / (2 * step * 1000) * ve;
      var gy = (hcache[k + W + 2] - hcache[k - W - 2]) / (2 * step * 1000) * ve;
      var nz = 1 / Math.sqrt(gx * gx + gy * gy + 1);
      var nx = -gx * nz, ny = -gy * nz;
      var lam = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
      var t = 0.18 + 0.62 * lam + 0.20 * Math.min(1, Math.max(0, hcache[k] / maxE));
      var c = rampAt(ramp, t);
      var eh = hcache[k];
      if (eh < mhi) { var f = 1 - Math.max(0, (eh - mlo) / (mhi - mlo)); f = Math.min(1, f) * 0.85;
        var mc = [mud[0] + (mudLit[0] - mud[0]) * lam, mud[1] + (mudLit[1] - mud[1]) * lam, mud[2] + (mudLit[2] - mud[2]) * lam];
        c = [c[0] + (mc[0] - c[0]) * f, c[1] + (mc[1] - c[1]) * f, c[2] + (mc[2] - c[2]) * f]; }
      var dith = (((x * 7 + y * 13) % 5) - 2) * 0.6;   /* ordered dither against banding */
      d[p] = c[0] + dith; d[p + 1] = c[1] + dith; d[p + 2] = c[2] + dith; d[p + 3] = 255;
    }
    var off = document.createElement('canvas'); off.width = W; off.height = H;
    off.getContext('2d').putImageData(img, 0, 0);
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
    cx.drawImage(off, rect[0] * 2, rect[1] * 2);
    cx.restore();
    return off;
  };

  S.lines = async function (assets) {
    var g = await (await fetch(assets + '/geo/ak-transmission-69kv.geo.json')).json();
    return g.lines;
  };

  S.cased = function (cx, pts, P, o) {
    o = o || {};
    cx.save(); cx.lineJoin = 'round'; cx.lineCap = 'round';
    function path() { cx.beginPath(); pts.forEach(function (q, i) { var p = P ? P.xy(q[0], q[1]) : q; if (i) cx.lineTo(p[0], p[1]); else cx.moveTo(p[0], p[1]); }); }
    if (o.dash) cx.setLineDash(o.dash);
    path(); cx.strokeStyle = o.casing || S.PAL.shadow; cx.lineWidth = (o.width || 2) + (o.case || 2.4) * 2; cx.stroke();
    path(); cx.strokeStyle = o.color || S.STEEL; cx.lineWidth = o.width || 2; cx.stroke();
    cx.restore();
  };

  S.polaris = function (x, y, s, z) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', s); svg.setAttribute('height', s);
    svg.setAttribute('viewBox', '-50 -50 100 100');
    svg.setAttribute('style', 'position:absolute;left:' + (x - s / 2) + 'px;top:' + (y - s / 2) + 'px;z-index:9;overflow:visible;');
    svg.setAttribute('data-decorative', '');
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M0,-50 C4,-14 14,-4 50,0 C14,4 4,14 0,50 C-4,14 -14,4 -50,0 C-14,-4 -4,-14 0,-50 Z');
    p.setAttribute('fill', S.GOLD);
    svg.appendChild(p); document.body.appendChild(svg);
    return svg;
  };

  /* Fixtures at z-index 9. o.light: dark ink for the drafting-film frame. */
  S.fixtures = function (n, o) {
    o = o || {};
    var ink = o.light ? S.PAL.ink : S.PAL.body, fx = o.light ? '#4A5866' : S.PAL.fixture;
    var halo = o.light ? '0 0 6px rgba(221,228,232,0.95)' : '0 0 6px rgba(5,11,16,0.95), 0 0 2px rgba(5,11,16,0.9)';
    var css = 'position:absolute;z-index:9;white-space:nowrap;text-shadow:' + halo + ';';
    function add(txt, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', css + style); d.textContent = txt; d.className = 'fx';
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    add('ALASKA.AI', 'left:80px;top:80px;font-family:"Fraunces",serif;font-variation-settings:"opsz" 36,"SOFT" 0,"WONK" 0;font-weight:600;font-size:24px;letter-spacing:0.10em;color:' + ink + ';');
    add((n < 10 ? '0' : '') + n + ' / 09', 'right:80px;top:82px;font-family:"JetBrains Mono",monospace;font-weight:500;font-size:24px;letter-spacing:0.06em;color:' + (o.light ? S.PAL.ink : S.PAL.label) + ';font-variant-numeric:tabular-nums;');
    add('alaskaaihq.com', 'left:80px;top:1250px;font-family:"JetBrains Mono",monospace;font-size:19px;letter-spacing:0.04em;color:' + fx + ';', true);
    if (o.coords !== false)
      add(S.COORDS, 'right:80px;top:1250px;font-family:"JetBrains Mono",monospace;font-size:18px;letter-spacing:0.04em;color:' + fx + ';', true);
  };

  S.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.08));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 640, strength: o.strength || 40, seed: o.seed || 103 });
    return d;
  };

  S.boxes = function (sel, pad) {
    pad = pad || 0; var out = [];
    document.querySelectorAll(sel).forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.width) out.push([r.left - pad, r.top - pad, r.width + 2 * pad, r.height + 2 * pad]);
    });
    return out;
  };

  global.SAWN = S;
})(window);
