/* akpour.js -- THE NIGHT POUR, the deck chassis for carousel No.58.
 *
 * TECHNIQUE_LIBRARY 96. Committed as a MODULE rather than as per-slide code,
 * for the same reason aksheet.js was (library 95): bespoke_check strips a
 * library loaded by src= as house harness, so shared furniture costs the
 * variety budget nothing and every slide's OWN drawing code stays its own.
 *
 * THE FORM. A concrete service pad, poured tonight, still green, seen low and
 * along its length, with one work lamp on it. Nine frames dolly right along
 * one continuous pour. The pad's far edge, its front lip and its aggregate
 * field are pure functions of globalX = slideIndex * 1080 + localX, so the
 * frames seam exactly.
 *
 * WHY IT EXISTS, and the one thing it is really for. Artwork craft has been
 * the weakest scored criterion in 6 of the 10 runs before 2026-09-13, and the
 * defect classes under it ("canvas mark near reserved text", "art touching
 * glyphs", "busy art under text", "top-loaded composition") are one defect:
 * type placed onto art that was drawn without knowing the type was coming.
 *
 * So the type well here is not a plate. It is the TROWELED BAND, which is a
 * real thing a real finisher makes: a magnesium float leaves the aggregate
 * showing, a steel trowel polishes a band smooth. `aggregate()` reads the
 * measured line boxes and its stone probability RAMPS to zero near them, so
 * the colliding mark is never generated, and `troweled()` lifts the surface
 * value and drops its roughness toward the same boxes, so the material gets
 * SMOOTHER and slightly BRIGHTER as it approaches the words. That is what a
 * trowel does. There are zero plates, zero scrims and zero knockouts in this
 * deck.
 *
 * THE LIGHT IS DECLARED ONCE AND NEVER VARIES. az 152, el 22, key to fill
 * 6.0 to 1. Under the house convention (azimuth clockwise from up, screen +y
 * DOWN) az 152 resolves to LIT FROM THE LOWER RIGHT, lee falling to the upper
 * left, and every shadow in nine frames runs up and to the left. Elevation 22
 * is a craft decision and not a mood: 20 to 30 is the band where a swelled
 * line spreads across its full width range, and a high key flattens every
 * stroke in the deck to one width.
 *
 * Load AFTER noise.js, akcolor.js, aksnow.js and aknight.js.
 *   AKPOUR.LIGHT / PAL / SEED
 *   AKPOUR.gx(slideIndex)            globalX base for a frame
 *   AKPOUR.farEdge(gx)               y of the pad's far edge, pure in gx
 *   AKPOUR.lipTop(gx)                y of the front lip's top edge, pure in gx
 *   AKPOUR.night(cx)                 the sky and haze behind everything
 *   AKPOUR.pour(cx, o)               the pad's lit band
 *   AKPOUR.troweled(cx, o)           the type well, drawn as a finished band
 *   AKPOUR.aggregate(cx, o)          the exposed stone population
 *   AKPOUR.polish(cx, o)             the finisher's arcs, the only marks allowed inside the reserve
 *   AKPOUR.lip(cx, o)                the chamfered front lip
 *   AKPOUR.joint(cx, o)              the chained saw-cut control joint
 *   AKPOUR.contact(cx, o)            pool, then cast, then seam, in that order
 *   AKPOUR.reserve(sel)              per line box rects
 *   AKPOUR.dist(boxes, x, y)         distance to the nearest reserved box
 *   AKPOUR.grainOn(el)               the grain tile, never a full frame turbulence rect
 */
(function (global) {
  'use strict';

  var P = {};
  var W = 1080, H = 1350;

  P.W = W; P.H = H;

  /* ONE LIGHT, DECLARED ONCE. */
  P.LIGHT = {
    azDeg: 152, elDeg: 22, keyFill: 6.0,
    key: '#E8EEF2',
    fill: '#16212C',
    /* screen-space unit vector toward the light, house convention */
    vec: (function () {
      var az = 152 * Math.PI / 180, el = 22 * Math.PI / 180;
      return [Math.cos(el) * Math.sin(az), -Math.cos(el) * Math.cos(az), Math.sin(el)];
    })(),
    /* bearing the shadows RUN, for AKSNOW.contactShadow's dirDeg */
    shadowDeg: 242
  };

  P.PAL = {
    night:    '#05080E',
    shadow:   '#0C1620',
    pourLo:   '#263038',
    pourHi:   '#3E4A50',
    trowel:   '#2A343C',
    steel:    '#8A97A2',
    steelHi:  '#C9D4DC',
    bronzeLo: '#7A6238',
    bronzeHi: '#A8874A',
    ink:      '#F4F8FF',
    ink2:     '#9FB0BC',
    mono:     '#6E808C',
    reader:   '#6EA5FF',
    gold:     '#FFC72C',
    goldHalo: '#FFDA6E',
    site:     '#46545F',
    haze:     '#0B1A2C'
  };

  /* Union Calendar 713, plus the run date. Every generator in the deck is
   * seeded from this, so the deck is reproducible from its own committed HTML. */
  P.SEED = 7130913;

  P.gx = function (slideIndex) { return slideIndex * W; };

  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  P.clamp = clamp;

  /* ---------------------------------------------------------------- geometry
   * Both edges are PURE FUNCTIONS OF globalX, which is what makes the spine
   * seam. Never author either per slide.
   */
  P.farEdge = function (gx) {
    return 486
      + 26 * Math.sin(gx / 2100)
      + 11 * Math.sin(gx / 640 + 1.7);
  };

  P.lipTop = function (gx) {
    return 1178
      + 14 * Math.sin(gx / 2600 + 0.4)
      + 5 * Math.sin(gx / 520 + 2.2);
  };

  /* ------------------------------------------------------------------- night */
  P.night = function (cx) {
    var g = cx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, P.PAL.night);
    g.addColorStop(0.30, '#070C14');
    g.addColorStop(0.62, P.PAL.shadow);
    cx.fillStyle = g;
    cx.fillRect(0, 0, W, H);
  };

  /* -------------------------------------------------------------------- pour
   * The lit band. A real wet slab under one low lamp is brightest along a
   * wedge running from the lamp side, and falls both toward the far edge (into
   * haze) and toward the near lip (out of the lamp's throw).
   */
  P.pour = function (cx, o) {
    o = o || {};
    var gx = o.gx || 0;
    var i, x, fe, lt, t;

    /* the slab body, drawn as a filled band between two computed edges */
    cx.beginPath();
    cx.moveTo(-4, P.farEdge(gx - 4));
    for (x = 0; x <= W + 4; x += 4) cx.lineTo(x, P.farEdge(gx + x));
    for (x = W + 4; x >= -4; x -= 4) cx.lineTo(x, P.lipTop(gx + x));
    cx.closePath();
    cx.save();
    cx.clip();

    /* the lamp's throw, a circle inside a transform. NEVER an elliptical
     * gradient: createRadialGradient is a circle, and pouring one into an
     * ellipse stops the paint on the short axis while the ramp still carries
     * alpha, which draws a hard arc across the ground. */
    cx.fillStyle = P.PAL.pourLo;
    cx.fillRect(0, 0, W, H);

    var lampX = o.lampX == null ? 980 : o.lampX;
    var lampY = o.lampY == null ? 1240 : o.lampY;
    var R = 100;
    var g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    g.addColorStop(0.00, 'rgba(96,112,122,0.92)');
    g.addColorStop(0.34, 'rgba(74,90,100,0.62)');
    g.addColorStop(0.68, 'rgba(52,66,76,0.28)');
    g.addColorStop(1.00, 'rgba(40,52,60,0)');
    cx.save();
    cx.translate(lampX, lampY);
    cx.scale((o.throwRx == null ? 900 : o.throwRx) / R, (o.throwRy == null ? 520 : o.throwRy) / R);
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(0, 0, R, 0, 6.283185); cx.fill();
    cx.restore();

    /* atmospheric falloff toward the far edge, lerped as (i/n)^1.4 */
    for (i = 0; i < 26; i++) {
      t = i / 25;
      cx.globalAlpha = 0.10 * Math.pow(1 - t, 1.4);
      cx.fillStyle = P.PAL.haze;
      cx.beginPath();
      cx.moveTo(-4, P.farEdge(gx - 4));
      for (x = 0; x <= W + 4; x += 8) cx.lineTo(x, P.farEdge(gx + x) + t * 112);
      cx.lineTo(W + 4, P.farEdge(gx + W + 4));
      cx.closePath();
      cx.fill();
    }
    cx.globalAlpha = 1;

    /* the screed crown. A finisher screeds a slight crown so water runs off,
     * and it is what keeps the modelled surface from falling in ONE axis,
     * which is the failure that retraces one iso-line into a knotted ribbon. */
    for (x = 0; x <= W; x += 3) {
      fe = P.farEdge(gx + x); lt = P.lipTop(gx + x);
      var crown = 0.5 + 0.5 * Math.sin((gx + x) / 380);
      var yc = fe + (lt - fe) * (0.42 + 0.06 * crown);
      cx.globalAlpha = 0.055 + 0.035 * crown;
      cx.fillStyle = P.PAL.pourHi;
      cx.fillRect(x, yc - 26, 3, 52);
    }
    cx.globalAlpha = 1;
    cx.restore();
  };

  /* ---------------------------------------------------------------- troweled
   * THE TYPE WELL, AND IT IS PART OF THE POUR.
   *
   * A steel trowel polishes a band smooth. Toward the reserved line boxes the
   * surface value lifts and its roughness falls, so the words sit on a lit,
   * finished surface instead of in a hole. Called BEFORE aggregate().
   */
  P.troweled = function (cx, o) {
    o = o || {};
    var boxes = o.boxes || [];
    if (!boxes.length) return;
    var reach = o.reach == null ? 124 : o.reach;
    var lift = o.lift == null ? 0.30 : o.lift;
    var step = o.step == null ? 6 : o.step;
    var x, y, d, m;
    cx.save();
    for (y = 0; y < H; y += step) {
      for (x = 0; x < W; x += step) {
        d = P.dist(boxes, x, y);
        if (d > reach) continue;
        m = 1 - clamp((d - 10) / (reach - 10), 0, 1);
        cx.globalAlpha = lift * m * m;
        cx.fillStyle = P.PAL.trowel;
        cx.fillRect(x, y, step, step);
      }
    }
    /* the broad soft specular a polished band takes from a low key */
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      var g = cx.createLinearGradient(b[0], b[1] - 18, b[0] + b[2], b[1] + b[3] + 18);
      g.addColorStop(0, 'rgba(150,172,186,0)');
      g.addColorStop(0.5, 'rgba(150,172,186,' + (o.spec == null ? 0.085 : o.spec) + ')');
      g.addColorStop(1, 'rgba(150,172,186,0)');
      cx.globalAlpha = 1;
      cx.fillStyle = g;
      cx.fillRect(b[0] - 26, b[1] - 20, b[2] + 52, b[3] + 40);
    }
    cx.restore();
  };

  /* --------------------------------------------------------------- aggregate
   * EXPOSED AGGREGATE, and the reserve is structural rather than cosmetic.
   *
   * Stone probability p = clamp((d - 28) / 96, 0, 1) ^ 1.6, where d is the
   * distance in design px to the nearest reserved line box. Inside 28px no
   * stone is GENERATED, which is the whole point: there is no mark to cover,
   * so there is no plate to size wrong and no glyph for a mark to cross.
   *
   * Sizes are LOGNORMAL off a Box-Muller normal, never uniform, because
   * uniform randomness is the tell of a machine-made mark. Each stone carries
   * a lit crescent on the lamp side and a dark occlusion arc opposite, from
   * the one global light, so the population is modelled tone and not texture.
   */
  function boxMuller(rnd) {
    var u = 1 - rnd(), v = rnd();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(6.283185 * v);
  }

  P.aggregate = function (cx, o) {
    o = o || {};
    var gx = o.gx || 0;
    var rnd = global.AK.rng(o.seed == null ? P.SEED : o.seed);
    var boxes = o.boxes || [];
    var count = o.count == null ? 1000 : o.count;
    var lit = P.LIGHT.vec;
    var litAng = Math.atan2(lit[1], lit[0]);
    var placed = [], i, j, k, ok, x, y, r, d, p, s, ang;
    var DARKS = ['rgba(5,9,15,0.22)', 'rgba(5,9,15,0.28)',
                 'rgba(5,9,15,0.34)', 'rgba(5,9,15,0.40)'];
    var LIGHTS = ['rgba(90,102,110,0.24)', 'rgba(106,120,128,0.26)',
                  'rgba(122,138,148,0.28)', 'rgba(138,156,166,0.30)',
                  'rgba(154,174,186,0.32)', 'rgba(170,192,204,0.34)',
                  'rgba(186,210,222,0.36)', 'rgba(202,228,242,0.38)'];

    for (i = 0; i < count * 9; i++) {
      if (placed.length >= count) break;
      x = -20 + rnd() * (W + 40);
      var fe = P.farEdge(gx + x), lt = P.lipTop(gx + x);
      y = fe + rnd() * (lt - fe);
      if (y < fe + 6) continue;

      d = P.dist(boxes, x, y);
      p = Math.pow(clamp((d - 28) / 96, 0, 1), 1.6);
      if (rnd() > p) continue;

      /* lognormal radius, scaled down with distance up the slab so the
       * population carries a real scale gradient into the haze */
      var depth = clamp((y - fe) / Math.max(1, lt - fe), 0, 1);
      s = Math.exp(-0.30 + 0.46 * boxMuller(rnd));
      r = clamp(s * 2.1, 0.65, 4.2) * (0.52 + 0.80 * depth);
      placed.push([x, y, r]);

      /* THE TOOTH, and it is deliberately NOT a field of drawn pebbles.
       * A troweled slab at this camera distance shows a fine sand tooth, not
       * exposed aggregate, and drawing visible stones with a lit crescent and
       * a seated shadow reads as foam on water rather than as concrete. Each
       * mark is a short flattened grain lying in the finish, with its lit edge
       * on the lamp side and a darker one opposite, and the population does
       * the modelling rather than any individual mark. */
      var v = 0.34 + 0.46 * depth + 0.18 * rnd();
      ang = litAng + (rnd() - 0.5) * 1.5;

      /* QUANTISED ON PURPOSE. Every distinct colour literal a frame paints is
       * one entry in qa.py's paint census, the census has a cap, and a field
       * of a few thousand marks each with its own computed rgba() fills that
       * cap and EVICTS the deck's law-bearing inks, so the ink law then reads
       * "no brush ever carried it" about gold that is plainly on the frame.
       * Eight steps is more tonal range than the eye can separate at this mark
       * size and it costs the census eight entries instead of two thousand. */
      cx.strokeStyle = DARKS[(rnd() * 4) | 0];
      cx.lineWidth = Math.max(0.55, r * 0.52);
      cx.beginPath();
      cx.moveTo(x - Math.cos(ang) * r * 0.7 - 0.7, y - Math.sin(ang) * r * 0.7 - 0.6);
      cx.lineTo(x + Math.cos(ang) * r * 0.7 - 0.7, y + Math.sin(ang) * r * 0.7 - 0.6);
      cx.stroke();

      cx.strokeStyle = LIGHTS[Math.min(7, (v * 8) | 0)];
      cx.lineWidth = Math.max(0.5, r * 0.44);
      cx.beginPath();
      cx.moveTo(x - Math.cos(ang) * r * 0.7, y - Math.sin(ang) * r * 0.7);
      cx.lineTo(x + Math.cos(ang) * r * 0.7, y + Math.sin(ang) * r * 0.7);
      cx.stroke();
    }

    /* air voids. Dark rings with a lit lower lip, which is what a void in a
     * troweled surface actually looks like under a raking lamp. */
    var voids = o.voids == null ? 46 : o.voids;
    for (i = 0; i < voids * 8; i++) {
      if (voids <= 0) break;
      x = -10 + rnd() * (W + 20);
      var fe2 = P.farEdge(gx + x), lt2 = P.lipTop(gx + x);
      y = fe2 + rnd() * (lt2 - fe2);
      if (P.dist(boxes, x, y) < 34) continue;
      r = 0.9 + Math.abs(boxMuller(rnd)) * 1.25;
      cx.strokeStyle = 'rgba(6,10,16,0.44)';
      cx.lineWidth = 0.8;
      cx.beginPath(); cx.arc(x, y, r, 0, 6.283185); cx.stroke();
      cx.strokeStyle = 'rgba(178,198,212,0.20)';
      cx.lineWidth = 0.7;
      cx.beginPath();
      cx.arc(x, y, r * 0.8, litAng - 0.8, litAng + 0.8);
      cx.stroke();
      voids--;
    }

    return placed.length;
  };

  /* ------------------------------------------------------------------ polish
   * The finisher's swept circular arcs. These are the ONLY marks permitted
   * inside 28px of a glyph box, they run at 0.75px hair and under 6 percent
   * contrast, and they are what makes the reserve read as a finished surface
   * rather than as an absence.
   */
  var POLISH = ['rgba(168,188,202,0.032)', 'rgba(168,188,202,0.042)',
                'rgba(168,188,202,0.052)'];

  P.polish = function (cx, o) {
    o = o || {};
    var boxes = o.boxes || [];
    var rnd = global.AK.rng((o.seed == null ? P.SEED : o.seed) + 77);
    cx.save();
    cx.lineWidth = 0.75;
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      var cxp = b[0] + b[2] / 2, cyp = b[1] + b[3] / 2;
      var n = Math.max(4, Math.round(b[2] / 46));
      for (var j = 0; j < n; j++) {
        var rr = 40 + j * 34 + rnd() * 22;
        var a0 = rnd() * 6.283185, sweep = 0.6 + rnd() * 1.5;
        cx.strokeStyle = POLISH[(rnd() * 3) | 0];
        cx.beginPath();
        cx.ellipse(cxp + (rnd() - 0.5) * b[2] * 0.5, cyp + (rnd() - 0.5) * 26,
                   rr, rr * 0.34, 0, a0, a0 + sweep);
        cx.stroke();
      }
    }
    cx.restore();
  };

  /* --------------------------------------------------------------------- lip
   * THE CHAMFERED FRONT LIP, and it is why no frame in this deck has a dead
   * bottom band. Top face lit by the key, vertical riser dark, ambient falloff
   * below it. Modelled tone, never a plate and never a hairline.
   */
  var LIPTOP = ['rgba(120,138,150,0.95)', 'rgba(130,148,160,0.95)',
                'rgba(140,159,170,0.95)', 'rgba(150,169,181,0.95)',
                'rgba(160,179,191,0.95)', 'rgba(170,190,202,0.95)',
                'rgba(180,200,212,0.95)', 'rgba(190,210,222,0.95)'];

  /* -------------------------------------------------------------- bareField
   * THE DECK'S SPINE. One punched rectangular field labelled DATE OF ENACTMENT,
   * present and EMPTY on all nine frames, because the bill has no enactment
   * date and a motif that quietly stops appearing is a motif that stopped
   * arguing. The first build drew it on five frames and left it off four, and
   * the critics found the gap on every one of the four.
   *
   * A recess under a lamp at the lower right is lit on its FAR wall, which is
   * up and left, and dark on the near wall down and right. Same law as the
   * incised clause on 07 and the struck dates on 09.
   */
  P.bareField = function (cx, o) {
    o = o || {};
    var x = o.x, y = o.y,
        w = o.w == null ? 300 : o.w,
        h = o.h == null ? 84 : o.h,
        lab = o.label !== false,
        warm = o.warm === true;
    cx.save();
    cx.beginPath(); cx.rect(x, y, w, h); cx.clip();
    var g = cx.createLinearGradient(x, y, x + w * 0.55, y + h);
    if (warm) {
      g.addColorStop(0, '#231A0C'); g.addColorStop(0.62, '#100B05'); g.addColorStop(1, '#05040A');
    } else {
      g.addColorStop(0, '#1A2530'); g.addColorStop(0.62, '#0B121A'); g.addColorStop(1, '#05080E');
    }
    cx.fillStyle = g; cx.fillRect(x, y, w, h);
    /* the floor's own tooth, so the recess is a place the material is FLAT and
     * not a place it is absent */
    for (var i = 0; i < 7; i++) {
      cx.strokeStyle = 'rgba(150,176,192,' + (0.05 + 0.012 * i) + ')';
      cx.lineWidth = 0.7;
      cx.beginPath();
      cx.moveTo(x + 7, y + 9 + i * (h - 18) / 6);
      cx.lineTo(x + w - 7, y + 8 + i * (h - 18) / 6);
      cx.stroke();
    }
    cx.restore();
    /* lit far wall, top and left */
    cx.strokeStyle = 'rgba(196,220,236,0.55)'; cx.lineWidth = 2.4;
    cx.beginPath();
    cx.moveTo(x, y + h); cx.lineTo(x, y); cx.lineTo(x + w, y); cx.stroke();
    /* near wall in the lee, right and bottom */
    cx.strokeStyle = 'rgba(4,7,12,0.94)'; cx.lineWidth = 4;
    cx.beginPath();
    cx.moveTo(x + w, y); cx.lineTo(x + w, y + h); cx.lineTo(x, y + h); cx.stroke();
    if (lab) {
      cx.save();
      cx.font = '500 ' + (o.labelPx || 20) + 'px "JetBrains Mono", monospace';
      cx.textAlign = 'left';
      cx.fillStyle = 'rgba(6,11,17,0.8)';
      cx.fillText('DATE OF ENACTMENT', x + 0.9, y - 13.1);
      cx.fillStyle = 'rgba(178,198,212,0.90)';
      cx.fillText('DATE OF ENACTMENT', x, y - 14);
      cx.restore();
    }
  };

  /* ---------------------------------------------------------------- falloff
   * THE NOTAN WELD. One lamp at a named point means the frame gets darker with
   * distance from it, and that is not decoration: `value_structure.py` reads
   * the 432 px thumb for MASSES, and this deck's first build scattered its
   * darks across five separate shapes on three frames while three more had no
   * mass over half the frame. A monotone falloff from the lamp welds the top
   * band, the far corners and the lower lee into ONE connected dark and puts
   * the dominant mass over the line, by moving light rather than by laying a
   * plate over anything.
   *
   * Four stops, all one rgb with four alphas, because the paint census caps
   * near 160 distinct literals and a free running gradient is how a law
   * bearing ink gets evicted from it. Text is DOM and sits above the canvas,
   * so this only ever raises type contrast.
   */
  P.falloff = function (cx, o) {
    o = o || {};
    var lx = o.lampX == null ? 980 : o.lampX,
        ly = o.lampY == null ? 1250 : o.lampY,
        r0 = o.inner == null ? 300 : o.inner,
        r1 = o.outer == null ? 1520 : o.outer,
        k  = o.strength == null ? 0.52 : o.strength;
    var g = cx.createRadialGradient(lx, ly, r0, lx, ly, r1);
    g.addColorStop(0.00, 'rgba(3,6,11,0)');
    g.addColorStop(0.42, 'rgba(3,6,11,' + (k * 0.26).toFixed(3) + ')');
    g.addColorStop(0.74, 'rgba(3,6,11,' + (k * 0.64).toFixed(3) + ')');
    g.addColorStop(1.00, 'rgba(3,6,11,' + k.toFixed(3) + ')');
    cx.fillStyle = g;
    cx.fillRect(0, 0, W, H);
  };

  P.lip = function (cx, o) {
    o = o || {};
    var gx = o.gx || 0;
    var x, yt;
    var chamfer = o.chamfer == null ? 17 : o.chamfer;
    var riser = o.riser == null ? 64 : o.riser;

    /* lit top face of the chamfer.
     * EIGHT PRECOMPUTED RAMPS, not one per column. 540 columns each building
     * their own gradient from a computed rgba is 540 entries in qa.py's paint
     * census, which fills the cap and evicts the deck's law-bearing inks. */
    var lampX = o.lampX == null ? 980 : o.lampX;
    var RAMPS = [], ri;
    for (ri = 0; ri < 8; ri++) {
      var k = ri / 7;
      var gr = cx.createLinearGradient(0, 0, 0, chamfer);
      gr.addColorStop(0, LIPTOP[ri]);
      gr.addColorStop(1, 'rgba(58,72,82,0.9)');
      RAMPS.push(LIPTOP[ri]);
    }
    for (x = 0; x <= W; x += 2) {
      yt = P.lipTop(gx + x);
      var lamp = 1 - clamp(Math.abs(x - lampX) / 1100, 0, 1);
      var g = cx.createLinearGradient(0, yt, 0, yt + chamfer);
      g.addColorStop(0, LIPTOP[Math.min(7, (lamp * 8) | 0)]);
      g.addColorStop(1, 'rgba(58,72,82,0.9)');
      cx.fillStyle = g;
      cx.fillRect(x, yt, 2, chamfer);
    }
    /* the riser, dark, with its own slight vertical ramp */
    for (x = 0; x <= W; x += 2) {
      yt = P.lipTop(gx + x) + chamfer;
      var g2 = cx.createLinearGradient(0, yt, 0, yt + riser);
      g2.addColorStop(0, 'rgba(22,32,40,0.98)');
      g2.addColorStop(1, 'rgba(8,13,20,1)');
      cx.fillStyle = g2;
      cx.fillRect(x, yt, 2, riser);
    }
    /* ambient falloff below the riser, onto whatever the pad stands on */
    var yb = P.lipTop(gx + W / 2) + chamfer + riser;
    var g3 = cx.createLinearGradient(0, yb, 0, H);
    g3.addColorStop(0, 'rgba(8,13,20,1)');
    g3.addColorStop(1, 'rgba(5,8,14,1)');
    cx.fillStyle = g3;
    cx.fillRect(0, yb - 2, W, H - yb + 4);

    /* the form line where the chamfer meets the top, at fine weight */
    cx.strokeStyle = 'rgba(200,218,230,0.42)';
    cx.lineWidth = 1.25;
    cx.beginPath();
    for (x = 0; x <= W; x += 3) {
      yt = P.lipTop(gx + x);
      if (x === 0) cx.moveTo(x, yt); else cx.lineTo(x, yt);
    }
    cx.stroke();
  };

  /* ------------------------------------------------------------------- joint
   * The saw-cut control joint. D3 of the continuity system. Its exit height on
   * every frame IS the next frame's entry height, declared once as a chain so
   * the swipe reads as one object and not nine.
   */
  P.JOINT_CHAIN = [742, 742, 768, 768, 796, 796, 812, 812, 830, null];

  P.joint = function (cx, o) {
    o = o || {};
    var yIn = o.yIn, yOut = o.yOut;
    var dead = o.dead === true;
    var boxes = o.boxes || [];
    var x, y, t, m;
    var end = dead ? (o.deadAt == null ? 760 : o.deadAt) : W;

    function yAt(xx) {
      return yIn + (yOut == null ? 0 : (yOut - yIn)) * (xx / W) + 3 * Math.sin(xx / 90);
    }
    /* THE TROWEL CLOSES THE CUT AT THE FINISHED BAND. A saw cut run straight
     * through a headline is the "art touching glyphs" hard fail, and covering
     * it with a plate is the defect this deck exists to avoid. So the cut's
     * own ink falls to nothing within 38px of a measured line box, the same
     * discipline the aggregate uses, and the words sit on unbroken finish. */
    function mAt(xx, yy) {
      if (!boxes.length) return 1;
      return clamp((P.dist(boxes, xx, yy) - 12) / 38, 0, 1);
    }

    cx.save();
    cx.lineCap = 'round';
    for (x = 0; x <= end; x += 3) {
      y = yAt(x);
      m = mAt(x, y);
      if (m <= 0.02) continue;
      /* the cut, a dark slot */
      cx.strokeStyle = 'rgba(6,10,16,' + (0.92 * m) + ')';
      cx.lineWidth = 5;
      cx.beginPath(); cx.moveTo(x, y); cx.lineTo(x + 3.4, yAt(x + 3.4)); cx.stroke();
      /* its lit lower lip, from the lamp below right */
      cx.strokeStyle = 'rgba(176,198,212,' + (0.40 * m) + ')';
      cx.lineWidth = 1.25;
      cx.beginPath();
      cx.moveTo(x, y + 3.2); cx.lineTo(x + 3.4, yAt(x + 3.4) + 3.2);
      cx.stroke();
    }
    if (dead) {
      /* the one terminus in the deck, on slide 09 */
      cx.lineWidth = 3;
      cx.strokeStyle = 'rgba(176,198,212,0.55)';
      cx.beginPath();
      var ey = yIn + (yOut == null ? 0 : (yOut - yIn)) * (end / W) + 3 * Math.sin(end / 90);
      cx.moveTo(end, ey - 11); cx.lineTo(end, ey + 11);
      cx.stroke();
    }
    cx.restore();
  };

  /* ----------------------------------------------------------------- contact
   * POOL, THEN CAST, THEN SEAM, and never any other order. A correctly drawn
   * shadow on ground that is already near black measures zero separation, so
   * the ground is lit FIRST and cast into afterwards. The rects that get
   * declared in data-contacts are MEASURED off the render with
   * scripts/contact_probe.py, never computed from the numbers passed here.
   */
  P.contact = function (cx, o) {
    o = o || {};
    global.AKNIGHT.contact(cx, {
      x: o.x, y: o.y,
      w: o.w == null ? 92 : o.w,
      dirDeg: P.LIGHT.shadowDeg,
      color: o.color || '#0A1320',
      poolK: o.poolK == null ? 1.6 : o.poolK,
      poolDy: o.poolDy == null ? 12 : o.poolDy,
      tightAlpha: o.tightAlpha == null ? 0.64 : o.tightAlpha,
      wideAlpha: o.wideAlpha == null ? 0.05 : o.wideAlpha,
      anchorAlpha: o.anchorAlpha == null ? 0.78 : o.anchorAlpha,
      anchorW: o.anchorW,
      anchorBlur: o.anchorBlur
    });
  };

  /* ----------------------------------------------------------------- reserve */
  P.reserve = function (selector, opts) {
    return global.AKNIGHT.reserve(selector, opts || {});
  };

  P.dist = function (boxes, x, y) {
    var best = 1e9, i, b, dx, dy, d;
    for (i = 0; i < boxes.length; i++) {
      b = boxes[i];
      dx = Math.max(b[0] - x, 0, x - (b[0] + b[2]));
      dy = Math.max(b[1] - y, 0, y - (b[1] + b[3]));
      d = Math.sqrt(dx * dx + dy * dy);
      if (d < best) best = d;
    }
    return best;
  };

  /* ------------------------------------------------------------------- grain
   * A SMALL REPEATING TILE, never a full-frame feTurbulence rect, which costs
   * 10 to 40 MB in the PDF while the tile embeds once.
   */
  P.grainOn = function (el, seed, alpha) {
    el.style.backgroundImage = 'url(' + global.AK.grainTile(280, 52, seed || 11) + ')';
    el.style.opacity = String(alpha == null ? 0.06 : alpha);
  };

  global.AKPOUR = P;
})(window);
