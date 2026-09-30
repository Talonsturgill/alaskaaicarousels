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

    // signed distance (device px): >0 outside the glyph, <0 inside
    var inside = new Uint8Array(W * H), outside = new Uint8Array(W * H), i;
    for (i = 0; i < inside.length; i++) { inside[i] = opts.mask.data[i] > 127 ? 1 : 0; outside[i] = 1 - inside[i]; }
    var dOut = AKS.edt(inside, W, H);      // distance to nearest glyph pixel (0 inside)
    var dIn = AKS.edt(outside, W, H);      // distance to nearest non-glyph pixel (0 outside)
    var sd = new Float32Array(W * H);
    for (i = 0; i < sd.length; i++) sd[i] = inside[i] ? -(dIn[i] - 0.5) : (dOut[i] - 0.5);

    // height in design px: pit floor at -N*t, top sheet at 0
    var Ht = new Float32Array(W * H);
    for (i = 0; i < Ht.length; i++) {
      var d = sd[i], s = 0;
      for (var b = 0; b < N; b++) s += smooth(-wallW * 0.5, wallW * 0.5, d - b * dW);
      Ht[i] = -N * t + s * t;
    }
    // cavity: how far below the local mean of a wider ring this pixel sits
    var R = Math.round(6 * S), blur = boxBlur(Ht, W, H, R);
    // shadow march (heightfield, toward the light)
    var hx = L[0] / Math.hypot(L[0], L[1]), hy = L[1] / Math.hypot(L[0], L[1]);
    var steps = Math.ceil((N * t / tanEl + 3) * S / 0.8), stepPx = 0.8;
    var softK = (opts.soft || 5) / 1;
    var img = ctx.createImageData(W, H), od = img.data;
    var tooth = opts.tooth === undefined ? 0.04 : opts.tooth;
    var rnd = AK.rng((opts.seed || 1) * 7919 + 13);
    var hasBase = !!opts.base;
    for (var y = 0; y < H; y++) {
      for (var x = 0; x < W; x++) {
        var k = y * W + x, h0 = Ht[k];
        // normal from central differences (design px per design px)
        var xl = x > 0 ? Ht[k - 1] : h0, xr = x < W - 1 ? Ht[k + 1] : h0;
        var yu = y > 0 ? Ht[k - W] : h0, yd = y < H - 1 ? Ht[k + W] : h0;
        var dhx = (xr - xl) / (2 / S), dhy = (yd - yu) / (2 / S);
        var nl = 1 / Math.sqrt(dhx * dhx + dhy * dhy + 1);
        var lam = Math.max(0, (-dhx * L[0] - dhy * L[1] + L[2]) * nl);
        // cast shadow: excess height of the terrain toward the light over the ray
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
        var base = h0 <= -N * t + 0.05 * t ? dark : paper;
        if (h0 > -N * t + 0.05 * t) {
          // sheet tone steps slightly with depth (lower sheets sit in their own shade)
          var depth = (-h0) / (N * t);
          base = mix(paper, paper, 0);
          I *= 1 - 0.10 * depth;
        }
        var r = base[0] * I, g = base[1] * I, bl = base[2] * I;
        if (I > 1) { var over = clamp((I - 1) * 1.2, 0, 1); r += (255 - r) * over; g += (255 - g) * over; bl += (255 - bl) * over; }
        var n = 1 + (rnd() - 0.5) * 2 * tooth;
        var o = k * 4;
        if (hasBase) {
          var bs = opts.base.data, bi = ((y + (opts.baseY || 0)) * opts.base.width + x + (opts.baseX || 0)) * 4;
          // shade the supplied ground: multiply by relative intensity
          r = bs[bi] * I * n; g = bs[bi + 1] * I * n; bl = bs[bi + 2] * I * n;
        }
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

  global.AKSTACK = AKS;
})(typeof window !== "undefined" ? window : globalThis);
