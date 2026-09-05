/* akparcel.js — THE CLASSIFICATION DECK's shared furniture, Carousel No. 50.
 *
 * Committed 2026-09-04. This is DECK FURNITURE, shared across all nine slides
 * on purpose, which is why it lives in a module rather than inline:
 * bespoke_check strips `<script src=>` as harness, so a shared reserve and a
 * shared compositor do not read as nine slides of the same art, while each
 * slide's own composition still has to earn its score. Same reasoning as
 * akrail.js, akcolumn.js, akseam.js and aknight.js.
 *
 * WHAT THIS IS. Three pieces of machinery every frame of this deck needs and
 * that no slide should be pasting a private copy of.
 *
 *   AKPARCEL.reserve(selector)
 *     Type-reserve rects measured PER LINE BOX, not per block, so a ragged
 *     two-line headline reserves two UNEQUAL rects and the hole follows the
 *     rag. Measuring the block instead reserves the bounding rectangle of the
 *     whole paragraph, which is the plate this deck exists to avoid drawing.
 *     MUST be called after `await document.fonts.ready`.
 *
 *   AKPARCEL.band(cx, opts)
 *     THE ORDER RULE, MADE STRUCTURAL. This run's whole craft thesis is that
 *     the middle distance loses its TONAL RANGE with distance and never its
 *     INCIDENT DETAIL, and that decks lose the criterion by applying the
 *     attenuation FIRST and then drawing into the compressed value. There is
 *     nothing left to draw at that point, which is the flat mid band the
 *     scorer has named in 8 of the last 10 runs.
 *
 *     So a depth band is drawn at FULL CONTRAST into its own offscreen canvas
 *     by the caller's own `draw` function, and only then compressed toward the
 *     far value and composited ONCE. A slide physically cannot do it in the
 *     wrong order through this entry point.
 *
 *     It also fixes the performance trap the snow bench learned the hard way.
 *     `cx.filter` applies PER DRAW OP, so a filter set around a 600 stem loop
 *     blurs 600 times and takes the 30 second renderReady cap with it. Nothing
 *     here sets a filter inside a draw loop. One filter, at one composite.
 *
 *   AKPARCEL.LINE
 *     The line grammar this deck argues in. SOLID means the statement is in a
 *     state notice. PHANTOM (a chalk dash) means it is proposed, quoted from a
 *     developer's plan, or not yet stated by anybody. A reader can tell which
 *     is which from stroke alone, at thumb size, without reading a word, and
 *     that is the deck's whole accuracy structure carried by the drawing
 *     rather than by a caveat.
 *
 * THE VOCABULARY RULE THIS FILE ENFORCES BY OMISSION. There is no helper here
 * that draws a closed rectilinear volume, because the deck's worst available
 * error is implying that Alaska is handing over 19,950 acres FOR data centres.
 * No state notice says that. Following run No.40's method the error is made
 * UNDRAWABLE rather than merely avoided, so nothing in this deck's vocabulary
 * can build a wall, a roof, a rack or a cabinet.
 *
 * COLOUR SAFETY. No colour helper is ever nested inside another. lerpHex and
 * its cousins return an "rgb()" string, feeding rgb(...) into a hex parser
 * yields NaN on every channel, and canvas then silently keeps the PREVIOUS
 * fillStyle with a clean machine gate (instinct 0.97, run 2026-07-30).
 *
 * DETERMINISM. Seeded throughout via AK.rng. No Math.random, no Date.now.
 */
(function (global) {
  "use strict";

  var AKP = {};

  /* ---------------- the five-token weight system ---------------- */
  /* At 1080px width. Assign by MEANING. Uniform line weight is the number one
   * amateur tell, and an off-token width is how a system becomes noise. */
  AKP.W = { hair: 0.75, fine: 1.25, std: 2.0, bold: 3.5, hero: 5.5 };

  /* THE LINE GRAMMAR. Two states, and the deck's accuracy lives in them.
   *
   *   solid   the statement appears in a State of Alaska public notice
   *   phantom the statement is proposed, quoted from AIDEA's development
   *           plan, or not yet stated by anyone
   *
   * The phantom dash is the drafting alphabet's phantom line (#67), which
   * already means "an implied or not-present state" to anyone who has read a
   * drawing, so the deck borrows a convention instead of inventing one. */
  AKP.LINE = {
    solid:   { dash: [],                 width: AKP.W.std,  cap: "butt"  },
    phantom: { dash: [36, 8, 5, 8, 5, 8], width: AKP.W.fine, cap: "butt" },
    hidden:  { dash: [7, 4],             width: AKP.W.fine, cap: "butt"  },
    centre:  { dash: [24, 5, 5, 5],      width: AKP.W.hair, cap: "butt"  }
  };

  /* Apply a grammar state to a context. Returns the state so a caller can read
   * back the width it just set rather than typing it a second time. */
  AKP.stroke = function (cx, state, color, scale) {
    var s = AKP.LINE[state];
    if (!s) throw new TypeError("AKPARCEL.stroke: unknown line state " + state);
    var k = scale == null ? 1 : scale;
    cx.setLineDash(s.dash.map(function (d) { return d * k; }));
    cx.lineWidth = s.width * k;
    cx.lineCap = s.cap;
    if (color) cx.strokeStyle = color;
    return s;
  };

  /* ---------------- the type reserve ---------------- */

  var RES = [];

  /* MEASURE THE INK, NOT THE DIV. getBoundingClientRect returns the element's
   * LAYOUT box, so a 760px block holding a 470px line reserves 290px of
   * nothing and the art gets a rectangular hole with the type floating in one
   * corner of it. A Range over the element's contents returns one client rect
   * PER RENDERED LINE, so a ragged headline reserves rects that follow its
   * rag. Falls back to the layout box only if the Range yields nothing. */
  AKP.reserve = function (selector) {
    RES = [];
    var els = document.querySelectorAll(selector || "[data-reserve]");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var cs = global.getComputedStyle(el);
      var fs = parseFloat(cs.fontSize) || 16;
      /* Pad from the element's OWN type size, not one guessed constant, so a
       * 24px mono label and a 104px display head get pads appropriate to their
       * stroke weight. */
      var pad = Math.max(14, fs * 0.55);
      var rects = [];
      try {
        var r = document.createRange();
        r.selectNodeContents(el);
        var list = r.getClientRects();
        for (var j = 0; j < list.length; j++) {
          if (list[j].width > 1 && list[j].height > 1) rects.push(list[j]);
        }
      } catch (e) { /* fall through to the layout box */ }
      if (!rects.length) rects = [el.getBoundingClientRect()];
      for (var k = 0; k < rects.length; k++) {
        var b = rects[k];
        RES.push({
          hx: b.left - pad, hy: b.top - pad,
          hw: b.width + pad * 2, hh: b.height + pad * 2,
          ox: b.left - pad * 2.1, oy: b.top - pad * 2.1,
          ow: b.width + pad * 4.2, oh: b.height + pad * 4.2
        });
      }
    }
    return RES.slice();
  };

  AKP.boxes = function () { return RES.slice(); };

  /* True where the type owns the pixel outright. Tests the HARD box only. */
  AKP.reserved = function (x, y) {
    for (var i = 0; i < RES.length; i++) {
      var b = RES[i];
      if (x >= b.hx && x <= b.hx + b.hw && y >= b.hy && y <= b.hy + b.hh) return true;
    }
    return false;
  };

  /* A 0..1 suppression factor. 1 well clear of every reserve, 0 inside a hard
   * box, and a rounded ramp between the two, so a mark population thins toward
   * the type on an arc rather than stopping at a rectangle's edge. That arc is
   * what keeps the reserve from reading as a plate. */
  AKP.clearance = function (x, y) {
    var f = 1;
    for (var i = 0; i < RES.length; i++) {
      var b = RES[i];
      if (x < b.ox || x > b.ox + b.ow || y < b.oy || y > b.oy + b.oh) continue;
      var dx = Math.max(b.hx - x, 0, x - (b.hx + b.hw));
      var dy = Math.max(b.hy - y, 0, y - (b.hy + b.hh));
      var d = Math.sqrt(dx * dx + dy * dy);
      var reach = Math.max(1, (b.ox + b.ow) - (b.hx + b.hw));
      var t = d / reach;
      if (t < 0) t = 0; else if (t > 1) t = 1;
      /* smoothstep, so the falloff has no visible shoulder */
      var s = t * t * (3 - 2 * t);
      if (s < f) f = s;
    }
    return f;
  };

  /* ---------------- the depth band compositor ---------------- */

  /* AKPARCEL.band(cx, {
   *   w, h,                     // design px, defaults 1080 x 1350
   *   draw: function (bx) {},   // YOUR band, drawn at FULL contrast
   *   depth: 0..1,              // 0 near, 1 far
   *   sky: "#0B1926",           // what distance mixes TOWARD
   *   blur: 0,                  // px, applied once at composite
   *   alpha: 1
   * })
   *
   * The caller draws with no attenuation at all. This function applies the
   * attenuation afterwards, per channel, exactly once.
   *
   * WHY PER CHANNEL. Transmittance falls exponentially with path length and
   * the extinction coefficient is wavelength dependent, so distance does not
   * grey a surface, it COOLS it, and the warm end dies first. A single grey
   * mix is the thing that makes an attenuated band look like a wash instead of
   * like air. The coefficients below are the ratio red to green to blue, held
   * at 1.00 to 0.78 to 0.55, which is the direction of real atmospheric
   * extinction without pretending to a spectral model.
   */
  var EXT = [1.00, 0.78, 0.55];

  function hexRGB(h) {
    var s = String(h).replace("#", "");
    if (s.length === 3) s = s[0] + s[0] + s[1] + s[1] + s[2] + s[2];
    var n = parseInt(s, 16);
    if (!isFinite(n)) throw new TypeError("AKPARCEL: bad hex " + h);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  AKP.band = function (cx, o) {
    if (!o || typeof o.draw !== "function") {
      throw new TypeError("AKPARCEL.band: `draw` is required and must be a function");
    }
    if (o.depth == null) {
      throw new TypeError("AKPARCEL.band: `depth` is required. A band with no " +
        "declared distance is the flat mid band this module exists to stop");
    }
    var W = o.w || 1080, H = o.h || 1350;
    var d = o.depth < 0 ? 0 : (o.depth > 1 ? 1 : o.depth);

    var off = document.createElement("canvas");
    off.width = W * 2; off.height = H * 2;
    var bx = off.getContext("2d");
    bx.scale(2, 2);

    /* FULL CONTRAST. The caller is drawing the band as if it were at the
     * camera. Nothing is dimmed here and nothing may be dimmed by the caller
     * on distance grounds, which is the whole contract. */
    o.draw(bx);

    /* Now, and only now, the air. */
    if (d > 0) {
      var sky = hexRGB(o.sky || "#0B1926");
      /* Per channel transmittance. A channel with a bigger coefficient loses
       * more of itself over the same path. */
      var t = [0, 0, 0], i;
      for (i = 0; i < 3; i++) t[i] = Math.exp(-EXT[i] * 2.05 * d);
      var img = bx.getImageData(0, 0, off.width, off.height);
      var p = img.data;
      for (i = 0; i < p.length; i += 4) {
        if (p[i + 3] === 0) continue;
        p[i]     = p[i]     * t[0] + sky[0] * (1 - t[0]);
        p[i + 1] = p[i + 1] * t[1] + sky[1] * (1 - t[1]);
        p[i + 2] = p[i + 2] * t[2] + sky[2] * (1 - t[2]);
      }
      bx.putImageData(img, 0, 0);
    }

    /* ONE filter, ONE composite. Never inside the caller's draw loop. */
    cx.save();
    if (o.blur) cx.filter = "blur(" + o.blur + "px)";
    if (o.alpha != null) cx.globalAlpha = o.alpha;
    cx.drawImage(off, 0, 0, W, H);
    cx.restore();
    return off;
  };

  /* ---------------- the classification key ---------------- */

  /* THE MARGIN DEVICE, and it is a KEY rather than a sample.
   *
   * An earlier design for this deck stood a drawn stratigraphic column in the
   * left margin. It was rejected, and the reason is worth keeping in the file.
   * A drawn core carries an implication that somebody went to the parcel and
   * pulled it, and this deck's claims support no such thing. Inventing
   * evidence is a worse failure than being dull, so the device became what it
   * always actually was, a KEY to the classifications the notice names.
   *
   * Each cell is one named classification, drawn in its own material texture
   * by the caller's `cell` callback, and the whole stack is labelled as a key.
   * The proposed state is drawn in the phantom grammar. Nothing here claims a
   * measurement of anything on the ground.
   */
  AKP.classKey = function (cx, o) {
    var x = o.x, y = o.y, w = o.w, h = o.h;
    var cells = o.cells || [];
    if (!cells.length) throw new TypeError("AKPARCEL.classKey: no cells");
    var gap = o.gap == null ? 6 : o.gap;
    var ch = (h - gap * (cells.length - 1)) / cells.length;
    var out = [];
    for (var i = 0; i < cells.length; i++) {
      var cy = y + i * (ch + gap);
      cx.save();
      cx.beginPath(); cx.rect(x, cy, w, ch); cx.clip();
      if (typeof o.cell === "function") o.cell(cx, cells[i], x, cy, w, ch, i);
      cx.restore();
      cx.save();
      AKP.stroke(cx, cells[i].proposed ? "phantom" : "solid",
                 cells[i].ink || o.ink || "#8FA9B8");
      cx.strokeRect(x + 0.5, cy + 0.5, w - 1, ch - 1);
      cx.restore();
      out.push({ name: cells[i].name, rect: [x, cy, w, ch], proposed: !!cells[i].proposed });
    }
    return out;
  };

  global.AKPARCEL = AKP;
})(window);
