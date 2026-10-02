/* akfield.js — the chassis for No.76, THE SUNDIAL FIELD (2026-10-03).
 *
 * Six timber posts with the proportions of a straight double-quote stroke stand
 * in three pairs on a frozen Interior plain. One sun, solved for Fairbanks on
 * election day, lights each frame at that frame's hour, so the casts sweep
 * across the deck toward polls closing. Every frame prints the same field in a
 * DIFFERENT hand (PBR, engraving, hachure, stipple, carved snow, relief wash,
 * halftone, crosshatch, glow), so this file is HOUSE FURNITURE ONLY: the sun,
 * the camera, the word-drift height field, the post outline, the 2x offscreen
 * and its reserve punch, and the fixtures. No slide calls a draw-the-whole-slide
 * function from here; each frame's mark-making lives in its own file.
 *
 * COORDINATES. Camera-local ground metres: u to the camera's right, d forward,
 * y up. Headings and azimuths are degrees clockwise from true north. A sun at
 * azimuth `az` seen from a camera heading `hd` sits at relative angle
 * rel = az - hd (clockwise from straight ahead); its casts point rel + 180.
 */
(function (global) {
  "use strict";
  var F = {};

  /* ---- the sun ----------------------------------------------------------
   * Low-precision NOAA/Meeus solar position, good to a few hundredths of a
   * degree for this purpose. Fairbanks 64.84 N, 147.72 W; AKDT is UTC-8. */
  F.LAT = 64.84; F.LON = -147.72;
  F.sunAt = function (localHour) {
    var ms = Date.UTC(2026, 9, 6, 0, 0, 0) + (localHour + 8) * 3600e3;
    var n = (ms - Date.UTC(2000, 0, 1, 12, 0, 0)) / 86400e3;
    var rad = Math.PI / 180;
    var L = (280.460 + 0.9856474 * n) % 360, g = ((357.528 + 0.9856003 * n) % 360) * rad;
    var lam = (L + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * rad;
    var eps = (23.439 - 0.0000004 * n) * rad;
    var ra = Math.atan2(Math.cos(eps) * Math.sin(lam), Math.cos(lam));
    var dec = Math.asin(Math.sin(eps) * Math.sin(lam));
    var gmst = (18.697374558 + 24.06570982441908 * n) % 24;
    var ha = (((gmst * 15 + F.LON) % 360) + 360) % 360 * rad - ra;
    var la = F.LAT * rad;
    var el = Math.asin(Math.sin(la) * Math.sin(dec) + Math.cos(la) * Math.cos(dec) * Math.cos(ha));
    var az = Math.atan2(-Math.sin(ha), Math.tan(dec) * Math.cos(la) - Math.sin(la) * Math.cos(ha));
    return { el: el / rad, az: ((az / rad) % 360 + 360) % 360, hour: localHour };
  };
  /* The frame hours, fixed in the storyboard's motif table. */
  F.HOURS = { 1: 9.5, 2: 10.5, 3: 11.5, 4: 12.5, 5: 13.633, 6: 15, 7: 17, 8: 18.5, 9: 20 };
  F.POLLS = [7, 20];

  /* Sun vector in camera-local axes [u, y, d] for a camera heading hd. */
  F.sunLocal = function (sun, hd) {
    var r = Math.PI / 180, rel = (sun.az - hd) * r, el = sun.el * r;
    return [Math.cos(el) * Math.sin(rel), Math.sin(el), Math.cos(el) * Math.cos(rel)];
  };
  /* Ground cast offset (du, dd) in metres for a point at height h. */
  F.castOffset = function (sun, hd, h) {
    var s = F.sunLocal(sun, hd);
    var k = h / Math.max(Math.tan(Math.max(sun.el, 0.4) * Math.PI / 180), 1e-3);
    var hl = Math.hypot(s[0], s[2]) || 1;
    return [-s[0] / hl * k, -s[2] / hl * k];
  };

  /* ---- the camera -------------------------------------------------------
   * Pinhole. pos height camH (m), pitch in degrees (negative looks down, which
   * RAISES the horizon in the frame),
   * vertical field of view vfov, frame W x H, principal point at the centre. */
  F.camera = function (o) {
    var W = o.W || 1080, H = o.H || 1350;
    var f = (H / 2) / Math.tan((o.vfov || 50) * Math.PI / 360);
    var p = (o.pitch || 0) * Math.PI / 180, cp = Math.cos(p), sp = Math.sin(p);
    var camH = o.camH == null ? 1.7 : o.camH, cx = W / 2, cy = H / 2;
    return {
      f: f, W: W, H: H, camH: camH, pitch: o.pitch || 0, heading: o.heading || 0,
      horizonY: cy + Math.tan(p) * f,     /* pitch DOWN (negative) raises the horizon */
      project: function (u, y, d) {
        var Y = y - camH;
        var zc = d * cp + Y * sp;          /* depth along the optical axis */
        var yc = -d * sp + Y * cp;
        if (zc <= 0.05) return null;
        return [cx + f * u / zc, cy - f * yc / zc, zc];
      }
    };
  };

  /* ---- the six answers, as words -----------------------------------------
   * The quotes the deck prints, verbatim from claims.json. Drift counts are a
   * property of the DRAWING and are tagged [design] wherever they are named. */
  F.QUOTES = {
    ramirez:  "I can't really say 'yay' or 'nay' because I think there need to be more studies done",
    howell:   "I would hate to see us dump a data center on top of that",
    lajiness: "I don't think that data centers are good for any community, to be honest with you",
    shupe:    "I'm somewhere in between the 'I'm worried about what it might bring' and 'I don't want to discount it' groups",
    crass:    "thinking about a project that would consume more energy than our entire town is absolutely terrifying at first blush",
    leaders:  "We need to take a serious look at the impact on the infrastructure, the power grid, the water and how that's affected"
  };
  F.BALLOT = ["ramirez", "howell", "lajiness", "shupe", "crass", "leaders"];
  F.words = function (key) {
    return F.QUOTES[key].replace(/[^A-Za-z' ]/g, " ").split(/\s+/).filter(Boolean)
      .map(function (w) { return w.replace(/^'+|'+$/g, ""); }).filter(Boolean);
  };

  /* Seeded mulberry32, so the module carries no dependency on noise.js. */
  F.rng = function (seed) {
    var a = seed >>> 0;
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  };

  /* One barchan per word, far to near in word order, size by letter count.
   * region: {u0, u1, d0, d1} in camera-local metres. windDeg is the direction
   * the wind blows TOWARD, relative to the camera heading. */
  F.drifts = function (keys, region, opts) {
    opts = opts || {};
    var R = F.rng(opts.seed || 20261003), out = [];
    var wind = (opts.windDeg == null ? 250 : opts.windDeg) * Math.PI / 180;
    var per = keys.length;
    keys.forEach(function (k, ki) {
      var ws = F.words(k), n = ws.length;
      var u0 = region.u0 + (region.u1 - region.u0) * ki / per;
      var u1 = region.u0 + (region.u1 - region.u0) * (ki + 1) / per;
      ws.forEach(function (w, i) {
        var t = (i + 0.5) / n;                         /* 0 far, 1 near */
        var d = region.d1 + (region.d0 - region.d1) * t;
        var u = u0 + (u1 - u0) * (0.15 + 0.7 * R());
        var L = Math.min(14, Math.max(2, w.length));
        var r = (0.6 + (L - 2) / 12 * 1.6) * (opts.scale || 1);
        var hgt = (0.04 + (L - 2) / 12 * 0.14) * (opts.hScale || 1);
        out.push({ key: k, word: w, u: u, d: d + (R() - 0.5) * 0.6, r: r, h: hgt,
                   wind: wind + (R() - 0.5) * 0.35 });
      });
    });
    return out;
  };
  /* Height of the drift field at (u, d): crescent barchans, slip face downwind. */
  F.height = function (dr, u, d) {
    var z = 0;
    for (var i = 0; i < dr.length; i++) {
      var q = dr[i], du = u - q.u, dd = d - q.d;
      if (du > 3.2 * q.r || du < -3.2 * q.r || dd > 3.2 * q.r || dd < -3.2 * q.r) continue;
      var cw = Math.cos(q.wind), sw = Math.sin(q.wind);
      var x = du * sw + dd * cw;             /* along the wind */
      var y = du * cw - dd * sw;             /* across it */
      var body = Math.exp(-((x / (1.0 * q.r)) * (x / (1.0 * q.r)) + (y / (1.35 * q.r)) * (y / (1.35 * q.r))));
      var bite = Math.exp(-(((x - 0.55 * q.r) / (0.62 * q.r)) * ((x - 0.55 * q.r) / (0.62 * q.r)) +
                            (y / (0.7 * q.r)) * (y / (0.7 * q.r))));
      var v = body - 0.55 * bite;
      if (v > 0) z += q.h * v;
    }
    return z;
  };

  /* ---- the post ---------------------------------------------------------
   * A straight double-quote stroke as a tapered timber prism: 0.45 m across
   * the top, 0.30 m at the foot, 0.18 m deep, 2.2 m tall. A PAIR stands 0.14 m
   * apart and reads as one quotation mark. */
  F.POST = { top: 0.45, base: 0.30, depth: 0.18, h: 2.2, pairGap: 0.14 };
  /* The eight corners of a post standing at (u, d), facing the camera, yawed
   * by yawDeg about its own axis. */
  F.postCorners = function (u, d, yawDeg) {
    var P = F.POST, a = (yawDeg || 0) * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
    function c(x, y, z) { return [u + x * ca + z * sa, y, d - x * sa + z * ca]; }
    var bt = P.base / 2, tp = P.top / 2, dz = P.depth / 2;
    return [c(-bt, 0, -dz), c(bt, 0, -dz), c(bt, 0, dz), c(-bt, 0, dz),
            c(-tp, P.h, -dz), c(tp, P.h, -dz), c(tp, P.h, dz), c(-tp, P.h, dz)];
  };

  /* ---- 2x offscreen and the reserve punch -------------------------------
   * The slide canvas is 2160 x 2700 with scale(2,2). An offscreen built here
   * is the SAME 2x backing with the same transform, so a field drawn on it
   * composites without resampling. */
  F.offscreen = function (W, H, fn) {
    var c = document.createElement("canvas");
    c.width = W * 2; c.height = H * 2;
    var g = c.getContext("2d"); g.scale(2, 2);
    fn(g, c);
    return c;
  };
  /* Measured per-line boxes of every [data-reserve] node, design px. */
  F.reserveBoxes = function (selector, pad) {
    pad = pad == null ? 12 : pad;
    var out = [];
    document.querySelectorAll(selector || "[data-reserve]").forEach(function (el) {
      var rects = null;
      try { var rg = document.createRange(); rg.selectNodeContents(el); rects = rg.getClientRects(); }
      catch (e) { rects = null; }
      var p = el.getAttribute("data-reserve") === "mono" ? Math.round(pad * 0.7) : pad;
      if (!rects || !rects.length) { var r = el.getBoundingClientRect(); rects = [r]; }
      for (var i = 0; i < rects.length; i++) {
        var b = rects[i];
        if (b.width > 0 && b.height > 0) out.push([b.left - p, b.top - p, b.width + 2 * p, b.height + 2 * p]);
      }
    });
    return out;
  };
  /* Punch blurred RECTANGLES out of an offscreen (destination-out, order
   * independent, one blur per box, never a radial). `g` carries scale(2,2). */
  F.punch = function (g, boxes, blur, strength) {
    g.save();
    g.globalCompositeOperation = "destination-out";
    g.filter = "blur(" + (blur == null ? 8 : blur) + "px)";
    g.fillStyle = "rgba(0,0,0," + (strength == null ? 1 : strength) + ")";
    boxes.forEach(function (b) { g.fillRect(b[0], b[1], b[2], b[3]); });
    g.restore();
  };

  /* ---- fixtures -----------------------------------------------------------
   * The sun clock: horizon, the day's elevation curve between the poll hours,
   * and this frame's sun, a gold disc above the horizon or a gold ring below.
   * SVG, so its gold is exact and the ink census reads it. */
  F.sunClock = function (svg, slideNo) {
    var NS = "http://www.w3.org/2000/svg", W = 84, H = 44, base = 30;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("width", W); svg.setAttribute("height", H);
    function x(h) { return 6 + (h - F.POLLS[0]) / (F.POLLS[1] - F.POLLS[0]) * (W - 12); }
    function y(el) { return base - el * 1.05; }
    var pts = [];
    for (var h = F.POLLS[0]; h <= F.POLLS[1] + 1e-6; h += 0.25) {
      var s = F.sunAt(h); pts.push(x(h).toFixed(1) + "," + y(s.el).toFixed(1));
    }
    function el(tag, attrs) {
      var e = document.createElementNS(NS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      svg.appendChild(e); return e;
    }
    el("line", { x1: 2, y1: base, x2: W - 2, y2: base, stroke: "#5F7385", "stroke-width": 1 });
    el("polyline", { points: pts.join(" "), fill: "none", stroke: "#5F7385",
                     "stroke-width": 1, "stroke-dasharray": "1.5 2.5" });
    var s0 = F.sunAt(F.HOURS[slideNo]), sx = x(s0.hour), sy = y(s0.el);
    if (s0.el > 0) el("circle", { cx: sx, cy: sy, r: 5.5, fill: "#FFC72C" });
    else el("circle", { cx: sx, cy: sy, r: 5, fill: "none", stroke: "#FFC72C", "stroke-width": 2.2 });
    return s0;
  };

  global.AKFIELD = F;
})(window);
