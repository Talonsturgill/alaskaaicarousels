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
    var ranks = [
      { step: 11, hMin: 16, hMax: 38, lift: 8,  mix: 0.62, salt: 3301 },
      { step: 15, hMin: 22, hMax: 58, lift: 0,  mix: 0.26, salt: 7919 }
    ];
    for (var k = 0; k < ranks.length; k++) {
      var R = ranks[k], i, gx, y, idx, rr, hgt, wd, t, spike;
      cx.beginPath();
      cx.moveTo(-40, H);
      for (i = -40; i <= W + 40; i += 2) {
        gx = gx0 + i;
        y = yHorizon(gx) - R.lift;
        idx = Math.floor(gx / R.step);
        rr = AK.rng(idx * R.salt);
        hgt = R.hMin + rr() * (R.hMax - R.hMin);
        wd = R.step * (0.55 + rr() * 0.75);
        t = (gx - idx * R.step) / wd;
        spike = t >= 0 && t < 1 ? (1 - Math.abs(2 * t - 1)) : 0;
        cx.lineTo(i, y - hgt * Math.pow(spike, 1.35));
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
    var ramp = AKC.ramp(hi, { steps: 7, keyHue: 60, ambientHue: 220 });
    var sunAz = LIGHT.az * Math.PI / 180;
    var p, gy, gxl, rnd;
    for (p = 0; p < passes; p++) {
      rnd = AK.rng(seed * 131 + p * 17);
      var azP = sunAz + (p - (passes - 1) / 2) * (3 * Math.PI / 180);
      cx.save();
      cx.globalAlpha = 0.22;
      cx.lineCap = "round";
      for (gy = y0; gy < y1; gy += grid) {
        for (gxl = -grid; gxl < W + grid; gxl += grid) {
          var jx = gxl + (rnd() - 0.5) * grid * 0.9;
          var jy = gy + (rnd() - 0.5) * grid * 0.9;
          var G = gx0 + jx;
          // central differences give slope and aspect
          var e = 2.2;
          var hL = field(G - e, jy), hR = field(G + e, jy);
          var hU = field(G, jy - e), hD = field(G, jy + e);
          var dzdx = (hR - hL) / (2 * e), dzdy = (hD - hU) / (2 * e);
          var slope = Math.hypot(dzdx, dzdy);
          var aspect = Math.atan2(dzdy, dzdx);
          // stroke width from slope, rotation from aspect, per Lehmann
          var wdt = 0.6 + Math.min(1.0, slope * 26) * 1.8;
          var len = grid * (1.5 + rnd() * 0.7);
          // shade against this pass's sun azimuth
          var nd = Math.max(0, Math.cos(aspect - azP));
          var step = Math.max(0, Math.min(ramp.length - 1,
                     Math.round(nd * (ramp.length - 1))));
          cx.strokeStyle = ramp[step];
          cx.lineWidth = wdt;
          var bend = (rnd() - 0.5) * 0.24;
          cx.beginPath();
          cx.moveTo(jx - Math.cos(aspect) * len / 2, jy - Math.sin(aspect) * len / 2);
          cx.quadraticCurveTo(jx + bend * len, jy + bend * len,
                              jx + Math.cos(aspect) * len / 2, jy + Math.sin(aspect) * len / 2);
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
  function cast(cx, path, h, alpha) {
    var v = castVec(h), steps = 16, i, t;
    var a = (alpha === undefined ? 0.55 : alpha);
    cx.save();
    cx.globalCompositeOperation = "multiply";
    cx.fillStyle = AKC.mixOklab(PAL.bounce, PAL.floor, 0.62);
    for (i = 1; i <= steps; i++) {
      t = i / steps;
      cx.globalAlpha = a * (1 - t * 0.62) * (2.6 / steps);
      cx.beginPath();
      path(cx, v[0] * t, v[1] * t);
      cx.fill();
    }
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
  function returnPts(gxFrom, gxTo, step) {
    var pts = [], gx;
    step = step || 18;
    for (gx = gxFrom; gx <= gxTo; gx += step) pts.push([gx, trackY(gx) + 40]);
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

    // AGGREGATE. The apron is not a flat fill. Exposed stone in the wearing
    // course, scale-graded with distance so the band carries a depth cue as
    // well as a texture, plus two polished tyre lanes where traffic runs.
    cx.save();
    cx.beginPath();
    cx.moveTo(0, hz);
    for (i = 0; i <= W; i += 6) cx.lineTo(i, yApron(gx0 + i));
    cx.lineTo(W, hz); cx.closePath(); cx.clip();
    rnd = AK.rng(seed * 401);
    for (i = 0; i < 11000; i++) {
      var ax = rnd() * W;
      var d = Math.pow(rnd(), 0.55);                 // 0 far, 1 near
      var ay = hz + d * (yApron(gx0 + ax) - hz);
      var ar = 0.35 + d * 2.2;
      var lit = rnd();
      cx.globalAlpha = (0.05 + d * 0.30) * (0.35 + 0.65 * d);
      cx.fillStyle = lit > 0.62 ? PAL.gravelHi
                   : (lit > 0.3 ? PAL.gravelMid : PAL.floor);
      cx.beginPath(); cx.arc(ax, ay, ar, 0, Math.PI * 2); cx.fill();
    }
    cx.restore();

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

    hachure(cx, gx0, { y0: ap - 12, y1: H, field: field, grid: o.grid || 9,
                       passes: o.passes || 4, seed: seed, hi: PAL.gravelHi });

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
  function baseWash(cx, gx0) {
    var hz = yHorizon(gx0 + W / 2);
    var g = cx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0.00, "#2A241D");
    g.addColorStop(hz / H * 0.82, "#3C342A");
    g.addColorStop(hz / H, "#5A4E3C");
    g.addColorStop(Math.min(0.98, hz / H + 0.20), "#332B21");
    g.addColorStop(1.00, "#221D17");
    cx.fillStyle = g;
    cx.fillRect(0, 0, W, H);
  }

  global.APRON = {
    W: W, H: H,
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
