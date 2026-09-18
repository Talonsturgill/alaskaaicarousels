/* akapron.js — THE RETURNED APRON chassis (carousel No. 62, 2026-09-18).
 *
 * WHAT THIS IS AND WHAT IT IS DELIBERATELY NOT.
 *
 * It is the deck's SEAM CONTRACT and its physics. One airport apron is drawn as
 * a 9 x 1080 = 9720 px panorama and sliced into nine windows, so the horizon,
 * the haze, the sky ramp and the gravel height field must all be pure functions
 * of GLOBAL x or adjacent frames will not seam. Run No.49 authored a catenary
 * per slide and missed seven junctions out of eight; the fix is that no slide
 * authors its own horizon, ever.
 *
 * It is NOT a drawTheWholeSlide(). bespoke_check.py measures pairwise similarity
 * of each slide's own drawing code with the house harness stripped out and FAILS
 * a deck whose median clears 0.60, and run 2026-08-05 shipped nine frames that
 * were one function called nine times. So this file gives every frame the same
 * GROUND and the same LIGHT, and every frame composes its own scene, its own
 * objects and its own marks on top.
 *
 * THE ONE LIGHT, declared here and never varied by a slide:
 *   azimuth 208 deg, elevation 24 deg, key to fill 3.5 to 1.
 *   Screen shadow vector down and to the right at 28 deg below horizontal.
 *   Cast length = 2.25 x object height, since tan(24 deg) = 0.445.
 *   Shadow ink is a darkened sky hue, never black.
 *
 * Load AFTER noise.js (needs AK.rng, AK.fbm2) and akcolor.js (needs AKC).
 */
(function (global) {
  "use strict";

  var W = 1080, H = 1350;

  /* ---- the panorama seam contract ------------------------------------- */
  // Pure functions of global x. A slide passes gx = slideIndex * 1080 + localX.
  // THE HORIZON SITS AT 620, not at 506 where it started. The kneeling camera
  // puts the reader's eye about 620 mm off the shoulder, and the deck's display
  // type all lives ABOVE the horizon in the dark part of the sky. At 506 the
  // body copy on slide 02 crossed the horizon glow, the punched reserve behind
  // it read as a flat plate, and that is the exact defect the reserve exists to
  // prevent. Raising the horizon gives every frame a type zone the art never
  // enters, which is cheaper and truer than reserving harder.
  function yHorizon(gx) {
    return 620 + 14 * Math.sin(2 * Math.PI * (gx - 1400) / 5200)
               + 6 * Math.sin(2 * Math.PI * gx / 1730);
  }
  function yApron(gx) {
    return 1000 + 9 * Math.sin(2 * Math.PI * (gx - 300) / 6100);
  }

  /* ---- the one light --------------------------------------------------- */
  var LIGHT = {
    az: 208, el: 24, keyFill: 3.5,
    shadowDeg: 28,          // screen angle of every cast, below horizontal
    castMul: 2.25           // cast length as a multiple of object height
  };
  // The deck's cast vector, in screen px, for an object of height h.
  function castVec(h) {
    var L = h * LIGHT.castMul, r = LIGHT.shadowDeg * Math.PI / 180;
    return [Math.cos(r) * L, Math.sin(r) * L];
  }

  /* ---- the palette ----------------------------------------------------- */
  var PAL = {
    floor:    "#1A1712",   // deepest ground shadow, warm near black
    gravelLo: "#2A241B",   // gravel shadow side
    gravelMid:"#4A3D2C",   // mid gravel body
    gravelHi: "#7A6A4F",   // lit gravel crown
    crown:    "#A8946F",   // specular glint
    tree:     "#3A3B33",   // spruce treeline
    haze:     "#6E6252",   // haze band
    skyTop:   "#443C31",   // sky ramp zenith
    skyLow:   "#9A8460",   // sky ramp horizon glow
    bounce:   "#5A6A78",   // sky bounce fill, the only cool thing in a warm world
    snow:     "#F4F8FF",   // type primary
    bone:     "#C9C2B4",   // type secondary
    fixture:  "#6B6355",   // mono watermark and counter
    phantom:  "#9FB3C4",   // WHAT IS NOT PUBLISHED. dashed, unfilled, never lit
    gold:     "#FFC72C"    // THE RECORD. sealed forms only
  };
  var PHANTOM_DASH = [30, 5, 6, 5, 6, 5];

  /* ---- the sky, a pure function of gx ---------------------------------- */
  function skyBand(cx, gx0) {
    var hz = yHorizon(gx0 + W / 2);
    var g = cx.createLinearGradient(0, 0, 0, hz + 40);
    // THE GLOW IS CONFINED TO A NARROW RIM AT THE HORIZON. The band above it
    // stays dark, because that band is where every display string in this deck
    // sits and snow type on a warm mid value fails the contrast floor.
    g.addColorStop(0.00, "#2A241D");
    g.addColorStop(0.50, "#332C23");
    g.addColorStop(0.80, "#42392C");
    g.addColorStop(0.93, "#6B5B43");
    g.addColorStop(1.00, PAL.skyLow);
    cx.fillStyle = g;
    cx.fillRect(0, 0, W, hz + 42);
    // the haze band sitting on the horizon, a soft wedge rather than a line
    var h2 = cx.createLinearGradient(0, hz - 62, 0, hz + 16);
    h2.addColorStop(0, "rgba(110,98,82,0)");
    h2.addColorStop(1, "rgba(110,98,82,0.72)");
    cx.fillStyle = h2;
    cx.fillRect(0, hz - 62, W, 80);
  }

  /* ---- the treeline, a pure function of gx ----------------------------- */
  // Spruce silhouette. Each tree's position and height derive from gx alone, so
  // a tree cut by the right edge of slide n completes on slide n+1.
  function treeline(cx, gx0) {
    // TWO RANKS. The far rank is lerped harder toward haze and sits a little
    // higher, which is atmospheric perspective doing the work rather than a
    // drawn outline, and it stops the treeline reading as one sawtooth strip.
    // A FIXED PERIOD IS WHAT MAKES A TREELINE READ AS A COMB. The first build
    // stepped both ranks on an exact grid with a symmetric triangle at every
    // node, and two critics independently called the result a sawtooth, one of
    // them noting it sat close enough to a waveform to be mistaken for the
    // sensor trace this deck refuses to draw. So each tree now gets its own
    // jitter off the grid, its own height multiplier and an asymmetric profile.
    // The multiplier only ever SHORTENS (0.42 to 1.00): the rank ceilings were
    // already lowered once to keep spruce out of the slide 02 body block, and a
    // taller tree would buy irregularity by reopening a type collision.
    var ranks = [
      { step: 13, hMin: 10, hMax: 34, lift: 10, mix: 0.74, salt: 3301 },
      { step: 17, hMin: 18, hMax: 58, lift: 0,  mix: 0.18, salt: 7919 }
    ];
    for (var k = 0; k < ranks.length; k++) {
      var R = ranks[k], i, gx, y, idx, rr, hgt, wd, t, spike, jit, prof;
      cx.beginPath();
      cx.moveTo(-40, H);
      for (i = -40; i <= W + 40; i += 2) {
        gx = gx0 + i;
        y = yHorizon(gx) - R.lift;
        idx = Math.floor(gx / R.step);
        rr = AK.rng(idx * R.salt);
        jit = (rr() - 0.5) * R.step * 0.85;
        hgt = (R.hMin + rr() * (R.hMax - R.hMin)) * (0.42 + rr() * 0.58);
        wd = R.step * (0.45 + rr() * 0.85);
        t = (gx - idx * R.step - jit) / wd;
        spike = t >= 0 && t < 1 ? (1 - Math.abs(2 * t - 1)) : 0;
        // a spruce is not an isosceles triangle. The windward half climbs fast
        // and the leeward half falls away slowly, so the two exponents differ.
        prof = Math.pow(spike, t < 0.5 ? 1.65 : 1.10);
        cx.lineTo(i, y - hgt * prof);
      }
      cx.lineTo(W + 40, H);
      cx.closePath();
      cx.fillStyle = AKC.mixOklab(PAL.tree, PAL.haze, R.mix);
      cx.fill();
    }
  }

  /* ---- the apron, a pure function of gx -------------------------------- */
  function apronBand(cx, gx0) {
    var hz = yHorizon(gx0 + W / 2), ap = yApron(gx0 + W / 2);
    var g = cx.createLinearGradient(0, hz, 0, ap + 30);
    g.addColorStop(0, AKC.mixOklab(PAL.gravelLo, PAL.haze, 0.30));
    g.addColorStop(1, PAL.gravelLo);
    cx.fillStyle = g;
    cx.beginPath();
    cx.moveTo(0, hz);
    for (var i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, hz);
    cx.closePath();
    cx.fill();
  }

  /* ---- the gravel height field ----------------------------------------- */
  // THE GROUND IS A FUNCTION OF GLOBAL X, so the shoulder seams exactly. A slide
  // adds its own TROUGHS (a tyre pass, a rut) as centreline polylines in GLOBAL
  // coordinates, and the field carries them.
  function makeField(troughs) {
    troughs = troughs || [];
    function base(gx, y) {
      return AK.fbm2(gx * 0.0075, y * 0.0075, 4) * 0.62
           + AK.fbm2(gx * 0.031, y * 0.031, 3) * 0.38;
    }
    function troughAt(gx, y) {
      var d = 0, k, t, i, best, dd;
      for (k = 0; k < troughs.length; k++) {
        t = troughs[k];
        best = 1e9;
        for (i = 0; i < t.pts.length - 1; i++) {
          dd = segDist(gx, y, t.pts[i][0], t.pts[i][1], t.pts[i + 1][0], t.pts[i + 1][1]);
          if (dd < best) best = dd;
        }
        d -= t.depth * Math.exp(-(best * best) / (2 * t.sigma * t.sigma));
      }
      return d;
    }
    return function (gx, y) { return base(gx, y) + troughAt(gx, y); };
  }
  function segDist(px, py, x1, y1, x2, y2) {
    var dx = x2 - x1, dy = y2 - y1, L = dx * dx + dy * dy;
    var t = L ? Math.max(0, Math.min(1, ((px - x1) * dx + (py - y1) * dy) / L)) : 0;
    var qx = x1 + t * dx, qy = y1 + t * dy;
    return Math.hypot(px - qx, py - qy);
  }

  /* ---- the hachure shoulder -------------------------------------------- */
  // Slope-and-aspect hachuring. Every stroke's WIDTH is the local slope of the
  // height field and its ROTATION is the local aspect, so the field CANNOT be
  // uniform unless the ground is. That is the whole reason this is not a
  // position-parameterised stipple, which is the texture this house has shipped
  // and which no reader has ever been able to see a falloff in.
  function hachure(cx, gx0, opts) {
    var o = opts || {};
    var y0 = o.y0 || 940, y1 = o.y1 || H;
    var field = o.field || makeField([]);
    var grid = o.grid || 9;
    var passes = o.passes || 4;
    var seed = o.seed || 1;
    var lo = o.lo || PAL.gravelLo, hi = o.hi || PAL.gravelHi;
    var base = AKC.ramp(hi, { steps: 7, keyHue: 60, ambientHue: 220 });
    var sunAz = LIGHT.az * Math.PI / 180;
    // THE SCALE GRADIENT IS WHAT MAKES THIS ONE SURFACE INSTEAD OF TWO. The first
    // build hachured only the shoulder and filled the apron above it with round
    // isotropic dots, which five critics read as dust, noise or a dead band, and
    // one measured the hard horizontal seam where the two textures butted. A
    // receding plane does not change texture with distance, it changes SCALE: the
    // same strokes get shorter, finer, denser and hazier toward the horizon.
    var s0 = o.scale0 === undefined ? 0.34 : o.scale0;   // stroke scale at y0
    var s1 = o.scale1 === undefined ? 1.00 : o.scale1;   // stroke scale at y1
    var hz0 = o.haze0 === undefined ? 0.52 : o.haze0;    // haze lerp at y0
    // the banded ramp, flattened: index = shadeStep + hazeBands * distanceBand
    var hazeBands = base.length, ramp = base.slice(), bi, si;
    if (hz0 > 0) {
      ramp = [];
      for (bi = 0; bi < 6; bi++) {
        for (si = 0; si < hazeBands; si++) {
          ramp[si + hazeBands * bi] = AKC.mixOklab(base[si], PAL.haze, hz0 * bi / 5);
        }
      }
    }
    var p, gy, gxl, rnd, span = Math.max(1, y1 - y0);
    for (p = 0; p < passes; p++) {
      rnd = AK.rng(seed * 131 + p * 17);
      var azP = sunAz + (p - (passes - 1) / 2) * (3 * Math.PI / 180);
      cx.save();
      cx.globalAlpha = o.alpha === undefined ? 0.22 : o.alpha;
      cx.lineCap = "round";
      for (gy = y0; gy < y1; gy += Math.max(3.4, grid * (s0 + ((gy - y0) / span) * (s1 - s0)))) {
        var tRow = (gy - y0) / span;
        var sc = s0 + tRow * (s1 - s0);
        var cell = Math.max(3.4, grid * sc);
        for (gxl = -cell; gxl < W + cell; gxl += cell) {
          var jx = gxl + (rnd() - 0.5) * cell * 0.9;
          var jy = gy + (rnd() - 0.5) * cell * 0.9;
          var G = gx0 + jx;
          // central differences give slope and aspect
          var e = 2.2;
          var hL = field(G - e, jy), hR = field(G + e, jy);
          var hU = field(G, jy - e), hD = field(G, jy + e);
          var dzdx = (hR - hL) / (2 * e), dzdy = (hD - hU) / (2 * e);
          var slope = Math.hypot(dzdx, dzdy);
          var aspect = Math.atan2(dzdy, dzdx);
          // stroke width from slope, rotation from aspect, per Lehmann
          // SHORTER AND HEAVIER. Three critics independently read this ground as
          // straw, stubble, dry grass, fur or a mown hayfield, which is the
          // deck's declared material missed on every frame at once. Three things
          // were making blades instead of chips: the strokes were long (up to 35
          // px), they were fine (0.6 to 2.4 px), and they all took their rotation
          // from the aspect field, so they COMBED into rows and the rows read as
          // a crop. Length is halved and capped, weight is roughly doubled, and
          // the cap below is absolute because a long fine stroke is a blade
          // whatever the grid says.
          var wdt = (1.4 + Math.min(1.0, slope * 26) * 1.8) * (0.52 + 0.48 * sc);
          var len = Math.min(11, grid * sc * (0.8 + rnd() * 0.45)
                                 * (o.lenMul === undefined ? 1 : o.lenMul));
          // shade against this pass's sun azimuth
          var nd = Math.max(0, Math.cos(aspect - azP));
          var step = Math.max(0, Math.min(hazeBands - 1,
                     Math.round(nd * (hazeBands - 1))));
          // AERIAL PERSPECTIVE, IN SIX BANDS AND NOT AS A CONTINUUM. Contrast
          // falls toward the horizon because the air between is doing the work.
          // The band count is not a stylistic preference: qa.py's paint census
          // holds 160 entries, and lerping every row to its own haze value minted
          // a fresh colour literal per row, which flooded the census and EVICTED
          // #FFC72C, so two frames failed the ink law reporting no gold on frames
          // that plainly had gold on them. Six bands times the seven step ramp is
          // 42 literals. It is also how an engraver actually cuts distance.
          cx.strokeStyle = hz0 > 0
            ? ramp[step + hazeBands * Math.min(5, Math.floor((1 - tRow) * 6))]
            : ramp[step];
          cx.lineWidth = wdt;
          // AND THE COMB IS BROKEN. Every stroke took its rotation purely from
          // the local aspect, so neighbouring strokes were near parallel and
          // ganged into visible rows. Gravel has no grain: each chip lies how it
          // fell. A wide rotation jitter on top of the aspect term keeps the
          // slope reading (the field still sets the population's mean direction)
          // while destroying the alignment that made it a crop.
          var rot = aspect + (rnd() - 0.5) * 1.22;      // +/- 35 degrees
          var bend = (rnd() - 0.5) * 0.16;
          var hx = Math.cos(rot) * len / 2, hy = Math.sin(rot) * len / 2;

          // THE SHADOW POCKET. This is the difference between gravel and grass,
          // and it is the one thing none of the earlier repairs supplied. Every
          // mark in this field was LIGHTER than the ground it sat on, so nothing
          // was ever occluded by anything: a population of pale needles with no
          // dark counterpart is stubble, whatever its length or weight. A stone
          // is legible because it casts into its own bed. So each lit stroke gets
          // a companion in the floor value, offset UP AND LEFT, which is opposite
          // the 208 degree key, at half the weight. The field acquires mass, and
          // the 24 degree raking light finally has evidence in the surface.
          cx.save();
          cx.strokeStyle = PAL.floor;
          cx.globalAlpha = 0.55;
          cx.lineWidth = wdt * 0.5;
          cx.beginPath();
          cx.moveTo(jx - hx - 2.4, jy - hy - 1.7);
          cx.lineTo(jx + hx - 2.4, jy + hy - 1.7);
          cx.stroke();
          cx.restore();

          cx.beginPath();
          cx.moveTo(jx - hx, jy - hy);
          cx.quadraticCurveTo(jx + bend * len, jy + bend * len, jx + hx, jy + hy);
          cx.stroke();
        }
      }
      cx.restore();
    }
  }

  /* ---- the specular crowns --------------------------------------------- */
  // 527 lit crowns in each 1080 px column, one per minute aloft (C04). Declared
  // in window.__akAssert with points and dispersed:true, because the marks stand
  // for HOW MUCH and deliberately not for WHERE, and verified against the
  // COMPOSITED png rather than against this loop.
  function crownPoints(gx0, y0, y1, seed) {
    var rnd = AK.rng((seed || 1) * 977 + Math.floor(gx0));
    var pts = [], i, x, y;
    for (i = 0; i < 527; i++) {
      x = 6 + rnd() * (W - 12);
      y = y0 + Math.pow(rnd(), 0.62) * (y1 - y0);
      pts.push([x, y]);
    }
    return pts;
  }
  function drawCrowns(cx, pts, field, gx0) {
    cx.save();
    for (var i = 0; i < pts.length; i++) {
      var x = pts[i][0], y = pts[i][1];
      var e = 2.0, G = gx0 + x;
      var dzdx = (field(G + e, y) - field(G - e, y)) / (2 * e);
      // a crown catches light where the ground turns toward the sun
      var lit = Math.max(0, -dzdx) * 30;
      cx.globalAlpha = Math.min(0.85, 0.16 + lit);
      cx.fillStyle = PAL.crown;
      cx.beginPath();
      cx.arc(x, y, 0.9 + Math.min(1.1, lit * 1.4), 0, Math.PI * 2);
      cx.fill();
    }
    cx.restore();
  }

  /* ---- a long directional cast ----------------------------------------- */
  // The deck's one shadow vector. Never black, always the darkened sky hue, and
  // it LEAVES the frame rather than closing under a foot.
  // Smeared along the light vector in steps, so the cast is ATTACHED at the foot
  // and fades with distance. A detached core is what reads as a hole, and the
  // fix for a weak contact is never a stronger shadow, it is a LIT GROUND laid
  // down first for the cast to subtract from.
  // A SHADOW'S TERMINATOR IS ITS ARGUMENT. The first build smeared sixteen
  // translucent copies of the silhouette straight onto the frame, and five
  // critics independently reported that no cast on any frame carried a readable
  // 28 degree edge: one called it a bruise, another said the chocks appeared to
  // EMIT light. The cause is that every step contributes another three percent
  // ramp, so the union never acquires a hard edge and the angle has nothing to
  // live in. The union is therefore built at FULL alpha in a 2x buffer and
  // composited once, and a second shorter union is laid over its near half, so
  // the cast is darkest at the foot and steps once on its way out. Two hard
  // edged tones model a cast. Twenty soft ones model nothing.
  function castUnion(cx, path, v, steps, alpha, ink) {
    var off = document.createElement("canvas"), i;
    off.width = W * 2; off.height = H * 2;
    var b = off.getContext("2d");
    b.scale(2, 2);
    b.fillStyle = ink;
    b.beginPath();
    for (i = 0; i <= steps; i++) path(b, v[0] * i / steps, v[1] * i / steps);
    b.fill();                                  // ONE fill, nonzero winding = union
    cx.save();
    cx.globalAlpha = alpha;
    cx.drawImage(off, 0, 0, W, H);
    cx.restore();
  }
  function cast(cx, path, h, alpha) {
    var v = castVec(h);
    var a = (alpha === undefined ? 0.55 : alpha);
    var ink = AKC.mixOklab(PAL.bounce, PAL.floor, 0.62);
    cx.save();
    cx.globalCompositeOperation = "multiply";
    // 0.85 and 0.72, not 0.54 and 0.48. The rebuilt cast has a hard terminator
    // but critics still could not FIND it, because at 27 percent a multiply of a
    // mid-dark ink over dark gravel moves the value by less than the lit pool
    // beside it moves it the other way, and the pool is the larger shape. A
    // shadow that loses to its own key light is not a shadow.
    castUnion(cx, path, v, 26, a * 0.85, ink);                       // full throw
    castUnion(cx, path, [v[0] * 0.42, v[1] * 0.42], 14, a * 0.72, ink); // near half
    cx.restore();
  }

  /* ---- the repoussoir clod --------------------------------------------- */
  // A genuinely out-of-focus foreground plane bleeding off the bottom edge, so
  // the sharp middle distance reads as depth rather than as flatness.
  function clod(cx, gx0, seed) {
    var off = document.createElement("canvas");
    off.width = W; off.height = 200;
    var g = off.getContext("2d");
    var rnd = AK.rng((seed || 1) * 613);
    g.fillStyle = PAL.gravelLo;
    for (var i = 0; i < 190; i++) {
      var x = rnd() * W, y = 60 + rnd() * 150, r = 10 + rnd() * 46;
      g.globalAlpha = 0.5 + rnd() * 0.5;
      g.beginPath(); g.ellipse(x, y, r, r * 0.58, rnd() * 3.14, 0, Math.PI * 2); g.fill();
    }
    cx.save();
    cx.filter = "blur(11px)";          // ONCE, on a composite, never in a loop
    cx.drawImage(off, 0, H - 150, W, 200);
    cx.restore();
  }

  /* ---- the tyre track, ONE path across the whole panorama -------------- */
  // The deck's continuity motif. Its centreline is a pure function of global x
  // like everything else here, so the track a reader follows on slide 03 is
  // literally the same track on slide 07. A slide asks for the window it needs
  // and adds any EXTRA pass of its own (the return on slide 02, the straight
  // rut on slide 05) as another trough.
  function trackY(gx) {
    return 1156 + 46 * Math.sin(2 * Math.PI * (gx - 900) / 4300)
                + 17 * Math.sin(2 * Math.PI * gx / 1180);
  }
  function trackPts(gxFrom, gxTo, step) {
    var pts = [], gx;
    step = step || 18;
    for (gx = gxFrom; gx <= gxTo; gx += step) pts.push([gx, trackY(gx)]);
    return pts;
  }
  // The second pass of slide 02, offset and crushing the first. THIS IS THE
  // DECK'S THESIS: a thousand kilometres that came back into its own impression.
  // NOT A CONSTANT GAP. The first build laid the return 40 px below the outbound
  // for the whole width. Against a 210 px track that is a 19 percent shift the
  // frame cannot resolve, and the critic's verdict was exact: it read as the two
  // WALLS OF ONE RUT, identical in structure to slide 01's, so the deck's thesis
  // was absent from the frame that exists to carry it. A return has to CROSS. It
  // comes in wide on the east and crosses the outbound at gx 1480, which is the
  // left third of slide 02's window, so the overlap is a lens in ONE PLACE rather
  // than a gap everywhere. Still a pure function of global x, so the seam holds.
  function returnOffset(gx) {
    return 86 * Math.tanh((gx - 1480) / 430);
  }
  function returnPts(gxFrom, gxTo, step) {
    var pts = [], gx;
    step = step || 18;
    for (gx = gxFrom; gx <= gxTo; gx += step) {
      pts.push([gx, trackY(gx) + returnOffset(gx)]);
    }
    return pts;
  }

  /* ---- the ground, apron and shoulder in one pass ---------------------- */
  // Shared PHYSICS, not a shared composition. Every frame stands on the same
  // apron under the same light; what each frame puts ON it is its own.
  function ground(cx, gx0, opts) {
    var o = opts || {}, i, rnd;
    var field = o.field || makeField([]);
    var seed = o.seed || 1;
    var ap = yApron(gx0 + W / 2), hz = yHorizon(gx0 + W / 2);

    // worn asphalt, graded away from the camera and lerped toward the haze
    var g = cx.createLinearGradient(0, hz, 0, ap + 8);
    g.addColorStop(0, AKC.mixOklab(PAL.gravelLo, PAL.haze, 0.34));
    g.addColorStop(0.55, AKC.mixOklab(PAL.gravelLo, PAL.haze, 0.12));
    g.addColorStop(1, "#231E17");
    cx.fillStyle = g;
    cx.beginPath();
    cx.moveTo(0, hz);
    for (i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, hz);
    cx.closePath();
    cx.fill();

    // the gravel shoulder, which the hachure models
    var sg = cx.createLinearGradient(0, ap - 10, 0, H);
    sg.addColorStop(0, PAL.gravelLo);
    sg.addColorStop(0.5, PAL.gravelMid);
    sg.addColorStop(1, "#241F18");
    cx.fillStyle = sg;
    cx.beginPath();
    cx.moveTo(0, yApron(gx0));
    for (i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, H); cx.lineTo(0, H); cx.closePath(); cx.fill();

    // AGGREGATE. Exposed stone in the wearing course, scale graded with distance.
    // These are ELLIPSES RAKED TO THE LIGHT, not discs: a round dot has no
    // orientation, so eleven thousand of them read as dirt on the lens, which is
    // what the first build shipped and what every critic who looked at the apron
    // called noise. A chip of aggregate is longer than it is tall and it lies down.
    // CLIPPED TO THE APRON, and only mildly elongated. Carried down over the
    // shoulder at a 3:1 axis ratio they stopped reading as chips of stone and
    // started reading as straw, which turned the best band in the deck into a
    // hedge. The shoulder already has the hachure and the crowns; this is the
    // apron's texture and it stops where the apron stops.
    cx.save();
    cx.beginPath();
    cx.moveTo(0, hz);
    for (i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, hz); cx.closePath(); cx.clip();
    rnd = AK.rng(seed * 401);
    for (i = 0; i < 6400; i++) {
      var ax = rnd() * W;
      var d = Math.pow(rnd(), 0.55);                 // 0 far, 1 near
      var ay = hz + d * (yApron(gx0 + ax) - hz);
      var ar = 0.32 + d * 1.9;
      var lit = rnd();
      cx.globalAlpha = (0.05 + d * 0.24) * (0.35 + 0.65 * d);
      cx.fillStyle = lit > 0.62 ? PAL.gravelHi
                   : (lit > 0.3 ? PAL.gravelMid : PAL.floor);
      cx.beginPath();
      cx.ellipse(ax, ay, ar * 1.55, ar * 0.82, -0.28 + (rnd() - 0.5) * 0.5,
                 0, Math.PI * 2);
      cx.fill();
    }
    cx.restore();

    // ONE SURFACE, HORIZON TO FOOT, IN TWO WEIGHTS THAT OVERLAP. Not a hachured
    // shoulder above a stippled apron with a seam between them, which is what the
    // first build shipped and what five critics called a dead band.
    //
    // But not a single full-strength pass over the whole thing either. That was
    // tried here and it was WORSE than the defect it replaced: at the shoulder's
    // density, carried up 724 px instead of 362, the frame read as fur. It also
    // kept the punched reserve visible, because a reserve is found by the fact
    // that the TEXTURE STOPS inside it, and matching the value underneath cannot
    // help when the surround is that loud. The apron is a graded surface seen at a
    // shallow angle: what it needs is DIRECTION, not coverage. So the far pass is
    // one sweep at a third of the alpha on a wide grid, and the near pass is the
    // shoulder's own weight, and the two overlap by 34 px so no seam can print.
    // ONE LONG LIT SWEEP along the apron's own y function, laid before the far
    // hachure so the strokes sit IN it. Without it the apron has direction but no
    // falloff, and 380 px of evenly lit ground is the same dead band by another
    // route. The camera kneels, so the light pools in the middle distance.
    var sw = cx.createLinearGradient(0, hz + 40, 0, ap);
    sw.addColorStop(0, "rgba(168,148,111,0)");
    sw.addColorStop(0.45, "rgba(168,148,111,0.13)");
    sw.addColorStop(1, "rgba(168,148,111,0)");
    cx.fillStyle = sw;
    cx.beginPath();
    cx.moveTo(0, hz);
    for (i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, hz); cx.closePath(); cx.fill();

    // AND THE APRON IS NOT ONE TONE. With direction but no tonal variation the
    // band still read as a dead field: uniform speckle, no value change, nothing
    // for an eye to cross. A graded surface has low spots that hold shade and
    // crowns that catch the key, on a scale of metres rather than of stones. Two
    // periods, both pure functions of GLOBAL x so the lobes carry across a seam,
    // giving the band a swing of roughly eight percent luminance.
    // AS A GRADIENT, NOT AS STRIPS. Sampling the lobe function into a row of
    // 8 px fillRects gave every strip its own flat alpha, and adjacent strips
    // banded against each other: the apron came out as CORDUROY, which is a
    // worse defect than the uniformity it was added to cure. A gradient
    // interpolates between its stops, so the same function sampled every 45 px
    // lands as smooth lobes with no edge anywhere.
    var lobe = cx.createLinearGradient(0, 0, W, 0);
    for (i = 0; i <= 24; i++) {
      var fx = i / 24, G2 = gx0 + fx * W;
      var u = Math.sin(2 * Math.PI * (G2 - 480) / 1460)
            + 0.55 * Math.sin(2 * Math.PI * G2 / 3700);
      var la = Math.min(0.16, Math.abs(u) * 0.085);
      lobe.addColorStop(fx, u > 0 ? "rgba(168,148,111," + la + ")"
                                  : "rgba(26,23,18," + la + ")");
    }
    cx.fillStyle = lobe;
    cx.beginPath();
    cx.moveTo(0, hz + (ap - hz) * 0.16);
    for (i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, hz + (ap - hz) * 0.16);
    cx.closePath(); cx.fill();

    hachure(cx, gx0, { y0: hz + 6, y1: ap + 20, field: field, grid: 16,
                       passes: 2, seed: seed, hi: PAL.gravelHi, alpha: 0.13, lenMul: 0.52,
                       scale0: 0.46, scale1: 0.95, haze0: 0.60 });
    // The shoulder pass is EXACTLY what it was on the first build (scale 1, no
    // haze lerp, four passes). Every critic who looked at it called it the best
    // ground this house has shipped, so it is not what the repair is for.
    hachure(cx, gx0, { y0: ap - 14, y1: H, field: field, grid: o.grid || 9,
                       passes: o.passes || 4, seed: seed, hi: PAL.gravelHi,
                       scale0: 1.00, scale1: 1.00, haze0: 0 });

    // CHIPS. A hachure field models a SURFACE, and every critic who looked at
    // this one named a crop, because nothing in it was a discrete solid object.
    // A gravel shoulder is stone lying loose on graded fines, so a sparse
    // population of small convex solids, each lit from 208 and each with a seam
    // where it meets the ground, gives the eye something to land on that is
    // unmistakably not a blade. Sparse on purpose, about one per 900 px2.
    cx.save();
    rnd = AK.rng(seed * 1597);
    var chipN = Math.round((H - ap) * W / 900);
    for (i = 0; i < chipN; i++) {
      var px = rnd() * W;
      var dd = Math.pow(rnd(), 0.62);
      var py = ap + dd * (H - ap);
      var pr = (1.6 + rnd() * 2.0) * (0.55 + 0.45 * dd);
      var rot2 = rnd() * Math.PI;
      var cg = cx.createLinearGradient(px - pr, py - pr, px + pr, py + pr);
      cg.addColorStop(0, PAL.crown);
      cg.addColorStop(0.52, PAL.gravelHi);
      cg.addColorStop(1, PAL.gravelLo);
      cx.globalAlpha = 0.30 + dd * 0.42;
      cx.fillStyle = cg;
      cx.beginPath();
      cx.ellipse(px, py, pr * 1.25, pr * 0.82, rot2, 0, Math.PI * 2);
      cx.fill();
      // the seam where the stone meets the fines, on the shadow side
      cx.globalAlpha = (0.30 + dd * 0.42) * 0.7;
      cx.strokeStyle = PAL.floor;
      cx.lineWidth = 0.9;
      cx.beginPath();
      cx.ellipse(px + 0.7, py + 0.7, pr * 1.25, pr * 0.82, rot2, 0.5, 2.9);
      cx.stroke();
    }
    cx.restore();

    var crowns = crownPoints(gx0, ap + 10, H - 24, seed);
    drawCrowns(cx, crowns, field, gx0);
    return crowns;
  }

  /* ---- a drawn tyre trough --------------------------------------------- */
  // The hachure models the ground, but a depression this shallow washes out
  // against the base noise, so the track is also DRAWN, as two walls under the
  // deck's one key at 24 degrees. The wall turned toward azimuth 208 is lit and
  // the wall turned away is in the darkened sky hue. That is a real optical
  // fact about a rut, and it is what makes the motif legible at 432 px.
  function trackMark(cx, gx0, pts, opts) {
    var o = opts || {}, halfW = o.width || 104, i, p0, p1;
    var lit = o.lit || PAL.gravelHi, dark = o.dark || PAL.floor;
    // the light comes from the upper left of screen at az 208, so on a trough
    // running left to right the FAR wall catches it and the NEAR wall is in shade
    function wall(off1, off2, fill, alpha) {
      cx.save();
      cx.globalAlpha = alpha;
      cx.fillStyle = fill;
      cx.beginPath();
      for (i = 0; i < pts.length; i++) {
        p0 = pts[i];
        if (i === 0) cx.moveTo(p0[0] - gx0, p0[1] + off1);
        else cx.lineTo(p0[0] - gx0, p0[1] + off1);
      }
      for (i = pts.length - 1; i >= 0; i--) {
        p1 = pts[i];
        cx.lineTo(p1[0] - gx0, p1[1] + off2);
      }
      cx.closePath();
      cx.fill();
      cx.restore();
    }
    // shaded near wall, then the trough floor, then the lit far lip
    wall(-halfW * 0.5, halfW * 0.16, AKC.mixOklab(dark, PAL.gravelLo, 0.35), 0.62);
    wall(halfW * 0.16, halfW * 0.5, AKC.mixOklab(lit, PAL.gravelMid, 0.42), 0.40);
    // the crushed centre, the deepest tone the trough carries
    wall(-halfW * 0.10, halfW * 0.10, dark, 0.34);
  }

  /* ---- a lit pool ------------------------------------------------------ */
  // A LIT POOL IS NOT A RECTANGLE. It was one in the first build of this deck,
  // carried on a fillRect, which is both wrong about light and is what
  // bespoke_check counts as blocky. The pool an object sits in is an ellipse
  // stretched along the light's own axis, and the cast subtracts from it.
  function litPool(cx, x, y, rx, ry, alpha) {
    // CANVAS HAS NO ELLIPTICAL GRADIENT. Pouring a circular ramp into an ellipse
    // stops the paint on the short axis while the ramp still carries alpha, and
    // leaves a hard arc. The ramp is built on a CIRCLE inside a transform, which
    // is the only way to get an elliptical falloff that actually falls off.
    var a = (alpha === undefined ? 0.30 : alpha);
    cx.save();
    cx.translate(x, y);
    cx.rotate(LIGHT.shadowDeg * Math.PI / 180);
    cx.scale(1, ry / rx);
    var g = cx.createRadialGradient(0, 0, rx * 0.10, 0, 0, rx);
    g.addColorStop(0, "rgba(168,148,111," + a + ")");
    g.addColorStop(0.46, "rgba(168,148,111," + a * 0.42 + ")");
    g.addColorStop(1, "rgba(168,148,111,0)");
    cx.fillStyle = g;
    cx.beginPath();
    cx.arc(0, 0, rx, 0, Math.PI * 2);
    cx.fill();
    cx.restore();
  }

  /* ---- the base wash --------------------------------------------------- */
  // WHAT A PUNCHED RESERVE REVEALS MATTERS AS MUCH AS THE PUNCH. The reserve
  // removes the art from a box, and whatever is UNDER that box is what the
  // reader sees. On the first build that was bare body background, so five
  // frames showed a flat dark rectangle behind their copy, which is precisely
  // the plate the doctrine bans and the reserve exists to avoid. This lays a
  // full-height graded wash on the visible canvas BEFORE the buffer composites,
  // so a hole reveals continuing modelled atmosphere instead of a box.
  // MATCHING THE VALUE IS HALF THE JOB, AND THE FIRST BUILD DID NEITHER HALF.
  // Five frames shipped a reserve that read as a LIT rectangle, because this ramp
  // was a hand-picked guess several percent ABOVE the apron it stands in for, and
  // because a matched but FLAT reveal is still findable: the reader locates the
  // box by the fact that the grain stops inside it. So the wash is now built from
  // the ground's own recipe rather than beside it, and it carries its own
  // scale-graded fleck field, so a punched hole reveals CONTINUING GROUND.
  function baseWash(cx, gx0) {
    var hz = yHorizon(gx0 + W / 2), ap = yApron(gx0 + W / 2), i;
    var g = cx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0.00, "#2A241D");
    g.addColorStop(Math.max(0.01, hz / H - 0.07), "#383026");
    // THE WASH HAS TO MATCH WHAT THE ART PUTS THERE, NOT WHAT THE GROUND RECIPE
    // SAYS. Copying ground()'s stops made the wash peak at exactly the horizon,
    // because the apron's top edge IS its brightest part. But the ART at that
    // line is the TREELINE, a dark silhouette drawn over it, so a punch revealed
    // a bright ridge where the frame is dark and two critics independently found
    // a hard bright rule with square ends running under the treeline on the
    // punched frames and absent on the one frame with no punch. The wash
    // therefore carries the treeline's own value through that band and only
    // reaches the apron's value once the trees have ended.
    g.addColorStop(hz / H, AKC.mixOklab(PAL.tree, PAL.haze, 0.42));
    g.addColorStop(Math.min(0.99, (hz + 54) / H),
                   AKC.mixOklab(PAL.gravelLo, PAL.haze, 0.30));
    g.addColorStop((hz + (ap - hz) * 0.55) / H,
                   AKC.mixOklab(PAL.gravelLo, PAL.haze, 0.12));
    g.addColorStop(ap / H, "#231E17");
    g.addColorStop(Math.min(0.995, (ap + (H - ap) * 0.5) / H), PAL.gravelMid);
    g.addColorStop(1.00, "#241F18");
    cx.fillStyle = g;
    cx.fillRect(0, 0, W, H);

    // the reveal's own aggregate, scale graded with distance exactly as the
    // apron's is, so there is no grain boundary for an eye to find a box by
    var rnd = AK.rng(Math.floor(gx0) * 7 + 11);
    cx.save();
    for (i = 0; i < 5400; i++) {
      var d = Math.pow(rnd(), 0.55);
      var ax = rnd() * W;
      var ay = hz + d * (H - hz);
      var ar = 0.30 + d * 1.45;
      cx.globalAlpha = 0.05 + d * 0.15;
      cx.fillStyle = rnd() > 0.52 ? PAL.gravelHi : PAL.floor;
      cx.beginPath();
      cx.ellipse(ax, ay, ar * 2.0, ar * 0.70, -0.24, 0, Math.PI * 2);
      cx.fill();
    }
    cx.restore();
  }

  /* ---- the deck's one prop, modelled -------------------------------------- */
  // A FILLED POLYGON IN A BRIGHT HUE IS A SHAPE, NOT A THING. The first build
  // authored this wedge twice, inline, as one flat trapezoid with hairline ribs,
  // and the verdicts were unanimous across four frames: a sticker on the cover,
  // a yellow tab on 02, an unreadable smudge on 06, and on 09 three values of
  // dark brown laid on dark brown gravel where no critic could find it at all.
  // What makes it a thing is three planes under the one declared light. It lives
  // here rather than in four slides because it is the object that has meant the
  // flight's two ends since slide 01, and a prop drawn four ways is four props.
  function chockGeom(x, y, o) {
    var hw = o.hw || 46, h = o.h || 46;
    return {
      hw: hw, h: h,
      A: [x - hw, y], B: [x + hw, y],
      C: [x + hw * 0.65, y - h], D: [x - hw * 0.65, y - h * 0.86],
      // 0.13, not 0.26. At a quarter of the face height the top plane was nearly
      // as deep as the front was tall, which a camera kneeling at 620 mm cannot
      // see, and it made the prop read as a flat tray viewed from above.
      dp: [-hw * 0.12, -h * 0.13]          // the top plane's recession
    };
  }
  // The SILHOUETTE, handed to cast() so the shadow is the object's own outline
  // and not a second guess at it.
  function chockPath(x, y, o) {
    var G = chockGeom(x, y, o || {});
    return function (g, dx, dy) {
      g.moveTo(G.A[0] + dx, G.A[1] + dy);
      g.lineTo(G.B[0] + dx, G.B[1] + dy);
      g.lineTo(G.C[0] + dx, G.C[1] + dy);
      g.lineTo(G.C[0] + G.dp[0] + dx, G.C[1] + G.dp[1] + dy);
      g.lineTo(G.D[0] + G.dp[0] + dx, G.D[1] + G.dp[1] + dy);
      g.lineTo(G.D[0] + dx, G.D[1] + dy);
      g.closePath();
    };
  }
  function chock(cx, x, y, opts) {
    var o = opts || {}, G = chockGeom(x, y, o), k;
    var body = o.body || ["#5A5145", "#3B342B", "#241F19"];
    var quad = function (p1, p2, p3, p4, fill) {
      cx.fillStyle = fill;
      cx.beginPath();
      cx.moveTo(p1[0], p1[1]); cx.lineTo(p2[0], p2[1]);
      cx.lineTo(p3[0], p3[1]); cx.lineTo(p4[0], p4[1]);
      cx.closePath(); cx.fill();
    };
    var Cp = [G.C[0] + G.dp[0], G.C[1] + G.dp[1]];
    var Dp = [G.D[0] + G.dp[0], G.D[1] + G.dp[1]];

    // 1. THE TOP PLANE, which the key at elevation 24 strikes most squarely and
    //    which is therefore the brightest thing on the object. ONE MATERIAL MEANS
    //    ONE HUE: this was set in the bone register while the front carried gold,
    //    so it read as a separate pale card lying on a yellow wedge and the pair
    //    came out as two dustpans on the deck's cover. A lit plane of a painted
    //    object is a lighter VALUE of that object's own colour.
    quad(G.D, G.C, Cp, Dp, o.gold === false
         ? AKC.mixOklab(body[0], PAL.crown, 0.45)
         : AKC.mixOklab(PAL.gold, PAL.snow, 0.22));
    // 2. THE SHADOW END, turned away from azimuth 208, in the bounce hue because
    //    the only light reaching it is sky.
    quad(G.B, G.C, Cp, [G.B[0] + G.dp[0], G.B[1] + G.dp[1]],
         AKC.mixOklab(PAL.bounce, PAL.floor, 0.72));
    // 3. THE FRONT PLANE, the rubber body, carrying the paint.
    var g = cx.createLinearGradient(G.D[0], G.D[1], G.B[0], G.B[1]);
    g.addColorStop(0, body[0]); g.addColorStop(0.5, body[1]); g.addColorStop(1, body[2]);
    quad(G.A, G.B, G.C, G.D, g);

    // the painted face, worn, inset from the rubber so the paint sits ON it
    if (o.gold !== false) {
      var gp = cx.createLinearGradient(G.D[0], G.D[1], G.C[0], G.C[1] + G.h * 0.7);
      gp.addColorStop(0, PAL.gold);
      gp.addColorStop(0.62, "#D9A526");
      gp.addColorStop(1, "#9A7A22");
      cx.save();
      cx.globalAlpha = 0.93;
      quad([G.A[0] + 8, G.A[1] - 9], [G.B[0] - 8, G.B[1] - 9],
           [G.C[0] - 2, G.C[1] + G.h * 0.05], [G.D[0] + 2, G.D[1] + G.h * 0.04], gp);
      cx.restore();
    }
    // THREE shallow grooves, not eight full-height lines. Eight evenly spaced
    // dark strokes across the whole face read as keys, or as the bristles of a
    // brush, which is half of why the pair came out as dustpans. A moulded rubber
    // chock has a few deep grooves, and they do not reach the chamfer.
    cx.strokeStyle = "rgba(26,23,18,0.35)";
    cx.lineWidth = Math.max(2, G.hw * 0.045);
    for (k = -G.hw * 0.34; k <= G.hw * 0.34; k += G.hw * 0.34) {
      cx.beginPath();
      cx.moveTo(x + k, y - G.h * 0.16);
      cx.lineTo(x + k * 0.78, y - G.h * 0.62);
      cx.stroke();
    }
    // ONE hard highlight, on the chamfer where the top plane meets the front.
    cx.strokeStyle = "rgba(244,248,255,0.55)";
    cx.lineWidth = Math.max(1.4, G.hw * 0.043);
    cx.beginPath();
    cx.moveTo(G.D[0], G.D[1]); cx.lineTo(G.C[0], G.C[1]); cx.stroke();
    // the rope eye, a punched hole with an interior shadow and a lit lower rim
    cx.save();
    cx.fillStyle = PAL.floor;
    cx.beginPath();
    cx.ellipse(x - G.hw * 0.34, y - G.h * 0.52, G.hw * 0.10, G.hw * 0.07, 0, 0, Math.PI * 2);
    cx.fill();
    cx.strokeStyle = "rgba(168,148,111,0.6)";
    cx.lineWidth = 1;
    cx.beginPath();
    cx.ellipse(x - G.hw * 0.34, y - G.h * 0.50, G.hw * 0.10, G.hw * 0.07, 0, 0.2, Math.PI - 0.2);
    cx.stroke();
    cx.restore();
  }

  global.APRON = {
    W: W, H: H,
    chock: chock, chockPath: chockPath, returnOffset: returnOffset,
    litPool: litPool, baseWash: baseWash,
    trackY: trackY, trackPts: trackPts, returnPts: returnPts,
    ground: ground, trackMark: trackMark,
    yHorizon: yHorizon, yApron: yApron,
    LIGHT: LIGHT, castVec: castVec,
    PAL: PAL, PHANTOM_DASH: PHANTOM_DASH,
    skyBand: skyBand, treeline: treeline, apronBand: apronBand,
    makeField: makeField, hachure: hachure,
    crownPoints: crownPoints, drawCrowns: drawCrowns,
    cast: cast, clod: clod
  };
})(this);
