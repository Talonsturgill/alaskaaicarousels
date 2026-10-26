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
    return { meta: meta, h: h, at: at,
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
      d.setAttribute('style', css + style); d.textContent = txt;
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

  S.province = async function (ctx, o) {
    var P = S.PROV, W = S.W, H = S.H, dem = o.dem, slide = o.slide, gx0 = (slide - 1) * 1080;
    var proj = S.provProjection(slide);
    var N = W * H, h = new Float32Array(N), land = new Uint8Array(N), lonA = new Float32Array(N), latA = new Float32Array(N);
    var m = dem.meta;
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var ll = proj.invert([x + 0.5, y + 0.5]), i = y * W + x;
      lonA[i] = ll[0]; latA[i] = ll[1];
      var inside = ll[0] > m.west && ll[0] < m.east && ll[1] > m.south && ll[1] < m.north;
      var v = inside ? dem.at(ll[0], ll[1]) : (ll[1] < m.south ? 900 : (ll[0] >= m.east ? (ll[1] < 69.62 ? 120 : -40) : -40));
      h[i] = v; land[i] = v > 0.5 ? 1 : 0;
    }
    // smoothed elevation decides the study area: the Brooks Range proper is outside the province
    var sm = new Float32Array(N), R = 9;
    (function () {
      var tmp = new Float32Array(N);
      for (var y = 0; y < H; y++) { var acc = 0, c = 0; for (var x = -R; x < W + R; x++) {
        var xi = Math.min(W - 1, Math.max(0, x + R)), xo = Math.min(W - 1, Math.max(0, x - R - 1));
        acc += h[y * W + xi]; c++; if (x - R - 1 >= -R) { acc -= h[y * W + xo]; c--; }
        if (x >= 0 && x < W) tmp[y * W + x] = acc / c; } }
      for (var x2 = 0; x2 < W; x2++) { var acc2 = 0, c2 = 0; for (var y2 = -R; y2 < H + R; y2++) {
        var yi = Math.min(H - 1, Math.max(0, y2 + R)), yo = Math.min(H - 1, Math.max(0, y2 - R - 1));
        acc2 += tmp[yi * W + x2]; c2++; if (y2 - R - 1 >= -R) { acc2 -= tmp[yo * W + x2]; c2--; }
        if (y2 >= 0 && y2 < H) sm[y2 * W + x2] = acc2 / c2; } }
    })();
    var outside = new Float32Array(N);
    for (var k = 0; k < N; k++) {
      var e = sm[k], t = Math.max(0, Math.min(1, (e - 560) / 260));
      if (latA[k] < 68.05) t = 1;
      outside[k] = land[k] ? t * t * (3 - 2 * t) : 0;
    }
    // casts toward the ice: march each column from the top (the sun is up, due south)
    var cast = new Float32Array(N), drop = Math.tan(P.castEl * Math.PI / 180) * P.kmPerPx * 1000;
    for (var cx = 0; cx < W; cx++) {
      var hs = -1e9;
      for (var cy = 0; cy < H; cy++) {
        var ii = cy * W + cx, hv = Math.max(0, h[ii]) * P.castVE;
        hs = Math.max(hs - drop, hv);
        cast[ii] = hs - hv > 25 ? Math.min(1, (hs - hv) / 220) : 0;
      }
    }
    // shading
    var img = ctx.createImageData(W, H), d = img.data;
    var el = P.shadeEl * Math.PI / 180, L = [0, -Math.cos(el), Math.sin(el)];
    var sc = P.reliefVE / (2 * P.kmPerPx * 1000);
    var sea0 = hex2('#26363B'), grease = hex2('#3D5054'), lead = hex2('#08131B'), floe = hex2('#C9D6DC'), mask = hex2('#0E1A2A'), castC = hex2('#142440');
    for (var y3 = 1; y3 < H - 1; y3++) for (var x3 = 1; x3 < W - 1; x3++) {
      var j = y3 * W + x3, gxv = x3 + gx0, r, g, b;
      if (land[j]) {
        var dx = (Math.max(0, h[j + 1]) - Math.max(0, h[j - 1])) * sc, dy = (Math.max(0, h[j + W]) - Math.max(0, h[j - W])) * sc;
        var nl = Math.sqrt(dx * dx + dy * dy + 1), s = (-dx * L[0] - dy * L[1] + L[2]) / nl;
        var tooth = AK.simplex2(gxv * 0.9, y3 * 0.9) * 0.018 + AK.fbm2(gxv * 0.012, y3 * 0.012, { octaves: 4 }) * 0.04;
        var c = S.rampAt(P.ramp, s * 0.92 + 0.06 + tooth);
        var cs = cast[j] * 0.62;
        c = [c[0] + (castC[0] - c[0]) * cs, c[1] + (castC[1] - c[1]) * cs, c[2] + (castC[2] - c[2]) * cs];
        var ot = outside[j] * 0.26;                   // the land outside the province, held back
        r = c[0] + (mask[0] - c[0]) * ot; g = c[1] + (mask[1] - c[1]) * ot; b = c[2] + (mask[2] - c[2]) * ot;
      } else {
        // young sea ice: broad grease patches on nilas, thin pressure cracks, lit where a crack faces the sun
        var gp1 = AK.fbm2(gxv * 0.0035, y3 * 0.009, { octaves: 4 });
        var c2 = sea0.slice(), gm = Math.max(0, Math.min(1, gp1 * 2.2 + 0.25));
        c2 = [c2[0] + (grease[0] - c2[0]) * gm, c2[1] + (grease[1] - c2[1]) * gm, c2[2] + (grease[2] - c2[2]) * gm];
        var wq = AK.fbm2(gxv * 0.006 + 9, y3 * 0.006 + 3, { octaves: 2 }) * 1.6;
        var cv = AK.fbm2(gxv * 0.009 + wq, y3 * 0.013, { octaves: 3 }), cu = AK.fbm2(gxv * 0.009 + wq, (y3 - 1.5) * 0.013, { octaves: 3 });
        var crack = Math.abs(cv - 0.08) < 0.0065;
        if (crack) { var lit2 = cu > cv ? 0.55 : 0.0; var tgt = lit2 ? floe : lead; var cm = lit2 ? lit2 : 0.6;
          c2 = [c2[0] + (tgt[0] - c2[0]) * cm, c2[1] + (tgt[1] - c2[1]) * cm, c2[2] + (tgt[2] - c2[2]) * cm]; }
        var spk = AK.simplex2(gxv * 0.7, y3 * 0.7) * 2.5; c2 = [c2[0] + spk, c2[1] + spk, c2[2] + spk];
        r = c2[0]; g = c2[1]; b = c2[2];
      }
      d[j * 4] = r; d[j * 4 + 1] = g; d[j * 4 + 2] = b; d[j * 4 + 3] = 255;
    }
    var base = document.createElement('canvas'); base.width = W; base.height = H;
    base.getContext('2d').putImageData(img, 0, 0);
    ctx.save(); ctx.imageSmoothingQuality = 'high'; ctx.drawImage(base, 0, 0, W, H); ctx.restore();

    // drainage from the DEM itself: steepest-descent flow accumulation, drawn where a channel gathers enough ground
    (function () {
      var order = [], k3, acc = new Float32Array(N), down = new Int32Array(N).fill(-1);
      // priority flood (Barnes 2014): fill pits from the sea and the frame edge inward, with a tiny epsilon so flats drain
      var fz = new Float32Array(N), done = new Uint8Array(N), heap = [], hv2 = [];
      function push(i, v) { heap.push(i); hv2.push(v); var c = heap.length - 1; while (c > 0) { var pp = (c - 1) >> 1; if (hv2[pp] <= hv2[c]) break;
        var ti = heap[pp]; heap[pp] = heap[c]; heap[c] = ti; var tv = hv2[pp]; hv2[pp] = hv2[c]; hv2[c] = tv; c = pp; } }
      function pop() { var top = heap[0], lastI = heap.pop(), lastV = hv2.pop(); if (heap.length) { heap[0] = lastI; hv2[0] = lastV; var c = 0;
        for (;;) { var l = 2 * c + 1, r = l + 1, m2 = c; if (l < heap.length && hv2[l] < hv2[m2]) m2 = l; if (r < heap.length && hv2[r] < hv2[m2]) m2 = r; if (m2 === c) break;
          var ti = heap[m2]; heap[m2] = heap[c]; heap[c] = ti; var tv = hv2[m2]; hv2[m2] = hv2[c]; hv2[c] = tv; c = m2; } } return top; }
      for (k3 = 0; k3 < N; k3++) { var xb = k3 % W, yb = (k3 - xb) / W;
        if (!land[k3] || xb === 0 || yb === 0 || xb === W - 1 || yb === H - 1) { fz[k3] = land[k3] ? h[k3] : 0; done[k3] = 1; if (land[k3] || true) push(k3, fz[k3]); } }
      var nb8 = [-1, 1, -W, W, -W - 1, -W + 1, W - 1, W + 1];
      while (heap.length) { var cq = pop(), cxq = cq % W, cyq = (cq - cxq) / W;
        for (var t4 = 0; t4 < 8; t4++) { var nq = cq + nb8[t4], nx = nq % W;
          if (nq < 0 || nq >= N || Math.abs(nx - cxq) > 1 || done[nq]) continue;
          done[nq] = 1; fz[nq] = Math.max(h[nq], fz[cq] + 0.01); push(nq, fz[nq]); } }
      for (k3 = 0; k3 < N; k3++) if (land[k3]) order.push(k3);
      for (var oi = 0; oi < order.length; oi++) {
        var q3 = order[oi], x7 = q3 % W, y7 = (q3 - x7) / W, best = -1, bd = 0;
        if (x7 < 1 || y7 < 1 || x7 > W - 2 || y7 > H - 2) continue;
        var nb = [-1, 1, -W, W, -W - 1, -W + 1, W - 1, W + 1];
        for (var t3 = 0; t3 < 8; t3++) {
          var n3 = q3 + nb[t3], dd = (fz[q3] - fz[n3]) / (t3 < 4 ? 1 : 1.414);
          if (dd > bd) { bd = dd; best = n3; }
        }
        down[q3] = best;
      }
      order.sort(function (a3, b3) { return fz[b3] - fz[a3]; });
      for (oi = 0; oi < order.length; oi++) { var q4 = order[oi]; acc[q4] += 1; if (down[q4] >= 0) acc[down[q4]] += acc[q4]; }
      ctx.save();
      for (oi = 0; oi < order.length; oi++) {
        var q5 = order[oi], A = acc[q5];
        if (A < 700 || down[q5] < 0 || outside[q5] > 0.6) continue;
        var x8 = q5 % W, y8 = (q5 - x8) / W, d5 = down[q5], x9 = d5 % W, y9 = (d5 - x9) / W;
        var wv = Math.min(2.4, 0.5 + Math.log(A / 700) * 0.45);
        ctx.strokeStyle = 'rgba(176,194,212,' + Math.min(0.62, 0.22 + Math.log(A / 700) * 0.1).toFixed(3) + ')';
        ctx.lineWidth = wv; ctx.beginPath(); ctx.moveTo(x8 + 0.5, y8 + 0.5); ctx.lineTo(x9 + 0.5, y9 + 0.5); ctx.stroke();
      }
      ctx.restore();
    })();

    // hachure: dark strokes in the lee, apricot strokes on the sunward faces, only where the land has slope
    var hgrid = function (u, v) {
      var X = Math.round(u * P.total - gx0), Y = Math.round(v * H);
      if (X < 1 || X > W - 2 || Y < 1 || Y > H - 2) {
        var ll2 = proj.invert([X, Y]); if (!ll2) return 0;
        var inside2 = ll2[0] > m.west && ll2[0] < m.east && ll2[1] > m.south && ll2[1] < m.north;
        return inside2 ? Math.max(0, dem.at(ll2[0], ll2[1])) / 2400 : 0;
      }
      return Math.max(0, h[Y * W + X]) / 2400;
    };
    var hl = S.layer(W, H), hx = hl.getContext('2d');
    AK.hachureField(hx, { x: -gx0, y: 0, w: P.total, h: H, scale: 2, seed: (o.seed || 96) + 11, height: hgrid,
      cell: 9, lenScale: 1.9, passes: 3, sunAz: 0, sunEl: P.shadeEl, sunJitter: 9, color: '#0A1426', alpha: 0.30,
      minWidth: 0.5, maxWidth: 3.0, relief: 60, slopeRef: 0.012 });
    AK.hachureField(hx, { x: -gx0, y: 0, w: P.total, h: H, scale: 2, seed: (o.seed || 96) + 23, height: hgrid,
      cell: 11, lenScale: 1.7, passes: 2, sunAz: 180, sunEl: P.shadeEl, sunJitter: 9, color: '#F2D9BE', alpha: 0.30,
      minWidth: 0.4, maxWidth: 2.2, relief: 60, slopeRef: 0.012 });
    // keep strokes on sloped land only, faded on the masked land
    var mk = document.createElement('canvas'); mk.width = W; mk.height = H;
    var mi = mk.getContext('2d').createImageData(W, H);
    for (var y4 = 1; y4 < H - 1; y4++) for (var x4 = 1; x4 < W - 1; x4++) {
      var q = y4 * W + x4;
      var sl = land[q] ? Math.hypot(h[q + 1] - h[q - 1], h[q + W] - h[q - W]) : 0;
      var a = Math.min(1, Math.max(0, (sl - 10) / 40)) * (1 - outside[q] * 0.7);
      mi.data[q * 4 + 3] = a * 255;
    }
    mk.getContext('2d').putImageData(mi, 0, 0);
    hx.save(); hx.setTransform(1, 0, 0, 1, 0, 0); hx.globalCompositeOperation = 'destination-in';
    hx.drawImage(mk, 0, 0, W * 2, H * 2); hx.restore();
    ctx.drawImage(hl, 0, 0, W, H);

    // the coast's lit lip and the province's offshore edge, about 3 miles out (4.83 km)
    var dist = new Float32Array(N);
    for (var k2 = 0; k2 < N; k2++) dist[k2] = land[k2] ? 0 : 1e6;
    for (var pass = 0; pass < 2; pass++) {
      for (var y5 = 1; y5 < H - 1; y5++) for (var x5 = 1; x5 < W - 1; x5++) {
        var p5 = y5 * W + x5; if (!dist[p5]) continue;
        dist[p5] = Math.min(dist[p5], dist[p5 - 1] + 1, dist[p5 - W] + 1, dist[p5 - W - 1] + 1.414, dist[p5 - W + 1] + 1.414);
      }
      for (var y6 = H - 2; y6 > 0; y6--) for (var x6 = W - 2; x6 > 0; x6--) {
        var p6 = y6 * W + x6; if (!dist[p6]) continue;
        dist[p6] = Math.min(dist[p6], dist[p6 + 1] + 1, dist[p6 + W] + 1, dist[p6 + W + 1] + 1.414, dist[p6 + W - 1] + 1.414);
      }
    }
    for (var bx = 0; bx < W; bx++) { dist[bx] = dist[W + bx]; dist[(H - 1) * W + bx] = dist[(H - 2) * W + bx]; }
    for (var by = 0; by < H; by++) { dist[by * W] = dist[by * W + 1]; dist[by * W + W - 1] = dist[by * W + W - 2]; }
    var buf = 4.83 / P.kmPerPx;
    var lines = d3.contours().size([W, H]).thresholds([0.5, buf])(Array.from(dist, function (v) { return Math.min(v, 60); }));
    var gp = d3.geoPath(null, ctx);
    ctx.save(); ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(201,214,220,0.55)'; ctx.lineWidth = 1.1; ctx.beginPath(); gp(lines[0]); ctx.stroke();
    ctx.restore();
    var edge = lines[1];

    return { proj: proj, land: land, dist: dist, outside: outside, edge: edge, h: h,
             xy: function (lon, lat) { return proj([lon, lat]); },
             inProvince: function (x, y) { var q = Math.round(y) * W + Math.round(x); return land[q] && outside[q] < 0.5; } };
  };

  /* Draw the province's offshore edge (aurora ice, the only use of #5AC8F0). */
  S.edgeLine = function (ctx, P, o) {
    o = o || {};
    var gp = d3.geoPath(null, ctx);
    ctx.save(); ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(5,10,20,0.55)'; ctx.lineWidth = 3.2; ctx.beginPath(); gp(P.edge); ctx.stroke();
    ctx.strokeStyle = '#5AC8F0'; ctx.lineWidth = o.width || 1.6; ctx.beginPath(); gp(P.edge); ctx.stroke();
    ctx.restore();
  };

  global.SLOPE = S;
})(window);
