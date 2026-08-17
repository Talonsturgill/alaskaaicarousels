/* akstipple.js — WEIGHTED STIPPLE, the drawn-substrate bench.  (Alaska.Ai)
 * Committed 2026-08-16 for Carousel No. 35.
 *
 * WHAT THIS IS. A substrate that puts modelled marks across the WHOLE frame by
 * construction, where the mark population is a function of the story's own
 * quantity rather than of screen position.
 *
 * WHY IT EXISTS. "Artwork craft and genuine detail" has been the weakest scored
 * criterion in 8 of the 10 runs to 2026-08-15, mean 6.1, and the two obvious
 * remedies have both now been tried and measured. No.32 went to akengrave and
 * scored 8.08 overall; No.34 climbed to rung 1 of the rendered ladder, real GPU
 * PBR with volumetric fog and authored contact occlusion, and STILL scored 6.0 on
 * artwork craft. So the weakness is not the rung. What the criterion actually
 * measures is DESIGN_DOCTRINE section 5, the zoom test, craft in every region,
 * and a smooth physically-rendered material is beautiful and has no marks in it.
 * The deck's whole detail budget then lands in the annotation furniture, the
 * furniture concentrates where the labels are, and the labels are up top. That is
 * also, precisely, why `top-loaded composition` is the number one recurring
 * machine warn. The two findings are one finding.
 *
 * THE TECHNIQUE. Secord-style darkness-weighted stippling, done by rejection
 * sampling against a height field rather than by Lloyd relaxation, because
 * relaxation costs seconds per slide and the rejection sampler costs about 1.1
 * and neither is distinguishable at 1080 px once radius and alpha also vary.
 *
 * THE THREE-FUNCTION RULE, and it is the whole point. DENSITY, RADIUS and ALPHA
 * are three SEPARATE functions of the same height h. A region therefore cannot be
 * flat unless the story's quantity is flat there, and non-uniformity is
 * structural instead of applied. This is akhachure.js's diagnosis generalized:
 *
 *     our detail is uniform because our stipple and tooth fields are
 *     parameterised by POSITION, so a density falloff is a gradient laid over a
 *     texture that is otherwise the same everywhere.
 *
 * `height` IS REQUIRED AND HAS NO DEFAULT, for the same reason akhachure gives.
 * A default noise field would let a slide get the look without the data, which is
 * the exact failure this file exists to stop. Pass the story's own quantity.
 *
 * THE HEIGHT FIELD MUST BE SMOOTH. A slow plane plus at most two broad gaussian
 * lobes plus ONE fbm warp at about 0.10 amplitude. This is No.32's three-round
 * lesson carried across the bench: an engraved lay is the gradient of its form,
 * so a high-frequency form produces marbling rather than tone. Stipple is more
 * forgiving than engraving and not infinitely so; a field dominated by high
 * frequencies produces noise, not modelled light.
 *
 * THE RESERVE, and it is MANDATORY when type sits over the field. A substrate
 * that puts marks in every region puts marks through every letterform, and
 * qa.py's `art touching glyphs` check reads PIXELS, so it sees this where the
 * DOM-only collision walk cannot. Prototype P4 on 2026-08-16 FAILED the deck on
 * exactly this, 9 percent of the ring around a mono label being ink of the
 * glyphs' own value.
 *
 * The fix is NOT a scrim and NOT a plate. DESIGN_DOCTRINE section 3 says to earn
 * it with the art, routing quiet zones under text by composition, before reaching
 * for a scrim. So the sampler reads the DOM and suppresses itself inside every
 * element marked `data-reserve`. Two properties matter and both were learned by
 * failing:
 *
 *   1. MEASURE AFTER `document.fonts.ready`. A box measured before the webfont
 *      loads is the wrong box.
 *   2. RAMP THE SUPPRESSION, and ramp it WIDER than the hole. A hard 0-or-1 hole
 *      reads as a black rectangle at feed size, which is the very thing plates
 *      were supposed to avoid. Prototype P6 shipped that. A ramp merely EQUAL to
 *      the pad still read as an edge on No.35, so the two are separate numbers
 *      now: pad `max(14, fontSize * 0.45)` is the hole, ramp `pad * 1.8` is the
 *      band it fades across, and the fade is by true distance from the hole so
 *      corners round off instead of mitring.
 *   3. MEASURE THE INK, NOT THE DIV. `getBoundingClientRect` returns the layout
 *      box, so a 700 px block holding a 490 px line reserves 210 px of nothing
 *      and that nothing is VISIBLE. Three pixel critics on No.35 found exactly
 *      that, floating rectangles whose right edges aligned to no word on the
 *      frame. A Range over the element's contents returns one rect per LINE BOX,
 *      hugging the glyph run, so a two-line block of unequal lines reserves two
 *      unequal rects and the suppression follows the rag.
 *
 * EVERY OTHER ART LAYER MUST HONOUR THE RESERVE TOO. Prototype P5 respected it in
 * the stipple and ignored it in d3's borough strokes, and the strokes ran through
 * the body copy. `AKSTIPPLE.reserved(x, y)` is exported for exactly that.
 *
 * DETERMINISM. Seeded mulberry32 via AK.rng. No Math.random anywhere, and no
 * Date.now either, including profiling lines, because qa.py's scanner reads
 * inline scripts and warns on a clock read that never touches the artwork.
 *
 * USAGE (slide code):
 *   <script src="@@ASSETS@@/js/noise.js"></script>
 *   <script src="@@ASSETS@@/js/akstipple.js"></script>   // load AFTER noise.js
 *
 *   await document.fonts.ready;                 // MANDATORY before reserve()
 *   AKSTIPPLE.reserve('[data-reserve]');
 *   AKSTIPPLE.field(cx, {
 *     seed: 20260817,
 *     count: 48000,
 *     w: 1080, h: 1350,
 *     height: function (x, y) { return <0..1, the story's quantity>; },
 *     ramp:   ['#33475A','#4A5F73','#61798C','#8098AB','#A6BACB','#C9DCE6'],
 *     radius: function (q) { return 0.9 + 1.4 * q; },
 *     alpha:  function (q) { return 0.30 + 0.55 * q; },
 *     clip:   function (x, y) { return true; }        // optional
 *   });
 */
(function (global) {
  "use strict";

  var AKS = {};
  var RES = [];

  /* ---------------- the reserve ---------------- */

  /* Read the DOM and remember the padded box of every matching element.
   * Pad defaults to max(16, fontSize * 0.6), measured off the element's own
   * computed style, so a 25px mono label and a 104px display head get pads
   * appropriate to their stroke weight rather than one guessed constant. */
  /* MEASURE THE INK, NOT THE DIV. getBoundingClientRect returns the element's
   * LAYOUT box, so a 700px block holding a 490px line reserves 210px of nothing
   * and that nothing is visible: three pixel critics on No.35 found soft-edged
   * rectangles floating in the field with their right edges aligned to no word
   * on the frame. A Range over the element's contents returns one rect PER LINE
   * BOX, each hugging the actual glyph run, so the suppression follows the
   * ragged edge of the type and reads as a halo around the words instead of a
   * plate behind them. Falls back to the layout box if the Range yields nothing
   * (an empty element, or a node the browser will not measure). */
  function inkRects(el) {
    var out = [];
    try {
      var rg = document.createRange();
      rg.selectNodeContents(el);
      var list = rg.getClientRects();
      for (var i = 0; i < list.length; i++) {
        var r = list[i];
        if (r.width > 0.5 && r.height > 0.5) out.push(r);
      }
      rg.detach && rg.detach();
    } catch (e) { /* fall through to the layout box */ }
    return out;
  }

  /* Each entry is [ox0, oy0, ox1, oy1, ramp, hx0, hy0, hx1, hy1]:
   * the HARD box (ink plus pad, where nothing is drawn) and the OUTER box it
   * ramps out to. Keeping them separate is what let the falloff widen without
   * widening the hole. */
  AKS.reserve = function (selector, opts) {
    opts = opts || {};
    RES = [];
    var els = document.querySelectorAll(selector || "[data-reserve]");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var fs = parseFloat(getComputedStyle(el).fontSize) || 24;
      var pad = opts.pad != null ? opts.pad : Math.max(14, fs * 0.45);
      /* The ramp is the band the suppression fades across, and it is WIDER than
       * the pad on purpose. Prototype P6 shipped a ramp equal to the pad and it
       * still read as an edge at 432px; the falloff has to be long relative to
       * the hole to disappear. */
      var ramp = opts.ramp != null ? opts.ramp : pad * 1.8;
      var rects = inkRects(el);
      if (!rects.length) {
        var lb = el.getBoundingClientRect();
        if (lb.width <= 0 || lb.height <= 0) continue;
        rects = [lb];
      }
      for (var j = 0; j < rects.length; j++) {
        var r = rects[j];
        var hx0 = r.left - pad, hy0 = r.top - pad;
        var hx1 = r.right + pad, hy1 = r.bottom + pad;
        RES.push([hx0 - ramp, hy0 - ramp, hx1 + ramp, hy1 + ramp, ramp,
                  hx0, hy0, hx1, hy1]);
      }
    }
    return RES.length;
  };

  AKS.boxes = function () { return RES.slice(); };

  /* Suppression factor at a point. 1 outside every outer box, 0 inside the hard
   * box, and a rounded ramp between the two: the falloff is the point's true
   * distance from the hard box, so corners fade on an arc rather than on a
   * mitre and nothing in the field carries a straight suppressed edge. */
  AKS.factor = function (x, y) {
    var f = 1;
    for (var k = 0; k < RES.length; k++) {
      var b = RES[k];
      if (x <= b[0] || x >= b[2] || y <= b[1] || y >= b[3]) continue;
      var dx = b[5] - x; if (x - b[7] > dx) dx = x - b[7]; if (dx < 0) dx = 0;
      var dy = b[6] - y; if (y - b[8] > dy) dy = y - b[8]; if (dy < 0) dy = 0;
      var v = Math.sqrt(dx * dx + dy * dy) / b[4];
      if (v > 1) v = 1;
      if (v < f) f = v;
      if (f === 0) return 0;
    }
    return f;
  };

  /* Hard test, for art layers that cannot be faded, such as a stroked path.
   * Returns true anywhere the type owns the pixel. Tests the HARD box only, so
   * a stroke may still run through the outer ramp band where the stipple has
   * merely thinned. */
  AKS.reserved = function (x, y) {
    for (var k = 0; k < RES.length; k++) {
      var b = RES[k];
      if (x > b[5] && x < b[7] && y > b[6] && y < b[8]) return true;
    }
    return false;
  };

  /* ---------------- the field ---------------- */

  AKS.field = function (cx, o) {
    if (typeof o.height !== "function") {
      throw new Error("akstipple: `height` is required and has no default. " +
                      "Pass the story's own quantity.");
    }
    var W = o.w || 1080, H = o.h || 1350;
    var ramp = o.ramp || ["#33475A", "#4A5F73", "#61798C", "#8098AB", "#A6BACB", "#C9DCE6"];
    var radius = o.radius || function (q) { return 0.9 + 1.4 * q; };
    var alpha = o.alpha || function (q) { return 0.30 + 0.55 * q; };
    var clip = o.clip || null;
    var want = o.count || 48000;
    var rnd = global.AK.rng(o.seed || 1);
    var tries = 0, placed = 0, cap = want * 12;
    var n = ramp.length;

    while (placed < want && tries < cap) {
      tries++;
      var x = rnd() * W, y = rnd() * H;
      if (clip && !clip(x, y)) continue;
      var q = o.height(x, y);
      if (q <= 0) continue;
      q *= AKS.factor(x, y);
      if (q <= 0) continue;
      if (rnd() > q) continue;
      var band = Math.floor(q * n);
      if (band > n - 1) band = n - 1;
      cx.fillStyle = ramp[band];
      cx.globalAlpha = alpha(q);
      cx.beginPath();
      cx.arc(x, y, radius(q), 0, 6.283185307179586);
      cx.fill();
      placed++;
    }
    cx.globalAlpha = 1;
    return { placed: placed, tries: tries };
  };

  /* A lit pool. Paint this BEFORE the object that sits on it, then cut the
   * shadow INTO it. A darker shadow on a dark ground measured 1.2 L* on No.26
   * and four pixel critics read the object as floating; the separation has to
   * come from the ground being lit, not from the shadow being darker. */
  AKS.pool = function (cx, x, y, r, inner, outer) {
    var g = cx.createRadialGradient(x, y, Math.max(1, r * 0.04), x, y, r);
    g.addColorStop(0, inner);
    g.addColorStop(0.55, outer);
    g.addColorStop(1, "rgba(0,0,0,0)");
    cx.fillStyle = g;
    cx.fillRect(x - r, y - r, r * 2, r * 2);
  };

  global.AKSTIPPLE = AKS;
})(window);
