/* akborough.js — THE REGISTERED LAYER, Carousel No.94's deck furniture.
 *
 * Committed 2026-10-23. Shared by all nine slides on purpose: the fixtures,
 * the Polaris, the grain, the two committed datasets (the Fairbanks North Star
 * Borough's terrain and its 1,129 zoning polygons) and the one registered plan
 * projection must be identical on every frame, so the deck reads as one layer
 * reprinted in nine media. bespoke_check strips `<script src=>` as house
 * harness, so this file costs the variety budget nothing; every slide still
 * draws its own largest object in its own code.
 *
 * DATA.
 *   assets/geo/fnsb-dem.bin + .json   heights in metres, int16, plate carree,
 *                                     1200 x 640 cells over the borough.
 *   assets/geo/fnsb-zoning.geo.json   the borough's zoning layer, WGS84, rings
 *                                     wound for d3, properties zone/base/acres.
 *
 * THE LIGHT (storyboard, declared once). Plan frames: az 315, el 24, from the
 * upper left, casts to the lower right (akrelief convention: az is where the
 * light is, clockwise from up, screen space). Oblique frames place the low
 * October sun at the upper left of the frame by the camera heading.
 *
 * THE GOLD LAW (storyboard D2). #FFC72C means where "large" is fenced, and the
 * Polaris. This file paints gold only in the Polaris (DOM SVG).
 */
(function (global) {
  'use strict';
  var B = {};
  B.W = 1080; B.H = 1350; B.SC = 2;
  B.LIGHT = { az: 315, el: 24 };
  B.COORDS = "64°50'N · 147°43'W";
  B.GOLD = '#FFC72C';
  B.PAL = {
    night: '#050A12', slate: '#16242F', deep: '#0D1824',
    jade: '#2E6B5E', jadeLit: '#4E8F7E', jadeLee: '#1B4038',
    frost: '#DCE6EA', frostShade: '#A9BAC2', rust: '#A9502E',
    fog: '#93A7B4', alpen: '#EFB39B', snow: '#F4F8FF', snowShade: '#B9C7D6',
    spruce: '#18241F', amber: '#E0954A', type: '#F4F8FF', body: '#C9D3D9',
    label: '#A9B8C2', fixture: '#6E7F8C'
  };
  /* The registered plan box (02, 08, 09 share it to the pixel). */
  B.PLAN_BOX = [[90, 520], [990, 1250]];

  B.lightVec = function (az, el) {
    var a = az * Math.PI / 180, e = el * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  /* An offscreen canvas at the 2x backing, already scaled to design px. */
  B.layer = function (w, h) {
    var c = document.createElement('canvas');
    c.width = Math.round((w || B.W) * B.SC); c.height = Math.round((h || B.H) * B.SC);
    var g = c.getContext('2d'); g.scale(B.SC, B.SC);
    return { c: c, g: g };
  };

  /* The art canvas: full frame, 2x backing, z-index 1. */
  B.canvas = function (id, z) {
    var c = document.createElement('canvas');
    c.id = id || 'art';
    c.width = B.W * B.SC; c.height = B.H * B.SC;
    c.setAttribute('style', 'position:absolute;left:0;top:0;width:' + B.W + 'px;height:' + B.H + 'px;z-index:' + (z || 1) + ';');
    document.body.insertBefore(c, document.body.firstChild);
    var g = c.getContext('2d'); g.scale(B.SC, B.SC);
    return { c: c, g: g };
  };

  /* ---- data ------------------------------------------------------------ */
  B.loadDEM = async function (base) {
    var meta = await (await fetch(base + '/geo/fnsb-dem.json')).json();
    var raw = new Int16Array(await (await fetch(base + '/geo/fnsb-dem.bin')).arrayBuffer());
    var C = meta.cols, R = meta.rows;
    var Hf = new Float32Array(C * R);
    for (var i = 0; i < C * R; i++) Hf[i] = raw[i];
    function colOf(lon) { return (lon - meta.west) / meta.dlon; }
    function rowOf(lat) { return (meta.north - lat) / meta.dlat; }
    function at(lon, lat) {
      var c = colOf(lon), r = rowOf(lat);
      if (c < 0) c = 0; if (r < 0) r = 0;
      if (c > C - 1.001) c = C - 1.001; if (r > R - 1.001) r = R - 1.001;
      var c0 = c | 0, r0 = r | 0, fc = c - c0, fr = r - r0;
      var a = Hf[r0 * C + c0], b = Hf[r0 * C + c0 + 1], d = Hf[(r0 + 1) * C + c0], e = Hf[(r0 + 1) * C + c0 + 1];
      return (a * (1 - fc) + b * fc) * (1 - fr) + (d * (1 - fc) + e * fc) * fr;
    }
    function lonOf(c) { return meta.west + c * meta.dlon; }
    function latOf(r) { return meta.north - r * meta.dlat; }
    return { meta: meta, H: Hf, C: C, R: R, at: at, colOf: colOf, rowOf: rowOf, lonOf: lonOf, latOf: latOf };
  };

  B.loadZoning = async function (base) {
    return await (await fetch(base + '/geo/fnsb-zoning.geo.json')).json();
  };

  /* District class: 1 General Use (GU-1, GU-5), 2 every other district,
   * 3 industrial (HI, LI) which is also "other". */
  B.cls = function (f) {
    var b = f.properties.base;
    if (b === 'GU-1' || b === 'GU-5') return 1;
    if (b === 'HI' || b === 'LI') return 3;
    return 2;
  };

  /* The registered equal-area plan projection, fitted to the borough. */
  B.planProjection = function (zoning, box) {
    return d3.geoConicEqualArea().parallels([55, 65]).rotate([147, 0])
      .fitExtent(box || B.PLAN_BOX, zoning);
  };

  /* Rasterise the zoning classes onto any lon/lat grid (plate carree), for a
   * texture or a mask. Returns {w, h, cls: Uint8Array} with 0 outside the
   * borough. Drawn with flat colours on a canvas and read back, no
   * antialiasing on the class edges (each pixel takes its nearest class). */
  B.zoneRaster = function (zoning, grid) {
    var w = grid.w, h = grid.h;
    var c = document.createElement('canvas'); c.width = w; c.height = h;
    var g = c.getContext('2d');
    g.imageSmoothingEnabled = false;
    var sx = w / (grid.east - grid.west), sy = h / (grid.north - grid.south);
    function px(lon) { return (lon - grid.west) * sx; }
    function py(lat) { return (grid.north - lat) * sy; }
    var COL = ['#000000', '#010000', '#020000', '#030000'];
    function ring(r) {
      for (var i = 0; i < r.length; i++) {
        var X = px(r[i][0]), Y = py(r[i][1]);
        if (i === 0) g.moveTo(X, Y); else g.lineTo(X, Y);
      }
      g.closePath();
    }
    // General Use first, every other district over it (they are disjoint in
    // the layer; this order only decides shared edges).
    [1, 2, 3].forEach(function (k) {
      zoning.features.forEach(function (f) {
        if (!f.geometry || B.cls(f) !== k) return;
        g.beginPath();
        var polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
        polys.forEach(function (p) { p.forEach(ring); });
        g.fillStyle = 'rgb(' + k + ',0,0)';
        g.fill('evenodd');
      });
    });
    var d = g.getImageData(0, 0, w, h).data;
    var out = new Uint8Array(w * h);
    for (var i = 0; i < w * h; i++) {
      var v = d[i * 4];
      out[i] = d[i * 4 + 3] > 127 ? (v >= 3 ? 3 : v >= 2 ? 2 : v >= 1 ? 1 : 0) : 0;
    }
    return { w: w, h: h, cls: out };
  };

  /* Paths of the zoning layer through any d3 projection into a 2D context. */
  B.pathOf = function (proj, g) { return d3.geoPath(proj, g); };

  /* ---- fixtures -------------------------------------------------------- */
  /* The Polaris: a four point star, gold, SVG (DOM, so the grade never
   * shifts it). Returns the svg element. */
  B.polaris = function (x, y, s, z) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', s); svg.setAttribute('height', s);
    svg.setAttribute('viewBox', '-50 -50 100 100');
    svg.setAttribute('style', 'position:absolute;left:' + (x - s / 2) + 'px;top:' + (y - s / 2) + 'px;z-index:' + (z || 9) + ';overflow:visible;');
    svg.setAttribute('data-decorative', '');
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M0,-50 C4,-14 14,-4 50,0 C14,4 4,14 0,50 C-4,14 -14,4 -50,0 C-14,-4 -4,-14 0,-50 Z');
    p.setAttribute('fill', B.GOLD);
    svg.appendChild(p);
    document.body.appendChild(svg);
    return svg;
  };

  /* Fixtures at z-index 9: Polaris and wordmark, counter, site line and
   * coordinates. o.ink, o.counter, o.site override the inks (05 is light). */
  B.fixtures = function (n, o) {
    o = o || {};
    var css = 'position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;';
    function add(txt, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', css + style); d.textContent = txt;
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    B.polaris(92, 101, 22);
    add('ALASKA.AI', 'left:112px;top:84px;font-family:"Fraunces",serif;font-variation-settings:"opsz" 36;font-weight:600;font-size:30px;letter-spacing:0.08em;color:' + (o.ink || B.PAL.type) + ';');
    add((n < 10 ? '0' : '') + n + ' / 09', 'right:80px;top:88px;font-size:24px;letter-spacing:0.06em;color:' + (o.counter || B.PAL.label) + ';font-variant-numeric:tabular-nums;');
    add('alaskaaihq.com', 'left:80px;top:1288px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || B.PAL.fixture) + ';', true);
    if (o.coords !== false)
      add(B.COORDS, 'right:80px;top:1288px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || B.PAL.fixture) + ';', true);
  };

  /* Grain as a DOM tile, one cell per device pixel, above the art and below
   * type (instinct: grainTile is a data URL, grain is a DOM layer). */
  B.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.07));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 280, strength: o.strength || 44, seed: o.seed || 94 });
    return d;
  };

  /* Text boxes of the type on the page, in design px, for routing art away. */
  B.boxes = function (sel, pad) {
    pad = pad || 0;
    var out = [];
    document.querySelectorAll(sel).forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.width) out.push([r.left - pad, r.top - pad, r.width + 2 * pad, r.height + 2 * pad]);
    });
    return out;
  };
  B.inBoxes = function (x, y, boxes) {
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      if (x >= b[0] && x <= b[0] + b[2] && y >= b[1] && y <= b[1] + b[3]) return true;
    }
    return false;
  };


  /* ---- the borough terrain, for akthree frames (01 and 06) -------------
   * A mesh from the real DEM cells inside `bounds`, the zoning layer draped
   * as its colour map on the DEM's own lon/lat grid (so the film registers
   * cell for cell), and a tiled spruce-stand detail multiplied in by a shader
   * hook so a mid-ground slope carries stands and open snow. World units are
   * kilometres about `origin`, x east, z south, y up times VE. Furniture: the
   * slide still owns its camera, light, sky, fog and overlays.
   *   o.film = {gu: [r,g,b,mix], other: [r,g,b,mix], outside: k}   */
  B.terrain = function (THREE, dem, zon, o) {
    o = o || {};
    var LON0 = o.origin[0], LAT0 = o.origin[1];
    var KX = Math.cos(LAT0 * Math.PI / 180) * 111.32, KZ = 110.57, VE = o.VE || 2;
    var bd = o.bounds || [dem.meta.west, dem.meta.east, dem.meta.north, dem.meta.south];
    var ST = o.stride || 1;
    var c0 = Math.max(0, Math.floor(dem.colOf(bd[0]))), c1 = Math.min(dem.C - 1, Math.ceil(dem.colOf(bd[1])));
    var r0 = Math.max(0, Math.floor(dem.rowOf(bd[2]))), r1 = Math.min(dem.R - 1, Math.ceil(dem.rowOf(bd[3])));
    var nc = Math.floor((c1 - c0) / ST) + 1, nr = Math.floor((r1 - r0) / ST) + 1;
    var geo = new THREE.BufferGeometry();
    var pos = new Float32Array(nc * nr * 3), uv = new Float32Array(nc * nr * 2), r, c;
    for (r = 0; r < nr; r++) for (c = 0; c < nc; c++) {
      var lon = dem.lonOf(c0 + c * ST), lat = dem.latOf(r0 + r * ST);
      var h = dem.H[(r0 + r * ST) * dem.C + c0 + c * ST], i = r * nc + c;
      pos[i * 3] = (lon - LON0) * KX; pos[i * 3 + 1] = h / 1000 * VE; pos[i * 3 + 2] = (LAT0 - lat) * KZ;
      uv[i * 2] = c / (nc - 1); uv[i * 2 + 1] = 1 - r / (nr - 1);
    }
    var idx = new Uint32Array((nr - 1) * (nc - 1) * 6), k = 0;
    for (r = 0; r < nr - 1; r++) for (c = 0; c < nc - 1; c++) {
      var a = r * nc + c, b = a + 1, d = a + nc, e = d + 1;
      idx[k++] = a; idx[k++] = d; idx[k++] = b; idx[k++] = b; idx[k++] = d; idx[k++] = e;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    geo.setIndex(new THREE.BufferAttribute(idx, 1)); geo.computeVertexNormals();
    var wE = dem.lonOf(c0 + (nc - 1) * ST), wS = dem.latOf(r0 + (nr - 1) * ST), wW = dem.lonOf(c0), wN = dem.latOf(r0);
    var TW = o.texW || 3072, TH = Math.round(TW * nr / nc);
    var zr = B.zoneRaster(zon, { w: TW, h: TH, west: wW, east: wE, north: wN, south: wS });
    var fm = o.film || {};
    var GU = fm.gu || [101, 160, 141, 0.38], OT = fm.other || [220, 230, 234, 0.5], OUT = fm.outside == null ? 0.7 : fm.outside;
    var tc = document.createElement('canvas'); tc.width = TW; tc.height = TH;
    var tg = tc.getContext('2d'), ti = tg.createImageData(TW, TH), x, y;
    for (y = 0; y < TH; y++) for (x = 0; x < TW; x++) {
      var lo = wW + (x / (TW - 1)) * (wE - wW), la = wN - (y / (TH - 1)) * (wN - wS);
      var hh = dem.at(lo, la);
      var n = AK.fbm2(x * 0.012, y * 0.012, { octaves: 4 }) * 0.5 + 0.5;
      var spruce = Math.max(0, Math.min(1, ((o.treeline || 620) - hh) / 380)) * (0.45 + 0.55 * n);
      var R = 205 - 150 * spruce, G = 214 - 148 * spruce, Bc = 224 - 150 * spruce;
      var kk = zr.cls[y * TW + x];
      if (kk === 1) { R = R * (1 - GU[3]) + GU[0] * GU[3]; G = G * (1 - GU[3]) + GU[1] * GU[3]; Bc = Bc * (1 - GU[3]) + GU[2] * GU[3]; }
      else if (kk >= 2) { R = R * (1 - OT[3]) + OT[0] * OT[3]; G = G * (1 - OT[3]) + OT[1] * OT[3]; Bc = Bc * (1 - OT[3]) + OT[2] * OT[3]; }
      else { R *= OUT; G *= OUT; Bc *= OUT * 1.03; }
      var q = (y * TW + x) * 4;
      ti.data[q] = Math.min(255, R); ti.data[q + 1] = Math.min(255, G); ti.data[q + 2] = Math.min(255, Bc); ti.data[q + 3] = 255;
    }
    tg.putImageData(ti, 0, 0);
    var tex = new THREE.CanvasTexture(tc); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    // stands of black spruce as stamped crowns, isotropic, wrapped at the tile
    // edges so the repeat has no seam; stand density from a periodic field
    var DT = 512, dcv = document.createElement('canvas'); dcv.width = DT; dcv.height = DT;
    var dg = dcv.getContext('2d'); dg.fillStyle = '#ffffff'; dg.fillRect(0, 0, DT, DT);
    var TP = Math.PI * 2;
    function standAt(X, Y) {
      var u = X / DT * TP, v = Y / DT * TP;
      return 0.5 + 0.22 * Math.sin(2 * u + 1.3) * Math.cos(3 * v + 0.4) + 0.18 * Math.sin(5 * u + 2 * v + 2.1)
           + 0.12 * Math.cos(7 * v - 3 * u + 0.7) + 0.08 * Math.sin(11 * u + 0.5) * Math.sin(9 * v + 1.9);
    }
    var drnd = AK.rng(o.seed || 2026102361);
    for (var t = 0; t < 26000; t++) {
      var X = drnd() * DT, Y = drnd() * DT;
      // near uniform within the tile: a periodic stand field printed as a
      // lattice across 150 repeats (No.94 round 1, slides 01 and 06)
      if (drnd() > 0.42 + 0.25 * (standAt(X, Y) - 0.5)) continue;
      var rr = 0.9 + drnd() * 1.9, aa = 0.38 + drnd() * 0.34;
      dg.fillStyle = 'rgba(28,40,44,' + aa.toFixed(3) + ')';
      [-DT, 0, DT].forEach(function (ox) { [-DT, 0, DT].forEach(function (oy) {
        var X2 = X + ox, Y2 = Y + oy;
        if (X2 < -4 || X2 > DT + 4 || Y2 < -4 || Y2 > DT + 4) return;
        dg.beginPath(); dg.arc(X2, Y2, rr, 0, TP); dg.fill();
      }); });
    }
    var detTex = new THREE.CanvasTexture(dcv); detTex.wrapS = detTex.wrapT = THREE.RepeatWrapping; detTex.anisotropy = 8;
    var rep = o.detailRepeat || [150, 140], mix = o.detailMix == null ? 0.7 : o.detailMix;
    var mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.93, metalness: 0 });
    mat.onBeforeCompile = function (sh) {
      sh.uniforms.detail = { value: detTex };
      sh.fragmentShader = 'uniform sampler2D detail;\n' + sh.fragmentShader.replace('#include <map_fragment>',
        '#include <map_fragment>\n  vec2 duv = vMapUv * vec2(' + rep[0].toFixed(1) + ', ' + rep[1].toFixed(1) + ');\n' +
        // two layers at a non-commensurate scale and a 36 degree turn, so the
        // product never repeats on screen
        '  vec2 duv2 = mat2(0.809, -0.588, 0.588, 0.809) * duv * 0.713 + vec2(0.37, 0.61);\n' +
        '  vec3 dd = sqrt(texture2D(detail, duv).rgb * texture2D(detail, duv2).rgb);\n' +
        '  diffuseColor.rgb *= mix(vec3(1.0), dd, ' + mix.toFixed(2) + ');');
    };
    var mesh = new THREE.Mesh(geo, mat);
    return { mesh: mesh, LON0: LON0, LAT0: LAT0, KX: KX, KZ: KZ, VE: VE, zr: zr,
             bounds: [wW, wE, wN, wS],
             world: function (lon, lat, hm) {
               return [(lon - LON0) * KX, (hm == null ? dem.at(lon, lat) : hm) / 1000 * VE, (LAT0 - lat) * KZ]; } };
  };

  global.AKB = B;
})(window);
