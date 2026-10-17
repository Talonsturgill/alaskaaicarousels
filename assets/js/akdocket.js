/* akdocket.js — the pleading page's furniture for No.88 (Alaska.Ai, 2026-10-16). A classic script.
 *
 * The deck is a hearing transcript. Every frame carries the same instrument in its left margin: an oxblood
 * double rule that is a CALENDAR, July 10th at y 150 to October 26th at y 1230, 10 design px per day, with a
 * notch for each dated document the frame cites. October 26th's notch is gold on every frame, because gold
 * means exactly one thing in this deck: the answer owed that day. Under every answer sits the ANSWER LINE,
 * whose shape (dashed, solid, a groove, stopped short, doubled, ending in the Polaris) says what kind of answer
 * the record holds. Both are SVG so they stay vector in the PDF.
 *
 *   AKDOCKET.DAY0 = 150, AKDOCKET.PXDAY = 10           // y = 150 + 10 * days since July 10th
 *   AKDOCKET.y('2026-09-22') -> 890
 *   AKDOCKET.chrome({n: 1, total: 9, notches: ['2026-09-22'], polaris: false})
 *   AKDOCKET.answerLine({y, x0, x1, state: 'dashed' | 'solid' | 'stop' | 'double' | 'broken' | 'polaris', stopAt, gapAt})
 *
 * The slide's <body> declares the calendar as a measured axis itself (data-scale must be literal markup);
 * AKDOCKET.scaleMarks(notches) returns the marks array a slide pastes there, so the two can't disagree.
 */
(function (global) {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const D = {};
  D.DAY0 = 150; D.PXDAY = 10; D.X_RULE = 118; D.TICK = [98, 116];
  D.OXBLOOD = "#8C3B32"; D.GOLD = "#FFC72C"; D.FIX = "#46545F";
  const START = Date.UTC(2026, 6, 10);
  D.days = function (iso) { const [y, m, d] = iso.split("-").map(Number); return Math.round((Date.UTC(y, m - 1, d) - START) / 86400000); };
  D.y = function (iso) { return D.DAY0 + D.PXDAY * D.days(iso); };
  function el(tag, attrs, parent) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  D.svg = function (z) {
    const s = el("svg", { width: 1080, height: 1350, viewBox: "0 0 1080 1350" });
    s.style.cssText = "position:absolute;left:0;top:0;width:1080px;height:1350px;pointer-events:none;z-index:" + (z || 5);
    document.body.appendChild(s); return s;
  };
  // the polaris: a four point star, long vertical arms
  D.polaris = function (svg, cx, cy, r, fill) {
    const a = r, b = r * 0.22, d = `M ${cx} ${cy - a} L ${cx + b} ${cy - b} L ${cx + a * 0.72} ${cy} L ${cx + b} ${cy + b} L ${cx} ${cy + a} L ${cx - b} ${cy + b} L ${cx - a * 0.72} ${cy} L ${cx - b} ${cy - b} Z`;
    return el("path", { d, fill: fill || D.GOLD }, svg);
  };
  D.chrome = function (o) {
    const s = D.svg(o.z || 6);
    // a dark casing under the rule where it crosses art, then the double rule
    el("line", { x1: D.X_RULE + 3, y1: D.DAY0 - 6, x2: D.X_RULE + 3, y2: D.y("2026-10-26") + 6, stroke: "#05070C", "stroke-width": 10, "stroke-opacity": o.casing == null ? 0.55 : o.casing }, s);
    el("line", { x1: D.X_RULE, y1: D.DAY0 - 6, x2: D.X_RULE, y2: D.y("2026-10-26") + 6, stroke: o.ruleColor || D.OXBLOOD, "stroke-width": 1.8 }, s);
    el("line", { x1: D.X_RULE + 6, y1: D.DAY0 - 6, x2: D.X_RULE + 6, y2: D.y("2026-10-26") + 6, stroke: o.ruleColor || D.OXBLOOD, "stroke-width": 0.9 }, s);
    (o.notches || []).forEach(iso => { const y = D.y(iso); el("line", { x1: D.TICK[0], y1: y, x2: D.TICK[1], y2: y, stroke: o.ruleColor || D.OXBLOOD, "stroke-width": 2.4 }, s); });
    const yg = D.y("2026-10-26");
    if (o.notchCasing) el("line", { x1: 90, y1: yg, x2: D.X_RULE + 12, y2: yg, stroke: o.notchCasing, "stroke-width": 7 }, s);   // on a light ground the gold needs a dark bed to read
    el("line", { x1: 92, y1: yg, x2: D.X_RULE + 10, y2: yg, stroke: D.GOLD, "stroke-width": 3.2 }, s);
    if (o.polaris) D.polaris(s, 80, yg, 13);
    return s;
  };
  D.scaleMarks = function (notches, polaris) {
    const m = (notches || []).map(n => ({ at: D.y(n.iso || n), means: (n.means || n.iso || n) }));
    m.push({ at: D.y("2026-10-26"), means: "October 26th, the hearing, gold" });
    return m;
  };
  D.answerLine = function (svg, o) {
    const g = el("g", {}, svg), y = o.y, x0 = o.x0 == null ? 200 : o.x0, x1 = o.x1 == null ? 1000 : o.x1;
    const st = o.state || "dashed", w = o.width || 3;
    const dash = { stroke: D.GOLD, "stroke-width": w, "stroke-dasharray": "22 10", "stroke-linecap": "butt" };
    if (st === "dashed") el("line", Object.assign({ x1: x0, y1: y, x2: x1, y2: y }, dash), g);
    else if (st === "stop") { el("line", Object.assign({ x1: x0, y1: y, x2: o.stopAt, y2: y }, dash), g); el("line", { x1: o.stopAt, y1: y - 9, x2: o.stopAt, y2: y + 9, stroke: D.GOLD, "stroke-width": 2 }, g); }
    else if (st === "broken") { el("line", Object.assign({ x1: x0, y1: y, x2: o.gapAt[0], y2: y }, dash), g); el("line", Object.assign({ x1: o.gapAt[1], y1: y, x2: x1, y2: y }, dash), g); }
    else if (st === "double") { el("line", Object.assign({ x1: x0, y1: y - 3.5, x2: x1, y2: y - 3.5 }, dash, { "stroke-width": 2 }), g); el("line", Object.assign({ x1: x0, y1: y + 3.5, x2: x1, y2: y + 3.5 }, dash, { "stroke-width": 2 }), g); }
    else if (st === "solid" || st === "polaris") { el("line", { x1: x0, y1: y, x2: st === "polaris" ? x1 - 30 : x1, y2: y, stroke: D.GOLD, "stroke-width": w }, g); if (st === "polaris") D.polaris(g, x1 - 12, y, 20); }
    return g;
  };
  // the fixed marks: wordmark, counter, site; all DOM so they stay vector and the gates can read them. z-index 9 because
  // every plate is a z-index 1 canvas and an unstacked fixture paints UNDER it (No.88 round 1: present in the DOM, absent in pixels)
  D.fixtures = function (o) {
    const css = "position:absolute;z-index:9;font-family:'JetBrains Mono';font-weight:500;letter-spacing:0.08em;";
    const w = document.createElement("div"); w.textContent = "ALASKA.AI"; w.setAttribute("data-decorative", "");
    w.style.cssText = css + "left:80px;top:84px;font-size:22px;color:" + (o.ink || "#B9BDC2") + ";"; document.body.appendChild(w);
    const c = document.createElement("div"); c.textContent = String(o.n).padStart(2, "0") + " / " + String(o.total).padStart(2, "0");
    c.style.cssText = css + "right:80px;top:82px;font-size:24px;color:" + (o.ink || "#B9BDC2") + ";"; c.className = "counter"; document.body.appendChild(c);
    const f = document.createElement("div"); f.textContent = "alaskaaihq.com"; f.setAttribute("data-decorative", "");
    f.style.cssText = "position:absolute;z-index:9;left:200px;top:1291px;font-family:'JetBrains Mono';font-weight:400;font-size:19px;letter-spacing:0.04em;color:" + (o.fix || D.FIX) + ";"; document.body.appendChild(f);
    return { wordmark: w, counter: c, site: f };
  };
  global.AKDOCKET = D;
})(window);
