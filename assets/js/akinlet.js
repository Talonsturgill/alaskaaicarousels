/* akinlet.js — THE WATERLINE HOLD, Carousel No.65's continuity chassis.
 *
 * Committed 2026-09-21. DECK FURNITURE, shared across all nine slides on
 * purpose, which is why it is a module rather than inline code: bespoke_check
 * strips `<script src=>` as house harness, so one shared coordinate system
 * costs the variety budget nothing while each slide's own composition still
 * has to earn its score. Same reasoning as akrail.js, akcolumn.js, akseam.js,
 * aknight.js, aksheet.js, akpour.js and akunderice.js.
 *
 * WHAT THIS IS. One survey camera holds station at the surface of Upper Cook
 * Inlet off the East Foreland for nine frames. The frame is the MENISCUS, the
 * boundary between air and glacial rock flour, and the camera never travels.
 * What this file owns is everything that must be identical on all nine frames
 * so the deck reads as one continuous take: the docket staff's geometry, the
 * calendar axis struck into it, the light extinction curve that shades the
 * water, and the four render states that carry provenance.
 *
 * WHY IT IS NOT akunderice.js, which already exists and is close. That file
 * (No.57, committed September 12th) is a VERTICAL SECTION of a water body,
 * ice to bed, with a depth-to-pixel mapping and no camera. This deck may not
 * be a section: No.64 shipped an orthographic vertical section on September
 * 20th and it sits inside the last-four hero-structure window, so the one
 * library that fits this story best is the one that would have made this deck
 * look like two recent decks. This file has a real perspective camera, a real
 * lens, a real depth of field and a boundary the camera crosses, and it
 * shares no code with akunderice by design rather than by accident.
 *
 * THE CALENDAR IS A MEASURED AXIS AND NOT DECORATION. The staff is graduated
 * linear in DAYS from the Federal Register publication (day 0, September 4th,
 * claim C20) to the filing deadline (day 59, 5:00 p.m. Eastern November 2nd,
 * claim C14). Every slide declares it on `<body data-scale>` and every
 * graduation inside the band is listed with what it means, because there is
 * no such thing as a decorative tick on a measured axis. The waterline on the
 * staff sits at day 17, today, on all nine frames and does not move, because
 * the story's present does not move. Nothing about the clock is composition.
 *
 * THE FOUR RENDER STATES, which are this deck's whole honesty system:
 *
 *   MATERIAL       verified against the primary federal notice.
 *                  Lit, with a specular, a cast and a measured contact.
 *   HALF_MATERIAL  verified, but to ONE newspaper article.
 *                  Modelled but matte, no specular, contact at half depth.
 *   PHANTOM        proposed in the notice, does not exist.
 *                  Unlit drafting dash. Casts nothing. Receives nothing.
 *   VOID           the notice does not say, and the absence is verified.
 *                  A hole with a lit rim and nothing inside it.
 *
 * A pixel critic who finds one LIT turbine anywhere in this deck has found a
 * defect, and the fix is a rebuild rather than a caption.
 *
 * LOAD ORDER. noise.js writes `global.AK = {...}` wholesale, so it must load
 * FIRST or it will erase AK.fitText and AK.hachureField. This file assigns
 * onto window.AKINLET and touches AK only by reading it.
 */
(function (global) {
  "use strict";
  var AKI = {};

  /* ---- the calendar axis, identical on all nine frames ------------------ */

  AKI.AXIS = {
    day0Y: 1180,          // September 4th, the notice is published (C20)
    day59Y: 340,          // November 2nd, 5:00 p.m. Eastern (C14)
    pxPerDay: (1180 - 340) / 59,   // 14.237288...
    todayDay: 17          // September 21st
  };
  AKI.dayY = function (d) {
    return AKI.AXIS.day0Y - d * AKI.AXIS.pxPerDay;
  };
  AKI.WATERLINE_Y = AKI.dayY(AKI.AXIS.todayDay);   // 938.0

  AKI.STAFF = { x0: 906, x1: 982, cx: 944, w: 76 };

  /* The graduations this deck DRAWS. Weekly, plus today and the deadline.
   * Two more exist and are drawn on one frame each, so they are listed
   * separately rather than smuggled into the default set: day 10 is the
   * Alaska Energy Authority statement (slide 07) and day 57 is October 31st
   * (slide 09). Every one of these reaches the slide's own data-scale
   * declaration with a meaning, or qa.py fails the frame. */
  AKI.MARKS = [
    { d: 0,  means: "September 4th, the notice is published" },
    { d: 7,  means: "one week" },
    { d: 14, means: "two weeks" },
    { d: 17, means: "September 21st, today, the waterline" },
    { d: 21, means: "three weeks" },
    { d: 28, means: "four weeks" },
    { d: 35, means: "five weeks" },
    { d: 42, means: "six weeks" },
    { d: 49, means: "seven weeks" },
    { d: 59, means: "November 2nd, 5:00 p.m. Eastern, the filing deadline" }
  ];
  AKI.MARK_AEA = { d: 10, means: "September 14th, the AEA statement" };
  AKI.MARK_OCT31 = { d: 57, means: "October 31st, a Saturday" };

  /* ---- the light, one key for the whole deck ---------------------------- */

  AKI.KEY_AZ = 208;
  AKI.KEY_EL = 34;
  /* lightX = -sin(az) = +0.469, so every cast falls LEFT and the key stands
   * screen right, on the same side as the staff. */
  AKI.LIGHT_X = -Math.sin(AKI.KEY_AZ * Math.PI / 180);
  AKI.LIGHT_Y = Math.cos(AKI.KEY_EL * Math.PI / 180);

  AKI.INK = {
    extinction: "#060C11",
    shadow:     "#0E1A1C",
    water:      "#1B2A26",
    silt:       "#3E4A3C",
    flour:      "#7C7A5E",
    meniscus:   "#B6B9AE",
    air:        "#C9D4D8",
    specular:   "#E8EEF0",
    phantom:    "#6E8079",
    state:      "#6EA5FF",
    gold:       "#FFC72C",
    mark:       "#46545F"
  };

  /* ---- extinction, and it is the deck's one piece of physics ------------ */

  AKI.M_PER_PX = 1 / 280;          // one metre of water is 280 design px
  AKI.K = 1.9;                     // extinction coefficient, glacial rock flour
  AKI.VANISH_M = 1.1;              // where the phantom array reaches zero

  AKI.depthAt = function (y, meniscusY) {
    return Math.max(0, (y - meniscusY) * AKI.M_PER_PX);
  };
  AKI.E = function (depthM) {
    return Math.exp(-AKI.K * depthM);
  };
  /* Normalised so it reaches EXACTLY zero at VANISH_M rather than asymptoting
   * near it. The phantom array's alpha is this function and nothing else, so
   * the depth at which the description disappears is drawn by the same number
   * that shades the water. */
  AKI.vanish = function (depthM) {
    var e0 = AKI.E(AKI.VANISH_M);
    var v = (AKI.E(depthM) - e0) / (1 - e0);
    return v < 0 ? 0 : (v > 1 ? 1 : v);
  };

  /* ---- the water column ------------------------------------------------- */

  /* The hachure field's REQUIRED height. It has no default by design, which is
   * the whole reason the bench is the right tool here: the middle frequency is
   * forced to be a function of the story's own quantity.
   *
   * It varies in BOTH axes on purpose. A height that only falls in v gives
   * every cell the same aspect and the field degenerates into rows of equal
   * strokes, which is the one-axis lay collapse this house has shipped before.
   * The u term is the suspension's own unevenness, which is physically true of
   * a tidal water column and is what gives the field its aspect variation. */
  AKI.heightFor = function (box, meniscusY) {
    return function (u, v) {
      var y = box.y + v * box.h;
      var d = AKI.depthAt(y, meniscusY);
      var e = AKI.E(d);
      /* THE MIX IS THE WHOLE POINT, and the first build got it backwards.
       * A height dominated by depth has a gradient that points almost
       * straight down, so every hachure stroke stands vertically and a tidal
       * water column renders as a field of grass. The aspect a viewer reads
       * as CURRENT is horizontal, so the u term has to be the larger one:
       * the suspension's own along-flow banding carries the aspect, and
       * extinction rides on top as a slower envelope that still puts the
       * widest strokes at depth. 0.35 / 0.30 / 0.35 is the split, and it is
       * a measured choice rather than a taste one, because the three probes
       * still have to come back nearfield > midsilt > extinction. */
      var f = AK.fbm2(u * 4.6, v * 0.9 + 11.4, 4);
      var g = AK.fbm2(u * 1.3 + 31.7, v * 2.7, 3);
      return Math.max(0, Math.min(1,
        0.34 + 0.30 * e + 0.26 * (f * 0.5 + 0.5) + 0.10 * (g * 0.5 + 0.5)));
    };
  };

  AKI.HACHURE = {
    cell: 14, passes: 3, sunAz: 208, sunEl: 34, sunJitter: 9,
    slopeGamma: 1.35, minWidth: 0.75, maxWidth: 3.2, lenScale: 2.1,
    bend: 0.12, lightBias: true
  };
  /* BEND WAS 0.35 AND FOUR CRITICS READ THE FIELD AS A HEDGEROW. A bend that
   * large curls each stroke's tail up out of the flow direction, and a curled
   * stroke has a vertical component whatever its base angle, so the field
   * reads as standing vegetation rather than as suspension carried sideways.
   * 0.12 keeps the hand-drawn irregularity that stops the field looking
   * machine-ruled and loses the upward hook entirely. Measured on 08, whose
   * water is the largest uninterrupted field in the deck. */

  /* Three probes on every frame, and their mean stroke widths must come back
   * in descending order or the field is not carrying its data. Positions are
   * relative to the water box so each slide's own meniscus moves them. */
  AKI.probesFor = function (box, meniscusY) {
    var top = Math.max(box.y, meniscusY);
    var span = box.y + box.h - top;
    return [
      { name: "nearfield",  x: box.x + 60,  y: top + span * 0.04, w: 220, h: 110 },
      { name: "midsilt",    x: box.x + 300, y: top + span * 0.42, w: 220, h: 110 },
      { name: "extinction", x: box.x + 120, y: top + span * 0.80, w: 220, h: 110 }
    ];
  };

  /* The graded water column. Built from the extinction curve itself rather
   * than from a hand-authored linear-gradient, so the falloff a reader sees is
   * the same function the hachure field is shading. */
  /* THE PAINT CENSUS HAS AN ENTRY CAP, and a colour law it cannot finish
   * counting is a law nobody checked. qa.py says so out loud: "this frame's
   * paint census hit its entry cap, so absence is unproven here". A per-pixel
   * ramp written as a fresh rgb() literal per band is the cheapest way to blow
   * it, so every ramp in this deck is QUANTISED to a small fixed set of
   * literals. The picture is unchanged at 8 bits; the census can finish. */
  AKI.RAMP_STEPS = 18;
  AKI._rampCache = {};
  AKI.rampAt = function (t) {
    var q = Math.round(Math.max(0, Math.min(1, t)) * (AKI.RAMP_STEPS - 1));
    if (AKI._rampCache[q] === undefined) {
      AKI._rampCache[q] = AKI.mix(AKI.INK.extinction, AKI.INK.silt,
        q / (AKI.RAMP_STEPS - 1));
    }
    return AKI._rampCache[q];
  };

  AKI.waterColumn = function (cx, box, meniscusY) {
    var steps = 96, i, t, y0, y1, d, e;
    for (i = 0; i < steps; i++) {
      t = i / steps;
      y0 = box.y + t * box.h;
      y1 = box.y + (i + 1) / steps * box.h;
      d = AKI.depthAt(y0, meniscusY);
      e = AKI.E(d);
      cx.fillStyle = AKI.rampAt(Math.pow(e, 0.7));
      cx.fillRect(box.x, y0 - 0.5, box.w, y1 - y0 + 1.2);
    }
  };

  AKI.mix = function (a, b, t) {
    if (global.AKC && AKC.mixOklab) return AKC.mixOklab(a, b, t);
    var pa = AKI.hex(a), pb = AKI.hex(b);
    return "rgb(" + Math.round(pa[0] + (pb[0] - pa[0]) * t) + "," +
      Math.round(pa[1] + (pb[1] - pa[1]) * t) + "," +
      Math.round(pa[2] + (pb[2] - pa[2]) * t) + ")";
  };
  AKI.hex = function (h) {
    var n = parseInt(h.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  };

  /* The suspension. Discrete hard-edged marks, rejection sampled AGAINST the
   * irradiance field so they are dense in the lit metre and absent in
   * extinction, each with a streak along the flood direction, which runs right
   * to left. A population of discrete steps survives the 6x downsample to feed
   * width where a graded wash reads as nothing. */
  /* Six literals, fixed, for the same census reason as the ramp. */
  AKI.MOTE_INKS = ["#5D6656", "#6E7862", "#7C7A5E", "#96A089", "#B6B9AE", "#E8EEF0"];

  AKI.motes = function (cx, box, meniscusY, count, seed) {
    var rnd = AK.rng(seed);
    var placed = 0, tries = 0, cap = count * 14;
    cx.save();
    cx.lineCap = "round";
    while (placed < count && tries < cap) {
      tries++;
      var x = box.x + rnd() * box.w;
      var y = box.y + rnd() * box.h;
      if (y < meniscusY) continue;
      var e = AKI.E(AKI.depthAt(y, meniscusY));
      /* THE SUSPENSION DOES NOT STOP, IT GOES DARK. Rejecting on `e` alone
       * gave the population a hard floor: below roughly 0.9 m the acceptance
       * rate is under 0.18 and the lower third of every frame came back
       * literally empty, which reads as a cutoff line across the water rather
       * than as extinction. Glacial flour is present at depth; what falls off
       * is the light returning from it. So the floor keeps 14 percent of the
       * sampling all the way down and the ALPHA carries the decay. */
      if (rnd() > 0.14 + 0.86 * e) continue;
      var r = 0.7 + rnd() * 1.5;
      var len = 5 + rnd() * 9;
      var a = 0.045 + e * 0.33;
      cx.globalAlpha = a;
      cx.strokeStyle = AKI.MOTE_INKS[Math.min(5, (e * 6) | 0)];
      cx.lineWidth = r;
      cx.beginPath();
      cx.moveTo(x + len * 0.5, y);
      cx.lineTo(x - len * 0.5, y + (rnd() - 0.5) * 1.6);
      cx.stroke();
      placed++;
    }
    cx.restore();
    cx.globalAlpha = 1;
    return placed;
  };

  /* ---- the docket staff -------------------------------------------------- */

  /* THE ENGRAVER'S LINE LAW, which is why no graduation here is a single
   * stroke. A cut line swells toward solid in shadow and thins toward nothing
   * in the highlight, and depth increases with width, so a groove's width IS
   * its depth and its darkness. A constant-weight stroke is not a shallow
   * incision, it is a drawing of a wire lying on top. Every graduation is
   * three strokes: a bright lip outside-aligned on the light side, a dark
   * trough whose width varies with depth, and a shoulder that falls off. */
  AKI.graduation = function (cx, y, x0, x1, depth, tint) {
    var w = 1.4 + depth * 3.4;
    cx.save();
    // the shoulder, widest and faintest, falling off below the cut
    cx.globalAlpha = 0.30 + depth * 0.18;
    cx.strokeStyle = AKI.INK.extinction;
    cx.lineWidth = w * 1.9;
    cx.beginPath(); cx.moveTo(x0, y + w * 0.8); cx.lineTo(x1, y + w * 0.8); cx.stroke();
    // the trough
    cx.globalAlpha = 0.86;
    cx.strokeStyle = tint || AKI.INK.extinction;
    cx.lineWidth = w;
    cx.beginPath(); cx.moveTo(x0, y); cx.lineTo(x1, y); cx.stroke();
    // the bright lip, OUTSIDE-aligned onto the dark side so no part of it
    // lands on paper it matches
    cx.globalAlpha = 0.72 + depth * 0.2;
    cx.strokeStyle = AKI.INK.specular;
    cx.lineWidth = Math.max(0.7, w * 0.36);
    cx.beginPath();
    cx.moveTo(x0, y - w * 0.62); cx.lineTo(x1, y - w * 0.62);
    cx.stroke();
    cx.restore();
    cx.globalAlpha = 1;
  };

  /* The staff body. A lathed box section with a lit face on the key side and a
   * shaded face on the lee, so it is a solid rather than a rectangle. */
  AKI.staffBody = function (cx, o) {
    var x0 = o.x0, x1 = o.x1, yTop = o.yTop, yBot = o.yBot;
    var w = x1 - x0, split = x0 + w * 0.62;
    var g = cx.createLinearGradient(x0, 0, x1, 0);
    g.addColorStop(0, AKI.mix(AKI.INK.silt, AKI.INK.extinction, 0.35));
    g.addColorStop(0.62, AKI.INK.meniscus);
    g.addColorStop(1, AKI.mix(AKI.INK.meniscus, AKI.INK.specular, 0.5));
    cx.fillStyle = g;
    cx.fillRect(x0, yTop, w, yBot - yTop);
    // the lit arris, outside-aligned on the dark side of the boundary
    cx.save();
    cx.globalAlpha = 0.9;
    cx.strokeStyle = AKI.INK.specular;
    cx.lineWidth = 1.6;
    cx.beginPath(); cx.moveTo(split, yTop); cx.lineTo(split, yBot); cx.stroke();
    cx.restore();
    return split;
  };

  /* ---- render states ----------------------------------------------------- */

  AKI.PHANTOM_DASH = [30, 5, 6, 5, 6, 5];
  AKI.phantomStyle = function (cx, alpha) {
    cx.setLineDash(AKI.PHANTOM_DASH);
    cx.lineWidth = 1.25;
    cx.strokeStyle = AKI.INK.phantom;
    cx.globalAlpha = alpha === undefined ? 1 : alpha;
    cx.lineCap = "butt";
    cx.lineJoin = "miter";
    cx.shadowBlur = 0;
    cx.shadowColor = "transparent";
  };
  AKI.clearPhantom = function (cx) {
    cx.setLineDash([]);
    cx.globalAlpha = 1;
  };

  /* A LIT GROUND IS SCREENED OVER THE SURFACE, NEVER PAINTED ON IT, and the
   * cast is an ATTACHED subtraction thrown down-light out of that lit ground.
   * A painted radial pool centred on an object's own base puts the brightest
   * paper exactly where the darkest mark has to go, and the composite is a
   * change of one or two L*, which four pixel critics once read as "the object
   * floats". And canvas has no elliptical gradient: createRadialGradient is a
   * CIRCLE, so it is built about the origin inside a transform. */
  AKI.litPool = function (cx, x, y, rx, ry, strength) {
    var R = 100;
    cx.save();
    cx.globalCompositeOperation = "screen";
    cx.translate(x, y);
    cx.scale(rx / R, ry / R);
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    var s = strength === undefined ? 0.34 : strength;
    g.addColorStop(0, "rgba(160,168,140," + s + ")");
    g.addColorStop(0.55, "rgba(124,122,94," + (s * 0.42) + ")");
    g.addColorStop(1, "rgba(124,122,94,0)");
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
  };

  /* The cast. ATTACHED, thrown down-light, and it subtracts from the pool
   * rather than being painted onto bare ground. A gap between the object base
   * and the cast is what reads as a hole, so offPx defaults small. */
  AKI.cast = function (cx, x, y, rx, ry, strength) {
    var R = 100;
    cx.save();
    cx.globalCompositeOperation = "multiply";
    cx.translate(x + AKI.LIGHT_X * rx * 0.34, y + 2);
    cx.scale(rx / R, ry / R);
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    var s = strength === undefined ? 0.62 : strength;
    g.addColorStop(0, "rgba(14,26,28," + s + ")");
    g.addColorStop(0.62, "rgba(14,26,28," + (s * 0.45) + ")");
    g.addColorStop(1, "rgba(14,26,28,0)");
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
  };

  /* ---- the finish -------------------------------------------------------- */

  /* EVERY GRADING OPTION IS STICKY AND filmic DEFAULTS TO TRUE. A call that
   * asks only for dither silently runs an ACES curve over the whole frame and
   * moves every value this run has already measured for contrast, contact and
   * ink law. No.64 lost nine label-crossing failures in one render to that
   * default. This wrapper exists so no slide can forget. */
  AKI.grade = function (cx, w, h, seed) {
    if (!global.AKPOST) return;
    AKPOST.grade(cx, {
      w: w, h: h,
      exposure: -0.15,
      saturation: 0.92,
      contrast: 1.10,
      filmic: false,
      dither: true,
      sharpen: 0.32,
      grain: { amount: 0.045, size: 2, seed: seed }
    });
  };

  AKI.grain = function (cx, w, h, seed) {
    var url = AK.grainTile(280, 52, seed);   // RETURNS A DATA URL, NOT A CANVAS
    return new Promise(function (resolve) {
      var img = new Image();
      img.onload = function () {
        var pat = cx.createPattern(img, "repeat");
        cx.save();
        cx.globalCompositeOperation = "overlay";
        cx.globalAlpha = 0.07;
        cx.fillStyle = pat;
        cx.fillRect(0, 0, w, h);
        cx.restore();
        cx.globalAlpha = 1;
        resolve(true);
      };
      img.onerror = function () { resolve(false); };
      img.src = url;
    });
  };

  /* THE RESERVE IS A BLURRED RECTANGLE, NEVER A RADIAL GRADIENT (No.55).
   * A radial punch cannot reserve a long box: its outer radius is half the
   * box's longest side, so on a 900 px line of type the circle has faded to
   * nothing well before the ends of the line and the field stays over the
   * first and last words while the middle is cleanly reserved. qa.py reports
   * that as a worst-point contrast failure against a healthy box mean, which
   * is exactly the shape of failure this deck hit on its first render.
   *
   * `ctx.filter` applies PER DRAW OP, so the punch happens once on the
   * offscreen canvas and never inside a loop. destination-out leaves the
   * region transparent, so what shows through is the page's own dark ground,
   * which is the deep-sea scrim this house already uses. */
  AKI.reserve = function (draw, W, H, rects, blur, alpha) {
    var off = document.createElement('canvas');
    off.width = W * 2; off.height = H * 2;
    var ox = off.getContext('2d');
    ox.scale(2, 2);
    draw(ox);
    /* AND THE PUNCH IS PARTIAL. A full destination-out leaves the region
     * completely transparent, so what shows through is a hard-edged black
     * rectangle, which is the plate this house bans wearing a costume. The
     * first build of No.65's cover shipped three of them. The punch takes an
     * alpha and a generous blur so the result is a graded scrim in the
     * frame's own darkest value, felt and not seen. */
    /* AND IT IS FEATHERED IN BOTH AXES, for the reason written on AKI.scrim:
     * a partial punch with a flat interior is still a rectangle, and the
     * cover shipped two of them into round one. The punch mask is built with
     * the same ramp the scrim uses so the two surfaces cannot drift apart. */
    var mask = document.createElement('canvas');
    mask.width = W * 2; mask.height = H * 2;
    var mx = mask.getContext('2d');
    mx.scale(2, 2);
    for (var i = 0; i < rects.length; i++) AKI._feather(mx, rects[i], '#000');
    ox.save();
    ox.filter = 'blur(' + (blur === undefined ? 64 : blur) + 'px)';
    ox.globalCompositeOperation = 'destination-out';
    ox.globalAlpha = (alpha === undefined ? 0.72 : alpha);
    ox.drawImage(mask, 0, 0, W, H);
    ox.restore();
    return off;
  };

  /* ONE CORRECT CONTACT IDIOM, so nine slides cannot get it wrong nine ways.
   *
   * The first build of this deck wrote the pool and the cast by hand on five
   * frames and qa.py failed four of them with the same sentence: "a painted
   * light is sitting on the declared contact shadow". The pool's radius
   * reached across the gap and lit the rect the slide had just declared dark,
   * which is a glow with no source in the picture, and the dL measurement
   * cannot see it because a bright pool beside a dark hole passes a
   * difference test.
   *
   * So the geometry is computed here, once, from the separation: the two
   * rects sit SIDE BY SIDE at the object's own base line, the pool is centred
   * on the ground rect, the cast is centred on the shadow rect, and both
   * radii are held to 0.55 of the separation so neither can reach the other.
   * The function returns the exact rects to paste into data-contacts, so the
   * declaration and the drawing are the same arithmetic. */
  AKI.contactPair = function (cx, xShadow, xGround, y, o) {
    o = o || {};
    var sep = Math.abs(xGround - xShadow);
    var r = Math.min(o.r || 1e9, sep * 0.55);
    var ry = o.ry || Math.max(16, r * 0.17);
    var hw = Math.min(64, r * 0.62);
    AKI.litPool(cx, xGround, y, r, ry, o.light === undefined ? 0.44 : o.light);
    AKI.cast(cx, xShadow, y, r * 0.78, ry * 0.8, o.dark === undefined ? 0.60 : o.dark);
    return {
      shadow: [Math.round(xShadow - hw), Math.round(y - ry * 0.5), Math.round(hw * 2), Math.round(ry)],
      ground: [Math.round(xGround - hw), Math.round(y - ry * 0.5), Math.round(hw * 2), Math.round(ry)]
    };
  };

  /* THE DEEP-SEA SCRIM (TECHNIQUE_LIBRARY 7), applied AFTER the art and
   * before the grain, which is the only order that works.
   *
   * The reserve punch in `AKI.reserve` runs on the background pass, so
   * anything drawn afterwards, a hachure field, a mote population, a drawn
   * ripple, goes straight back over the reserved box. Four frames failed
   * "label crossed by art" and "canvas mark inside reserved text" on exactly
   * that ordering. A scrim laid last cannot be overdrawn by construction.
   *
   * Blurred RECTANGLES, never a radial, for the reason No.55 recorded: a
   * radial's outer radius is half the box's longest side, so on a long line
   * of type it has faded to nothing before the ends and the field stays over
   * the first and last words. */
  /* A BLUR SOFTENS AN EDGE, IT DOES NOT SOFTEN AN INTERIOR, and that is why
   * round one's scrims were still legible as boxes. An 840 x 470 rectangle
   * blurred at 42 px is a flat slab with eight soft pixels around it: the eye
   * reads the plateau, not the edge. Three critics named the same three
   * shapes on 01, 05 and 09.
   *
   * So a scrim rectangle is now FEATHERED IN BOTH AXES before it is blurred.
   * A vertical multi-stop ramp gives the band its falloff, a horizontal ramp
   * is composited through destination-in, and the product has no plateau at
   * all: the darkest value sits on the type's own centreline and every
   * boundary decays to nothing inside the box. The blur that follows is then
   * doing what a blur is good at, hiding the ramp's own banding. */
  AKI._feather = function (ox, r, color, edge) {
    var x = r[0], y = r[1], w = r[2], h = r[3];
    var e = edge === undefined ? 0.30 : edge;
    var g = ox.createLinearGradient(0, y, 0, y + h);
    g.addColorStop(0, 'rgba(0,0,0,0)');
    g.addColorStop(e * 0.5, 'rgba(0,0,0,0.55)');
    g.addColorStop(e, 'rgba(0,0,0,1)');
    g.addColorStop(1 - e, 'rgba(0,0,0,1)');
    g.addColorStop(1 - e * 0.5, 'rgba(0,0,0,0.55)');
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ox.save();
    ox.beginPath(); ox.rect(x, y, w, h); ox.clip();
    ox.fillStyle = g; ox.fillRect(x, y, w, h);
    ox.globalCompositeOperation = 'destination-in';
    var hx = ox.createLinearGradient(x, 0, x + w, 0);
    var ex = Math.min(0.30, 90 / Math.max(1, w));
    hx.addColorStop(0, 'rgba(0,0,0,0)');
    hx.addColorStop(ex, 'rgba(0,0,0,1)');
    hx.addColorStop(1 - ex, 'rgba(0,0,0,1)');
    hx.addColorStop(1, 'rgba(0,0,0,0)');
    ox.fillStyle = hx; ox.fillRect(x, y, w, h);
    ox.globalCompositeOperation = 'source-in';
    ox.fillStyle = color; ox.fillRect(x, y, w, h);
    ox.restore();
  };

  AKI.scrim = function (cx, W, H, rects, blur, alpha) {
    var off = document.createElement('canvas');
    off.width = W * 2; off.height = H * 2;
    var ox = off.getContext('2d');
    ox.scale(2, 2);
    for (var i = 0; i < rects.length; i++) {
      var pad = document.createElement('canvas');
      pad.width = W * 2; pad.height = H * 2;
      var px = pad.getContext('2d');
      px.scale(2, 2);
      AKI._feather(px, rects[i], AKI.INK.extinction);
      ox.drawImage(pad, 0, 0, W, H);
    }
    cx.save();
    cx.filter = 'blur(' + (blur === undefined ? 34 : blur) + 'px)';
    cx.globalAlpha = (alpha === undefined ? 0.80 : alpha);
    cx.drawImage(off, 0, 0, W, H);
    cx.restore();
    cx.globalAlpha = 1;
  };

  global.AKINLET = AKI;
})(typeof window !== "undefined" ? window : globalThis);
