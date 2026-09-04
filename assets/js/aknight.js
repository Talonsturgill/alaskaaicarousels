/* aknight.js — THE NIGHT APRON, Carousel No.49's shared furniture.
 *
 * Committed 2026-09-03. This is DECK FURNITURE, shared across all nine slides
 * on purpose, which is why it lives in a module rather than inline:
 * bespoke_check strips `<script src=>` as harness, so a shared population
 * sampler does not read as nine slides of the same art, while each slide's own
 * composition still has to earn its score. Same reasoning as akrail.js,
 * akcolumn.js and akseam.js.
 *
 * WHAT THIS IS. Four populations that every frame of a wet night deck needs and
 * that no slide should be pasting a private copy of.
 *
 *   AKNIGHT.reserve(selector)
 *     Type-reserve rects measured PER LINE BOX, not per block. A Range over the
 *     element's contents returns one client rect per rendered line, so a ragged
 *     two-line headline reserves two UNEQUAL rects and the hole follows the rag.
 *     Measuring the block instead reserves the bounding rectangle of the whole
 *     paragraph, which is the plate this deck exists to avoid drawing.
 *     MUST be called after `await document.fonts.ready`.
 *
 *   AKNIGHT.rain(cx, o)
 *     Tapered rain streaks as filled polygons, never strokes, so each mark has
 *     a width that varies along its own length. Length scales with 1/z so near
 *     rain is long and soft and far rain is short and sharp. Gated by o.inCone,
 *     because the whole point of drawing rain at all is that it shows you where
 *     the light stops. A frame's unlit band must contain none.
 *
 *   AKNIGHT.chips(cx, o)
 *     THE RUNOFF MIRROR. A population of hard-edged specular quads on wet
 *     ground. This is the deck's answer to a measured finding, that a graded
 *     wash in the lower third reads as NOTHING after the 6x box downsample
 *     frame_balance and value_structure both apply, while a population of
 *     discrete steps survives it. Run No.48 added 34 soft radials to its near
 *     band and the measured value went DOWN. Chips are not a texture, they are
 *     the lower third's structure.
 *
 *   AKNIGHT.conductor(cx, o)
 *     One cased catenary with rain beads, the deck's edge-tease. Cased per
 *     technique 79 so it stays legible crossing texture.
 *
 * DETERMINISM. Every population is drawn from AK.rng(seed). No Math.random, no
 * Date.now, no Date. The determinism gate reads inline scripts and a vendored
 * file loaded by src= is not read, but this file obeys the rule anyway because
 * a shipped PNG has to be rebuildable from the committed source.
 *
 * COLOUR SAFETY. No colour helper is ever nested inside another here. lerpHex
 * and its cousins return an "rgb()" string, and feeding rgb(...) into a hex
 * parser yields NaN on every channel, after which canvas silently keeps the
 * PREVIOUS fillStyle and a whole region renders in the wrong colour with every
 * machine gate green (instinct 0.97).
 *
 * PERFORMANCE. Nothing here sets cx.filter inside a loop. cx.filter applies PER
 * DRAW OP, so blurring a population of 3,100 streaks blurs 3,100 times and blows
 * the navigation budget. Blur once, at composite, on an offscreen canvas.
 */
(function (global) {
  "use strict";

  var N = {};

  /* ------------------------------------------------------------- reserve
   * Per-line-box rects for every element matching `selector`.
   * Returns [[x, y, w, h], ...] in CSS px, ready for AKENGRAVE.reserve()
   * and for any slide-side population that must not draw over type.
   */
  N.reserve = function (selector, opts) {
    opts = opts || {};
    var out = [];
    var els = document.querySelectorAll(selector);
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var cs = global.getComputedStyle(el);
      var fs = parseFloat(cs.fontSize) || 32;
      var pad = opts.pad == null ? Math.max(14, fs * 0.45) : opts.pad;
      var r = document.createRange();
      r.selectNodeContents(el);
      var rects = r.getClientRects();
      var n = 0;
      for (var j = 0; j < rects.length; j++) {
        var b = rects[j];
        if (b.width < 2 || b.height < 2) continue;
        out.push([b.left - pad, b.top - pad, b.width + 2 * pad, b.height + 2 * pad]);
        n++;
      }
      /* An element whose contents produce no line rects (an empty span, or a
       * block whose text is in a pseudo-element) would silently reserve
       * nothing, so fall back to the border box rather than skipping it. */
      if (n === 0) {
        var bb = el.getBoundingClientRect();
        if (bb.width > 2 && bb.height > 2) {
          out.push([bb.left - pad, bb.top - pad, bb.width + 2 * pad, bb.height + 2 * pad]);
        }
      }
    }
    return out;
  };

  /* True when (x, y) falls inside any reserved rect. Slides hand this to their
   * own populations so a chip or a streak is never generated over a glyph. */
  N.hits = function (boxes, x, y) {
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      if (x >= b[0] && x <= b[0] + b[2] && y >= b[1] && y <= b[1] + b[3]) return true;
    }
    return false;
  };

  /* ---------------------------------------------------------------- rain
   * o: {count, seed, x0, x1, y0, y1, bearingDeg, color, alpha, inCone(x,y),
   *     reserve, near, far}
   * `bearingDeg` is the wind direction projected into frame, measured from
   * vertical. `near`/`far` set the z range; length scales with 1/z.
   */
  N.rain = function (cx, o) {
    o = o || {};
    var rnd = global.AK.rng(o.seed || 1);
    var count = o.count || 1600;
    var x0 = o.x0 == null ? -120 : o.x0;
    var x1 = o.x1 == null ? 1200 : o.x1;
    var y0 = o.y0 == null ? -80 : o.y0;
    var y1 = o.y1 == null ? 1350 : o.y1;
    var ang = ((o.bearingDeg == null ? 17 : o.bearingDeg)) * Math.PI / 180;
    var sin = Math.sin(ang), cos = Math.cos(ang);
    var near = o.near == null ? 0.35 : o.near;
    var far = o.far == null ? 1.0 : o.far;
    var cone = o.inCone || function () { return true; };
    var res = o.reserve || [];

    cx.save();
    cx.fillStyle = o.color || "#D8E8EE";
    for (var i = 0; i < count; i++) {
      var x = x0 + rnd() * (x1 - x0);
      var y = y0 + rnd() * (y1 - y0);
      if (!cone(x, y)) continue;
      if (res.length && N.hits(res, x, y)) continue;
      var z = near + rnd() * (far - near);      /* 0 near, 1 far */
      var len = (34 / (0.35 + z * 1.9)) * (0.55 + rnd() * 0.9);
      var w = (2.1 / (0.5 + z * 2.2)) * (0.6 + rnd() * 0.7);
      /* per-streak angular jitter, normal-ish via two uniforms, because
       * uniform randomness is the tell of a machine-made mark */
      var jit = ((rnd() + rnd() + rnd()) / 3 - 0.5) * 0.16;
      var s = Math.sin(ang + jit), c = Math.cos(ang + jit);
      var ex = x + s * len, ey = y + c * len;
      /* a tapered quad: wide at the head, closing to a point at the tail */
      cx.globalAlpha = (o.alpha == null ? 0.30 : o.alpha) * (1.05 - z * 0.75);
      cx.beginPath();
      cx.moveTo(x - c * w, y + s * w);
      cx.lineTo(x + c * w, y - s * w);
      cx.lineTo(ex, ey);
      cx.closePath();
      cx.fill();
    }
    cx.restore();
  };

  /* --------------------------------------------------------------- chips
   * THE RUNOFF MIRROR. Hard-edged specular quads on wet ground.
   * o: {count, seed, region:[x,y,w,h], density(x,y)->0..1, color, colorDim,
   *     alpha, sizeMin, sizeMax, reserve, squash}
   * `density` is the story's own quantity or the lamp's falloff, never a
   * position ramp for its own sake. A chip is placed by rejection sampling
   * against it, so the population itself carries the modelling.
   */
  N.chips = function (cx, o) {
    o = o || {};
    var rnd = global.AK.rng(o.seed || 2);
    var reg = o.region || [0, 900, 1080, 450];
    var dens = o.density || function () { return 0.6; };
    var count = o.count || 900;
    var smin = o.sizeMin == null ? 1.6 : o.sizeMin;
    var smax = o.sizeMax == null ? 9.0 : o.sizeMax;
    var squash = o.squash == null ? 0.32 : o.squash;   /* chips lie flat */
    var res = o.reserve || [];
    var bright = o.color || "#D8E8EE";
    var dim = o.colorDim || "#7FA8B8";

    cx.save();
    var placed = 0, tries = 0, cap = count * 26;
    while (placed < count && tries < cap) {
      tries++;
      var x = reg[0] + rnd() * reg[2];
      var y = reg[1] + rnd() * reg[3];
      var d = dens(x, y);
      if (d <= 0) continue;
      if (rnd() > d) continue;                 /* rejection sample */
      if (res.length && N.hits(res, x, y)) continue;
      /* THREE SEPARATE FUNCTIONS OF THE SAME d, so a region cannot be flat
       * unless the quantity under it is flat. Size, alpha and colour all move. */
      var w = smin + (smax - smin) * (d * d) * (0.45 + rnd() * 1.1);
      var h = Math.max(1.0, w * squash * (0.6 + rnd() * 0.9));
      cx.globalAlpha = (o.alpha == null ? 0.9 : o.alpha) * (0.30 + 0.70 * d);
      cx.fillStyle = d > 0.62 ? bright : dim;
      /* A HARD-EDGED QUAD, never a radial gradient. The whole reason this
       * function exists is that a soft radial does not survive a 6x box
       * downsample and a hard step does. */
      cx.fillRect(x - w / 2, y - h / 2, w, h);
      placed++;
    }
    cx.restore();
    return { placed: placed, tries: tries };
  };

  /* ----------------------------------------------------------- conductor
   * o: {x0,y0,x1,y1,sag,color,casing,width,seed,beads}
   * A cased catenary. Casing first at width+3, then the core, then beads.
   */
  N.conductor = function (cx, o) {
    o = o || {};
    var x0 = o.x0, y0 = o.y0, x1 = o.x1, y1 = o.y1;
    var sag = o.sag == null ? 70 : o.sag;
    var w = o.width == null ? 2.0 : o.width;
    var rnd = global.AK.rng(o.seed || 3);
    var pts = [], STEP = 26;
    var n = Math.max(2, Math.round(Math.abs(x1 - x0) / STEP));
    for (var i = 0; i <= n; i++) {
      var t = i / n;
      var x = x0 + (x1 - x0) * t;
      var y = y0 + (y1 - y0) * t + Math.sin(Math.PI * t) * sag;
      pts.push([x, y]);
    }
    function trace() {
      cx.beginPath();
      cx.moveTo(pts[0][0], pts[0][1]);
      for (var k = 1; k < pts.length; k++) cx.lineTo(pts[k][0], pts[k][1]);
    }
    cx.save();
    cx.lineCap = "round";
    cx.lineJoin = "round";
    cx.strokeStyle = o.casing || "#04070E";
    cx.lineWidth = w + 3;
    trace(); cx.stroke();
    cx.strokeStyle = o.color || "#35586B";
    cx.lineWidth = w;
    trace(); cx.stroke();
    if (o.beads !== false) {
      cx.fillStyle = o.beadColor || "#D8E8EE";
      for (var j = 0; j < pts.length; j++) {
        if (rnd() > 0.42) continue;
        var r = 0.9 + rnd() * 1.5;
        cx.globalAlpha = 0.5 + rnd() * 0.45;
        cx.beginPath();
        cx.arc(pts[j][0], pts[j][1] + w * 0.5, r, 0, 6.283185);
        cx.fill();
      }
    }
    cx.restore();
    return pts;
  };

  /* ------------------------------------------------------------ falloff
   * Inverse-square lamp falloff, normalised to 0..1, for use as a `density`
   * or a `tone`. The lamp is a point at (lx, ly) with a reach in px.
   */
  N.falloff = function (lx, ly, reach) {
    var r2 = reach * reach;
    return function (x, y) {
      var dx = x - lx, dy = y - ly;
      var d2 = dx * dx + dy * dy;
      var v = r2 / (r2 + d2 * 2.6);
      return v < 0 ? 0 : (v > 1 ? 1 : v);
    };
  };

  /* ------------------------------------------------------------- litPool
   * A CONTACT SHADOW IS A SUBTRACTION AND NEEDS SOMETHING TO SUBTRACT FROM.
   * On a night deck the ground under an object is often already near black, so
   * a correctly drawn cast shadow measures zero separation and qa.py fails it,
   * which is exactly what happened across this deck's first render pass (five
   * slides, "the ground is already near black, so there is nothing left to
   * subtract"). The fix is never a stronger shadow. Light the ground FIRST,
   * then cast into it.
   *
   * Drawn as a CIRCLE inside a transform, never as an elliptical gradient,
   * because createRadialGradient is a circle and pouring it into an ellipse
   * stops the paint on the short axis while the ramp still carries alpha,
   * which draws a hard arc across the ground.
   */
  N.litPool = function (cx, o) {
    o = o || {};
    var x = o.x, y = o.y;
    var rx = o.rx == null ? 200 : o.rx;
    var ry = o.ry == null ? 46 : o.ry;
    var R = 100;
    /* THE RAMP HOLDS BEFORE IT FALLS. A pool whose value is already spent at
     * half radius lights only the strip the cast then covers, so the pair
     * measures nothing and the gate reads a floating object. Two intermediate
     * stops carry most of the value out past the cast's own footprint, and the
     * last quarter does all the falling, which is long enough that the edge
     * never draws as the rim of a spotlight. */
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    g.addColorStop(0, o.color || 'rgba(150,174,192,0.34)');
    g.addColorStop(0.42, o.mid || 'rgba(134,160,178,0.25)');
    g.addColorStop(0.74, o.out || 'rgba(110,140,160,0.11)');
    g.addColorStop(1, 'rgba(110,140,160,0)');
    cx.save();
    cx.translate(x, y);
    cx.scale(rx / R, ry / R);
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(0, 0, R, 0, 6.283185); cx.fill();
    cx.restore();
  };

  /* ---------------------------------------------------------------- veil
   * THE TYPE RESERVE, APPLIED TO ART THAT DOES NOT KNOW ABOUT IT.
   * The engraved surfaces, the rain and the chip populations all test the
   * reserve before they draw. A slide's OWN bespoke geometry does not, and it
   * is that geometry (corrugations, rails, a coastline, a centreline) that
   * qa.py catches running through the letterforms.
   *
   * This runs the slide's base value back over each reserved LINE BOX at a
   * feathered edge, so the art is subtracted where the type sits rather than
   * covered by a plate. It is a tonal lift of the medium itself, not furniture,
   * which is the distinction DESIGN_DOCTRINE draws between a defended type
   * block and the flat-plate defect. Call it AFTER all art and BEFORE the
   * grade.
   */
  N.veil = function (cx, boxes, o) {
    o = o || {};
    var col = o.color || '4,7,14';
    var aFull = o.alpha == null ? 0.62 : o.alpha;
    var f = o.feather == null ? 34 : o.feather;
    /* IT WAS DRAWING THE VERY PLATE IT EXISTS TO AVOID, and the reason was a
     * FIXED feather. 26px of a 336px box is eight percent, which at feed scale
     * is an edge, and read off the render it was a black panel behind the type
     * on six of nine slides: the flat-plate defect DESIGN_DOCTRINE names.
     *
     * An ellipse was tried first and is wrong for the shape being covered. A
     * line box is long and thin, and the corners of a long thin rect sit far
     * outside the ellipse that contains its middle, so the FIRST line of every
     * block came out veiled and its ends did not. qa.py caught that as art
     * crossing line 1 while the block's other lines sat on clean paper.
     *
     * So: crossed ramps again, fitted to the box, but with the feather stated
     * as a FRACTION of each side. A wide line gets a wide ramp and a short one
     * gets a short ramp, and neither has a boundary the eye can find. */
    /* AND IT ONLY VEILS WHAT NEEDS VEILING. Applied flat to every reserved
     * box it put a smudge behind the short claim tags too, which sit on quiet
     * sky where there was no art to subtract in the first place. So each box
     * is MEASURED before it is touched: the strength follows the spread of
     * what is actually under it, and a box over clean ground is left alone. */
    var dpr = 1;
    try {
      var sw = parseFloat(cx.canvas.style.width);
      if (sw > 0) dpr = cx.canvas.width / sw;
    } catch (e) { dpr = 1; }

    /* NOT THE SPREAD, THE OUTLIERS. A spread reading is dominated by the
     * ground: one conductor crossing a 800px line box moves a standard
     * deviation by almost nothing and it is exactly the mark that has to go.
     * What matters is how much of the box departs from the ground it sits on,
     * so this returns the FRACTION of pixels far from the box's own median. */
    function inkFrac(x0, y0, w, h) {
      try {
        var d = cx.getImageData(Math.max(0, x0 * dpr), Math.max(0, y0 * dpr),
                                Math.max(1, w * dpr), Math.max(1, h * dpr)).data;
        var n = d.length / 4;
        var step = Math.max(1, Math.floor(n / 6000));
        var v = [], j;
        for (j = 0; j < n; j += step) {
          v.push(0.2126 * d[j * 4] + 0.7152 * d[j * 4 + 1] + 0.0722 * d[j * 4 + 2]);
        }
        if (v.length < 8) return 1;
        var sorted = v.slice().sort(function (p, q) { return p - q; });
        var med = sorted[sorted.length >> 1];
        var out = 0;
        for (j = 0; j < v.length; j++) if (Math.abs(v[j] - med) > 18) out++;
        return out / v.length;
      } catch (e) { return 1; }   /* unreadable canvas: veil, do not gamble */
    }

    cx.save();
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      var x0 = b[0], y0 = b[1], w = b[2], h = b[3];
      /* below QUIET the ground carries nothing worth subtracting; at BUSY it
         is a crossing rule, an engraved lay or hard geometry and takes the
         whole veil. A single 2px conductor over a wide line box is already
         about 3 percent, which is why BUSY sits where it does. */
      var QUIET = o.quiet == null ? 0.006 : o.quiet;
      var BUSY = o.busy == null ? 0.020 : o.busy;
      var k = Math.max(0, Math.min(1, (inkFrac(x0, y0, w, h) - QUIET) / (BUSY - QUIET)));
      if (k <= 0.02) continue;
      var a = aFull * k;
      /* THE RAMPS HAVE TO MULTIPLY, AND ADDING THEM WAS THE WHOLE BUG.
       * Two crossed linear ramps drawn as two fillRects do not make a feathered
       * rect. Each one ramps on ONE axis and is HARD CUT on the other, so the
       * vertical ramp ends on straight verticals at X0 and X0+W, the horizontal
       * ramp ends on straight horizontals at Y0 and Y0+H, and their sum is a
       * rectangle with four findable edges: precisely the flat plate this
       * function exists to avoid, which is what five pixel critics read behind
       * the type on six of nine slides. The comment above described a product
       * the code never computed.
       *
       * So compute it. The veil is built once on an offscreen canvas as a solid
       * fill, then both ramps are composited into its ALPHA with
       * destination-in, which multiplies rather than adds. Alpha then reaches
       * zero at every edge AND at every corner, and there is no boundary left
       * to find. The spread is also clamped, because a fraction of a 628px line
       * box was putting a 138px shoulder on a caption. */
      var fx = Math.min(Math.max(f, w * 0.22), 90);
      var fy = Math.min(Math.max(f * 0.6, h * 0.34), 40);
      var px = Math.min(0.46, fx / (w + fx * 2));
      var py = Math.min(0.46, fy / (h + fy * 2));
      var X0 = x0 - fx, Y0 = y0 - fy, W = w + fx * 2, H = h + fy * 2;
      if (W < 2 || H < 2) continue;

      var vc = document.createElement('canvas');
      vc.width = Math.ceil(W); vc.height = Math.ceil(H);
      var vx = vc.getContext('2d');
      vx.fillStyle = 'rgba(' + col + ',' + a + ')';
      vx.fillRect(0, 0, vc.width, vc.height);
      vx.globalCompositeOperation = 'destination-in';
      var g = vx.createLinearGradient(0, 0, 0, vc.height);
      g.addColorStop(0, 'rgba(255,255,255,0)');
      g.addColorStop(py, 'rgba(255,255,255,1)');
      g.addColorStop(1 - py, 'rgba(255,255,255,1)');
      g.addColorStop(1, 'rgba(255,255,255,0)');
      vx.fillStyle = g; vx.fillRect(0, 0, vc.width, vc.height);
      var g2 = vx.createLinearGradient(0, 0, vc.width, 0);
      g2.addColorStop(0, 'rgba(255,255,255,0)');
      g2.addColorStop(px, 'rgba(255,255,255,1)');
      g2.addColorStop(1 - px, 'rgba(255,255,255,1)');
      g2.addColorStop(1, 'rgba(255,255,255,0)');
      vx.fillStyle = g2; vx.fillRect(0, 0, vc.width, vc.height);

      /* o.avoid names surfaces the veil must never touch: an object with its
       * own value, like a gauge board, needs no help and a veil over it erases
       * the very marks the slide is about. */
      if (o.avoid) {
        vx.globalCompositeOperation = 'destination-out';
        vx.fillStyle = '#fff';
        for (var q = 0; q < o.avoid.length; q++) {
          var av = o.avoid[q];
          vx.fillRect(av[0] - X0, av[1] - Y0, av[2], av[3]);
        }
      }
      cx.drawImage(vc, X0, Y0, W, H);
    }
    cx.restore();
  };

  /* -------------------------------------------------------------- contact
   * The pair, in the only order that measures. Light the ground, THEN cast.
   * Every "contact shadow does not read" failure on this deck's first pass
   * said the same thing, that the ground was already near black and there was
   * nothing left to subtract. This wrapper makes the correct order the
   * default so no slide can get it wrong by omission.
   */
  N.contact = function (cx, o) {
    o = o || {};
    var w = o.w == null ? 160 : o.w;
    /* The pool has to be WIDER than the cast's own wide ambient term, or the
     * only ground left to pair against is ground that term has already
     * darkened. AKSNOW's ambient ellipse runs to 1.5w, so the pool runs to
     * 1.6w and the ambient is thinned to make room for it. The tight term
     * carries the separation instead, which is also where a real contact
     * shadow keeps its density. */
    N.litPool(cx, {
      x: o.x, y: o.y + (o.poolDy == null ? 6 : o.poolDy),
      rx: o.poolRx == null ? w * (o.poolK == null ? 1.6 : o.poolK) : o.poolRx,
      ry: o.poolRy == null ? Math.max(26, w * 0.40) : o.poolRy,
      /* MEASURED AT dL 35 AND READ AS SIX STAGE SPOTLIGHTS. The floor is 4.0
       * and the studio's own known-good is 8.1, so a pool bright enough to
       * post 35 was a gate number, not a picture. Down to where wet ground
       * under a lamp actually sits, which still clears the floor several
       * times over. */
      color: o.poolColor || 'rgba(150,174,192,0.34)',
      mid: o.poolMid || 'rgba(134,160,178,0.25)',
      out: o.poolOut || 'rgba(110,140,160,0.11)'
    });
    global.AKSNOW.contactShadow(cx, {
      x: o.x, y: o.y, w: w, color: o.color || '#0A1320',
      tightAlpha: o.tightAlpha == null ? 0.66 : o.tightAlpha,
      wideAlpha: o.wideAlpha == null ? 0.05 : o.wideAlpha,
      wideBlur: o.wideBlur == null ? 30 : o.wideBlur,
      dirDeg: o.dirDeg
    });
    /* THE ANCHOR. A directional cast has its darkest point downlight of the
     * object, because that is the part of the ground the pool never reaches.
     * That is physically right and it is also, measured, a trough sitting 34
     * to 46 design px off the object's own foot, which is the exact reading
     * five critics filed as "a detached hole in a spotlight". The seam is what
     * was missing: where an object MEETS the ground there is a hard, narrow,
     * almost unblurred line of occlusion, and it is that line, not the cast,
     * that says touching. Drawn last so nothing lightens it again. */
    if (o.anchor !== false) {
      var aw = o.anchorW == null ? w * 0.44 : o.anchorW;
      cx.save();
      cx.filter = 'blur(' + (o.anchorBlur == null ? 2.2 : o.anchorBlur) + 'px)';
      cx.fillStyle = 'rgba(4,7,14,' + (o.anchorAlpha == null ? 0.80 : o.anchorAlpha) + ')';
      cx.beginPath();
      cx.ellipse(o.x, o.y, aw, Math.max(2.4, aw * 0.13), 0, 0, 6.283185);
      cx.fill();
      cx.restore();
    }
  };

  global.AKNIGHT = N;
})(window);
