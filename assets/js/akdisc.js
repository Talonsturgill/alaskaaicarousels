/* akdisc.js — THE SEASON DISC, Carousel No. 63's continuity chassis.
 *
 * Committed 2026-09-19. DECK FURNITURE, shared across all nine slides on purpose,
 * which is why it is a module rather than inline code: `bespoke_check` strips
 * `<script src=>` as harness, so one shared coordinate system and one shared
 * material vocabulary cost the variety budget nothing, while each slide's own
 * composition still has to earn its score. Same reasoning as akrail.js,
 * akcolumn.js, akseam.js, aknight.js, aksheet.js and akunderice.js.
 *
 * WHAT THIS IS. One parallel-oblique projection of a machined disc, plus the
 * material populations the deck reuses (wet gravel, wind chop, the contact
 * triple). The disc carries QUANTITIES, so the projection is parallel and never
 * perspective, per the 3D data honesty mandate in DESIGN_DOCTRINE section 4.
 *
 * THE ONE RULE THIS FILE EXISTS TO ENFORCE. Both records in this deck, the
 * model's and the observers', are drawn in ONE ink at ONE value and are told
 * apart by LINE VOICE alone. `ruled()` sets the model's voice, constant width,
 * butt caps, miter joins. `swelled()` sets the observation's, width per stroke
 * from the light. Colour-coding them into two teams would contradict claim C15
 * on the same frame it is printed on, which is why neither function takes a
 * colour argument at all.
 *
 * NO TEXT IS EVER DRAWN HERE. Canvas text rasterises in the PDF and is invisible
 * to half the collision gates. Type is DOM or SVG, always, on every slide.
 */
(function (global) {
  "use strict";

  /* ---- palette. NILAS, BLACK WATER AND MILLED ICE ---- */
  var PAL = {
    deep:      "#04080F",
    base:      "#0A1622",
    mid:       "#12263A",
    iceLit:    "#CFE3EE",
    iceShadow: "#46687E",
    shadow:    "#24384A",
    paper:     "#E6E0D4",
    paperInk:  "#1B2A33",
    record:    "#9FB6C4",   /* BOTH records. One ink. Never two. */
    datum:     "#6EA5FF",
    warm:      "#B4694A",
    snow:      "#F4F8FF",
    gold:      "#FFC72C",
    goldHalo:  "#FFDA6E",
    wetChip:   "#58697A"
  };

  /* per-slide mid-tone, the palette arc. Warms into the 2019 heatwave, cools out. */
  var ARC = ["#12263A", "#14283C", "#17293A", "#1E2B36", "#2A2C31",
             "#33292A", "#16283C", "#101F30", "#0A1826"];

  /* ---- deterministic randomness. Normal, never uniform, never Math.random ---- */
  function mk(seed) {
    var r = AK.rng(seed >>> 0);
    var spare = null;
    return {
      u: r,
      range: function (a, b) { return a + (b - a) * r(); },
      int: function (a, b) { return Math.floor(a + (b - a + 1) * r()); },
      /* Box-Muller. Populations that look placed rather than sprayed. */
      norm: function (mu, sd) {
        if (spare !== null) { var s = spare; spare = null; return mu + sd * s; }
        var u1 = Math.max(r(), 1e-9), u2 = r();
        var m = Math.sqrt(-2 * Math.log(u1));
        spare = m * Math.sin(2 * Math.PI * u2);
        return mu + sd * m * Math.cos(2 * Math.PI * u2);
      },
      pick: function (a) { return a[Math.floor(r() * a.length)]; }
    };
  }

  /* ---- the disc. Parallel oblique, 32 degrees above its own plane ----
   * P(r, theta, z) -> [x, y].  0.53 is sin(32deg). Every groove, tick, leader
   * endpoint and fracture vertex comes through this one function, so nothing in
   * the deck is eyeballed and slide 07 is demonstrably the SAME object as 01.
   */
  var DISC = { cx: 648, cy: 880, squash: 0.44, lift: 0.85 };

  function P(r, theta, z) {
    return [DISC.cx + r * Math.cos(theta),
            DISC.cy + r * Math.sin(theta) * DISC.squash - (z || 0) * DISC.lift];
  }

  /* angle of a month boundary. Origin at twelve o'clock on September, clockwise,
   * per the paper's own September to August calendar (claim C20). */
  function monthAngle(i) { return -Math.PI / 2 + (i / 12) * Math.PI * 2; }

  /* radius of a hindcast year groove. 1993 innermost, 2023 outermost (claim C10).
   * The COUNT of grooves is a property of the drawing and is tagged [design] in
   * the dossier; the deck never prints a year count, because the figure lives
   * only in C10's notes and a note is reasoning rather than verification. */
  var YEAR0 = 1993, YEAR1 = 2023, RIN = 168, ROUT = 392;
  function yearRadius(y) {
    return RIN + (ROUT - RIN) * (y - YEAR0) / (YEAR1 - YEAR0);
  }

  /* Screen-space key direction. The scene key is azimuth 168, elevation 22;
   * projected into the picture plane it rakes from the upper right, and every
   * slide uses THIS constant so the deck has one light rather than nine. */
  var KEY = -0.55;

  /* ---- the two line voices ---- */
  function ruled(cx, w) {            /* THE MODEL. machined, constant, butt caps */
    cx.lineCap = "butt";
    cx.lineJoin = "miter";
    cx.lineWidth = w;
  }
  function swelled(cx, path, light, opts) {  /* THE OBSERVATION. width from light */
    var o = opts || {};
    var wMin = o.wMin != null ? o.wMin : 0.75;
    var wMax = o.wMax != null ? o.wMax : 3.2;
    cx.lineCap = "round";
    cx.lineJoin = "round";
    for (var i = 1; i < path.length; i++) {
      var a = path[i - 1], b = path[i];
      var ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
      var ndotl = Math.max(0, Math.cos(ang - light));
      cx.lineWidth = wMin + (wMax - wMin) * Math.pow(1 - ndotl, 1.6);
      cx.beginPath();
      cx.moveTo(a[0], a[1]);
      cx.lineTo(b[0], b[1]);
      cx.stroke();
    }
  }

  /* ---- wet beach gravel. Individually drawn clasts, never a fill ----
   * Long axes imbricated seaward, because wave-sorted gravel does that and a
   * reader who has stood on one feels it without naming it.
   */
  function clastField(cx, o) {
    var R = mk(o.seed), i, j;
    var n = o.count || 2400;
    var lit = o.lit || PAL.iceShadow, dark = o.dark || PAL.base;
    for (i = 0; i < n; i++) {
      var t = R.u();
      var y = o.y0 + (o.y1 - o.y0) * Math.pow(t, 0.7);
      var depth = (y - o.y0) / Math.max(1, o.y1 - o.y0);
      var rad = (o.rMin || 1.4) + ((o.rMax || 9) - (o.rMin || 1.4)) * depth;
      var x = R.range(o.x0, o.x1);
      var verts = R.int(5, 9);
      var tilt = R.norm(0.38, 0.12);            /* imbrication, ~18 to 26 deg */
      cx.beginPath();
      for (j = 0; j < verts; j++) {
        var a = (j / verts) * Math.PI * 2 + tilt;
        var rr = rad * R.norm(1, 0.22);
        var px = x + Math.cos(a) * rr * 1.35, py = y + Math.sin(a) * rr * 0.72;
        if (j === 0) cx.moveTo(px, py); else cx.lineTo(px, py);
      }
      cx.closePath();
      cx.fillStyle = dark;
      cx.fill();
      /* lit facet on the key side */
      cx.beginPath();
      cx.moveTo(x - rad, y);
      cx.quadraticCurveTo(x, y - rad * 0.85, x + rad * 1.1, y - rad * 0.15);
      cx.lineTo(x + rad * 0.6, y + rad * 0.2);
      cx.closePath();
      cx.fillStyle = lit;
      cx.globalAlpha = 0.55 + 0.35 * depth;
      cx.fill();
      cx.globalAlpha = 1;
      /* wet specular chip on 38 percent of them, because it is raining */
      if (R.u() < 0.38) {
        cx.beginPath();
        cx.ellipse(x + rad * 0.25, y - rad * 0.4, rad * 0.26, rad * 0.12,
                   -0.5, 0, Math.PI * 2);
        cx.fillStyle = o.chip || PAL.wetChip;
        cx.globalAlpha = 0.35;
        cx.fill();
        cx.globalAlpha = 1;
      }
    }
  }

  /* ---- wind chop. Facets with a lit upwind face and a dark lee face ---- */
  function chopField(cx, o) {
    var R = mk(o.seed);
    var n = o.count || 1400;
    var wind = (o.windDeg != null ? o.windDeg : 118) * Math.PI / 180;
    for (var i = 0; i < n; i++) {
      var t = R.u();
      var y = o.y0 + (o.y1 - o.y0) * Math.pow(t, 0.55);
      var depth = (y - o.y0) / Math.max(1, o.y1 - o.y0);
      var x = R.range(o.x0, o.x1);
      var len = (o.lMin || 6) + ((o.lMax || 18) - (o.lMin || 6)) * depth;
      var a = wind + R.norm(0, 0.24);
      var dx = Math.cos(a) * len, dy = Math.sin(a) * len * 0.22;
      var h = len * 0.30 * R.norm(1, 0.2);
      cx.beginPath();                        /* lit upwind face */
      cx.moveTo(x, y);
      cx.lineTo(x + dx * 0.5, y + dy * 0.5 - h);
      cx.lineTo(x + dx, y + dy);
      cx.closePath();
      cx.fillStyle = o.lit || PAL.iceShadow;
      cx.globalAlpha = (0.30 + 0.5 * depth) * (o.alpha || 1);
      cx.fill();
      cx.beginPath();                        /* dark lee face */
      cx.moveTo(x + dx * 0.5, y + dy * 0.5 - h);
      cx.lineTo(x + dx, y + dy);
      cx.lineTo(x + dx * 0.72, y + dy + h * 0.5);
      cx.closePath();
      cx.fillStyle = o.lee || PAL.deep;
      cx.globalAlpha = (0.45 + 0.35 * depth) * (o.alpha || 1);
      cx.fill();
      cx.globalAlpha = 1;
    }
  }

  /* ---- the contact triple. POOL, then CAST, then SEAM. Never reordered. ----
   *
   * A contact shadow is a SUBTRACTION and needs something to subtract from, so
   * the LIT GROUND is laid first and the cast is dropped into it. The cure for a
   * weak contact is never a darker shadow, it is a wider, brighter pool. And the
   * floor is not a target: if the contact reads, stop. The SEAM is the mark that
   * says attached, and a gap where the seam should be is what reads as a hole.
   *
   * The rects the slide DECLARES in data-contacts are measured off the render
   * with scripts/contact_probe.py, never computed from these arguments.
   */
  function contactTriple(cx, o) {
    var fx = o.x, fy = o.y, w = o.w || 96;
    var g = cx.createRadialGradient(fx, fy + 14, 0, fx, fy + 14, o.pool || 210);
    g.addColorStop(0.00, o.poolHi || "#3B4A58");
    g.addColorStop(0.62, o.poolHi || "#3B4A58");   /* ramp HOLDS before it falls */
    g.addColorStop(1.00, "rgba(0,0,0,0)");
    cx.globalAlpha = o.poolAlpha != null ? o.poolAlpha : 0.55;
    cx.fillStyle = g;
    cx.beginPath();
    cx.ellipse(fx, fy + 14, o.pool || 210, (o.pool || 210) * 0.34, 0, 0, Math.PI * 2);
    cx.fill();
    cx.globalAlpha = 1;

    var c = cx.createRadialGradient(fx, fy + 2, 0, fx, fy + 2, o.ambient || 150);
    c.addColorStop(0, o.cast || PAL.shadow);
    c.addColorStop(1, "rgba(0,0,0,0)");
    cx.globalAlpha = 0.62;
    cx.fillStyle = c;
    cx.beginPath();
    cx.ellipse(fx, fy + 2, o.ambient || 150, (o.ambient || 150) * 0.22, 0, 0, Math.PI * 2);
    cx.fill();
    cx.globalAlpha = 1;

    cx.beginPath();                              /* the tight core */
    cx.ellipse(fx, fy + 2, w, w * 0.16, 0, 0, Math.PI * 2);
    cx.fillStyle = o.cast || PAL.shadow;
    cx.globalAlpha = 0.85;
    cx.fill();
    cx.globalAlpha = 1;

    cx.beginPath();                              /* THE SEAM. attached, not floating */
    cx.ellipse(fx, fy, w * 0.92, Math.max(1.4, w * 0.035), 0, 0, Math.PI * 2);
    cx.fillStyle = o.seam || "#050B12";
    cx.globalAlpha = 0.9;
    cx.fill();
    cx.globalAlpha = 1;
  }

  /* ---- reserve punch. BLURRED RECTANGLES, never a radial gradient ----
   * A radial punch's outer radius is half the box's longest side, so on a 900px
   * line of type the circle has faded to nothing well before the ends of the
   * line and the field stays over the first and last words. A rect follows the
   * SHAPE of the thing being reserved. ctx.filter applies PER DRAW OP, so this
   * punches once, on the offscreen canvas, and never inside a stroke loop.
   */
  function punch(ctx, boxes, o) {
    var opt = o || {}, blur = opt.blur != null ? opt.blur : 14, pad = opt.pad || 10;
    ctx.save();
    ctx.globalCompositeOperation = "destination-out";
    ctx.filter = "blur(" + blur + "px)";
    ctx.fillStyle = "#000";
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      ctx.fillRect(b[0] - pad, b[1] - pad, b[2] + pad * 2, b[3] + pad * 2);
    }
    ctx.restore();
  }

  /* boxes for DOM elements, in design px. Call AFTER document.fonts.ready, and
   * per LINE BOX rather than per block, so a ragged paragraph reserves a ragged
   * hole instead of one fat rectangle. */
  function boxesFor(sel) {
    var out = [], els = document.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++) {
      var rects = els[i].getClientRects();
      for (var j = 0; j < rects.length; j++) {
        var r = rects[j];
        if (r.width > 2 && r.height > 2) out.push([r.left, r.top, r.width, r.height]);
      }
    }
    return out;
  }

  function offscreen(w, h) {
    var c = document.createElement("canvas");
    c.width = w * 2; c.height = h * 2;
    var x = c.getContext("2d");
    x.scale(2, 2);
    return { c: c, x: x };
  }

  /* grain as a small repeating tile. NEVER a full-frame feTurbulence rect, which
   * embeds at 10 to 40 MB in the PDF. grainTile returns a DATA URL, not a canvas,
   * so it goes on a DOM div's background and never into createPattern. */
  function grainCss(seed) {
    return "url(" + AK.grainTile(280, 52, seed) + ")";
  }

  global.AKDISC = {
    PAL: PAL, ARC: ARC, DISC: DISC,
    mk: mk, P: P, monthAngle: monthAngle, yearRadius: yearRadius,
    YEAR0: YEAR0, YEAR1: YEAR1, RIN: RIN, ROUT: ROUT,
    KEY: KEY,
    ruled: ruled, swelled: swelled,
    clastField: clastField, chopField: chopField, contactTriple: contactTriple,
    punch: punch, boxesFor: boxesFor, offscreen: offscreen, grainCss: grainCss
  };
})(typeof window !== "undefined" ? window : globalThis);
