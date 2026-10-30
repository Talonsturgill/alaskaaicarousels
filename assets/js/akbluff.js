/* akbluff.js — THE NIGHT CRANE, Carousel No.99's shared world (2026-10-29).
 *
 * One illustrative den drift banked against one Beaufort cutbank, under one
 * raking moon. Every frame of the deck composes its own picture of it in its
 * own file (PBR, engraving, carved snow, particles, thermal, hachure); nothing
 * here draws a slide. bespoke_check strips `<script src>` as harness, and it
 * should: the drift is the same drift because it is the same place.
 *
 * WORLD (metres): x east along the bank, z NORTH (toward the sea ice), y up.
 *   The plateau stands about 6.3 m south of the bank (z < 0), the scarp falls
 *   to the floodplain by z = 3, and a drift is banked on the scarp's north
 *   side, cresting at about 6.4 m at z = 0.6 and running out by z = 14. The
 *   drift thins to nothing past |x| = 30. Sastrugi run along the wind, which
 *   blows from the east north-east toward 250 degrees.
 *   The den is ILLUSTRATIVE: DEN = [1.4, z 5.4], about 1.6 m under the snow.
 *
 * LIGHT: the moon at azimuth 330 (north north-west), elevation 22. In three.js
 *   world (+z = north) its unit vector is MOON3. In a north-up PLAN (screen y
 *   down = south) it lights from the upper left: MOON_PLAN is the screen-space
 *   direction the light comes FROM.
 *
 * Needs noise.js (AK.simplex2, AK.fbm2) loaded first.
 *
 *   AKBLUFF.h(x, z)            height in metres
 *   AKBLUFF.snowDepth(x, z)    drift depth above the bare bank, metres
 *   AKBLUFF.normal(x, z)       unit normal [nx, ny, nz] (central difference, 5 cm)
 *   AKBLUFF.lambert(x, z, el?) max(0, n . moon), el overrides the moon elevation
 *   AKBLUFF.geometry(THREE, o) displaced PlaneGeometry over [x0,x1] x [z0,z1],
 *                              o.seg segments, o.heat true adds vertex colours of
 *                              the den's heat (gaussian, sigma o.sigma m) over a
 *                              base colour o.base [r,g,b] 0..1
 *   AKBLUFF.moonLight(THREE, i) a DirectionalLight from the moon, shadow-mapped
 */
(function (global) {
  "use strict";
  var B = {};
  var D2R = Math.PI / 180;

  B.MOON = { azDeg: 330, elDeg: 22, color: "#C7D6EE" };
  B.WIND_TO_DEG = 250;
  B.DEN = [1.4, 5.4];

  function moonVec(az, el) {
    var a = az * D2R, e = el * D2R;
    // three.js: +x east, +y up, +z north
    return [Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e)];
  }
  B.MOON3 = moonVec(B.MOON.azDeg, B.MOON.elDeg);
  // plan, north up: screen x = east, screen y = -north. Light comes FROM:
  B.MOON_PLAN = [B.MOON3[0], -B.MOON3[2]];

  function sstep(a, b, t) {
    var u = Math.min(1, Math.max(0, (t - a) / (b - a)));
    return u * u * (3 - 2 * u);
  }

  function noise() {
    if (!global.AK || !global.AK.simplex2) throw new Error("akbluff.js needs noise.js loaded first");
    return global.AK;
  }

  // the bare bank: plateau, scarp, floodplain
  function bare(x, z) {
    var A = noise();
    var plateau = 6.3 + 0.25 * A.fbm2(x * 0.045 + 3.1, z * 0.045 - 1.7, 3);
    var plain = 0.3 + 0.12 * A.fbm2(x * 0.03 - 7.0, z * 0.03 + 2.0, 3);
    var t = sstep(-0.6, 3.0, z + 0.35 * A.simplex2(x * 0.08, 4.4));
    return plateau * (1 - t) + plain * t;
  }

  // the drift's top, before sastrugi
  function driftTop(x, z) {
    var A = noise();
    var crestZ = 0.6 + 0.5 * A.simplex2(x * 0.05, 1.3);
    var runOut = 14 + 2.2 * A.simplex2(x * 0.04, 8.8);
    var top = 6.45 + 0.2 * A.simplex2(x * 0.07, 5.5) - 6.15 * sstep(crestZ, runOut, z);
    var env = sstep(31, 17, Math.abs(x - 1.0));
    return { top: top, env: env };
  }

  function sastrugi(x, z) {
    var A = noise();
    var w = B.WIND_TO_DEG * D2R;
    var u = x * Math.sin(w) + z * Math.cos(w);        // along the wind
    var v = x * Math.cos(w) - z * Math.sin(w);        // across it
    // sastrugi grow where the snow lies flat and wind-packed (the plain beyond the drift foot)
    var plainW = 0.55 + 0.9 * sstep(8, 18, z);
    var s = 0.07 * A.fbm2(u * 0.11, v * 0.95, 4);
    // smooth abs and smooth max: a crease sharper than the mesh cell prints as low-poly facets
    var f1 = A.fbm2(u * 0.30, v * 2.0, 3), f2 = A.fbm2(u * 0.62, v * 3.4, 2);
    s += plainW * 0.05 * Math.sqrt(f1 * f1 + 0.0025);
    s += plainW * 0.022 * 0.5 * (f2 + Math.sqrt(f2 * f2 + 0.0025));
    s += 0.004 * A.simplex2(x * 3.0, z * 3.0);
    return s;
  }

  B.snowDepth = function (x, z) {
    var b = bare(x, z), d = driftTop(x, z);
    return d.env * Math.max(0, d.top - b);
  };

  // the bank and drift without the sastrugi: for line work that must model the landform, not the noise
  B.hForm = function (x, z) {
    return bare(x, z) + B.snowDepth(x, z);
  };
  // the landform alone, with no small-scale noise at all: the bank as an engraver should read it
  B.hSmooth = function (x, z) {
    var A = noise();
    var t = sstep(-0.6, 3.0, z + 0.35 * A.simplex2(x * 0.08, 4.4));
    var b = 6.3 * (1 - t) + 0.3 * t;
    var d = driftTop(x, z);
    return b + d.env * Math.max(0, d.top - b);
  };

  B.h = function (x, z) {
    return bare(x, z) + B.snowDepth(x, z) + sastrugi(x, z);
  };

  B.normal = function (x, z) {
    var e = 0.05;
    var dx = (B.h(x + e, z) - B.h(x - e, z)) / (2 * e);
    var dz = (B.h(x, z + e) - B.h(x, z - e)) / (2 * e);
    var n = [-dx, 1, -dz], l = Math.hypot(n[0], n[1], n[2]);
    return [n[0] / l, n[1] / l, n[2] / l];
  };

  B.lambert = function (x, z, el) {
    var m = el == null ? B.MOON3 : moonVec(B.MOON.azDeg, el);
    var n = B.normal(x, z);
    return Math.max(0, n[0] * m[0] + n[1] * m[1] + n[2] * m[2]);
  };

  B.heat = function (x, z, sigma) {
    var s = sigma || 0.9;
    var d2 = (x - B.DEN[0]) * (x - B.DEN[0]) + (z - B.DEN[1]) * (z - B.DEN[1]);
    return Math.exp(-d2 / (2 * s * s));
  };

  B.geometry = function (THREE, o) {
    o = o || {};
    var x0 = o.x0 != null ? o.x0 : -40, x1 = o.x1 != null ? o.x1 : 40;
    var z0 = o.z0 != null ? o.z0 : -12, z1 = o.z1 != null ? o.z1 : 40;
    var seg = o.seg || 400;
    var g = new THREE.PlaneGeometry(x1 - x0, z1 - z0, seg, seg);
    g.rotateX(-Math.PI / 2);             // plane now in x/z; +z of the plane = north after the flip below
    var pos = g.attributes.position;
    var cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
    var col = o.heat ? new Float32Array(pos.count * 3) : null;
    var base = o.base || [1, 1, 1];
    for (var i = 0; i < pos.count; i++) {
      var x = pos.getX(i) + cx;
      var z = pos.getZ(i) + cz;           // rotateX(-90) maps plane +y to world -z; we treat world z as north directly
      pos.setX(i, x); pos.setZ(i, z);
      pos.setY(i, B.h(x, z));
      if (col) {
        var ht = B.heat(x, z, o.sigma || 0.45) * (o.heatGain != null ? o.heatGain : 1);
        var hot = o.hot || [1.0, 0.78, 0.17];
        col[i * 3] = base[0] * (1 - ht) + hot[0] * ht;
        col[i * 3 + 1] = base[1] * (1 - ht) + hot[1] * ht;
        col[i * 3 + 2] = base[2] * (1 - ht) + hot[2] * ht;
      }
    }
    if (col) g.setAttribute("color", new THREE.BufferAttribute(col, 3));
    g.computeVertexNormals();
    return g;
  };

  B.moonLight = function (THREE, intensity, o) {
    o = o || {};
    var L = new THREE.DirectionalLight(o.color || 0xc7d6ee, intensity != null ? intensity : 2.4);
    var d = o.dist || 60;
    L.position.set(B.MOON3[0] * d + (o.tx || 0), B.MOON3[1] * d, B.MOON3[2] * d + (o.tz || 0));
    L.target.position.set(o.tx || 0, 0, o.tz || 0);
    L.castShadow = true;
    var s = o.shadowSize || 30;
    L.shadow.mapSize.set(o.mapSize || 4096, o.mapSize || 4096);
    L.shadow.camera.left = -s; L.shadow.camera.right = s;
    L.shadow.camera.top = s; L.shadow.camera.bottom = -s;
    L.shadow.camera.near = 1; L.shadow.camera.far = d * 2.5;
    L.shadow.bias = -0.0003; L.shadow.normalBias = 0.02;
    L.shadow.radius = o.radius != null ? o.radius : 4;
    return L;
  };

  global.AKBLUFF = B;
})(typeof window !== "undefined" ? window : this);
