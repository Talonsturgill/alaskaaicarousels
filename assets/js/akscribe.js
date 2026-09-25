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

  /* A smoothed copy of a DEM (separable box blur, `passes` times, radius r
   * cells). Terrain tiles store whole metres, so on flat ground an exaggerated
   * gradient prints every 1 m step as a stripe (the Milepost 390 prototype,
   * 2026-09-25). Smoothing before the gradient is the honest fix: it removes
   * the quantisation, not the land. */
  AKS.smoothDEM = function (dem, r, passes) {
    var m = dem.meta, C = m.cols, R = m.rows, src = new Float32Array(dem.data), tmp = new Float32Array(C * R);
    r = r || 2; passes = passes || 2;
    for (var p = 0; p < passes; p++) {
      for (var j = 0; j < R; j++) for (var i = 0; i < C; i++) {
        var s = 0, n = 0;
        for (var k = -r; k <= r; k++) { var ii = i + k; if (ii >= 0 && ii < C) { s += src[j * C + ii]; n++; } }
        tmp[j * C + i] = s / n;
      }
      for (j = 0; j < R; j++) for (i = 0; i < C; i++) {
        s = 0; n = 0;
        for (k = -r; k <= r; k++) { var jj = j + k; if (jj >= 0 && jj < R) { s += tmp[jj * C + i]; n++; } }
        src[j * C + i] = s / n;
      }
    }
    function sample(lon, lat) {
      var fi = (lon - m.west) / m.dlon, fj = (m.north - lat) / m.dlat;
      if (!(fi >= 0 && fj >= 0 && fi <= C - 1 && fj <= R - 1)) return NaN;
      var i0 = Math.min(C - 2, Math.floor(fi)), j0 = Math.min(R - 2, Math.floor(fj));
      var u = fi - i0, v = fj - j0, q = j0 * C + i0;
      return src[q] * (1 - u) * (1 - v) + src[q + 1] * u * (1 - v) + src[q + C] * (1 - u) * v + src[q + C + 1] * u * v;
    }
    return { meta: m, data: src, sample: sample };
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
      sunEl: o.keyEl === undefined ? 40 : o.keyEl,
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
   * Returns {cells, strokes, widthRatio, drop:{strokes, medianM, p90M},
   *          probes:[{name, meanSlope, strokes}]}
   *
   * FUR, MEASURED (upgrade 2026-09-25, run No.68). A stroke is a claim that the
   * ground falls along it, and the fall it claims is slope x stroke length:
   * s (m/km) * len (px) / pxPerKm. `drop` is the distribution of that fall over
   * the first pass's strokes. When the MEDIAN stroke claims under
   * FUR_MEDIAN_DROP_M metres, the strokes are drawing the DEM's own texture and
   * quantisation, not form, and the field reads as fur at any s0: No.68's slide
   * 04 (z11 Slope, 19 px/km) measured 5 to 21 m across all five variants three
   * critic rounds rejected (s0 3, 9, 14, 22, and a long stroke), while the eight
   * shipped frames measured 180 to 489 m. s0 can't fix it (it only thins the
   * same short falls), so this console.errors under AKSCRIBE: (a qa WARN) and
   * names the two remedies that can. `lowReliefIntended: true` silences it for a
   * frame that means to draw micro-relief, putting the intent in the source. */
  var FUR_MEDIAN_DROP_M = 50, FUR_MIN_STROKES = 300;
  var ALLOWED_SCRIBE = ["x", "y", "w", "h", "pxPerKm", "cell", "s0", "s1", "keyAz",
    "keyEl", "color", "alpha", "minWidth", "maxWidth", "lenScale", "seed", "passes",
    "mask", "probes", "jitter", "sea", "lowReliefIntended"];
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
    var strokes = 0, wLo = Infinity, wHi = 0, d = cell * 0.5, falls = [];
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
        if (pass === 0) falls.push(s * len / ppk);      // metres this stroke claims
        for (q = 0; q < probes.length; q++) {
          pr = probes[q];
          if (x >= pr.x && x <= pr.x + pr.w && y >= pr.y && y <= pr.y + pr.h) pst[q].strokes++;
        }
      }
    }
    cx.restore();
    falls.sort(function (a, b) { return a - b; });
    var nf = falls.length;
    var drop = { strokes: nf, medianM: nf ? falls[nf >> 1] : 0, p90M: nf ? falls[Math.floor(nf * 0.9)] : 0 };
    if (nf >= FUR_MIN_STROKES && drop.medianM < FUR_MEDIAN_DROP_M && !o.lowReliefIntended) {
      console.error("AKSCRIBE: scribeRelief region [" + [X, Y, W, H].join(",") + "] will read as FUR: its median " +
        "stroke claims " + drop.medianM.toFixed(1) + " m of fall (p90 " + drop.p90M.toFixed(1) + " m, " + nf +
        " strokes), under " + FUR_MEDIAN_DROP_M + " m, so the strokes draw the DEM's texture, not form. Raising s0 " +
        "only thins the same short falls. Draw this ground with AKS.glow alone, or zoom out (lower pxPerKm) until " +
        "a stroke spans real relief. Pass lowReliefIntended: true if micro-relief is the subject.");
    }
    return { cells: cols * rows, strokes: strokes, widthRatio: wHi / wLo, drop: drop,
             probes: pst.map(function (p) { return { name: p.name, meanSlope: p.n ? p.s / p.n : 0, strokes: p.strokes }; }) };
  };

  /* LIT-FACE GLOW. The continuous-tone half of the relief: a Lambert shade of
   * the real DEM computed at `res` design px per sample, keeping only the light
   * that faces the key above flat ground's own value, written as light of
   * `color` with alpha = excess. Screened under the scribe strokes it gives the
   * ranges FORM (ridge, lit flank, dark lee) that strokes alone read as fuzz.
   *   o: x,y,w,h, pxPerKm, res, keyAz, keyEl, exag, gain, color, mask, sea */
  var ALLOWED_GLOW = ["x", "y", "w", "h", "pxPerKm", "res", "keyAz", "keyEl", "exag",
    "gain", "color", "mask", "sea"];
  AKS.glow = function (cx, proj, dem, o) {
    contract("AKS.glow", o, ALLOWED_GLOW);
    var X = o.x || 0, Y = o.y || 0, W = o.w, H = o.h, r = o.res || 3, ppk = o.pxPerKm;
    if (!(ppk > 0)) throw new Error("AKS.glow: pxPerKm is required");
    var cols = Math.ceil(W / r), rows = Math.ceil(H / r);
    var az = (o.keyAz === undefined ? 330 : o.keyAz) * Math.PI / 180;
    var el = (o.keyEl === undefined ? 40 : o.keyEl) * Math.PI / 180;
    var lx = Math.cos(el) * Math.sin(az), ly = -Math.cos(el) * Math.cos(az), lz = Math.sin(el);
    var exag = o.exag === undefined ? 6 : o.exag, gain = o.gain === undefined ? 1.6 : o.gain;
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

  /* THE MERIDIAN LOCATOR (No.68 D3). A scribed rail standing for latitude
   * lat0..lat1 along one meridian, drawn at x from y0 (north) to y1 (south),
   * with the frame's own window bracketed. Furniture, drawn in light.
   * Returns the rail rect for __akMotifs. */
  AKS.locator = function (cx, o) {
    var x = o.x, y0 = o.y0, y1 = o.y1, n = o.north || 70.6, s = o.south || 60;
    var Y = function (lat) { return y0 + (n - lat) / (n - s) * (y1 - y0); };
    cx.save();
    cx.strokeStyle = "rgba(191,221,240,0.30)"; cx.lineWidth = 1;
    cx.beginPath(); cx.moveTo(x, y0); cx.lineTo(x, y1); cx.stroke();
    for (var lat = Math.ceil(s); lat <= Math.floor(n); lat++) {
      var w = lat % 5 === 0 ? 7 : 3.5;
      cx.beginPath(); cx.moveTo(x - w, Y(lat)); cx.lineTo(x + w, Y(lat)); cx.stroke();
    }
    var a = Y(Math.min(n, o.top)), b = Y(Math.max(s, o.bottom));
    cx.strokeStyle = "#EEF7FF"; cx.lineWidth = 2;
    cx.beginPath();
    cx.moveTo(x - 7, a); cx.lineTo(x + 7, a); cx.moveTo(x, a); cx.lineTo(x, b);
    cx.moveTo(x - 7, b); cx.lineTo(x + 7, b); cx.stroke();
    (o.marks || []).forEach(function (m) {
      cx.fillStyle = m.color || "#EEF7FF";
      cx.beginPath(); cx.arc(x, Y(m.lat), m.r || 2.6, 0, Math.PI * 2); cx.fill();
    });
    cx.restore();
    return [x - 8, y0 - 2, 16, y1 - y0 + 4];
  };

  /* A federal site: a dashed ring, never filled (the deck's ink law). */
  AKS.ring = function (cx, x, y, r, o) {
    o = o || {};
    cx.save();
    // a coat-dark bed under the dashes, so a ring stays countable on lit relief or a coast (No.68 critics)
    if (o.halo !== 0) {
      cx.strokeStyle = "rgba(4,7,11," + (o.haloAlpha || 0.82) + ")"; cx.lineWidth = (o.width || 2.2) + (o.halo || 4);
      cx.beginPath(); cx.arc(x, y, r, 0, Math.PI * 2); cx.stroke();
    }
    cx.strokeStyle = o.color || "#7F93A6"; cx.lineWidth = o.width || 2.2;
    cx.lineCap = "round"; cx.setLineDash(o.dash || [0.1, 6.2]);
    cx.beginPath(); cx.arc(x, y, r, 0, Math.PI * 2); cx.stroke();
    cx.restore();
  };

  /* State ink: a gold bead or polygon laid on the film, with a meniscus
   * highlight on the key side and a thin dark ink body at the lee edge. */
  AKS.ink = function (cx, pts, o) {
    o = o || {};
    var trace = function () {
      cx.beginPath();
      if (typeof pts[0] === "number") { cx.arc(pts[0], pts[1], pts[2], 0, Math.PI * 2); }
      else { pts.forEach(function (p, i) { i ? cx.lineTo(p[0], p[1]) : cx.moveTo(p[0], p[1]); }); cx.closePath(); }
    };
    cx.save();
    trace();
    cx.shadowColor = "rgba(1,3,6,0.85)"; cx.shadowBlur = o.cast || 4;
    cx.shadowOffsetX = o.dx === undefined ? 1.2 : o.dx; cx.shadowOffsetY = o.dy === undefined ? 1.6 : o.dy;
    cx.fillStyle = "#9A7418"; cx.fill();
    cx.shadowColor = "transparent";
    var b = o.box || (typeof pts[0] === "number" ? [pts[0] - pts[2], pts[1] - pts[2], pts[2] * 2, pts[2] * 2] : null);
    if (b) {
      var g = cx.createLinearGradient(b[0], b[1], b[0] + b[2], b[1] + b[3]);
      g.addColorStop(0, "#FFDA6E"); g.addColorStop(0.38, "#FFC72C"); g.addColorStop(1, "#C9961E");
      cx.fillStyle = g;
    } else cx.fillStyle = "#FFC72C";
    // canvas stores a path in device space as it is built, so the lit body is
    // re-traced AFTER the shift; filling the old path would cover the dark lee edge
    cx.save(); cx.clip(); cx.translate(-0.6, -0.8); trace();
    cx.fill(); cx.restore();
    cx.restore();
  };

  /* THE LAMP POOL. The pen is lit by one lamp above the table, so where it
   * lies the coat is lit too, and that lit ground is what its cast shadow
   * subtracts from (house lesson No.26 and No.41: a shadow on unlit ground
   * measures nothing). Drawn as a LAY OF FINE RULES along the light axis at
   * `pitch` px, each rule's alpha following an elliptical falloff, which is the
   * No.60 recipe and never an additive radial.
   *   o: x, y (centre), rx, ry, keyAz, pitch, color, alpha */
  AKS.pool = function (cx, o) {
    var az = ((o.keyAz === undefined ? 330 : o.keyAz) - 90) * Math.PI / 180;
    var pitch = o.pitch || 1.7, rx = o.rx, ry = o.ry, a0 = o.alpha === undefined ? 0.2 : o.alpha;
    var rgb = (o.color || "#D8CBB0").match(/[0-9a-f]{2}/gi).map(function (h) { return parseInt(h, 16); });
    var col = function (a) { return "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + "," + a.toFixed(3) + ")"; };
    cx.save();
    cx.translate(o.x, o.y); cx.rotate(az);
    cx.lineWidth = 0.9;
    for (var v = -ry; v <= ry; v += pitch) {
      var t = v / ry, half = rx * Math.sqrt(Math.max(0, 1 - t * t));
      if (half < 2) continue;
      var peak = a0 * Math.pow(1 - t * t, 1.4);
      var g = cx.createLinearGradient(-half, 0, half, 0);
      g.addColorStop(0, col(0)); g.addColorStop(0.3, col(peak * 0.7)); g.addColorStop(0.5, col(peak));
      g.addColorStop(0.7, col(peak * 0.7)); g.addColorStop(1, col(0));
      cx.strokeStyle = g;
      cx.beginPath(); cx.moveTo(-half, v); cx.lineTo(half, v); cx.stroke();
    }
    cx.restore();
  };

  /* TYPE RESERVES. Punch feathered holes in a light layer where type will sit,
   * so relief never runs under a headline. Each entry is [x, y, w, h, blur,
   * alpha]; blur defaults 22, alpha 0.9. A blurred RECT, never a radial, so a
   * long line of type is reserved end to end (SKILL.md, 2026-09-10). */
  AKS.reserve = function (cx, rects) {
    cx.save();
    cx.globalCompositeOperation = "destination-out";
    rects.forEach(function (r) {
      cx.filter = "blur(" + (r[4] || 22) + "px)";
      cx.fillStyle = "rgba(0,0,0," + (r[5] === undefined ? 0.9 : r[5]) + ")";
      cx.fillRect(r[0], r[1], r[2], r[3]);
    });
    cx.restore();
  };

  /* Great-circle distance in km, for scale bars and asserts. */
  AKS.km = function (a, b) { return d3.geoDistance(a, b) * 6371.0088; };
})(window);
