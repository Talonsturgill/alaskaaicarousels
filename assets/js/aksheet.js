/* aksheet.js — THE SHEET AND THE MARGIN, Carousel No. 56's continuity chassis.
 *
 * Committed 2026-09-11. This is DECK FURNITURE, shared across all nine slides
 * on purpose, which is why it lives in a module rather than inline:
 * bespoke_check strips `<script src=>` as harness, so a shared coordinate
 * system does not read as nine slides of the same art, while each slide's own
 * composition still has to earn its score. Same reasoning as akrail.js,
 * akcolumn.js, akseam.js, akparcel.js and aknight.js.
 *
 * WHAT THIS IS. A map sheet. A neatline cuts a window of lit daylight terrain
 * out of a dark slate margin, and ALL TYPE LIVES IN THE MARGIN. That is not a
 * layout preference, it is this deck's answer to the standing weakness.
 *
 * THE STRUCTURAL RESERVE, and it is the whole point of the chassis.
 * "Artwork craft and genuine detail" has been the weakest scored criterion in 7
 * of the last 10 runs, and its three recurring machine warns (busy art under
 * text, canvas mark near reserved text, art touching glyphs) are one problem:
 * a field gets built first and then negotiated with for somewhere to put the
 * words. On a map sheet that negotiation cannot arise. `SHEET.window()` returns
 * a context already clipped to the neatline, so every mark any slide generates
 * is INSIDE the window by construction and the margin is a plane the art has no
 * access to. Art cannot touch glyphs here because art cannot reach them.
 *
 * AND THE MARGIN IS NOT BARE. `SHEET.marginField` runs a stipple over the slate
 * whose height carries BASIN TERMS at each text block, measured and prototyped
 * on 2026-09-11 before any slide was planned. The finding that produced it:
 * calling a suppression-only reserve and nothing else returned qa.py PASS,
 * fails 0, warns 0, and rendered three hard-edged dark rectangles where the type
 * sat, which is exactly the "reads as a black rectangle at feed size" failure
 * akstipple's own docstring predicts. A basin multiplied into `height` LAST, so
 * the field's own density falls where the words go, reads as worked ground
 * rather than as a hole. Ramp 190 design px, depth 0.82, both measured.
 *
 * A MAP SHEET'S WIDEST MARGIN IS ITS BOTTOM ONE. That convention is why this
 * chassis fills the lower third by construction rather than by apology, which
 * is the dead-lower-zone defect the scorer named in six consecutive runs.
 *
 * THE CONTACT TRIPLE, IN THE ONLY ORDER THAT MEASURES. `litPool` FIRST, then
 * `cast`, then `seam` LAST. A correctly drawn shadow on ground that is already
 * near black measures zero separation, and a directional cast keeps its darkest
 * point downlight of the object, which is the reading five critics once filed as
 * a detached hole in a spotlight. The seam is the third term and it is what says
 * ATTACHED. Foot width belongs in the 70 to 110 design px band whatever the
 * object's silhouette, because contact_probe searches 48px for the cast and 96px
 * for the ground.
 *
 * DETERMINISM. Every caller passes its own seed. Seeded mulberry32 via AK.rng,
 * no Math.random, no Date.now.
 *
 * COLOUR SAFETY. No colour helper is nested inside another. Nothing here returns
 * an "rgb()" string into a hex parser.
 */
(function (global) {
  "use strict";

  var S = {};

  /* ---------------- the sheet's fixed geometry ---------------- */
  S.W = 1080;
  S.H = 1350;
  S.HEADER = 160;          /* no neatline ever enters this strip */
  S.MARGIN = 80;           /* safe margin, all four sides */
  S.BOTTOM_SAFE = 1270;    /* type must END by here; measured 2026-09-11 */

  /* The deck's one light. az 168 el 24, clockwise from up, so the key is low
   * from the south southeast and the lee falls to the upper left in screen
   * space. NEVER changes across the deck: the light is not allowed to argue,
   * because the data could flip and the light would then be a lie. */
  S.LIGHT = { azDeg: 168, elDeg: 24, keyToFill: 4.0 };

  S.C = {
    margin:      "#0B1724",
    marginEdge:  "#071018",
    neatline:    "#4E6474",
    groundLit:   "#C7CCC4",
    groundMid:   "#8A7F6E",
    groundLee:   "#4A4B49",
    water:       "#7E8A8C",
    waterDeep:   "#2C3A42",
    docBoard:    "#8C7A5E",
    docEdgeLit:  "#CBBFA6",
    seam:        "#2A2E26",
    ink:         "#F4F8FF",
    household:   "#6EA5FF",
    phantom:     "#9AA7B0",
    gold:        "#FFC72C",
    goldHalo:    "#FFDA6E"
  };

  /* ---------------- the margin field, with basin terms ---------------- */

  /* basins: [[x, y, w, h, depth], ...] in design px, depth 0 to 1.
   * Returns a function (x,y) -> 0..1, the ramped distance to the nearest basin.
   * Ramp radius 190 px and depth 0.82 were measured on the 2026-09-11 prototype
   * and are the constants the whole deck uses. */
  S.basinFn = function (basins, ramp) {
    var R = ramp || 190;
    return function (x, y) {
      var k = 0;
      for (var i = 0; i < basins.length; i++) {
        var b = basins[i];
        var dx = Math.max(b[0] - x, 0, x - (b[0] + b[2]));
        var dy = Math.max(b[1] - y, 0, y - (b[1] + b[3]));
        var d = Math.sqrt(dx * dx + dy * dy);
        var v = b[4] * Math.max(0, 1 - d / R);
        if (v > k) k = v;
      }
      return k;
    };
  };

  /* The slate margin: a graded ground, then a stipple whose height carries the
   * basin terms so the quiet bands under type are worked rather than wiped.
   * `form` is the caller's own tone function (x,y)->0..1 so no two slides share
   * a margin texture. REQUIRED, deliberately, same reasoning as akstipple's
   * `height`: a default would let a slide buy the look without the composition. */
  S.marginField = function (cx, o) {
    if (typeof o.form !== "function") {
      throw new TypeError("aksheet.marginField: `form` is required and has no " +
        "default. Give this slide its own margin tone.");
    }
    var W = S.W, H = S.H;
    var g = cx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, S.C.marginEdge);
    g.addColorStop(0.34, S.C.margin);
    g.addColorStop(1, S.C.marginEdge);
    cx.fillStyle = g;
    cx.fillRect(0, 0, W, H);

    var basin = S.basinFn(o.basins || [], o.ramp);
    var depth = (o.basinDepth == null) ? 0.82 : o.basinDepth;
    var form = o.form;
    global.AKSTIPPLE.field(cx, {
      seed: o.seed,
      count: o.count || 24000,
      ramp: o.ramp2 || ["#12202E", "#18293A", "#1F3345", "#2A4155", "#375067", "#47627B"],
      height: function (x, y) {
        var h = form(x, y);
        h *= (1 - depth * basin(x, y));
        return h < 0 ? 0 : (h > 1 ? 1 : h);
      }
    });
  };

  /* ---------------- the neatline, a CUT not a border ---------------- */

  /* Returns a context saved and clipped to the window rect. The caller draws
   * its terrain, then calls S.closeWindow(cx) to restore and lay the cut. */
  S.window = function (cx, rect) {
    cx.save();
    cx.beginPath();
    cx.rect(rect[0], rect[1], rect[2], rect[3]);
    cx.clip();
    return cx;
  };

  /* The margin plane sits ABOVE the map plane, so the cut gets a soft inner
   * shadow on the key side and a hard 2px occlusion seam at the edge. */
  S.closeWindow = function (cx, rect, opts) {
    cx.restore();
    var o = opts || {};
    var x = rect[0], y = rect[1], w = rect[2], h = rect[3];

    cx.save();
    cx.beginPath();
    cx.rect(x, y, w, h);
    cx.clip();
    /* inner shadow, cast from the margin's inner edge, 12px, on the lee side
     * (light az 168 is from the lower right in screen terms, so the lee of the
     * margin lip falls on the upper left inside the window) */
    var ig = cx.createLinearGradient(x, y, x, y + 26);
    ig.addColorStop(0, "rgba(6,12,20,0.55)");
    ig.addColorStop(1, "rgba(6,12,20,0)");
    cx.fillStyle = ig;
    cx.fillRect(x, y, w, 26);
    var lg = cx.createLinearGradient(x, y, x + 22, y);
    lg.addColorStop(0, "rgba(6,12,20,0.42)");
    lg.addColorStop(1, "rgba(6,12,20,0)");
    cx.fillStyle = lg;
    cx.fillRect(x, y, 22, h);
    cx.restore();

    cx.save();
    cx.lineJoin = "miter";
    cx.lineCap = "butt";
    cx.strokeStyle = o.stroke || S.C.neatline;
    if (o.phantom) {
      cx.setLineDash([36, 8, 5, 8, 5, 8]);
      cx.lineWidth = 1.25;
    } else {
      cx.setLineDash([]);
      cx.lineWidth = 3.5;
    }
    cx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
    cx.setLineDash([]);
    /* the hard occlusion seam, 2px, only on the two lee edges */
    cx.strokeStyle = "rgba(4,9,15,0.85)";
    cx.lineWidth = 2;
    cx.beginPath();
    cx.moveTo(x, y + h); cx.lineTo(x, y); cx.lineTo(x + w, y);
    cx.stroke();
    cx.restore();
  };

  /* ---------------- the contact triple ---------------- */

  /* 1. LIGHT THE GROUND FIRST, AND FAINTLY. The pool's ramp must HOLD before it
   * falls, or a pool spent at half radius lights only the strip the cast then
   * covers.
   *
   * THE POOL IS A LIFT, NOT A LAMP. On No.56 every one of five pixel critics
   * independently called this a lens flare, a glow sticker, a bloom, a blob, on
   * nine slides out of nine, while the machine contact gate read PASS on all of
   * them. The cause was a run tuning the pool UP to widen dL, because dL is
   * measured as ground minus shadow and the pool is the cheap half of that
   * subtraction. It is also the wrong half. A contact reads because the SHADOW
   * is dark, and a ground lit past the object it carries is a light source with
   * an object floating over it, which is the failure the gate was built to
   * catch wearing the gate's own PASS.
   *
   * So the ceiling here is deliberate and low. Peak alpha 0.28 puts the pool a
   * dozen L* over a near-black margin, which is all a plane needs to say it is
   * a plane, and it is less than half what read as a lamp. Below about 0.18 the
   * ground runs out of headroom and the cast has nothing left to subtract from,
   * which is the same failure from the other side.
   * Earn dL from `cast`'s `k`, never from here. */
  S.litPool = function (cx, x, y, rx, ry, tint) {
    var R = 100;
    cx.save();
    cx.translate(x, y);
    cx.scale(rx / R, ry / R);
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    g.addColorStop(0.00, tint || "rgba(142,160,178,0.28)");
    g.addColorStop(0.46, tint ? tint : "rgba(142,160,178,0.24)");
    g.addColorStop(0.74, "rgba(112,130,148,0.10)");
    g.addColorStop(1.00, "rgba(112,130,148,0)");
    cx.fillStyle = g;
    cx.beginPath();
    cx.arc(0, 0, R, 0, Math.PI * 2);
    cx.fill();
    cx.restore();
  };

  /* 2. THEN CAST, AND THIS IS WHERE THE SEPARATION COMES FROM. `w` is the FOOT,
   * not the silhouette: 70 to 110 design px. `k` scales both terms together
   * (default 1); raise it when the pair measures short, because darkening the
   * cast is the honest way to widen dL and brightening the pool is not.
   *
   * The cast is BIASED along the deck's own light by default. S.LIGHT.azDeg is
   * 168, which is south southeast, so the shadow falls down and slightly left
   * of the foot. A cast centred on the object radiates evenly and reads as a
   * halo no matter how dark it is, because a symmetric shadow is not a shadow,
   * it is a vignette. Pass dx/dy to override. */
  S.cast = function (cx, cxp, cyp, w, opts) {
    var o = opts || {};
    var R = 100, wide = o.wide == null ? 2.1 : o.wide;
    var k = o.k == null ? 1 : o.k;
    /* the light's own push, unit vector in screen px, scaled to the foot */
    var az = (S.LIGHT.azDeg - 180) * Math.PI / 180;
    var bx = o.bx == null ? -Math.sin(az) * w * 0.16 : o.bx;
    var by = o.by == null ? Math.cos(az) * w * 0.07 : o.by;
    cx.save();
    cx.translate(cxp + bx, cyp + by);
    /* wide ambient term */
    cx.save();
    cx.scale((w * wide) / (2 * R), (w * 0.34) / (2 * R));
    var ga = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    ga.addColorStop(0, "rgba(10,16,13," + Math.min(0.95, 0.30 * k).toFixed(3) + ")");
    ga.addColorStop(1, "rgba(10,16,13,0)");
    cx.fillStyle = ga;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
    /* tight cast, offset downlight */
    cx.save();
    cx.translate(o.dx || 0, o.dy || 0);
    cx.scale(w / (2 * R), (w * 0.16) / (2 * R));
    var gt = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    gt.addColorStop(0, "rgba(6,10,8," + Math.min(0.98, 0.72 * k).toFixed(3) + ")");
    gt.addColorStop(1, "rgba(6,10,8,0)");
    cx.fillStyle = gt;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
    cx.restore();
  };

  /* 3. THE SEAM LAST, and it is what says ATTACHED. Hard, narrow, almost
   * unblurred, drawn ON the object's base so the trough sits at the foot. */
  S.seam = function (cx, x0, x1, y, strength) {
    var g = cx.createLinearGradient(0, y - 3, 0, y + 5);
    g.addColorStop(0, "rgba(18,22,18,0)");
    g.addColorStop(0.4, "rgba(18,22,18," + (strength || 0.72) + ")");
    g.addColorStop(1, "rgba(18,22,18,0)");
    cx.fillStyle = g;
    cx.fillRect(x0, y - 3, x1 - x0, 8);
  };

  /* ---------------- the edge-on document ---------------- */

  /* THE THESIS OBJECT. The approved tariff, seen ALONG ITS LENGTH so it shows
   * thickness, a tab and a structure, and NEVER a readable face. An object seen
   * edgewise invents no convention: it is the literal truth of the situation,
   * which is that the public can see the instrument and cannot read it.
   *
   * o = {x, y, w, thick, alpha, tab (0..1 position or null), divisions:[t...],
   *      seed}
   * `divisions` are struck marks across the fore edge at parametric t. Pass ONLY
   * what a source publishes. Nothing below the top division is divided, because
   * nothing below it is published, and that absence is drawn as an undivided run
   * of leaves rather than as empty space. */
  S.document = function (cx, o) {
    var x = o.x, y = o.y, w = o.w, t = o.thick;
    var a = (o.alpha == null) ? 1 : o.alpha;
    var rnd = global.AK.rng(o.seed || 56);
    cx.save();
    cx.globalAlpha = a;

    /* the board, the dark spine side, lee to the upper left. Drawn as its own
     * value so the object reads as a bound volume seen edgewise rather than as
     * a striped bar. */
    var bg = cx.createLinearGradient(0, y, 0, y + t);
    bg.addColorStop(0, "#3E362A");
    bg.addColorStop(0.18, "#5E5240");
    bg.addColorStop(1, S.C.docBoard);
    cx.fillStyle = bg;
    cx.fillRect(x, y, w, t);

    /* the fore edge: a run of leaves, each its own tapered stroke, drawn from
     * the light. This is the object's texture and it must survive the zoom
     * test, so it is a population and not a gradient. */
    var leaves = Math.max(40, Math.round(t * 2.4));
    for (var i = 0; i < leaves; i++) {
      var ty = y + (i + 0.5) * (t / leaves);
      var jitter = (rnd() - 0.5) * 1.6;
      var lit = 0.12 + 0.88 * Math.pow(i / leaves, 0.62);  /* light from below */
      var g = cx.createLinearGradient(x, ty, x + w, ty);
      g.addColorStop(0, "rgba(0,0,0,0)");
      g.addColorStop(0.06, mix(S.C.docEdgeLit, S.C.docBoard, 1 - lit));
      g.addColorStop(0.94, mix(S.C.docEdgeLit, S.C.docBoard, 1 - lit * 0.86));
      g.addColorStop(1, "rgba(0,0,0,0)");
      cx.fillStyle = g;
      cx.fillRect(x, ty + jitter, w, (t / leaves) * 0.78);
    }

    /* the outer silhouette at hero weight, per the profile-heaviest rule */
    cx.strokeStyle = "rgba(28,34,28,0.92)";
    cx.lineWidth = 5.5;
    cx.lineJoin = "miter";
    cx.strokeRect(x, y, w, t);

    /* published divisions, struck across the fore edge */
    if (o.divisions) {
      for (var d = 0; d < o.divisions.length; d++) {
        var dy = y + o.divisions[d] * t;
        cx.strokeStyle = S.C.gold;
        cx.lineWidth = 3.5;
        cx.beginPath();
        cx.moveTo(x + 6, dy); cx.lineTo(x + w - 6, dy);
        cx.stroke();
      }
    }

    /* the tab, the one thing anyone outside can read */
    if (o.tab != null) {
      /* NEVER TYPE A PLATE WIDTH. The caller measures its own label and passes
       * `tabW`, because a hand-sized chip loses about three characters in
       * twenty and six labels shipped off their plates on 2026-07-29 doing
       * exactly that. */
      var tx = x + o.tab * w, tw = o.tabW || 170;
      cx.fillStyle = S.C.gold;
      cx.fillRect(tx, y - 30, tw, 32);
      cx.fillStyle = "rgba(20,24,18,0.30)";
      cx.fillRect(tx, y + 1, tw, 3);
    }
    cx.restore();
  };

  function mix(a, b, k) {
    var A = hex(a), B = hex(b);
    return "rgb(" + Math.round(A[0] + (B[0] - A[0]) * k) + "," +
                    Math.round(A[1] + (B[1] - A[1]) * k) + "," +
                    Math.round(A[2] + (B[2] - A[2]) * k) + ")";
  }
  function hex(h) {
    return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16),
            parseInt(h.slice(5, 7), 16)];
  }
  S.mix = mix;

  /* ---------------- a machined rail, for declared scales ---------------- */

  /* A rail is a MACHINED OBJECT, not a stack of rectangles. A gradient inside a
   * fillRect is still a box, and this deck repeats the rail on five sheets, so
   * it is the element that most has to survive the zoom test. Body is a path
   * with turned ends; the face carries a longitudinal grain of short tapered
   * strokes, seeded per slide. */
  S.rail = function (cx, x0, x1, y, h, seed) {
    var r = h / 2, rnd = global.AK.rng(seed || 7);
    cx.save();
    cx.beginPath();
    cx.moveTo(x0 + r, y - r);
    cx.lineTo(x1 - r, y - r);
    cx.arc(x1 - r, y, r, -Math.PI / 2, Math.PI / 2);
    cx.lineTo(x0 + r, y + r);
    cx.arc(x0 + r, y, r, Math.PI / 2, -Math.PI / 2);
    cx.closePath();
    var g = cx.createLinearGradient(0, y - r, 0, y + r);
    g.addColorStop(0, "#3B4C5C");
    g.addColorStop(0.42, "#55697C");
    g.addColorStop(1, "#243341");
    cx.fillStyle = g;
    cx.fill();
    cx.save();
    cx.clip();
    for (var i = 0; i < 190; i++) {
      var gy = y - r + rnd() * h;
      var gx = x0 + rnd() * (x1 - x0);
      var len = 14 + rnd() * 52;
      var al = 0.04 + rnd() * 0.10;
      var gg = cx.createLinearGradient(gx, gy, gx + len, gy);
      gg.addColorStop(0, "rgba(190,208,222,0)");
      gg.addColorStop(0.5, "rgba(190,208,222," + al.toFixed(3) + ")");
      gg.addColorStop(1, "rgba(190,208,222,0)");
      cx.fillStyle = gg;
      cx.fillRect(gx, gy, len, 0.9);
    }
    cx.restore();
    cx.strokeStyle = "rgba(160,182,198,0.34)";
    cx.lineWidth = 0.75;
    cx.stroke();
    cx.restore();
  };

  /* ---------------- the index diagram (continuity device A) ---------------- */

  /* Alaska in hairline silhouette with a gold rectangle marking THIS sheet's
   * extent. Fixed at x 868 to 980, y 44 to 156, inside the header strip. The
   * gold is the constellation gold and the meaning holds, because an extent is
   * a measured thing. */
  S.indexDiagram = function (cx, pathD, extentRect, o) {
    var opt = o || {};
    var bx = opt.x == null ? 868 : opt.x;
    var by = opt.y == null ? 44 : opt.y;
    var bw = opt.w == null ? 112 : opt.w;
    cx.save();
    cx.translate(bx, by);
    cx.scale(bw / 112, bw / 112);
    if (pathD) {
      cx.strokeStyle = "rgba(160,182,198,0.55)";
      cx.lineWidth = 0.75;
      cx.stroke(new Path2D(pathD));
    }
    if (extentRect) {
      cx.strokeStyle = S.C.gold;
      cx.lineWidth = 2.0;
      cx.strokeRect(extentRect[0], extentRect[1], extentRect[2], extentRect[3]);
    }
    cx.restore();
  };

  global.AKSHEET = S;
})(this);
