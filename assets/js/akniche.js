/* akniche.js — THE INSTRUMENT NICHE, Carousel No.113's deck furniture.
 *
 * Committed 2026-11-12. One Southeast slate window sill scanned end to end
 * across nine frames (a panorama spine): the sill lines, the key light, the
 * gold channel and the fixtures are identical on every frame by construction,
 * so the deck reads as one niche under one run of windows. bespoke_check strips
 * `<script src=>` as house harness; every slide still draws its own instrument
 * (its largest object) in its own code. This file never paints an instrument.
 *
 * GEOMETRY (design px, constant on every frame):
 *   void / niche back   y 0 to 968
 *   sill top            y 968 (back edge) to 1024 (front arris), foreshortened
 *   chamfer             y 1024 to 1032
 *   face                y 1032 to 1350
 *   gold channel        y 1130 to 1162 on the face
 * Global x for frame n is gx = (n - 1) * 1080 + x, so a seam is exact.
 *
 * THE KEY. A run of tall windows behind camera left, about 35 degrees up, pale
 * warm #FFE2B8, at roughly 6:1 to a cool slate bounce #142338. Its strength is
 * one smooth function of gx through the frame-centre values in N.KEYS, which
 * is the deck's tonal arc (peak on 05, darkest on 07 under a stone pier).
 * Window mullions throw slanted shadow bars across the sill top.
 *
 * THE INK LAW. Gold #FFC72C is the line where a number belongs, nothing else
 * (plus the brand Polaris on 09). This file draws the CHANNEL the gold sits in
 * and never paints gold itself; the gold is DOM text above the art.
 */
(function (global) {
  'use strict';
  var N = {};
  N.W = 1080; N.H = 1350; N.SC = 2;
  N.Y_BACK = 968; N.Y_ARRIS = 1024; N.Y_CHAMF = 1032;
  N.CH_Y = 1130; N.CH_H = 32;
  N.KEYS = [0.85, 1.05, 1.10, 0.60, 1.45, 1.05, 0.30, 0.95, 1.30];
  N.SEED = 113012;
  N.COORDS = "61°13'N · 149°54'W";
  N.KEY_DIR = [0.62, 0.78];        // screen direction a cast travels: down and right

  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function smooth(e0, e1, x) { var t = clamp((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t); }
  N.clamp = clamp; N.smooth = smooth;
  function hex(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  N.hex = hex;

  /* Monotone cubic through the frame centres: K(gx). */
  N.key = function (gx) {
    var xs = [], ys = N.KEYS, n = ys.length, i;
    for (i = 0; i < n; i++) xs.push(i * 1080 + 540);
    if (gx <= xs[0]) return ys[0];
    if (gx >= xs[n - 1]) return ys[n - 1];
    var d = [], m = [];
    for (i = 0; i < n - 1; i++) d.push((ys[i + 1] - ys[i]) / 1080);
    m.push(d[0]);
    for (i = 1; i < n - 1; i++) m.push(d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2);
    m.push(d[n - 2]);
    for (i = 0; i < n - 1; i++) {
      if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
      var a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b;
      if (s > 9) { var t = 3 / Math.sqrt(s); m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]; }
    }
    for (i = 0; i < n - 1; i++) if (gx <= xs[i + 1]) {
      var h = 1080, u = (gx - xs[i]) / h, u2 = u * u, u3 = u2 * u;
      return (2 * u3 - 3 * u2 + 1) * ys[i] + (u3 - 2 * u2 + u) * h * m[i] +
             (-2 * u3 + 3 * u2) * ys[i + 1] + (u3 - u2) * h * m[i + 1];
    }
    return ys[n - 1];
  };

  /* Offscreen layer at the 2x backing, scaled to design px. */
  N.layer = function (w, h) {
    var c = document.createElement('canvas');
    c.width = Math.round((w || N.W) * N.SC); c.height = Math.round((h || N.H) * N.SC);
    var g = c.getContext('2d'); g.scale(N.SC, N.SC);
    return { c: c, g: g };
  };

  /* The art canvas, full frame, 2x backing, z-index 1. */
  N.canvas = function (id) {
    var c = document.createElement('canvas');
    c.id = id || 'art';
    c.width = N.W * N.SC; c.height = N.H * N.SC;
    c.setAttribute('style', 'position:absolute;left:0;top:0;width:1080px;height:1350px;z-index:1');
    document.body.insertBefore(c, document.body.firstChild);
    var g = c.getContext('2d'); g.scale(N.SC, N.SC);
    return { c: c, g: g };
  };

  /* Window mullion bars on the sill top: 1 in the light, 0 in a bar. The bars
   * slant because the key comes from the left. */
  function mullion(gx, t) {
    var u = gx + 150 * t + 260, p = ((u % 1350) + 1350) % 1350;
    return 1 - 0.62 * (smooth(1180, 1210, p) - smooth(1290, 1320, p));
  }
  N.mullion = mullion;

  /* Slate height and vein strength at texture coords (u, v). */
  function slate(u, v) {
    var w = AK.fbm2(u * 0.004, v * 0.004, { octaves: 3 });
    var lam = Math.sin(v * 0.21 + w * 5.0 + AK.simplex2(u * 0.002, v * 0.01) * 2.4) + 0.5 * Math.sin(v * 0.07 + w * 2.0);
    // open quartz veins: a warped diagonal phase, so the lines run long and never close into loops
    var ph = (u * 0.62 + v * 0.78) * 0.0036 + AK.fbm2(u * 0.0018 + 11.3, v * 0.0026 - 4.1, { octaves: 3 }) * 1.9;
    var fr = ph - Math.floor(ph), taper = smooth(0.15, 0.55, AK.fbm2(u * 0.0012 - 3.3, v * 0.002 + 8.1, { octaves: 2 }) + 0.35);
    var vein = (1 - smooth(0.0, 0.012, Math.min(fr, 1 - fr))) * taper;
    var ph2 = (u * 0.9 - v * 0.4) * 0.0052 + AK.fbm2(u * 0.003 - 7.7, v * 0.004 + 2.2, { octaves: 2 }) * 1.4;
    var fr2 = ph2 - Math.floor(ph2);
    var vein2 = (1 - smooth(0.0, 0.008, Math.min(fr2, 1 - fr2))) * taper * 0.6;
    var grain = AK.simplex2(u * 0.35, v * 0.9) * 0.5 + AK.simplex2(u * 1.1, v * 1.7) * 0.25;
    var h = 0.9 * w + 0.30 * lam + 0.25 * vein + 0.10 * vein2 + 0.10 * grain;
    return [h, Math.max(vein, vein2 * 0.5) * 0.55, grain];
  }

  var SL = [hex('#141C26'), hex('#2B3642'), hex('#5E6B78'), hex('#8996A3')];
  var QZ = hex('#C9CFD3');
  function slateCol(t) {
    t = clamp(t, 0, 1.3);
    var seg = t < 0.4 ? 0 : t < 0.8 ? 1 : 2, a = seg * 0.4, u = clamp((t - a) / 0.4, 0, 1);
    var c0 = SL[seg], c1 = SL[Math.min(3, seg + 1)];
    return [c0[0] + (c1[0] - c0[0]) * u, c0[1] + (c1[1] - c0[1]) * u, c0[2] + (c1[2] - c0[2]) * u];
  }

  /* The niche: void, sill top, arris, chamfer, face, gold channel, optional
   * jambs. g is the art context (design px). n is the frame number 1..9.
   * o: {jamb: 'left'|'right', channel: [x0, x1] the channel's extent}. */
  N.sill = function (g, n, o) {
    o = o || {};
    AK.reseed(N.SEED);
    var sc = N.SC, x0 = (n - 1) * 1080;
    // void and niche back: flat, with a faint bounce rising just above the sill
    g.fillStyle = '#04070F'; g.fillRect(0, 0, N.W, N.Y_BACK);
    // the window key reaches the niche's back wall, low and to the left, column by column in gx so no seam steps
    for (var cxp = 0; cxp < N.W; cxp += 4) {
      var Kx = N.key(x0 + cxp + 2), wash = clamp((Kx - 0.3) / 1.1, 0, 1);
      var bw = g.createLinearGradient(0, N.Y_BACK - 620, 0, N.Y_BACK);
      bw.addColorStop(0, 'rgba(30,42,60,0)');
      bw.addColorStop(0.6, 'rgba(40,54,76,' + (0.55 * wash * wash) + ')');
      bw.addColorStop(1, 'rgba(70,86,110,' + (0.85 * wash * wash) + ')');
      g.fillStyle = bw; g.fillRect(cxp, N.Y_BACK - 620, 4.6, 620);
    }
    // per-pixel sill top + chamfer + face
    var Y0 = N.Y_BACK, H = N.H - Y0, Wp = N.W * sc, Hp = H * sc;
    var img = g.createImageData(Wp, Hp), d = img.data;
    var bnc = hex('#142338');
    for (var j = 0; j < Hp; j++) {
      var y = Y0 + (j + 0.5) / sc;
      for (var i = 0; i < Wp; i++) {
        var x = (i + 0.5) / sc, gx = x0 + x, K = N.key(gx), c, lit;
        if (y < N.Y_ARRIS) {                       // sill top, foreshortened
          var t = (y - N.Y_BACK) / (N.Y_ARRIS - N.Y_BACK);
          var v = t * 300, s = slate(gx, v + 4000);
          var hx = slate(gx + 1.5, v + 4000)[0] - s[0];
          var m = mullion(gx, t);
          lit = (0.34 + 0.55 * K * m) * (0.72 + 0.28 * t) * (1 + 0.9 * hx) + 0.06 * s[2];
          c = slateCol(lit * 0.95);
          var q = s[1] * (0.55 + 0.45 * K * m);
          c = [c[0] + (QZ[0] - c[0]) * q * 0.55, c[1] + (QZ[1] - c[1]) * q * 0.55, c[2] + (QZ[2] - c[2]) * q * 0.55];
          var back = smooth(0, 0.18, t);          // the back edge meets the niche in shade
          c = [c[0] * (0.45 + 0.55 * back), c[1] * (0.45 + 0.55 * back), c[2] * (0.45 + 0.55 * back)];
        } else if (y < N.Y_CHAMF) {                // arris and chamfer catch the key
          var tc = (y - N.Y_ARRIS) / (N.Y_CHAMF - N.Y_ARRIS);
          var e = AK.simplex2(gx * 0.05, 3.1);
          lit = (0.85 + 0.5 * K) * (1 - 0.55 * tc) * (0.9 + 0.1 * e);
          c = slateCol(lit);
          if (tc > 0.8) c = [c[0] * 0.55, c[1] * 0.55, c[2] * 0.6];
        } else {                                   // face
          var f = (y - N.Y_CHAMF) / (N.H - N.Y_CHAMF);
          var s2 = slate(gx, y), sx = slate(gx + 1.5, y)[0] - s2[0], sy = slate(gx, y + 1.5)[0] - s2[0];
          var lam = clamp(1 + 1.4 * (-sx * 0.62 - sy * 0.55), 0.4, 1.6);
          var fall = 1 - 0.5 * Math.pow(f, 1.3);
          lit = (0.20 + 0.28 * K) * fall * lam + 0.05 * s2[2];
          c = slateCol(lit);
          var q2 = s2[1] * (0.16 + 0.18 * K) * fall;
          c = [c[0] + (QZ[0] - c[0]) * q2 * 0.45, c[1] + (QZ[1] - c[1]) * q2 * 0.45, c[2] + (QZ[2] - c[2]) * q2 * 0.45];
          if (f < 0.03) { var u2 = f / 0.03; c = [c[0] * (0.5 + 0.5 * u2), c[1] * (0.5 + 0.5 * u2), c[2] * (0.5 + 0.5 * u2)]; }
        }
        c = [c[0] + bnc[0] * 0.06, c[1] + bnc[1] * 0.06, c[2] + bnc[2] * 0.08];
        var p = (j * Wp + i) * 4;
        d[p] = clamp(c[0], 0, 255); d[p + 1] = clamp(c[1], 0, 255); d[p + 2] = clamp(c[2], 0, 255); d[p + 3] = 255;
      }
    }
    var off = document.createElement('canvas'); off.width = Wp; off.height = Hp;
    off.getContext('2d').putImageData(img, 0, 0);
    g.drawImage(off, 0, Y0, N.W, H);
    // chips along the arris
    var rng = AK.rng(N.SEED + n);
    g.save();
    for (var k = 0; k < 0; k++) {
      var cx = rng() * N.W, w = 4 + rng() * 10;
      var cg = g.createLinearGradient(0, N.Y_ARRIS - 1, 0, N.Y_ARRIS + 5);
      cg.addColorStop(0, 'rgba(8,12,18,0.45)'); cg.addColorStop(1, 'rgba(8,12,18,0)');
      g.fillStyle = cg;
      g.beginPath(); g.moveTo(cx, N.Y_ARRIS - 0.5); g.quadraticCurveTo(cx + w * 0.5, N.Y_ARRIS + 3 + rng() * 2, cx + w, N.Y_ARRIS - 0.5); g.closePath(); g.fill();
    }
    g.restore();
    if (o.channel) N.channel(g, n, o.channel[0], o.channel[1]);
    if (o.jamb) N.jamb(g, n, o.jamb);
  };

  /* The cut channel the gold line sits in. */
  N.channel = function (g, n, xa, xb) {
    var K = N.key((n - 1) * 1080 + (xa + xb) / 2), y = N.CH_Y - 2, h = N.CH_H + 4, w = xb - xa;
    g.save();
    g.beginPath(); g.roundRect(xa, y, w, h, 3);
    var fill = g.createLinearGradient(0, y, 0, y + h);
    fill.addColorStop(0, 'rgba(8,12,18,0.90)'); fill.addColorStop(0.45, 'rgba(14,20,30,0.84)'); fill.addColorStop(1, 'rgba(24,33,44,0.78)');
    g.fillStyle = fill; g.fill();
    g.clip();
    // the inner shadow the upper lip throws into the cut
    var gi = g.createLinearGradient(0, y, 0, y + 9);
    gi.addColorStop(0, 'rgba(0,0,0,0.7)'); gi.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gi; g.fillRect(xa, y, w, 9);
    var gl = g.createLinearGradient(xa, 0, xa + 8, 0);
    gl.addColorStop(0, 'rgba(0,0,0,0.5)'); gl.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gl; g.fillRect(xa, y, 8, h);
    g.restore();
    g.save();
    g.strokeStyle = 'rgba(200,212,224,' + (0.22 + 0.25 * K) + ')'; g.lineWidth = 1.1;    // the lit lower lip
    g.beginPath(); g.moveTo(xa + 3, y + h + 0.6); g.lineTo(xb - 3, y + h + 0.6); g.stroke();
    g.strokeStyle = 'rgba(200,212,224,' + (0.10 + 0.14 * K) + ')';                       // the lit right wall
    g.beginPath(); g.moveTo(xb + 0.6, y + 3); g.lineTo(xb + 0.6, y + h - 2); g.stroke();
    g.strokeStyle = 'rgba(0,0,0,0.75)';                                                      // the shadowed upper lip
    g.beginPath(); g.moveTo(xa + 3, y - 0.6); g.lineTo(xb - 3, y - 0.6); g.stroke();
    g.restore();
  };

  /* A stone jamb: the niche's left (frame 1) or right (frame 9) side. */
  N.jamb = function (g, n, side) {
    var w = 60, xL = side === 'left' ? 0 : N.W - w;
    var img = g.createImageData(w * N.SC, N.H * N.SC), d = img.data;
    for (var j = 0; j < N.H * N.SC; j++) for (var i = 0; i < w * N.SC; i++) {
      var x = xL + (i + 0.5) / N.SC, y = (j + 0.5) / N.SC;
      var s = slate(x * 3 + 90000, y * 0.6);
      var edge = side === 'left' ? (w - (x - xL)) / w : (x - xL) / w;
      var lit = (side === 'left' ? 0.32 : 0.16) + 0.2 * s[0] - 0.1 * edge;
      var c = slateCol(lit);
      var p = (j * w * N.SC + i) * 4;
      d[p] = c[0] * 0.8; d[p + 1] = c[1] * 0.8; d[p + 2] = c[2] * 0.85; d[p + 3] = 255;
    }
    var off = document.createElement('canvas'); off.width = w * N.SC; off.height = N.H * N.SC;
    off.getContext('2d').putImageData(img, 0, 0);
    g.drawImage(off, xL, 0, w, N.H);
    g.save();
    var ex = side === 'left' ? w : N.W - w;
    g.fillStyle = side === 'left' ? 'rgba(190,200,212,0.35)' : 'rgba(0,0,0,0.6)';
    g.fillRect(ex - (side === 'left' ? 1.5 : 0), 0, 1.5, N.H);
    var sh = g.createLinearGradient(ex, 0, ex + (side === 'left' ? 40 : -40), 0);
    sh.addColorStop(0, side === 'left' ? 'rgba(0,0,0,0.5)' : 'rgba(0,0,0,0.55)'); sh.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = sh; g.fillRect(side === 'left' ? ex : ex - 40, 0, 40, N.H);
    g.restore();
  };

  /* A lit pool on the sill under an object's foot: a circle inside a transform
   * (canvas has no elliptical gradient). col '58,70,84', a peak alpha. */
  N.pool = function (g, x, y, rx, ry, a, col) {
    col = col || '120,134,150';
    g.save(); g.translate(x, y); g.scale(1, ry / rx);
    var r = g.createRadialGradient(0, 0, 0, 0, 0, rx);
    r.addColorStop(0, 'rgba(' + col + ',' + a + ')');
    r.addColorStop(0.5, 'rgba(' + col + ',' + (a * 0.55) + ')');
    r.addColorStop(1, 'rgba(' + col + ',0)');
    g.globalCompositeOperation = 'screen';
    g.fillStyle = r; g.beginPath(); g.arc(0, 0, rx, 0, Math.PI * 2); g.fill();
    g.restore();
  };

  /* Cast a silhouette layer (2x canvas, design px drawing): tinted dark slate,
   * offset (dx, dy) design px, feathered by a design-px blur, at alpha a. */
  N.cast = function (g, sil, dx, dy, blur, a, col) {
    var L = N.layer(), t = L.g;
    t.drawImage(sil, 0, 0, N.W, N.H);
    t.globalCompositeOperation = 'source-in';
    t.fillStyle = col || '#020409'; t.fillRect(0, 0, N.W, N.H);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
    g.filter = 'blur(' + (blur * N.SC) + 'px)';
    g.globalAlpha = a;
    g.drawImage(L.c, dx * N.SC, dy * N.SC);
    g.restore();
  };

  /* Base CSS for the deck's DOM type. */
  N.css = function () {
    var s = document.createElement('style');
    s.textContent = [
      'html,body{margin:0;width:1080px;height:1350px;overflow:hidden;background:#04070F}',
      'body{position:relative}',
      '.t{position:absolute;z-index:5}',
      '.kick{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:24px;letter-spacing:0.10em;color:#8E9BA8;text-transform:uppercase;line-height:1.2}',
      '.disp{font-family:"Instrument Serif",serif;font-weight:400;color:#EFE6D4;letter-spacing:-0.02em;line-height:0.98;margin:0}',
      '.body{font-family:"Bricolage Grotesque",sans-serif;font-variation-settings:"opsz" 36,"wdth" 90;font-weight:430;font-size:34px;line-height:1.38;color:#C3CAD3;margin:0}',
      '.inc{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:24px;letter-spacing:0.08em;color:#A9B3BD;text-transform:uppercase;text-shadow:0 1.2px 0 rgba(255,240,220,0.30),0 -1.2px 0 rgba(0,0,0,0.85),0 0 6px rgba(0,0,0,0.5);white-space:nowrap}',
      '.motif{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:30px;letter-spacing:0;color:#FFC72C;line-height:32px;height:32px;white-space:nowrap}',
      '.fx{position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;white-space:nowrap}'
    ].join('\n');
    document.head.appendChild(s);
  };

  function el(tag, cls, text, style) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (style) e.setAttribute('style', style);
    return e;
  }
  N.el = el;

  /* Fixtures: wordmark, counter, site line, coordinates. */
  N.fixtures = function (n, o) {
    o = o || {};
    var b = document.body;
    var wm = el('div', 'fx', 'ALASKA.AI', 'left:96px;top:80px;font-family:"Instrument Serif",serif;font-size:30px;letter-spacing:0.04em;color:#D9D2C2');
    var ct = el('div', 'fx', (n < 10 ? '0' : '') + n + ' / 09', 'right:96px;top:84px;font-size:24px;letter-spacing:0.08em;color:#8E9BA8');
    var site = el('div', 'fx', 'alaskaaihq.com', 'left:96px;top:1288px;font-size:19px;letter-spacing:0.06em;color:#46545F');
    site.setAttribute('data-decorative', '');
    var co = el('div', 'fx', N.COORDS, 'right:96px;top:1289px;font-size:18px;letter-spacing:0.06em;color:#46545F');
    co.setAttribute('data-decorative', '');
    [wm, ct, site, co].forEach(function (e) { b.appendChild(e); });
    if (o.noWordmark) wm.remove();
  };

  /* The gold motif in its channel, with an optional incised label above it. */
  N.motif = function (text, x, o) {
    o = o || {};
    var m = el('div', 't motif', text, 'left:' + x + 'px;top:' + N.CH_Y + 'px');
    document.body.appendChild(m);
    if (o.label) {
      var lb = el('div', 't inc', o.label, 'left:' + (o.lx != null ? o.lx : x) + 'px;top:' + (o.ly != null ? o.ly : N.CH_Y - 40) + 'px');
      document.body.appendChild(lb);
    }
    return m;
  };

  N.incised = function (text, x, y, o) {
    o = o || {};
    var e = el('div', 't inc', text, 'left:' + x + 'px;top:' + y + 'px' + (o.size ? ';font-size:' + o.size + 'px' : '') + (o.style ? ';' + o.style : ''));
    document.body.appendChild(e);
    return e;
  };

  global.AKNICHE = N;
})(typeof window !== 'undefined' ? window : this);
