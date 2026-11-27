/* akdater.js — the band dater, Carousel No.125's deck furniture (2026-11-26).
 *
 * Classic script, global AKDATER. bespoke_check strips `<script src=>` as
 * harness, so the fixtures here cost the variety budget nothing while every
 * frame's own drawing stays its own code.
 *
 * WHAT IT OWNS (and nothing about composition)
 *   AKDATER.fixtures(n, o)   counter, site fixture and THE DATE CHIP as DOM/SVG.
 *   AKDATER.INK              the deck's ink law, one meaning per ink:
 *                              RED   #B53A2E  a date or a change the record prints
 *                              GOLD  #FFC72C  June 30th, 2028, and the time before
 *                                             it to write rules (and the Polaris)
 *                              dashed graphite  a date that is arithmetic or a
 *                                             projection, or a start not yet set
 *   AKDATER.lampFall(x, y)   the deck's one light law in 2D: the tungsten lamp at
 *                            the upper left, returned as 0..1 falloff for a point
 *                            in design px. Every drawn frame lights from here.
 */
(function (global) {
  "use strict";
  var D = global.AKDATER || (global.AKDATER = {});
  D.INK = { RED: "#B53A2E", GOLD: "#FFC72C", DASH: "#8E9AA6" };
  D.LAMP = { x: -260, y: -420, reach: 1900 };

  D.lampFall = function (x, y) {
    var dx = x - D.LAMP.x, dy = y - D.LAMP.y;
    var d = Math.sqrt(dx * dx + dy * dy) / D.LAMP.reach;
    var f = 1 - d;
    return f < 0 ? 0 : f > 1 ? 1 : f * f * (3 - 2 * f);
  };

  var CSS = "" +
    ".akd-counter{position:absolute;right:80px;top:80px;z-index:20;font:500 22px/1 'JetBrains Mono',monospace;letter-spacing:.08em;color:#A8B6BC;text-align:right;white-space:nowrap}" +
    ".akd-counter b{font-weight:500;color:#F4F8FF;margin-left:18px}" +
    ".akd-site{position:absolute;left:80px;bottom:50px;z-index:20;font:500 20px/1 'JetBrains Mono',monospace;letter-spacing:.06em;color:#8E9EA4}" +
    ".akd-chip{position:absolute;right:80px;bottom:44px;z-index:20;width:180px;height:38px}";

  /* fixtures(n, o)
   *   o.chip   {text: "2028-06-30" | "", ink: "red" | "gold" | "dash"}
   *   o.dark   true when the frame's bottom is paper (ink fixtures instead of snow)
   */
  D.fixtures = function (n, o) {
    o = o || {};
    if (!document.getElementById("akd-css")) {
      var st = document.createElement("style"); st.id = "akd-css"; st.textContent = CSS; document.head.appendChild(st);
    }
    var host = o.host || document.body;
    var c = document.createElement("div"); c.className = "akd-counter"; c.setAttribute("data-decorative", "");
    c.innerHTML = "ALASKA.AI<b>" + (n < 10 ? "0" + n : n) + " / 09</b>";
    if (o.counterColor) c.style.color = o.counterColor;
    if (o.boldColor) c.querySelector("b").style.color = o.boldColor;
    host.appendChild(c);
    var s = document.createElement("div"); s.className = "akd-site"; s.setAttribute("data-decorative", "");
    s.textContent = "alaskaaihq.com"; if (o.siteColor) s.style.color = o.siteColor;
    host.appendChild(s);
    if (o.chip) D.chip(host, o.chip, o);
  };

  /* THE DATE CHIP: a band-dater impression in a small plate, the deck's motif.
   * Its ink is the ink law. A blank chip is an empty dashed band: no date set. */
  D.chip = function (host, chip, o) {
    var NS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "akd-chip"); svg.setAttribute("viewBox", "0 0 180 38");
    svg.setAttribute("data-decorative", "");
    function el(t, a, parent) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); (parent || svg).appendChild(e); return e; }
    var ink = chip.ink === "gold" ? D.INK.GOLD : chip.ink === "red" ? D.INK.RED : D.INK.DASH;
    var plate = o.plate || "rgba(6,10,18,0.78)";
    el("rect", { x: 1, y: 1, width: 178, height: 36, rx: 2, fill: plate });
    var dashed = chip.ink === "dash";
    el("rect", { x: 7, y: 6, width: 166, height: 26, rx: 1.5, fill: "none", stroke: ink,
                 "stroke-width": 1.6, "stroke-dasharray": dashed ? "4 3" : "none" });
    if (chip.text) {
      var t = el("text", { x: 90, y: 24.5, "text-anchor": "middle", fill: ink,
                           "font-family": "JetBrains Mono, monospace", "font-weight": 500, "font-size": 16,
                           "letter-spacing": "1.6" });
      t.textContent = chip.text;
      if (dashed) t.setAttribute("fill-opacity", "0.9");
    }
    host.appendChild(svg);
    return svg;
  };
})(this);
