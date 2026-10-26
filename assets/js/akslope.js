/* akslope.js -- deck furniture for No.96 (2026-10-25), the North Slope gas deck.
 *
 * Committed 2026-10-25. Shared by all nine slides on purpose: the fixtures,
 * the grain tile, the North Slope DEM loader and the text-box router. None of
 * it draws a slide; each frame owns its own art (bespoke_check measures that).
 *
 *   SLOPE.fixtures(n, {ink, counter, site, coords, display})
 *   SLOPE.grain({opacity, strength, seed})
 *   SLOPE.canvas(id, z)            a 2x-backed full-frame canvas, ctx scaled
 *   SLOPE.layer(w, h)              an offscreen 2x canvas
 *   SLOPE.loadDEM(base, name)      {meta, h:Int16Array, at(lon,lat), ...}
 *   SLOPE.boxes(sel, pad)          design-px rects of type, to route art
 *   SLOPE.lightVec(az, el)         az clockwise from up, screen space
 */
(function (global) {
  'use strict';
  var S = {};
  S.W = 1080; S.H = 1350;
  S.GOLD = '#FFC72C';
  S.COORDS = "70°15'N · 148°20'W";
  S.PAL = { type: '#F4F8FF', body: '#C9D3DA', label: '#A7B6C1', fixture: '#66788A' };

  S.lightVec = function (az, el) {
    var a = az * Math.PI / 180, e = el * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  S.layer = function (w, h) {
    var c = document.createElement('canvas');
    c.width = (w || S.W) * 2; c.height = (h || S.H) * 2;
    var x = c.getContext('2d'); x.scale(2, 2);
    return c;
  };

  S.canvas = function (id, z) {
    var c = document.createElement('canvas');
    c.id = id; c.width = S.W * 2; c.height = S.H * 2;
    c.setAttribute('style', 'position:absolute;left:0;top:0;width:' + S.W + 'px;height:' + S.H + 'px;z-index:' + (z || 1) + ';');
    document.body.appendChild(c);
    var x = c.getContext('2d'); x.scale(2, 2);
    return x;
  };

  function bs(t) {
    var t2 = t * t, t3 = t2 * t, m = 1 - t;
    return [m * m * m / 6, (3 * t3 - 6 * t2 + 4) / 6, (-3 * t3 + 3 * t2 + 3 * t + 1) / 6, t3 / 6];
  }
  function hh(a, b) { var q = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return q - Math.floor(q); }
  S.hash = hh;

  S.loadDEM = async function (base, name) {
    var meta = await (await fetch(base + '/geo/' + name + '.json')).json();
    var buf = await (await fetch(base + '/geo/' + name + '.bin')).arrayBuffer();
    var h = new Int16Array(buf);
    function at(lon, lat) {
      var fc = (lon - meta.west) / meta.dlon - 0.5, fr = (meta.north - lat) / meta.dlat - 0.5;
      var c0 = Math.max(0, Math.min(meta.cols - 2, Math.floor(fc)));
      var r0 = Math.max(0, Math.min(meta.rows - 2, Math.floor(fr)));
      var u = Math.max(0, Math.min(1, fc - c0)), v = Math.max(0, Math.min(1, fr - r0));
      var i = r0 * meta.cols + c0;
      return h[i] * (1 - u) * (1 - v) + h[i + 1] * u * (1 - v) + h[i + meta.cols] * (1 - u) * v + h[i + meta.cols + 1] * u * v;
    }
    // cubic B-spline sampling: bilinear has a kink at every cell edge, and a hillshade of
    // it prints the DEM's lattice as facets (No.96 round 1, every terrain frame)
    function atS(lon, lat) {
      var fc = (lon - meta.west) / meta.dlon - 0.5, fr = (meta.north - lat) / meta.dlat - 0.5;
      var c0 = Math.floor(fc), r0 = Math.floor(fr), u = fc - c0, v = fr - r0, out = 0;
      var wu = bs(u), wv = bs(v);
      for (var j = -1; j <= 2; j++) {
        var rr = Math.max(0, Math.min(meta.rows - 1, r0 + j)), row = 0;
        for (var i = -1; i <= 2; i++) row += wu[i + 1] * h[rr * meta.cols + Math.max(0, Math.min(meta.cols - 1, c0 + i))];
        out += wv[j + 1] * row;
      }
      return out;
    }
    return { meta: meta, h: h, at: at, atS: atS,
             lonOf: function (c) { return meta.west + (c + 0.5) * meta.dlon; },
             latOf: function (r) { return meta.north - (r + 0.5) * meta.dlat; } };
  };

  /* The Polaris, a gold four point star, SVG so no grade ever shifts it. */
  S.polaris = function (x, y, s, z) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', s); svg.setAttribute('height', s);
    svg.setAttribute('viewBox', '-50 -50 100 100');
    svg.setAttribute('style', 'position:absolute;left:' + (x - s / 2) + 'px;top:' + (y - s / 2) + 'px;z-index:' + (z || 9) + ';overflow:visible;');
    svg.setAttribute('data-decorative', '');
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M0,-50 C4,-14 14,-4 50,0 C14,4 4,14 0,50 C-4,14 -14,4 -50,0 C-14,-4 -4,-14 0,-50 Z');
    p.setAttribute('fill', S.GOLD);
    svg.appendChild(p);
    document.body.appendChild(svg);
    return svg;
  };

  /* Fixtures at z-index 9: Polaris and wordmark, counter, site line and
   * coordinates. o.display names the deck's display family for the wordmark. */
  S.fixtures = function (n, o) {
    o = o || {};
    var css = 'position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;white-space:nowrap;';
    function add(txt, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', css + style); d.textContent = txt; d.className = 'fx';
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    S.polaris(92, 101, 22);
    add('ALASKA.AI', 'left:112px;top:84px;font-family:' + (o.display || '"Instrument Serif",serif') + ';font-size:32px;letter-spacing:0.08em;color:' + (o.ink || S.PAL.type) + ';');
    add((n < 10 ? '0' : '') + n + ' / 09', 'right:80px;top:90px;font-size:24px;letter-spacing:0.06em;color:' + (o.counter || S.PAL.label) + ';font-variant-numeric:tabular-nums;');
    add('alaskaaihq.com', 'left:80px;top:1288px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || S.PAL.fixture) + ';', true);
    if (o.coords !== false)
      add(o.coordsText || S.COORDS, 'right:80px;top:1288px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || S.PAL.fixture) + ';', true);
  };

  /* Grain as a DOM tile, one cell per device pixel, above the art and below
   * the type (instinct grain-as-tile). */
  S.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.07));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 280, strength: o.strength || 44, seed: o.seed || 96 });
    return d;
  };

  S.boxes = function (sel, pad) {
    pad = pad || 0;
    var out = [];
    document.querySelectorAll(sel).forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.width) out.push([r.left - pad, r.top - pad, r.width + 2 * pad, r.height + 2 * pad]);
    });
    return out;
  };

  /* ---- THE PROVINCE PANORAMA (slides 01 to 03) ------------------------
   * One south-up plan of the Northern Alaska Province, 3240 px wide, drawn as
   * a function of global x so the three frames seam exactly. Needs d3, noise,
   * akhachure. South is UP (projection.angle(180)), so east is on the LEFT and
   * the noon sun sits at the top of the frame: lit faces are the upper, south
   * facing ones and every cast runs down the frame toward the ice.
   *   const P = await SLOPE.province(ctx, {dem, slide: 1|2|3, seed})
   *   P.xy(lon, lat) -> [x, y] in this slide's design px
   *   P.land, P.dist: Uint8Array land mask and px distance to land (1x grid)
   *   P.inProvince(x, y) */
  S.PROV = { scale: 16883, centerLon: -155.5, centerLat: 69.98, cy: 875, total: 3240,
             shadeEl: 22, castEl: 9, castVE: 3, reliefVE: 8, kmPerPx: 0.3772,
             ramp: [[0, '#0E1830'], [0.26, '#1F2D4C'], [0.40, '#36425A'], [0.52, '#6E6E7C'], [0.68, '#C7A68A'], [0.84, '#EBCFB2'], [1, '#F8EADA']] };

  S.provProjection = function (slide) {
    var P = S.PROV;
    return d3.geoConicEqualArea().parallels([68, 71]).rotate([-P.centerLon, 0]).center([0, P.centerLat])
      .angle(180).scale(P.scale).translate([P.total / 2 - (slide - 1) * 1080, P.cy]);
  };

  function hex2(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  S.rampAt = function (ramp, t) {
    t = Math.max(0, Math.min(1, t));
    for (var i = 1; i < ramp.length; i++) {
      if (t <= ramp[i][0]) {
        var a = ramp[i - 1], b = ramp[i], u = (t - a[0]) / (b[0] - a[0]);
        var ca = hex2(a[1]), cb = hex2(b[1]);
        return [ca[0] + (cb[0] - ca[0]) * u, ca[1] + (cb[1] - ca[1]) * u, ca[2] + (cb[2] - ca[2]) * u];
      }
    }
    return hex2(ramp[ramp.length - 1][1]);
  };

  /* Box blur in place, separable, radius r, n passes (a cheap Gaussian). */
  function boxBlur(a, W, H, r, n) {
    var tmp = new Float32Array(W * H);
    for (var p = 0; p < n; p++) {
      for (var y = 0; y < H; y++) { var acc = 0, row = y * W;
        for (var x = -r; x <= r; x++) acc += a[row + Math.max(0, Math.min(W - 1, x))];
        for (x = 0; x < W; x++) { tmp[row + x] = acc / (2 * r + 1);
          acc += a[row + Math.min(W - 1, x + r + 1)] - a[row + Math.max(0, x - r)]; } }
      for (var x2 = 0; x2 < W; x2++) { var acc2 = 0;
        for (var y2 = -r; y2 <= r; y2++) acc2 += tmp[Math.max(0, Math.min(H - 1, y2)) * W + x2];
        for (y2 = 0; y2 < H; y2++) { a[y2 * W + x2] = acc2 / (2 * r + 1);
          acc2 += tmp[Math.min(H - 1, y2 + r + 1) * W + x2] - tmp[Math.max(0, y2 - r) * W + x2]; } }
    }
    return a;
  }
  S.boxBlur = boxBlur;

  /* Bilinear read of a 1x field at design coordinates. */
  function bil(a, W, H, x, y) {
    x = Math.max(0, Math.min(W - 1.001, x - 0.5)); y = Math.max(0, Math.min(H - 1.001, y - 0.5));
    var x0 = x | 0, y0 = y | 0, u = x - x0, v = y - y0, i = y0 * W + x0;
    return a[i] * (1 - u) * (1 - v) + a[i + 1] * u * (1 - v) + a[i + W] * (1 - u) * v + a[i + W + 1] * u * v;
  }
  S.bil = bil;

  /* Central-difference gradient of a 1x field, per design px. Read it back with
   * bil(): differencing a bilinear field prints its cell lattice as a grid. */
  S.grad = function (a, W, H) {
    var gx = new Float32Array(W * H), gy = new Float32Array(W * H);
    for (var y = 1; y < H - 1; y++) for (var x = 1; x < W - 1; x++) { var i = y * W + x; gx[i] = (a[i + 1] - a[i - 1]) / 2; gy[i] = (a[i + W] - a[i - W]) / 2; }
    return [gx, gy];
  };

  /* Chamfer distance in design px from every 0 cell of `src` (land) to the rest. */
  function chamfer(land, W, H) {
    var dist = new Float32Array(W * H);
    for (var k = 0; k < W * H; k++) dist[k] = land[k] ? 0 : 1e6;
    for (var pass = 0; pass < 2; pass++) {
      for (var y = 1; y < H - 1; y++) for (var x = 1; x < W - 1; x++) {
        var p = y * W + x; if (!dist[p]) continue;
        dist[p] = Math.min(dist[p], dist[p - 1] + 1, dist[p - W] + 1, dist[p - W - 1] + 1.414, dist[p - W + 1] + 1.414);
      }
      for (var y2 = H - 2; y2 > 0; y2--) for (var x2 = W - 2; x2 > 0; x2--) {
        var q = y2 * W + x2; if (!dist[q]) continue;
        dist[q] = Math.min(dist[q], dist[q + 1] + 1, dist[q + W] + 1, dist[q + W + 1] + 1.414, dist[q + W - 1] + 1.414);
      }
    }
    for (var bx = 0; bx < W; bx++) { dist[bx] = dist[W + bx]; dist[(H - 1) * W + bx] = dist[(H - 2) * W + bx]; }
    for (var by = 0; by < H; by++) { dist[by * W] = dist[by * W + 1]; dist[by * W + W - 1] = dist[by * W + W - 2]; }
    return dist;
  }
  S.chamfer = chamfer;

  /* YOUNG SEA ICE as shore-parallel streak lay (No.96 round 1: "cloud noise with
   * dead-pixel specks" on five frames). Returns [r,g,b] for one device pixel.
   *   u     distance from the coast in design px (the cross-shore coordinate)
   *   gx    the along-shore coordinate in design px (the panorama's global x)
   *   y     design y, for low-frequency grease patches
   * Bands widen offshore (shorefast and narrow at the coast, open leads far out);
   * each band breaks into floes 70 to 160 px long, a floe's coast-side edge faces
   * the noon sun at the top of the frame and is lit, its far edge is in lee. */
  var ICE = { nilas: [38, 54, 59], grease: [61, 80, 84], lead: [8, 19, 27], floe: [201, 214, 220], young: [62, 80, 86],
              greaseSoft: [47, 64, 69], leadSoft: [25, 38, 45] };
  S.ICE = ICE;
  S.iceAt = function (u, gx, y, o) {
    // FLOES, not bands (No.96 round 3: shore-parallel bands read as folded rock strata on four frames).
    // Anisotropic Worley cells in (along-shore, log cross-shore): plates about 70 px long, 12 px deep at
    // the coast growing to about 70 px offshore, split by thin open cracks; the coast-side rim of each
    // plate faces the noon sun and is lit, its offshore rim is in lee; a few plates are open leads.
    o = o || {};
    var uu = Math.max(0, u + AK.fbm2(gx * 0.004 + 3.1, u * 0.01 + 5.7, { octaves: 2 }) * 10);
    var SX = 52, SY = 6.5, vp = 60 * Math.log(1 + uu / 80), ky = SY / (60 / (80 + uu));
    var X = gx / SX, Y = vp / SY, cx0 = Math.floor(X), cy0 = Math.floor(Y);
    var b1 = 1e9, b2 = 1e9, p1x = 0, p1y = 0, p2x = 0, p2y = 0, id1 = 0;
    for (var j = -1; j <= 1; j++) for (var i = -1; i <= 1; i++) {
      var ci = cx0 + i, cj = cy0 + j;
      var fx = ci + 0.15 + 0.7 * hh(ci, cj), fy = cj + 0.2 + 0.6 * hh(cj + 0.37, ci + 1.3);
      var dx = (X - fx) * SX, dy = (Y - fy) * ky, d2 = dx * dx + dy * dy;
      if (d2 < b1) { b2 = b1; p2x = p1x; p2y = p1y; b1 = d2; p1x = fx * SX; p1y = fy * ky; id1 = ci * 7.13 + cj * 3.71; }
      else if (d2 < b2) { b2 = d2; p2x = fx * SX; p2y = fy * ky; }
    }
    var sep = Math.hypot(p2x - p1x, p2y - p1y) || 1, dB = (b2 - b1) / (2 * sep);   // px to the floe boundary
    var hv = hh(id1, 0.5), pLead = 0.02 + Math.min(0.025, u / 12000);
    var base = hv < pLead ? ICE.leadSoft : hv < pLead + 0.32 ? ICE.greaseSoft : hv > 0.9 ? ICE.young : ICE.nilas;
    var gp = Math.max(0, Math.min(1, AK.fbm2(gx * 0.003, y * 0.008, { octaves: 3 }) * 1.8 + 0.15));
    var c = [base[0] + (ICE.grease[0] - base[0]) * gp * 0.3, base[1] + (ICE.grease[1] - base[1]) * gp * 0.3, base[2] + (ICE.grease[2] - base[2]) * gp * 0.3];
    var tv = AK.fbm2(gx * 0.006, uu * 0.09, { octaves: 2 }) * 3 + (hh(id1, 2.1) - 0.5) * 6;
    c[0] += tv; c[1] += tv; c[2] += tv;
    if (base === ICE.leadSoft) return c;
    var lit = (o.lit == null ? 0.42 : o.lit) * (1 - Math.min(0.45, u / 900));
    var coastSide = p2y < p1y;                                   // the neighbour across this rim is nearer the coast
    var cw = 0.55 + Math.min(0.9, u / 500);
    if (dB < cw) { var t = 0.7; return [c[0] + (ICE.lead[0] - c[0]) * t, c[1] + (ICE.lead[1] - c[1]) * t, c[2] + (ICE.lead[2] - c[2]) * t]; }
    if (coastSide && dB < cw + 1.3 && hh(id1, 4.4) > 0.25) {
      var la = lit * (1 - (dB - cw) / 1.3);
      c = [c[0] + (ICE.floe[0] - c[0]) * la, c[1] + (ICE.floe[1] - c[1]) * la, c[2] + (ICE.floe[2] - c[2]) * la];
    } else if (!coastSide && dB < cw + 1.6) {
      var le = 0.32 * (1 - (dB - cw) / 1.6);
      c = [c[0] + (ICE.lead[0] - c[0]) * le, c[1] + (ICE.lead[1] - c[1]) * le, c[2] + (ICE.lead[2] - c[2]) * le];
    }
    return c;
  };

  /* Paint the ice into every device pixel of `ctx` (a 2x canvas) where `isSea`
   * says so; `distAt(x, y)` gives design px from the coast. For frames that are
   * not on the panorama. */
  S.paintIce = function (ctx, o) {
    var W2 = S.W * 2, H2 = S.H * 2, cv = ctx.canvas, img = ctx.getImageData(0, 0, W2, H2), d = img.data;
    for (var y = 0; y < H2; y++) for (var x = 0; x < W2; x++) {
      var xd = (x + 0.5) / 2, yd = (y + 0.5) / 2;
      if (!o.isSea(xd, yd)) continue;
      var c = S.iceAt(o.distAt(xd, yd), xd + (o.gx0 || 0), yd, o), i = (y * W2 + x) * 4;
      var k = o.dim == null ? 1 : o.dim;
      d[i] = c[0] * k; d[i + 1] = c[1] * k; d[i + 2] = c[2] * k; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  };

  S.province = async function (ctx, o) {
    var P = S.PROV, W = S.W, H = S.H, dem = o.dem, slide = o.slide, gx0 = (slide - 1) * 1080;
    var proj = S.provProjection(slide);
    var N = W * H, h = new Float32Array(N), land = new Uint8Array(N), latA = new Float32Array(N);
    var m = dem.meta;
    function sample(x, y) {
      var ll = proj.invert([x, y]);
      var inside = ll[0] > m.west && ll[0] < m.east && ll[1] > m.south && ll[1] < m.north;
      return [inside ? dem.atS(ll[0], ll[1]) : (ll[1] < m.south ? 900 : -40), ll[1]];
    }
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var sv = sample(x + 0.5, y + 0.5), i = y * W + x;
      h[i] = sv[0]; latA[i] = sv[1]; land[i] = sv[0] > 0.5 ? 1 : 0;
    }
    // smoothed elevation decides the study area: the Brooks Range proper is outside the province
    var sm = boxBlur(Float32Array.from(h), W, H, 9, 1);
    var outside = new Float32Array(N), outsideE = new Float32Array(N);
    for (var k = 0; k < N; k++) {
      var t = Math.max(0, Math.min(1, (sm[k] - 560) / 260));
      outsideE[k] = land[k] ? t * t * (3 - 2 * t) : 0;
      outside[k] = land[k] ? t * t * (3 - 2 * t) : 0;
    }
    var dist = chamfer(land, W, H), distS = boxBlur(Float32Array.from(dist), W, H, 6, 2);
    await new Promise(function (r) { setTimeout(r, 0); });

    // ---- shading, per DEVICE pixel (a 1x field drawn up to 2x printed as upscale blur and stair-steps)
    var W2 = W * 2, H2 = H * 2, N2 = W2 * H2, h2 = new Float32Array(N2);
    for (var yy = 0; yy < H2; yy++) for (var xx = 0; xx < W2; xx++) h2[yy * W2 + xx] = sample((xx + 0.5) / 2, (yy + 0.5) / 2)[0];
    var cast = new Float32Array(N2), drop = Math.tan(P.castEl * Math.PI / 180) * P.kmPerPx * 500;
    for (var cx = 0; cx < W2; cx++) {
      var hs = -1e9;
      for (var cy = 0; cy < H2; cy++) {
        var ii = cy * W2 + cx, hv = Math.max(0, h2[ii]) * P.castVE;
        hs = Math.max(hs - drop, hv);
        cast[ii] = hs - hv > 25 ? Math.min(1, (hs - hv) / 220) : 0;
      }
    }
    boxBlur(cast, W2, H2, 2, 2);                                               // casts have a penumbra
    var img = ctx.createImageData(W2, H2), d = img.data;
    var el = P.shadeEl * Math.PI / 180, L = [0, -Math.cos(el), Math.sin(el)];
    var sc = P.reliefVE / (2 * P.kmPerPx * 500);
    var mask = hex2('#0E1A2A'), castC = hex2('#142440');
    for (var y3 = 1; y3 < H2 - 1; y3++) for (var x3 = 1; x3 < W2 - 1; x3++) {
      var j = y3 * W2 + x3, xd = (x3 + 0.5) / 2, yd = (y3 + 0.5) / 2, gxv = xd + gx0, r, g, b;
      if (h2[j] > 0.5) {
        var dx = (Math.max(0, h2[j + 1]) - Math.max(0, h2[j - 1])) * sc, dy = (Math.max(0, h2[j + W2]) - Math.max(0, h2[j - W2])) * sc;
        var nl = Math.sqrt(dx * dx + dy * dy + 1), s = (-dx * L[0] - dy * L[1] + L[2]) / nl;
        var tooth = AK.simplex2(gxv * 0.45, yd * 0.45) * 0.012 + AK.fbm2(gxv * 0.012, yd * 0.012, { octaves: 4 }) * 0.04;
        var c = S.rampAt(P.ramp, s * 0.92 + 0.06 + tooth);
        var cs = cast[j] * 0.62;
        c = [c[0] + (castC[0] - c[0]) * cs, c[1] + (castC[1] - c[1]) * cs, c[2] + (castC[2] - c[2]) * cs];
        var ot = bil(outside, W, H, xd, yd) * 0.26;                         // the land outside the province, held back
        r = c[0] + (mask[0] - c[0]) * ot; g = c[1] + (mask[1] - c[1]) * ot; b = c[2] + (mask[2] - c[2]) * ot;
      } else {
        var ci = S.iceAt(bil(distS, W, H, xd, yd), gxv, yd);
        r = ci[0]; g = ci[1]; b = ci[2];
      }
      d[j * 4] = r; d[j * 4 + 1] = g; d[j * 4 + 2] = b; d[j * 4 + 3] = 255;
    }
    var base = document.createElement('canvas'); base.width = W2; base.height = H2;
    base.getContext('2d').putImageData(img, 0, 0);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(base, 0, 0); ctx.restore();
    await new Promise(function (r) { setTimeout(r, 0); });

    // drainage from the DEM itself: priority flood, steepest descent, then traced as smoothed polylines
    (function () {
      var acc = new Float32Array(N), down = new Int32Array(N).fill(-1), k3;
      // a whisper of noise on the routing surface only, so flats drain in meanders and not in ruled lines
      var hr = new Float32Array(N);
      for (k3 = 0; k3 < N; k3++) { var xq = k3 % W, yq = (k3 - xq) / W;
        hr[k3] = h[k3] + AK.fbm2((xq + gx0) * 0.03, yq * 0.03, { octaves: 3 }) * 4; }
      var fz = new Float32Array(N), done = new Uint8Array(N), heap = [], hv2 = [];
      function push(i, v) { heap.push(i); hv2.push(v); var c = heap.length - 1; while (c > 0) { var pp = (c - 1) >> 1; if (hv2[pp] <= hv2[c]) break;
        var ti = heap[pp]; heap[pp] = heap[c]; heap[c] = ti; var tv = hv2[pp]; hv2[pp] = hv2[c]; hv2[c] = tv; c = pp; } }
      function pop() { var top = heap[0], lastI = heap.pop(), lastV = hv2.pop(); if (heap.length) { heap[0] = lastI; hv2[0] = lastV; var c = 0;
        for (;;) { var l = 2 * c + 1, r = l + 1, m2 = c; if (l < heap.length && hv2[l] < hv2[m2]) m2 = l; if (r < heap.length && hv2[r] < hv2[m2]) m2 = r; if (m2 === c) break;
          var ti = heap[m2]; heap[m2] = heap[c]; heap[c] = ti; var tv = hv2[m2]; hv2[m2] = hv2[c]; hv2[c] = tv; c = m2; } } return top; }
      for (k3 = 0; k3 < N; k3++) { var xb = k3 % W, yb = (k3 - xb) / W;
        if (!land[k3] || xb === 0 || yb === 0 || xb === W - 1 || yb === H - 1) { fz[k3] = land[k3] ? hr[k3] : 0; done[k3] = 1; push(k3, fz[k3]); } }
      var nb8 = [-1, 1, -W, W, -W - 1, -W + 1, W - 1, W + 1];
      while (heap.length) { var cq = pop(), cxq = cq % W;
        for (var t4 = 0; t4 < 8; t4++) { var nq = cq + nb8[t4], nx = nq % W;
          if (nq < 0 || nq >= N || Math.abs(nx - cxq) > 1 || done[nq]) continue;
          done[nq] = 1; fz[nq] = Math.max(hr[nq], fz[cq] + 0.01); push(nq, fz[nq]); } }
      var order = [];
      for (k3 = 0; k3 < N; k3++) if (land[k3]) order.push(k3);
      for (var oi = 0; oi < order.length; oi++) {
        var q3 = order[oi], x7 = q3 % W, y7 = (q3 - x7) / W, best = -1, bd = 0;
        if (x7 < 1 || y7 < 1 || x7 > W - 2 || y7 > H - 2) continue;
        for (var t3 = 0; t3 < 8; t3++) {
          var n3 = q3 + nb8[t3], dd = (fz[q3] - fz[n3]) / (t3 < 4 ? 1 : 1.414);
          if (dd > bd) { bd = dd; best = n3; }
        }
        down[q3] = best;
      }
      order.sort(function (a3, b3) { return fz[b3] - fz[a3]; });
      for (oi = 0; oi < order.length; oi++) { var q4 = order[oi]; acc[q4] += 1; if (down[q4] >= 0) acc[down[q4]] += acc[q4]; }
      var A0 = 1400, seen = new Uint8Array(N), lines = [];
      for (oi = 0; oi < order.length; oi++) {
        var q5 = order[oi];
        if (seen[q5] || acc[q5] < A0 || outside[q5] > 0.6) continue;
        var pts = [], c5 = q5;
        while (c5 >= 0 && acc[c5] >= A0) {
          var xc = c5 % W; pts.push([xc + 0.5, (c5 - xc) / W + 0.5, acc[c5]]);
          if (seen[c5]) break;
          seen[c5] = 1; c5 = down[c5];
        }
        if (c5 >= 0 && !seen[c5]) { var xe = c5 % W; pts.push([xe + 0.5, (c5 - xe) / W + 0.5, acc[c5] || A0]); }
        if (pts.length > 3 || (lines.length && pts.length > 1)) lines.push(pts);
      }
      function chaikin(p) {
        var o2 = [p[0]];
        for (var i = 0; i < p.length - 1; i++) {
          var a = p[i], b = p[i + 1];
          o2.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25, a[2] * 0.75 + b[2] * 0.25]);
          o2.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75, a[2] * 0.25 + b[2] * 0.75]);
        }
        o2.push(p[p.length - 1]); return o2;
      }
      ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      lines.forEach(function (pts) {
        var len = 0; for (var i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
        if (len < 18 && pts[pts.length - 1][2] < 4 * A0) return;
        var thin = pts.filter(function (pp, ix) { return ix % 4 === 0 || ix === pts.length - 1; });
        var sp = chaikin(chaikin(chaikin(thin.length > 2 ? thin : pts)));
        for (var i2 = 1; i2 < sp.length; i2++) {
          var Av = sp[i2][2], lg = Math.log(Av / A0);
          ctx.strokeStyle = 'rgba(176,194,212,' + Math.min(0.48, 0.16 + lg * 0.09).toFixed(3) + ')';
          ctx.lineWidth = Math.min(2.0, 0.5 + lg * 0.36);
          ctx.beginPath(); ctx.moveTo(sp[i2 - 1][0], sp[i2 - 1][1]); ctx.lineTo(sp[i2][0], sp[i2][1]); ctx.stroke();
        }
      });
      ctx.restore();
    })();

    // hachure: dark strokes in the lee, apricot strokes on the sunward faces, only where the land has slope
    var hgrid = function (u, v) {
      var X = u * P.total - gx0, Y = v * H;
      if (X < 1 || X > W - 2 || Y < 1 || Y > H - 2) {
        var ll2 = proj.invert([X, Y]); if (!ll2) return 0;
        var inside2 = ll2[0] > m.west && ll2[0] < m.east && ll2[1] > m.south && ll2[1] < m.north;
        return inside2 ? Math.max(0, dem.atS(ll2[0], ll2[1])) / 2400 : 0;
      }
      return Math.max(0, bil(h, W, H, X, Y)) / 2400;
    };
    var hl = S.layer(W, H), hx = hl.getContext('2d');
    AK.hachureField(hx, { x: -gx0, y: 0, w: P.total, h: H, scale: 2, seed: (o.seed || 96) + 11, height: hgrid,
      cell: 9, lenScale: 1.9, passes: 3, sunAz: 0, sunEl: P.shadeEl, sunJitter: 9, color: '#0A1426', alpha: 0.30,
      minWidth: 0.5, maxWidth: 3.0, relief: 60, slopeRef: 0.012 });
    AK.hachureField(hx, { x: -gx0, y: 0, w: P.total, h: H, scale: 2, seed: (o.seed || 96) + 23, height: hgrid,
      cell: 11, lenScale: 1.7, passes: 2, sunAz: 180, sunEl: P.shadeEl, sunJitter: 9, color: '#F2D9BE', alpha: 0.30,
      minWidth: 0.4, maxWidth: 2.2, relief: 60, slopeRef: 0.012 });
    // keep strokes on sloped land only, faded on the masked land, with a soft foot rather than a cutoff
    var mk = document.createElement('canvas'); mk.width = W; mk.height = H;
    var mv = new Float32Array(N);
    for (var y4 = 1; y4 < H - 1; y4++) for (var x4 = 1; x4 < W - 1; x4++) {
      var q = y4 * W + x4;
      var sl = land[q] ? Math.hypot(h[q + 1] - h[q - 1], h[q + W] - h[q - W]) : 0;
      mv[q] = Math.min(1, Math.max(0, (sl - 14) / 44)) * (1 - outside[q] * 0.7);
    }
    boxBlur(mv, W, H, 6, 2);
    var mi = mk.getContext('2d').createImageData(W, H);
    for (q = 0; q < N; q++) mi.data[q * 4 + 3] = Math.min(255, mv[q] * 300) * (land[q] ? 1 : 0);
    mk.getContext('2d').putImageData(mi, 0, 0);
    hx.save(); hx.setTransform(1, 0, 0, 1, 0, 0); hx.globalCompositeOperation = 'destination-in';
    hx.imageSmoothingQuality = 'high'; hx.drawImage(mk, 0, 0, W * 2, H * 2); hx.restore();
    ctx.drawImage(hl, 0, 0, W, H);

    // the coast's lit lip (the upper, sunward side of every floe edge) and the offshore edge, about 3 miles out (4.83 km)
    var gp = d3.geoPath(null, ctx);
    var coast = d3.contours().size([W, H]).thresholds([0.5])(Array.from(h, function (v) { return Math.max(-20, Math.min(20, v)); }));
    ctx.save(); ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.rect(2, 2, W - 4, H - 4); ctx.clip();                // contours close along the frame; never draw that
    ctx.strokeStyle = 'rgba(201,214,220,0.6)'; ctx.lineWidth = 1.1; ctx.beginPath(); gp(coast[0]); ctx.stroke();
    ctx.restore();
    var buf = 4.83 / P.kmPerPx;
    var edge = d3.contours().size([W, H]).thresholds([buf])(Array.from(dist, function (v) { return Math.min(v, 60); }))[0];

    return { proj: proj, land: land, dist: dist, outside: outside, outsideE: outsideE, edge: edge, h: h,
             xy: function (lon, lat) { return proj([lon, lat]); },
             inProvince: function (x, y) { var q = Math.round(y) * W + Math.round(x); return land[q] && outside[q] < 0.5; } };
  };

  /* Draw the province's offshore edge (aurora ice, the only use of #5AC8F0). */
  S.edgeLine = function (ctx, P, o) {
    o = o || {};
    var gp = d3.geoPath(null, ctx);
    ctx.save(); ctx.lineJoin = 'round'; ctx.beginPath(); ctx.rect(3, 3, S.W - 6, S.H - 6); ctx.clip();
    ctx.strokeStyle = 'rgba(5,10,20,0.55)'; ctx.lineWidth = 3.2; ctx.beginPath(); gp(P.edge); ctx.stroke();
    ctx.strokeStyle = '#5AC8F0'; ctx.lineWidth = o.width || 1.6; ctx.beginPath(); gp(P.edge); ctx.stroke();
    ctx.restore();
  };

  /* The north arrow for a south-up sheet: a gold Polaris pointing DOWN, with
   * its N as DOM text beneath (SVG text under other layers trips qa's paint-over
   * check, and the N is a label a reader needs). */
  S.northArrow = function (x, y) {
    var NS = 'http://www.w3.org/2000/svg', na = document.createElementNS(NS, 'svg');
    na.setAttribute('width', 26); na.setAttribute('height', 50); na.setAttribute('viewBox', '-13 -19 26 50');
    na.setAttribute('style', 'position:absolute;left:' + (x - 13) + 'px;top:' + (y - 19) + 'px;z-index:8;overflow:visible');
    na.setAttribute('data-decorative', '');
    na.innerHTML = '<path d="M0,-18 C2,-5 5,-2 12,0 C5,2 2,5 0,30 C-2,5 -5,2 -12,0 C-5,-2 -2,-5 0,-18 Z" fill="#FFC72C"/>';
    document.body.appendChild(na);
    var n = document.createElement('div');
    n.textContent = 'N';
    n.setAttribute('style', 'position:absolute;z-index:8;left:' + (x - 7) + 'px;top:' + (y + 22) + 'px;font:500 24px/1 "JetBrains Mono",monospace;color:#C9D3DA;');
    n.className = 'north-n';
    document.body.appendChild(n);
    return [x - 13, y - 19, 26, 66];
  };

  /* A halo under every label matching `sel`, in the ground's own colour. It is
   * GLYPH-SHAPED (stacked text-shadows), not a canvas box: a feathered rect still
   * printed as a plate on flat ground and erased the stipple on 08 (No.96 round 2).
   * `o.extra` rects (non-text marks) still get a small feathered canvas reserve. */
  S.halo = function (ctx, sel, color, o) {
    o = o || {};
    var c = hex2(color), rgba = function (a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; };
    document.querySelectorAll(sel).forEach(function (el) {
      el.style.textShadow = '0 0 2px ' + rgba(0.95) + ', 0 0 4px ' + rgba(0.9) + ', 0 0 8px ' + rgba(0.8) + ', 0 0 14px ' + rgba(0.55);
    });
    if (o.extra && o.extra.length) AKPOST.reserve(ctx, o.extra, { color: color, feather: o.feather || 6, strength: o.strength || 0.92 });
  };

  /* A quiet ground under the two footer fixtures (site line and coordinates),
   * for frames whose art runs under them. */
  S.footGround = function (ctx, color, strength) {
    AKPOST.reserve(ctx, [[80, 1286, 176, 24], [780, 1286, 220, 24]], { color: color, feather: 9, strength: strength == null ? 0.85 : strength });
  };

  /* A full-width scrim under a type band: holds `strength` of `color` from y0
   * to y1 and eases to nothing by y2 (smoothstep, many stops), so the type's
   * ground has no x edge and no corner to find (No.96 round 1, 01 and 03). */
  S.scrim = function (ctx, y0, y1, y2, color, strength, top) {
    var c = hex2(color), g = ctx.createLinearGradient(0, top == null ? y0 - 40 : top, 0, y2);
    var a0 = top == null ? y0 - 40 : top, span = y2 - a0;
    for (var i = 0; i <= 24; i++) {
      var yy = a0 + span * i / 24, t;
      if (yy < y0) t = (yy - a0) / Math.max(1, y0 - a0); else if (yy <= y1) t = 1; else t = 1 - (yy - y1) / Math.max(1, y2 - y1);
      t = Math.max(0, Math.min(1, t)); t = t * t * (3 - 2 * t);
      g.addColorStop(i / 24, 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (t * strength).toFixed(4) + ')');
    }
    ctx.save(); ctx.fillStyle = g; ctx.fillRect(0, a0, S.W, span); ctx.restore();
  };

  /* The reach at radius zero: a gold crosshair with a soft cast ring, sized to
   * be found at the 432 px thumb. */
  S.crosshair = function (ctx, x, y, o) {
    o = o || {}; var r = o.r || 28, gap = o.gap || 9;
    ctx.save();
    ctx.strokeStyle = 'rgba(5,10,20,0.55)'; ctx.lineWidth = 6; ctx.filter = 'blur(3px)';
    ctx.beginPath(); ctx.arc(x, y + 3, r * 0.62, 0, Math.PI * 2); ctx.stroke(); ctx.filter = 'none';
    ctx.strokeStyle = 'rgba(5,10,20,0.7)'; ctx.lineWidth = 5; ctx.lineCap = 'round';
    [[-1, 0], [1, 0], [0, -1], [0, 1]].forEach(function (v) { ctx.beginPath(); ctx.moveTo(x + v[0] * gap, y + v[1] * gap); ctx.lineTo(x + v[0] * r, y + v[1] * r); ctx.stroke(); });
    ctx.strokeStyle = S.GOLD; ctx.lineWidth = 2.5; ctx.lineCap = 'butt';
    [[-1, 0], [1, 0], [0, -1], [0, 1]].forEach(function (v) { ctx.beginPath(); ctx.moveTo(x + v[0] * gap, y + v[1] * gap); ctx.lineTo(x + v[0] * r, y + v[1] * r); ctx.stroke(); });
    ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(x, y, r * 0.62, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.arc(x, y, 3.2, 0, Math.PI * 2); ctx.fillStyle = S.GOLD; ctx.fill();
    ctx.restore();
  };

  global.SLOPE = S;
})(window);
