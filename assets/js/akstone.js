/* akstone.js — THE COMPOSING STONE, Carousel No.93's deck furniture.
 *
 * Committed 2026-10-22. Shared by all nine slides on purpose: the fixtures, the
 * one skylight, the stone ground and the relit-height helpers must be identical
 * on every frame so the deck reads as one room under one key. bespoke_check
 * strips `<script src=>` as house harness, so this file costs the variety budget
 * nothing; every slide still draws its own largest object in its own code.
 *
 * THE ONE SKYLIGHT. Key from the upper right, az 35 (clockwise from up, screen
 * space +x right, +y down, the akrelief convention: az 35 is lit from the upper
 * right and the lee falls to the lower left), elevation 26. Casts fall down and
 * to the left, by CAST_DX, CAST_DY per unit of height.
 *
 * THE INK LAW (storyboard D1). Gold #FFC72C is DeepGreen's own words only.
 * Every slide declares it on <body data-ink>; this file never paints gold.
 */
(function (global) {
  'use strict';
  var S = {};
  S.W = 1080; S.H = 1350; S.SC = 2;
  S.LIGHT = { az: 35, el: 26 };
  S.COORDS = "60°43'N · 151°30'W";
  S.CAST = [-0.70, 0.71];             // unit direction a cast travels, down and left

  S.lightVec = function (az, el) {
    var a = az * Math.PI / 180, e = el * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  /* An offscreen canvas at the 2x backing, already scaled to design px. */
  S.layer = function (w, h) {
    var c = document.createElement('canvas');
    c.width = Math.round((w || S.W) * S.SC); c.height = Math.round((h || S.H) * S.SC);
    var g = c.getContext('2d'); g.scale(S.SC, S.SC);
    return { c: c, g: g };
  };

  /* The art canvas: full frame, 2x backing, z-index 1. */
  S.canvas = function (id) {
    var c = document.createElement('canvas');
    c.id = id || 'art';
    c.width = S.W * S.SC; c.height = S.H * S.SC;
    c.setAttribute('style', 'position:absolute;left:0;top:0;width:1080px;height:1350px;z-index:1');
    document.body.insertBefore(c, document.body.firstChild);
    var g = c.getContext('2d'); g.scale(S.SC, S.SC);
    return { c: c, g: g };
  };

  function hex(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  S.hex = hex;
  S.mix = function (a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; };
  /* A multi-stop ramp in linear-ish light: stops [[t, '#hex'], ...]. */
  S.ramp = function (stops) {
    var st = stops.map(function (s) { return [s[0], hex(s[1])]; });
    return function (t) {
      t = Math.max(0, Math.min(1, t));
      for (var i = 1; i < st.length; i++) if (t <= st[i][0]) {
        var a = st[i - 1], b = st[i], u = (t - a[0]) / Math.max(1e-6, b[0] - a[0]);
        u = u * u * (3 - 2 * u) * 0.35 + u * 0.65;
        return S.mix(a[1], b[1], u);
      }
      return st[st.length - 1][1];
    };
  };

  /* Brushed steel imposing stone with lit pools. pools: [{x, y, rx, ry, a}] in
   * design px; the pool is a circle inside a transform (never an ellipse fill:
   * canvas has no elliptical gradient). */
  S.stone = function (g, o) {
    o = o || {};
    var rng = AK.rng(o.seed || 9300);
    g.save();
    var base = g.createLinearGradient(0, 0, S.W, S.H);
    base.addColorStop(0, o.far || '#0A121C');
    base.addColorStop(0.55, o.mid || '#0D1621');
    base.addColorStop(1, o.near || '#081019');
    g.fillStyle = base; g.fillRect(0, 0, S.W, S.H);
    // the skylight falls from the upper right: a broad wash over the stone
    var wash = g.createRadialGradient(S.W * 0.95, -S.H * 0.05, 0, S.W * 0.95, -S.H * 0.05, S.H * 1.25);
    wash.addColorStop(0, 'rgba(120,140,160,' + (o.wash != null ? o.wash : 0.16) + ')');
    wash.addColorStop(1, 'rgba(120,140,160,0)');
    g.fillStyle = wash; g.fillRect(0, 0, S.W, S.H);
    (o.pools || []).forEach(function (p) {
      g.save(); g.translate(p.x, p.y); g.scale(1, p.ry / p.rx);
      var r = g.createRadialGradient(0, 0, 0, 0, 0, p.rx);
      var col = p.color || '58,76,96';
      r.addColorStop(0, 'rgba(' + col + ',' + p.a + ')');
      r.addColorStop(0.45, 'rgba(' + col + ',' + (p.a * 0.62) + ')');
      r.addColorStop(1, 'rgba(' + col + ',0)');
      g.fillStyle = r; g.beginPath(); g.arc(0, 0, p.rx, 0, Math.PI * 2); g.fill();
      g.restore();
    });
    // brushing: long faint strokes at 8 degrees, one opaque layer composited once
    var L = S.layer(); var h = L.g;
    h.strokeStyle = '#9FB2C4'; h.lineCap = 'butt';
    var n = o.strokes || 900;
    for (var i = 0; i < n; i++) {
      var y = rng() * (S.H + 200) - 100, x = rng() * S.W, len = 120 + rng() * 420;
      h.lineWidth = 0.4 + rng() * 0.8;
      h.globalAlpha = 0.25 + rng() * 0.75;
      h.beginPath(); h.moveTo(x, y); h.lineTo(x + len * 0.990, y + len * 0.139); h.stroke();
    }
    g.globalAlpha = o.brush != null ? o.brush : 0.045; g.drawImage(L.c, 0, 0, S.W, S.H);
    g.restore();
  };

  /* A soft two-part cast from a silhouette layer (any canvas at the 2x backing,
   * drawn in design px): a wide ambient cast and a tight contact cast, both down
   * and to the left, coloured as darkened stone, never black. */
  S.cast = function (g, sil, o) {
    o = o || {};
    var h = o.height || 12, col = o.color || '#03060B';
    var parts = [[h * 1.0, 18, o.ambient != null ? o.ambient : 0.55], [h * 0.25, 3, o.contact != null ? o.contact : 0.85]];
    parts.forEach(function (p) {
      var L = S.layer(); var t = L.g;
      t.drawImage(sil, 0, 0, S.W, S.H);
      t.globalCompositeOperation = 'source-in'; t.fillStyle = col; t.fillRect(0, 0, S.W, S.H);
      g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
      g.filter = 'blur(' + (p[1] * S.SC) + 'px)';
      g.globalAlpha = p[2];
      g.drawImage(L.c, S.CAST[0] * p[0] * S.SC, S.CAST[1] * p[0] * S.SC);
      g.restore();
    });
  };

  /* Relit height field into a region. height(x, y) in design px returns
   * [h, mask] (h in px of relief, mask 0..1); colour(x, y, lit, h) returns rgb.
   * Lambert against the one key plus a sky fill; written to an offscreen and
   * drawn over (mask is alpha), so it composes rather than overwrites. */
  S.relief = function (g, rect, height, colour, o) {
    o = o || {};
    var sc = S.SC, x0 = rect[0], y0 = rect[1], w = rect[2], hgt = rect[3];
    var W = Math.ceil(w * sc), H = Math.ceil(hgt * sc);
    var Hf = new Float32Array((W + 2) * (H + 2)), M = new Float32Array((W + 2) * (H + 2));
    for (var j = -1; j <= H; j++) for (var i = -1; i <= W; i++) {
      var r = height(x0 + (i + 0.5) / sc, y0 + (j + 0.5) / sc);
      Hf[(j + 1) * (W + 2) + (i + 1)] = r[0]; M[(j + 1) * (W + 2) + (i + 1)] = r[1];
    }
    var Lv = S.lightVec(o.az != null ? o.az : S.LIGHT.az, o.el != null ? o.el : S.LIGHT.el);
    var amb = o.ambient != null ? o.ambient : 0.28, dif = o.diffuse != null ? o.diffuse : 0.9;
    var off = document.createElement('canvas'); off.width = W; off.height = H;
    var cg = off.getContext('2d'), img = cg.createImageData(W, H), d = img.data;
    var str = sc * (o.strength || 1);
    for (j = 0; j < H; j++) for (i = 0; i < W; i++) {
      var k = (j + 1) * (W + 2) + (i + 1), m = M[k];
      if (m <= 0) continue;
      var dx = (Hf[k + 1] - Hf[k - 1]) * 0.5 * str / sc, dy = (Hf[k + W + 2] - Hf[k - W - 2]) * 0.5 * str / sc;
      var nx = -dx, ny = -dy, nz = 1, nl = Math.sqrt(nx * nx + ny * ny + 1);
      var lam = Math.max(0, (nx * Lv[0] + ny * Lv[1] + nz * Lv[2]) / nl);
      var lit = amb + dif * lam;
      var c = colour(x0 + (i + 0.5) / sc, y0 + (j + 0.5) / sc, lit, Hf[k]);
      var p = (j * W + i) * 4;
      d[p] = c[0]; d[p + 1] = c[1]; d[p + 2] = c[2]; d[p + 3] = Math.round(255 * Math.min(1, m));
    }
    cg.putImageData(img, 0, 0);
    g.drawImage(off, x0, y0, w, hgt);
    return off;
  };

  /* A sheet of paper on the stone, relit under the one key: a low cockle, a
   * slight curl at the edges, an optional lifted corner, and a fine tooth that
   * fades to nothing inside `quiet` rects (where type sits). Returns the
   * silhouette layer (for S.cast) and the lift region (for its own cast).
   * o: {seed, cockle, curl, lift: {corner: 'br'|'tr'|'bl', size, h}, low, high,
   *     tooth, quiet: [[x,y,w,h]], strength}. */
  S.paper = function (g, x0, y0, w, h, o) {
    o = o || {};
    AK.reseed(o.seed || 9300);
    var ck = o.cockle != null ? o.cockle : 3, curl = o.curl != null ? o.curl : 2.5;
    var lift = o.lift, ramp = S.ramp([[0, o.low || '#8F918B'], [0.55, o.mid || '#C6C8C1'], [1, o.high || '#E9EAE4']]);
    var quiet = o.quiet || [], tooth = o.tooth != null ? o.tooth : 0.035, wr = o.wrinkle || 0;
    function inQuiet(x, y) {
      for (var i = 0; i < quiet.length; i++) { var q = quiet[i];
        var dx = Math.max(q[0] - x, 0, x - q[0] - q[2]), dy = Math.max(q[1] - y, 0, y - q[1] - q[3]);
        var d = Math.hypot(dx, dy); if (d < 24) return 1 - d / 24; }
      return 0;
    }
    function liftH(x, y) {
      if (!lift) return 0;
      var u = lift.corner.indexOf('r') >= 0 ? (x - x0) : (x0 + w - x), v = lift.corner.indexOf('b') >= 0 ? (y - y0) : (y0 + h - y);
      var t = (u + v - (w + h - lift.size)) / lift.size;
      return t > 0 ? lift.h * t * t : 0;
    }
    var sil = S.layer(), sg = sil.g;
    sg.fillStyle = '#000'; sg.fillRect(x0, y0, w, h);
    S.relief(g, [x0 - 1, y0 - 1, w + 2, h + 2], function (x, y) {
      var inside = Math.min(1, Math.max(0, Math.min(x - x0, x0 + w - x, y - y0, y0 + h - y) + 0.5));
      var e = Math.min(x - x0, x0 + w - x, y - y0, y0 + h - y);
      var hh = ck * AK.fbm2(x * 0.0032, y * 0.0032, { octaves: 2 }) + wr * AK.fbm2(x * 0.012 + 7.1, y * 0.012 + 3.3, { octaves: 2 }) + (e < 28 ? curl * (1 - e / 28) * (1 - e / 28) : 0) + liftH(x, y);
      return [hh, inside];
    }, function (x, y, lit) {
      var q = inQuiet(x, y), tt = tooth * (1 - q) * AK.simplex2(x * 0.9, y * 0.9);
      var t = Math.max(0, Math.min(1, (lit - 0.25) / 0.95 + tt));
      return ramp(t);
    }, { strength: o.strength || 1.2, ambient: 0.32, diffuse: 0.85 });
    // the lit top and right edges, the lee bottom and left edges (one key, upper right)
    g.save();
    g.lineWidth = 1.2; g.strokeStyle = 'rgba(255,255,250,0.55)';
    g.beginPath(); g.moveTo(x0, y0 + 0.6); g.lineTo(x0 + w - 0.6, y0 + 0.6); g.lineTo(x0 + w - 0.6, y0 + h); g.stroke();
    g.strokeStyle = 'rgba(40,42,46,0.55)';
    g.beginPath(); g.moveTo(x0 + 0.6, y0); g.lineTo(x0 + 0.6, y0 + h - 0.6); g.lineTo(x0 + w, y0 + h - 0.6); g.stroke();
    g.restore();
    return { sil: sil.c, liftH: liftH };
  };

  /* A glyph mask canvas for metal type: text drawn white on transparent,
   * mirrored when reversed (metal type reads backwards). Offscreen only, never
   * on the slide's own canvas, so render.py's canvas-text hook is not asked to
   * judge ornament as copy. */
  S.glyphMask = function (text, o) {
    o = o || {};
    var w = o.w || 1200, h = o.h || 160;
    var c = document.createElement('canvas'); c.width = w; c.height = h;
    var g = c.getContext('2d');
    g.fillStyle = '#fff';
    g.font = (o.weight || 400) + ' ' + (o.size || 120) + 'px ' + (o.family || '"Instrument Serif"');
    g.textBaseline = 'alphabetic';
    if (o.mirror !== false) { g.translate(w, 0); g.scale(-1, 1); }
    g.fillText(text, o.x || 20, o.baseline || h * 0.78);
    return c;
  };

  /* Sample a mask canvas as a 0..1 function of (u, v) in [0,1]. Bilinear. */
  S.sampler = function (c) {
    var g = c.getContext('2d'), w = c.width, h = c.height;
    var d = g.getImageData(0, 0, w, h).data;
    return function (u, v) {
      var x = u * w - 0.5, y = v * h - 0.5;
      if (x < 0 || y < 0 || x > w - 1 || y > h - 1) return 0;
      var x0 = Math.floor(x), y0 = Math.floor(y), fx = x - x0, fy = y - y0;
      function a(xx, yy) { return d[(Math.min(h - 1, yy) * w + Math.min(w - 1, xx)) * 4 + 3] / 255; }
      return (a(x0, y0) * (1 - fx) + a(x0 + 1, y0) * fx) * (1 - fy) + (a(x0, y0 + 1) * (1 - fx) + a(x0 + 1, y0 + 1) * fx) * fy;
    };
  };

  /* A blurred copy of a canvas (for type shoulders). blur in canvas px. */
  S.blurred = function (c, px) {
    var o = document.createElement('canvas'); o.width = c.width; o.height = c.height;
    var g = o.getContext('2d'); g.filter = 'blur(' + px + 'px)'; g.drawImage(c, 0, 0);
    return o;
  };

  /* Fixtures at z-index 9: wordmark, counter, the D3 stamp, the site line and
   * the coordinates. The stamp is the frame's own filing number. */
  S.fixtures = function (n, stamp, o) {
    o = o || {};
    var css = 'position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;';
    function add(txt, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', css + style); d.textContent = txt;
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    var wm = add('ALASKA.AI', 'left:80px;top:60px;font-family:"Instrument Serif",serif;font-size:30px;letter-spacing:0.08em;color:' + (o.ink || '#F4F8FF') + ';');
    add((n < 10 ? '0' : '') + n + ' / 09', 'right:80px;top:66px;font-size:24px;letter-spacing:0.06em;color:' + (o.counter || '#A3AAB2') + ';font-variant-numeric:tabular-nums;');
    if (stamp) {
      var st = add(stamp, 'right:80px;top:104px;font-size:19px;letter-spacing:0.08em;color:' + (o.stampInk || '#8D96A0') +
        ';border:1px solid ' + (o.stampInk || '#8D96A0') + ';padding:3px 8px 2px 8px;font-variant-numeric:tabular-nums;', true);
      st.className = 'stamp';
    }
    add('alaskaaihq.com', 'left:80px;top:1284px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || '#6F8294') + ';', true);
    if (o.coords !== false)
      add(S.COORDS, 'right:80px;top:1284px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || '#6F8294') + ';', true);
    return wm;
  };

  /* Grain as a DOM tile, one cell per device pixel, above the art and below type. */
  S.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.06));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 280, strength: o.strength || 44, seed: o.seed || 93 });
    return d;
  };

  /* Lay a declared ink over a rendered material through its own silhouette.
   * `mask` is any canvas at the 2x backing whose alpha is the region (a
   * silhouette layer, a transparent second render of the meshes alone); the
   * ink is filled into that alpha and composited with `color`, so the
   * material keeps its light and takes the ink's hue. A brass relief computed
   * pixel by pixel never passes through a brush, so without this the ink the
   * frame promises was never painted, only approximated. */
  S.inkTint = function (g, mask, hex, o) {
    o = o || {};
    var L = S.layer(); var t = L.g;
    t.setTransform(1, 0, 0, 1, 0, 0);
    t.drawImage(mask, 0, 0, L.c.width, L.c.height);
    t.globalCompositeOperation = 'source-in';
    t.fillStyle = hex; t.fillRect(0, 0, L.c.width, L.c.height);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
    g.globalCompositeOperation = o.op || 'color'; g.globalAlpha = o.alpha == null ? 1 : o.alpha;
    g.drawImage(L.c, 0, 0); g.restore();
  };

  /* Rects of every [data-reserve] element, in design px, padded. */
  S.reserveRects = function (sel, pad) {
    pad = pad || 0;
    return Array.prototype.map.call(document.querySelectorAll(sel || '[data-reserve]'), function (el) {
      var r = el.getBoundingClientRect();
      return [r.left - pad, r.top - pad, r.width + 2 * pad, r.height + 2 * pad];
    });
  };

  global.STONE = S;
})(typeof window !== 'undefined' ? window : this);
