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
    var az = this.azDeg * DEG;
    this.lightX = -Math.sin(az);          /* screen x component of the key */
    this.lightY = -Math.cos(az) * 0.35;   /* shallow, this is a section */
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
        var w = widthAt(seg[k] / total) * 0.5 + pad;
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

    cx.save();
    /* the trough first, centred on the path and biased down-light */
    band(-w * 0.5, w, trough, 0.92);
    /* then the lit lip on the up-light shoulder, thinner and brighter */
    var upSign = (lx * 0 + ly * -1) >= 0 ? -1 : 1;
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
    cx.translate(cxx + off * 5, cyy + 3);
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
    cx.translate(cxx + off * 3, cyy + 1);
    cx.scale(1, squash * 0.8);
    var g2 = cx.createRadialGradient(0, 0, 0, 0, 0, w * 0.30);
    g2.addColorStop(0.00, "#050604");
    g2.addColorStop(1.00, "rgba(5,6,4,0)");
    cx.fillStyle = g2;
    cx.beginPath(); cx.arc(0, 0, w * 0.30, 0, Math.PI * 2); cx.fill();
    cx.restore();
    return this;
  };

  global.AKSECT = {
    create: function (o) { return new Section(o); },
    _Section: Section
  };
})(this);
