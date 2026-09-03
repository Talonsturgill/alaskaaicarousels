/* akseam.js — THE PANORAMA SEAM, and the two passes that keep a type reserve
   made of the same material as the art.

   Added 2026-09-02 (run No.48). Three things were being pasted into all nine
   slide files, which is exactly the shared drawing code bespoke_check exists to
   catch, and it was right to catch it: this is HOUSE MACHINERY, not any one
   frame's art. It lives here so a slide calls it with its own parameters and
   keeps its own drawing code to itself.

   AKSEAM.y(globalX)
     One continuous curve across a whole deck, with globalX = (n-1)*W + x.
     Every slide draws the same curve over its own window, so the lane's height
     and slope at x = W on slide n are IDENTICAL to its height and slope at
     x = 0 on slide n+1, at every seam, without any slide knowing anything about
     its neighbours. A panorama cannot be an intention; it has to be a function
     of global x, because nobody is going to butt the frames together and check.

   AKSEAM.lane(cx, opts)
     The tube's brightest pass across the mass, in two passes. The second lights
     the slide's own sheet arrises inside the band. The FIRST carries arrises of
     its own whose path is a pure function of globalX and which run the full
     width and off both edges, because relying on the slide's real sheets alone
     leaves the seams dark wherever a sheet's reach noise did not send it to the
     frame edge. Measured on run No.48: 3 of 8 seams carried a matching lit band
     with pass 2 alone, 8 of 8 with pass 1 added.

   AKSEAM.veil(cx, opts)
     Runs the sheet lay back through the reserve at a contrast far below the
     type's, so the reserve stops reading as a soft-edged bright plate. PER LINE,
     never per block: it skips each text line's own client rect with a small pad,
     so the lay comes right up to the letterforms and never crosses one. An
     element rect is a rectangle the size of the whole block, which is the plate
     this is trying to kill.

   AKSEAM.lineLift(cx, opts)
     The last thing the art does. A slide's mass is drawn as FILLED polygons and
     only its strokes are broken around type, so where one sheet face ends
     mid-block its tonal step runs straight through the letterforms and reads as
     a strike-through. Run No.48 shipped a hard rule through the middle of a mono
     chip for exactly this reason, ending at x 675 because that is where that
     sheet's reach ended. This lifts each text line's own box back to the lit
     paper value, feathered, hugging the line. The lay still runs between the
     lines; what it can no longer do is put a step across a word.
*/
(function (root) {
  "use strict";

  function lineRects(sel, pad) {
    pad = pad || [0, 0];
    var out = [], els = document.querySelectorAll(sel);
    for (var e = 0; e < els.length; e++) {
      var walker = document.createTreeWalker(els[e], NodeFilter.SHOW_TEXT, null), t;
      while ((t = walker.nextNode())) {
        if (!t.nodeValue || !t.nodeValue.trim()) continue;
        var rg = document.createRange();
        rg.selectNodeContents(t);
        var rects = rg.getClientRects();
        for (var k = 0; k < rects.length; k++) {
          var r = rects[k];
          if (r.width < 2 || r.height < 2) continue;
          out.push([r.left - pad[0], r.top - pad[1], r.right + pad[0], r.bottom + pad[1]]);
        }
      }
    }
    return out;
  }

  function boxHit(boxes, x, y) {
    for (var i = 0; i < boxes.length; i++) {
      var b = boxes[i];
      if (x >= b[0] && x <= b[2] && y >= b[1] && y <= b[3]) return true;
    }
    return false;
  }

  var AKSEAM = {
    /* deck geometry. W is the frame width, N the slide count. */
    W: 1080,
    N: 9,

    y: function (gx) {
      var span = this.W * this.N;
      var t = gx / span;
      var base = 250 + 760 * (0.5 - 0.5 * Math.cos(Math.PI * (0.12 + 0.88 * t)));
      return base + 108 * AK.simplex2(gx * 0.00072, 91.7)
                  + 34 * AK.simplex2(gx * 0.0031, 17.3);
    },

    half: function (gx) {
      return 58 + 26 * AK.simplex2(gx * 0.0011, 55.1);
    },

    /* opts: {slide, ns, xEnd(i), edgeY(i,x), reserveSel} */
    lane: function (CX, opts) {
      var self = this;
      var G0 = (opts.slide - 1) * this.W;
      var RES = lineRects(opts.reserveSel || "[data-reserve]", [16, 12]);
      function blocked(x, y) {
        return boxHit(RES, x - 4, y) || boxHit(RES, x, y) || boxHit(RES, x + 4, y)
            || boxHit(RES, x, y - 4) || boxHit(RES, x, y + 4);
      }
      CX.save();

      /* pass 1, the lane's own sheets: a pure function of globalX */
      var K = 9;
      for (var k = 0; k < K; k++) {
        var f = (k + 0.5) / K, off = f * 2 - 1;
        var a = Math.pow(1 - Math.abs(off), 1.15);
        var jit = 30 + k * 7;
        var pairs = [
          { dy: 0,   col: "#F1F2E4", w: 0.9 + 2.2 * a, al: 0.24 + 0.60 * a },
          { dy: 3.0, col: "#0B1118", w: 1.0,           al: (0.24 + 0.60 * a) * 0.55 }
        ];
        for (var q = 0; q < pairs.length; q++) {
          var P = pairs[q], open = false;
          CX.globalAlpha = P.al; CX.lineWidth = P.w; CX.strokeStyle = P.col;
          for (var x = -8; x <= this.W + 8; x += 6) {
            var gx = G0 + x;
            var y = self.y(gx) + off * self.half(gx)
                  + 5.5 * AK.simplex2(gx * 0.0042, jit) + P.dy;
            if (blocked(x, y)) { if (open) { CX.stroke(); open = false; } continue; }
            if (!open) { CX.beginPath(); CX.moveTo(x, y); open = true; } else CX.lineTo(x, y);
          }
          if (open) CX.stroke();
        }
      }

      /* pass 2, the slide's real sheets lit inside the same band */
      for (var i = 0; i < opts.ns; i++) {
        var xEnd = opts.xEnd(i); if (xEnd < 40) continue;
        var open2 = false, lastA = 0;
        for (var x2 = 0; x2 <= xEnd; x2 += 7) {
          var y2 = opts.edgeY(i, x2), gx2 = G0 + x2;
          var d = Math.abs(y2 - self.y(gx2)) / self.half(gx2);
          if (d >= 1 || blocked(x2, y2)) { if (open2) { CX.stroke(); open2 = false; } continue; }
          var aa = Math.pow(1 - d, 1.35);
          if (!open2 || Math.abs(aa - lastA) > 0.18) {
            if (open2) CX.stroke();
            CX.beginPath(); CX.moveTo(x2, y2); open2 = true;
            CX.globalAlpha = 0.30 + 0.52 * aa;
            CX.lineWidth = 0.9 + 1.9 * aa;
            CX.strokeStyle = "#F1F2E4";
            lastA = aa;
          } else CX.lineTo(x2, y2);
        }
        if (open2) CX.stroke();
      }
      CX.restore();
    },

    /* opts: {ns, h, xEnd(i), edgeY(i,x), baseY(i), a0, a1, reserveSel} */
    veil: function (CX, opts) {
      var LB = lineRects(opts.reserveSel || "[data-reserve]", [7, 4]);
      function onType(x, y) { return boxHit(LB, x, y) || boxHit(LB, x + 4, y); }
      CX.save();
      for (var i = 0; i < opts.ns; i++) {
        var xEnd = opts.xEnd(i); if (xEnd < 40) continue;
        var y0 = opts.baseY(i);
        if (y0 < -40 || y0 > opts.h + 40) continue;
        var lit = Math.min(1, Math.max(0, (y0 - 300) / 950));
        var al = opts.a0 + opts.a1 * lit;
        var layers = [
          { dy: 0,    col: "#5E6C66", w: 1.0,  al: al },
          { dy: -1.9, col: "#EDF1E2", w: 0.75, al: al * 0.8 }
        ];
        for (var q = 0; q < layers.length; q++) {
          var L = layers[q], open = false;
          CX.globalAlpha = L.al; CX.lineWidth = L.w; CX.strokeStyle = L.col;
          for (var x = 0; x <= xEnd; x += 9) {
            var y = opts.edgeY(i, x) + L.dy;
            if (onType(x, y)) { if (open) { CX.stroke(); open = false; } continue; }
            if (!open) { CX.beginPath(); CX.moveTo(x, y); open = true; } else CX.lineTo(x, y);
          }
          if (open) CX.stroke();
        }
      }
      CX.restore();
    },

    /* opts: {sel, rgb} — sel defaults to the dark-ink text the bloom serves */
    lineLift: function (CX, opts) {
      opts = opts || {};
      var rgb = opts.rgb || "203,210,190";
      var rects = lineRects(opts.sel || "[data-bloom]", [10, 5]);
      CX.save();
      for (var i = 0; i < rects.length; i++) {
        var b = rects[i];
        if (b[2] - b[0] < 6 || b[3] - b[1] < 6) continue;
        var g = CX.createLinearGradient(0, b[1] - 9, 0, b[3] + 9);
        g.addColorStop(0, "rgba(" + rgb + ",0)");
        g.addColorStop(0.24, "rgba(" + rgb + ",0.62)");
        g.addColorStop(0.76, "rgba(" + rgb + ",0.62)");
        g.addColorStop(1, "rgba(" + rgb + ",0)");
        CX.fillStyle = g;
        CX.fillRect(b[0], b[1] - 9, b[2] - b[0], (b[3] - b[1]) + 18);
      }
      CX.restore();
    }
  };


  /* ---------------------------------------------------------------------
     THE RESERVE MACHINERY, also house furniture rather than any frame's art.
     Every slide in run No.48 carried its own verbatim copy of measureReserve,
     inRes, segBlocked, strokeBroken and fanBloom, which is what pushed
     bespoke_check's median pairwise similarity to 0.605 and is exactly the
     shared-drawing-code the gate exists to catch. A slide now supplies its own
     pads and its own curve and keeps its composition to itself.

     TWO THINGS THIS ENCODES that were learned the hard way (2026-09-02):
     THE PAD SCALES WITH THE STROKE. A lee stroke in a splayed lane can be 26px
     wide, so a centreline 24px clear of a glyph box still paints inside it.
     A SEGMENT, not a point, is what gets drawn. Testing only the sample points
     lets the span between two samples cross a glyph, which is what qa.py's
     canvas-mark-inside-reserved-text check caught on five slides.
     --------------------------------------------------------------------- */
  AKSEAM.reserve = function (sel, pad) {
    pad = pad || [24, 24, 24, 22];
    var R = [], els = document.querySelectorAll(sel || "[data-reserve]");
    for (var i = 0; i < els.length; i++) {
      var r = els[i].getBoundingClientRect();
      R.push([r.left - pad[0], r.top - pad[1], r.right + pad[2], r.bottom + pad[3]]);
    }
    return {
      boxes: R,
      hit: function (x, y, p) {
        p = p || 0;
        for (var i = 0; i < R.length; i++) {
          var b = R[i];
          if (x >= b[0] - p && x <= b[2] + p && y >= b[1] - p && y <= b[3] + p) return true;
        }
        return false;
      },
      seg: function (fy, x, step, p) {
        for (var t = 0; t <= 1.0001; t += 0.2) {
          var xx = x + step * t;
          if (this.hit(xx, fy(xx), p)) return true;
        }
        return false;
      }
    };
  };

  AKSEAM.strokeBroken = function (CX, res, fy, x0, x1, step, lw, color) {
    CX.lineWidth = lw; CX.strokeStyle = color;
    var open = false, pad = lw * 0.55 + 9;
    for (var x = x0; x <= x1; x += step) {
      if (res.seg(fy, x - step, step * 2, pad)) { if (open) { CX.stroke(); open = false; } continue; }
      var y = fy(x);
      if (!open) { CX.beginPath(); CX.moveTo(x, y); open = true; } else CX.lineTo(x, y);
    }
    if (open) CX.stroke();
  };

  /* Where the stack is thumbed fully open the individual faces stop reading as
     separate bands and merge into one lit surface, so the tonal banding under
     the type flattens FOR A PHYSICAL REASON. Feathered hard, made of the
     material's own lit colour, never a hard plate edge. */
  AKSEAM.bloom = function (CX, opts) {
    opts = opts || {};
    var sel = opts.sel || "[data-bloom]";
    var m = opts.margin || [30, 30, 30, 26];
    var gx = opts.grow || [72, 38];
    var rgb = opts.rgb || "203,210,190";
    var mid = (opts.mid === undefined) ? 0.66 : opts.mid;
    var midA = (opts.midA === undefined) ? 0.56 : opts.midA;
    var els = document.querySelectorAll(sel);
    for (var k = 0; k < els.length; k++) {
      var rr = els[k].getBoundingClientRect();
      var b = [rr.left - m[0], rr.top - m[1], rr.right + m[2], rr.bottom + m[3]];
      var cx0 = (b[0] + b[2]) / 2, cy0 = (b[1] + b[3]) / 2;
      var rx = (b[2] - b[0]) / 2 + gx[0], ry = (b[3] - b[1]) / 2 + gx[1];
      var rad = Math.max(rx, ry);
      CX.save();
      CX.translate(cx0, cy0); CX.scale(rx / rad, ry / rad); CX.translate(-cx0, -cy0);
      var g2 = CX.createRadialGradient(cx0, cy0, rad * 0.34, cx0, cy0, rad);
      g2.addColorStop(0, "rgba(" + rgb + ",0.74)");
      g2.addColorStop(mid, "rgba(" + rgb + "," + midA + ")");
      g2.addColorStop(1, "rgba(" + rgb + ",0)");
      CX.fillStyle = g2;
      CX.beginPath(); CX.arc(cx0, cy0, rad, 0, 6.2832); CX.fill();
      CX.restore();
    }
  };

  root.AKSEAM = AKSEAM;
})(typeof window !== "undefined" ? window : this);
