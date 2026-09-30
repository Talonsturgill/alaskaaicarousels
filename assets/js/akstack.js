/* akstack.js — THE COPY DESK, Carousel No. 72's chassis (2026-09-29).
 *
 * DECK FURNITURE, shared across the deck on purpose and kept in a module so
 * bespoke_check strips `<script src=>` as harness, exactly like aksheet.js,
 * aknight.js and akengrave.js. Every slide's own composition and drawing code
 * still has to earn its similarity score; this file only supplies the physics
 * of a paper world so nine frames share ONE lamp and ONE kind of sheet.
 *
 * THE WORLD. A printed federal notice is worked the way a copy desk works a
 * galley. The notice's questions are CUT through stacked sheets (terraced
 * apertures) or set as letterpress on cool newsprint. Alaska's numbers are
 * PASTED on as gold slips or shown as edge-on reams. One desk lamp, declared
 * once, azimuth 305 (upper left), elevation 26 (raking), key to fill about 3.3:1.
 * Every cast falls to the lower right, tinted as a darkened ground hue.
 *
 * THE FOUR DEPTH DEVICES.
 *  - terrace(): a glyph mask becomes a stepped aperture through N sheets. A
 *    signed distance field gives the height, a chamfer gives the walls their
 *    width, a heightfield shadow march gives the cast, and a cavity term gives
 *    the darkening a real gap has. It is the deck's master depth frame.
 *  - paperGround()/inkGround(): a sheet with bow (lamp falloff) and a
 *    raking-lit fibre tooth height field, so a large flat area is never flat.
 *  - ream(): a stack of sheets seen from the side, each sheet edge its own
 *    mark with seeded tone and offset jitter, three-face light.
 *  - slip()/tear(): the paste-up and the torn seam.
 *
 * DETERMINISM. Every caller passes its own seed. AK.rng (mulberry32), no
 * Math.random, no Date.now. Load AFTER noise.js.
 *
 * COLOUR SAFETY. Colours are [r,g,b] arrays inside this file and only turned
 * into strings at the last moment; no colour helper is nested in another.
 */
(function (global) {
  "use strict";

  var AKS = {};
  var AK = global.AK;

  /* ---------------- the lamp, declared once ---------------- */
  AKS.LIGHT = { az: 305, el: 26, key: 0.70, fill: 0.30 };
  AKS.lightVec = function (az, el) {
    var a = (az === undefined ? AKS.LIGHT.az : az) * Math.PI / 180;
    var e = (el === undefined ? AKS.LIGHT.el : el) * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  /* ---------------- colour helpers (arrays only) ---------------- */
  function hex(h) {
    h = h.replace("#", "");
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)];
  }
  function css(c, a) {
    var r = Math.max(0, Math.min(255, Math.round(c[0])));
    var g = Math.max(0, Math.min(255, Math.round(c[1])));
    var b = Math.max(0, Math.min(255, Math.round(c[2])));
    return a === undefined || a >= 1 ? "rgb(" + r + "," + g + "," + b + ")" : "rgba(" + r + "," + g + "," + b + "," + a + ")";
  }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
  function smooth(e0, e1, x) { var t = clamp((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t); }
  AKS.hex = hex; AKS.css = css; AKS.mix = mix;

  /* ---------------- Euclidean distance transform (Felzenszwalb) ---------------- */
  // f: Float32Array of 0 (feature) or INF; returns squared distances in place.
  var INF = 1e20;
  function edt1d(f, d, v, z, n) {
    var k = 0; v[0] = 0; z[0] = -INF; z[1] = INF;
    for (var q = 1; q < n; q++) {
      var s;
      while (true) {
        var p = v[k];
        s = ((f[q] + q * q) - (f[p] + p * p)) / (2 * q - 2 * p);
        if (s <= z[k]) { k--; if (k < 0) { k = 0; break; } } else break;
      }
      if (s <= z[k] && k === 0 && v[0] === 0 && false) { /* keep lints quiet */ }
      k++; v[k] = q; z[k] = s; z[k + 1] = INF;
    }
    k = 0;
    for (var q2 = 0; q2 < n; q2++) {
      while (z[k + 1] < q2) k++;
      var dq = q2 - v[k];
      d[q2] = dq * dq + f[v[k]];
    }
  }
  // inside[i] truthy => a feature pixel. Returns Float32Array of distance to the nearest feature pixel.
  AKS.edt = function (inside, w, h) {
    var g = new Float32Array(w * h);
    for (var i = 0; i < g.length; i++) g[i] = inside[i] ? 0 : INF;
    var n = Math.max(w, h);
    var f = new Float32Array(n), d = new Float32Array(n), v = new Int32Array(n), z = new Float32Array(n + 1);
    var x, y;
    for (x = 0; x < w; x++) {
      for (y = 0; y < h; y++) f[y] = g[y * w + x];
      edt1d(f, d, v, z, h);
      for (y = 0; y < h; y++) g[y * w + x] = d[y];
    }
    for (y = 0; y < h; y++) {
      for (x = 0; x < w; x++) f[x] = g[y * w + x];
      edt1d(f, d, v, z, w);
      for (x = 0; x < w; x++) g[y * w + x] = Math.sqrt(d[x]);
    }
    return g;
  };

  /* ---------------- glyph masks ---------------- */
  // Rasterise a drawing into a device-resolution alpha mask for `region`
  // ([x,y,w,h] design px). draw(ctx) is called with the context translated so
  // design coordinates land in the mask and scaled by `scale`.
  AKS.mask = function (region, scale, draw) {
    var S = scale || 2, W = Math.round(region[2] * S), H = Math.round(region[3] * S);
    // OffscreenCanvas on purpose: render.py's canvas-text hook watches the
    // on-page 2D prototype, and a mask is geometry, not a label a reader sees.
    var cv = (typeof OffscreenCanvas !== "undefined") ? new OffscreenCanvas(W, H) : document.createElement("canvas");
    cv.width = W; cv.height = H;
    var c = cv.getContext("2d", { willReadFrequently: true });
    c.fillStyle = "#000"; c.fillRect(0, 0, W, H);
    c.save(); c.scale(S, S); c.translate(-region[0], -region[1]);
    c.fillStyle = "#fff"; c.strokeStyle = "#fff";
    draw(c);
    c.restore();
    var id = c.getImageData(0, 0, W, H).data, out = new Uint8Array(W * H);
    for (var i = 0; i < out.length; i++) out[i] = id[i * 4];
    return { w: W, h: H, data: out, scale: S, region: region };
  };

  // Draw each DOM line of an element into a mask context, matching the DOM
  // glyphs (same font, size, letter-spacing, baseline). `el` must contain one
  // text node per line, e.g. <span class="ln">Limited</span>.
  AKS.domLines = function (el) {
    var out = [];
    var spans = el.querySelectorAll(".ln");
    if (!spans.length) spans = [el];
    var probe = document.createElement("canvas").getContext("2d");
    for (var i = 0; i < spans.length; i++) {
      var s = spans[i];
      var cs = getComputedStyle(s);
      var range = document.createRange(); range.selectNodeContents(s);
      var rects = range.getClientRects();
      if (!rects.length) continue;
      var r = rects[0];
      var font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
      probe.font = font;
      var ls = cs.letterSpacing === "normal" ? "0px" : cs.letterSpacing;
      if ("letterSpacing" in probe) probe.letterSpacing = ls;
      var m = probe.measureText(s.textContent);
      var asc = m.fontBoundingBoxAscent;
      out.push({ text: s.textContent, x: r.left, y: r.top + asc, font: font, letterSpacing: ls, w: r.width, h: r.height });
    }
    return out;
  };
  AKS.drawLines = function (c, lines) {
    c.textBaseline = "alphabetic"; c.textAlign = "left";
    for (var i = 0; i < lines.length; i++) {
      var l = lines[i];
      c.font = l.font;
      if ("letterSpacing" in c) c.letterSpacing = l.letterSpacing;
      c.fillText(l.text, l.x, l.y);
    }
  };

  // A blurred, offset copy of a drawn shape laid on the ground: the cast of a
  // raised cut-out numeral or map. ctx is in design px (scaled by 2 already);
  // draw(c) paints the shape in design px. o: {dx,dy,blur,color,alpha}.
  AKS.dropShadow = function (ctx, region, draw, o) {
    o = o || {};
    var S = 2, W = Math.round(region[2] * S), H = Math.round(region[3] * S);
    var cv = (typeof OffscreenCanvas !== "undefined") ? new OffscreenCanvas(W, H) : document.createElement("canvas");
    cv.width = W; cv.height = H;
    var c = cv.getContext("2d");
    c.save(); c.scale(S, S); c.translate(-region[0], -region[1]);
    c.fillStyle = o.color || "#02060A"; c.strokeStyle = c.fillStyle;
    draw(c);
    c.restore();
    ctx.save();
    ctx.globalAlpha = o.alpha === undefined ? 0.6 : o.alpha;
    ctx.filter = "blur(" + (o.blur === undefined ? 7 : o.blur) + "px)";
    ctx.drawImage(cv, region[0] + (o.dx || 10), region[1] + (o.dy || 8), region[2], region[3]);
    ctx.restore();
  };

  /* ---------------- the terraced aperture ----------------
   * opts: { region:[x,y,w,h], mask:(from AKS.mask), steps:4, stepW:5 (design px),
   *   wall:1.7, t:4.2 (sheet thickness, design px), paper:[r,g,b], pit:[r,g,b],
   *   tone:{amb,key}, soft:5, ao:0.55, tooth:0.05, seed }
   * Writes device pixels straight into ctx (a 2x canvas) with putImageData, so
   * it REPLACES whatever is in the region: lay the ground first if you want it
   * to show through the paper, or pass opts.base to shade a supplied ImageData.
   */
  AKS.terrace = function (ctx, opts) {
    var S = opts.mask.scale, W = opts.mask.w, H = opts.mask.h;
    var N = opts.steps || 4, dW = (opts.stepW || 5) * S, wallW = (opts.wall || 1.7) * S;
    var t = opts.t || 4.2;               // design px per sheet
    var paper = opts.paper, pit = opts.pit;
    var L = AKS.lightVec(opts.az, opts.el);
    var tanEl = Math.tan((opts.el === undefined ? AKS.LIGHT.el : opts.el) * Math.PI / 180);
    var amb = opts.tone ? opts.tone.amb : AKS.LIGHT.fill, key = opts.tone ? opts.tone.key : AKS.LIGHT.key;
    var iFlat = amb + key * L[2];
    var dark = opts.pit || [14, 26, 36];

    // signed distance (device px): >0 outside the glyph, <0 inside. `invert`
    // swaps the roles, so the drawn shape becomes a RAISED plateau that steps
    // up from the ground (a paper-cut map, cut-paper numerals) instead of a hole.
    var inside = new Uint8Array(W * H), outside = new Uint8Array(W * H), i;
    for (i = 0; i < inside.length; i++) {
      var on = opts.mask.data[i] > 127 ? 1 : 0;
      if (opts.invert) on = 1 - on;
      inside[i] = on; outside[i] = 1 - on;
    }
    var dOut = AKS.edt(inside, W, H);
    var dIn = AKS.edt(outside, W, H);
    var sd = new Float32Array(W * H);
    for (i = 0; i < sd.length; i++) sd[i] = inside[i] ? -(dIn[i] - 0.5) : (dOut[i] - 0.5);

    // height in design px: pit floor at -N*t, top sheet at 0
    var Ht = new Float32Array(W * H);
    for (i = 0; i < Ht.length; i++) {
      var d = sd[i], s = 0;
      for (var b = 0; b < N; b++) s += smooth(-wallW * 0.5, wallW * 0.5, d - b * dW);
      Ht[i] = -N * t + s * t;
    }
    var R = Math.round(6 * S), blur = boxBlur(Ht, W, H, R);
    var hx = L[0] / Math.hypot(L[0], L[1]), hy = L[1] / Math.hypot(L[0], L[1]);
    var steps = Math.ceil((N * t / tanEl + 3) * S / 0.8), stepPx = 0.8;
    var softK = (opts.soft || 5) / 1;
    var img = ctx.createImageData(W, H), od = img.data;
    var tooth = opts.tooth === undefined ? 0.04 : opts.tooth;
    var rnd = AK.rng((opts.seed || 1) * 7919 + 13);
    var ground = opts.base ? opts.base : null;          // ImageData of the ground, device res, same region
    var pitEps = -N * t + 0.05 * t;
    for (var y = 0; y < H; y++) {
      for (var x = 0; x < W; x++) {
        var k = y * W + x, h0 = Ht[k];
        var xl = x > 0 ? Ht[k - 1] : h0, xr = x < W - 1 ? Ht[k + 1] : h0;
        var yu = y > 0 ? Ht[k - W] : h0, yd = y < H - 1 ? Ht[k + W] : h0;
        var dhx = (xr - xl) / (2 / S), dhy = (yd - yu) / (2 / S);
        var nl = 1 / Math.sqrt(dhx * dhx + dhy * dhy + 1);
        var lam = Math.max(0, (-dhx * L[0] - dhy * L[1] + L[2]) * nl);
        var maxEx = 0;
        for (var st = 1; st <= steps; st++) {
          var sx = Math.round(x + hx * st * stepPx), sy = Math.round(y + hy * st * stepPx);
          if (sx < 0 || sy < 0 || sx >= W || sy >= H) break;
          var ex = Ht[sy * W + sx] - (h0 + st * stepPx / S * tanEl);
          if (ex > maxEx) maxEx = ex;
        }
        var sh = 1 - smooth(0, softK * 0.1 * t, maxEx);
        var cav = clamp((blur[k] - h0) / (N * t * 0.6), 0, 1);
        var ao = 1 - (opts.ao === undefined ? 0.5 : opts.ao) * cav;
        var I = (amb * ao + key * lam * (0.35 + 0.65 * sh) * (0.6 + 0.4 * ao)) / iFlat;
        var o = k * 4, n = 1 + (rnd() - 0.5) * 2 * tooth;
        var isPit = h0 <= pitEps;
        if (isPit && ground && opts.invert) {
          // raised shape on a ground: the ground shows through, darkened only by the cast and cavity terms
          var gi = k * 4, Ig = clamp(I, 0, 1.15);
          od[o] = clamp(ground.data[gi] * Ig, 0, 255); od[o + 1] = clamp(ground.data[gi + 1] * Ig, 0, 255);
          od[o + 2] = clamp(ground.data[gi + 2] * Ig, 0, 255); od[o + 3] = 255;
          continue;
        }
        var base = isPit ? dark : paper;
        if (!isPit && ground && !opts.invert) { var gj = k * 4; base = [ground.data[gj], ground.data[gj + 1], ground.data[gj + 2]]; }
        if (!isPit) I *= 1 - 0.10 * ((-h0) / (N * t));
        var r = base[0] * I, g = base[1] * I, bl = base[2] * I;
        if (I > 1) { var over = clamp((I - 1) * 1.2, 0, 1); r += (255 - r) * over; g += (255 - g) * over; bl += (255 - bl) * over; }
        od[o] = clamp(r * n, 0, 255); od[o + 1] = clamp(g * n, 0, 255); od[o + 2] = clamp(bl * n, 0, 255); od[o + 3] = 255;
      }
    }
    ctx.putImageData(img, Math.round(opts.mask.region[0] * S), Math.round(opts.mask.region[1] * S));
    return { W: W, H: H, height: Ht };
  };

  function boxBlur(src, W, H, R) {
    var tmp = new Float32Array(W * H), out = new Float32Array(W * H), x, y, acc, n = 2 * R + 1;
    for (y = 0; y < H; y++) {
      acc = 0;
      for (x = -R; x <= R; x++) acc += src[y * W + clamp(x, 0, W - 1)];
      for (x = 0; x < W; x++) {
        tmp[y * W + x] = acc / n;
        acc += src[y * W + clamp(x + R + 1, 0, W - 1)] - src[y * W + clamp(x - R, 0, W - 1)];
      }
    }
    for (x = 0; x < W; x++) {
      acc = 0;
      for (y = -R; y <= R; y++) acc += tmp[clamp(y, 0, H - 1) * W + x];
      for (y = 0; y < H; y++) {
        out[y * W + x] = acc / n;
        acc += tmp[clamp(y + R + 1, 0, H - 1) * W + x] - tmp[clamp(y - R, 0, H - 1) * W + x];
      }
    }
    return out;
  }
  AKS.boxBlur = boxBlur;


  /* ---------------- grounds ---------------- */
  // A sheet with bow (the lamp falls off toward the lower right) and a
  // raking-lit fibre tooth. opts: {rect:[x,y,w,h], color:[r,g,b], seed, bow:0.07,
  // tooth:0.035, fibres:900, freq:0.55}. Draws at device resolution into a 2x canvas.
  AKS.paperGround = function (ctx, opts) {
    var S = 2, r = opts.rect, W = Math.round(r[2]), H = Math.round(r[3]);
    var col = opts.color, bow = opts.bow === undefined ? 0.07 : opts.bow;
    var toothA = opts.tooth === undefined ? 0.035 : opts.tooth, fq = opts.freq || 0.55;
    var L = AKS.lightVec(), rnd = AK.rng((opts.seed || 1) * 104729 + 5);
    var hf = new Float32Array((W + 2) * (H + 2)), x, y;
    var ox = (opts.seed || 1) * 37.1, oy = (opts.seed || 1) * 11.7;
    for (y = 0; y < H + 2; y++) for (x = 0; x < W + 2; x++)
      hf[y * (W + 2) + x] = AK.fbm2(ox + x * fq, oy + y * fq, { octaves: 3, lacunarity: 2.1, gain: 0.55 });
    var cv = document.createElement("canvas"); cv.width = W; cv.height = H;
    var c = cv.getContext("2d"), img = c.createImageData(W, H), d = img.data;
    var lx = L[0], ly = L[1];
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) {
      var k = (y + 1) * (W + 2) + x + 1;
      var gx = hf[k + 1] - hf[k - 1], gy = hf[k + W + 2] - hf[k - W - 2];
      var lit = (-gx * lx - gy * ly) * 2.2;           // raking light on the fibre relief
      var fall = 1 + bow * (0.5 - (x / W * 0.55 + y / H * 0.45)) * 2; // lamp falloff (bow)
      var f = fall * (1 + lit * toothA * 4);
      var o = (y * W + x) * 4;
      d[o] = clamp(col[0] * f, 0, 255); d[o + 1] = clamp(col[1] * f, 0, 255); d[o + 2] = clamp(col[2] * f, 0, 255); d[o + 3] = 255;
    }
    c.putImageData(img, 0, 0);
    // loose fibres: short curved hairs, light and dark, very low alpha
    var nF = opts.fibres === undefined ? 900 : opts.fibres;
    c.lineWidth = 0.6;
    for (var i = 0; i < nF; i++) {
      var fx = rnd() * W, fy = rnd() * H, a = rnd() * Math.PI, len = 5 + rnd() * 17, bend = (rnd() - 0.5) * 0.9;
      var lightF = rnd() < 0.5;
      c.strokeStyle = lightF ? "rgba(255,255,255," + (0.10 + rnd() * 0.14) + ")" : "rgba(20,32,42," + (0.05 + rnd() * 0.07) + ")";
      c.beginPath(); c.moveTo(fx, fy);
      c.quadraticCurveTo(fx + Math.cos(a + bend) * len * 0.5, fy + Math.sin(a + bend) * len * 0.5, fx + Math.cos(a) * len, fy + Math.sin(a) * len);
      c.stroke();
    }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
    ctx.drawImage(cv, 0, 0, W, H, r[0] * S, r[1] * S, W * S, H * S);
    ctx.restore();
  };

  // Press-black ink film: low-frequency mottle, orange-peel relief, bow.
  AKS.inkGround = function (ctx, opts) {
    var S = 2, r = opts.rect, W = Math.round(r[2]), H = Math.round(r[3]);
    var col = opts.color, bow = opts.bow === undefined ? 0.16 : opts.bow;
    var L = AKS.lightVec(), x, y, ox = (opts.seed || 1) * 19.3, oy = (opts.seed || 1) * 7.9;
    var hf = new Float32Array((W + 2) * (H + 2));
    for (y = 0; y < H + 2; y++) for (x = 0; x < W + 2; x++)
      hf[y * (W + 2) + x] = AK.fbm2(ox + x * 0.16, oy + y * 0.16, { octaves: 3, lacunarity: 2.2, gain: 0.5 });
    var cv = document.createElement("canvas"); cv.width = W; cv.height = H;
    var c = cv.getContext("2d"), img = c.createImageData(W, H), d = img.data;
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) {
      var k = (y + 1) * (W + 2) + x + 1;
      var gx = hf[k + 1] - hf[k - 1], gy = hf[k + W + 2] - hf[k - W - 2];
      var lit = (-gx * L[0] - gy * L[1]);
      var mot = 1 + hf[k] * 0.07;
      var fall = 1 + bow * (0.5 - (x / W * 0.55 + y / H * 0.45)) * 2;
      var f = fall * mot * (1 + lit * 0.55);
      var o = (y * W + x) * 4;
      d[o] = clamp(col[0] * f, 0, 255); d[o + 1] = clamp(col[1] * f, 0, 255); d[o + 2] = clamp(col[2] * f, 0, 255); d[o + 3] = 255;
    }
    c.putImageData(img, 0, 0);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
    ctx.drawImage(cv, 0, 0, W, H, r[0] * S, r[1] * S, W * S, H * S);
    ctx.restore();
  };

  /* ---------------- objects (design-px context, already scale(2,2)) ---------------- */
  var CAST = [0.819, 0.574];   // horizontal direction shadows fall, from the lamp
  AKS.CAST = CAST;

  AKS.grabGround = function (ctx, region) {
    var S = 2;
    return ctx.getImageData(Math.round(region[0] * S), Math.round(region[1] * S), Math.round(region[2] * S), Math.round(region[3] * S));
  };

  // Lamp pool: lit ground under an object. The idiom is a circle inside a transform.
  AKS.pool = function (cx, x, y, rx, ry, color, alpha) {
    cx.save(); cx.translate(x, y); cx.scale(rx / 100, ry / 100);
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, 100);
    g.addColorStop(0, css(color, alpha)); g.addColorStop(0.45, css(color, alpha * 0.75));
    g.addColorStop(0.8, css(color, alpha * 0.25)); g.addColorStop(1, css(color, 0));
    cx.fillStyle = g; cx.beginPath(); cx.arc(0, 0, 100, 0, Math.PI * 2); cx.fill(); cx.restore();
  };

  // Two-part cast: a tight contact term and a wide ambient term, tinted, never black.
  // pathFn(cx) must only build a path (no beginPath).
  AKS.cast = function (cx, pathFn, o) {
    o = o || {};
    var col = o.color || [4, 8, 12];
    var tight = o.tight === undefined ? 2.2 : o.tight, wide = o.wide === undefined ? 9 : o.wide;
    var passes = [
      { d: tight, blur: 1.3, a: (o.aTight === undefined ? 0.42 : o.aTight) },
      { d: wide, blur: 7, a: (o.aWide === undefined ? 0.24 : o.aWide) }
    ];
    for (var i = 0; i < passes.length; i++) {
      cx.save();
      cx.filter = "blur(" + passes[i].blur + "px)";
      cx.translate(CAST[0] * passes[i].d, CAST[1] * passes[i].d);
      cx.fillStyle = css(col, passes[i].a);
      cx.beginPath(); pathFn(cx); cx.fill();
      cx.restore();
    }
  };

  // Seeded deckled polygon for a rectangle.
  function deckle(x, y, w, h, amp, rnd) {
    var pts = [], step = 7, i, n;
    function edge(x0, y0, x1, y1, nx, ny) {
      n = Math.max(2, Math.round(Math.hypot(x1 - x0, y1 - y0) / step));
      var prev = 0;
      for (i = 0; i < n; i++) {
        var t = i / n, j = (rnd() - 0.5) * 2 * amp; j = prev * 0.45 + j * 0.55; prev = j;
        pts.push([x0 + (x1 - x0) * t + nx * j, y0 + (y1 - y0) * t + ny * j]);
      }
    }
    edge(x, y, x + w, y, 0, 1); edge(x + w, y, x + w, y + h, -1, 0);
    edge(x + w, y + h, x, y + h, 0, -1); edge(x, y + h, x, y, 1, 0);
    return pts;
  }
  AKS.deckle = deckle;

  function polyPath(cx, pts) {
    cx.moveTo(pts[0][0], pts[0][1]);
    for (var i = 1; i < pts.length; i++) cx.lineTo(pts[i][0], pts[i][1]);
    cx.closePath();
  }

  /* slip: a gold paste-up strip. opts {x,y,w,h,seed,rot,lift:{size},dash:false,
   * gold:[base,lit,lee] as [r,g,b] arrays, amp} ; returns {pts}.
   * With opts.dash the slip is an empty phantom (hidden-line dash, no fill). */
  AKS.slip = function (cx, o) {
    var rnd = AK.rng((o.seed || 1) * 6151 + 3);
    var G = o.gold || [hex("#FFC72C"), hex("#FFD766"), hex("#B58913")];
    var amp = o.amp === undefined ? 1.5 : o.amp;
    cx.save();
    if (o.rot) { cx.translate(o.x + o.w / 2, o.y + o.h / 2); cx.rotate(o.rot * Math.PI / 180); cx.translate(-(o.x + o.w / 2), -(o.y + o.h / 2)); }
    var pts = deckle(o.x, o.y, o.w, o.h, amp, rnd);
    if (o.dash) {
      cx.strokeStyle = css(o.dashColor || [35, 71, 154], 0.9); cx.lineWidth = 2; cx.setLineDash([12, 7, 4, 7]); cx.lineCap = "butt";
      cx.beginPath(); polyPath(cx, pts); cx.stroke(); cx.setLineDash([]); cx.restore(); return { pts: pts };
    }
    var lift = o.lift ? o.lift.size : 0;
    var body = pts;
    if (lift) {
      // cut the lower-right corner off along the fold line
      body = [];
      var fx = o.x + o.w, fy = o.y + o.h;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        if ((p[0] - (fx - lift)) + (p[1] - (fy - lift)) > lift) continue; // beyond the fold diagonal
        body.push(p);
      }
      // close along the fold diagonal
      var q = [[fx - lift * 0.02, fy - lift * 1.0], [fx - lift * 1.0, fy - lift * 0.02]];
      // insert fold points in order: after last top/right point
      var ins = [];
      for (var j = 0; j < body.length; j++) ins.push(body[j]);
      body = ins;
      var cut = [];
      for (var m = 0; m < pts.length; m++) cut.push(pts[m]);
      // rebuild cleanly: walk the polygon, replace the corner run by the two fold points
      body = [];
      var inCorner = false;
      for (var k = 0; k < pts.length; k++) {
        var pk = pts[k], onCorner = (pk[0] - (fx - lift)) + (pk[1] - (fy - lift)) > lift;
        if (onCorner) { if (!inCorner) { body.push([fx, fy - lift]); body.push([fx - lift, fy]); inCorner = true; } }
        else body.push(pk);
      }
    }
    // shadows first (two-part), then the body
    AKS.cast(cx, function (c) { polyPath(c, body); }, { tight: o.tight === undefined ? 2.4 : o.tight, wide: o.wide === undefined ? 9 : o.wide, aTight: 0.55, aWide: 0.34, color: o.castColor || [16, 28, 36] });
    var g = cx.createLinearGradient(o.x, o.y, o.x + o.w * 0.6, o.y + o.h * 1.6);
    g.addColorStop(0, css(G[1])); g.addColorStop(0.35, css(G[0])); g.addColorStop(1, css(mix(G[0], G[2], 0.55)));
    cx.fillStyle = g; cx.beginPath(); polyPath(cx, body); cx.fill();
    // fibre tooth clipped to the slip
    cx.save(); cx.beginPath(); polyPath(cx, body); cx.clip();
    var nf = Math.round(o.w * o.h / 90);
    for (var f = 0; f < nf; f++) {
      var fx0 = o.x + rnd() * o.w, fy0 = o.y + rnd() * o.h, a = rnd() * Math.PI, len = 3 + rnd() * 9;
      cx.strokeStyle = rnd() < 0.5 ? "rgba(255,244,190," + (0.10 + rnd() * 0.16) + ")" : "rgba(120,80,0," + (0.05 + rnd() * 0.08) + ")";
      cx.lineWidth = 0.6; cx.beginPath(); cx.moveTo(fx0, fy0); cx.lineTo(fx0 + Math.cos(a) * len, fy0 + Math.sin(a) * len); cx.stroke();
    }
    // lit upper-left rim, shaded lower-right rim (the paper's own edge)
    cx.lineWidth = 1.6; cx.strokeStyle = css(G[1], 0.85);
    cx.beginPath(); cx.moveTo(o.x, o.y + o.h); cx.lineTo(o.x, o.y); cx.lineTo(o.x + o.w, o.y); cx.stroke();
    cx.strokeStyle = css(G[2], 0.55); cx.beginPath(); cx.moveTo(o.x + o.w, o.y); cx.lineTo(o.x + o.w, o.y + o.h); cx.lineTo(o.x, o.y + o.h); cx.stroke();
    cx.restore();
    if (lift) {
      var fxx = o.x + o.w, fyy = o.y + o.h;
      // the flap: the corner folded back over the slip, its underside a paler gold
      var flap = [[fxx, fyy - lift], [fxx - lift, fyy], [fxx - lift * 1.05, fyy - lift * 1.05]];
      cx.save();
      cx.filter = "blur(4px)"; cx.fillStyle = "rgba(20,32,40,0.30)";
      cx.beginPath(); cx.moveTo(flap[0][0] - lift * 0.1, flap[0][1] + 3); cx.lineTo(flap[1][0] + 3, flap[1][1] - lift * 0.1); cx.lineTo(flap[2][0] + 5, flap[2][1] + 5); cx.closePath(); cx.fill();
      cx.restore();
      var fg = cx.createLinearGradient(flap[2][0], flap[2][1], fxx, fyy);
      fg.addColorStop(0, css(mix(G[1], [255, 255, 240], 0.55))); fg.addColorStop(1, css(mix(G[0], [255, 250, 220], 0.35)));
      cx.fillStyle = fg; cx.beginPath(); cx.moveTo(flap[0][0], flap[0][1]); cx.lineTo(flap[1][0], flap[1][1]); cx.lineTo(flap[2][0], flap[2][1]); cx.closePath(); cx.fill();
      cx.strokeStyle = css(G[2], 0.5); cx.lineWidth = 0.9; cx.stroke();
    }
    cx.restore();
    return { pts: body };
  };

  /* ream: edge-on stack of sheets in cabinet oblique.
   * o {x, y (base), w, sheets, pitch, dx, dy, seed, jitter, gold:[from,to] in sheet units from the bottom,
   *    paper:{front,side,top} arrays, gold:{front,side,top}, castLen} */
  AKS.ream = function (cx, o) {
    var rnd = AK.rng((o.seed || 1) * 4241 + 7);
    var P = o.paper || { front: hex("#C6D0D3"), side: hex("#7F8E96"), top: hex("#E4E9EA") };
    var Gd = o.goldSet || { front: hex("#FFC72C"), side: hex("#B58913"), top: hex("#FFD766") };
    var n = o.sheets, pitch = o.pitch, dx = o.dx || 0, dy = o.dy || 0, jit = o.jitter === undefined ? 1.1 : o.jitter;
    var total = n * pitch, topY = o.y - total;
    var g0 = o.gold ? o.gold[0] : 1e9, g1 = o.gold ? o.gold[1] : -1;
    var castLen = o.castLen === undefined ? 130 : o.castLen;
    // ground shadow: a parallelogram on the ground plane, fading with distance
    if (castLen > 0) {
      cx.save();
      var gs = cx.createLinearGradient(o.x + o.w, o.y, o.x + o.w + castLen, o.y);
      gs.addColorStop(0, "rgba(3,7,11,0.55)"); gs.addColorStop(0.6, "rgba(3,7,11,0.22)"); gs.addColorStop(1, "rgba(3,7,11,0)");
      cx.filter = "blur(3px)"; cx.fillStyle = gs;
      cx.beginPath(); cx.moveTo(o.x + 4, o.y + 1); cx.lineTo(o.x + o.w + castLen, o.y + 1);
      cx.lineTo(o.x + o.w + castLen + dx, o.y - dy); cx.lineTo(o.x + dx + 4, o.y - dy); cx.closePath(); cx.fill();
      cx.restore();
    }
    var tones = [], jx = [], jw = [];
    for (var k = 0; k < n; k++) { tones.push(1 + (rnd() - 0.5) * 0.10); jx.push((rnd() - 0.5) * 2 * jit); jw.push((rnd() - 0.5) * 2 * jit); }
    function paintSheet(k, F, Sd, tn, x0, w, yb, yt) {
      if (dx) {
        cx.fillStyle = css([Sd[0] * tn, Sd[1] * tn, Sd[2] * tn]);
        cx.beginPath(); cx.moveTo(x0 + w, yt); cx.lineTo(x0 + w + dx, yt - dy); cx.lineTo(x0 + w + dx, yb - dy); cx.lineTo(x0 + w, yb); cx.closePath(); cx.fill();
        cx.strokeStyle = "rgba(6,12,18,0.42)"; cx.lineWidth = 0.6;
        cx.beginPath(); cx.moveTo(x0 + w, yb); cx.lineTo(x0 + w + dx, yb - dy); cx.stroke();
      }
      cx.fillStyle = css([F[0] * tn, F[1] * tn, F[2] * tn]); cx.fillRect(x0, yt, w, pitch + 0.25);
      cx.fillStyle = "rgba(255,255,255,0.30)"; cx.fillRect(x0, yt, Math.min(2.6, w), pitch);              // lit left cap
      cx.fillStyle = "rgba(6,12,18,0.20)"; cx.fillRect(x0 + w - 2.2, yt, 2.2, pitch);                      // shaded right edge
      cx.fillStyle = "rgba(255,255,255,0.28)"; cx.fillRect(x0, yt, w, 0.7);                                  // lit top edge of the sheet
      cx.fillStyle = "rgba(6,12,18,0.50)"; cx.fillRect(x0, yb - 0.75, w, 0.75);                             // seam
    }
    for (k = 0; k < n; k++) {
      var yb = o.y - k * pitch, yt = yb - pitch;
      var x0 = o.x + jx[k], w = o.w + jw[k], tn = tones[k];
      paintSheet(k, P.front, P.side, tn, x0, w, yb, yt);
      var a = Math.max(k, g0), b = Math.min(k + 1, g1);
      if (b > a) {                       // gold occupies [a,b] of this sheet, in sheet units from the bottom
        var yA = o.y - a * pitch, yB = o.y - b * pitch;
        cx.save(); cx.beginPath(); cx.rect(x0 - 1, yB - dy - 1, w + dx + 2, (yA - yB) + dy + 2); cx.clip();
        if (b - a >= 0.999) paintSheet(k, Gd.front, Gd.side, tn, x0, w, yb, yt);
        else {
          cx.fillStyle = css(Gd.front); cx.fillRect(x0, yB, w, yA - yB);
          cx.fillStyle = "rgba(255,255,255,0.35)"; cx.fillRect(x0, yB, w, 0.7);
          if (dx) { cx.fillStyle = css(Gd.side); cx.beginPath(); cx.moveTo(x0 + w, yB); cx.lineTo(x0 + w + dx, yB - dy); cx.lineTo(x0 + w + dx, yA - dy); cx.lineTo(x0 + w, yA); cx.closePath(); cx.fill(); }
        }
        cx.restore();
      }
    }
    // lamp falloff across the front face: lit at the left, shaded toward the right, and a faint bow toward the base
    var fo = cx.createLinearGradient(o.x, 0, o.x + o.w, 0);
    fo.addColorStop(0, "rgba(255,255,255,0.05)"); fo.addColorStop(1, "rgba(4,10,16,0.24)");
    cx.fillStyle = fo; cx.fillRect(o.x - 1, topY, o.w + 2, total);
    var fv = cx.createLinearGradient(0, topY, 0, o.y);
    fv.addColorStop(0, "rgba(255,255,255,0.04)"); fv.addColorStop(1, "rgba(4,10,16,0.16)");
    cx.fillStyle = fv; cx.fillRect(o.x - 1, topY, o.w + 2, total);
    // top face
    var lastGold = (g1 >= n && (g1 - Math.max(g0, n - 1)) >= 0.999);
    var T = lastGold ? Gd.top : P.top;
    if (dx) {
      var tg = cx.createLinearGradient(o.x, topY, o.x + dx + o.w, topY - dy);
      tg.addColorStop(0, css(T)); tg.addColorStop(1, css(mix(T, [150, 165, 172], 0.35)));
      cx.fillStyle = tg; cx.beginPath(); cx.moveTo(o.x, topY); cx.lineTo(o.x + dx, topY - dy); cx.lineTo(o.x + o.w + dx, topY - dy); cx.lineTo(o.x + o.w, topY); cx.closePath(); cx.fill();
      cx.strokeStyle = "rgba(255,255,255,0.55)"; cx.lineWidth = 1; cx.beginPath(); cx.moveTo(o.x, topY); cx.lineTo(o.x + dx, topY - dy); cx.stroke();
      for (var sp = 0; sp < 40; sp++) {
        cx.fillStyle = rnd() < 0.5 ? "rgba(255,255,255,0.14)" : "rgba(10,20,30,0.08)";
        var u = rnd(), v = rnd(); cx.fillRect(o.x + v * dx + u * o.w, topY - v * dy, 1.2, 1);
      }
    }
    return { top: topY, total: total };
  };

  /* record: the ten funding years as slabs whose thickness is dollars.
   * o {x, y (base), w, values (in $ millions, bottom first), k (px per $ million), dx, dy, seed,
   *    theme:'ink'|'paper', goldIdx, hairIdx:[..], partIdx, castLen} */
  AKS.record = function (cx, o) {
    var rnd = AK.rng((o.seed || 1) * 991 + 17);
    var ink = (o.theme || "ink") === "ink";
    var front = ink ? hex("#C6D0D3") : hex("#6F808B"), side = ink ? hex("#7F8E96") : hex("#3F505B"), top = ink ? hex("#E4E9EA") : hex("#93A3AD");
    var G = { front: hex("#FFC72C"), side: hex("#B58913"), top: hex("#FFD766") };
    var dx = o.dx === undefined ? 14 : o.dx, dy = o.dy === undefined ? 8 : o.dy;
    var y = o.y, i, hair = o.hairIdx || [];
    var totalH = 0; for (i = 0; i < o.values.length; i++) totalH += o.values[i] * o.k;
    if ((o.castLen === undefined ? 60 : o.castLen) > 0) {
      var cl = o.castLen === undefined ? 60 : o.castLen;
      cx.save(); var gs = cx.createLinearGradient(o.x + o.w, o.y, o.x + o.w + cl + dx, o.y);
      gs.addColorStop(0, ink ? "rgba(3,7,11,0.55)" : "rgba(30,44,54,0.42)"); gs.addColorStop(1, "rgba(3,7,11,0)");
      cx.filter = "blur(2.5px)"; cx.fillStyle = gs;
      cx.beginPath(); cx.moveTo(o.x + 3, y + 1); cx.lineTo(o.x + o.w + cl, y + 1); cx.lineTo(o.x + o.w + cl + dx, y - dy); cx.lineTo(o.x + dx + 3, y - dy); cx.closePath(); cx.fill(); cx.restore();
    }
    var bounds = [];
    for (i = 0; i < o.values.length; i++) {
      var h = o.values[i] * o.k, yb = y, yt = y - h;
      var gold = (i === o.goldIdx), part = (i === o.partIdx), tn = 1 + (rnd() - 0.5) * 0.06;
      var F = gold ? G.front : front, Sd = gold ? G.side : side, T = gold ? G.top : top;
      var jx = (rnd() - 0.5) * 1.6;
      if (part) {
        cx.save(); cx.setLineDash([9, 6]); cx.lineWidth = 1.4; cx.strokeStyle = css(ink ? [198, 208, 211] : [63, 80, 91], 0.9);
        cx.strokeRect(o.x + jx, yt, o.w, h); cx.setLineDash([]);
        cx.strokeStyle = css(ink ? [198, 208, 211] : [63, 80, 91], 0.35); cx.lineWidth = 0.7;
        for (var hx = 0; hx < o.w; hx += 8) { cx.beginPath(); cx.moveTo(o.x + jx + hx, yt + h); cx.lineTo(o.x + jx + Math.min(o.w, hx + h), yt); cx.stroke(); }
        cx.restore();
      } else {
        if (dx) {
          cx.fillStyle = css([Sd[0] * tn, Sd[1] * tn, Sd[2] * tn]);
          cx.beginPath(); cx.moveTo(o.x + jx + o.w, yt); cx.lineTo(o.x + jx + o.w + dx, yt - dy); cx.lineTo(o.x + jx + o.w + dx, yb - dy); cx.lineTo(o.x + jx + o.w, yb); cx.closePath(); cx.fill();
        }
        var g = cx.createLinearGradient(0, yt, 0, yb);
        g.addColorStop(0, css([F[0] * tn * 1.06, F[1] * tn * 1.06, F[2] * tn * 1.06])); g.addColorStop(1, css([F[0] * tn * 0.92, F[1] * tn * 0.92, F[2] * tn * 0.92]));
        cx.fillStyle = g; cx.fillRect(o.x + jx, yt, o.w, h + 0.25);
        if (o.sheetPx && h >= 7) {           // the individual sheets inside a slab: fine seams with seeded tone and offset
          for (var ly = yt + o.sheetPx; ly < yb - 1; ly += o.sheetPx * (0.85 + rnd() * 0.3)) {
            cx.fillStyle = "rgba(6,12,18," + (0.16 + rnd() * 0.16) + ")"; cx.fillRect(o.x + jx + (rnd() - 0.5) * 1.6, ly, o.w, 0.7);
            cx.fillStyle = "rgba(255,255,255," + (0.10 + rnd() * 0.12) + ")"; cx.fillRect(o.x + jx, ly + 0.7, o.w, 0.6);
          }
        }
        cx.fillStyle = "rgba(255,255,255,0.28)"; cx.fillRect(o.x + jx, yt, 2.6, h);
        cx.fillStyle = "rgba(255,255,255,0.32)"; cx.fillRect(o.x + jx, yt, o.w, 0.8);
        cx.fillStyle = "rgba(6,12,18,0.55)"; cx.fillRect(o.x + jx, yb - 0.8, o.w, 0.8);
        if (hair.indexOf(i) >= 0) { cx.strokeStyle = css(G.front, 0.95); cx.lineWidth = 1.2; cx.strokeRect(o.x + jx + 0.6, yt + 0.6, o.w - 1.2, h - 1.2); }
        // the slab's top face, visible only where nothing sits above
        if (dx && i === o.values.length - 1) {
          cx.fillStyle = css(T); cx.beginPath(); cx.moveTo(o.x + jx, yt); cx.lineTo(o.x + jx + dx, yt - dy); cx.lineTo(o.x + jx + o.w + dx, yt - dy); cx.lineTo(o.x + jx + o.w, yt); cx.closePath(); cx.fill();
        }
      }
      bounds.push([yt, yb]);
      y = yt;
    }
    return { top: y, total: totalH, bounds: bounds };
  };

  /* sheetRow: n upright sheets in a row (n may be fractional; the last is cut to width).
   * o {x, y (top of the row), h, n, pitch, sheet, seed, dx, dy, gold:bool} */
  AKS.sheetRow = function (cx, o) {
    var rnd = AK.rng((o.seed || 1) * 313 + 29);
    var P = o.gold ? { front: hex("#FFC72C"), side: hex("#B58913"), top: hex("#FFD766") } : { front: hex("#C6D0D3"), side: hex("#7F8E96"), top: hex("#E4E9EA") };
    var dx = o.dx === undefined ? 5 : o.dx, dy = o.dy === undefined ? 4 : o.dy;
    var full = Math.floor(o.n), frac = o.n - full, total = Math.ceil(o.n);
    var endX = o.x + (total - 1) * o.pitch + (frac > 0 ? o.sheet * frac : o.sheet);
    // one cast for the whole row
    cx.save(); cx.filter = "blur(2.5px)"; cx.fillStyle = "rgba(3,7,11,0.42)";
    cx.beginPath(); cx.moveTo(o.x + 3, o.y + o.h + 1); cx.lineTo(endX + 6, o.y + o.h + 1); cx.lineTo(endX + 6 + 6, o.y + o.h + 6); cx.lineTo(o.x + 9, o.y + o.h + 6); cx.closePath(); cx.fill(); cx.restore();
    for (var i = 0; i < total; i++) {
      var sx = o.x + i * o.pitch, sw = (i === full && frac > 0) ? Math.max(1.2, o.sheet * frac) : o.sheet;
      var tn = 1 + (rnd() - 0.5) * 0.12, jy = (rnd() - 0.5) * 1.2;
      cx.fillStyle = css([P.front[0] * tn, P.front[1] * tn, P.front[2] * tn]); cx.fillRect(sx, o.y + jy, sw, o.h);
      cx.fillStyle = "rgba(255,255,255,0.34)"; cx.fillRect(sx, o.y + jy, Math.min(1.5, sw), o.h);
      cx.fillStyle = "rgba(6,12,18,0.26)"; cx.fillRect(sx + sw - 1.2, o.y + jy, 1.2, o.h);
      cx.fillStyle = css(P.top); cx.beginPath(); cx.moveTo(sx, o.y + jy); cx.lineTo(sx + dx * 0.6, o.y + jy - dy); cx.lineTo(sx + sw + dx * 0.6, o.y + jy - dy); cx.lineTo(sx + sw, o.y + jy); cx.closePath(); cx.fill();
    }
    return { endX: endX };
  };

  /* tear: a seeded torn-seam polyline, x as a function of y. */
  AKS.tearPath = function (seed, x0, y0, y1, amp) {
    var rnd = AK.rng((seed || 1) * 271 + 5), pts = [], ph = rnd() * 100, prev = 0;
    for (var y = y0; y <= y1; y += 3) {
      var n = AK.fbm2(ph + y * 0.008, seed * 3.1, { octaves: 4, lacunarity: 2.3, gain: 0.55 });
      prev = prev * 0.5 + (rnd() - 0.5) * 3.2 * 0.5;
      pts.push([x0 + n * amp + prev, y]);
    }
    return pts;
  };
  // Draws the paper's torn edge over the ink: cast onto the ink at the right, a pale fibre fringe.
  AKS.tearEdge = function (cx, path, seed) {
    var rnd = AK.rng((seed || 1) * 733 + 41), i;
    cx.save(); cx.filter = "blur(4px)"; cx.fillStyle = "rgba(2,6,10,0.55)";
    cx.beginPath(); cx.moveTo(path[0][0] + 2, path[0][1]);
    for (i = 1; i < path.length; i++) cx.lineTo(path[i][0] + 8, path[i][1] + 5);
    for (i = path.length - 1; i >= 0; i--) cx.lineTo(path[i][0] - 4, path[i][1]);
    cx.closePath(); cx.fill(); cx.restore();
    // fibre fringe: pale strokes leaving the edge
    for (i = 0; i < path.length; i++) {
      var k = 1 + Math.floor(rnd() * 3);
      for (var f = 0; f < k; f++) {
        var len = 2 + rnd() * 9, a = (rnd() - 0.5) * 1.3, px = path[i][0], py = path[i][1] + (rnd() - 0.5) * 3;
        cx.strokeStyle = "rgba(226,232,234," + (0.35 + rnd() * 0.5) + ")"; cx.lineWidth = 0.5 + rnd() * 0.7;
        cx.beginPath(); cx.moveTo(px - 1, py); cx.quadraticCurveTo(px + len * 0.5, py + Math.sin(a) * len * 0.5, px + len, py + Math.sin(a) * len); cx.stroke();
      }
    }
    cx.strokeStyle = "rgba(240,244,245,0.70)"; cx.lineWidth = 1.2; cx.beginPath();
    cx.moveTo(path[0][0], path[0][1]); for (i = 1; i < path.length; i++) cx.lineTo(path[i][0], path[i][1]); cx.stroke();
    cx.strokeStyle = "rgba(120,134,142,0.55)"; cx.lineWidth = 2.4; cx.beginPath();
    cx.moveTo(path[0][0] - 3, path[0][1]); for (i = 1; i < path.length; i++) cx.lineTo(path[i][0] - 3, path[i][1]); cx.stroke();
  };

  /* ribbon: a tapered hand-drawn stroke with graphite grain along a polyline. */
  AKS.ribbon = function (cx, pts, o) {
    var rnd = AK.rng((o.seed || 1) * 557 + 3), w = o.w || 3, col = o.color || [42, 85, 168];
    var n = pts.length, left = [], right = [], i;
    for (i = 0; i < n; i++) {
      var a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
      var t = i / (n - 1), tw = w * (0.35 + 0.65 * Math.pow(Math.sin(Math.PI * t), 0.6)) * (1 + (rnd() - 0.5) * 0.12);
      left.push([pts[i][0] - dy / l * tw / 2, pts[i][1] + dx / l * tw / 2]); right.push([pts[i][0] + dy / l * tw / 2, pts[i][1] - dx / l * tw / 2]);
    }
    cx.save(); cx.fillStyle = css(col, 0.88);
    cx.beginPath(); cx.moveTo(left[0][0], left[0][1]); for (i = 1; i < n; i++) cx.lineTo(left[i][0], left[i][1]);
    for (i = n - 1; i >= 0; i--) cx.lineTo(right[i][0], right[i][1]); cx.closePath(); cx.fill();
    cx.clip();
    for (i = 0; i < n * 26; i++) {           // graphite grain: pale flecks knocked out of the stroke
      var q = pts[Math.floor(rnd() * n)]; cx.fillStyle = "rgba(230,236,238," + (0.10 + rnd() * 0.22) + ")";
      cx.fillRect(q[0] + (rnd() - 0.5) * w * 1.4, q[1] + (rnd() - 0.5) * w * 1.4, 0.8 + rnd() * 1.4, 0.7 + rnd() * 1.1);
    }
    cx.restore();
  };

  // Polaris: a four-point star, gold, the only star in the deck.
  AKS.polaris = function (cx, x, y, r, color) {
    var c = color || [255, 199, 44];
    cx.save(); cx.translate(x, y);
    cx.beginPath();
    for (var i = 0; i < 8; i++) {
      var a = -Math.PI / 2 + i * Math.PI / 4, rr = (i % 2 === 0) ? r : r * 0.26;
      cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr);
    }
    cx.closePath();
    var g = cx.createLinearGradient(-r, -r, r, r); g.addColorStop(0, css(mix(c, [255, 240, 190], 0.6))); g.addColorStop(0.5, css(c)); g.addColorStop(1, css(mix(c, [120, 80, 0], 0.4)));
    cx.fillStyle = g; cx.fill(); cx.restore();
  };

  global.AKSTACK = AKS;
})(typeof window !== "undefined" ? window : globalThis);
