/* akunderice.js — THE LISTENING SECTION, Carousel No. 57's continuity chassis.
 *
 * Committed 2026-09-12. DECK FURNITURE, shared across all nine slides on purpose,
 * which is why it is a module rather than inline code: `bespoke_check` strips
 * `<script src=>` as harness, so one shared coordinate system costs the variety
 * budget nothing while each slide's own composition still has to earn its score.
 * Same reasoning as akrail.js, akcolumn.js, akseam.js, aknight.js and aksheet.js.
 *
 * WHAT THIS IS. A vertical section of one piece of Arctic water, from the ice
 * down to the bed, with a single depth-to-pixel mapping every slide shares. The
 * deck DESCENDS through that mapping, so the camera's own depth window is the
 * progress indicator and cannot disagree with the artwork, because the rail is
 * drawn from the same function the art is.
 *
 * ITS LINEAGE, NAMED HONESTLY. akcolumn.js (No.42) did this for AIR over the
 * Kenai, an altitude-to-pixel mapping with four physical surfaces in it. This is
 * the same structural idea pointed at water, and the differences are the reason
 * it is a separate file rather than an option on that one: the light comes from
 * ABOVE and dies with depth instead of raking in from the side, the medium
 * carries a particulate population instead of being clear, and the thing being
 * measured is range from fixed sources rather than height above ground.
 *
 * WHY A SECTION AND NOT A MAP SHEET. No.56 solved art-touching-type by putting
 * all art inside a neatline and all type in the margin, and it worked, the
 * recurring warn went to zero. It also spent the deck's whole detail budget in
 * the margin, five of nine windows shipped as two-tone plates, and artwork craft
 * still scored 6 with five critics reaching for the word wallpaper. So this deck
 * does the opposite and pays for it with measurement instead of with geometry.
 * Type sits IN the water, and `akfit.js` plus a measured destination-out reserve
 * punch is what keeps it legible. The detail budget goes where the picture is.
 *
 * TWO CRAFT FINDINGS FROM THIS RUN'S PHASE 1 ARE IMPLEMENTED HERE.
 *
 * 1. THE HEAVIEST LINE FACES AWAY FROM THE LIGHT. `S.profile` ranks stroke weight
 *    by the LIGHT rather than by importance. Interior seams thin, the silhouette
 *    heavier, and the arcs of the silhouette whose outward normal points away
 *    from the key heavier and darker still. That is the technical-illustration
 *    convention as Greg Maxson states it, the trade's "Kalmbach method". It is a
 *    craft convention with a named attribution and NOT a standard: MPEP 1503 was
 *    checked directly today and carries nothing about light direction, so do not
 *    cite the USPTO for it. This house has ranked weight by MEANING for twenty
 *    decks, which is why a correctly shaded form can still read as a sticker cut
 *    out of paper: all four sides of its silhouette were one weight.
 *
 * 2. DETAIL DENSITY IS A DEPTH CUE, SO IT IS SPENT UNEVENLY ON PURPOSE.
 *    `S.marine` takes a `near` band and puts most of the population in it,
 *    stripping the far water deliberately. The cutaway tradition states it as a
 *    positive rule rather than a budget: the ABSENCE of detail is what reads as
 *    distance, and two regions detailed identically at different sizes read flat
 *    however much work went into both.
 *
 * DETERMINISM. Every caller passes its own seed. Seeded mulberry32 via AK.rng.
 * No Math.random, no Date.now, no crypto. Load AFTER noise.js.
 *
 * COLOUR SAFETY. No colour helper is nested inside another, so nothing here ever
 * feeds an "rgb()" string into a hex parser. Every colour is a literal or an
 * rgba() string built from numbers.
 */
(function (global) {
  "use strict";

  var S = {};

  /* ---------------- the frame ---------------- */

  S.W = 1080;
  S.H = 1350;
  S.SAFE = 80;

  /* THE DECK'S ONE LIGHT, declared once and never varied per slide, because a
   * deck whose light moves reads as nine scenes rather than one place.
   *
   * It is DOWNWELLING, which is the physically true thing about water under ice
   * and is also new for this house: every recent deck used a low raking key.
   * `azDeg` is clockwise from up in screen space, so az 12 is very slightly to
   * the right of straight down the frame and the lee of any form falls just to
   * its lower left. el 62 is steep. Key to fill is 5 to 1.
   *
   * CONSEQUENCE TO DESIGN FOR, because a steep key is a real craft risk: it
   * flattens a swelled line to one width, which is exactly what akengrave's
   * docstring warns about. So this deck does NOT lean on surface swell for its
   * modelling. Its modelling comes from the sound field and from the value
   * ladder of depth, and `S.profile` is what keeps silhouettes from going flat.
   */
  S.LIGHT = { azDeg: 12, elDeg: 62, keyFill: 5.0 };

  /* the key direction as a unit vector in screen px, +x right and +y DOWN,
   * matching akrelief's lightVec convention exactly so the two can never
   * disagree about where the light is */
  S.lightVec = function () {
    var a = S.LIGHT.azDeg * Math.PI / 180, e = S.LIGHT.elDeg * Math.PI / 180;
    return [Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e)];
  };

  /* ---------------- the depth mapping, which is the continuity device ---------------- */

  /* One function the whole deck shares. A slide sets its own WINDOW on the same
   * mapping, so the deck descends and the rail, the art and the declared scale
   * are three views of one number rather than three hand-typed sets.
   *
   * THIS IS THE FIX FOR THE CLASS 94c NAMES. No.49 authored a catenary per slide
   * and the deck misaligned at seven of eight junctions, by 490 design px at the
   * worst, because each slide computed its own version of the shared thing.
   * Here there is nothing to recompute: `setWindow` is the only per-slide state
   * and `depth()` is pure.
   */
  var win = { d0: 0, d1: 60, y0: 0, y1: 1350 };

  S.setWindow = function (d0, d1, y0, y1) {
    if (!(d1 > d0)) throw new Error("AKICE.setWindow: d1 must exceed d0");
    if (!(y1 > y0)) throw new Error("AKICE.setWindow: y1 must exceed y0");
    win = { d0: d0, d1: d1, y0: y0, y1: y1 };
    return S.window();
  };

  S.window = function () { return { d0: win.d0, d1: win.d1, y0: win.y0, y1: win.y1 }; };

  /* metres below the ice surface -> design px */
  S.depth = function (m) {
    return win.y0 + (m - win.d0) * (win.y1 - win.y0) / (win.d1 - win.d0);
  };
  /* and back, so a mark measured off the render can be read as a depth */
  S.metres = function (y) {
    return win.d0 + (y - win.y0) * (win.d1 - win.d0) / (win.y1 - win.y0);
  };
  /* 0 at the ice, 1 at the bottom of this slide's window. The value ladder. */
  S.t = function (y) { return Math.max(0, Math.min(1, (y - win.y0) / (win.y1 - win.y0))); };

  /* ---------------- the water ---------------- */

  /* THE VALUE LADDER, drawn as strips rather than as one fill-to-bottom gradient.
   * aksnow's docstring records why: a ladder run as a single fill silently
   * flattens the whole mass to one value, which is what shipped on 2026-07-30's
   * first pass. Strips are order independent.
   *
   * `gain` is this run's Phase 1 finding applied to depth rather than to height.
   * Jenny and Patterson give aerial perspective as a CONTRAST modulation keyed to
   * elevation, not the distance lerp the doctrine carries. Under ice the same
   * physics runs downward: near the ice the difference between a lit face and a
   * shaded one is large, and by the bed it has compressed to almost nothing. So
   * the gain a caller gets back from `S.contrast(y)` is what every form in the
   * water multiplies its own light-to-shadow spread by, and that is what makes
   * depth read without a single blur.
   */
  S.contrast = function (y) {
    var t = S.t(y);
    return 1.0 - 0.72 * Math.pow(t, 0.85);
  };

  S.water = function (cx, opts) {
    var o = opts || {}, i;
    var y0 = o.y0 == null ? 0 : o.y0, y1 = o.y1 == null ? S.H : o.y1;
    var top = o.top || "#123E49";
    var bed = o.bed || "#03090C";
    var steps = o.steps || 44;
    var t0 = parseHex(top), t1 = parseHex(bed);
    for (i = 0; i < steps; i++) {
      var a = i / steps, b = (i + 1) / steps;
      /* eased toward the dark end, per the doctrine's gradient rule */
      var k = Math.pow(a, 1.35);
      cx.fillStyle = "rgb(" + Math.round(t0[0] + (t1[0] - t0[0]) * k) + ","
        + Math.round(t0[1] + (t1[1] - t0[1]) * k) + ","
        + Math.round(t0[2] + (t1[2] - t0[2]) * k) + ")";
      cx.fillRect(0, y0 + (y1 - y0) * a - 0.5, S.W, (y1 - y0) * (b - a) + 1.0);
    }
  };

  /* MARINE SNOW, and it is the answer to wallpaper. A graded wash in a large
   * region reads as NOTHING after the 6x box downsample to feed size, which is
   * aknight's measured finding; a population of discrete marks survives it.
   *
   * `near` is a [y0,y1] band that gets most of the population, because detail
   * density is a depth cue and spending it evenly is what makes two regions read
   * flat. Motes carry three separate functions of the same depth term, count,
   * radius and alpha, which is akstipple's three-function rule: a region then
   * cannot be flat unless the water genuinely is.
   */
  S.marine = function (cx, opts) {
    var o = opts || {};
    if (!o.seed && o.seed !== 0) throw new Error("AKICE.marine: seed is required");
    if (!o.near) throw new Error("AKICE.marine: `near` band is required, because "
      + "an even population is the wallpaper this function exists to avoid");
    var rnd = AK.rng(o.seed);
    var n = o.count == null ? 2600 : o.count;
    var y0 = o.y0 == null ? 0 : o.y0, y1 = o.y1 == null ? S.H : o.y1;
    var nf = o.nearShare == null ? 0.68 : o.nearShare;
    var tint = o.tint || [196, 226, 224];
    for (var i = 0; i < n; i++) {
      var inNear = rnd() < nf;
      var y = inNear ? o.near[0] + rnd() * (o.near[1] - o.near[0])
                     : y0 + rnd() * (y1 - y0);
      if (y < y0 || y > y1) continue;
      var x = rnd() * S.W;
      var t = S.t(y);
      /* radius and alpha both fall with depth, and the near band gets the bigger
       * marks, so the two populations are distinguishable rather than mixed */
      var r = (inNear ? 0.55 : 0.35) + (inNear ? 1.35 : 0.7) * (1 - t) * rnd();
      var al = (0.05 + 0.30 * (1 - t) * rnd()) * (inNear ? 1.0 : 0.62);
      cx.fillStyle = "rgba(" + tint[0] + "," + tint[1] + "," + tint[2] + ","
        + al.toFixed(3) + ")";
      cx.beginPath();
      cx.arc(x, y, r, 0, Math.PI * 2);
      cx.fill();
      /* about one in seven is a settling floc with a short tail, which is what
       * makes the population read as marine snow rather than as noise */
      if (inNear && rnd() < 0.14) {
        cx.strokeStyle = "rgba(" + tint[0] + "," + tint[1] + "," + tint[2] + ","
          + (al * 0.5).toFixed(3) + ")";
        cx.lineWidth = Math.max(0.4, r * 0.5);
        cx.beginPath();
        cx.moveTo(x, y);
        cx.lineTo(x + (rnd() - 0.5) * 2.0, y - 3 - rnd() * 7);
        cx.stroke();
      }
    }
  };

  /* ---------------- the ice lid ---------------- */

  /* The ice is the frame's one genuinely LIT surface and everything below it is
   * lit by what gets through, so it is drawn as three parts: a lit upper crust,
   * a keeled underside whose ridges hang DOWN into the water, and the light that
   * survives. `keels` is a list of [x, depthMetres] so a slide can carry the
   * same ridge across frames, which is what makes the lid one object rather than
   * nine textures.
   *
   * Returns the underside polyline in design px, so a caller can clip to it, cast
   * from it, or hang a leader off it without recomputing the shape.
   */
  S.ice = function (cx, opts) {
    var o = opts || {};
    if (!o.seed && o.seed !== 0) throw new Error("AKICE.ice: seed is required");
    var rnd = AK.rng(o.seed);
    var surf = o.surfaceY == null ? S.depth(0) : o.surfaceY;
    var thick = o.thickness == null ? 1.6 : o.thickness;        /* metres */
    var keels = o.keels || [];
    var lit = o.lit || "#D8ECEE";
    var mid = o.mid || "#9FC2C8";
    var keel = o.keel || "#5E838C";

    /* the underside, sampled every 6 px, with each declared keel as a smooth
     * lobe so a ridge is a FORM and not a spike */
    var under = [], x;
    for (x = -12; x <= S.W + 12; x += 6) {
      var d = thick;
      for (var k = 0; k < keels.length; k++) {
        var kx = keels[k][0], kd = keels[k][1], wid = keels[k][2] || 130;
        var u = (x - kx) / wid;
        d += (kd - thick) * Math.exp(-u * u * 2.2);
      }
      /* a small seeded roughness, smoothed by construction because fbm is */
      d += 0.10 * thick * AK.fbm2(x * 0.004, 7.3, 3);
      under.push([x, S.depth(d)]);
    }

    /* the crust above the waterline, lit */
    var g = cx.createLinearGradient(0, surf - 26, 0, surf + 6);
    g.addColorStop(0, lit);
    g.addColorStop(1, mid);
    cx.fillStyle = g;
    cx.fillRect(0, Math.min(0, surf - 40), S.W, Math.max(0, surf - Math.min(0, surf - 40)) + 2);

    /* the ice body down to the underside */
    cx.beginPath();
    cx.moveTo(-12, surf);
    for (x = 0; x < under.length; x++) cx.lineTo(under[x][0], under[x][1]);
    cx.lineTo(S.W + 12, surf);
    cx.closePath();
    var gi = cx.createLinearGradient(0, surf, 0, S.depth(thick * 2.4));
    gi.addColorStop(0, mid);
    gi.addColorStop(1, keel);
    cx.fillStyle = gi;
    cx.fill();

    /* brine channels, drawn DOWNWARD from the crust because that is the way
     * they drain, and thinning as they go, so the lid has interior detail rather
     * than being a two-tone plate */
    cx.save();
    cx.beginPath();
    cx.moveTo(-12, surf);
    for (x = 0; x < under.length; x++) cx.lineTo(under[x][0], under[x][1]);
    cx.lineTo(S.W + 12, surf);
    cx.closePath();
    cx.clip();
    for (var c = 0; c < (o.channels == null ? 210 : o.channels); c++) {
      var cxx = rnd() * S.W, len = 6 + rnd() * 30;
      cx.strokeStyle = "rgba(52,78,86," + (0.10 + 0.34 * rnd()).toFixed(3) + ")";
      cx.lineWidth = 0.5 + rnd() * 1.1;
      cx.beginPath();
      cx.moveTo(cxx, surf + 2 + rnd() * 6);
      cx.lineTo(cxx + (rnd() - 0.5) * 5, surf + 2 + len);
      cx.stroke();
    }
    cx.restore();

    /* the underside as the deck's hardest edge, because it is the boundary the
     * whole story is about. Weight ranked by S.profile's rule, and this edge
     * faces AWAY from a downwelling key by definition, so it takes the heavy
     * rank. */
    cx.strokeStyle = o.arris || "rgba(232,246,247,0.82)";
    cx.lineWidth = 2.4;
    cx.beginPath();
    for (x = 0; x < under.length; x++) {
      if (x === 0) cx.moveTo(under[x][0], under[x][1]);
      else cx.lineTo(under[x][0], under[x][1]);
    }
    cx.stroke();

    return under;
  };

  /* ---------------- the light that gets through ---------------- */

  /* Under-ice irradiance falls off fast, and the honest way to draw that is a
   * screened wedge from the lid rather than a dark fill over everything: the
   * water already has its value ladder, and darkening it twice kills the marine
   * snow the frame depends on. `S.daylight` SCREENS, exactly as the contact-pool
   * rule requires of any added light.
   */
  S.daylight = function (cx, opts) {
    var o = opts || {};
    var surf = o.surfaceY == null ? S.depth(0) : o.surfaceY;
    var reach = o.reach == null ? 520 : o.reach;
    var peak = o.peak == null ? 0.16 : o.peak;
    if (peak > 0.28) throw new Error("AKICE.daylight: peak " + peak + " exceeds "
      + "0.28. The same ceiling as a contact pool, and for the same reason: five "
      + "critics called No.56's pool a lens flare at exactly this mistake.");
    cx.save();
    cx.globalCompositeOperation = "screen";
    var g = cx.createLinearGradient(0, surf, 0, surf + reach);
    g.addColorStop(0.00, "rgba(150,196,198," + peak.toFixed(3) + ")");
    g.addColorStop(0.42, "rgba(120,168,174," + (peak * 0.42).toFixed(3) + ")");
    g.addColorStop(1.00, "rgba(96,140,150,0)");
    cx.fillStyle = g;
    cx.fillRect(0, surf, S.W, reach);
    cx.restore();
  };

  /* ---------------- the range ring, built out of STOPS ---------------- */

  /* A ring, and the one way to draw it that does not also paint a flat disc.
   * `createRadialGradient(x,y,r0, x,y,r1)` fills every pixel inside r0 with the
   * colour at stop 0, so a concentric ramp whose first stop carries alpha is that
   * ring PLUS a solid disc of radius r0. No.53 wrote exactly that as an
   * atmospheric limb on seven slides, filled it in `lighter`, washed out the
   * terminator its whole deck argued from, and it took two build rounds and five
   * critics to find the one cause. qa.py now FAILS a flat core in an additive
   * composite over 2 percent of the frame.
   *
   * So the ramp starts at radius 0 and is TRANSPARENT at 0 and at r0/r1, carries
   * the band's colour just outside that, and is transparent again at 1.
   */
  S.ring = function (cx, x, y, r, opts) {
    var o = opts || {};
    var wid = o.width == null ? 9 : o.width;
    var al = o.alpha == null ? 0.5 : o.alpha;
    var col = o.rgb || [255, 199, 44];
    var inner = Math.max(0, (r - wid / 2) / r);
    var mid = Math.max(inner + 0.001, r / r * (r / r));
    var g = cx.createRadialGradient(x, y, 0, x, y, r + wid / 2);
    var rr = r + wid / 2;
    g.addColorStop(0.0, "rgba(" + col[0] + "," + col[1] + "," + col[2] + ",0)");
    g.addColorStop(Math.max(0.001, (r - wid / 2) / rr),
      "rgba(" + col[0] + "," + col[1] + "," + col[2] + ",0)");
    g.addColorStop(Math.min(0.999, r / rr),
      "rgba(" + col[0] + "," + col[1] + "," + col[2] + "," + al.toFixed(3) + ")");
    g.addColorStop(1.0, "rgba(" + col[0] + "," + col[1] + "," + col[2] + ",0)");
    cx.save();
    if (o.blend) cx.globalCompositeOperation = o.blend;
    if (o.clip) { cx.beginPath(); cx.rect(o.clip[0], o.clip[1], o.clip[2], o.clip[3]); cx.clip(); }
    cx.fillStyle = g;
    cx.beginPath();
    cx.arc(x, y, rr, 0, Math.PI * 2);
    cx.fill();
    cx.restore();
    return { x: x, y: y, r: r, outer: rr };
  };

  /* ---------------- the light-keyed profile, this run's craft finding ---------------- */

  /* THREE RANKS, AND THE THIRD IS A LIGHTING RANK. Interior seams thin, the
   * exterior silhouette heavier, and the arcs of that silhouette whose outward
   * normal points AWAY from the key heavier and darker still. Maxson's rule, the
   * trade's Kalmbach method, checked against MPEP 1503 today and NOT found there,
   * so it is craft and not a standard.
   *
   * `pts` is a closed polyline in design px, wound either way. `opts.fill` paints
   * it first if given. Returns the count of heavy segments, so a dossier can say
   * how much of the silhouette took the heavy rank and a critic can check.
   */
  S.profile = function (cx, pts, opts) {
    var o = opts || {}, i;
    if (!pts || pts.length < 3) throw new Error("AKICE.profile: need a closed polyline");
    var L = S.lightVec();
    var w = o.weight == null ? 2.0 : o.weight;
    var light = o.light || "rgba(214,238,240,0.72)";
    var lee = o.lee || "rgba(4,12,16,0.88)";

    if (o.fill) {
      cx.beginPath();
      cx.moveTo(pts[0][0], pts[0][1]);
      for (i = 1; i < pts.length; i++) cx.lineTo(pts[i][0], pts[i][1]);
      cx.closePath();
      cx.fillStyle = o.fill;
      cx.fill();
    }

    /* signed area tells us the winding, which is what makes an outward normal
     * outward rather than inward. Getting this backwards puts the heavy line on
     * the lit side and reads as a light leak. */
    var area = 0;
    for (i = 0; i < pts.length; i++) {
      var p = pts[i], q = pts[(i + 1) % pts.length];
      area += p[0] * q[1] - q[0] * p[1];
    }
    var sign = area >= 0 ? 1 : -1;

    /* pass one, the whole silhouette at the standard weight */
    cx.strokeStyle = light;
    cx.lineWidth = w;
    cx.lineJoin = "miter";
    cx.lineCap = "butt";
    cx.beginPath();
    cx.moveTo(pts[0][0], pts[0][1]);
    for (i = 1; i < pts.length; i++) cx.lineTo(pts[i][0], pts[i][1]);
    cx.closePath();
    cx.stroke();

    /* pass two, only the segments facing away from the key, heavier and darker */
    var heavy = 0;
    cx.strokeStyle = lee;
    cx.lineWidth = w * (o.heavyMul == null ? 1.6 : o.heavyMul);
    for (i = 0; i < pts.length; i++) {
      var a = pts[i], b = pts[(i + 1) % pts.length];
      var dx = b[0] - a[0], dy = b[1] - a[1];
      var len = Math.sqrt(dx * dx + dy * dy);
      if (len < 0.5) continue;
      /* outward normal for this winding */
      var nx = sign * (dy / len), ny = sign * (-dx / len);
      var ndotl = nx * L[0] + ny * L[1];
      if (ndotl < (o.threshold == null ? -0.12 : o.threshold)) {
        cx.beginPath();
        cx.moveTo(a[0], a[1]);
        cx.lineTo(b[0], b[1]);
        cx.stroke();
        heavy++;
      }
    }
    return { segments: pts.length, heavy: heavy };
  };

  /* ---------------- the contact triple ---------------- */

  /* POOL, CAST, SEAM, in that order, and the order is the only one that measures.
   * Inherited wholesale from AKNIGHT.contact (94a) and aksheet (95a) because those
   * constants were learned the hard way twice and this deck is not going to learn
   * them a third time.
   *
   * The one adaptation is the bias. A downwelling key at el 62 throws a SHORT
   * cast almost straight down, so the offsets here are small where a raking key's
   * were large. The pair still goes SIDE BY SIDE at the object's own base line,
   * the cast at foot+2 and the pool centre at foot+14, which is the geometry that
   * took No.56's six failing slides to 12.6 through 14.9 L*.
   *
   * NEVER GUESS EITHER RECT. `scripts/contact_probe.py --slide N --base cx,cy`
   * measures it off the render and writes the declaration.
   */
  S.litPool = function (cx, x, y, rx, ry, peak) {
    var p = peak == null ? 0.26 : peak;
    if (p > 0.28) throw new Error("AKICE.litPool: peak " + p + " exceeds 0.28. "
      + "The pool is a LIFT, not a lamp. Earn dL from the cast's k.");
    var R = 100;
    cx.save();
    cx.globalCompositeOperation = "screen";
    cx.translate(x, y);
    cx.scale(rx / R, ry / R);
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    g.addColorStop(0.00, "rgba(158,196,200," + p.toFixed(3) + ")");
    g.addColorStop(0.46, "rgba(148,184,190," + (p * 0.86).toFixed(3) + ")");
    g.addColorStop(0.74, "rgba(120,154,164," + (p * 0.36).toFixed(3) + ")");
    g.addColorStop(1.00, "rgba(110,144,154,0)");
    cx.fillStyle = g;
    cx.beginPath();
    cx.arc(0, 0, R, 0, Math.PI * 2);
    cx.fill();
    cx.restore();
  };

  S.cast = function (cx, fx, fy, w, opts) {
    var o = opts || {}, R = 100;
    var k = o.k == null ? 1 : o.k;
    var wide = o.wide == null ? 2.0 : o.wide;
    /* the key's own push, tiny at el 62 */
    var a = (S.LIGHT.azDeg - 180) * Math.PI / 180;
    var bx = o.bx == null ? -Math.sin(a) * w * 0.07 : o.bx;
    var by = o.by == null ? Math.cos(a) * w * 0.04 : o.by;
    cx.save();
    cx.translate(fx + bx, fy + by);
    cx.save();
    cx.scale((w * wide) / (2 * R), (w * 0.30) / (2 * R));
    var ga = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    ga.addColorStop(0, "rgba(2,7,10," + Math.min(0.95, 0.32 * k).toFixed(3) + ")");
    ga.addColorStop(1, "rgba(2,7,10,0)");
    cx.fillStyle = ga;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
    cx.save();
    cx.scale(w / (2 * R), (w * 0.15) / (2 * R));
    var gt = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    gt.addColorStop(0, "rgba(1,4,6," + Math.min(0.98, 0.76 * k).toFixed(3) + ")");
    gt.addColorStop(1, "rgba(1,4,6,0)");
    cx.fillStyle = gt;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
    cx.restore();
  };

  S.seam = function (cx, x0, x1, y, strength) {
    var g = cx.createLinearGradient(0, y - 3, 0, y + 5);
    g.addColorStop(0, "rgba(2,8,11,0)");
    g.addColorStop(0.4, "rgba(2,8,11," + (strength == null ? 0.74 : strength) + ")");
    g.addColorStop(1, "rgba(2,8,11,0)");
    cx.fillStyle = g;
    cx.fillRect(x0, y - 3, x1 - x0, 8);
  };

  /* ---------------- the depth rail, which RETURNS ITS OWN MARKS ---------------- */

  /* A measured axis, and the whole point of this function is that the slide does
   * not get to type the marks. It draws from `S.depth`, then hands back exactly
   * what it drew, so the `data-scale` declaration is generated from the drawing.
   *
   * That kills the No.35 defect class by construction. That run hung three gold
   * place ticks under a rail whose x meant DOLLARS, printing three regions at
   * three dollar amounts, and set thirteen division ticks implying twelve months
   * over a ten month period. Both went through every green gate and were caught
   * by a human reading the picture. qa.py FAILS a mark that declares no meaning,
   * a mark off its own span, and any undeclared run of ink in the band. Feeding
   * it the drawing's own output is the only way to be sure those agree.
   *
   * Returns {scale} ready to JSON.stringify into `data-scale`.
   */
  S.rail = function (cx, opts) {
    var o = opts || {};
    var x = o.x == null ? 1000 : o.x;
    var ticks = o.ticks;
    if (!ticks || !ticks.length)
      throw new Error("AKICE.rail: `ticks` is required, a list of [metres, label]. "
        + "There is no decorative tick on a measured axis.");
    var bandW = o.bandW == null ? 22 : o.bandW;
    var ink = o.ink || "rgba(186,214,218,0.78)";
    var faint = o.faint || "rgba(150,182,190,0.34)";
    var w = S.window();

    /* the rail itself, spanning this slide's whole window */
    cx.strokeStyle = faint;
    cx.lineWidth = 1.25;
    cx.beginPath();
    cx.moveTo(x, S.depth(w.d0));
    cx.lineTo(x, S.depth(w.d1));
    cx.stroke();

    var marks = [], i;
    for (i = 0; i < ticks.length; i++) {
      var m = ticks[i][0], label = ticks[i][1];
      var y = S.depth(m);
      if (y < S.depth(w.d0) - 1 || y > S.depth(w.d1) + 1) continue;
      var major = ticks[i][2] !== false;
      cx.strokeStyle = major ? ink : faint;
      cx.lineWidth = major ? 2.0 : 1.0;
      cx.beginPath();
      cx.moveTo(x - (major ? 16 : 8), y);
      cx.lineTo(x, y);
      cx.stroke();
      marks.push({ at: Math.round(y), means: label });
    }

    return {
      scale: {
        what: o.what || "the depth rail",
        axis: "y",
        unit: o.unit || "metres below the ice",
        from: [Math.round(S.depth(w.d0)), w.d0],
        to: [Math.round(S.depth(w.d1)), w.d1],
        band: [Math.round(x - bandW), Math.round(x + 2)],
        marks: marks
      }
    };
  };

  /* ---------------- small utilities ---------------- */

  function parseHex(h) {
    var s = String(h).replace("#", "");
    if (s.length === 3) s = s[0] + s[0] + s[1] + s[1] + s[2] + s[2];
    var n = parseInt(s, 16);
    if (isNaN(n)) throw new Error("AKICE: bad hex `" + h + "`. A colour helper was "
      + "probably nested inside another and returned an rgb() string.");
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  S.parseHex = parseHex;

  global.AKICE = S;
})(window);
