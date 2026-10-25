/* akkachemak.js — THE TRIPOD ON THE FLATS, Carousel No.95's shared furniture (2026-10-24).
 *
 * One tripod on the tide flats near the head of Kachemak Bay, nine frames. This file is
 * house furniture, shared on purpose: the fixtures, the Polaris, the grain, the committed
 * Kachemak DEM, the horizon march that turns it into a real skyline from the tripod, the
 * perspective cloud deck and the twilight sky. bespoke_check strips `<script src=>` as
 * harness; every slide still composes and draws its own largest object in its own file,
 * and nothing here draws a slide. The cloud field is used by three frames only (01, 07,
 * 09), the CRAFT PLAN's limit for one drawing.
 *
 * DATA. assets/geo/ak-kachemak-dem.bin + .json: int16 metres, 1000 x 750, plate carree,
 * 59.40 to 60.00 N, 151.90 to 150.30 W (AWS terrain tiles, z12).
 *
 * FRAMES. ENU metres about the tripod: x east, y north, z up (metres above sea level).
 * Screen: a pinhole camera with vertical fov `fovV`, heading `heading` (degrees clockwise
 * from north) and pitch `pitch` (degrees, up positive). y = cy - f * tan(elev - pitch),
 * x = W/2 + f * tan(az - heading). Earth curvature with standard refraction (k 0.13) is
 * applied to every terrain sample.
 *
 * THE LIGHT. Night frames key from the northwest afterglow; object frames take az 315,
 * el 30 to 40 in screen space (the akrelief convention: az is where the light is,
 * clockwise from up). The gold is painted here only in the Polaris (DOM SVG).
 */
(function (global) {
  'use strict';
  var K = {};
  K.W = 1080; K.H = 1350; K.SC = 2;
  K.GOLD = '#FFC72C';
  K.COORDS = "59°47'N · 151°03'W";
  K.STATION = { lon: -150.985, lat: 59.795 };
  K.PAL = {
    night: '#03070E', deck: '#070D17', twilight: '#2B4A6E', belly: '#3A4659', rim: '#9FB2C6',
    glowLow: '#E6A15C', glowHigh: '#F2E2B0', mud: '#2A2A27', sheen: '#8FA3B5',
    sedge: '#5E6B3E', sedgeOct: '#A0814E', flare: '#D2463A', flareCore: '#FFD2B8',
    agi: '#D8D0A8', snow: '#F4F8FF', body: '#C9D3DD', label: '#A9B8C6', fixture: '#6F8294'
  };
  var D2R = Math.PI / 180, RE = 6371000, REFR = 0.13;

  K.hex = function (h) {
    h = h.replace('#', '');
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  };
  K.mix = function (a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; };
  K.clamp = function (v, a, b) { return v < a ? a : (v > b ? b : v); };
  K.smooth = function (a, b, v) { var t = K.clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
  K.css = function (c, a) { return 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + (a == null ? 1 : a) + ')'; };

  /* ---- canvases --------------------------------------------------------- */
  K.layer = function (w, h) {
    var c = document.createElement('canvas');
    c.width = Math.round((w || K.W) * K.SC); c.height = Math.round((h || K.H) * K.SC);
    var g = c.getContext('2d'); g.scale(K.SC, K.SC);
    return { c: c, g: g };
  };
  K.canvas = function (id, z) {
    var c = document.createElement('canvas');
    c.id = id || 'art';
    c.width = K.W * K.SC; c.height = K.H * K.SC;
    c.setAttribute('style', 'position:absolute;left:0;top:0;width:' + K.W + 'px;height:' + K.H + 'px;z-index:' + (z || 1) + ';');
    document.body.insertBefore(c, document.body.firstChild);
    var g = c.getContext('2d'); g.scale(K.SC, K.SC);
    return { c: c, g: g };
  };
  /* A per-pixel pass at design resolution (1080 x 1350, one sample per design px),
   * drawn into a 2x context with high quality smoothing. Soft fields (sky, cloud,
   * water) only; edges and marks are drawn as vectors at 2x afterwards.
   * fn(x, y) returns [r, g, b] or [r, g, b, a] in 0..255. */
  K.pixels = function (g, fn, o) {
    o = o || {};
    var x0 = o.x || 0, y0 = o.y || 0, w = o.w || K.W, h = o.h || K.H, s = o.scale || 1;
    var cw = Math.round(w * s), ch = Math.round(h * s);
    var off = document.createElement('canvas'); off.width = cw; off.height = ch;
    var og = off.getContext('2d'), img = og.createImageData(cw, ch), d = img.data;
    for (var j = 0; j < ch; j++) {
      var y = y0 + (j + 0.5) / s;
      for (var i = 0; i < cw; i++) {
        var c = fn(x0 + (i + 0.5) / s, y);
        var p = (j * cw + i) * 4;
        if (!c) { d[p + 3] = 0; continue; }
        d[p] = c[0]; d[p + 1] = c[1]; d[p + 2] = c[2]; d[p + 3] = c.length > 3 ? c[3] : 255;
      }
    }
    og.putImageData(img, 0, 0);
    g.save(); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    g.drawImage(off, x0, y0, w, h); g.restore();
    return off;
  };

  /* ---- fixtures --------------------------------------------------------- */
  K.polaris = function (x, y, s, z) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', s); svg.setAttribute('height', s);
    svg.setAttribute('viewBox', '-50 -50 100 100');
    svg.setAttribute('style', 'position:absolute;left:' + (x - s / 2) + 'px;top:' + (y - s / 2) + 'px;z-index:' + (z || 9) + ';overflow:visible;');
    svg.setAttribute('data-decorative', '');
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M0,-50 C4,-14 14,-4 50,0 C14,4 4,14 0,50 C-4,14 -14,4 -50,0 C-14,-4 -4,-14 0,-50 Z');
    p.setAttribute('fill', K.GOLD);
    svg.appendChild(p);
    document.body.appendChild(svg);
    return svg;
  };
  /* n: slide number; o.readout: the tripod readout string; o.tag: true for the
   * reconstruction tag; o.ink/o.counter/o.site override colours. */
  K.fixtures = function (n, o) {
    o = o || {};
    var mono = 'position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;';
    function add(txt, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', mono + style); d.textContent = txt;
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    K.polaris(92, 97, 22);
    add('ALASKA.AI', 'left:112px;top:80px;font-family:"Archivo",sans-serif;font-stretch:112%;font-weight:640;font-size:30px;letter-spacing:0.06em;color:' + (o.ink || K.PAL.snow) + ';');
    add((n < 10 ? '0' : '') + n + ' / 09', 'right:80px;top:84px;font-size:24px;letter-spacing:0.06em;color:' + (o.counter || K.PAL.label) + ';font-variant-numeric:tabular-nums;');
    if (o.tag) add('RECONSTRUCTION · POSITIONS ILLUSTRATIVE', 'right:80px;top:120px;font-size:19px;letter-spacing:0.06em;color:' + (o.site || K.PAL.fixture) + ';', true);
    add('alaskaaihq.com', 'left:80px;top:1294px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || K.PAL.fixture) + ';', true);
    if (o.readout) add(o.readout, 'right:80px;top:1266px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || K.PAL.fixture) + ';', true);
    add(K.COORDS, 'right:80px;top:1294px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || K.PAL.fixture) + ';', true);
  };
  K.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.07));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 280, strength: o.strength || 44, seed: o.seed || 95 });
    return d;
  };
  K.boxes = function (sel, pad) {
    pad = pad || 0;
    var out = [];
    document.querySelectorAll(sel).forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.width) out.push([r.left - pad, r.top - pad, r.width + 2 * pad, r.height + 2 * pad]);
    });
    return out;
  };

  /* ---- the DEM ---------------------------------------------------------- */
  K.loadDEM = async function (base) {
    var meta = await (await fetch(base + '/geo/ak-kachemak-dem.json')).json();
    var raw = new Int16Array(await (await fetch(base + '/geo/ak-kachemak-dem.bin')).arrayBuffer());
    var C = meta.cols, R = meta.rows, Hf = new Float32Array(C * R);
    for (var i = 0; i < C * R; i++) Hf[i] = raw[i];
    function inside(lon, lat) { return lon >= meta.west && lon <= meta.east && lat >= meta.south && lat <= meta.north; }
    function at(lon, lat) {
      var c = (lon - meta.west) / meta.dlon, r = (meta.north - lat) / meta.dlat;
      if (c < 0) c = 0; if (r < 0) r = 0;
      if (c > C - 1.001) c = C - 1.001; if (r > R - 1.001) r = R - 1.001;
      var c0 = c | 0, r0 = r | 0, fc = c - c0, fr = r - r0;
      var a = Hf[r0 * C + c0], b = Hf[r0 * C + c0 + 1], d = Hf[(r0 + 1) * C + c0], e = Hf[(r0 + 1) * C + c0 + 1];
      return (a * (1 - fc) + b * fc) * (1 - fr) + (d * (1 - fc) + e * fc) * fr;
    }
    return { meta: meta, H: Hf, C: C, R: R, at: at, inside: inside };
  };
  /* metres east / north of a reference point and back */
  K.enu = function (lon, lat, ref) {
    ref = ref || K.STATION;
    return [(lon - ref.lon) * 111320 * Math.cos(ref.lat * D2R), (lat - ref.lat) * 110570];
  };
  K.lonlat = function (e, n, ref) {
    ref = ref || K.STATION;
    return [ref.lon + e / (111320 * Math.cos(ref.lat * D2R)), ref.lat + n / 110570];
  };

  /* ---- the camera ------------------------------------------------------- */
  K.camera = function (o) {
    var cam = {
      lon: o.lon != null ? o.lon : K.STATION.lon, lat: o.lat != null ? o.lat : K.STATION.lat,
      eye: o.eye != null ? o.eye : 1.6, heading: o.heading || 0, pitch: o.pitch || 0,
      fovV: o.fovV || 54, W: o.W || K.W, H: o.H || K.H, cy: o.cy != null ? o.cy : (o.H || K.H) / 2,
      ground: o.ground != null ? o.ground : 2
    };
    cam.f = (cam.H / 2) / Math.tan(cam.fovV * D2R / 2);
    cam.z = cam.ground + cam.eye;
    cam.yOf = function (elevRad) { return cam.cy - cam.f * Math.tan(elevRad - cam.pitch * D2R); };
    cam.xOf = function (azDeg) { var da = ((azDeg - cam.heading + 540) % 360) - 180; return cam.W / 2 + cam.f * Math.tan(da * D2R); };
    cam.azOf = function (x) { return cam.heading + Math.atan2(x - cam.W / 2, cam.f) / D2R; };
    cam.elOf = function (y) { return Math.atan2(cam.cy - y, cam.f) + cam.pitch * D2R; };
    /* unit ray (ENU) through a screen point; the horizontal angle uses the true
     * pinhole direction so the plane intersections stay consistent */
    cam.ray = function (x, y) {
      var h = cam.heading * D2R, p = cam.pitch * D2R;
      var vx = (x - cam.W / 2) / cam.f, vy = (cam.cy - y) / cam.f;
      // camera basis: forward (heading, pitch), right, up
      var fx = Math.sin(h) * Math.cos(p), fy = Math.cos(h) * Math.cos(p), fz = Math.sin(p);
      var rx = Math.cos(h), ry = -Math.sin(h), rz = 0;
      var ux = -Math.sin(h) * Math.sin(p), uy = -Math.cos(h) * Math.sin(p), uz = Math.cos(p);
      var dx = fx + vx * rx + vy * ux, dy = fy + vx * ry + vy * uy, dz = fz + vx * rz + vy * uz;
      var n = Math.sqrt(dx * dx + dy * dy + dz * dz);
      return [dx / n, dy / n, dz / n];
    };
    return cam;
  };

  /* ---- the skyline: a horizon march per screen column --------------------
   * For every column, march the DEM along that column's azimuth and keep, for
   * each distance band, the highest elevation angle the terrain reaches inside
   * the band, plus the terrain normal and height at that point. Bands are drawn
   * far to near by the slide. Returns {bands: [{d0, d1, ang: Float32Array,
   * h: Float32Array, nx, ny, nz}], cols}. */
  K.horizon = function (dem, cam, o) {
    o = o || {};
    var cols = o.cols || cam.W, step = cam.W / cols;
    var edges = o.bands || [0, 3000, 8000, 16000, 30000, 70000];
    var nb = edges.length - 1, bands = [];
    for (var b = 0; b < nb; b++) bands.push({ d0: edges[b], d1: edges[b + 1], ang: new Float32Array(cols).fill(-1),
      h: new Float32Array(cols), nx: new Float32Array(cols), ny: new Float32Array(cols), nz: new Float32Array(cols).fill(1), dist: new Float32Array(cols) });
    var kx = 111320 * Math.cos(cam.lat * D2R), ky = 110570, ex = 40;
    for (var c = 0; c < cols; c++) {
      var az = cam.azOf((c + 0.5) * step) * D2R, sa = Math.sin(az), ca = Math.cos(az);
      var d = o.dmin || 40, bi = 0;
      while (d < edges[nb]) {
        while (bi < nb - 1 && d > edges[bi + 1]) bi++;
        var lon = cam.lon + d * sa / kx, lat = cam.lat + d * ca / ky;
        if (!dem.inside(lon, lat)) break;
        var hh = dem.at(lon, lat);
        if (hh < 0) hh = 0;   // the sea surface
        var drop = d * d / (2 * RE) * (1 - REFR);
        var a = Math.atan2(hh - cam.z - drop, d);
        var B = bands[bi];
        if (a > B.ang[c]) {
          B.ang[c] = a; B.h[c] = hh; B.dist[c] = d;
          var dlon = ex / kx, dlat = ex / ky;
          var gx = (dem.at(lon + dlon, lat) - dem.at(lon - dlon, lat)) / (2 * ex);
          var gy = (dem.at(lon, lat + dlat) - dem.at(lon, lat - dlat)) / (2 * ex);
          var nn = Math.sqrt(gx * gx + gy * gy + 1);
          B.nx[c] = -gx / nn; B.ny[c] = -gy / nn; B.nz[c] = 1 / nn;
        }
        d += Math.max(o.stepMin || 18, d * (o.stepK || 0.006));
      }
    }
    // a band with no terrain inside it inherits nothing; fill gaps from the next band
    return { bands: bands, cols: cols, step: step };
  };

  /* ---- the twilight sky ---------------------------------------------------
   * Colour by elevation (degrees) and azimuth (degrees) for a sun below the
   * horizon at (o.sunAz, o.sunEl). zenith/horizon/glowLow/glowHigh as rgb. */
  K.sky = function (o) {
    var Z = K.hex(o.zenith || '#070D17'), Hc = K.hex(o.horizon || '#2B4A6E');
    var GL = K.hex(o.glowLow || K.PAL.glowLow), GH = K.hex(o.glowHigh || K.PAL.glowHigh);
    var gAz = o.glowAz != null ? o.glowAz : 305, gS = o.glow != null ? o.glow : 1, spread = o.spread || 55;
    return function (el, az) {
      var t = Math.pow(K.clamp(el / (o.span || 38), 0, 1), 0.55);
      var c = K.mix(Hc, Z, t);
      var da = Math.abs(((az - gAz + 540) % 360) - 180);
      var g = gS * Math.exp(-Math.pow(da / spread, 2)) * Math.exp(-Math.max(el, 0) / (o.glowH || 7));
      if (g > 0.001) {
        var gc = K.mix(GH, GL, K.clamp(1 - el / 4, 0, 1));
        c = K.mix(c, gc, K.clamp(g, 0, 0.95));
      }
      return c;
    };
  };

  /* ---- the cloud deck -----------------------------------------------------
   * A stratocumulus layer between `base` and base + `thick` metres. sample(dir)
   * intersects the ray from the tripod with the base plane and returns
   * {a: opacity, lit: 0..1, dist: metres, d: density} or null when the ray
   * misses. Density is domain-warped fbm in ground metres, so cells shrink and
   * flatten with distance; opacity is Beer-Lambert over the slant thickness;
   * `lit` compares the density a step toward the light, so the cell edges facing
   * the light carry rims and the bellies fall dark. o.mask(x, y) in ENU metres
   * can open lanes (0..1 multiplier). */
  K.cloudField = function (o) {
    o = o || {};
    var base = o.base || 900, thick = o.thick || 300, scale = o.scale || 2600, cov = o.coverage != null ? o.coverage : 0.52;
    var sigma = o.sigma || 0.011, ox = o.ox || 13.7, oy = o.oy || -4.2, warp = o.warp != null ? o.warp : 0.6;
    var la = (o.lightAz != null ? o.lightAz : 305) * D2R, lStep = o.lightStep || 380;
    var lx = Math.sin(la) * lStep, ly = Math.cos(la) * lStep, camZ = o.camZ || 3.6, fade = o.fade || 42000;
    var oct = { octaves: o.octaves || 5, lacunarity: 2.03, gain: 0.52 };
    var soft = o.soft != null ? o.soft : 0.36, detail = o.detail || 0;
    var lo = 1 - cov - soft * 0.4, hi = 1 - cov + soft * 0.6;
    var oct2 = { octaves: 3, lacunarity: 2.1, gain: 0.5 };
    function dens(x, y) {
      var q = AK.warp2(x / scale + ox, y / scale + oy, warp, oct) * 0.5 + 0.5;
      if (detail) q += detail * 0.18 * AK.fbm2(x / (scale * 0.18) - ox, y / (scale * 0.18) + 3.3, oct2);
      if (o.cells) q += o.cells * (0.5 - K.cells(x / (o.cellSize || 1500) + ox, y / (o.cellSize || 1500) + oy));
      var v = K.smooth(lo, hi, q);
      if (o.mask) v *= o.mask(x, y);
      return v;
    }
    return {
      dens: dens,
      sample: function (dir, alt) {
        var z0 = alt != null ? alt : base;
        if (dir[2] <= 0.004) return null;
        var t = (z0 - camZ) / dir[2];
        var x = dir[0] * t, y = dir[1] * t, dist = t;
        var d0 = dens(x, y);
        if (d0 <= 0.002) return { a: 0, lit: 1, dist: dist, d: 0 };
        var d1 = dens(x + lx, y + ly);
        var lit = K.clamp(0.55 + (d0 - d1) * 1.6, 0, 1);
        var slant = Math.min(thick / Math.max(dir[2], 0.06), thick * 7);
        var a = 1 - Math.exp(-sigma * d0 * slant);
        a *= Math.exp(-dist / fade * 0.35);
        return { a: a, lit: lit, dist: dist, d: d0 };
      }
    };
  };

  /* ---- the terrain, column marched ---------------------------------------
   * The classic voxel-column render: for every device column, march the DEM
   * from near to far along that column's azimuth and paint each new surface
   * span upward from the last drawn screen y, so nearer ground occludes farther
   * ground with no sort. Only terrain above `minH` metres is painted (the flats
   * and the sea are the slide's own plane). shade(s) receives {h, nx, ny, nz,
   * dist, lon, lat, slope} and returns [r, g, b]. Spans are interpolated in
   * shade down each revealed run so nothing prints as terraces. Draws into g
   * (a 2x context) and returns {top: Float32Array of the skyline y per design
   * column}. */
  K.terrain = function (g, dem, cam, shade, o) {
    o = o || {};
    var SC = o.scale || 2, Wd = Math.round(cam.W * SC), Hd = Math.round(cam.H * SC);
    var off = document.createElement('canvas'); off.width = Wd; off.height = Hd;
    var og = off.getContext('2d'), img = og.createImageData(Wd, Hd), px = img.data;
    var kx = 111320 * Math.cos(cam.lat * D2R), ky = 110570, ex = o.normalStep || 45;
    var minH = o.minH != null ? o.minH : 10, dmax = o.dmax || 70000;
    var top = new Float32Array(cam.W).fill(1e9);
    var yBottom = o.yBottom != null ? o.yBottom * SC : Hd;
    for (var c = 0; c < Wd; c++) {
      var xd = (c + 0.5) / SC;
      var az = cam.azOf(xd) * D2R, sa = Math.sin(az), ca = Math.cos(az);
      // the horizontal distance in the pinhole model is along the column ray
      var kcol = Math.cos(Math.atan2(xd - cam.W / 2, cam.f));
      var ymin = yBottom, prev = null, d = o.dmin || 60;
      while (d < dmax) {
        var lon = cam.lon + d * sa / kx, lat = cam.lat + d * ca / ky;
        if (!dem.inside(lon, lat)) break;
        var hh = dem.at(lon, lat);
        var drop = d * d / (2 * RE) * (1 - REFR);
        var ys = (cam.cy - cam.f * Math.tan(Math.atan2(Math.max(hh, 0) - cam.z - drop, d) - cam.pitch * D2R)) * SC;
        if (hh > minH && ys < ymin) {
          var dlon = ex / kx, dlat = ex / ky;
          var gx = (dem.at(lon + dlon, lat) - dem.at(lon - dlon, lat)) / (2 * ex);
          var gy = (dem.at(lon, lat + dlat) - dem.at(lon, lat - dlat)) / (2 * ex);
          var nn = Math.sqrt(gx * gx + gy * gy + 1);
          var col = shade({ h: hh, nx: -gx / nn, ny: -gy / nn, nz: 1 / nn, dist: d, lon: lon, lat: lat,
            slope: Math.atan(Math.sqrt(gx * gx + gy * gy)) / D2R, x: xd, y: ys / SC });
          var y0 = Math.max(0, Math.floor(ys)), y1 = Math.min(Hd, Math.ceil(ymin));
          var pc = prev || col;
          for (var y = y0; y < y1; y++) {
            var t = y1 - y0 > 1 ? (y - y0) / (y1 - y0) : 0;
            var p = (y * Wd + c) * 4;
            px[p] = col[0] + (pc[0] - col[0]) * t; px[p + 1] = col[1] + (pc[1] - col[1]) * t;
            px[p + 2] = col[2] + (pc[2] - col[2]) * t; px[p + 3] = 255;
          }
          ymin = ys; prev = col;
        } else if (hh <= minH) { prev = null; if (ys < ymin) ymin = ys; }
        d += Math.max(o.stepMin || 12, d * (o.stepK || 0.004));
      }
      var dc = Math.min(cam.W - 1, xd | 0);
      if (ymin / SC < top[dc]) top[dc] = ymin / SC;
    }
    og.putImageData(img, 0, 0);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(off, 0, 0); g.restore();
    return { top: top, canvas: off };
  };

  /* cellular lumps (Worley F1, seeded hash) for stratocumulus cells */
  K.cells = function (x, y) {
    var xi = Math.floor(x), yi = Math.floor(y), best = 9;
    for (var j = -1; j <= 1; j++) for (var i = -1; i <= 1; i++) {
      var cx = xi + i, cy = yi + j;
      var h = Math.sin(cx * 127.1 + cy * 311.7) * 43758.5453; h -= Math.floor(h);
      var k = Math.sin(cx * 269.5 + cy * 183.3) * 43758.5453; k -= Math.floor(k);
      var dx = cx + 0.15 + 0.7 * h - x, dy = cy + 0.15 + 0.7 * k - y, dd = dx * dx + dy * dy;
      if (dd < best) best = dd;
    }
    return Math.sqrt(best);
  };

  /* Henyey-Greenstein phase for forward scatter toward a light direction */
  K.hg = function (cosT, g) { var gg = g * g; return (1 - gg) / Math.pow(1 + gg - 2 * g * cosT, 1.5) / (4 * Math.PI); };

  global.KACH = K;
})(typeof window !== 'undefined' ? window : globalThis);
