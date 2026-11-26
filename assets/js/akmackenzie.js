/* akmackenzie.js — the Port MacKenzie line, Carousel No.124's deck furniture (2026-11-25).
 *
 * Classic script, global AKMAC. bespoke_check strips `<script src=>` as
 * harness, so the shared geometry and fixtures here cost the variety budget
 * nothing while every frame's own drawing stays its own code.
 *
 * WHAT IT OWNS (and nothing about composition)
 *   AKMAC.load(A)          the corridor DEM (assets/geo/ak-portmac-dem, AWS
 *                          terrain tiles z12), a lightly smoothed copy for
 *                          shading (terrain tiles store whole metres, so the
 *                          raw gradient prints 1 m steps on the flats), the
 *                          stitched track (assets/geo/ak-portmac-track.json,
 *                          OpenStreetMap, ODbL) and the Houston conveyance
 *                          outline (assets/geo/ak-houston-ffd-6800.geo.json).
 *   AKMAC.view(o)          a north-up local equal-scale view: lon scaled by the
 *                          cosine of lat0, kmPx design px per km, (x0, y0) the
 *                          pixel of (lon0, lat0). xy(lon,lat), ll(x,y), kmPx.
 *   AKMAC.along(T, km)     the chain point at an along-track distance from the
 *                          junction near Houston (0) toward the port.
 *   AKMAC.chainPath(cx, T, V, a, b)  adds the chain between km a and b as a
 *                          subpath (no beginPath, house rule).
 *   AKMAC.fixtures(n, o)   counter, wordmark, site fixture, corridor locator,
 *                          optional OSM credit, as DOM.
 *   AKMAC.ring(svg, x, y, r)  the hollow forget-me-not end ring (proposed,
 *                          unnamed), dashed.
 *
 * THE INK LAW. Gold #FFC72C is the funded line and nothing else (the 09
 * Polaris is the brand fixture). Forget-me-not #6EA5FF, dashed, is proposed
 * and unnamed. Both are drawn after any grade.
 */
(function (global) {
  "use strict";
  var M = global.AKMAC || (global.AKMAC = {});
  M.GOLD = "#FFC72C";
  M.BLUE = "#6EA5FF";
  M.KM_PER_DEG_LAT = 110.574;
  M.TOTAL_KM = null;

  M.load = async function (A, o) {
    o = o || {};
    var dem = await AKS.loadDEM(A + "/geo/ak-portmac-dem");
    var shade = AKS.smoothDEM(dem, o.smoothR == null ? 1 : o.smoothR, o.smoothPasses == null ? 2 : o.smoothPasses);
    var T = await (await fetch(A + "/geo/ak-portmac-track.json")).json();
    M.TOTAL_KM = T.chain_km[T.chain_km.length - 1];
    var ffd = o.ffd === false ? null : await (await fetch(A + "/geo/ak-houston-ffd-6800.geo.json")).json();
    return { dem: dem, shade: shade, track: T, ffd: ffd };
  };

  M.view = function (o) {
    var c = Math.cos(o.lat0 * Math.PI / 180);
    var kx = M.KM_PER_DEG_LAT * c * o.kmPx, ky = M.KM_PER_DEG_LAT * o.kmPx;
    return {
      kmPx: o.kmPx,
      xy: function (lon, lat) { return [o.x0 + (lon - o.lon0) * kx, o.y0 - (lat - o.lat0) * ky]; },
      ll: function (x, y) { return [o.lon0 + (x - o.x0) / kx, o.lat0 - (y - o.y0) / ky]; }
    };
  };

  M.along = function (T, km) {
    var C = T.chain, K = T.chain_km;
    if (km <= 0) return C[0].slice();
    if (km >= K[K.length - 1]) return C[C.length - 1].slice();
    var lo = 0, hi = K.length - 1;
    while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (K[mid] < km) lo = mid; else hi = mid; }
    var t = (km - K[lo]) / (K[hi] - K[lo] || 1);
    return [C[lo][0] + (C[hi][0] - C[lo][0]) * t, C[lo][1] + (C[hi][1] - C[lo][1]) * t];
  };

  M.chainPoints = function (T, a, b) {
    a = a == null ? 0 : a; b = b == null ? T.chain_km[T.chain_km.length - 1] : b;
    var pts = [M.along(T, a)];
    for (var i = 0; i < T.chain.length; i++) if (T.chain_km[i] > a && T.chain_km[i] < b) pts.push(T.chain[i]);
    pts.push(M.along(T, b));
    return pts;
  };

  M.chainPath = function (cx, T, V, a, b) {
    var pts = M.chainPoints(T, a, b);
    for (var i = 0; i < pts.length; i++) {
      var p = V.xy(pts[i][0], pts[i][1]);
      if (i === 0) cx.moveTo(p[0], p[1]); else cx.lineTo(p[0], p[1]);
    }
  };

  M.loopPath = function (cx, T, V) {
    for (var i = 0; i < T.loop.length; i++) {
      var p = V.xy(T.loop[i][0], T.loop[i][1]);
      if (i === 0) cx.moveTo(p[0], p[1]); else cx.lineTo(p[0], p[1]);
    }
  };

  /* fixtures ---------------------------------------------------------- */
  var CSS = "" +
    ".akm-counter{position:absolute;right:80px;top:80px;font:500 22px/1 'JetBrains Mono',monospace;letter-spacing:.08em;color:#A8B6BC;text-align:right;white-space:nowrap}" +
    ".akm-counter b{font-weight:500;color:#F4F8FF;margin-left:18px}" +
    ".akm-site{position:absolute;left:80px;bottom:52px;font:500 20px/1 'JetBrains Mono',monospace;letter-spacing:.06em;color:#56686E}" +
    ".akm-osm{position:absolute;left:80px;bottom:84px;font:400 16px/1 'JetBrains Mono',monospace;letter-spacing:.04em;color:#56686E}" +
    ".akm-loc{position:absolute;right:80px;bottom:44px;width:180px;height:30px}";

  M.fixtures = function (n, o) {
    o = o || {};
    if (!document.getElementById("akm-css")) {
      var st = document.createElement("style"); st.id = "akm-css"; st.textContent = CSS; document.head.appendChild(st);
    }
    var host = o.host || document.body;
    var c = document.createElement("div"); c.className = "akm-counter"; c.setAttribute("data-decorative", "");
    c.innerHTML = "ALASKA.AI<b>" + (n < 10 ? "0" + n : n) + " / 09</b>";
    if (o.counterColor) c.style.color = o.counterColor;
    host.appendChild(c);
    var s = document.createElement("div"); s.className = "akm-site"; s.setAttribute("data-decorative", "");
    s.textContent = "alaskaaihq.com"; if (o.siteColor) s.style.color = o.siteColor; host.appendChild(s);
    if (o.osm) {
      var m = document.createElement("div"); m.className = "akm-osm"; m.setAttribute("data-decorative", "");
      m.textContent = "(c) OpenStreetMap contributors"; if (o.siteColor) m.style.color = o.siteColor; host.appendChild(m);
    }
    /* the corridor locator: the 32 miles as a horizontal schematic, Houston at
     * the left, the port at the right; the frame's own extent lit in gold. */
    var lit = o.lit || [0, 1];
    var NS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "akm-loc"); svg.setAttribute("viewBox", "0 0 180 30"); svg.setAttribute("data-decorative", "");
    function el(t, a) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); svg.appendChild(e); return e; }
    var x0 = 12, x1 = 168, y = 15, dim = o.locDim || "#3B4A52";
    el("line", { x1: x0, y1: y, x2: x1, y2: y, stroke: dim, "stroke-width": 2, "stroke-linecap": "butt" });
    el("line", { x1: x0 + (x1 - x0) * lit[0], y1: y, x2: x0 + (x1 - x0) * lit[1], y2: y, stroke: M.GOLD, "stroke-width": 3, "stroke-linecap": "butt", opacity: o.locAlpha || 1 });
    el("circle", { cx: x0, cy: y, r: 5, fill: "none", stroke: M.BLUE, "stroke-width": 1.6, "stroke-dasharray": "2.4 2" });
    el("circle", { cx: x1, cy: y, r: 5, fill: "none", stroke: M.BLUE, "stroke-width": 1.6, "stroke-dasharray": "2.4 2" });
    host.appendChild(svg);
  };

  M.ring = function (svg, x, y, r, o) {
    o = o || {};
    var NS = "http://www.w3.org/2000/svg";
    var c = document.createElementNS(NS, "circle");
    c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", r);
    c.setAttribute("fill", "none"); c.setAttribute("stroke", M.BLUE);
    c.setAttribute("stroke-width", o.w || 3); c.setAttribute("stroke-dasharray", o.dash || "7 6");
    svg.appendChild(c);
    if (o.halo) {
      var h = document.createElementNS(NS, "circle");
      h.setAttribute("cx", x); h.setAttribute("cy", y); h.setAttribute("r", r);
      h.setAttribute("fill", "none"); h.setAttribute("stroke", o.halo);
      h.setAttribute("stroke-width", (o.w || 3) + 5); h.setAttribute("opacity", 0.55);
      svg.insertBefore(h, c);
    }
    return c;
  };

  /* Lambert shade of a DEM at (lon, lat) under the deck sun (screen az 200,
   * el 24 unless o says otherwise), from the smoothed cubic sampler. ex is the
   * vertical exaggeration; dkm the sampling step in km. Returns 0..1. */
  M.sun = function (o) {
    o = o || {};
    var az = (o.az == null ? 200 : o.az) * Math.PI / 180, el = (o.el == null ? 24 : o.el) * Math.PI / 180;
    return [Math.cos(el) * Math.sin(az), -Math.cos(el) * Math.cos(az), Math.sin(el)];
  };
  M.normal = function (dem, lon, lat, dkm, ex) {
    var c = Math.cos(lat * Math.PI / 180);
    var dlon = dkm / (M.KM_PER_DEG_LAT * c), dlat = dkm / M.KM_PER_DEG_LAT;
    var s = dem.sampleCubic;
    var hx = (s(lon + dlon, lat) - s(lon - dlon, lat)) / (2000 * dkm) * ex;
    var hy = (s(lon, lat + dlat) - s(lon, lat - dlat)) / (2000 * dkm) * ex;
    /* screen y points south, so the screen-space normal's y is +hy */
    var nx = -hx, ny = hy, nz = 1, l = Math.hypot(nx, ny, nz);
    return [nx / l, ny / l, nz / l];
  };
})(this);
