/* akdrift.js — the chassis for No.61, THE DRIFT LINE (2026-09-17).
 *
 * A snow fence standing on open tundra at civil twilight, where the BAY INDEX
 * IS A CALENDAR and the PANEL POROSITY IS A DATA CLASSIFICATION. This file is
 * house furniture: the camera solve, the bay mapping, the fence geometry, the
 * screened ground, the barred cast and the type reserves. Every slide's own
 * composition lives in its own file and no slide calls a draw-the-whole-slide
 * function from here, because bespoke_check measures the outcome.
 *
 * ARCHITECTURE, and the reason for it. The DRIFT is drawn in Canvas 2D through
 * AKSNOW.surface rather than as displaced geometry in three.js. That is
 * deliberate. The bottom third of every frame is what qa.py's frame_balance()
 * measures, it only counts a cell carrying MODELED tone (luminance spread >= 8
 * AND tonal entropy >= 0.55), and AKSNOW.surface is the one helper in this
 * house fitted against that measurement. The FENCE is real PBR geometry
 * rendered through akthree into an offscreen canvas and composited, so the
 * structure gets real materials and soft shadow maps. The barred cast is drawn
 * on the 2D side from the same bay arithmetic that built the geometry, so the
 * shadow and the thing casting it can never disagree.
 *
 * THE LIGHT IS DECLARED ONCE, HERE, AND NEVER VARIED PER SLIDE.
 */
(function (global) {
  "use strict";
  var D = {};

  /* ---- the declared light ------------------------------------------------
   * Azimuth 158, elevation 14, key to fill 5.0 to 1. One disclosed exception,
   * written into the storyboard rather than hidden: the micro relief benches
   * shade at elevation 22 on the SAME azimuth, because a swelled line and a
   * slope width only spread across their legible range between about 20 and 30
   * degrees. Macro cast geometry at 14, micro form shading at 22.
   */
  D.LIGHT = {
    azDeg: 158,
    elDeg: 14,
    microElDeg: 22,
    keyToFill: 5.0,
    keyColor: 0xDCE9FF,
    fillColor: 0x16304C,
    shadowInk: "#071223"
  };

  /* ---- palette, one table, so no slide invents a hex ---------------------- */
  D.P = {
    zenith:   "#050B18",
    skyMid:   "#0B1728",
    haze:     "#16304C",
    shadow:   "#071223",
    lee:      "#0D1D31",
    snowFar:  "#1E3C5C",
    snowMid:  "#2E4F72",
    snowLit:  "#6E8FB4",
    crest:    "#AFC6E2",
    timberDk: "#2A3340",
    timberLt: "#5D6B7C",
    proposed: "#6EA5FF",
    gold:     "#FFC72C",
    snow:     "#F4F8FF",
    fixture:  "#46545F",
    mono:     "#8FA0AE"
  };

  /* ---- THE BAY CHAIN -----------------------------------------------------
   * Bay 01 is January 2025, one bay per month. The standing line ends at bay
   * 21, September 2026. Bay 23 is November and bay 25 is January 2027, and
   * both of those are stakes rather than fence, because a plan has built
   * nothing. Declared once for the deck; no slide authors its own fence.
   */
  D.BAY_ONE_YEAR = 2025;
  D.BAY_ONE_MONTH = 1;          /* January 2025 = bay 1 */
  D.BAY_LAST_BUILT = 21;        /* September 2026 */
  D.BAY_NOVEMBER = 23;
  D.BAY_REVIEW = 25;            /* January 2027 */
  D.BAY_PITCH_M = 2.4;
  D.RAIL_H_M = 1.8;

  D.bayToMonth = function (bay) {
    var m0 = (D.BAY_ONE_YEAR * 12 + (D.BAY_ONE_MONTH - 1)) + (bay - 1);
    return { year: Math.floor(m0 / 12), month: (m0 % 12) + 1 };
  };
  D.MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY",
              "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"];
  /* Month-first, and the run year is dropped per the house date rule. */
  D.bayLabel = function (bay, runYear) {
    var t = D.bayToMonth(bay);
    var s = D.MONTHS[t.month - 1];
    return t.year === runYear ? s : s + " " + t.year;
  };

  /* ---- THE THREE CLASSIFICATIONS, as porosity ---------------------------
   * These ratios are a property of the DRAWING, not a published figure, and
   * every dossier tags them [design]. The only load-bearing fact encoded here
   * is that NO PANEL IS EVER SOLID, because the standard conditions rather
   * than forbids. minGap() is the binary check every scene slide runs.
   */
  D.PANELS = [
    { key: "public",   label: "PUBLIC",       gap: 0.62 },
    { key: "internal", label: "INTERNAL USE", gap: 0.28 },
    { key: "restricted", label: "RESTRICTED", gap: 0.12 }
  ];
  D.panel = function (key) {
    for (var i = 0; i < D.PANELS.length; i++) if (D.PANELS[i].key === key) return D.PANELS[i];
    throw new Error("akdrift: no panel " + key);
  };
  D.minGap = function () {
    var m = 1; for (var i = 0; i < D.PANELS.length; i++) m = Math.min(m, D.PANELS[i].gap);
    return m;   /* must be strictly > 0 on every scene frame */
  };
  /* The panel a bay carries. Deterministic, so the same bay is the same class
   * on every slide that sees it, which is what makes the line ONE object. */
  D.bayPanel = function (bay) {
    return D.PANELS[(bay * 7 + 2) % 3];
  };

  /* ---- THE CAMERA SOLVE --------------------------------------------------
   * Solved once here so no slide eyeballs a horizon. fov is vertical and fixed
   * at 54 degrees for the whole deck.
   *   f = (H/2) / tan(fov/2)
   *   horizonY = cy - f * tan(pitchDown)
   *   a ground point at distance d projects to horizonY + f*h/d
   * THE CONTRACT IS horizonY IN PIXELS. If a renderer signs pitch the other
   * way, solve for pitch and the frame is unchanged.
   */
  D.W = 1080; D.H = 1350; D.FOV_DEG = 54;
  D.solve = function (heightM, pitchDownDeg) {
    var f = (D.H / 2) / Math.tan((D.FOV_DEG / 2) * Math.PI / 180);
    var cy = D.H / 2;
    var horizonY = cy - f * Math.tan(pitchDownDeg * Math.PI / 180);
    return {
      f: f, cy: cy, horizonY: horizonY, h: heightM, pitch: pitchDownDeg,
      groundY: function (d) { return horizonY + f * heightM / d; },
      /* apparent height in px of a vertical of `m` metres at distance d */
      vert: function (m, d) { return f * m / d; },
      /* on-screen bay pitch at distance d, which is what a repeated contact
       * pool radius must be checked against, never the post's own width */
      bayPx: function (d) { return f * D.BAY_PITCH_M / d; }
    };
  };

  /* ---- WORLD TO SCREEN ---------------------------------------------------
   * The same pinhole the GL stage is framed with, handed to the 2D pass.
   * D.solve answers questions about a FLAT ground at a known depth, which is
   * all a plan needs; this answers where an arbitrary world point lands, which
   * is what a 2D mark laid on a rendered object needs. Every law-bearing mark
   * in this deck was first placed at a hand-tuned constant, and a constant is
   * a number that has to be re-tuned every time the camera moves and is
   * silently wrong in between.
   *
   * Give it the frame's own `from` and `look`, the same two arrays passed to
   * AKT.frame, so there is one camera and not two. fov is VERTICAL, the way
   * three.js reads it, so f = (H/2) / tan(fov/2), which is the same f D.solve
   * computes. Returns null BEHIND the camera rather than a mirrored point.
   */
  D.camera = function (from, look, fovDeg) {
    var f = (D.H / 2) / Math.tan((fovDeg == null ? D.FOV_DEG : fovDeg) * Math.PI / 360);
    var fx = look[0] - from[0], fy = look[1] - from[1], fz = look[2] - from[2];
    var fl = Math.sqrt(fx * fx + fy * fy + fz * fz) || 1;
    fx /= fl; fy /= fl; fz /= fl;
    /* right = normalize(forward x worldUp); worldUp is (0,1,0) */
    var rx = -fz, ry = 0, rz = fx;
    var rl = Math.sqrt(rx * rx + rz * rz) || 1;
    rx /= rl; rz /= rl;
    /* up = right x forward */
    var ux = ry * fz - rz * fy, uy = rz * fx - rx * fz, uz = rx * fy - ry * fx;
    return {
      f: f,
      toScreen: function (x, y, z) {
        var dx = x - from[0], dy = y - from[1], dz = z - from[2];
        var d = dx * fx + dy * fy + dz * fz;
        if (!(d > 0.05)) return null;
        return {
          x: D.W / 2 + f * (dx * rx + dy * ry + dz * rz) / d,
          y: D.H / 2 - f * (dx * ux + dy * uy + dz * uz) / d,
          d: d
        };
      },
      /* apparent size in px of `m` metres at depth d, for a mark that has to
       * match the object it sits under */
      px: function (m, d) { return f * m / d; }
    };
  };

  /* ---- THE CONTACT COROLLARY ---------------------------------------------
   * A shadow map fitted to tens of metres of fence line cannot resolve the
   * centimetre of darkness where a post enters snow. Measured on slide 01 of
   * run No.61, the feet sat 1.7 L* under the snow beside them, which qa.py's
   * contact gate calls floating and which is also what the eye calls it. The
   * doctrine asks for a TWO-PART shadow, a tight contact plus a wide ambient,
   * and this paints exactly that at each foot: a core about a post wide and a
   * pool four times that, sized out of the depth so a near foot gets a bigger
   * pool than a far one for free.
   *
   * MULTIPLY, never an additive pool. A bright ring under every object with no
   * emitter anywhere in the picture is its own defect, it is what run No.59
   * shipped on nine frames out of nine, and qa.py now FAILS a declared contact
   * that sits inside one.
   *
   * SNAPPED TO THE SILHOUETTE, not to the flat-ground projection. This deck's
   * ground is a drift, so a post's real meeting with the snow is above where a
   * bare plane would put it; on slide 01 the sixth bay stands about 60 px of
   * deposit proud of its own flat-ground point. The mark walks UP the post's
   * own column in the composite and stops at the last row dark enough to be
   * timber, so it lands where the object and the snow actually meet. With no
   * separation in the strip it leaves the point alone rather than guessing.
   */
  D.footAO = function (cx, marks, o) {
    o = o || {};
    var tint = o.tint || "6,16,30";
    var coreA = o.core == null ? 0.62 : o.core;
    var poolA = o.pool == null ? 0.34 : o.pool;
    var off = D.offscreen(D.W, D.H), ox = off.cx;
    var placed = [];

    function ellipse(c, x, y, rx, ry, a0, stops) {
      var g = c.createRadialGradient(x, y, 0, x, y, rx);
      for (var i = 0; i < stops.length; i++) {
        g.addColorStop(stops[i][0], "rgba(" + tint + "," + (a0 * stops[i][1]).toFixed(4) + ")");
      }
      c.save();
      c.translate(x, y); c.scale(1, ry / rx); c.translate(-x, -y);
      c.fillStyle = g;
      c.beginPath(); c.arc(x, y, rx, 0, Math.PI * 2); c.fill();
      c.restore();
    }

    for (var i = 0; i < marks.length; i++) {
      var m = marks[i];
      if (!m) continue;
      var x = m.x, y = m.y, w = Math.max(1.2, m.w);
      if (x < -60 || x > D.W + 60) continue;
      if (o.snap !== false) y = D.snapToSilhouette(cx, x, y, w, o.snapReach == null ? 150 : o.snapReach);
      var pr = Math.max(18, w * 5.0);
      ellipse(ox, x, y, pr, Math.max(5, pr * 0.30), poolA, [[0, 1], [0.55, 0.42], [1, 0]]);
      var cr = Math.max(4.5, w * 1.30);
      ellipse(ox, x, y, cr, Math.max(2.4, cr * 0.42), coreA, [[0, 1], [0.60, 0.70], [1, 0]]);
      placed.push({ x: x, y: y, w: w, core: cr, pool: pr });
    }

    cx.save();
    cx.globalCompositeOperation = "multiply";
    if (o.blur !== 0) cx.filter = "blur(" + (o.blur == null ? 2 : o.blur) + "px)";
    cx.drawImage(off.canvas, 0, 0, D.W, D.H);
    cx.restore();
    return placed;
  };

  /* The silhouette walk, separate because it is the part that can be wrong and
   * the part worth reading on its own. Device pixels, because getImageData
   * ignores the context transform and this deck draws at scale(2,2).
   */
  D.snapToSilhouette = function (cx, x, y, w, reach) {
    var dpr = cx.canvas.width / D.W;
    var sx = Math.max(0, Math.round((x - w * 0.6) * dpr));
    var sw = Math.max(2, Math.min(cx.canvas.width - sx, Math.round(w * 1.2 * dpr)));
    var y0 = Math.max(0, Math.round((y - reach) * dpr));
    var y1 = Math.min(cx.canvas.height, Math.round((y + 26) * dpr));
    if (sw < 2 || y1 - y0 < 8) return y;
    var d;
    try { d = cx.getImageData(sx, y0, sw, y1 - y0).data; } catch (e) { return y; }
    var rows = y1 - y0, lum = new Float32Array(rows), lo = Infinity, hi = -Infinity;
    for (var r = 0; r < rows; r++) {
      var s = 0;
      for (var c = 0; c < sw; c++) {
        var i = (r * sw + c) * 4;
        s += 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
      }
      lum[r] = s / sw;
      if (lum[r] < lo) lo = lum[r];
      if (lum[r] > hi) hi = lum[r];
    }
    if (hi - lo < 24) return y;
    var cut = lo + (hi - lo) * 0.42;
    for (r = rows - 1; r >= 0; r--) if (lum[r] < cut) return y0 / dpr + r / dpr;
    return y;
  };

  /* ---- TYPE RESERVES -----------------------------------------------------
   * Measure the DOM first, then generate the field around it. The order is
   * always geometry, then the DOM the geometry implies, then reserve, then
   * draw. Boxes come from getBoundingClientRect so they are what actually
   * rendered, never a guess.
   */
  D.lineBoxes = function (sel, pad) {
    pad = pad == null ? 16 : pad;
    var out = [], els = document.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++) {
      var r = els[i].getBoundingClientRect();
      if (r.width < 2 || r.height < 2) continue;
      out.push([r.left - pad, r.top - pad, r.width + pad * 2, r.height + pad * 2]);
    }
    return out;
  };
  /* Reject-sample a point away from reserved boxes. An opaque element dropped
   * on a counted field erases the count, so any field whose COUNT is a claim
   * is told where the type is BEFORE it is generated. */
  D.clearOf = function (boxes, x, y) {
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      if (x >= b[0] && x <= b[0] + b[2] && y >= b[1] && y <= b[1] + b[3]) return false;
    }
    return true;
  };
  /* Punch reserves out of an offscreen field with BLURRED RECTANGLES, never a
   * radial gradient. A radial punch cannot reserve a long box: its outer
   * radius is half the longest side, so a 900px line of type keeps the field
   * over its first and last words while the middle is cleanly reserved. */
  D.punch = function (cx, boxes, blur) {
    blur = blur == null ? 9 : blur;
    cx.save();
    cx.globalCompositeOperation = "destination-out";
    cx.filter = "blur(" + blur + "px)";
    cx.fillStyle = "#000";
    for (var i = 0; i < boxes.length; i++) {
      cx.fillRect(boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]);
    }
    cx.restore();
  };
  D.offscreen = function (w, h) {
    var c = document.createElement("canvas");
    c.width = w * 2; c.height = h * 2;
    var x = c.getContext("2d"); x.scale(2, 2);
    return { canvas: c, cx: x };
  };

  /* ---- THE SCREENED GROUND ----------------------------------------------
   * One broad ramp across the WHOLE field along the light axis, never a radial
   * pool at an object's foot. A painted radial centred on an object's base
   * puts the frame's brightest and darkest values concentrically, which is a
   * hole in a spotlight and has been named by critics across three runs. The
   * cast is then an ATTACHED subtraction from this ramp.
   */
  D.groundRamp = function (cx, o) {
    var y0 = o.y0, y1 = o.y1, x0 = o.x0 == null ? 0 : o.x0, x1 = o.x1 == null ? D.W : o.x1;
    var ax = Math.cos((D.LIGHT.azDeg - 90) * Math.PI / 180);
    var ay = Math.sin((D.LIGHT.azDeg - 90) * Math.PI / 180);
    var g = cx.createLinearGradient(x0 - ax * (x1 - x0) * 0.5, y0 - ay * (y1 - y0) * 0.5,
                                    x1 + ax * (x1 - x0) * 0.5, y1 + ay * (y1 - y0) * 0.5);
    g.addColorStop(0.00, o.dark || D.P.lee);
    g.addColorStop(0.45, o.mid || D.P.snowMid);
    g.addColorStop(0.78, o.lit || D.P.snowLit);
    g.addColorStop(1.00, o.dark || D.P.lee);
    cx.save();
    cx.globalCompositeOperation = o.blend || "screen";
    cx.globalAlpha = o.alpha == null ? 0.5 : o.alpha;
    cx.fillStyle = g;
    cx.fillRect(x0, y0, x1 - x0, y1 - y0);
    cx.restore();
  };

  /* ---- THE BARRED CAST ---------------------------------------------------
   * The duty cycle of the bars on the snow EQUALS the gap ratio of the panel
   * that cast them, so the bottom band literally carries the classification
   * data. Drawn as a subtraction from the ramp above, never as painted
   * stripes. Below a 5 px period the bars stop and a graded directional tone
   * takes over, because at that pitch they are moire at feed scale and the
   * ratio is better kept in the label than in unreadable stripes.
   */
  D.MIN_BAR_PX = 5;
  D.barredCast = function (cx, o) {
    var period = o.period;                 /* on-screen px per bay-slat cycle */
    var duty = o.duty;                     /* == the panel's gap ratio */
    var x0 = o.x0, x1 = o.x1, yTop = o.yTop, yBot = o.yBot;
    var skew = o.skew == null ? 0.42 : o.skew;   /* run toward the camera */
    cx.save();
    cx.globalCompositeOperation = "multiply";
    if (period < D.MIN_BAR_PX) {
      cx.globalAlpha = o.alpha == null ? 0.5 : o.alpha;
      var g = cx.createLinearGradient(x0, yTop, x1, yBot);
      g.addColorStop(0, D.P.shadow); g.addColorStop(1, D.P.lee);
      cx.fillStyle = g; cx.fillRect(x0, yTop, x1 - x0, yBot - yTop);
      cx.restore();
      return { bars: 0, graded: true };
    }
    cx.fillStyle = o.ink || D.P.shadow;
    var barW = period * (1 - duty);        /* the SLAT casts; the gap passes */
    var n = 0;
    /* PERSPECTIVE, when the caller hands over its horizon (2026-09-17, No.61).
     * Parallel bars of constant period are right for a short band and wrong for
     * a ladder that runs to the bottom edge: ground scale is proportional to
     * (y - horizonY), so real bars widen AND spread as they come at you, and a
     * constant period reads as a printed stripe pattern rather than as light on
     * snow. With horizonY given, every bar edge is carried down the ray from
     * the vanishing point through its own start, which is what makes the set
     * converge. Without it, the old parallel behaviour is unchanged. */
    var hz = o.horizonY, k = 1;
    if (hz != null && yTop > hz) k = (yBot - hz) / (yTop - hz);
    var vpX = o.vpX == null ? (x0 + x1) / 2 - (yTop - (hz == null ? yTop : hz)) * skew : o.vpX;
    function foot(x) {
      if (hz == null || !(yTop > hz)) return x + (yBot - yTop) * skew;
      return vpX + (x - vpX) * k;
    }
    for (var x = x0; x < x1; x += period) {
      cx.globalAlpha = (o.alpha == null ? 0.55 : o.alpha) * (0.82 + 0.18 * Math.sin(x * 0.013));
      cx.beginPath();
      cx.moveTo(x, yTop);
      cx.lineTo(x + barW, yTop);
      cx.lineTo(foot(x + barW), yBot);
      cx.lineTo(foot(x), yBot);
      cx.closePath();
      cx.fill();
      n++;
    }
    cx.restore();
    return { bars: n, graded: false };
  };

  /* ---- THE FENCE, as real geometry --------------------------------------
   * Slats go in as InstancedMesh because twenty bays at engraving density is
   * thousands of thin boxes at 2160x2700, and the shadow camera is fitted to
   * the near field only. Any bay beyond `farSolid` metres is replaced by a
   * single plane carrying the same porosity, so no thin geometry exists at
   * distance to alias.
   */
  D.fence = function (THREE, AKT, R, o) {
    o = o || {};
    var fromBay = o.fromBay, toBay = o.toBay;
    /* yawDeg is measured OFF THE IMAGE PLANE, because that is how the
     * storyboard and every dossier state it ("the line runs roughly parallel
     * to the image plane at yaw 14 degrees"). Internally the step is taken
     * from the z axis, so the two differ by 90 and the conversion lives HERE,
     * once. Slide 01's first build passed 14 straight through, which put the
     * whole line outside the frustum and rendered a frame with no fence in it
     * and no error anywhere. */
    var yawRad = (90 - (o.yawDeg == null ? 14 : o.yawDeg)) * Math.PI / 180;
    /* AND THE MESHES TURN BY A DIFFERENT NUMBER (2026-09-17, No.61). The line
     * STEPS along (sin yaw, 0, cos yaw). A three.js mesh rotated by
     * rotation.y = phi sends its local X to (cos phi, 0, -sin phi), and those
     * two are the SAME direction only when phi = yaw - 90. Passing yawRad
     * straight to rotation.y turns every mesh a quarter turn off the line it
     * belongs to, and it rendered plausibly for a whole deck: the four rails
     * per bay, whose length runs along local X, stabbed away from the camera
     * and read as diagonal bracing (a critic called slide 04's gate "a tangle
     * of heavy black diagonal beams"), and every slat presented its 0.028 m
     * EDGE instead of its 0.055 m face, so the drawn open fraction was
     * 1 - 0.028/pitch instead of 1 - 0.055/pitch. That is why the Restricted
     * panel measured about 0.45 open against a printed 0.12: the frame's whole
     * data-in-art mapping was inverted by a missing 90 degrees. */
    var meshYaw = yawRad - Math.PI / 2;
    var z0 = o.z0 == null ? 0 : o.z0;
    var group = new THREE.Group();
    var timber = AKT.mat.clay(0x5D6B7C, { roughness: 0.86 });
    var timberDk = AKT.mat.clay(0x2A3340, { roughness: 0.9 });
    var slatGeo = new THREE.BoxGeometry(0.055, D.RAIL_H_M * 0.94, 0.028);
    var counts = 0, slatXf = [];
    /* the world point where each post enters the ground, returned so the 2D
     * pass can lay its contact under the post it belongs to instead of at a
     * constant that stops being true the next time the camera moves */
    var feet = [];

    for (var b = fromBay; b <= toBay; b++) {
      var along = (b - fromBay) * D.BAY_PITCH_M;
      var px = Math.sin(yawRad) * along + (o.x0 == null ? 0 : o.x0);
      var pz = z0 + Math.cos(yawRad) * along;

      /* post */
      var post = new THREE.Mesh(new THREE.BoxGeometry(0.10, D.RAIL_H_M * 1.04, 0.10), timberDk);
      post.position.set(px, D.RAIL_H_M / 2, pz);
      post.rotation.y = meshYaw;
      group.add(post);
      feet.push([px, 0, pz]);

      if (b === toBay) continue;
      var pan = o.forcePanel ? D.panel(o.forcePanel) : D.bayPanel(b);
      /* SLAT PITCH IS SOLVED FROM THE POROSITY, not guessed. A slat of width w
       * at pitch p leaves an open fraction 1 - w/p, so p = w / (1 - gap). The
       * first build used a fixed 0.22 m pitch with 0.14 m slats, which drew ten
       * fat bars per bay and read as a row of gravestones rather than a snow
       * fence. Real Wyoming-pattern slats are about 6 cm. */
      var SLAT_W = 0.055;
      var pitch = SLAT_W / Math.max(0.02, 1 - pan.gap);
      var nSlat = Math.max(3, Math.round(D.BAY_PITCH_M / pitch));
      for (var s = 0; s < nSlat; s++) {
        var t = (s + 0.5) / nSlat;
        slatXf.push([px + Math.sin(yawRad) * D.BAY_PITCH_M * t,
                     D.RAIL_H_M * 0.5,
                     pz + Math.cos(yawRad) * D.BAY_PITCH_M * t]);
        counts++;
      }
      /* four rails */
      for (var r4 = 0; r4 < 4; r4++) {
        var rail = new THREE.Mesh(
          new THREE.BoxGeometry(D.BAY_PITCH_M, 0.055, 0.038), timber);
        rail.position.set(px + Math.sin(yawRad) * D.BAY_PITCH_M / 2,
                          0.28 + r4 * 0.46,
                          pz + Math.cos(yawRad) * D.BAY_PITCH_M / 2);
        rail.rotation.y = meshYaw;
        group.add(rail);
      }
    }
    if (counts) {
      var inst = new THREE.InstancedMesh(slatGeo, timber, counts);
      var m = new THREE.Matrix4(), q = new THREE.Quaternion(),
          sc = new THREE.Vector3(1, 1, 1), v = new THREE.Vector3();
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), meshYaw);
      for (var i = 0; i < counts; i++) {
        v.set(slatXf[i][0], slatXf[i][1], slatXf[i][2]);
        m.compose(v, q, sc);
        inst.setMatrixAt(i, m);
      }
      inst.castShadow = true; inst.receiveShadow = false;
      inst.instanceMatrix.needsUpdate = true;
      group.add(inst);
    }
    /* ONE parent, ONE add. three.js REMOVES a mesh from its previous parent
     * when it is added to another, so `AKT.add(R, mesh)` followed by
     * `group.add(mesh)` silently empties the scene and renders a frame with
     * no fence in it and no error anywhere. Slide 01's first two builds did
     * exactly that. Build into the group, then add the group. */
    AKT.add(R, group);
    return { group: group, slats: counts, feet: feet, postW: 0.10 };
  };

  /* ---- THE GATE ----------------------------------------------------------
   * A gauged opening with three graduated chutes in the Restricted panel. It
   * carries the deck's ENTIRE gold budget and it is the conditional regime
   * made physical: the opening is the point, which is why gold is the OPENING
   * and never the barrier.
   */
  D.gate = function (THREE, AKT, R, o) {
    var g = new THREE.Group();
    var gold = AKT.mat.gold({ roughness: 0.3 });
    for (var i = 0; i < 3; i++) {
      var lip = new THREE.Mesh(new THREE.BoxGeometry(0.42 - i * 0.1, 0.045, 0.05), gold);
      lip.position.set(o.x, 0.52 + i * 0.4, o.z);
      /* the caller passes the LINE's yaw, the mesh turns by yaw - 90; see the
       * note in D.fence for the quarter turn this cost a whole deck */
      lip.rotation.y = (o.yawRad || 0) - Math.PI / 2;
      g.add(lip);
    }
    AKT.add(R, g);
    return g;
  };

  /* ---- THE DRIFT, AS GEOMETRY -------------------------------------------
   * The lee deposit belongs in the SAME scene as the fence, not pasted over
   * the render afterwards. Slide 01's first builds drew it as a separate 2D
   * mass and the two never met: the fence stood on a bare plane and an
   * unrelated white wave began below it with a hard edge. A displaced plane
   * costs almost nothing and gives the fence something to actually sit in,
   * with the GPU's own cast shadows falling across it.
   *
   * Profile is the standard lee lens, rising from the fence foot, cresting at
   * about 1.2 fence heights downwind and tapering out by about 11 heights,
   * which is the snow-fence engineering convention and is tagged [design]
   * wherever a slide prints it.
   */
  D.drift = function (THREE, AKT, R, o) {
    o = o || {};
    var lenAlong = o.lenAlong == null ? 70 : o.lenAlong;
    var reach = o.reach == null ? D.RAIL_H_M * 11 : o.reach;
    var peak = o.peak == null ? D.RAIL_H_M * 0.62 : o.peak;
    var segA = 180, segB = 40;
    /* how many metres the deposit takes to die at each end of the line */
    var endTaper = o.endTaper == null ? Math.min(7, lenAlong * 0.16) : o.endTaper;
    var g = new THREE.PlaneGeometry(lenAlong, reach, segA, segB);
    var pos = g.attributes.position;
    var rnd = (global.AK && AK.fbm2) ? AK.fbm2 : function () { return 0; };
    for (var i = 0; i < pos.count; i++) {
      var u = pos.getX(i), v = pos.getY(i);        /* v: 0 at fence, reach away */
      /* CLAMPED. A hair of floating-point slop at the leading edge makes t
       * negative, and Math.pow(negative, 0.42) is NaN, which poisons the
       * whole position attribute and prints a NaN bounding-sphere error
       * while still rendering a plausible frame. */
      var t = Math.min(1, Math.max(0, (v + reach / 2) / reach));
      /* lee lens: quick rise, crest at ~0.14 of the reach, long taper */
      var lens = Math.pow(Math.sin(Math.PI * Math.pow(t, 0.42)), 1.7);
      var h = peak * lens * (o.scale == null ? 1 : o.scale);
      h *= 0.82 + 0.34 * rnd(u * 0.07, 3.1, 4);    /* along-line variation */
      h += rnd(u * 0.5, 9.2, 3) * 0.05;            /* wind ripple */
      /* THE DEPOSIT HAS ENDS AND THEY ARE NOT WALLS. The carrier is a
       * rectangular plane, so the height field ran square off both ends of the
       * line: slide 06 of run No.61 rendered a pale mass with a near vertical
       * right edge dropping into fogged ground, which reads as a compositing
       * seam and is the exact thing that frame's own dossier said to avoid, "a
       * tapering lens with its own falloff, never an edge". Real drift stops
       * where the fence stops, and it takes a few metres to do it. */
      if (endTaper > 0.01) {
        var e = Math.min(u + lenAlong / 2, lenAlong / 2 - u) / endTaper;
        e = Math.min(1, Math.max(0, e));
        h *= e * e * (3 - 2 * e);                  /* smoothstep, both ends */
      }
      pos.setZ(i, h);
    }
    g.computeVertexNormals();
    var m = new THREE.Mesh(g, AKT.mat.clay(o.color == null ? 0x8FB0D0 : o.color,
      { roughness: 0.95, metalness: 0.0 }));
    m.rotation.x = -Math.PI / 2;
    m.position.set(o.x == null ? 0 : o.x, 0.012, o.z == null ? 0 : o.z);
    if (o.yawDeg != null) m.rotation.z = (90 - o.yawDeg) * Math.PI / 180;
    AKT.add(R, m, { cast: false, receive: true });
    return m;
  };

  /* ---- THE STAGE ---------------------------------------------------------
   * The scene setup every scene frame shares: the sky backdrop, the IBL, the
   * declared rig, the ground. It lives here because it is HOUSE FURNITURE and
   * because bespoke_check measures how much of each slide's own drawing code
   * is its own. What a slide does with the stage, what it puts on it and how
   * it frames it, is the slide's own file.
   *
   * Returns R plus a compose(cx) that blits the render and reports the
   * snapshot sentinel, so no slide can forget to check .ok.
   */
  D.stage = function (THREE, AKT, glCanvas, o) {
    o = o || {};
    var R = AKT.setup(glCanvas, {
      w: D.W, h: D.H, fov: D.FOV_DEG,
      fog: o.fog || [0x16304C, 34, 120],
      exposure: o.exposure == null ? 1.08 : o.exposure
    });
    /* sky as a backdrop INSIDE the scene: at low camera heights the fence
     * crosses the horizon, so a 2D sky pass would clip its tops. */
    var c = document.createElement("canvas");
    c.width = 8; c.height = 512;
    var xx = c.getContext("2d");
    var g = xx.createLinearGradient(0, 0, 0, 512);
    var stops = (o.sky || [[0, D.P.zenith], [0.44, D.P.skyMid], [0.86, D.P.haze], [1, D.P.haze]]).slice();
    /* THE SKY'S LAST STOP IS THE FOG COLOUR, ALWAYS (2026-09-17, No.61).
     * The ground plane is 300 m across and the fog closes at 120, so the ground
     * is EXACTLY the fog colour long before its own far edge. The sky backdrop
     * hangs behind that edge. If the gradient's bottom stop is any other hue,
     * the two meet in a dead straight full width step with no physical cause:
     * slide 01 shipped one at y 473 in #16304C against #20415F and a critic
     * read it as a composite seam in the deck's largest soft gradient. Tying
     * the stop to the fog argument makes the two unable to disagree, whatever
     * a slide passes for the rest of the ramp. */
    var fogArg = o.fog || [0x16304C, 34, 120];
    var fogHex = "#" + ("000000" + (fogArg[0] >>> 0).toString(16)).slice(-6);
    stops[stops.length - 1] = [stops[stops.length - 1][0], fogHex];
    for (var i = 0; i < stops.length; i++) g.addColorStop(stops[i][0], stops[i][1]);
    xx.fillStyle = g; xx.fillRect(0, 0, 8, 512);
    var tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    var sky = new THREE.Mesh(new THREE.PlaneGeometry(500, 220),
      new THREE.MeshBasicMaterial({ map: tex, fog: false, depthWrite: false }));
    sky.position.set(0, 56, -150);
    R.scene.add(sky);

    AKT.environment(R, { intensity: o.ibl == null ? 0.40 : o.ibl });

    var az = D.LIGHT.azDeg * Math.PI / 180, el = D.LIGHT.elDeg * Math.PI / 180;
    var ki = o.keyI == null ? 3.35 : o.keyI;
    AKT.rig(R, {
      key:  { color: D.LIGHT.keyColor, i: ki, radius: o.softness == null ? 6 : o.softness,
              shadowSize: o.shadowSize == null ? 26 : o.shadowSize,
              pos: [Math.sin(az) * 34, Math.tan(el) * 34, Math.cos(az) * 34] },
      fill: { color: D.LIGHT.fillColor, i: ki / D.LIGHT.keyToFill, pos: [-9, 10, 16] },
      ambient: { color: 0x16304C, i: o.ambient == null ? 0.78 : o.ambient }
    });
    AKT.ground(R, { size: 300, color: o.ground == null ? 0x27486C : o.ground,
                    roughness: 0.97, y: 0 });

    R.compose = async function (cx) {
      var shot = await AKT.snapshot(R);
      var ok = !!(shot && shot.ok);
      if (ok) cx.drawImage(glCanvas, 0, 0, D.W, D.H);
      return ok;    /* never ship a black frame: the caller draws its fallback */
    };
    return R;
  };

  /* ---- THE STAKE LINE ----------------------------------------------------
   * What is PROPOSED and not built. Survey stakes beyond the last standing
   * bay, drawn in forget-me-not, carrying NO drift and casting NO shadow,
   * because a plan has deposited nothing. Gold never touches this line.
   */
  D.stakes = function (THREE, AKT, R, o) {
    var g = new THREE.Group();
    var yawRad = (90 - (o.yawDeg == null ? 14 : o.yawDeg)) * Math.PI / 180;
    var mat = new THREE.MeshBasicMaterial({ color: 0x6EA5FF, fog: true });
    for (var b = o.fromBay; b <= o.toBay; b++) {
      var along = (b - o.fromBay) * D.BAY_PITCH_M;
      var px = Math.sin(yawRad) * along + o.x0;
      var pz = o.z0 + Math.cos(yawRad) * along;
      /* a stake is a dashed vertical: short segments with gaps, so it reads as
       * a drafting phantom rather than as a post */
      for (var k = 0; k < 5; k++) {
        var seg = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.13, 0.045), mat);
        seg.position.set(px, 0.10 + k * 0.23, pz);
        seg.castShadow = false; seg.receiveShadow = false;
        g.add(seg);
      }
    }
    R.scene.add(g);      /* NOT AKT.add: these must not cast or receive */
    return g;
  };

  /* ---- THE LAW-BEARING INKS, DRAWN IN 2D --------------------------------
   * The gate and the stake line are geometry in the GL scene, and the GL frame
   * reaches the art canvas through a single drawImage. qa.py's ink-law census
   * reads the BRUSH, meaning canvas ops, gradient stops, DOM text and SVG
   * shapes, and it cannot see inside a composited bitmap. So a frame whose
   * data-ink promises gold, with the only gold inside the render, fails its
   * own declaration while looking correct.
   *
   * These two draw the law-bearing inks ON the art canvas, at the gate's and
   * the stakes' own projected positions. That satisfies the census honestly,
   * because the mark IS the thing the law is about, and it fixes a real
   * legibility problem at the same time: at 432 px the gate was a few pixels
   * of specular and the stake line nearly vanished.
   */
  D.gateMark = function (cx, o) {
    var x = o.x, y = o.y, w = o.w == null ? 46 : o.w;
    cx.save();
    cx.strokeStyle = D.P.gold;
    cx.lineCap = "round";
    for (var i = 0; i < 3; i++) {
      var ww = w * (1 - i * 0.22);
      cx.lineWidth = (o.weight == null ? 3.2 : o.weight) * (1 - i * 0.12);
      cx.globalAlpha = 0.95 - i * 0.12;
      cx.beginPath();
      cx.moveTo(x - ww / 2, y + i * (o.pitch == null ? 15 : o.pitch));
      cx.lineTo(x + ww / 2, y + i * (o.pitch == null ? 15 : o.pitch));
      cx.stroke();
    }
    cx.restore();
    return { what: "the gate, three graduated chutes",
             rect: [x - w / 2 - 4, y - 6, w + 8, 2 * (o.pitch == null ? 15 : o.pitch) + 12] };
  };

  D.stakeMark = function (cx, pts, o) {
    o = o || {};
    cx.save();
    cx.strokeStyle = D.P.proposed;
    cx.lineWidth = o.weight == null ? 2.6 : o.weight;
    cx.globalAlpha = o.alpha == null ? 0.92 : o.alpha;
    cx.setLineDash(o.dash || [7, 9]);
    for (var i = 0; i < pts.length; i++) {
      cx.beginPath();
      cx.moveTo(pts[i][0], pts[i][1]);
      cx.lineTo(pts[i][0], pts[i][1] - (pts[i][2] == null ? 44 : pts[i][2]));
      cx.stroke();
    }
    /* the run of the proposed line, dashed, carrying nothing */
    if (o.run && pts.length > 1) {
      cx.globalAlpha = 0.55;
      cx.beginPath();
      for (var k = 0; k < pts.length; k++) {
        var yy = pts[k][1] - (pts[k][2] == null ? 44 : pts[k][2]);
        if (k === 0) cx.moveTo(pts[k][0], yy); else cx.lineTo(pts[k][0], yy);
      }
      cx.stroke();
    }
    cx.setLineDash([]);
    cx.restore();
  };

  /* ---- THE MEASURED VEIL -------------------------------------------------
   * A soft dark wash laid under MEASURED line boxes, on the art canvas, before
   * the DOM paints over it. This is how display type keeps its worst-point
   * contrast over a lit ground without a hard plate, which would read as
   * furniture and would score as flat in the bottom band. Boxes come from
   * getBoundingClientRect, so the veil is under what actually rendered.
   *
   * Per line box, never one rect over a paragraph: a single wash over a block
   * darkens the gaps between lines as much as the glyphs and reads as a plate.
   */
  D.veil = function (cx, boxes, o) {
    o = o || {};
    /* THE FEATHER IS SOLVED FROM THE BOX, NEVER FIXED (2026-09-17, No.61).
     * The first version filled hard rectangles and blurred the whole sheet by
     * a constant 16 px. On a 40 px line that is a soft wash; on slide 02's
     * 240 px block under MAY it left four straight edges, and the critic
     * called it the single most damaging craft defect on the frame, visible
     * as a black box even in the 432 px thumb. A wash that is trying not to
     * read as a plate cannot have a straight edge anywhere, at any size.
     *
     * So each box is drawn as a LOZENGE, inset by its own feather and blurred
     * by it, which means the ink never reaches a corner and the falloff is
     * always about as wide as the line is tall. The blur is set per box while
     * it is drawn, so a mono kicker and a 186 px display word get the falloff
     * each of them needs out of one call. */
    var off = D.offscreen(D.W, D.H), ox = off.cx;
    var ink = o.ink || "#040A14";
    var placed = [];
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      var w = b[2], h = b[3];
      if (!(w > 1 && h > 1)) continue;
      var feather = o.feather == null
        ? Math.max(16, Math.min(h * 0.60, w * 0.30)) : o.feather;
      /* INSET, BUT NEVER MORE THAN A FIFTH OF EITHER SIDE. Insetting by the
       * full feather on a long thin line box eats its two ends: the lozenge
       * shrinks to the middle of the run and the blur tapers away before the
       * first and last words, which is the same end-of-line weakness a radial
       * reserve has. qa.py measured it as 4.3 at the ends of a 205 px line
       * whose middle read 10.2. Give the box its own inset per axis. */
      var ix = Math.min(feather * 0.5, w * 0.20);
      var iy = Math.min(feather * 0.5, h * 0.20);
      var x = b[0] + ix, y = b[1] + iy;
      var ww = Math.max(2, w - ix * 2), hh = Math.max(2, h - iy * 2);
      var r = Math.min(hh / 2, ww / 2);
      ox.save();
      ox.filter = "blur(" + feather.toFixed(1) + "px)";
      ox.fillStyle = ink;
      ox.beginPath();
      if (ox.roundRect) {
        ox.roundRect(x, y, ww, hh, r);
      } else {
        ox.moveTo(x + r, y);
        ox.arcTo(x + ww, y, x + ww, y + hh, r);
        ox.arcTo(x + ww, y + hh, x, y + hh, r);
        ox.arcTo(x, y + hh, x, y, r);
        ox.arcTo(x, y, x + ww, y, r);
      }
      ox.fill();
      ox.restore();
      placed.push([x, y, ww, hh, feather]);
    }
    cx.save();
    cx.globalCompositeOperation = "multiply";
    cx.globalAlpha = o.alpha == null ? 0.62 : o.alpha;
    cx.drawImage(off.canvas, 0, 0, D.W, D.H);
    cx.restore();
    return placed;
  };

  /* ---- INK EXTENTS, NOT ELEMENT BOXES -----------------------------------
   * getBoundingClientRect on a text block returns the BLOCK, so a two line ask
   * whose longest line ends at x 690 hands back a box to x 885 and the veil
   * under it overruns its own type by 195 px and reads as a third plate
   * (slide 09, No.61). Range.getClientRects returns one rect per LINE BOX, at
   * the width the line actually inked, which is the thing a wash is supposed
   * to follow. Falls back to the element box when a node has no text.
   */
  D.inkBoxes = function (sel, pad) {
    pad = pad == null ? 12 : pad;
    var out = [], els = document.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++) {
      var el = els[i], got = 0;
      try {
        var rng = document.createRange();
        rng.selectNodeContents(el);
        var rects = rng.getClientRects();
        for (var k = 0; k < rects.length; k++) {
          var r = rects[k];
          if (r.width < 2 || r.height < 2) continue;
          out.push([r.left - pad, r.top - pad, r.width + pad * 2, r.height + pad * 2]);
          got++;
        }
      } catch (e) { /* fall through to the element box */ }
      if (!got) {
        var b = el.getBoundingClientRect();
        if (b.width > 1 && b.height > 1) {
          out.push([b.left - pad, b.top - pad, b.width + pad * 2, b.height + pad * 2]);
        }
      }
    }
    return out;
  };

  /* ---- THE HOUSE GRADE, declared once ------------------------------------
   * AKPOST.grade's contract is strict and its failure mode is a black canvas
   * with errors=0, so the deck's grade is written here ONCE in the validated
   * shape and every slide passes D.GRADE or D.GRADE_FLAT. exposure is in
   * STOPS (akthree's AKT.setup exposure is a MULTIPLIER, and confusing the two
   * shipped a full stop over on eighteen slides across two earlier runs).
   * lift and gain are 3-element numeric arrays, never hex strings.
   */
  D.GRADE = {
    exposure: 0.0, saturation: 1.04, contrast: 1.06, vignette: 0.18,
    bloom: { threshold: 0.74, strength: 0.26, radius: 8 },
    grain: { amount: 0.055, size: 2, seed: 20260917 },
    lift: [0.010, 0.015, 0.028], gain: [1.012, 1.0, 0.978],
    dither: true, aberration: 0.5, sharpen: 0.32
  };
  /* No aberration on a frame carrying a COMPARISON or a measured axis, per
   * the restraint note in TECHNIQUE_LIBRARY 89. */
  D.GRADE_FLAT = (function () {
    var g = {}; for (var k in D.GRADE) g[k] = D.GRADE[k];
    g.aberration = 0; g.bloom = { threshold: 0.78, strength: 0.18, radius: 6 };
    return g;
  })();

  global.AKDRIFT = D;
})(window);
