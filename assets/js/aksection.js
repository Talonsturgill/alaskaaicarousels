/* aksection.js — THE JURISDICTION SECTION, a chassis for orthographic
 * section decks.  (Alaska.Ai, committed 2026-09-20 for Carousel No. 64.)
 *
 * WHAT THIS IS. House furniture for decks whose hero is a VERTICAL SECTION
 * rather than an object under a camera: a fixed ground datum, a modelled earth
 * slab below it, air above it, and the drafting furniture a section needs to
 * be read as a measured drawing rather than as a picture of a hill.
 *
 * WHAT IT IS NOT. It is not a slide renderer. It draws PRIMITIVES. Every slide
 * that uses it still writes its own composition, its own scene and its own
 * drawing code, because `scripts/bespoke_check.py` measures the outcome and
 * nine frames sharing one drawSlide() is a template whatever it is called.
 * A shared projection helper is furniture; a shared whole-slide function is not.
 *
 * WHY IT EXISTS. No.64's standing weakness was artwork craft, weakest in 7 of
 * the previous 10 runs, and the named mechanism was "stroking hairlines onto a
 * gradient" where the dossier called for an incised substrate. Three of the
 * primitives here exist specifically so that failure is unavailable:
 *
 *   ribbon()   a line across air is a TAPERED CASED POLYGON, fat in the middle
 *              and tapering at both ends, filled and never stroked.
 *   incise()   a line on ground is a CUT, drawn as a bright lip on the up-light
 *              shoulder and a dark trough on the down-light side, two filled
 *              polygons, never one stroked path.
 *   step()     a terrace is a modelled tread and riser with its own AO, never
 *              a rectangle with a border.
 *
 * THE LIGHT IS PASSED IN ONCE AND EVERY PRIMITIVE OBEYS IT. Azimuth and
 * elevation in degrees. The lip always sits on the up-light shoulder, the
 * trough always on the down-light side, and casts always fall down-light. A
 * primitive that took its own light would let one frame disagree with the deck.
 *
 * COLOUR SAFETY, the 0.97 instinct. No colour helper is ever nested inside
 * another here. lerpHex and its cousins return an "rgb()" string, feeding
 * rgb(...) into a hex parser yields NaN on every channel, and canvas then
 * silently keeps the PREVIOUS fillStyle with every machine gate green.
 * Everything below resolves through an integer-indexed ramp built once.
 *
 * DETERMINISM. Every random draw goes through the seeded rng handed to
 * create(). Two runs of the same dossier produce the same image.
 *
 * USAGE
 *   <script src="@@ASSETS@@/js/noise.js"></script>
 *   <script src="@@ASSETS@@/js/akcolor.js"></script>
 *   <script src="@@ASSETS@@/js/aksection.js"></script>
 *
 *   var S = AKSECT.create({seed: 20260920, light: {azDeg: 205, elDeg: 23},
 *                          datumY: 960});
 *   var prof = S.profile({spanKm: 30, reliefPx: 180});  // x -> y, screen px
 *   S.slab(cx, {profile: prof, bottom: 1350, body:"#2C2A26",
 *               lip:"#6E6250", trough:"#131410"});
 */
(function (global) {
  "use strict";

  var DEG = Math.PI / 180;

  function need(v, name) {
    if (v == null) throw new TypeError("AKSECT: missing required option " + name);
    return v;
  }
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function lerp(a, b, t) { return a + (b - a) * t; }

  /* Seeded integer hash. Never a per-call Math.random, or a re-render of the
   * same dossier produces a different picture and the determinism contract
   * in SKILL.md is broken. */
  function hash1(i, seed) {
    var s = Math.sin(i * 127.1 + seed * 0.000173) * 43758.5453;
    return s - Math.floor(s);
  }

  function Section(o) {
    o = o || {};
    this.seed = o.seed == null ? 20260920 : o.seed;
    var L = o.light || {};
    this.azDeg = L.azDeg == null ? 205 : L.azDeg;
    this.elDeg = L.elDeg == null ? 23 : L.elDeg;
    this.datumY = o.datumY == null ? 960 : o.datumY;

    /* The light reduced to the two numbers every primitive actually needs:
     * which way is up-light in screen x, and how hard the falloff is. An
     * azimuth left of 180 lights from the left. */
    var az = this.azDeg * DEG, el = this.elDeg * DEG;
    /* AZIMUTH GIVES THE HORIZONTAL, ELEVATION GIVES THE VERTICAL (Codex, PR
     * #391). The first build took the vertical from cos(azimuth), so elDeg
     * fed nothing but `rake`, the key pointed DOWN-screen at az 205, and a
     * flat surface's upward normal (0, -1) clamped ndotl to zero: every flat
     * lit lip in the deck sat on its 0.30 floor. It also meant rotating the
     * light changed its apparent elevation, and that at az 90 or 270 the
     * vertical component vanished whatever elevation was asked for. */
    this.lightX = -Math.sin(az) * Math.cos(el);
    this.lightY = -Math.sin(el);          /* negative y is up-screen: the key is above */
    var n = Math.sqrt(this.lightX * this.lightX + this.lightY * this.lightY) || 1;
    this.lightX /= n; this.lightY /= n;
    /* A raking key spreads the shading across its range. At elevation 23 this
     * is about 0.39, which is what makes a lip read as a lip. */
    this.rake = Math.cos(this.elDeg * DEG) * 0.42;
  }

  /* ------------------------------------------------------------- profile
   * A deterministic terrain profile across the section.
   *
   * HONESTY NOTE, and it is load bearing. This repo commits Alaska boroughs,
   * places and the state outline; it commits NO elevation data. So this
   * profile is a DRAWING PROPERTY and never a measurement, and any dossier
   * using it marks the bullet [design]. It is shaped, not surveyed: a broad
   * bench rising inland with fbm relief on top, which is what a Kenai
   * transect looks like without claiming what one IS.
   */
  Section.prototype.profile = function (o) {
    o = o || {};
    var relief = o.reliefPx == null ? 160 : o.reliefPx;
    var freq = o.freq == null ? 2.4 : o.freq;
    var oct = o.octaves == null ? 5 : o.octaves;
    var rise = o.risePx == null ? 90 : o.risePx;
    var seed = this.seed + (o.salt || 0);
    var datum = this.datumY;
    var W = o.width == null ? 1080 : o.width;

    return function (x) {
      var t = x / W;
      /* the inland rise, a smoothstep so both ends are flat enough to carry
       * a datum readout without the terrain fighting the type */
      var s = t * t * (3 - 2 * t);
      var h = rise * s;
      /* fbm relief, seeded */
      var amp = relief, f = freq, sum = 0, norm = 0;
      for (var i = 0; i < oct; i++) {
        sum += amp * AK.simplex2(t * f + seed * 0.001, seed * 0.007 + i * 3.1);
        norm += amp;
        amp *= 0.5; f *= 2.0;
      }
      var r = norm ? (sum / norm) * relief : 0;
      return datum - h - r * 0.5;
    };
  };

  /* ---------------------------------------------------------------- slab
   * The modelled earth. A filled body, a LIT TOP LIP that follows the
   * profile, and a dark trough at the cut plane beneath the lip. Three
   * filled bands, never a stroked outline.
   */
  Section.prototype.slab = function (cx, o) {
    var prof = need(o.profile, "profile");
    var bottom = o.bottom == null ? 1350 : o.bottom;
    var W = o.width == null ? 1080 : o.width;
    var x0 = o.x0 == null ? 0 : o.x0;
    var body = o.body || "#2C2A26";
    var lip = o.lip || "#6E6250";
    var trough = o.trough || "#131410";
    var lipPx = o.lipPx == null ? 7 : o.lipPx;
    var troughPx = o.troughPx == null ? 22 : o.troughPx;
    var step = o.step == null ? 2 : o.step;
    var x;

    /* 1. the body */
    cx.save();
    cx.beginPath();
    cx.moveTo(x0, bottom);
    for (x = x0; x <= x0 + W; x += step) cx.lineTo(x, prof(x));
    cx.lineTo(x0 + W, bottom);
    cx.closePath();
    cx.fillStyle = body;
    cx.fill();

    /* 2. the trough, a dark band hugging the underside of the surface. This
     * is the shadowed shoulder of the cut and it is what makes the lip read.
     * Drawn BEFORE the lip so the lip sits on top of it. */
    cx.beginPath();
    for (x = x0; x <= x0 + W; x += step) cx.lineTo(x, prof(x));
    for (x = x0 + W; x >= x0; x -= step) cx.lineTo(x, prof(x) + troughPx);
    cx.closePath();
    cx.fillStyle = trough;
    cx.globalAlpha = 0.85;
    cx.fill();
    cx.globalAlpha = 1;

    /* 3. the lit lip, whose THICKNESS varies with how the surface faces the
     * key. A flat-on face gets the full lip; a face turned away gets almost
     * none. This is the whole difference between a modelled edge and a
     * stroked outline, and it is why lipPx is a maximum rather than a width. */
    cx.beginPath();
    var first = true;
    for (x = x0; x <= x0 + W; x += step) {
      var y = prof(x);
      var dy = prof(x + step) - y;
      var nx = dy, ny = -step;                 /* surface normal, unnormalised */
      var nl = Math.sqrt(nx * nx + ny * ny) || 1;
      var ndotl = clamp((nx / nl) * this.lightX + (ny / nl) * this.lightY, 0, 1);
      var w = lipPx * (0.30 + 0.70 * Math.pow(ndotl, 1.15)) * (0.55 + this.rake);
      if (first) { cx.moveTo(x, y); first = false; } else cx.lineTo(x, y);
      cx.lineTo(x, y);
      cx.rect(x, y, step + 0.6, Math.max(0.6, w));
    }
    cx.fillStyle = lip;
    cx.fill();
    cx.restore();
    return this;
  };

  /* -------------------------------------------------------------- ribbon
   * A line across AIR. Tapered at both ends, fat in the middle, drawn as a
   * filled polygon with an optional casing. NEVER a stroked path, because a
   * constant-weight stroke is a drawing of a wire lying on top of the scene.
   *
   * pts is a polyline in design px. Returns the polygon it filled so a caller
   * can declare it.
   */
  Section.prototype.ribbon = function (cx, pts, o) {
    o = o || {};
    var wMax = o.w == null ? 7 : o.w;
    var hex = o.hex || "#FFC72C";
    var casing = o.casing || null;
    var casePx = o.casePx == null ? 2.2 : o.casePx;
    var taper = o.taper == null ? 0.82 : o.taper;   /* how fat the middle is */
    if (!pts || pts.length < 2) return null;

    /* cumulative length, so the taper follows arc length and not index */
    var seg = [0], total = 0, i;
    for (i = 1; i < pts.length; i++) {
      var dx = pts[i][0] - pts[i - 1][0], dy = pts[i][1] - pts[i - 1][1];
      total += Math.sqrt(dx * dx + dy * dy);
      seg.push(total);
    }
    if (!total) return null;

    /* A TWO POINT RIBBON HAD NO BODY (Codex, PR #391). widthAt() tapers to
     * nothing at t = 0 and t = 1, and a two point polyline samples nothing
     * else, so the coloured polygon had zero area and every locator tick
     * rendered as bare casing. The path is resampled so the taper always has
     * interior points to be expressed at, whatever the caller passed. */
    var DENSE = 6;
    if (total / (pts.length - 1) > DENSE) {
      var dense = [pts[0]];
      for (i = 1; i < pts.length; i++) {
        var ax = pts[i - 1][0], ay = pts[i - 1][1];
        var bx = pts[i][0], by = pts[i][1];
        var segLen = Math.sqrt((bx - ax) * (bx - ax) + (by - ay) * (by - ay));
        var steps = Math.max(1, Math.ceil(segLen / DENSE));
        for (var q = 1; q <= steps; q++) {
          dense.push([ax + (bx - ax) * q / steps, ay + (by - ay) * q / steps]);
        }
      }
      pts = dense;
      seg = [0]; total = 0;
      for (i = 1; i < pts.length; i++) {
        var ddx = pts[i][0] - pts[i - 1][0], ddy = pts[i][1] - pts[i - 1][1];
        total += Math.sqrt(ddx * ddx + ddy * ddy);
        seg.push(total);
      }
      if (!total) return null;
    }

    function widthAt(t) {
      /* sin gives a true taper to nothing at both ends */
      return wMax * Math.pow(Math.sin(Math.PI * clamp(t, 0, 1)), taper);
    }

    function side(sign, pad) {
      var out = [];
      for (var k = 0; k < pts.length; k++) {
        var p = pts[k];
        var prev = pts[k - 1] || pts[k];
        var next = pts[k + 1] || pts[k];
        var tx = next[0] - prev[0], ty = next[1] - prev[1];
        var tl = Math.sqrt(tx * tx + ty * ty) || 1;
        var nx = -ty / tl, ny = tx / tl;
        /* the casing tapers WITH the ribbon, or a ribbon that ends in a
         * point ends in a blunt casing-coloured cap instead */
        var tt = seg[k] / total;
        var ww = widthAt(tt);
        var w = ww * 0.5 + pad * clamp(ww / (wMax * 0.28), 0, 1);
        out.push([p[0] + nx * w * sign, p[1] + ny * w * sign]);
      }
      return out;
    }

    function fillPoly(pad, colour) {
      var a = side(1, pad), b = side(-1, pad);
      cx.beginPath();
      cx.moveTo(a[0][0], a[0][1]);
      for (var k = 1; k < a.length; k++) cx.lineTo(a[k][0], a[k][1]);
      for (var m = b.length - 1; m >= 0; m--) cx.lineTo(b[m][0], b[m][1]);
      cx.closePath();
      cx.fillStyle = colour;
      cx.fill();
    }

    cx.save();
    if (casing) fillPoly(casePx, casing);
    fillPoly(0, hex);
    cx.restore();
    return pts;
  };

  /* -------------------------------------------------------------- incise
   * A line ON GROUND. A cut, drawn as a bright lip on the up-light shoulder
   * and a dark trough on the down-light side. Two filled bands offset
   * perpendicular to the path, so the groove has width, depth and a light
   * direction. Never one stroked path.
   */
  Section.prototype.incise = function (cx, pts, o) {
    o = o || {};
    var w = o.w == null ? 5 : o.w;
    var lip = o.lip || "#8A7A62";
    var trough = o.trough || "#0B0C08";
    if (!pts || pts.length < 2) return null;
    var lx = this.lightX, ly = this.lightY;

    function band(offset, thick, colour, alpha) {
      cx.beginPath();
      var first = true;
      for (var k = 0; k < pts.length; k++) {
        var p = pts[k];
        var prev = pts[k - 1] || pts[k];
        var next = pts[k + 1] || pts[k];
        var tx = next[0] - prev[0], ty = next[1] - prev[1];
        var tl = Math.sqrt(tx * tx + ty * ty) || 1;
        var nx = -ty / tl, ny = tx / tl;
        var x = p[0] + nx * offset, y = p[1] + ny * offset;
        if (first) { cx.moveTo(x, y); first = false; } else cx.lineTo(x, y);
      }
      for (var m = pts.length - 1; m >= 0; m--) {
        var q = pts[m];
        var pv = pts[m - 1] || pts[m];
        var nx2 = pts[m + 1] || pts[m];
        var ux = nx2[0] - pv[0], uy = nx2[1] - pv[1];
        var ul = Math.sqrt(ux * ux + uy * uy) || 1;
        var mx = -uy / ul, my = ux / ul;
        cx.lineTo(q[0] + mx * (offset + thick), q[1] + my * (offset + thick));
      }
      cx.closePath();
      cx.globalAlpha = alpha == null ? 1 : alpha;
      cx.fillStyle = colour;
      cx.fill();
      cx.globalAlpha = 1;
    }

    /* WHICH SIDE IS UP-LIGHT IS A PROPERTY OF THE PATH, NOT OF THE GLOBAL Y
     * (Codex, PR #391). The first build read `lx * 0 + ly * -1`, so the
     * horizontal key was multiplied out and a vertical groove could not put
     * its lip up-light at all. A single-offset band can only take one side,
     * so the side comes from the path's MEAN normal against the key. */
    var mnx = 0, mny = 0;
    for (var s0 = 0; s0 < pts.length; s0++) {
      var pp = pts[s0 - 1] || pts[s0], nn = pts[s0 + 1] || pts[s0];
      var sx = nn[0] - pp[0], sy = nn[1] - pp[1];
      var sl = Math.sqrt(sx * sx + sy * sy) || 1;
      mnx += -sy / sl; mny += sx / sl;
    }
    var ml = Math.sqrt(mnx * mnx + mny * mny) || 1;
    mnx /= ml; mny /= ml;

    cx.save();
    /* the trough first, centred on the path and biased down-light */
    band(-w * 0.5, w, trough, 0.92);
    /* then the lit lip on the up-light shoulder, thinner and brighter */
    var upSign = (mnx * lx + mny * ly) >= 0 ? 1 : -1;
    band(upSign * w * 0.5, Math.max(1.2, w * 0.36), lip, 0.95);
    cx.restore();
    return pts;
  };

  /* ---------------------------------------------------------------- step
   * One terrace. A modelled tread and riser with AO in the inside corner, so
   * a row of them reads as cut steps rather than as stacked rectangles.
   */
  Section.prototype.step = function (cx, o) {
    var x = need(o.x, "x"), y = need(o.y, "y");
    var w = need(o.w, "w"), h = need(o.h, "h");
    var tread = o.tread || "#3A382F";
    var riser = o.riser || "#1D1E19";
    var lip = o.lip || "#8A7A62";
    var ao = o.ao == null ? 0.55 : o.ao;

    cx.save();
    /* riser, the vertical face, in shadow */
    cx.fillStyle = riser;
    cx.fillRect(x, y, w, h);
    /* AO in the inside corner, a short vertical gradient at the top of the
     * riser. This is a SUBTRACTION and it needs the riser under it. */
    var g = cx.createLinearGradient(0, y, 0, y + Math.min(18, h));
    g.addColorStop(0, "rgba(0,0,0," + ao + ")");
    g.addColorStop(1, "rgba(0,0,0,0)");
    cx.fillStyle = g;
    cx.fillRect(x, y, w, Math.min(18, h));
    /* tread, the horizontal face, catching the key */
    cx.fillStyle = tread;
    cx.fillRect(x, y - 5, w, 5);
    /* the lit nosing */
    cx.fillStyle = lip;
    cx.fillRect(x, y - 6.4, w, 2.0);
    cx.restore();
    return this;
  };

  /* ------------------------------------------------------------ scaleBar
   * An INCISED checkerboard scale bar. Modelled, never a hairline rule.
   * The caller supplies the span label; the bar itself is [design].
   */
  Section.prototype.scaleBar = function (cx, o) {
    var x = need(o.x, "x"), y = need(o.y, "y");
    var w = o.w == null ? 220 : o.w;
    var h = o.h == null ? 11 : o.h;
    var cells = o.cells == null ? 4 : o.cells;
    var dark = o.dark || "#0B0C08";
    var light = o.light || "#8A7A62";
    var cw = w / cells;
    cx.save();
    /* trough the whole length first, so every cell sits in a real groove */
    cx.fillStyle = dark;
    cx.fillRect(x - 1.5, y - 1.5, w + 3, h + 3);
    for (var i = 0; i < cells; i++) {
      cx.fillStyle = (i % 2 === 0) ? light : dark;
      cx.fillRect(x + i * cw, y, cw, h);
    }
    /* the lit upper lip of the groove */
    cx.fillStyle = light;
    cx.globalAlpha = 0.75;
    cx.fillRect(x - 1.5, y - 2.6, w + 3, 1.6);
    cx.globalAlpha = 1;
    cx.restore();
    return this;
  };

  /* ------------------------------------------------------------ contact
   * A lit ground pool, then an ATTACHED cast thrown down-light into it.
   * Screened, not painted, because a painted radial pool centred on an
   * object reads as a spotlight with a hole in it (instinct 0.98).
   * Call BEFORE the object is drawn.
   */
  Section.prototype.contact = function (cx, o) {
    var cxx = need(o.x, "x"), cyy = need(o.y, "y");
    var w = o.w == null ? 90 : o.w;
    var castHex = o.cast || "#0B0C08";
    var squash = o.squash == null ? 0.26 : o.squash;
    /* HOW FAR THE CAST IS THROWN, in px of key direction. The default of
     * 5 is right for a small object sitting flat, and wrong for anything
     * whose own silhouette covers the pool: a ring 88 px across leaves the
     * shadow nowhere to be measured, and qa.py reads the object's own lit
     * face as the shadow. At el 23 a raking key throws a long way, so a
     * wide object asks for a long throw rather than a wider pool. */
    var throwPx = o.offPx == null ? 5 : o.offPx;

    /* A CONTACT SHADOW IS A SUBTRACTION AND NOTHING ELSE (2026-09-20).
     *
     * The first build of this chassis screened a warm pool under the object
     * and then cast into it. qa.py failed every declaration that used it, and
     * the message was the right one: "Light painted where the slide declared
     * dark is a glow with no source in the picture, and the dL measurement
     * can't see it because a bright pool beside a dark hole passes a
     * difference test." The pool was also landing ON the rect the slide
     * declared as shadow, so the measurement was reading the pool.
     *
     * The ground in this deck is an engraved slab that already carries the
     * key. It does not need a painted light and it never did. So this draws
     * ONLY the attached cast, down-light, as a genuine subtraction from
     * whatever the picture's own light put there.
     *
     * CANVAS HAS NO ELLIPTICAL GRADIENT, so the ramp is built on a circle
     * inside a scaled transform; poured straight into an ellipse it stops on
     * the short axis while still carrying alpha and leaves a hard arc.
     */
    var off = this.lightX * -1;
    cx.save();
    cx.globalAlpha = o.alpha == null ? 0.82 : o.alpha;
    cx.translate(cxx + off * throwPx, cyy + 3);
    cx.scale(1, squash);
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, w * 0.52);
    g.addColorStop(0.00, castHex);
    g.addColorStop(0.45, "rgba(8,9,6,0.62)");
    g.addColorStop(1.00, "rgba(0,0,0,0)");
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(0, 0, w * 0.52, 0, Math.PI * 2); cx.fill();
    cx.restore();

    /* the tight core, where the object actually touches. Narrow, dark and
     * ATTACHED, because a gap is what reads as a hole. */
    cx.save();
    cx.globalAlpha = 0.9;
    cx.translate(cxx + off * throwPx * 0.6, cyy + 1);
    cx.scale(1, squash * 0.8);
    var g2 = cx.createRadialGradient(0, 0, 0, 0, 0, w * 0.30);
    g2.addColorStop(0.00, "#050604");
    g2.addColorStop(1.00, "rgba(5,6,4,0)");
    cx.fillStyle = g2;
    cx.beginPath(); cx.arc(0, 0, w * 0.30, 0, Math.PI * 2); cx.fill();
    cx.restore();
    return this;
  };

  /* ------------------------------------------------------------- locator
   * D4, the locator key. The deck's ONLY plan view: a small incised window in
   * the upper right carrying the true Kenai Peninsula Borough outline in the
   * canonical projection, with the section's own transect stamped across it,
   * and a per-slide STATE that is the only thing allowed to change.
   *
   * It lives in the chassis rather than in nine slides because furniture that
   * is redrawn frame by frame stops being furniture. A reader only tracks a
   * key if the window, the projection and the transect are pixel-identical
   * every time and the state is the one variable. Nine hand-written copies
   * guarantee the opposite, and round one of 2026-09-20's pixel review found
   * the cheaper failure mode first: it was promised in every dossier and
   * drawn on no frame at all.
   *
   * THERE ARE NO LETTERS IN HERE. The slide contract keeps text in the DOM,
   * so the transect is stamped as an incised line ticked at both ends and the
   * A end is marked by the state that needs it, never by a drawn glyph.
   *
   * Requires d3 (projection + path) and GeoJSON the caller has already
   * fetched, so the key never guesses at geography it was not handed.
   *
   *   S.locator(cx, {x: 820, y: 150, borough: kpb, release: [-151.55, 59.64]})
   */
  Section.prototype.locator = function (cx, o) {
    if (typeof d3 === "undefined") throw new Error("AKSECT.locator requires d3");
    var x = need(o.x, "x"), y = need(o.y, "y");
    var s = o.size == null ? 180 : o.size;
    var borough = need(o.borough, "borough");
    var pad = Math.max(9, s * 0.10);
    var gold = o.gold || "#FFC72C";
    var blue = o.blue || "#6EA5FF";
    var bone = o.bone || "#C6D4DC";
    var hero = !!o.hero;
    var seed = this.seed + 419;

    var fitTo = o.inset ? need(o.state, "state") : borough;
    var proj = d3.geoConicEqualArea().parallels([55, 65]).rotate([154, 0])
      .fitExtent([[x + pad, y + pad], [x + s - pad, y + s - pad]], fitTo);
    var gp = d3.geoPath(proj, cx);

    cx.save();

    /* 1. the window itself, and it is OPAQUE on purpose.
     * A plan view and a section are two coordinate spaces, and a section
     * line that runs visibly across the plan makes them one air. Round two
     * called the translucent first build a decal for exactly that reason.
     * Filled solid and drawn last, the window OCCLUDES whatever the frame
     * ran past it, which turns the collision into the cleanest depth cue
     * on the page. */
    cx.fillStyle = "#0A121C";
    cx.fillRect(x, y, s, s);
    /* the recess: a lit inner bevel on the up-light side, dark opposite */
    cx.fillStyle = "#46545F";
    cx.fillRect(x, y, s, 2); cx.fillRect(x, y, 2, s);
    cx.fillStyle = "#080D14";
    cx.fillRect(x, y + s - 2, s, 2); cx.fillRect(x + s - 2, y, 2, s);
    this.incise(cx, [[x, y], [x + s, y], [x + s, y + s], [x, y + s], [x, y]],
                { w: 3.4, lip: "#6E6250", trough: "#0B0C08" });

    /* 2. the geography. Alaska first when the key is inset, so the borough
     *    reads as a piece OF something and not as an island. */
    if (o.inset) {
      cx.beginPath(); gp(o.state);
      cx.fillStyle = "#151C22"; cx.fill();
      cx.lineWidth = 1.0; cx.strokeStyle = "#39454E"; cx.stroke();
    }

    /* 3. state ground under the borough, when the slide is about whose land
     *    it is. Continuous, because that is the claim. */
    if (o.parcels) {
      cx.save();
      cx.beginPath(); gp(borough); cx.clip();
      cx.fillStyle = "#3A3222"; cx.globalAlpha = 0.85;
      cx.fillRect(x, y, s, s);
      cx.globalAlpha = 1;
      /* and the borough's own reach scattered across it, DISCONTINUOUS,
       * because a second-class borough's land is parcels and not a blanket */
      for (var p = 0; p < 90; p++) {
        var px = x + pad + hash1(p * 2 + 1, seed) * (s - pad * 2);
        var py = y + pad + hash1(p * 2 + 2, seed) * (s - pad * 2);
        var pr = 0.9 + hash1(p + 700, seed) * 1.5;
        cx.globalAlpha = 0.42 + hash1(p + 900, seed) * 0.5;
        cx.fillStyle = blue;
        cx.beginPath(); cx.arc(px, py, pr, 0, Math.PI * 2); cx.fill();
      }
      cx.globalAlpha = 1;
      cx.restore();
    }

    /* 4. the borough outline. Weight is the state, not a decoration: hero
     *    weight is how the key says THIS frame is inside the borough. */
    cx.beginPath(); gp(borough);
    if (!o.inset && !o.parcels) { cx.fillStyle = "#101820"; cx.fill(); }
    cx.lineWidth = hero ? 2.6 : 1.4;
    cx.strokeStyle = hero ? bone : "#8FA3B0";
    cx.stroke();
    if (hero) {
      /* a lit shoulder on the up-light side of the outline, so hero weight
       * reads as a raised edge rather than as a thicker pen */
      cx.save();
      cx.translate(this.lightX * 1.3, -Math.abs(this.lightY) * 1.3);
      cx.beginPath(); gp(borough);
      cx.lineWidth = 1.0; cx.globalAlpha = 0.55;
      cx.strokeStyle = "#F4F8FF"; cx.stroke();
      cx.restore();
    }

    /* 5. the transect, stamped across the key in the same ink the section
     *    uses for its datum, with a tick at each end. */
    /* A TRANSECT HAS TO CROSS THE THING IT CUTS (round two).
     * The first build incised the line between the two true endpoints,
     * which at borough extent is a 25 px scratch in the middle of a 180 px
     * key: "at full size it is barely findable and at 432 px the key is a
     * bare outline." The cut is now extended along its own bearing to the
     * window edges and clipped there, so it reads as a section line drawn
     * across a plan, while the TICKS stay on the real endpoints and a
     * filled square marks the A end, which is where the reader stands. */
    var tr = o.transect;
    var a = null, b = null;
    if (tr) {
      a = proj(tr[0]); b = proj(tr[1]);
      if (a && b) {
        var tx = b[0] - a[0], ty = b[1] - a[1];
        var tl = Math.sqrt(tx * tx + ty * ty) || 1;
        var ux = tx / tl, uy = ty / tl;
        cx.save();
        cx.beginPath(); cx.rect(x + 2, y + 2, s - 4, s - 4); cx.clip();
        this.incise(cx, [[a[0] - ux * s, a[1] - uy * s],
                         [b[0] + ux * s, b[1] + uy * s]],
                    { w: 3.0, lip: "#DCE6EC", trough: "#05070A" });
        cx.restore();
        var nx = -uy * 5.4, ny = ux * 5.4;
        cx.beginPath();
        cx.moveTo(a[0] - nx, a[1] - ny); cx.lineTo(a[0] + nx, a[1] + ny);
        cx.moveTo(b[0] - nx, b[1] - ny); cx.lineTo(b[0] + nx, b[1] + ny);
        cx.lineWidth = 2.0; cx.strokeStyle = "#DCE6EC"; cx.stroke();
        /* the A end, a filled square: the station the section is drawn from */
        cx.fillStyle = "#F4F8FF";
        cx.fillRect(a[0] - 2.6, a[1] - 2.6, 5.2, 5.2);
      }
    }

    /* 6. the states that add a mark */
    if (o.release) {
      var r = proj(o.release);
      if (r) {
        cx.beginPath(); cx.arc(r[0], r[1], 3.4, 0, Math.PI * 2);
        cx.fillStyle = gold; cx.fill();
        cx.beginPath(); cx.arc(r[0], r[1], 6.2, 0, Math.PI * 2);
        cx.lineWidth = 1.0; cx.globalAlpha = 0.55;
        cx.strokeStyle = gold; cx.stroke(); cx.globalAlpha = 1;
      }
    }
    if (o.aDot && a) {
      cx.beginPath(); cx.arc(a[0], a[1], 3.8, 0, Math.PI * 2);
      cx.fillStyle = gold; cx.fill();
    }
    if (o.ring) {
      var rg = proj(o.ring);
      if (rg) {
        /* EMPTY on purpose. Juneau is where the bill would have been filed. */
        cx.beginPath(); cx.arc(rg[0], rg[1], 5.0, 0, Math.PI * 2);
        cx.lineWidth = 1.8; cx.strokeStyle = gold; cx.stroke();
      }
    }
    if (o.ticks) {
      /* notice leaving the key through its own top edge, which is the whole
       * of D1 compressed into 180 px */
      for (var t = 0; t < o.ticks; t++) {
        var gx = x + s * (0.42 + t * 0.21);
        this.ribbon(cx, [[gx, y + s * 0.34], [gx + 2, y - 16]],
                    { w: 5.0, hex: gold, casing: "#5A4A18", casePx: 1.8,
                      taper: 0.5 });
      }
    }

    cx.restore();
    return { box: [x, y, s, s], project: proj };
  };

  /* -------------------------------------------------------------- strata
   * BEDS IN THE SLAB, and the reason this exists is a measurement.
   *
   * The 2026-09-20 scorer put artwork craft at 6 and named the cause: the
   * earth on five frames was "a large flat brown field carrying only faint
   * contour squiggles across roughly a third of each frame", which is the
   * deck's own banned failure wearing a texture. More hatching does not fix
   * it. An engraved lay is TONE; what a flat field is short of is STRUCTURE,
   * and a section's structure is beds.
   *
   * So this draws n beds parallel to the surface, each a filled polygon with
   * a lit upper lip and a shadowed base, thinning with depth the way a
   * section's beds do, with sparse clasts sitting in them. Every mark is a
   * fill, so the drawn share goes up rather than down.
   *
   * It is a DRAWING PROPERTY and never a measurement: this repo commits no
   * Alaska stratigraphy any more than it commits elevation, and any dossier
   * using it marks the bullet [design].
   */
  Section.prototype.strata = function (cx, o) {
    var prof = need(o.profile, "profile");
    var bottom = o.bottom == null ? 1350 : o.bottom;
    var W = o.width == null ? 1080 : o.width;
    var x0 = o.x0 == null ? 0 : o.x0;
    var n = o.beds == null ? 6 : o.beds;
    var top = o.topPx == null ? 70 : o.topPx;   /* first bed below the surface */
    var lip = o.lip || "#6E6250";
    var base = o.base || "#16150F";
    var body = o.body || "#33302A";
    var seed = this.seed + (o.salt || 0) + 911;
    var step = o.step == null ? 6 : o.step;
    var x, i, k;
    /* the earth actually available below the surface, measured across the run */
    var surf = prof(x0 + W * 0.5);
    for (x = x0; x <= x0 + W; x += 60) surf = Math.max(surf, prof(x));
    var span = Math.max(top + 40, bottom - surf);

    cx.save();
    for (i = 0; i < n; i++) {
      var t0 = i / n;
      /* THE DEPTH RANGE IS THE SLAB, NOT THE CANVAS (Codex, PR #391).
       * `bottom` is an absolute canvas coordinate and bedY() adds depth to
       * prof(x), so subtracting `top` from it treated almost the whole frame
       * as available earth: with the defaults the third bed started 476 px
       * below a surface at 960 and every bed after it fell off the canvas, so
       * `beds: 6` rendered about two. */
      var depth = top + Math.pow(t0, 0.82) * (span - top) * 0.88;
      var thick = (o.thickPx == null ? 52 : o.thickPx) * (1 - t0 * 0.58);
      var amp = 9 + hash1(i * 7 + 1, seed) * 13;
      var freq = 0.0035 + hash1(i * 11 + 2, seed) * 0.004;
      var ph = hash1(i * 13 + 3, seed) * 6.28;
      function bedY(xx) {
        return prof(xx) + depth + Math.sin(xx * freq + ph) * amp;
      }
      /* the bed body */
      cx.beginPath();
      for (x = x0; x <= x0 + W; x += step) cx.lineTo(x, bedY(x));
      for (x = x0 + W; x >= x0; x -= step) cx.lineTo(x, bedY(x) + thick);
      cx.closePath();
      cx.globalAlpha = 0.55 - t0 * 0.18;
      cx.fillStyle = body;
      cx.fill();
      /* the shadowed base, drawn first so the lip sits over it */
      cx.beginPath();
      for (x = x0; x <= x0 + W; x += step) cx.lineTo(x, bedY(x) + thick - 4);
      for (x = x0 + W; x >= x0; x -= step) cx.lineTo(x, bedY(x) + thick + 2.4);
      cx.closePath();
      cx.globalAlpha = 0.72;
      cx.fillStyle = base;
      cx.fill();
      /* the lit upper lip, thinner where the bed dips away from the key */
      cx.beginPath();
      for (x = x0; x <= x0 + W; x += step) {
        var dy = bedY(x + step) - bedY(x);
        var nl = Math.sqrt(dy * dy + step * step) || 1;
        var ndotl = clamp((dy / nl) * this.lightX + (-step / nl) * this.lightY, 0, 1);
        cx.rect(x, bedY(x) - 1.0, step + 0.8,
                Math.max(0.7, 2.6 * (0.34 + 0.66 * ndotl)));
      }
      cx.globalAlpha = 0.62 - t0 * 0.16;
      cx.fillStyle = lip;
      cx.fill();
      /* clasts: a few pebbles sitting IN the bed, each with its own lit crown */
      var clasts = Math.max(0, (o.clasts == null ? 7 : o.clasts) - i);
      for (k = 0; k < clasts; k++) {
        var cxp = x0 + hash1(i * 31 + k * 3 + 5, seed) * W;
        var cyp = bedY(cxp) + thick * (0.3 + hash1(i * 17 + k, seed) * 0.4);
        var cr = 2.4 + hash1(i * 23 + k * 5, seed) * 4.2;
        cx.globalAlpha = 0.85;
        cx.fillStyle = base;
        cx.beginPath();
        cx.ellipse(cxp, cyp, cr, cr * 0.74, 0, 0, Math.PI * 2);
        cx.fill();
        cx.fillStyle = lip;
        cx.globalAlpha = 0.7;
        cx.beginPath();
        cx.ellipse(cxp + this.lightX * cr * 0.3, cyp - cr * 0.34,
                   cr * 0.62, cr * 0.3, 0, 0, Math.PI * 2);
        cx.fill();
      }
    }
    cx.globalAlpha = 1;
    cx.restore();
    return this;
  };

  /* --------------------------------------------------------- counterTick
   * The deck header declares "a 6 px counter tick which is a declared
   * fixture on all nine", and slide 04's acceptance list is built on it:
   * that frame holds the notice path out entirely, so the tick is its only
   * tie to what gold means here. Round two found it drawn on no frame. It
   * lives in the chassis so nine frames cannot disagree about where the
   * one fixture sits.
   */
  Section.prototype.counterTick = function (cx, o) {
    o = o || {};
    var x = o.x == null ? 866 : o.x;
    var y = o.y == null ? 96 : o.y;
    cx.save();
    cx.fillStyle = o.hex || "#FFC72C";
    cx.fillRect(x, y, 6, o.h == null ? 26 : o.h);
    cx.restore();
    return this;
  };

  global.AKSECT = {
    create: function (o) { return new Section(o); },
    _Section: Section
  };
})(this);
