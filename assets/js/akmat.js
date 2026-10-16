/* akmat.js — THE CUTTING MAT, Carousel No.87's chassis (2026-10-15).
 *
 * DECK FURNITURE, kept in a module so bespoke_check strips `<script src=>` as harness, exactly like akstack.js
 * and aksheet.js. Every slide's own composition still has to earn its similarity score; this file supplies only
 * the physics of one world so ten frames share ONE sun, ONE mat and ONE ruler.
 *
 * THE WORLD. One long self-healing cutting mat seen straight down (orthographic, so every length is honest),
 * under a row of south windows. A low October sun at azimuth 300 (upper left, akbench convention: 0 toward the
 * top of the frame, clockwise) and elevation 20 lays skewed panes of warm key light across the mat; outside the
 * panes only the cool sky reaches it. Type sits on the unlit mat, so the reserve is the room's own shade.
 *
 * THE LAW. Every frame is exactly 100 MW wide: 10.8 CSS px per MW, never changed. A museum-board ruler runs
 * along the lower third of every frame as ONE object, a pure function of the global x (frame * 1080 + x), so the
 * seams chain exactly and ten frames are one gigawatt.
 *
 * MATERIAL IDS (shared so every frame reads the same world):
 *   0 mat, 1 ruler board, 2 museum board, 3 gold leaf, 4 cut floor (a slot through to the base), 5 vellum,
 *   6 board edge core (the cut face of a board, lighter), 7 ink (printed lines on board)
 *
 * DETERMINISM. Every caller passes its own seed. Hash noise only, no Math.random.
 * Load AFTER noise.js and akbench.js.
 */
(function (global) {
  "use strict";
  var M = {};
  M.PXMW = 10.8;                                  // CSS px per MW, the deck's one scale
  M.FRAME_MW = 100;
  M.LIGHT = { azDeg: 300, elDeg: 20 };            // upper left, raking
  M.KEY = [1.06, 0.90, 0.70];                     // warm low sun
  M.AMB = [0.42, 0.58, 0.74];                     // cool north sky
  M.RULER = { top: 1166, bottom: 1234, h: 6, band: [1168, 1190] };
  M.SHEAR = 1.732;                                // pane sides run down the light: at az 300 a ray moves 1.732 px in x per px of y, the same direction every cast takes

  function lin(hex) {
    hex = hex.replace("#", "");
    var r = parseInt(hex.substr(0, 2), 16) / 255, g = parseInt(hex.substr(2, 2), 16) / 255, b = parseInt(hex.substr(4, 2), 16) / 255;
    return [Math.pow(r, 2.2), Math.pow(g, 2.2), Math.pow(b, 2.2)];
  }
  M.lin = lin;
  function hash(x, y, s) {
    var h = (x * 374761393 + y * 668265263 + (s | 0) * 2147483647) | 0;
    h = (h ^ (h >>> 13)) * 1274126177 | 0;
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }
  M.hash = hash;
  function vnoise(x, y, s) {                       // smooth value noise, unit cells
    var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    var u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    var a = hash(xi, yi, s), b = hash(xi + 1, yi, s), c = hash(xi, yi + 1, s), d = hash(xi + 1, yi + 1, s);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  M.vnoise = vnoise;
  function smooth(e0, e1, x) { var t = Math.max(0, Math.min(1, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t); }
  M.smooth = smooth;

  /* ---- the sun panes. A pane is {x0, x1, y0, y1, mull: [u...]} in sheared space u = X - (Y - y0) * SHEAR,
   * so its long edges run down the light. Soft edges carry the penumbra of a window 3 m off; mullions throw
   * thin shadows along the same direction. Returns the key fraction 0..1. */
  M.pane = function (X, Y, panes) {
    var best = 0;
    for (var p = 0; p < panes.length; p++) {
      var P = panes[p], pen = P.pen || 9;
      var u = X - (Y - P.y0) * M.SHEAR;
      var a = smooth(P.x0 - pen, P.x0 + pen, u) * (1 - smooth(P.x1 - pen, P.x1 + pen, u));
      a *= smooth(P.y0 - pen, P.y0 + pen, Y) * (1 - smooth(P.y1 - pen, P.y1 + pen, Y));
      if (P.mull) for (var q = 0; q < P.mull.length; q++) {
        var dm = Math.abs(u - P.mull[q]);
        a *= smooth(4, 12, dm) * 0.92 + 0.08;
      }
      if (P.rail) for (var r = 0; r < P.rail.length; r++) {
        var dr = Math.abs(Y - P.rail[r]);
        a *= smooth(3, 10, dr) * 0.92 + 0.08;
      }
      a *= (P.k == null ? 1 : P.k);
      if (a > best) best = a;
    }
    return best;
  };

  /* ---- the mat. A dark blue-green self-healing mat: a printed grid every 10 MW (108 px) in both axes, a
   * fainter 5 MW grid, a fine rubber tooth, and healed knife scores (thin straight cuts that closed, slightly
   * glossier than the field). gx is the GLOBAL x so the grid chains across frames. */
  var MAT = lin("#6C9DA8"), GRID = lin("#A9C7CE"), SCORE = lin("#7FA7B0");
  M.matAlbedo = function (X, Y, frame, scores) {
    var gx = frame * 1080 + X;
    var t = vnoise(gx * 0.9, Y * 0.9, 11) * 0.5 + vnoise(gx * 0.23, Y * 0.23, 12) * 0.5;
    var big = vnoise(gx / 260, Y / 260, 13);
    var k = 0.86 + 0.10 * t + 0.10 * big;
    var c = [MAT[0] * k, MAT[1] * k, MAT[2] * k];
    var mx = gx % 108, my = Y % 108; if (mx < 0) mx += 108;
    var lineA = 0;
    var dx = Math.min(mx, 108 - mx), dy = Math.min(my, 108 - my);
    if (dx < 1.1) lineA = 0.55; else if (dy < 1.1) lineA = 0.55;
    var hx = Math.abs(mx - 54), hy = Math.abs(my - 54);
    if (!lineA && (hx < 0.6 || hy < 0.6)) lineA = 0.22;
    if (lineA) { c[0] += (GRID[0] - c[0]) * lineA * 0.5; c[1] += (GRID[1] - c[1]) * lineA * 0.5; c[2] += (GRID[2] - c[2]) * lineA * 0.5; }
    if (scores) for (var s = 0; s < scores.length; s++) {
      var S = scores[s], vx = S[2] - S[0], vy = S[3] - S[1], L2 = vx * vx + vy * vy;
      var tt = ((X - S[0]) * vx + (Y - S[1]) * vy) / L2;
      if (tt < 0 || tt > 1) continue;
      var px = S[0] + vx * tt - X, py = S[1] + vy * tt - Y, dd = Math.sqrt(px * px + py * py);
      if (dd < 1.4) { var w = (1 - dd / 1.4) * 0.6 * Math.sin(Math.PI * tt); c[0] += (SCORE[0] - c[0]) * w; c[1] += (SCORE[1] - c[1]) * w; c[2] += (SCORE[2] - c[2]) * w; }
    }
    return c;
  };

  /* ---- museum board. Off-white four-ply with a fibre tooth; `tint` lets a frame cool or warm one board. */
  var BOARD = lin("#E3E9EA");
  M.boardAlbedo = function (X, Y, seed, tint) {
    var f = vnoise(X * 1.3, Y * 0.35, seed) * 0.6 + vnoise(X * 0.31, Y * 0.31, seed + 1) * 0.4;
    var k = 0.90 + 0.10 * f, b = tint || BOARD;
    return [b[0] * k, b[1] * k, b[2] * k];
  };
  /* ---- gold leaf. Squares of leaf about 54 px, each a slightly different gold, with darker overlapping
   * seams where two leaves meet and a few skips where the bole shows through. */
  var GOLD = lin("#F2B53A"), BOLE = lin("#7A3E1A");
  M.goldAlbedo = function (X, Y, seed) {
    var cs = 54, ix = Math.floor(X / cs + 0.31 * Math.floor(Y / cs)), iy = Math.floor(Y / cs);
    var fx = X / cs + 0.31 * Math.floor(Y / cs) - ix, fy = Y / cs - iy;
    var v = 0.88 + 0.16 * hash(ix, iy, seed);
    var e = Math.min(fx, 1 - fx, fy, 1 - fy) * cs;
    var seam = e < 1.2 ? 0.86 + 0.14 * (e / 1.2) : 1;
    var c = [GOLD[0] * v * seam, GOLD[1] * v * seam * 0.96, GOLD[2] * v * seam * 0.8];
    var skip = vnoise(X / 9, Y / 9, seed + 7);
    if (skip > 0.93) { var w = (skip - 0.93) / 0.07; c = [c[0] + (BOLE[0] - c[0]) * w, c[1] + (BOLE[1] - c[1]) * w, c[2] + (BOLE[2] - c[2]) * w]; }
    return c;
  };

  /* ---- gold leaf is never flat: each leaf is a slightly domed, crinkled skin, which is what throws glints. */
  M.leafCrinkle = function (X, Y, seed) {
    var cs = 54, fx = X / cs + 0.31 * Math.floor(Y / cs), fy = Y / cs;
    var u = fx - Math.floor(fx), v = fy - Math.floor(fy);
    return 0.55 * Math.sin(Math.PI * u) * Math.sin(Math.PI * v) + 0.35 * (vnoise(X / 6, Y / 6, seed) - 0.5) + 0.25 * (vnoise(X / 17, Y / 17, seed + 3) - 0.5);
  };

  /* ---- a board lying on the mat: a rounded rectangle with a bevelled cut edge. Returns height in CSS px
   * (0 outside) and, through `out`, whether the pixel is on the bevel (the cut face reads lighter). */
  M.box = function (X, Y, b, out) {
    var r = b.r == null ? 2 : b.r, bev = b.bev == null ? 1.6 : b.bev;
    var cx = (b.x0 + b.x1) / 2, cy = (b.y0 + b.y1) / 2, hw = (b.x1 - b.x0) / 2 - r, hh = (b.y1 - b.y0) / 2 - r;
    var qx = Math.abs(X - cx) - hw, qy = Math.abs(Y - cy) - hh;
    var d = Math.min(Math.max(qx, qy), 0) + Math.hypot(Math.max(qx, 0), Math.max(qy, 0)) - r;
    if (d > 0) return 0;
    var inside = -d;
    if (out) out.bevel = inside < bev;
    return b.h * Math.min(1, 0.35 + 0.65 * smooth(0, bev, inside));
  };

  /* ---- the ruler. A strip of museum board the full width of every frame, 6 px thick with bevelled long
   * edges, scored with a V groove at every 5 MW of the GLOBAL axis and a deeper one at every 10 MW. Returns
   * {h, m} for a pixel on it, or null. The numerals are DOM text below the groove band, never canvas. */
  M.TAB = { x0: -8, x1: 116, y0: 1230, y1: 1266 };
  M.ruler = function (X, Y, frame) {
    var R = M.RULER, T = M.TAB;
    if (Y > R.bottom - 4 && Y <= T.y1 && X >= T.x0 && X <= T.x1) {
      var te = Math.min(X - T.x0, T.x1 - X, T.y1 - Y); return { h: R.h * Math.min(1, 0.4 + 0.6 * smooth(0, 1.8, te)), m: 1 };
    }
    if (Y < R.top || Y > R.bottom) return null;
    var e = Math.min(Y - R.top, R.bottom - Y), h = R.h * Math.min(1, 0.4 + 0.6 * smooth(0, 1.8, e));
    var gmw = (frame * 1080 + X) / M.PXMW, f = gmw - Math.round(gmw / 5) * 5, dpx = Math.abs(f) * M.PXMW;
    var major = Math.round(gmw / 5) % 2 === 0;
    var len = major ? 22 : 14;
    if (Y - R.top < len + 2) {
      var hw = major ? 1.3 : 0.9, depth = major ? 2.6 : 1.6;
      if (dpx < hw + 0.8) h -= depth * Math.max(0, 1 - dpx / (hw + 0.8)) * smooth(len + 2, len - 2, Y - R.top);
    }
    return { h: h, m: 1 };
  };
  /* the ruler's marks for a frame, as the data-scale `marks` list wants them, in CSS px */
  M.rulerMarks = function (frame) {
    var out = [];
    for (var mw = 0; mw <= 100; mw += 5) {
      var x = mw * M.PXMW; if (x > 1079.5) continue;
      out.push({ at: +x.toFixed(1), means: (frame * 100 + mw) + " MW on the one deck scale" });
    }
    return out;
  };


  /* ---- gold leaf catches the window: a soft band of reflected sky across the leaf, perpendicular to the
   * sun, so a flat leafed face is never one value. `c` places the band (in px along the band axis). */
  M.goldSheen = function (X, Y, c, w) {
    var a = X * 0.5 + Y * 0.866, d = (a - c) / (w || 150);
    return 0.62 + 0.95 * Math.exp(-d * d);
  };

  /* ================= THE PLUMBING (harness, not art) =================
   * ready(fn): fonts, the load event, one yield (a long synchronous draw must start after it, SKILL.md),
   * then fn(); resolves renderReady when fn's promise settles. */
  M.ready = function (fn) {
    window.renderReady = new Promise(function (resolve, reject) {
      (async function () {
        await document.fonts.ready;
        await new Promise(function (r) { if (document.readyState === "complete") r(); else window.addEventListener("load", r); });
        await new Promise(function (r) { setTimeout(r, 0); });
        await fn();
        resolve();
      })().catch(function (e) { console.error(e); reject(e); });
    });
  };
  /* the ruler's local numerals and the running-total tab, as DOM text (vector in the PDF) */
  M.numerals = function (frame, host) {
    host = host || document.body;
    for (var mw = 0; mw < 100; mw += 10) {
      var d = document.createElement("div");
      d.className = "akm-num"; d.setAttribute("data-decorative", "");
      d.style.cssText = "position:absolute;top:1198px;font-family:'JetBrains Mono',monospace;font-weight:500;font-size:24px;color:#22303A;transform:translateX(-50%);left:" + (mw * M.PXMW + (mw === 0 ? 14 : 0)) + "px";
      d.textContent = String(mw); host.appendChild(d);
    }
    var t = document.createElement("div");
    t.className = "akm-tab"; t.setAttribute("data-decorative", "");
    t.style.cssText = "position:absolute;left:0;top:1236px;width:112px;height:30px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:20px;letter-spacing:.06em;color:#1E2A2E;text-align:center;line-height:30px";
    t.textContent = (frame * 100).toLocaleString("en-US") + " MW"; host.appendChild(t);
  };
  /* the deck's one relief call: the same sun, the same sky, the key gated by the frame's panes */
  M.relief = function (cx, o) {
    return AKBENCH.relief(cx, { x: 0, y: 0, w: 1080, h: 1350, scale: 2,
      height: o.height, material: o.material, albedo: o.albedo, spec: o.spec, light: M.LIGHT,
      keyMask: function (X, Y) { return M.pane(X, Y, o.panes); }, keyColor: M.KEY, ambColor: M.AMB,
      ambient: o.ambient == null ? 0.17 : o.ambient, diffuse: o.diffuse == null ? 3.1 : o.diffuse,
      ao: o.ao == null ? 0.8 : o.ao, shadow: o.shadow == null ? 0.9 : o.shadow,
      softness: o.softness == null ? 16 : o.softness, castLength: o.castLength == null ? 160 : o.castLength });
  };
  /* the deck grade, once, after all canvas drawing; then the grain tile on the DOM overlay */
  M.finish = function (cx, seed, o) {
    o = o || {};
    AKPOST.grade(cx, { w: 1080, h: 1350, exposure: o.exposure || 0, saturation: 1.02, contrast: 1.04, filmic: true,
      lift: [0.004, 0.008, 0.012], gain: [1.01, 1.0, 0.98], vignette: 0.12,
      bloom: { threshold: 0.86, strength: 0.18, radius: 10 }, grain: { amount: 0.03, size: 2, seed: seed },
      dither: true, sharpen: 0.2 });
    var g = document.getElementById("grain"); if (g) AK.grainOn(g, { size: 280, strength: 0.06, seed: seed * 10 + 1 });
  };

  global.AKMAT = M;
})(typeof window !== "undefined" ? window : globalThis);
