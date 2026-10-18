/* aklattice.js — deck furniture for No.89, THE ANALYSIS LATTICE (2026-10-17).
 *
 * WHAT IT OWNS. The fixtures every frame carries (wordmark, counter, site line,
 * coordinates footer, the camera's ALT readout), the deck palette, and the one
 * recurring motif, THE DELTA CELL: a wireframe lattice cell drawn in 2D from
 * eight already-projected corners, so a 3D scene, a plan map and a legend can
 * each place it in their own space. It owns no composition. Each slide draws
 * its own world and decides where the cell stands.
 *
 * USAGE
 *   AKLAT.fixtures({ n: 5, total: 9, alt: "ALT 20 M" });
 *   AKLAT.cell(cx, corners8, { state: "hollow" | "solid" | "phantom", gold: [x, y] });
 *   AKLAT.dimension(cx, [x, y0], [x, y1], { tick: 6 });
 *
 * Fixtures sit at z-index 9 above every art canvas (No.88: fixtures appended
 * after a z-index 1 canvas with no z-index of their own painted under it).
 */
(function (global) {
  "use strict";
  var L = {};
  L.P = {
    night: "#050B12", elev1: "#0A1620", elev2: "#122434",
    stratus0: "#1E2C36", stratus1: "#33454F", break0: "#B9C7C9", break1: "#E6ECEA",
    waterDeep: "#23353C", waterMid: "#7F9396", sheen: "#C3D0D0",
    silt: "#3A3A30", siltLit: "#6A6648", lee: "#1E211C", sedge: "#6E4B33",
    ice: "#5AC8F0", iceLit: "#9FE0F5", phantom: "#5C6B74",
    gold: "#FFC72C", goldHalo: "#FFDA6E",
    type: "#F4F8FF", type2: "#A9B7BF", fix: "#46545F"
  };

  function el(tag, css, text, deco) {
    var e = document.createElement(tag);
    e.style.cssText = css;
    if (text != null) e.textContent = text;
    if (deco) e.setAttribute("data-decorative", "");
    document.body.appendChild(e);
    return e;
  }

  /* wordmark top left, counter top right, ALT readout under the counter,
   * site line and coordinates along the bottom. All z-index 9. */
  L.fixtures = function (o) {
    o = o || {};
    var ink = o.ink || "#A9B7BF", fix = o.fix || L.P.fix;
    var base = "position:absolute;z-index:9;font-family:'JetBrains Mono';font-weight:500;letter-spacing:0.08em;";
    var out = {};
    out.wordmark = el("div", base + "left:80px;top:62px;font-size:22px;color:" + ink + ";", "ALASKA.AI", true);
    out.counter = el("div", base + "right:80px;top:60px;font-size:24px;color:" + ink + ";",
      String(o.n).padStart(2, "0") + " / " + String(o.total).padStart(2, "0"));
    out.counter.className = "counter";
    if (o.alt) out.alt = el("div", base + "right:80px;top:96px;font-size:18px;font-weight:400;color:" + (o.altInk || "#7F9396") + ";", o.alt, true);
    out.site = el("div", "position:absolute;z-index:9;left:80px;top:1291px;font-family:'JetBrains Mono';font-weight:400;font-size:19px;letter-spacing:0.04em;color:" + fix + ";", "alaskaaihq.com", true);
    out.coords = el("div", "position:absolute;z-index:9;right:80px;top:1291px;font-family:'JetBrains Mono';font-weight:400;font-size:19px;letter-spacing:0.04em;color:" + fix + ";",
      o.coords || "59°56'N 164°03'W", true);
    return out;
  };

  function rgba(hex, a) {
    var v = hex.replace("#", "");
    return "rgba(" + parseInt(v.slice(0, 2), 16) + "," + parseInt(v.slice(2, 4), 16) + "," + parseInt(v.slice(4, 6), 16) + "," + a + ")";
  }
  L.rgba = rgba;

  /* THE DELTA CELL. corners: 8 points [x, y] in design px, ordered
   * bottom face 0..3 then top face 4..7 (4 above 0, etc.). `depth` (optional,
   * 8 numbers, larger is farther) lets the far edges thin and fade. States:
   *   hollow  ice edges, nothing inside
   *   solid   ice edges plus a faint ice fill on the near faces
   *   phantom dashed edges in the phantom ink
   * `gold` [x, y] places a measured point inside it (gold law). */
  L.EDGES = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  L.cell = function (cx, c, o) {
    o = o || {};
    var state = o.state || "hollow", w = o.width || 1.6, a = o.alpha == null ? 0.9 : o.alpha;
    var d = o.depth || [0, 0, 0, 0, 0, 0, 0, 0];
    var dmin = Math.min.apply(null, d), dmax = Math.max.apply(null, d), span = Math.max(1e-6, dmax - dmin);
    cx.save();
    cx.lineCap = "round";
    if (state === "solid") {
      cx.fillStyle = rgba(L.P.ice, 0.10);
      [[4, 5, 6, 7], [0, 1, 5, 4]].forEach(function (f) {
        cx.beginPath(); cx.moveTo(c[f[0]][0], c[f[0]][1]);
        for (var i = 1; i < 4; i++) cx.lineTo(c[f[i]][0], c[f[i]][1]);
        cx.closePath(); cx.fill();
      });
    }
    L.EDGES.forEach(function (e) {
      var t = ((d[e[0]] + d[e[1]]) / 2 - dmin) / span;   // 0 near, 1 far
      cx.lineWidth = w * (1 - 0.55 * t);
      if (state === "phantom") {
        cx.setLineDash([7, 5]);
        cx.strokeStyle = rgba(L.P.phantom, a * (1 - 0.4 * t));
      } else {
        cx.setLineDash([]);
        cx.strokeStyle = rgba(t < 0.5 ? L.P.iceLit : L.P.ice, a * (1 - 0.5 * t));
      }
      cx.beginPath(); cx.moveTo(c[e[0]][0], c[e[0]][1]); cx.lineTo(c[e[1]][0], c[e[1]][1]); cx.stroke();
    });
    cx.setLineDash([]);
    if (o.ring) {   // an empty ring where a measurement would sit
      cx.strokeStyle = rgba(L.P.phantom, 0.9); cx.lineWidth = 1.4; cx.setLineDash([4, 3]);
      cx.beginPath(); cx.arc(o.ring[0], o.ring[1], o.ring[2] || 7, 0, Math.PI * 2); cx.stroke();
      cx.setLineDash([]);
    }
    if (o.gold) {
      var g = cx.createRadialGradient(o.gold[0], o.gold[1], 0, o.gold[0], o.gold[1], 14);
      g.addColorStop(0, rgba(L.P.goldHalo, 0.55)); g.addColorStop(1, rgba(L.P.goldHalo, 0));
      cx.fillStyle = g; cx.beginPath(); cx.arc(o.gold[0], o.gold[1], 14, 0, Math.PI * 2); cx.fill();
      cx.fillStyle = L.P.gold; cx.beginPath(); cx.arc(o.gold[0], o.gold[1], o.goldR || 4.5, 0, Math.PI * 2); cx.fill();
    }
    cx.restore();
  };

  /* An axis-aligned box cell from a projector: proj([x, y, z]) -> [sx, sy, depth]. */
  L.boxCorners = function (proj, x0, y0, z0, sx, sy, sz) {
    var pts = [[x0, y0, z0], [x0 + sx, y0, z0], [x0 + sx, y0, z0 + sz], [x0, y0, z0 + sz],
               [x0, y0 + sy, z0], [x0 + sx, y0 + sy, z0], [x0 + sx, y0 + sy, z0 + sz], [x0, y0 + sy, z0 + sz]];
    var c = [], d = [];
    pts.forEach(function (p) { var q = proj(p); c.push([q[0], q[1]]); d.push(q[2] || 0); });
    return { corners: c, depth: d };
  };

  /* A drafting dimension: extension ticks at both ends, a line between, a
   * cased stroke so it reads over a busy field. */
  L.dimension = function (cx, a, b, o) {
    o = o || {};
    var tick = o.tick || 7, col = o.color || L.P.type, w = o.width || 1.4;
    var dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy), nx = -dy / len, ny = dx / len;
    cx.save(); cx.lineCap = "butt";
    [[L.P.night, w + 2.4, 0.55], [col, w, 1]].forEach(function (s) {
      cx.strokeStyle = s[0]; cx.lineWidth = s[1]; cx.globalAlpha = s[2];
      cx.beginPath(); cx.moveTo(a[0], a[1]); cx.lineTo(b[0], b[1]);
      [a, b].forEach(function (p) { cx.moveTo(p[0] - nx * tick, p[1] - ny * tick); cx.lineTo(p[0] + nx * tick, p[1] + ny * tick); });
      cx.stroke();
    });
    cx.restore();
  };

  /* The canonical Alaska projection (parallels 55/65, rotate 154). */
  L.alaskaProjection = function (d3) {
    return d3.geoConicEqualArea().parallels([55, 65]).rotate([154, 0]);
  };

  global.AKLAT = L;
})(window);
