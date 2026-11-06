/* akletter.js -- changeable letterboard letters, Carousel No.106's shared furniture (2026-11-05).
 *
 * One deck draws the same white monoline letters on four frames: a GPU case at dusk (01), a frontal
 * plan relief of the felt (02), a macro focus pull on one letter (05) and the case at night (09).
 * The letters must be IDENTICAL on all four (the deck's claim is that the number never moves, only
 * where it lives), so their skeletons live here once. Nothing here draws a slide: each frame builds
 * its own scene, light and composition, and bespoke_check strips `<script src>` as harness.
 *
 *   AKLETTER.GLYPHS     monoline skeletons in a unit em (x right, y UP, baseline 0, cap height 1).
 *                       Each glyph is {adv, strokes:[{pts:[[x,y]...], curve:bool}]}.
 *   AKLETTER.layout(text, o)
 *                       Places glyphs left to right: returns [{ch, x, glyph}] in em units with
 *                       o.tracking (em, default 0.16) between advances; a space advances 0.42.
 *   AKLETTER.segments(text, o)
 *                       Every stroke flattened to 2D line segments [[x0,y0,x1,y1]...] in em units,
 *                       curves sampled at o.samples (default 14) per span: the 2D frames compute a
 *                       distance-to-skeleton height field from these.
 *   AKLETTER.build3D(THREE, text, o)
 *                       A THREE.Group of tube letters lying in the XZ plane (the board face), x right,
 *                       letter up = -Z, proud along +Y. o.height (m, cap height, default 0.1),
 *                       o.radius (m, stroke radius, default 0.004), o.flat (y scale of the tube,
 *                       default 0.55), o.mat (a material), o.pins (true: short pins below each glyph).
 *                       Straight strokes are cylinders with sphere joints, so corners stay crisp;
 *                       curves are Catmull-Rom tubes. Returns the group with userData.glyphs, one
 *                       sub-group per glyph (named by its character and index) for projection.
 *   AKLETTER.dome(THREE, R, o)
 *                       A painted sky-dome environment through PMREM: o.zenith, o.horizon, o.ground,
 *                       o.band (an optional warm band hex and its height fraction), o.window (an
 *                       optional bright rectangle {hex, u, v, w, h} in equirect UV, for a reflected
 *                       window), o.intensity. Replaces AKT.environment's softbox room, whose panels
 *                       would read in a glass pane as a studio.
 */
(function (global) {
  "use strict";
  var L = {};

  function C(x, y) { return [x, y]; }
  L.GLYPHS = {
    "1": { adv: 0.46, strokes: [{ pts: [C(0.06, 0.80), C(0.30, 1.0), C(0.30, 0.0)] }] },
    "4": { adv: 0.74, strokes: [
      { pts: [C(0.56, 0.0), C(0.56, 1.0)] },
      { pts: [C(0.56, 1.0), C(0.04, 0.30), C(0.72, 0.30)] }] },
    "D": { adv: 0.70, strokes: [
      { pts: [C(0.08, 0.0), C(0.08, 1.0)] },
      { pts: [C(0.08, 1.0), C(0.34, 1.0), C(0.56, 0.90), C(0.65, 0.66), C(0.65, 0.34),
              C(0.56, 0.10), C(0.34, 0.0), C(0.08, 0.0)], curve: true }] },
    "A": { adv: 0.70, strokes: [
      { pts: [C(0.02, 0.0), C(0.35, 1.0), C(0.68, 0.0)] },
      { pts: [C(0.14, 0.34), C(0.56, 0.34)] }] },
    "Y": { adv: 0.68, strokes: [
      { pts: [C(0.02, 1.0), C(0.34, 0.50), C(0.66, 1.0)] },
      { pts: [C(0.34, 0.50), C(0.34, 0.0)] }] },
    "S": { adv: 0.64, strokes: [
      { pts: [C(0.58, 0.86), C(0.47, 0.97), C(0.30, 1.0), C(0.13, 0.94), C(0.06, 0.78),
              C(0.14, 0.62), C(0.32, 0.54), C(0.50, 0.46), C(0.60, 0.30), C(0.56, 0.11),
              C(0.38, 0.0), C(0.19, 0.02), C(0.05, 0.14)], curve: true }] },
    "M": { adv: 0.80, strokes: [
      { pts: [C(0.06, 0.0), C(0.06, 1.0), C(0.40, 0.36), C(0.74, 1.0), C(0.74, 0.0)] }] },
    "E": { adv: 0.58, strokes: [
      { pts: [C(0.52, 1.0), C(0.08, 1.0), C(0.08, 0.0), C(0.52, 0.0)] },
      { pts: [C(0.08, 0.52), C(0.44, 0.52)] }] },
    "K": { adv: 0.64, strokes: [
      { pts: [C(0.08, 0.0), C(0.08, 1.0)] },
      { pts: [C(0.58, 1.0), C(0.10, 0.40)] },
      { pts: [C(0.24, 0.56), C(0.60, 0.0)] }] },
    "R": { adv: 0.64, strokes: [
      { pts: [C(0.08, 0.0), C(0.08, 1.0)] },
      { pts: [C(0.08, 1.0), C(0.36, 1.0), C(0.52, 0.93), C(0.58, 0.76), C(0.52, 0.59),
              C(0.36, 0.52), C(0.08, 0.52)], curve: true },
      { pts: [C(0.34, 0.52), C(0.60, 0.0)] }] },
    "T": { adv: 0.62, strokes: [
      { pts: [C(0.02, 1.0), C(0.60, 1.0)] },
      { pts: [C(0.31, 1.0), C(0.31, 0.0)] }] }
  };

  L.layout = function (text, o) {
    o = o || {};
    var tr = o.tracking == null ? 0.16 : o.tracking, x = 0, out = [];
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (ch === " ") { x += 0.42; continue; }
      var g = L.GLYPHS[ch];
      if (!g) throw new Error("AK CONTRACT: AKLETTER has no glyph '" + ch + "'");
      out.push({ ch: ch, x: x, glyph: g, index: i });
      x += g.adv + tr;
    }
    out.width = x - tr;
    return out;
  };

  function catmull(p0, p1, p2, p3, t) {
    var t2 = t * t, t3 = t2 * t;
    return [0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
            0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)];
  }
  function flatten(stroke, samples) {
    var p = stroke.pts;
    if (!stroke.curve) return p.slice();
    var out = [p[0]];
    for (var i = 0; i < p.length - 1; i++) {
      var p0 = p[Math.max(0, i - 1)], p1 = p[i], p2 = p[i + 1], p3 = p[Math.min(p.length - 1, i + 2)];
      for (var s = 1; s <= samples; s++) out.push(catmull(p0, p1, p2, p3, s / samples));
    }
    return out;
  }
  L.flatten = flatten;

  L.segments = function (text, o) {
    o = o || {};
    var lay = L.layout(text, o), segs = [], n = o.samples || 14;
    lay.forEach(function (g) {
      g.glyph.strokes.forEach(function (st) {
        var pts = flatten(st, n);
        for (var i = 0; i < pts.length - 1; i++)
          segs.push([g.x + pts[i][0], pts[i][1], g.x + pts[i + 1][0], pts[i + 1][1], g.index]);
      });
    });
    segs.width = lay.width;
    return segs;
  };

  L.build3D = function (THREE, text, o) {
    o = o || {};
    var H = o.height || 0.1, r = o.radius || 0.004, flat = o.flat == null ? 0.55 : o.flat;
    var mat = o.mat || new THREE.MeshStandardMaterial({ color: 0xeef1f4, roughness: 0.38, metalness: 0 });
    var pinMat = o.pinMat || new THREE.MeshStandardMaterial({ color: 0xc9cfd6, roughness: 0.5 });
    var lay = L.layout(text, o), root = new THREE.Group();
    root.userData.glyphs = [];
    function W(p, gx) { return new THREE.Vector3((gx + p[0]) * H, 0, -p[1] * H); }
    lay.forEach(function (g) {
      var grp = new THREE.Group(); grp.name = g.ch + "#" + g.index;
      g.glyph.strokes.forEach(function (st) {
        if (st.curve) {
          var pts = st.pts.map(function (p) { return W(p, g.x); });
          var curve = new THREE.CatmullRomCurve3(pts, false, "catmullrom", 0.5);
          var tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 160, r, 18, false), mat);
          grp.add(tube);
          [pts[0], pts[pts.length - 1]].forEach(function (e) {
            var cap = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 12), mat);
            cap.position.copy(e); grp.add(cap);
          });
        } else {
          for (var i = 0; i < st.pts.length - 1; i++) {
            var a = W(st.pts[i], g.x), b = W(st.pts[i + 1], g.x);
            var len = a.distanceTo(b);
            var cyl = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 18, 1, false), mat);
            cyl.position.copy(a).add(b).multiplyScalar(0.5);
            cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
            grp.add(cyl);
          }
          st.pts.forEach(function (p) {
            var j = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 12), mat);
            j.position.copy(W(p, g.x)); grp.add(j);
          });
        }
      });
      if (o.pins) {
        [[0.25, 0.2], [0.25, 0.8]].forEach(function (pp) {
          var pin = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.35, r * 0.35, r * 3, 8), pinMat);
          pin.position.set((g.x + Math.min(pp[0], g.glyph.adv * 0.5)) * H, -r * 1.6, -pp[1] * H);
          grp.add(pin);
        });
      }
      grp.scale.set(1, flat, 1);
      root.add(grp);
      root.userData.glyphs.push({ ch: g.ch, x: g.x * H, adv: g.glyph.adv * H, group: grp });
    });
    root.userData.width = lay.width * H;
    return root;
  };

  L.dome = function (THREE, R, o) {
    o = o || {};
    var c = document.createElement("canvas"); c.width = 1024; c.height = 512;
    var g = c.getContext("2d");
    var grad = g.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0.00, o.zenith || "#1C3550");
    grad.addColorStop(0.46, o.horizon || "#4E6F8F");
    if (o.band) { grad.addColorStop(0.49, o.band.hex); }
    grad.addColorStop(0.52, o.horizon || "#4E6F8F");
    grad.addColorStop(0.56, o.ground || "#15191E");
    grad.addColorStop(1.00, o.ground || "#15191E");
    g.fillStyle = grad; g.fillRect(0, 0, 1024, 512);
    if (o.window) {
      var w = o.window; g.fillStyle = w.hex;
      g.fillRect(w.u * 1024, w.v * 512, w.w * 1024, w.h * 512);
    }
    var tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    tex.colorSpace = THREE.SRGBColorSpace;
    var pm = new THREE.PMREMGenerator(R.renderer);
    var env = pm.fromEquirectangular(tex).texture;
    R.scene.environment = env;
    if ("environmentIntensity" in R.scene) R.scene.environmentIntensity = o.intensity != null ? o.intensity : 0.7;
    pm.dispose();
    return env;
  };

  global.AKLETTER = L;
})(typeof window !== "undefined" ? window : this);
