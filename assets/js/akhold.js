/* akhold.js -- the cargo hold chassis, built for carousel No. 59 (2026-09-14).
 *
 * WHAT THIS IS. The deck "NEW: THE HOLD AT ALTITUDE" is shot from inside the
 * cargo bay of a working Western Alaska freighter. Nine frames share one light,
 * one airframe vocabulary and one way of seating type, and this file is those
 * three things and nothing else. Every frame's COMPOSITION is written per slide.
 *
 * WHAT THIS IS NOT. There is no drawScene() here and there never will be. A
 * shared projection helper is house furniture; a shared drawTheWholeSlide is a
 * template, and scripts/bespoke_check.py measures the difference. This file
 * gives a slide primitives, and the slide decides what to build from them.
 *
 * LOAD ORDER. noise.js, then akcolor.js, then this. akengrave.js throws
 * "AKC is not defined" unless akcolor.js precedes it, and the same trap is
 * one import away here, so the order is stated rather than discovered.
 */
(function (global) {
  'use strict';

  var AKHOLD = {};

  /* ---------------------------------------------------------------- light
   *
   * ONE LIGHT, NINE FRAMES, DECLARED ONCE.
   *
   * az 76, el 12, resolved through lightVec(az, el) =
   *   [cos(el)sin(az), -cos(el)cos(az), sin(el)]
   * in screen space with +y DOWN, which gives x = +0.949 and y = -0.237.
   *
   * THE LIGHT IS TO THE UPPER RIGHT AND EVERY CAST RUNS TO THE LOWER LEFT.
   *
   * That sentence is written here, in the storyboard, and verbatim in every
   * slide's inline comment. Run No.51 typed one azimuth, hand shaded for the
   * opposite direction, and carried two light directions through nine frames,
   * three build rounds, five pixel critics and every gate.
   */
  AKHOLD.LIGHT = { az: 76, el: 12, keyToFill: 6.0 };

  AKHOLD.lightVec = function () {
    var a = AKHOLD.LIGHT.az * Math.PI / 180, e = AKHOLD.LIGHT.el * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  /* The unit vector a cast travels along, in screen px. Lower left. */
  AKHOLD.castDir = function () {
    var v = AKHOLD.lightVec(), L = Math.hypot(v[0], v[1]) || 1;
    return [-v[0] / L, -v[1] / L];
  };

  /* ---------------------------------------------------------------- basins
   *
   * HOW TYPE IS SEATED, AND IT IS NEVER A PLATE.
   *
   * Measured PER LINE BOX with a Range against getClientRects, so a ragged
   * block reserves unequal rects and the hole follows the rag. Reserving the
   * paragraph's bounding rectangle is the plate this exists to avoid: No.58
   * seated grey type on a linear gradient inside a fillRect, which does not
   * reach zero at its own left and right sides, and four critics on four
   * frames reported the two findable edges as a plate.
   */
  AKHOLD.lineBoxes = function (selector, pad) {
    pad = pad == null ? 16 : pad;
    var out = [];
    var nodes = document.querySelectorAll(selector);
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      var t;
      while ((t = walker.nextNode())) {
        if (!t.nodeValue || !t.nodeValue.trim()) continue;
        var r = document.createRange();
        r.selectNodeContents(t);
        var rects = r.getClientRects();
        for (var j = 0; j < rects.length; j++) {
          var b = rects[j];
          if (b.width < 2 || b.height < 2) continue;
          out.push([b.left - pad, b.top - pad, b.width + pad * 2, b.height + pad * 2]);
        }
      }
    }
    return out;
  };

  /* The punch is a BLURRED RECTANGLE and never a radial gradient.
   *
   * A radial's outer radius is half the box's longest side, so on a 900px line
   * of type the circle has faded to nothing well before the ends of the line,
   * the field stays over the first and last words, and qa.py reports that as a
   * worst-point contrast failure against a healthy box mean.
   *
   * ctx.filter applies PER DRAW OP, so this punches once on an offscreen canvas
   * and is never called inside a stroke loop.
   */
  AKHOLD.punch = function (ctx, rects, opts) {
    opts = opts || {};
    var blur = opts.blur == null ? 24 : opts.blur;
    ctx.save();
    ctx.globalCompositeOperation = 'destination-out';
    ctx.filter = 'blur(' + blur + 'px)';
    ctx.fillStyle = '#000';
    for (var i = 0; i < rects.length; i++) {
      var r = rects[i];
      /* Inset by the blur radius so the VISIBLE hole equals the measured box
       * rather than growing by the blur. */
      ctx.fillRect(r[0] + blur, r[1] + blur, r[2] - blur * 2, r[3] - blur * 2);
    }
    ctx.restore();
  };

  /* A density mask a field generator consults BEFORE it draws, so the
   * colliding stroke is never generated at all. Returns f(x, y) in 0..1. */
  AKHOLD.reserveMask = function (rects, feather) {
    feather = feather == null ? 26 : feather;
    return function (x, y) {
      var keep = 1;
      for (var i = 0; i < rects.length; i++) {
        var r = rects[i];
        var dx = Math.max(r[0] - x, 0, x - (r[0] + r[2]));
        var dy = Math.max(r[1] - y, 0, y - (r[1] + r[3]));
        var d = Math.hypot(dx, dy);
        if (d <= 0) return 0;
        if (d < feather) keep = Math.min(keep, d / feather);
      }
      return keep;
    };
  };

  /* --------------------------------------------------------- offscreen */
  AKHOLD.offscreen = function (w, h, draw) {
    var c = document.createElement('canvas');
    c.width = w * 2; c.height = h * 2;
    var x = c.getContext('2d');
    x.scale(2, 2);
    if (draw) draw(x, w, h);
    return c;
  };

  /* ------------------------------------------------------------- contact
   *
   * THE CONTACT TRIPLE, IN THE ONLY ORDER THAT MEASURES.
   *
   * Lit pool FIRST, screened over the surface. Then the cast, an ATTACHED
   * subtraction from that pool thrown down-light. Then the hard narrow seam.
   *
   * A painted radial pool centred on an object's own base puts the frame's
   * brightest point directly under the object, which five critics on No.41
   * read as a detached black hole inside a spotlight with no light source.
   * The pool here is offset UP-light from the foot and the cast runs down-light
   * from it, so the two sit side by side on one piece of ground, which is also
   * what keeps them inside qa.CONTACT_PAIR_SPAN.
   *
   * THE 4.0 L* FLOOR IS NOT A TARGET. If a contact reads, stop.
   */
  AKHOLD.contact = function (cx, o) {
    var fx = o.x, fy = o.y, w = o.w || 90, strength = o.k == null ? 0.5 : o.k;
    var d = AKHOLD.castDir();
    var squash = 0.34;

    /* CANVAS HAS NO ELLIPTICAL GRADIENT. A circular ramp poured into an ellipse
     * stops on the short axis while the ramp still carries alpha, which leaves a
     * hard arc. Build the ramp on a CIRCLE inside a transform instead. qa.py
     * names this one by arithmetic, and the deck's first pass drew nine of them. */
    function blob(cxp, cyp, r, inner, outer) {
      cx.save();
      cx.translate(cxp, cyp); cx.scale(1, squash);
      var g = cx.createRadialGradient(0, 0, 0, 0, 0, r);
      g.addColorStop(0, inner); g.addColorStop(1, outer);
      cx.fillStyle = g;
      cx.beginPath(); cx.arc(0, 0, r, 0, Math.PI * 2); cx.fill();
      cx.restore();
    }

    /* ------------------------------------------------------------------
     * THE ADDITIVE POOL IS GONE (2026-09-14, run No.59, five pixel critics).
     *
     * The version above this one laid a SCREENED radial blob of
     * rgba(196,216,232) down-light of the foot and then bit a small round
     * hole in it. On paper that was "the lit ground the cast falls on". In
     * the pixels it was the brightest region of nine frames out of nine,
     * with no source anywhere in the picture, and five critics reviewing
     * the deck independently arrived at the same three words for it: a
     * glowing manhole. One called it "an object glowing on its shadow
     * side", which is the exact physics: ground DOWN-light of an object is
     * the ground in shadow, and that is where the old routine put its
     * brightest paint.
     *
     * What replaces it is the thing the frames were missing rather than a
     * softer version of the thing they had. At the deck's elevation of 12
     * degrees an object throws a LONG shallow cast, and none of the nine
     * frames had one. The cast below is a tapering quad built inside a
     * squashed transform, so it lies in the floor plane instead of standing
     * up off it, drawn as four nested layers so its long edges are soft
     * without the cost of a blur pass.
     *
     * THE LIT GROUND IS NOW THE SLIDE'S JOB, not this routine's. Every
     * frame in this deck already draws a lit wedge or a lit floor; a
     * contact routine that paints its own light is a routine competing with
     * the picture's light. `o.lit` is available for a frame that genuinely
     * stands on near-black, and it is a HARD-EDGED sliver at low alpha in
     * source-over, never an additive blob.
     * ------------------------------------------------------------------ */
    var squash = o.squash != null ? o.squash : 0.34;
    var len = o.len != null ? o.len : w * 1.30;
    var seamW = o.seamW || w * 0.44;

    cx.save();
    cx.translate(fx, fy);
    cx.scale(1, squash);

    /* the cast direction inside the squashed frame: unsquashing it afterwards
     * is what lays the shadow down onto the floor rather than up the wall */
    var ex = d[0], ey = d[1] / squash;
    var em = Math.hypot(ex, ey) || 1;
    ex /= em; ey /= em;
    var qx = -ey, qy = ex;                     /* perpendicular, squashed frame */

    function castLayer(halfFoot, halfTip, a0) {
      var g = cx.createLinearGradient(0, 0, ex * len, ey * len);
      g.addColorStop(0, 'rgba(4,9,16,' + a0.toFixed(3) + ')');
      g.addColorStop(0.40, 'rgba(4,9,16,' + (a0 * 0.58).toFixed(3) + ')');
      g.addColorStop(1, 'rgba(4,9,16,0)');
      cx.fillStyle = g;
      cx.beginPath();
      cx.moveTo(qx * halfFoot, qy * halfFoot);
      cx.lineTo(ex * len + qx * halfTip, ey * len + qy * halfTip);
      cx.lineTo(ex * len - qx * halfTip, ey * len - qy * halfTip);
      cx.lineTo(-qx * halfFoot, -qy * halfFoot);
      cx.closePath(); cx.fill();
    }
    var hf = w * 0.46, ht = w * 0.31;
    castLayer(hf * 1.34, ht * 1.42, 0.15 * strength);
    castLayer(hf * 1.14, ht * 1.18, 0.21 * strength);
    castLayer(hf * 0.97, ht * 0.99, 0.29 * strength);
    castLayer(hf * 0.79, ht * 0.80, 0.34 * strength);

    /* THE SEAM, hard and narrow, right at the foot. Drawn last so the darkest
     * value in the whole contact is the line where the object meets the floor,
     * which is the one place a contact shadow is genuinely near black. */
    cx.save(); cx.scale(1, 0.47);
    cx.fillStyle = 'rgba(4,8,14,' + (0.80 * strength).toFixed(3) + ')';
    cx.beginPath(); cx.arc(0, 0, seamW, 0, Math.PI * 2); cx.fill();
    cx.restore();
    cx.restore();

    /* OPTIONAL LIT GROUND, for a frame that really does stand on near-black.
     * A hard-edged sliver up-light of the foot at low alpha in source-over.
     * It is off unless a slide asks, and it can never be additive. */
    if (o.lit) {
      var lk = o.litK == null ? 0.26 : o.litK;
      cx.save();
      cx.translate(fx - d[0] * (w * 0.42), fy - d[1] * (w * 0.42));
      cx.scale(1, squash * 0.62);
      cx.globalAlpha = lk;
      cx.fillStyle = o.lit;
      cx.beginPath(); cx.arc(0, 0, w * 0.40, 0, Math.PI * 2); cx.fill();
      cx.restore();
    }

    /* The rects a slide should DECLARE for this contact: one ON the cast, one
     * on clean ground the same distance the other side of the foot. They are
     * returned rather than guessed, and they are still re-measured off the
     * render with scripts/contact_probe.py before ship. */
    var mid = len * 0.34;
    var sx = fx + d[0] * mid, sy = fy + d[1] * mid * squash;
    var gx = fx - d[0] * mid, gy = fy - d[1] * mid * squash;
    return {
      shadow: [Math.round(sx - 13), Math.round(sy - 5), 26, 10],
      ground: [Math.round(gx - 13), Math.round(gy - 5), 26, 10]
    };
  };

  /* -------------------------------------------------------------- airframe */

  /* One rivet, with a lit upper lip and a lee lower lip. Never a pattern fill
   * and never a flat dot: a rivet without a lip is the flat-lazy region the
   * zoom test exists to catch. */
  AKHOLD.rivet = function (cx, x, y, r, lit, lee) {
    cx.save();
    cx.beginPath(); cx.arc(x, y, r, 0, Math.PI * 2);
    cx.fillStyle = lee; cx.fill();
    cx.beginPath(); cx.arc(x - r * 0.22, y - r * 0.30, r * 0.62, 0, Math.PI * 2);
    cx.fillStyle = lit; cx.fill();
    cx.beginPath(); cx.arc(x + r * 0.30, y + r * 0.34, r * 0.44, 0, Math.PI * 2);
    cx.fillStyle = 'rgba(5,10,18,0.42)'; cx.fill();
    cx.restore();
  };

  /* A run of rivets along a segment, consulting a reserve mask so the loop
   * never draws into a line box. Returns the centres it actually used, so a
   * caller can hand them to window.__akAssert and let the FRAME do the
   * counting. An `actual` derived from the loop bound agrees with the type and
   * disagrees with the picture, which is the one disagreement that matters. */
  AKHOLD.rivetRun = function (cx, x0, y0, x1, y1, pitch, r, lit, lee, mask) {
    var n = Math.max(1, Math.floor(Math.hypot(x1 - x0, y1 - y0) / pitch));
    var pts = [];
    for (var i = 0; i <= n; i++) {
      var t = i / n, x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t;
      if (mask && mask(x, y) < 0.5) continue;
      AKHOLD.rivet(cx, x, y, r, lit, lee);
      pts.push([x, y]);
    }
    return pts;
  };

  /* ------------------------------------------------------------ the tube
   *
   * A cargo bay is a TUBE, and the thing that makes it read as one in a single
   * frame is a run of frame rings receding to a vanishing point. The first
   * build of this deck drew ribs as straight lines across a black field and
   * they read as rules floating on nothing, which is the flat-lazy region the
   * zoom test exists to catch. A ring has a lit face, a lee face and a real
   * silhouette, and eight of them nested give occlusion and a scale gradient
   * for free, which is two depth cues out of one primitive.
   *
   * `ring` returns the path of one frame station as a rounded rectangle scaled
   * about the vanishing point, so a caller can fill it, clip to it, or walk it.
   */
  AKHOLD.ringRect = function (vp, box, s) {
    var x = vp[0] + (box[0] - vp[0]) * s;
    var y = vp[1] + (box[1] - vp[1]) * s;
    return [x, y, box[2] * s, box[3] * s];
  };

  AKHOLD.ringPath = function (cx, r, rad) {
    var x = r[0], y = r[1], w = r[2], h = r[3];
    var k = Math.min(rad == null ? 92 : rad, w / 2, h / 2);
    cx.beginPath();
    cx.moveTo(x + k, y);
    cx.lineTo(x + w - k, y);
    cx.quadraticCurveTo(x + w, y, x + w, y + k);
    cx.lineTo(x + w, y + h - k);
    cx.quadraticCurveTo(x + w, y + h, x + w - k, y + h);
    cx.lineTo(x + k, y + h);
    cx.quadraticCurveTo(x, y + h, x, y + h - k);
    cx.lineTo(x, y + k);
    cx.quadraticCurveTo(x, y, x + k, y);
    cx.closePath();
  };

  /* One frame station drawn as a real structural member, with the key on its
   * upper right and the lee on its lower left, per the deck's one light. */
  AKHOLD.ringMember = function (cx, vp, box, s, depth, pal) {
    var outer = AKHOLD.ringRect(vp, box, s);
    var inner = AKHOLD.ringRect(vp, [box[0] + depth, box[1] + depth,
                                     box[2] - depth * 2, box[3] - depth * 2], s);
    cx.save();
    AKHOLD.ringPath(cx, outer, 92 * s);
    AKHOLD.ringPath(cx, inner, 82 * s);
    cx.fillStyle = pal.lee;
    cx.fill('evenodd');
    /* the lit upper-right arc of the member, which is what says az 76 */
    cx.beginPath();
    cx.ellipse(outer[0] + outer[2] / 2, outer[1] + outer[3] / 2,
               outer[2] / 2, outer[3] / 2, 0, -Math.PI * 0.62, Math.PI * 0.10);
    cx.lineWidth = Math.max(1, depth * s * 0.44);
    cx.strokeStyle = pal.lit;
    cx.stroke();
    cx.restore();
    return { outer: outer, inner: inner };
  };

  /* --------------------------------------------------------------- streak
   *
   * The world seen through the cargo door is smeared along the flight vector.
   * A box convolution on an offscreen canvas, applied ONCE, never inside a
   * loop. Sharp airframe plus smeared world is the deck's depth signature and
   * it says MOVING with no arrow and no speed line.
   */
  AKHOLD.streak = function (src, px) {
    var w = src.width, h = src.height;
    var out = document.createElement('canvas');
    out.width = w; out.height = h;
    var oc = out.getContext('2d');
    var n = Math.max(2, Math.round(px));
    oc.globalAlpha = 1 / n;
    for (var i = 0; i < n; i++) oc.drawImage(src, (i - n / 2) * 2, 0);
    oc.globalAlpha = 1;
    return out;
  };

  /* ---------------------------------------------------------------- wedge
   *
   * THE LIT WEDGE. One hard, door shaped parallelogram of low September sun on
   * the floor. It is the deck's key and its clock, and because it is a hard
   * edged shape screened across the whole floor rather than a radial pool under
   * an object, the failure mode above is impossible here by construction.
   */
  AKHOLD.wedge = function (cx, poly, o) {
    o = o || {};
    var a = o.alpha == null ? 0.34 : o.alpha;
    cx.save();
    cx.beginPath();
    cx.moveTo(poly[0][0], poly[0][1]);
    for (var i = 1; i < poly.length; i++) cx.lineTo(poly[i][0], poly[i][1]);
    cx.closePath();
    cx.clip();
    var g = cx.createLinearGradient(o.gx0 || poly[0][0], o.gy0 || poly[0][1],
                                    o.gx1 || poly[2][0], o.gy1 || poly[2][1]);
    g.addColorStop(0, 'rgba(175,198,216,' + a + ')');
    g.addColorStop(1, 'rgba(175,198,216,' + (a * 0.42) + ')');
    cx.globalCompositeOperation = 'screen';
    cx.fillStyle = g;
    cx.fillRect(0, 0, 1080, 1350);
    cx.restore();
  };

  /* Dust inside a polygon only, seeded, with the centres returned so a caller
   * can declare the count. */
  AKHOLD.motes = function (cx, poly, n, seed, colour) {
    var rng = (global.AK && AK.rng) ? AK.rng(seed) : (function (s) {
      return function () { s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; };
    })(seed);
    var xs = poly.map(function (p) { return p[0]; }), ys = poly.map(function (p) { return p[1]; });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
    var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var pts = [], guard = 0;
    while (pts.length < n && guard++ < n * 80) {
      var x = x0 + rng() * (x1 - x0), y = y0 + rng() * (y1 - y0);
      if (!AKHOLD.inPoly(x, y, poly)) continue;
      /* A centre off the canvas paints nothing a reader can count, so it is
       * never declared. qa.py counts the FRAME, and the frame is 1080 x 1350. */
      if (x < 4 || x > 1076 || y < 4 || y > 1346) continue;
      pts.push([x, y]);
    }
    cx.save();
    cx.globalCompositeOperation = 'screen';
    for (var i = 0; i < pts.length; i++) {
      var r = 0.8 + (i % 5) * 0.14;
      cx.fillStyle = colour || 'rgba(215,228,238,0.42)';
      cx.beginPath(); cx.arc(pts[i][0], pts[i][1], r, 0, Math.PI * 2); cx.fill();
    }
    cx.restore();
    return pts;
  };

  AKHOLD.inPoly = function (x, y, poly) {
    var inside = false;
    for (var i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      var xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside;
    }
    return inside;
  };

  /* ---------------------------------------------------------------- grade
   *
   * THE DECK'S FILM GRADE, WRITTEN ONCE SO THE UNITS MISTAKE HAPPENS ONCE.
   *
   * `exposure` is in STOPS and not a multiplier. 0 is unchanged, +1 is twice as
   * bright, and the house dark-arctic grade lives in -0.15 to +0.06. A value
   * near 1.0 is the units error that shipped on 2026-08-08 and 2026-08-12 and
   * that this deck's first render reproduced on slide 01 before anything else
   * had been built, which is the cheapest possible place to find it.
   *
   * `lift` and `gain` are TOP-LEVEL three element ARRAYS, never hex strings.
   * `bloom` takes threshold, strength and radius. `grain` takes amount, size
   * and seed. A wrong shape throws rather than coercing, because a grade that
   * coerces writes NaN into every pixel and reports errors 0.
   *
   * IGN dither is ON for every frame in this deck without exception. The hold
   * is a large soft near-black gradient on all nine frames and 8 bit banding
   * across it is the one defect that survives LinkedIn recompression.
   */
  AKHOLD.grade = function (cx, over) {
    if (!(global.AKPOST && AKPOST.grade)) return;
    var o = {
      exposure: 0.03,
      saturation: 1.04,
      contrast: 1.08,
      filmic: true,
      lift: [0.010, 0.015, 0.026],
      gain: [1.016, 1.000, 0.972],
      bloom: { threshold: 0.74, strength: 0.26, radius: 8 },
      grain: { amount: 0.045, size: 2, seed: 20260914 },
      dither: true,
      sharpen: 0.30
    };
    if (over) for (var k in over) if (Object.prototype.hasOwnProperty.call(over, k)) o[k] = over[k];
    AKPOST.grade(cx, o);
  };

  /* ----------------------------------------------------------------- ramp
   * One call, one palette, so warm light and cool shadow are numerical rather
   * than guessed. keyHue 44 is the low sun, ambientHue 222 the aluminium bounce.
   */
  AKHOLD.ramp = function (base, steps) {
    if (global.AKC && AKC.ramp) {
      return AKC.ramp(base, { steps: steps || 7, keyHue: 44, ambientHue: 222, drift: 0.06 });
    }
    return [base];
  };

  global.AKHOLD = AKHOLD;
})(window);
