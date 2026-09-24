/* akvalley.js — REAL terrain seen through a perspective camera, drawn as marks.
 * Added 2026-09-24 for run No.67 (XPRIZE Wildfire at Nenana). House furniture:
 * it loads a committed DEM and draws the ground; every slide still owns its own
 * composition, overlays and instruments.
 *
 * WHAT IT DRAWS. Ridgeline profiles cut PERPENDICULAR TO THE CAMERA HEADING
 * (not along lines of latitude, which read as radiating spokes to any camera
 * not looking due north or south), far to near, each one filled with the ground
 * colour before it is stroked, so nearer ground occludes farther ground with no
 * sort. The stroke of every segment is LIT OR LEE by the dot product of the real
 * terrain normal with one key light, so relief is carried by line weight and
 * tone rather than by fill. Draped lines (rivers, a survey square) are bucketed
 * by depth and flushed between profiles, so a ridge hides what is behind it.
 *
 * DATA. assets/geo/nenana-dem.bin + .json (AWS terrain tiles, zoom 10, 197 m
 * cells, Web Mercator rows). Heights are metres; the vertical exaggeration VE
 * is a parameter the slide prints. Nothing here is noise: take the DEM away and
 * there is no picture.
 *
 * GEOMETRY. Local kilometres about an origin (default Nenana, 64.5639 N
 * 149.0931 W): x east, z SOUTH, y up in km times VE. Heading is degrees
 * clockwise from north; pitch is degrees, negative looks down.
 *
 *   const V = await AKV.load('@@ASSETS@@');
 *   const cam = V.camera({lon, lat, agl: 2500, heading: 190, pitch: -14,
 *                         fov: 56, W: 1080, H: 1350, cy: 560});
 *   const st = V.terrain(cx, cam, {light: {az: 315, el: 30}, ...});
 *   const p = V.project(cam, lon, lat, 0);   // [x, y, depth] or null
 */
(function (global) {
  "use strict";
  var D2R = Math.PI / 180;

  function hexRGB(s) {
    s = s.replace("#", "");
    return [parseInt(s.slice(0, 2), 16), parseInt(s.slice(2, 4), 16), parseInt(s.slice(4, 6), 16)];
  }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function css(c, a) { return "rgba(" + (c[0] | 0) + "," + (c[1] | 0) + "," + (c[2] | 0) + "," + (a === undefined ? 1 : a) + ")"; }

  /* quiet: knock the art back behind small type (the station card and the
   * site fixture), feathered, so no stroke crosses a glyph. It clears the
   * canvas to the sky beneath rather than laying a plate on top. */
  function quietCanvas(cx, sels, st) {
    st = st || {};
    var pad = st.pad || [22, 10], fe = st.feather || 10;
    cx.save();
    cx.globalCompositeOperation = "destination-out";
    cx.filter = "blur(" + fe + "px)";
    cx.fillStyle = "rgba(0,0,0," + (st.alpha || 0.92) + ")";
    sels.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (!r.width) return;
        cx.fillRect(r.left - pad[0], r.top - pad[1], r.width + 2 * pad[0], r.height + 2 * pad[1]);
      });
    });
    cx.restore();
  }

  async function load(base, opts) {
    var o = opts || {};
    var meta = await (await fetch(base + "/geo/nenana-dem.json")).json();
    var H = new Int16Array(await (await fetch(base + "/geo/nenana-dem.bin")).arrayBuffer());
    var rivers = await (await fetch(base + "/geo/nenana-rivers.geo.json")).json();
    var transport = await (await fetch(base + "/geo/nenana-transport.geo.json")).json();
    var C = meta.cols, R = meta.rows, n = Math.pow(2, meta.z), f = meta.downsample;
    var cL = meta.crop_px[0], cT = meta.crop_px[1];
    var LAT0 = o.lat0 === undefined ? 64.5639 : o.lat0;
    var LON0 = o.lon0 === undefined ? -149.0931 : o.lon0;
    var KX = Math.cos(LAT0 * D2R) * 111.32, KZ = 110.57;

    function colOf(lon) { return (((lon + 180) / 360 * n - meta.tile_x0) * 256 - cL) / f; }
    function rowOf(lat) {
      var r = lat * D2R;
      return (((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2 * n - meta.tile_y0) * 256 - cT) / f;
    }
    function heightAt(lon, lat) {
      var c = colOf(lon), r = rowOf(lat);
      if (!(c >= 0 && r >= 0 && c < C - 1 && r < R - 1)) return null;
      var c0 = c | 0, r0 = r | 0, fc = c - c0, fr = r - r0;
      var a = H[r0 * C + c0], b = H[r0 * C + c0 + 1], d = H[(r0 + 1) * C + c0], e = H[(r0 + 1) * C + c0 + 1];
      return (a * (1 - fc) + b * fc) * (1 - fr) + (d * (1 - fc) + e * fc) * fr;
    }
    function lonlatOf(x, z) { return [LON0 + x / KX, LAT0 - z / KZ]; }
    function worldOf(lon, lat) { return [(lon - LON0) * KX, (LAT0 - lat) * KZ]; }
    function hWorld(x, z) { var ll = lonlatOf(x, z); return heightAt(ll[0], ll[1]); }

    // A box-blurred copy of the DEM, built on first use. Lighting only: the
    // shade is taken from h + k * (h - blur(h)), so the real terraces, slough
    // banks and oxbow rims of the Tanana Flats, a few metres high, print as
    // lit and lee modulation while the geometry keeps its stated x3.
    var HB = null;
    function blurDEM(rad) {
      var A = new Float32Array(C * R), B = new Float32Array(C * R), x, y, s, k;
      for (y = 0; y < R; y++) for (x = 0; x < C; x++) {
        s = 0; k = 0;
        for (var i = -rad; i <= rad; i++) { var xx = x + i; if (xx >= 0 && xx < C) { s += H[y * C + xx]; k++; } }
        A[y * C + x] = s / k;
      }
      for (y = 0; y < R; y++) for (x = 0; x < C; x++) {
        s = 0; k = 0;
        for (var j = -rad; j <= rad; j++) { var yy = y + j; if (yy >= 0 && yy < R) { s += A[yy * C + x]; k++; } }
        B[y * C + x] = s / k;
      }
      return B;
    }
    function blurAt(lon, lat) {
      var c = colOf(lon), r = rowOf(lat);
      if (!(c >= 0 && r >= 0 && c < C - 1 && r < R - 1)) return null;
      var c0 = c | 0, r0 = r | 0, fc = c - c0, fr = r - r0;
      var a = HB[r0 * C + c0], b = HB[r0 * C + c0 + 1], d = HB[(r0 + 1) * C + c0], e = HB[(r0 + 1) * C + c0 + 1];
      return (a * (1 - fc) + b * fc) * (1 - fr) + (d * (1 - fc) + e * fc) * fr;
    }
    function hLight(x, z, k) {
      var ll = lonlatOf(x, z), h = heightAt(ll[0], ll[1]);
      if (h === null || !k) return h;
      var b = blurAt(ll[0], ll[1]);
      return b === null ? h : h + k * (h - b);
    }

    var V = { meta: meta, rivers: rivers, transport: transport, heightAt: heightAt,
      lonlatOf: lonlatOf, worldOf: worldOf, KX: KX, KZ: KZ, LON0: LON0, LAT0: LAT0 };

    /* camera: position by lon/lat and either agl (metres above the DEM there)
     * or alt (metres above sea level). VE applies to the camera too, so the
     * camera sits in the same exaggerated world it looks at. */
    V.camera = function (c) {
      var VE = c.VE || 3;
      var g = heightAt(c.lon, c.lat) || 100;
      var altM = c.alt !== undefined ? c.alt : g + (c.agl || 1000);
      var w = worldOf(c.lon, c.lat);
      var th = c.heading * D2R, ph = (c.pitch || 0) * D2R;
      var cam = {
        pos: [w[0], altM / 1000 * VE, w[1]], VE: VE, heading: c.heading, pitch: c.pitch || 0,
        fwdH: [Math.sin(th), -Math.cos(th)], rightH: [Math.cos(th), Math.sin(th)],
        F: [Math.sin(th) * Math.cos(ph), Math.sin(ph), -Math.cos(th) * Math.cos(ph)],
        U: [-Math.sin(th) * Math.sin(ph), Math.cos(ph), Math.cos(th) * Math.sin(ph)],
        R: [Math.cos(th), 0, Math.sin(th)],
        W: c.W || 1080, H: c.H || 1350, fov: c.fov || 55
      };
      cam.f = (cam.H / 2) / Math.tan(cam.fov / 2 * D2R);
      cam.cx = c.cx === undefined ? cam.W / 2 : c.cx;
      cam.cy = c.cy === undefined ? cam.H / 2 : c.cy;
      cam.altM = altM; cam.groundM = g;
      return cam;
    };

    function projW(cam, x, y, z) {
      var dx = x - cam.pos[0], dy = y - cam.pos[1], dz = z - cam.pos[2];
      var zf = dx * cam.F[0] + dy * cam.F[1] + dz * cam.F[2];
      if (zf < 0.05) return null;
      var xr = dx * cam.R[0] + dz * cam.R[2];
      var yu = dx * cam.U[0] + dy * cam.U[1] + dz * cam.U[2];
      return [cam.cx + cam.f * xr / zf, cam.cy - cam.f * yu / zf, zf];
    }
    V.projectWorld = projW;
    /* project a lon/lat on the ground, lifted by liftM metres (true metres). */
    V.project = function (cam, lon, lat, liftM) {
      var h = heightAt(lon, lat); if (h === null) h = 100;
      var w = worldOf(lon, lat);
      return projW(cam, w[0], (h + (liftM || 0)) / 1000 * cam.VE, w[1]);
    };
    /* forward horizontal distance of a lon/lat from the camera, in km */
    V.depthOf = function (cam, lon, lat) {
      var w = worldOf(lon, lat);
      return (w[0] - cam.pos[0]) * cam.fwdH[0] + (w[1] - cam.pos[2]) * cam.fwdH[1];
    };

    /* drape: turn [[lon,lat],...] polylines into depth-tagged screen segments,
     * densified every stepKm so each short piece can be occluded on its own. */
    V.drape = function (cam, lines, st) {
      var segs = [], step = st.stepKm || 0.2, lift = st.liftM || 6;
      for (var li = 0; li < lines.length; li++) {
        var L = lines[li];
        for (var i = 0; i < L.length - 1; i++) {
          var a = worldOf(L[i][0], L[i][1]), b = worldOf(L[i + 1][0], L[i + 1][1]);
          var len = Math.hypot(b[0] - a[0], b[1] - a[1]);
          var dm = Math.max(0.5, ((a[0] + b[0]) / 2 - cam.pos[0]) * cam.fwdH[0] + ((a[1] + b[1]) / 2 - cam.pos[2]) * cam.fwdH[1]);
          var k = Math.max(1, Math.ceil(len / Math.min(step, dm * 0.012)));
          for (var j = 0; j < k; j++) {
            var t0 = j / k, t1 = (j + 1) / k;
            var x0 = a[0] + (b[0] - a[0]) * t0, z0 = a[1] + (b[1] - a[1]) * t0;
            var x1 = a[0] + (b[0] - a[0]) * t1, z1 = a[1] + (b[1] - a[1]) * t1;
            var h0 = hWorld(x0, z0), h1 = hWorld(x1, z1);
            if (h0 === null || h1 === null) continue;
            var p0 = projW(cam, x0, (h0 + lift) / 1000 * cam.VE, z0);
            var p1 = projW(cam, x1, (h1 + lift) / 1000 * cam.VE, z1);
            if (!p0 || !p1) continue;
            // Tag each piece with its NEARER end, so it is drawn after every
            // profile it lies beyond and no nearer-but-lower profile fill can
            // chip it into dashes (measured on the 2026-09-24 prototype).
            var dA = (x0 - cam.pos[0]) * cam.fwdH[0] + (z0 - cam.pos[2]) * cam.fwdH[1];
            var dB = (x1 - cam.pos[0]) * cam.fwdH[0] + (z1 - cam.pos[2]) * cam.fwdH[1];
            var d = Math.min(dA, dB) - (st.bias === undefined ? 0.02 : st.bias);
            segs.push({ a: p0, b: p1, d: d, style: st, idx: li });
          }
        }
      }
      return segs;
    };

    /* terrain: the ridgeline stack. Options (all have defaults):
     *   dmin, dmax (km), profiles (count), lateral samples per profile,
     *   ground/lit/lee/fog hex, fogDensity, light {az, el}, widthNear/widthFar,
     *   litAlpha, drapes: array of V.drape() outputs, skipNear (profiles to
     *   leave for a foreground pass). Returns stats. */
    V.terrain = function (cx, cam, o) {
      o = o || {};
      var dmin = o.dmin || 2, dmax = o.dmax || 60, NP = o.profiles || 240, NS = o.samples || 420;
      var ground = hexRGB(o.ground || "#0A1712"), lit = hexRGB(o.lit || "#9FBF8F");
      var lee = hexRGB(o.lee || "#1D3325"), fog = hexRGB(o.fog || "#1C2B2C");
      var fogK = o.fogDensity === undefined ? 1 / 38 : o.fogDensity;
      var az = (o.light ? o.light.az : 315) * D2R, el = (o.light ? o.light.el : 30) * D2R;
      var Lx = Math.sin(az) * Math.cos(el), Ly = Math.sin(el), Lz = -Math.cos(az) * Math.cos(el);
      var wN = o.widthNear || 1.9, wF = o.widthFar || 0.45;
      var VE = cam.VE, hf = Math.tan((cam.fov * cam.W / cam.H) / 2 * D2R) * 1.25;
      var drapes = [];
      // Fog is quantised to eighths. A continuous mix mints a new ink per
      // profile, which blows the engine's 160-ink paint census and leaves every
      // ink law on the frame unproven (qa.py, 2026-09-24). Eighths are below
      // what the eye resolves in a 0.4 to 2.5 px line.
      var Q = function (v) { return Math.round(v * 8) / 8; };
      (o.drapes || []).forEach(function (s) { drapes = drapes.concat(s); });
      drapes.sort(function (p, q) { return q.d - p.d; });
      var di = 0, drawn = 0, strokes = 0;
      var relK = o.relief || 0;
      if (relK && !HB) HB = blurDEM(o.reliefRadius || 5);
      // HAZE (o.haze): the DEM is a crop, and a profile that runs off its edge
      // ends in a vertical step that reads as a mesa. With haze on, dmax is
      // held inside the crop for the whole visible width, the last quarter of
      // the range fades wholly into the fog ink, and a fog floor with a
      // feathered top is laid behind the stack, so the eye meets air.
      var dEnd = dmax;
      if (o.haze) {
        dEnd = Math.min(dmax, V.cropDepth(cam, dmin));
        var yh = null, fh0 = hWorld(cam.pos[0] + cam.fwdH[0] * dEnd, cam.pos[2] + cam.fwdH[1] * dEnd);
        var ph0 = projW(cam, cam.pos[0] + cam.fwdH[0] * dEnd, (fh0 === null ? cam.groundM : fh0) / 1000 * VE, cam.pos[2] + cam.fwdH[1] * dEnd);
        if (ph0) yh = ph0[1];
        if (yh !== null) {
          var fe = o.haze.feather || 70, gr = cx.createLinearGradient(0, yh - fe, 0, yh + 6);
          gr.addColorStop(0, css(fog, 0)); gr.addColorStop(1, css(fog, o.haze.alpha || 1));
          cx.fillStyle = gr; cx.fillRect(0, yh - fe, cam.W, fe + 6);
          cx.fillStyle = css(fog, o.haze.alpha || 1); cx.fillRect(0, yh + 6, cam.W, cam.H + 40 - yh);
        }
        V.lastHaze = {dEnd: dEnd, y: yh};
      }
      function fogT(d) {
        var t = 1 - Math.exp(-Math.pow(d * fogK, 2));
        if (o.haze) { var ff = o.haze.fadeFrom || 0.72, a = Math.max(0, Math.min(1, (d - ff * dEnd) / ((1 - ff) * dEnd))); t = Math.max(t, a * a * (3 - 2 * a)); }
        return Q(t);
      }
      var fillMix = o.haze ? 1 : 0.9;
      // SPACING (o.spacing = p): profiles are spaced uniformly in d^-p. p = 1
      // spaces them evenly in 1/d, which over flat ground is evenly on SCREEN,
      // a venetian blind. p toward 0 (log spacing) opens the gaps toward the
      // camera, which is the depth cue. o.minGap drops a profile whose
      // flat-ground screen row falls within minGap px of the last one kept,
      // so the far field never packs into a moire band.
      var p = o.spacing === undefined ? 1 : o.spacing;
      var cand = [];
      for (var i = 0; i < NP; i++) {
        var fr = i / (NP - 1);
        cand.push(p === 0 ? dEnd * Math.pow(dmin / dEnd, fr)
          : Math.pow(Math.pow(dEnd, -p) + (Math.pow(dmin, -p) - Math.pow(dEnd, -p)) * fr, -1 / p));
      }
      var depths = [], lastY = -1e9;
      for (var ci = 0; ci < cand.length; ci++) {
        if (o.minGap) {
          var dd = cand[ci], gp = projW(cam, cam.pos[0] + cam.fwdH[0] * dd, cam.groundM / 1000 * VE, cam.pos[2] + cam.fwdH[1] * dd);
          if (gp && gp[1] - lastY < o.minGap && ci !== cand.length - 1) continue;
          if (gp) lastY = gp[1];
        }
        depths.push(cand[ci]);
      }
      var bottom = o.bottom === undefined ? cam.H + 40 : o.bottom;
      function flushTo(d) {
        while (di < drapes.length && drapes[di].d > d) {
          var s = drapes[di++], st = s.style;
          var t = fogT(s.d);
          var col = mix(hexRGB(st.color), fog, t * (st.fogMix === undefined ? 0.85 : st.fogMix));
          cx.strokeStyle = css(col, st.alpha === undefined ? 1 : st.alpha);
          cx.lineWidth = Math.max(0.35, (st.width || 1.5) * Math.min(1.6, Math.max(0.35, (st.depthRef || 12) / s.d)));
          cx.lineCap = "round";
          if (st.dash) { cx.setLineDash(st.dash); } else { cx.setLineDash([]); }
          cx.beginPath(); cx.moveTo(s.a[0], s.a[1]); cx.lineTo(s.b[0], s.b[1]); cx.stroke();
          strokes++;
        }
        cx.setLineDash([]);
      }
      var profilesOut = [];
      for (var pi = 0; pi < depths.length; pi++) {
        var d = depths[pi];
        if (o.skipNear && pi >= depths.length - o.skipNear) break;
        flushTo(d);
        // lateral reach from CAMERA-SPACE depth, not horizontal distance: a
        // high camera pitched down sees the near ground at a depth well past
        // d, and sizing by d left bare wedges at the frame's lower corners
        // (slide 04, round 3)
        var zc = d * Math.cos(cam.pitch * D2R) - (cam.pos[1] - cam.groundM / 1000 * VE) * Math.sin(cam.pitch * D2R);
        var half = Math.max(d, zc) * hf, pts = [];
        var cxw = cam.pos[0] + cam.fwdH[0] * d, czw = cam.pos[2] + cam.fwdH[1] * d;
        for (var si = 0; si <= NS; si++) {
          var s = -half + 2 * half * si / NS;
          var x = cxw + cam.rightH[0] * s, z = czw + cam.rightH[1] * s;
          var h = hWorld(x, z);
          if (h === null) { pts.push(null); continue; }
          var e = 0.2, hc = relK ? hLight(x, z, relK) : h;
          var hx = (hLight(x + e, z, relK) || hc) - (hLight(x - e, z, relK) || hc);
          var hz = (hLight(x, z + e, relK) || hc) - (hLight(x, z - e, relK) || hc);
          var gx = hx / 1000 * VE / (2 * e), gz = hz / 1000 * VE / (2 * e);
          var nl = Math.hypot(gx, 1, gz);
          var ndl = (-gx * Lx + Ly - gz * Lz) / nl;
          var p = projW(cam, x, h / 1000 * VE, z);
          if (!p) { pts.push(null); continue; }
          p.push(ndl, Math.hypot(gx, gz));
          pts.push(p);
        }
        var t = fogT(d);
        var gcol = mix(ground, fog, t * fillMix);
        // occluding fill
        var run = [];
        var flushRun = function () {
          if (run.length < 2) { run = []; return; }
          cx.beginPath(); cx.moveTo(run[0][0], bottom);
          for (var k = 0; k < run.length; k++) cx.lineTo(run[k][0], run[k][1]);
          cx.lineTo(run[run.length - 1][0], bottom); cx.closePath();
          cx.fillStyle = css(gcol); cx.fill();
          profilesOut.push(run);
          run = [];
        };
        var runs = [];
        for (var k2 = 0; k2 < pts.length; k2++) {
          if (pts[k2]) run.push(pts[k2]); else { if (run.length) runs.push(run.slice()); flushRun(); }
        }
        if (run.length) runs.push(run.slice());
        flushRun();
        // lit / lee strokes, bucketed so a profile costs a handful of paths
        // width: linear in d by default; o.widthPow scales it by nearness in
        // 1/d instead, so the near field carries the weight
        var wd = o.widthPow ? wF + (wN - wF) * Math.pow(Math.max(0, (1 / d - 1 / dEnd) / (1 / dmin - 1 / dEnd)), o.widthPow)
          : wN + (wF - wN) * Math.min(1, (d - dmin) / (dEnd - dmin));
        var BK = 9;
        for (var r = 0; r < runs.length; r++) {
          var R0 = runs[r];
          for (var bk = 0; bk < BK; bk++) {
            cx.beginPath(); var any = false;
            for (var q = 0; q < R0.length - 1; q++) {
              var lv = (R0[q][3] + R0[q + 1][3]) / 2;
              // o.contrast: spread the shade about flat ground's own value,
              // so micro-relief on the flats reaches both ends of the ramp
              if (o.contrast) lv = Ly + (lv - Ly) * o.contrast;
              var b = Math.max(0, Math.min(BK - 1, Math.floor((lv + 0.15) / 1.15 * BK)));
              if (b !== bk) continue;
              cx.moveTo(R0[q][0], R0[q][1]); cx.lineTo(R0[q + 1][0], R0[q + 1][1]); any = true;
            }
            if (!any) continue;
            var tt = bk / (BK - 1);
            var col = mix(mix(lee, lit, Math.pow(tt, 1.3)), fog, t * 0.92);
            // o.quietFlat {band, alpha}: the shade buckets nearest flat
            // ground's own value are drawn faint, so a floodplain stops
            // reading as ruled paper and only its real relief prints
            var qf = 1;
            if (o.quietFlat) {
              var lvc = (bk + 0.5) / BK * 1.15 - 0.15;
              if (Math.abs(lvc - Ly) < (o.quietFlat.band || 0.08)) qf = o.quietFlat.alpha === undefined ? 0.3 : o.quietFlat.alpha;
            }
            cx.strokeStyle = css(col, (o.litAlpha === undefined ? 1 : o.litAlpha) * qf);
            cx.lineWidth = Math.max(0.3, wd * (0.45 + 0.75 * tt));
            cx.lineJoin = "round"; cx.lineCap = "round";
            cx.stroke(); strokes++;
          }
        }
        // FLAT GROUND GETS MARKS (o.flats). A profile over the Tanana Flats is a
        // straight line and a field of straight lines reads as stripes, not
        // ground. Where the slope is gentle, short upright ticks stand on the
        // profile, their height and spacing falling with distance, placed by
        // a deterministic hash of profile and sample so a re-render is
        // identical. Ticks go up from the line, in the profile's own lit ink.
        if (o.flats) {
          var F = o.flats, every = F.every || 2, smax = F.maxSlope || 0.06;
          var hNear = F.height || 5, near = F.nearKm || 4;
          var th = Math.max(0.6, hNear * Math.min(1, near / d));
          if (th > (F.minHeight || 0.9)) {
            cx.beginPath();
            for (var rr = 0; rr < runs.length; rr++) {
              var RR = runs[rr];
              for (var qq = 0; qq < RR.length; qq += every) {
                var P0 = RR[qq]; if (P0[4] > smax) continue;
                var hsh = Math.sin((pi + 1) * 12.9898 + (qq + 1) * 78.233) * 43758.5453;
                hsh = hsh - Math.floor(hsh);
                if (hsh > (F.density || 0.55)) continue;
                var h2 = Math.sin((pi + 7) * 39.3468 + (qq + 3) * 11.135) * 24634.6345;
                h2 = h2 - Math.floor(h2);
                var P1 = RR[Math.min(RR.length - 1, qq + 1)];
                var bx = P0[0] + (P1[0] - P0[0]) * h2, by = P0[1] + (P1[1] - P0[1]) * h2;
                var tl = th * (0.35 + 1.3 * h2 * h2);
                cx.moveTo(bx, by); cx.lineTo(bx + (hsh - 0.5) * 0.9, by - tl);
              }
            }
            var fc = mix(mix(lee, lit, F.tone === undefined ? 0.55 : F.tone), fog, t * 0.92);
            cx.strokeStyle = css(fc, F.alpha === undefined ? 0.8 : F.alpha);
            cx.lineWidth = Math.max(0.4, wd * 0.55); cx.lineCap = "round";
            cx.stroke(); strokes++;
          }
        }
        drawn++;
        if (o.onProfile) o.onProfile(pi, d, runs);
      }
      flushTo(-1e9);
      return { profiles: drawn, strokes: strokes, depths: depths, dEnd: dEnd };
    };

    /* cropDepth: the farthest forward distance at which the whole visible
     * width of a profile still lies on the DEM. Past it a profile is cut off
     * mid-frame by the crop, which is the mesa the haze option exists to hide. */
    V.cropDepth = function (cam, dFrom) {
      var hw = (cam.W / 2) / cam.f * 1.08, last = dFrom || 1;
      for (var d = dFrom || 1; d < 200; d += 0.5) {
        var ok = true, cxw = cam.pos[0] + cam.fwdH[0] * d, czw = cam.pos[2] + cam.fwdH[1] * d;
        for (var k = 0; k <= 40 && ok; k++) {
          var s = -d * hw + 2 * d * hw * k / 40;
          if (hWorld(cxw + cam.rightH[0] * s, czw + cam.rightH[1] * s) === null) ok = false;
        }
        if (!ok) break;
        last = d;
      }
      return last;
    };

    V.quiet = quietCanvas;

    /* aim: a camera solved from what the frame must show rather than guessed.
     * Stand `distKm` back from a target lon/lat along `heading`, `agl` metres
     * above the ground there, then search pitch so the target lands on screen
     * row `yTarget` while the ground `farKm` ahead of the camera lands on row
     * `yFar`. Returns the camera, with the solved pitch and cy on it. */
    V.aim = function (o) {
      var th = o.heading * D2R, t = worldOf(o.target[0], o.target[1]);
      var ll = lonlatOf(t[0] - Math.sin(th) * o.distKm, t[1] + Math.cos(th) * o.distKm);
      var best = null;
      for (var pt = -70; pt <= -2; pt += 0.25) {
        var cam = V.camera({lon: ll[0], lat: ll[1], agl: o.agl, heading: o.heading, pitch: pt,
                            fov: o.fov, W: o.W, H: o.H, cy: 0, cx: o.cx, VE: o.VE});
        var pT = V.project(cam, o.target[0], o.target[1], 0);
        var fx = cam.pos[0] + cam.fwdH[0] * o.farKm, fz = cam.pos[2] + cam.fwdH[1] * o.farKm;
        var fh = hWorld(fx, fz); if (fh === null) fh = 120;
        var pF = projW(cam, fx, fh / 1000 * cam.VE, fz);
        if (!pT || !pF) continue;
        var cy = o.yTarget - pT[1];
        var err = Math.abs((pF[1] + cy) - o.yFar);
        if (!best || err < best.err) best = {err: err, pitch: pt, cy: cy};
      }
      var out = V.camera({lon: ll[0], lat: ll[1], agl: o.agl, heading: o.heading, pitch: best.pitch,
                          fov: o.fov, W: o.W, H: o.H, cy: best.cy, cx: o.cx, VE: o.VE});
      out.solveErr = best.err; out.lon = ll[0]; out.lat = ll[1];
      return out;
    };

    /* visible: is a world point seen from the camera, or does terrain block
     * the line of sight? Marches the ray in 48 steps against the DEM. */
    V.visible = function (cam, x, y, z) {
      for (var i = 1; i < 48; i++) {
        var t = i / 48;
        var px = cam.pos[0] + (x - cam.pos[0]) * t, py = cam.pos[1] + (y - cam.pos[1]) * t;
        var pz = cam.pos[2] + (z - cam.pos[2]) * t;
        var h = hWorld(px, pz);
        if (h !== null && h / 1000 * cam.VE > py + 0.002) return false;
      }
      return true;
    };
    /* overlay: draw lon/lat polylines ON TOP of the finished terrain, keeping
     * only the pieces with a clear line of sight. For bold marks (a survey
     * square) that must not be chipped into dashes by the profile strokes that
     * cross them, which is what depth-bucketing does to a line lying on the
     * ground. Returns the drawn screen points. */
    V.overlay = function (cx, cam, lines, st) {
      var step = st.stepKm || 0.15, lift = st.liftM || 8, out = [];
      var layers = st.casing ? [[st.casing, st.casingWidth || (st.width || 2) + 3.5], [st.color, st.width || 2]] : [[st.color, st.width || 2]];
      var pieces = [];
      lines.forEach(function (L) {
        for (var i = 0; i < L.length - 1; i++) {
          var a = worldOf(L[i][0], L[i][1]), b = worldOf(L[i + 1][0], L[i + 1][1]);
          var k = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / step));
          for (var j = 0; j < k; j++) {
            var x0 = a[0] + (b[0] - a[0]) * j / k, z0 = a[1] + (b[1] - a[1]) * j / k;
            var x1 = a[0] + (b[0] - a[0]) * (j + 1) / k, z1 = a[1] + (b[1] - a[1]) * (j + 1) / k;
            var h0 = hWorld(x0, z0), h1 = hWorld(x1, z1);
            if (h0 === null || h1 === null) continue;
            var y0 = (h0 + lift) / 1000 * cam.VE, y1 = (h1 + lift) / 1000 * cam.VE;
            var p0 = projW(cam, x0, y0, z0), p1 = projW(cam, x1, y1, z1);
            if (!p0 || !p1) continue;
            var vis = V.visible(cam, x0, y0, z0) && V.visible(cam, x1, y1, z1);
            pieces.push([p0, p1, vis]);
          }
        }
      });
      // runs of consecutive pieces with the same visibility. A visible run
      // shorter than st.minRun screen px is an orphan tick between two
      // occlusions and reads as a stray mark (pixel critic, slide 02), so it
      // is demoted to hidden.
      var runs = [], cur = null;
      pieces.forEach(function (pc) {
        var joined = cur && Math.abs(cur.last[0] - pc[0][0]) < 0.01 && Math.abs(cur.last[1] - pc[0][1]) < 0.01;
        if (!cur || !joined || cur.vis !== pc[2]) { cur = {vis: pc[2], pts: [pc[0]], len: 0, last: pc[0]}; runs.push(cur); }
        cur.pts.push(pc[1]); cur.last = pc[1];
        // only the on-screen part of a run counts toward minRun
        var onS = function (q) { return q[0] >= 0 && q[0] <= cam.W && q[1] >= 0 && q[1] <= cam.H; };
        if (onS(pc[0]) && onS(pc[1])) cur.len += Math.hypot(pc[1][0] - pc[0][0], pc[1][1] - pc[0][1]);
      });
      runs.forEach(function (r) { if (r.vis && st.minRun && r.len < st.minRun) r.vis = false; });
      function strokeRuns(want, layersIn, dash) {
        layersIn.forEach(function (ly) {
          cx.strokeStyle = ly[0]; cx.lineWidth = ly[1]; cx.lineCap = "round"; cx.lineJoin = "round";
          cx.setLineDash(dash || []);
          // one subpath per run, so a dash pattern runs along the whole line
          // instead of restarting on every short piece
          cx.beginPath();
          runs.forEach(function (r) {
            if (r.vis !== want) return;
            r.pts.forEach(function (q, i) { if (i) cx.lineTo(q[0], q[1]); else cx.moveTo(q[0], q[1]); });
          });
          cx.stroke(); cx.setLineDash([]);
        });
      }
      // st.hidden: draw the occluded runs too, faint and dashed, so a shape
      // the ridge hides still closes (the survey convention for a hidden edge)
      if (st.hidden) strokeRuns(false, [[st.hidden.color, st.hidden.width || 1.2]], st.hidden.dash || [4, 5]);
      strokeRuns(true, layers, st.dash);
      runs.forEach(function (r) { if (r.vis) r.pts.forEach(function (q) { out.push(q); }); });
      return out;
    }

    V.riverLines = function (rank) {
      var out = [];
      rivers.features.forEach(function (ft) {
        if (rank && ft.properties.rank !== rank) return;
        out.push(ft.geometry.coordinates);
      });
      return out;
    };
    V.transportOf = function (kind) {
      return transport.features.filter(function (ft) { return ft.properties.kind === kind; });
    };
    /* a square of side km, centred on lon/lat, axis-aligned to north, as a
     * closed lon/lat ring (for draping). */
    V.squareRing = function (lon, lat, sideKm) {
      var c = worldOf(lon, lat), s = sideKm / 2;
      var P = [[c[0] - s, c[1] - s], [c[0] + s, c[1] - s], [c[0] + s, c[1] + s], [c[0] - s, c[1] + s], [c[0] - s, c[1] - s]];
      return P.map(function (p) { return lonlatOf(p[0], p[1]); });
    };
    return V;
  }

  global.AKV = { load: load, quietCanvas: quietCanvas };
})(typeof window !== "undefined" ? window : this);
