/* aklocator.js -- THE ONE-LINE LOCATOR, Carousel No.102's deck furniture (2026-11-01).
 *
 * A single-line electrical diagram, drawn in drafting voice, that sits in the
 * top band of every frame and changes state BY SHAPE with the story: source,
 * line, town bus, (rules breaker), transformer, switch, then two branches, up
 * to the grid LOAD and down to on-site GEN. It is furniture, like the counter:
 * it draws no slide. Every slide passes its own state.
 *
 *   AKLOC.mount(el, state)   writes an inline SVG into el (440 x 48 design px)
 *
 *   state = {
 *     gold:  'hydro' | 'xfmr' | 'switch' | 'gen' | 'load' | 'rules' | null,
 *            the ONE node this frame is about, ringed in flag gold
 *     twoSources: bool,   a second source circle upstream (own plant + SEAPA)
 *     rules: null | 'phantom' | 'solid',   a breaker square on the town bus
 *     loadDash: bool,     the LOAD box drawn dashed (a proposal, not a load)
 *     genPhantom: bool,   the GEN circle drawn as a phantom (the doubted case)
 *     genStop: bool,      a stop bar across the GEN branch (the draft pause)
 *     tick: bool,         a gold dimension tick under XFMR to LOAD
 *     dim: number         overall opacity (breather frames)
 *   }
 *
 * Colours: energized #5AC8F0 hairline, phantom #5A6B73 dash 5 3, nodes
 * #A9B8C4, gold #FFC72C. Labels are 12 px mono and data-decorative: the
 * locator is a recognition mark, its story is told by the slide's own type.
 */
(function (global) {
  "use strict";
  var ICE = "#5AC8F0", PH = "#5A6B73", ND = "#A9B8C4", GOLD = "#FFC72C";

  function ring(x, y, r) {
    return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="none" stroke="' + GOLD +
      '" stroke-width="2.4"/>';
  }
  function label(x, y, t, anchor) {
    return '<text x="' + x + '" y="' + y + '" text-anchor="' + (anchor || "middle") +
      '" font-family="JetBrains Mono, monospace" font-size="13" font-weight="500" ' +
      'letter-spacing="0.9" fill="#7F909B">' + t + '</text>';
  }
  function line(x1, y1, x2, y2, live) {
    return '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="' +
      (live ? ICE : PH) + '" stroke-width="' + (live ? 1.5 : 1.2) + '"' +
      (live ? '' : ' stroke-dasharray="5 3"') + ' stroke-linecap="butt"/>';
  }

  function svg(s) {
    s = s || {};
    var o = [], y = 20;
    // source(s)
    var sx = s.twoSources ? 36 : 14;
    if (s.twoSources) {
      o.push('<circle cx="6" cy="' + y + '" r="6" fill="none" stroke="' + ND + '" stroke-width="1.2"/>');
      o.push('<path d="M2 ' + y + ' q2 -3.5 4 0 t4 0" fill="none" stroke="' + ND + '" stroke-width="1"/>');
      o.push(line(12, y, sx - 8, y, true));
    }
    o.push('<circle cx="' + sx + '" cy="' + y + '" r="8" fill="none" stroke="' + ND + '" stroke-width="1.3"/>');
    o.push('<path d="M' + (sx - 5) + ' ' + y + ' q2.5 -4.5 5 0 t5 0" fill="none" stroke="' + ND + '" stroke-width="1.1"/>');
    if (s.gold === "hydro") o.push(ring(sx, y, 12));
    o.push(label(sx, 44, "HYDRO"));
    // line to the town bus
    o.push(line(sx + 8, y, 104, y, true));
    o.push('<rect x="104" y="' + (y - 10) + '" width="4" height="20" fill="' + ND + '"/>');
    o.push(label(106, 44, "TOWN"));
    // rules breaker on the bus side
    var bx = 108;
    if (s.rules) {
      o.push(line(108, y, 140, y, true));
      o.push('<rect x="140" y="' + (y - 7) + '" width="14" height="14" fill="none" stroke="' + ND +
        '" stroke-width="1.3"' + (s.rules === "phantom" ? ' stroke-dasharray="3 2"' : '') + '/>');
      if (s.gold === "rules") o.push(ring(147, y, 13));
      o.push(label(147, 4, "RULES"));
      bx = 154;
    }
    // transformer: two touching circles
    o.push(line(bx, y, 196, y, true));
    o.push('<circle cx="204" cy="' + y + '" r="8" fill="none" stroke="' + ND + '" stroke-width="1.3"/>');
    o.push('<circle cx="216" cy="' + y + '" r="8" fill="none" stroke="' + ND + '" stroke-width="1.3"/>');
    if (s.gold === "xfmr") o.push('<ellipse cx="210" cy="' + y + '" rx="18" ry="12" fill="none" stroke="' + GOLD + '" stroke-width="2.4"/>');
    o.push(label(210, 44, "2 MW"));
    // idle: everything past the transformer is phantom
    o.push(line(224, y, 254, y, false));
    // switch blade
    o.push('<circle cx="256" cy="' + y + '" r="2" fill="' + ND + '"/>');
    o.push('<line x1="256" y1="' + y + '" x2="280" y2="' + (y - 9) + '" stroke="' + ND + '" stroke-width="1.6"/>');
    o.push('<circle cx="284" cy="' + y + '" r="2" fill="' + ND + '"/>');
    if (s.gold === "switch") o.push(ring(270, y - 3, 15));
    // branches
    o.push(line(286, y, 300, y, false));
    o.push(line(300, y, 300, 6, false)); o.push(line(300, 6, 352, 6, false));
    o.push(line(300, y, 300, 34, false)); o.push(line(300, 34, 352, 34, false));
    // load box (top)
    o.push('<rect x="352" y="0" width="22" height="12" fill="none" stroke="' + ND + '" stroke-width="1.3"' +
      (s.loadDash ? ' stroke-dasharray="3 2"' : '') + '/>');
    if (s.gold === "load") o.push(ring(363, 6, 14));
    o.push(label(384, 10, "GRID LOAD", "start"));
    // generator (bottom)
    o.push('<circle cx="362" cy="34" r="7" fill="none" stroke="' + (s.genPhantom ? PH : ND) + '" stroke-width="1.3"' +
      (s.genPhantom ? ' stroke-dasharray="3 2"' : '') + '/>');
    o.push('<text x="362" y="38" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="' +
      (s.genPhantom ? PH : ND) + '">G</text>');
    if (s.gold === "gen") o.push(ring(362, 34, 12));
    o.push(label(384, 38, "ON-SITE", "start"));
    if (s.genStop) o.push('<line x1="326" y1="27" x2="326" y2="41" stroke="' + ND + '" stroke-width="2.2"/>');
    if (s.tick) {
      o.push('<line x1="216" y1="52" x2="352" y2="52" stroke="' + GOLD + '" stroke-width="1.2"/>');
      o.push('<line x1="216" y1="48" x2="216" y2="56" stroke="' + GOLD + '" stroke-width="1.2"/>');
      o.push('<line x1="352" y1="48" x2="352" y2="56" stroke="' + GOLD + '" stroke-width="1.2"/>');
    }
    var op = s.dim != null ? s.dim : 1;
    return '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="48" viewBox="0 0 500 48" ' +
      'style="overflow:visible;opacity:' + op + '"><g transform="translate(10,0)">' + o.join("") + '</g></svg>';
  }

  global.AKLOC = {
    svg: svg,
    mount: function (el, state) { el.innerHTML = svg(state); el.setAttribute("data-decorative", ""); return el; }
  };
})(typeof window !== "undefined" ? window : this);
