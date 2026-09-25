/* akscribe.js — the light-table scribe bench (No.68, 2026-09-25).
 *
 * WHAT IT DRAWS. A map made the way USGS drew maps before computers: a sheet of
 * scribecoat film (an opaque coat on clear base) on a light table. The graver
 * cuts lines through the coat and those cuts are the ONLY places light gets
 * through, so geography is drawn as transmitted light on a dark ground. Relief
 * is a slope-and-aspect hachure field (akhachure, technique 92) off a REAL DEM,
 * with the strokes on the faces turned toward the key, drawn in light, so ranges
 * blaze and flats stay dark coat.
 *
 * WHY A BENCH AND NOT A TEMPLATE. This file owns the physics every frame shares
 * (the coat, the table glow, the halation, reading the DEM, the strip
 * projection). It owns no composition. Each slide chooses its own window, scale,
 * layers and marks, so bespoke_check sees nine different drawings.
 *
 * DATA HONESTY. Hachures are FORM shading. They are honest about relative
 * steepness and never carry a quantity. Heights come from AWS Terrain Tiles
 * (terrarium), resampled to a lon/lat grid and committed under assets/geo so a
 * render is offline and deterministic. No noise term anywhere in the height.
 *
 * USAGE
 *   const dem = await AKS.loadDEM('@@ASSETS@@/geo/ak-corridor149-dem');
 *   const proj = AKS.strip({ lon0: -149, lat0: 65.4, pxPerKm: 1.05, cx: 540, cy: 675 });
 *   AKS.coat(cx, 1080, 1350, { lamp: [220, 160], ...});
 *   AKS.relief(cx, proj, dem, { x, y, w, h, cell, ... });   // scribed light
 *   AKS.halate(cx, layerCanvas, { blur: 6, alpha: 0.22 });
 */
(function (global) {
  "use strict";
  var AKS = global.AKS || (global.AKS = {});

  var ALLOWED_RELIEF = ["x", "y", "w", "h", "cell", "passes", "seed", "keyAz",
    "keyEl", "color", "alpha", "minWidth", "maxWidth", "lenScale", "gamma",
    "hRef", "slopeRef", "relief", "mask", "probes", "jitter", "bend", "sunJitter"];

  function contract(name, opts, allowed) {
    Object.keys(opts || {}).forEach(function (k) {
      if (allowed.indexOf(k) < 0) {
        console.error("AK CONTRACT: " + name + " does not know option '" + k + "'");
        throw new Error(name + ": unknown option " + k);
      }
    });
  }

  /* A committed DEM: <base>.json (meta) + <base>.bin (int16 LE, row-major,
   * north up, plate carree). sample(lon, lat) is bilinear, NaN outside. */
  AKS.loadDEM = async function (base) {
    var meta = await (await fetch(base + ".json")).json();
    var buf = await (await fetch(base + ".bin")).arrayBuffer();
    var a = new Int16Array(buf);
    if (a.length !== meta.cols * meta.rows) {
      console.error("AK CONTRACT: DEM " + base + " has " + a.length + " cells, meta says " + meta.cols * meta.rows);
    }
    var C = meta.cols, R = meta.rows;
    function sample(lon, lat) {
      var fi = (lon - meta.west) / meta.dlon, fj = (meta.north - lat) / meta.dlat;
      if (!(fi >= 0 && fj >= 0 && fi <= C - 1 && fj <= R - 1)) return NaN;
      var i = Math.min(C - 2, Math.floor(fi)), j = Math.min(R - 2, Math.floor(fj));
      var u = fi - i, v = fj - j, k = j * C + i;
      return a[k] * (1 - u) * (1 - v) + a[k + 1] * u * (1 - v) +
             a[k + C] * (1 - u) * v + a[k + C + 1] * u * v;
    }
    return { meta: meta, data: a, sample: sample };
  };

  /* Transverse Mercator on its own central meridian, north up: the projection
   * an Ogilby strip map uses. pxPerKm is exact at the central meridian. */
  AKS.strip = function (o) {
    var R_EARTH_KM = 6371.0088;
    return d3.geoTransverseMercator()
      .rotate([-o.lon0, 0])
      .center([0, o.lat0])
      .scale(o.pxPerKm * R_EARTH_KM)
      .translate([o.cx, o.cy]);
  };

  /* The coat. Dark opaque film over a table that glows through it faintly,
   * lamp-lit from the key side by a LINEAR wash along the light axis (never an
   * additive radial pool, per the 2026-09 floor lessons), plus a film tooth made
   * of fine horizontal base striations drawn as marks. */
  AKS.coat = function (cx, W, H, o) {
    o = o || {};
    var base = o.base || "#0B1520", lit = o.lit || "#13212E", deep = o.deep || "#070D14";
    var az = (o.keyAz === undefined ? 330 : o.keyAz) * Math.PI / 180;
    var dx = Math.sin(az), dy = -Math.cos(az);
    var L = Math.hypot(W, H) / 2, mx = W / 2, my = H / 2;
    var g = cx.createLinearGradient(mx + dx * L, my + dy * L, mx - dx * L, my - dy * L);
    g.addColorStop(0, lit); g.addColorStop(0.55, base); g.addColorStop(1, deep);
    cx.fillStyle = g; cx.fillRect(0, 0, W, H);
    // film tooth: base striations, seeded, very low contrast
    var rnd = AK.rng(o.seed || 1);
    cx.save();
    cx.globalAlpha = o.tooth === undefined ? 0.05 : o.tooth;
    cx.strokeStyle = o.toothInk || "#2A4254";
    cx.lineWidth = 0.6;
    for (var y = 0; y < H; y += 3.1) {
      var x = -40 + rnd() * 60;
      cx.beginPath(); cx.moveTo(x, y + rnd() * 0.8);
      while (x < W + 40) { x += 60 + rnd() * 180; cx.lineTo(x, y + (rnd() - 0.5) * 0.9); }
      cx.stroke();
    }
    cx.restore();
  };

  /* Scribed relief: the hachure field run so its strokes land on faces turned
   * TOWARD the key (sun azimuth reversed), drawn in light. `mask(lon,lat)` may
   * return a 0..1 factor (e.g. the corridor band) multiplied into height so the
   * masked land stays uncut coat. Returns akhachure's own evidence. */
  AKS.relief = function (cx, proj, dem, o) {
    contract("AKS.relief", o, ALLOWED_RELIEF);
    var X = o.x || 0, Y = o.y || 0, W = o.w, H = o.h;
    var hRef = o.hRef || 2400;
    var mask = o.mask || null;
    function height(u, v) {
      var p = proj.invert([X + u * W, Y + v * H]);
      if (!p) return 0;
      var e = dem.sample(p[0], p[1]);
      if (!(e > 0)) return 0;
      var t = Math.min(1, e / hRef);
      if (mask) t *= mask(p[0], p[1]);
      return t;
    }
    var key = o.keyAz === undefined ? 330 : o.keyAz;
    return AK.hachureField(cx, {
      x: X, y: Y, w: W, h: H,
      seed: o.seed || 1,
      height: height,
      cell: o.cell || 7,
      passes: o.passes || 4,
      sunAz: (key + 180) % 360,        // strokes on the LIT faces
      sunEl: o.keyEl || 40,
      sunJitter: o.sunJitter === undefined ? 9 : o.sunJitter,
      color: o.color || "#BFDDF0",
      alpha: o.alpha === undefined ? 0.2 : o.alpha,
      minWidth: o.minWidth === undefined ? 0.35 : o.minWidth,
      maxWidth: o.maxWidth === undefined ? 2.4 : o.maxWidth,
      lenScale: o.lenScale === undefined ? 1.7 : o.lenScale,
      slopeGamma: o.gamma === undefined ? 0.62 : o.gamma,
      slopeRef: o.slopeRef,
      relief: o.relief === undefined ? 1 : o.relief,
      jitter: o.jitter, bend: o.bend,
      probes: o.probes || []
    });
  };

  /* SCRIBED RELIEF, measured. akhachure strokes every cell, which on a light
   * table turns flat ground into fur (prototype, 2026-09-25). A scribe only
   * cuts where there is form, so this pass measures the REAL slope in metres
   * per km (the projection's pxPerKm makes screen gradients true) and draws a
   * stroke only where it clears s0, running down the line of steepest descent,
   * brighter on faces turned to the key. Flats stay uncut coat, which is the
   * honest picture of the Slope and the Tanana flats.
   *   o: x,y,w,h, pxPerKm, cell, s0, s1 (m/km), keyAz, keyEl, color, alpha,
   *      minWidth, maxWidth, lenScale, seed, passes, mask(lon,lat)->0..1, probes
   * Returns {cells, strokes, widthRatio, probes:[{name, meanSlope, strokes}]} */
  var ALLOWED_SCRIBE = ["x", "y", "w", "h", "pxPerKm", "cell", "s0", "s1", "keyAz",
    "keyEl", "color", "alpha", "minWidth", "maxWidth", "lenScale", "seed", "passes",
    "mask", "probes", "jitter", "sea"];
  AKS.scribeRelief = function (cx, proj, dem, o) {
    contract("AKS.scribeRelief", o, ALLOWED_SCRIBE);
    var X = o.x || 0, Y = o.y || 0, W = o.w, H = o.h;
    var cell = o.cell || 6, ppk = o.pxPerKm;
    if (!(ppk > 0)) throw new Error("AKS.scribeRelief: pxPerKm is required");
    var s0 = o.s0 === undefined ? 12 : o.s0, s1 = o.s1 === undefined ? 180 : o.s1;
    var az = (o.keyAz === undefined ? 330 : o.keyAz) * Math.PI / 180;
    var el = (o.keyEl === undefined ? 40 : o.keyEl) * Math.PI / 180;
    var lx = Math.cos(el) * Math.sin(az), ly = -Math.cos(el) * Math.cos(az), lz = Math.sin(el);
    var rgb = (o.color || "#CFE6F5").match(/[0-9a-f]{2}/gi).map(function (h) { return parseInt(h, 16); });
    var a0 = o.alpha === undefined ? 0.5 : o.alpha;
    var wMin = o.minWidth || 0.4, wMax = o.maxWidth || 2.2, lenS = o.lenScale || 1.6;
    var passes = o.passes || 2, jit = o.jitter === undefined ? 0.35 : o.jitter;
    var mask = o.mask || null, probes = o.probes || [];
    var pst = probes.map(function (p) { return { name: p.name, n: 0, s: 0, strokes: 0 }; });
    var e = function (x, y) {
      var p = proj.invert([x, y]); if (!p) return NaN;
      return dem.sample(p[0], p[1]);
    };
    var cols = Math.floor(W / cell), rows = Math.floor(H / cell);
    var strokes = 0, wLo = Infinity, wHi = 0, d = cell * 0.5;
    cx.save(); cx.lineCap = "round";
    for (var pass = 0; pass < passes; pass++) {
      var rnd = AK.rng((o.seed || 1) + pass * 7919);
      var gauss = function () {
        var u = 0, v = 0, m = 0;
        do { u = rnd() * 2 - 1; v = rnd() * 2 - 1; m = u * u + v * v; } while (m >= 1 || m === 0);
        return u * Math.sqrt(-2 * Math.log(m) / m);
      };
      for (var j = 0; j < rows; j++) for (var i = 0; i < cols; i++) {
        var x = X + (i + 0.5 + gauss() * jit) * cell, y = Y + (j + 0.5 + gauss() * jit) * cell;
        var h0 = e(x, y);
        var ll = null;
        if (!(h0 > (o.sea === undefined ? 1 : o.sea))) { gauss(); gauss(); continue; }
        var gx = (e(x + d, y) - e(x - d, y)) / (2 * d) * ppk;   // metres per km
        var gy = (e(x, y + d) - e(x, y - d)) / (2 * d) * ppk;
        if (!(isFinite(gx) && isFinite(gy))) { gauss(); gauss(); continue; }
        var s = Math.sqrt(gx * gx + gy * gy);
        for (var q = 0; q < probes.length; q++) {
          var pr = probes[q];
          if (pass === 0 && x >= pr.x && x <= pr.x + pr.w && y >= pr.y && y <= pr.y + pr.h) { pst[q].n++; pst[q].s += s; }
        }
        var t = (s - s0) / (s1 - s0);
        if (t <= 0) { gauss(); gauss(); continue; }
        t = Math.min(1, t);
        // surface normal in (x right, y down, z up); 1 km horizontal = 1000 m
        var nx = -gx / 1000, ny = -gy / 1000, nz = 1, nl = Math.sqrt(nx * nx + ny * ny + 1);
        var lam = Math.max(0, (nx * lx + ny * ly + nz * lz) / nl);
        var lamF = Math.max(0, (nx * lx + ny * ly) / nl * 6 + 0.5);   // exaggerated facing term
        var m = mask ? (ll = proj.invert([x, y]), mask(ll[0], ll[1])) : 1;
        var al = a0 * Math.pow(t, 0.75) * Math.min(1, 0.18 + 0.82 * lamF) * m / passes * 1.6;
        var wpx = wMin + (wMax - wMin) * Math.pow(t, 0.8);
        var len = cell * lenS * (0.75 + 0.6 * t) * (1 + gauss() * 0.12);
        var dx = -gx / s, dy = -gy / s;                 // steepest descent
        var b = gauss() * 0.22 * len;
        if (al < 0.01) continue;
        cx.strokeStyle = "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + "," + Math.min(1, al).toFixed(3) + ")";
        cx.lineWidth = wpx;
        cx.beginPath();
        cx.moveTo(x - dx * len / 2, y - dy * len / 2);
        cx.quadraticCurveTo(x - dy * b, y + dx * b, x + dx * len / 2, y + dy * len / 2);
        cx.stroke();
        strokes++; if (wpx < wLo) wLo = wpx; if (wpx > wHi) wHi = wpx;
        for (q = 0; q < probes.length; q++) {
          pr = probes[q];
          if (x >= pr.x && x <= pr.x + pr.w && y >= pr.y && y <= pr.y + pr.h) pst[q].strokes++;
        }
      }
    }
    cx.restore();
    return { cells: cols * rows, strokes: strokes, widthRatio: wHi / wLo,
             probes: pst.map(function (p) { return { name: p.name, meanSlope: p.n ? p.s / p.n : 0, strokes: p.strokes }; }) };
  };

  /* LIT-FACE GLOW. The continuous-tone half of the relief: a Lambert shade of
   * the real DEM computed at `res` design px per sample, keeping only the light
   * that faces the key above flat ground's own value, written as light of
   * `color` with alpha = excess. Screened under the scribe strokes it gives the
   * ranges FORM (ridge, lit flank, dark lee) that strokes alone read as fuzz.
   *   o: x,y,w,h, pxPerKm, res, keyAz, keyEl, exag, gain, color, mask, sea */
  var ALLOWED_GLOW = ["x", "y", "w", "h", "pxPerKm", "res", "keyAz", "keyEl", "exag",
    "gain", "color", "mask", "sea", "lee"];
  AKS.glow = function (cx, proj, dem, o) {
    contract("AKS.glow", o, ALLOWED_GLOW);
    var X = o.x || 0, Y = o.y || 0, W = o.w, H = o.h, r = o.res || 3, ppk = o.pxPerKm;
    var cols = Math.ceil(W / r), rows = Math.ceil(H / r);
    var az = (o.keyAz === undefined ? 330 : o.keyAz) * Math.PI / 180;
    var el = (o.keyEl === undefined ? 40 : o.keyEl) * Math.PI / 180;
    var lx = Math.cos(el) * Math.sin(az), ly = -Math.cos(el) * Math.cos(az), lz = Math.sin(el);
    var exag = o.exag || 6, gain = o.gain || 1.6, lee = o.lee || 0;
    var rgb = (o.color || "#BFDDF0").match(/[0-9a-f]{2}/gi).map(function (h) { return parseInt(h, 16); });
    var E = new Float32Array((cols + 2) * (rows + 2)), C2 = cols + 2;
    for (var j = -1; j <= rows; j++) for (var i = -1; i <= cols; i++) {
      var p = proj.invert([X + (i + 0.5) * r, Y + (j + 0.5) * r]);
      var v = p ? dem.sample(p[0], p[1]) : NaN;
      E[(j + 1) * C2 + i + 1] = isFinite(v) ? v : 0;
    }
    var flat = lz;                                // Lambert of level ground
    var cv = document.createElement("canvas"); cv.width = cols; cv.height = rows;
    var g = cv.getContext("2d"), img = g.createImageData(cols, rows), D = img.data;
    var sea = o.sea === undefined ? 1 : o.sea;
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) {
      var k = (j + 1) * C2 + i + 1, h0 = E[k], q = (j * cols + i) * 4;
      if (!(h0 > sea)) { D[q + 3] = 0; continue; }
      var gx = (E[k + 1] - E[k - 1]) / (2 * r) * ppk / 1000 * exag;
      var gy = (E[k + C2] - E[k - C2]) / (2 * r) * ppk / 1000 * exag;
      var nl = Math.sqrt(gx * gx + gy * gy + 1);
      var lam = (-gx * lx - gy * ly + lz) / nl;
      var a = Math.max(0, lam - flat) * gain;
      if (lee) a = Math.max(a, 0);
      var m = 1;
      if (o.mask) { var pp = proj.invert([X + (i + 0.5) * r, Y + (j + 0.5) * r]); m = o.mask(pp[0], pp[1]); }
      D[q] = rgb[0]; D[q + 1] = rgb[1]; D[q + 2] = rgb[2]; D[q + 3] = Math.min(255, a * m * 255);
    }
    g.putImageData(img, 0, 0);
    cx.save();
    cx.imageSmoothingEnabled = true; cx.imageSmoothingQuality = "high";
    cx.drawImage(cv, X, Y, cols * r, rows * r);
    cx.restore();
  };

  /* Halation: the light layer blurred ONCE offscreen and screened back, so the
   * cuts glow like light through film. ctx.filter is applied once per call. */
  AKS.halate = function (cx, layer, o) {
    o = o || {};
    var W = layer.width, H = layer.height;
    var h = document.createElement("canvas"); h.width = W; h.height = H;
    var hx = h.getContext("2d");
    hx.filter = "blur(" + (o.blur || 6) * 2 + "px)";
    hx.drawImage(layer, 0, 0);
    cx.save();
    cx.setTransform(1, 0, 0, 1, 0, 0);
    cx.globalCompositeOperation = "screen";
    cx.globalAlpha = o.alpha === undefined ? 0.22 : o.alpha;
    if (o.tint) {
      hx.filter = "none";
      hx.globalCompositeOperation = "source-in";
      hx.fillStyle = o.tint; hx.fillRect(0, 0, W, H);
    }
    cx.drawImage(h, 0, 0);
    cx.restore();
  };

  /* A 2x offscreen layer the same size as the art canvas, in design px. */
  AKS.layer = function (W, H) {
    var c = document.createElement("canvas");
    c.width = W * 2; c.height = H * 2;
    var x = c.getContext("2d"); x.scale(2, 2);
    return { canvas: c, cx: x };
  };

  /* A scribed line: a geo feature stroked as a cut, a hairline core over a
   * wider dim body, so a cut reads engraved rather than drawn with a marker. */
  AKS.scribe = function (cx, path, feature, o) {
    o = o || {};
    cx.save();
    cx.lineJoin = "round"; cx.lineCap = "round";
    cx.beginPath(); path.context(cx)(feature);
    cx.strokeStyle = o.body || "rgba(191,221,240,0.35)";
    cx.lineWidth = (o.width || 2) * 1.9; cx.stroke();
    cx.strokeStyle = o.core || "#EEF7FF";
    cx.lineWidth = o.width || 2; cx.stroke();
    cx.restore();
    path.context(null);
  };

  /* Great-circle distance in km, for scale bars and asserts. */
  AKS.km = function (a, b) { return d3.geoDistance(a, b) * 6371.0088; };
})(window);
