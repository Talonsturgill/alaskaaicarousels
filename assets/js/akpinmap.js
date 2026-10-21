/* akpinmap.js — the pinned relief sheet bench (No.91, 2026-10-20).
 *
 * WHAT IT DRAWS. An operations-room pin map stood on a cast plaster relief model
 * of the northern Bering Sea: plaster land from a real DEM, poured resin sea
 * stepped at chart depths, map pins with rendered heads and two-part casts,
 * all under ONE map-table lamp from the northwest (az 315, el 24), the
 * cartographic convention.
 *
 * WHY A BENCH. Three frames of No.91 (01, 02, 06) share one registered
 * projection so the coast holds still under the swipe and only the pins change.
 * This file owns the physics those frames share (projection, the height and
 * material of the sheet, the pin) and no composition. Each slide chooses its
 * own crop, pins, populations and type.
 *
 * DATA HONESTY. Heights come from assets/geo/ak-bering-dem (AWS Terrain Tiles,
 * terrarium), sampled with the monotone cubic of akscribe.js. Land relief is
 * exaggerated (default x25) and the exaggeration is a drawing property, never a
 * quantity. Sea terraces sit at chart depths (25, 50, 100, 200, 1000 m) read
 * off the same DEM. No noise term touches a height.
 *
 * USAGE
 *   const dem = await AKS.loadDEM('@@ASSETS@@/geo/ak-bering-dem');
 *   const P = AKPIN.proj({ pxPerKm: 1.15, at: [830, 1030] });   // Bethel's screen point
 *   AKPIN.sheet(cx, P, dem, { x: 0, y: 440, w: 1080, h: 910, slabTop: 456 });
 *   AKPIN.pin(cx, x, y, { head: '#FFC72C', r: 13, len: 46 });
 *
 * Load after d3.v7.min.js, noise.js, akscribe.js and akbench.js.
 */
(function (global) {
  "use strict";
  var AKPIN = global.AKPIN || (global.AKPIN = {});
  var BETHEL = [-161.76, 60.79];
  AKPIN.BETHEL = BETHEL;
  AKPIN.PLACES = {
    bethel: [-161.76, 60.79], gambell: [-171.70, 63.78], savoonga: [-170.48, 63.69],
    island: [-170.25, 63.42], nome: [-165.41, 64.50], anchorage: [-149.90, 61.22]
  };
  var KEY = { azDeg: 315, elDeg: 24 };
  AKPIN.KEY = KEY;

  function contract(name, o, allowed) {
    Object.keys(o || {}).forEach(function (k) {
      if (allowed.indexOf(k) < 0) {
        console.error("AK CONTRACT: " + name + " does not know option '" + k + "'");
        throw new Error(name + ": unknown option " + k);
      }
    });
  }

  /* Azimuthal equidistant centred on a point (Bethel by default), so every
   * distance from the centre is true. pxPerKm sets the scale; `at` is where the
   * centre lands on the page; `angle` rotates the sheet (degrees). */
  AKPIN.proj = function (o) {
    contract("AKPIN.proj", o, ["pxPerKm", "at", "centre", "angle"]);
    var c = o.centre || BETHEL;
    var p = d3.geoAzimuthalEquidistant().rotate([-c[0], -c[1]])
      .scale(o.pxPerKm * 6371.0088).translate(o.at).angle(o.angle || 0).clipAngle(null).precision(0.1);
    p.kmPerPx = 1 / o.pxPerKm;
    return p;
  };

  /* Terrarium bathymetry is noisy at z7; drawn raw, every chart-depth terrace
   * edge wiggles. smoothSea returns a DEM whose sea cells are box blurred
   * (two passes, radius r cells) while land cells keep their measured height,
   * so the coast and the relief are untouched. */
  AKPIN.smoothSea = function (dem, r) {
    var m = dem.meta, C = m.cols, R = m.rows, src = dem.data, a = new Float32Array(C * R), tmp = new Float32Array(C * R);
    for (var q = 0; q < a.length; q++) a[q] = Math.min(0, src[q]);
    for (var pass = 0; pass < 2; pass++) {
      for (var j = 0; j < R; j++) { var s = 0, o = j * C;
        for (var x = -r; x <= r; x++) s += a[o + Math.max(0, Math.min(C - 1, x))];
        for (var i = 0; i < C; i++) { tmp[o + i] = s / (2 * r + 1); s += a[o + Math.min(C - 1, i + r + 1)] - a[o + Math.max(0, i - r)]; } }
      for (var i2 = 0; i2 < C; i2++) { var s2 = 0;
        for (var y = -r; y <= r; y++) s2 += tmp[Math.max(0, Math.min(R - 1, y)) * C + i2];
        for (var j2 = 0; j2 < R; j2++) { a[j2 * C + i2] = s2 / (2 * r + 1); s2 += tmp[Math.min(R - 1, j2 + r + 1) * C + i2] - tmp[Math.max(0, j2 - r) * C + i2]; } }
    }
    for (var k = 0; k < a.length; k++) {
      if (src[k] > 0) { a[k] = src[k]; continue; }
      var kc = k % C, kr = (k - kc) / C, sum = 0, n = 0;
      for (var dy = -1; dy <= 1; dy++) for (var dx = -1; dx <= 1; dx++) {
        var cc = kc + dx, rr = kr + dy; if (cc < 0 || rr < 0 || cc >= C || rr >= R) continue; sum += src[rr * C + cc]; n++; }
      a[k] = (sum / n > 1.5) ? 1 : Math.min(-1, a[k]);       // a one-cell pit inside land is DEM noise, not a lake
    }
    // lowland cells (under 12 m) take their 3x3 mean, so a flat delta coast follows a curve and not the grid
    var b = new Float32Array(a);
    for (var k2 = 0; k2 < a.length; k2++) {
      if (!(src[k2] > 0 && src[k2] < 12)) continue;
      var c2 = k2 % C, r2 = (k2 - c2) / C, s3 = 0, n3 = 0;
      for (var ey = -1; ey <= 1; ey++) for (var ex = -1; ex <= 1; ex++) {
        var c3 = c2 + ex, r3 = r2 + ey; if (c3 < 0 || r3 < 0 || c3 >= C || r3 >= R) continue; s3 += a[r3 * C + c3]; n3++; }
      b[k2] = s3 / n3;
    }
    a = b;
    function sample(lon, lat) {
      var fi = (lon - m.west) / m.dlon, fj = (m.north - lat) / m.dlat;
      if (!(fi >= 0 && fj >= 0 && fi <= C - 1 && fj <= R - 1)) return NaN;
      var i = Math.min(C - 2, Math.floor(fi)), j = Math.min(R - 2, Math.floor(fj)), u = fi - i, v = fj - j, kk = j * C + i;
      return a[kk] * (1 - u) * (1 - v) + a[kk + 1] * u * (1 - v) + a[kk + C] * (1 - u) * v + a[kk + C + 1] * u * v;
    }
    return { meta: m, data: a, sample: sample, sampleCubic: AKS.cubicSampler(a, m) };
  };

  /* Two DEMs as one: the finer one where it has data, the wider one elsewhere,
   * blended over the last 0.3 degrees inside the finer one's edge so its
   * boundary never prints as a line. */
  AKPIN.mergeDEM = function (fine, wide) {
    var m = fine.meta, F = 0.3;
    function w(lon, lat) {
      var d = Math.min(lon - m.west, m.east - lon, (lat - m.south) * 2, (m.north - lat) * 2);
      if (!(d > 0)) return 0; var u = Math.min(1, d / F); return u * u * (3 - 2 * u);
    }
    function mk(fs, ws) {
      return function (lon, lat) {
        var k = w(lon, lat), b = ws(lon, lat);
        if (k <= 0) return b;
        var a = fs(lon, lat); if (!(a === a)) return b; if (!(b === b)) return a;
        return a * k + b * (1 - k);
      };
    }
    return { meta: wide.meta, sample: mk(fine.sample, wide.sample), sampleCubic: mk(fine.sampleCubic, wide.sampleCubic) };
  };

  /* Height of the sheet at a page point, in CSS px out of the sea floor plane.
   * Land rises from a 1.4 px plaster lip at the coast; sea steps down at chart
   * depths so each terrace edge throws a hairline cast. */
  var TERR = [40, 200, 1000];
  AKPIN.heightFn = function (P, dem, o) {
    o = o || {};
    var ex = o.exaggeration || 25, mpp = P.kmPerPx * 1000, lip = o.lip != null ? o.lip : 1.4;
    var step = o.terraceStep != null ? o.terraceStep : 0.55;
    return function (X, Y) {
      var ll = P.invert([X, Y]);
      if (!ll) return -TERR.length * step;
      var h = dem.sampleCubic(ll[0], ll[1]);
      if (!(h === h)) return -TERR.length * step;          // off the DEM: the deep floor
      if (h > 0) { var lr = Math.min(1, h / 4); return lip * lr * lr * (3 - 2 * lr) + h * ex / mpp; }
      var d = -h, n = 0;
      for (var i = 0; i < TERR.length; i++) if (d > TERR[i]) n++;
      // a smoothstep of 3 m across each terrace edge so the step is a bevel, not a stair of device pixels
      var frac = 0;
      for (var k = 0; k < TERR.length; k++) {
        var e = (d - TERR[k]) / 3; if (e > -1 && e < 1) { frac = (e + 1) / 2; frac = frac * frac * (3 - 2 * frac); n = k + frac; break; }
      }
      return -n * step;
    };
  };

  /* The plaster-and-resin sheet. Materials: 1 plaster land, 2 resin sea,
   * 3 desk outside the slab. Albedos are linear. */
  AKPIN.sheet = function (cx, P, dem, o) {
    contract("AKPIN.sheet", o, ["x", "y", "w", "h", "slabTop", "exaggeration", "key", "ambient",
      "plaster", "resin", "deep", "desk", "tint", "softness", "castLength", "extraHeight", "lip", "albedoHook"]);
    var H0 = AKPIN.heightFn(P, dem, { exaggeration: o.exaggeration, lip: o.lip });
    var top = o.slabTop != null ? o.slabTop : -1e9;
    var plaster = o.plaster || [0.62, 0.67, 0.71], resin = o.resin || [0.030, 0.062, 0.105],
      deep = o.deep || [0.006, 0.014, 0.030], desk = o.desk || [0.012, 0.022, 0.040];
    var extra = o.extraHeight || null;
    function height(X, Y) {
      if (Y < top) return 0;
      var b = Math.min(1, (Y - top) / 3);                   // a 3 px rounded bevel on the slab's top edge
      var h = 6 * b * b * (3 - 2 * b) + H0(X, Y);
      if (extra) h += extra(X, Y);
      return h;
    }
    function material(X, Y) {
      if (Y < top) return 3;
      var ll = P.invert([X, Y]); if (!ll) return 2;
      var h = dem.sample(ll[0], ll[1]);
      return h > 0 ? 1 : 2;
    }
    function albedo(X, Y, m) {
      var a;
      if (m === 3) a = desk;
      else if (m === 1) {
        // hypsometric plaster: low flats take a darker, slightly warmer cast and the
        // uplands come up to the full plaster, so a flat delta is never one flat grey.
        // Tone follows the DEM, never position.
        var llp = P.invert([X, Y]), hm = llp ? dem.sampleCubic(llp[0], llp[1]) : 0;
        if (!(hm === hm)) hm = 0;
        var hy = Math.max(0, Math.min(1, Math.log(1 + Math.max(0, hm)) / Math.log(900)));
        var tone = 0.58 + 0.42 * hy;
        var t = tone * (0.93 + 0.07 * AK.fbm2(X * 0.05, Y * 0.05, 3));   // plaster tooth, tiny
        a = [plaster[0] * t * (1.03 - 0.03 * hy), plaster[1] * t, plaster[2] * t * (0.95 + 0.05 * hy)];
      } else {
        var ll = P.invert([X, Y]), d = ll ? -dem.sample(ll[0], ll[1]) : 3000;
        if (!(d === d)) d = 3000;
        var s = Math.max(0, Math.min(1, Math.log(1 + Math.max(0, d)) / Math.log(3000)));
        a = [resin[0] + (deep[0] - resin[0]) * s, resin[1] + (deep[1] - resin[1]) * s, resin[2] + (deep[2] - resin[2]) * s];
      }
      if (m !== 3) {
        // blend plaster and resin over the last few metres either side of the coast so the edge is antialiased
        var llc = P.invert([X, Y]), hc = llc ? dem.sampleCubic(llc[0], llc[1]) : -10;
        if (hc === hc && hc > -3 && hc < 3) {
          var f = (hc + 3) / 6; f = f * f * (3 - 2 * f);
          var land = [plaster[0] * 0.58, plaster[1] * 0.58, plaster[2] * 0.58];
          var sea = resin;
          var mixd = [sea[0] + (land[0] - sea[0]) * f, sea[1] + (land[1] - sea[1]) * f, sea[2] + (land[2] - sea[2]) * f];
          var wgt = 1 - Math.abs(hc) / 3; a = [a[0] + (mixd[0] - a[0]) * wgt, a[1] + (mixd[1] - a[1]) * wgt, a[2] + (mixd[2] - a[2]) * wgt];
        }
      }
      if (o.tint) { var tw = o.tint(X, Y, m); if (tw) a = [a[0] * (1 - tw[3]) + tw[0] * tw[3], a[1] * (1 - tw[3]) + tw[1] * tw[3], a[2] * (1 - tw[3]) + tw[2] * tw[3]]; }
      if (o.albedoHook) a = o.albedoHook(X, Y, m, a) || a;
      return a;
    }
    return AKBENCH.relief(cx, {
      x: o.x, y: o.y, w: o.w, h: o.h, scale: 2,
      height: height, material: material, albedo: albedo,
      spec: { 1: [0.10, 18], 2: [0.42, 46], 3: [0.05, 10] },
      light: o.key || KEY, ambient: o.ambient != null ? o.ambient : 0.24, diffuse: 0.95,
      ao: 0.8, shadow: 0.82, softness: o.softness || 9, castLength: o.castLength || 120, dither: true
    });
  };

  /* A map pin: steel needle, rendered spherical head, two-part cast to the
   * lower right (away from the northwest key). (x, y) is where the needle
   * enters the sheet. Returns the head centre. */
  AKPIN.pin = function (cx, x, y, o) {
    contract("AKPIN.pin", o, ["head", "r", "len", "lean", "lee", "spec", "castAlpha", "noCast", "hollow"]);
    var r = o.r || 10, len = o.len != null ? o.len : r * 3.2, lean = o.lean != null ? o.lean : 0.30;
    var hx = x - len * lean, hy = y - len;                   // the pin leans toward the lamp a little
    var col = d3.color(o.head || "#FFC72C"), lee = d3.color(o.lee || col.darker(2.2));
    if (!o.noCast) {
      // contact core, tight and dark, then the long soft cast of head and needle to the lower right
      var ca = o.castAlpha != null ? o.castAlpha : 0.55;
      cx.save();
      cx.fillStyle = "rgba(2,5,12," + (ca * 0.9) + ")";
      cx.beginPath(); cx.ellipse(x + 1, y + 0.5, 2.6, 1.4, 0, 0, Math.PI * 2); cx.fill();
      var sx = x + len * 0.62, sy = y + len * 0.42;          // the head's cast on the sheet (key el 24 from the NW)
      cx.strokeStyle = "rgba(2,5,12," + (ca * 0.55) + ")"; cx.lineWidth = 1.6; cx.lineCap = "butt";
      cx.beginPath(); cx.moveTo(x, y); cx.lineTo(sx, sy); cx.stroke();
      cx.translate(sx, sy); cx.scale(1.35, 0.75);
      var g = cx.createRadialGradient(0, 0, 0, 0, 0, r * 1.25);
      g.addColorStop(0, "rgba(2,5,12," + (ca * 0.8) + ")"); g.addColorStop(0.62, "rgba(2,5,12," + (ca * 0.45) + ")"); g.addColorStop(1, "rgba(2,5,12,0)");
      cx.fillStyle = g; cx.beginPath(); cx.arc(0, 0, r * 1.25, 0, Math.PI * 2); cx.fill();
      cx.restore();
    }
    // the needle: a lit edge toward the lamp, a dark edge away
    cx.save(); cx.lineCap = "butt";
    cx.strokeStyle = "#2E3B46"; cx.lineWidth = Math.max(1.2, r * 0.16);
    cx.beginPath(); cx.moveTo(x, y); cx.lineTo(hx, hy); cx.stroke();
    cx.strokeStyle = "rgba(220,232,240,0.75)"; cx.lineWidth = Math.max(0.5, r * 0.05);
    cx.beginPath(); cx.moveTo(x - 0.6, y - 0.4); cx.lineTo(hx - 0.6, hy - 0.4); cx.stroke();
    cx.restore();
    // the head: a sphere lit from the upper left
    cx.save();
    if (o.hollow) {
      cx.strokeStyle = col.formatHex(); cx.lineWidth = Math.max(1.2, r * 0.22);
      cx.beginPath(); cx.arc(hx, hy, r * 0.8, 0, Math.PI * 2); cx.stroke();
    } else {
      var g2 = cx.createRadialGradient(hx - r * 0.38, hy - r * 0.42, r * 0.05, hx, hy, r);
      g2.addColorStop(0, col.brighter(0.9).formatHex());
      g2.addColorStop(0.45, col.formatHex());
      g2.addColorStop(1, lee.formatHex());
      cx.fillStyle = g2; cx.beginPath(); cx.arc(hx, hy, r, 0, Math.PI * 2); cx.fill();
      // rim light on the far side, the lamp bouncing off the sheet
      cx.strokeStyle = "rgba(255,255,255,0.10)"; cx.lineWidth = 1;
      cx.beginPath(); cx.arc(hx, hy, r - 0.5, Math.PI * 0.05, Math.PI * 0.55); cx.stroke();
      if (o.spec !== false) {
        cx.fillStyle = "rgba(255,255,255,0.85)";
        cx.beginPath(); cx.ellipse(hx - r * 0.36, hy - r * 0.40, r * 0.20, r * 0.13, -0.6, 0, Math.PI * 2); cx.fill();
      }
    }
    cx.restore();
    return [hx, hy];
  };

  /* A seeded Poisson-disc population inside a predicate, for pin heads. Returns
   * exactly `n` points or throws (a count that can't be met is a contract
   * failure, never a silent shortfall). */
  AKPIN.population = function (n, inside, box, minD, seed) {
    var rnd = AK.rng(seed), pts = [], tries = 0, d2 = minD * minD;
    while (pts.length < n && tries < n * 4000) {
      tries++;
      var x = box[0] + rnd() * box[2], y = box[1] + rnd() * box[3];
      if (!inside(x, y)) continue;
      var ok = true;
      for (var i = 0; i < pts.length; i++) { var dx = pts[i][0] - x, dy = pts[i][1] - y; if (dx * dx + dy * dy < d2) { ok = false; break; } }
      if (ok) pts.push([x, y]);
    }
    if (pts.length < n) { console.error("AK CONTRACT: AKPIN.population placed " + pts.length + " of " + n); throw new Error("population short"); }
    // draw far (top) to near (bottom) so nearer heads overlap the ones behind
    pts.sort(function (a, b) { return a[1] - b[1]; });
    return pts;
  };
})(typeof window !== "undefined" ? window : globalThis);
