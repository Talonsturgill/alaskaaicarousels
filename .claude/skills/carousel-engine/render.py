#!/usr/bin/env python3
"""render.py — deterministic slide renderer for Alaska.Ai LinkedIn carousels.

Renders per-slide HTML files to exact-size PNGs via headless Chromium
(pre-installed in the cloud environment), and extracts an objective in-page
QA report (console/page errors, missing fonts, text-node geometry, clipped
or offscreen text) that downstream gates consume.

Conventions the slide HTML must follow (see SKILL.md for the full contract):
  - One file per slide, named  slide-01.html, slide-02.html, ...
  - Canvas is the viewport: design for exactly 1080x1350 CSS px (4:5).
  - Reference committed assets with the @@ASSETS@@ token, e.g.
      <link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
      <script src="@@ASSETS@@/js/noise.js"></script>
      fetch("@@ASSETS@@/geo/alaska-state.geo.json")
    The renderer resolves the token to an absolute file:// path.
  - NO external URLs (no CDNs, no Google Fonts, no http(s) at all).
  - If artwork draws asynchronously (canvas animation frames, fetched
    geodata), set  window.renderReady = new Promise(...)  and resolve it
    when the final frame is painted. The renderer awaits it (30s cap).

Usage:
  python .claude/skills/carousel-engine/render.py \
      --slides-dir out/run/slides --out-dir out/run/render [--scale 2] [--only 2,5]

Exit codes: 0 = all slides rendered (warnings possible; read the report),
            1 = at least one slide hard-failed (JS error, timeout, missing PNG).
Writes: <out-dir>/slide-XX.png + <out-dir>/render_report.json
"""

import argparse
import base64
import glob
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[3]
ASSETS_DIR = REPO_ROOT / "assets"

CHROMIUM_ARGS = [
    "--allow-file-access-from-files",   # lets slides fetch() committed geodata
    "--hide-scrollbars",
    "--force-color-profile=srgb",
    "--disable-lcd-text",               # subpixel AA looks wrong in screenshots
    "--font-render-hinting=none",       # fixes headless kerning/letter-spacing bugs
    "--enable-unsafe-swiftshader",      # software WebGL (experimental; probe before relying on it)
]

# Instrument canvas text BEFORE any slide script runs (add_init_script runs
# before all page scripts). Canvas fillText/strokeText ink is a raster bitmap:
# invisible to render.py's DOM walk, to copy_sync_check, to the LinkedIn ranker,
# and to accessibility, and it pixelates in the vector PDF. We record every
# non-empty text call so qa.py can WARN when a slide draws MEANINGFUL text on
# canvas (2026-07-19: S7 loop labels + S8 annotations were cx.fillText and had
# to be converted to DOM by hand; no gate saw the unauthored ones). The wrapper
# only observes and forwards; it never alters the drawn frame.
CANVAS_TEXT_HOOK_JS = """
(() => {
  try {
    window.__akCanvasText = [];
    const proto = window.CanvasRenderingContext2D && window.CanvasRenderingContext2D.prototype;
    if (!proto) return;
    for (const fn of ['fillText', 'strokeText']) {
      const orig = proto[fn];
      if (typeof orig !== 'function') continue;
      proto[fn] = function (text) {
        try {
          const s = (text == null ? '' : String(text));
          if (s.trim().length && window.__akCanvasText.length < 500) {
            /* MEASURE IT WHERE IT LANDS (2026-08-13). Capturing only the
               string let run No.32 ship a canvas label whose tail ran off the
               right frame edge: the render printed "MORE THAN 20. TWO READS
               DISA" and the claim-id was severed. Canvas has no layout engine,
               so nothing overflowed and nothing warned, and qa.py, copy_sync
               and the aggregate gate all returned clean. The scorer caught it
               by eye. Recording x/y and the measured advance makes the bound
               checkable; qa.py does the checking. */
            var _e = { text: s.slice(0, 80), fn: fn, font: this.font || '' };
            try {
              var _t = this.getTransform ? this.getTransform() : null;
              var _w = this.measureText(s).width;
              _e.x = arguments[1]; _e.y = arguments[2];
              _e.w = _w;
              _e.align = this.textAlign || 'start';
              _e.canvas_w = this.canvas ? this.canvas.width : 0;
              _e.canvas_h = this.canvas ? this.canvas.height : 0;
              if (_t) {
                _e.sx = _t.a; _t_b = _t.b;
                _e.skew = (_t.b || 0) !== 0 || (_t.c || 0) !== 0;
                /* device-space span of the laid-out string */
                var _x0 = arguments[1];
                if (_e.align === 'center') _x0 = arguments[1] - _w / 2;
                else if (_e.align === 'right' || _e.align === 'end') _x0 = arguments[1] - _w;
                _e.dev_left = _t.a * _x0 + _t.e;
                _e.dev_right = _t.a * (_x0 + _w) + _t.e;
              }
            } catch (e2) {}
            window.__akCanvasText.push(_e);
          }
        } catch (e) {}
        return orig.apply(this, arguments);
      };
    }
  } catch (e) {}
})();
"""

# A CIRCULAR GRADIENT POURED INTO AN ELLIPSE (2026-08-26). Canvas has no
# elliptical gradient. The only way to get one is to scale a circle inside a
# transform (translate, scale(1, ry/r), arc), which is what this deck's lit
# pools already do. Run No.41 added a type reserve to six slides written the
# other way -- createRadialGradient(0,0,24, 0,0,r) filled into
# ctx.ellipse(cx,cy,r,ry) with ry well under r -- so the ramp was CIRCULAR and
# the fill was ELLIPTICAL, and vertically the paint stopped while the ramp was
# still carrying about 0.30 alpha. Every one of the six slides got a hard arc
# across its ground. Four independent pixel critics reported that arc as the
# most conspicuous thing in the frame, one bug in one idiom cost a full editing
# round to put back, and no machine gate saw it: the render succeeded, nothing
# overflowed, contrast improved, and the arc is a legitimate shape as far as
# every existing measurement is concerned.
#
# This reads the two numbers that make it a defect. It records a fill only when
# ALL of the following hold, which is why it is quiet on honest drawing:
#   * the path is exactly one ellipse and nothing else,
#   * the fill style is a radial gradient whose LAST stop is transparent, so
#     the author's declared intent was a fade to nothing,
#   * the alpha still standing where the ellipse's SHORT axis cuts the ramp is
#     materially higher than the alpha at the long axis. A fill clipped equally
#     on both axes is a deliberate hard-edged blob and is not reported.
# Everything is measured in user space, where both the path and the gradient
# live, so the current transform distorts them together and cancels out.
# The wrapper only observes and forwards; it never alters the drawn frame.
GRADIENT_CLIP_HOOK_JS = """
(() => {
  try {
    window.__akGradientClip = [];
    const proto = window.CanvasRenderingContext2D && window.CanvasRenderingContext2D.prototype;
    const gproto = window.CanvasGradient && window.CanvasGradient.prototype;
    if (!proto || !gproto) return;
    const meta = new WeakMap();
    const ALPHA_GAP = 0.03;   /* ~8/255: the step a hard edge needs to be seen */
    const TAIL_ALPHA = 0.02;  /* below this the author meant "fade to nothing" */

    const origRad = proto.createRadialGradient;
    if (typeof origRad === 'function') {
      proto.createRadialGradient = function (x0, y0, r0, x1, y1, r1) {
        const g = origRad.apply(this, arguments);
        try { meta.set(g, { x1: x1, y1: y1, r0: r0, r1: r1, stops: [] }); } catch (e) {}
        return g;
      };
    }
    const origStop = gproto.addColorStop;
    if (typeof origStop === 'function') {
      gproto.addColorStop = function (off, col) {
        try {
          const m = meta.get(this);
          if (m && m.stops.length < 32) m.stops.push([Number(off), String(col)]);
        } catch (e) {}
        return origStop.apply(this, arguments);
      };
    }

    /* Alpha of a colour string. Anything we cannot read is treated as opaque,
       which can only make the check QUIETER (an opaque tail is not a fade). */
    const alphaOf = (c) => {
      c = (c || '').trim().toLowerCase();
      if (c === 'transparent') return 0;
      let m = c.match(/^rgba?\\(([^)]+)\\)$/);
      if (m) {
        const p = m[1].split(/[,\\/\\s]+/).filter((s) => s.length);
        return p.length >= 4 ? Math.max(0, Math.min(1, parseFloat(p[3]))) : 1;
      }
      m = c.match(/^#([0-9a-f]{8})$/);
      if (m) return parseInt(m[1].slice(6), 16) / 255;
      m = c.match(/^#([0-9a-f]{4})$/);
      if (m) return parseInt(m[1].slice(3) + m[1].slice(3), 16) / 255;
      return 1;
    };
    /* Alpha the ramp is carrying at offset t, linearly between its stops. */
    const alphaAt = (stops, t) => {
      if (!stops.length) return 1;
      const s = stops.slice().sort((a, b) => a[0] - b[0]);
      if (t <= s[0][0]) return alphaOf(s[0][1]);
      if (t >= s[s.length - 1][0]) return alphaOf(s[s.length - 1][1]);
      for (let i = 1; i < s.length; i++) {
        if (t <= s[i][0]) {
          const span = s[i][0] - s[i - 1][0];
          const f = span <= 0 ? 1 : (t - s[i - 1][0]) / span;
          return alphaOf(s[i - 1][1]) * (1 - f) + alphaOf(s[i][1]) * f;
        }
      }
      return alphaOf(s[s.length - 1][1]);
    };

    const path = (ctx) => {
      if (!ctx.__akPath) ctx.__akPath = { ell: [], other: 0 };
      return ctx.__akPath;
    };
    const origBegin = proto.beginPath;
    proto.beginPath = function () {
      try { this.__akPath = { ell: [], other: 0 }; } catch (e) {}
      return origBegin.apply(this, arguments);
    };
    const origEllipse = proto.ellipse;
    if (typeof origEllipse === 'function') {
      proto.ellipse = function (x, y, rx, ry) {
        try { path(this).ell.push({ x: x, y: y, rx: Math.abs(rx), ry: Math.abs(ry) }); } catch (e) {}
        return origEllipse.apply(this, arguments);
      };
    }
    for (const fn of ['arc', 'arcTo', 'rect', 'roundRect', 'moveTo', 'lineTo',
                      'quadraticCurveTo', 'bezierCurveTo']) {
      const orig = proto[fn];
      if (typeof orig !== 'function') continue;
      proto[fn] = function () {
        try { path(this).other++; } catch (e) {}
        return orig.apply(this, arguments);
      };
    }

    const origFill = proto.fill;
    proto.fill = function () {
      try {
        if (!(arguments.length && arguments[0] && typeof arguments[0] === 'object')) {
          const p = path(this);
          if (p.ell.length === 1 && p.other === 0 &&
              window.__akGradientClip.length < 40) {
            const e = p.ell[0], m = meta.get(this.fillStyle);
            if (m && m.r1 > 0 && Math.abs(e.rx - e.ry) > 0.5 && m.stops.length) {
              const tail = alphaAt(m.stops, 1);
              if (tail <= TAIL_ALPHA) {
                /* Where each axis of the ellipse cuts the ramp, as an offset
                   along the ramp measured from the ramp's own outer centre. */
                const tOf = (px, py) =>
                  Math.hypot(px - m.x1, py - m.y1) / m.r1;
                const tShort = Math.min(
                  e.rx <= e.ry ? tOf(e.x - e.rx, e.y) : tOf(e.x, e.y - e.ry),
                  e.rx <= e.ry ? tOf(e.x + e.rx, e.y) : tOf(e.x, e.y + e.ry));
                const tLong = Math.min(
                  e.rx > e.ry ? tOf(e.x - e.rx, e.y) : tOf(e.x, e.y - e.ry),
                  e.rx > e.ry ? tOf(e.x + e.rx, e.y) : tOf(e.x, e.y + e.ry));
                const aShort = alphaAt(m.stops, tShort), aLong = alphaAt(m.stops, tLong);
                if (aShort - aLong >= ALPHA_GAP) {
                  const key = [e.rx, e.ry, m.r1].map((v) => Math.round(v)).join('|');
                  const hit = window.__akGradientClip.find((z) => z.key === key);
                  if (hit) { hit.n++; } else {
                    window.__akGradientClip.push({
                      key: key, n: 1,
                      rx: +e.rx.toFixed(1), ry: +e.ry.toFixed(1),
                      r1: +m.r1.toFixed(1),
                      t_short: +tShort.toFixed(3), t_long: +tLong.toFixed(3),
                      a_short: +aShort.toFixed(3), a_long: +aLong.toFixed(3),
                      cx: Math.round(e.x), cy: Math.round(e.y)
                    });
                  }
                }
              }
            }
          }
        }
      } catch (e) {}
      return origFill.apply(this, arguments);
    };
  } catch (e) {}
})();
"""

# --- A DRAWING ROUTINE THAT PAINTED NOTHING (2026-09-01) ---------------------
# Run No.47's slide 07 solved nine analytic shadow tips and drew none of them.
# A clip test asked whether each cast point was left of a surveyed cut and broke
# at s = 0 for every marker, so every wedge was built base-to-base, filled at
# zero length, and the slide's declared focal point was never in the picture.
# render.py, qa.py, dossier_check and bespoke_check all passed it; a pixel critic
# caught it a full review round after it shipped into the first render. It is the
# same family as the 2026-08-25 buried motif and the 2026-08-31 clipped marks:
# the code is right, the picture is wrong, and every instrument was pointed at
# the code. Those two ask whether declared ink SURVIVED. This asks the cheaper,
# earlier question nothing was asking: did the canvas ever have anything to
# survive?
#
# So every fill() is measured. The wrapper accumulates the current path's
# bounding box from the path-building calls, and on fill() records, PER CALL
# SITE, how many fills that site made and how many of them enclosed nothing.
# Degeneracy is affine invariant, so the box is kept in user space and the
# current transform never has to be unwound.
#
# ALL of it in one line: an isolated degenerate fill is ordinary (a mesh
# triangle seen edge on, a bar whose value is zero), and it is a call site whose
# fills ALL painted nothing that means a routine ran for nothing. Measured over
# 22 known-good slides from three decks (out/2026-09-01, runs/2026-08-31,
# examples/demo-deck), 10,999 fills across 155 call sites: exactly ONE
# degenerate fill anywhere, ak3d.js's triangle rasteriser at 1 of 9,216 at that
# site, a ratio of 0.0001 against the 0.8 the gate needs and 1 against the 3.
# The reconstruction of slide 07 hits 9 of 9. qa.py sets the two thresholds.
#
# COST, measured on the 9,386-fill stress slide (examples/demo-deck/slide-04):
# 60 ms of a 280 ms render, all of it the per-fill stack. Error.stackTraceLimit
# is deliberately left alone, because lowering it to 4 saved nothing measurable
# and it would have truncated the page-error stacks this same run collects.
PAINT_HOOK_JS = """
(() => {
  try {
    const rep = window.__akPaint = { fills: 0, sites: {}, site_cap: false };
    const proto = window.CanvasRenderingContext2D && window.CanvasRenderingContext2D.prototype;
    if (!proto) return;
    const SITE_MAX = 400;
    const FLAT = 0.35;              /* under a third of a pixel encloses nothing */
    const boxes = new WeakMap();
    const box = (c) => {
      let b = boxes.get(c);
      if (!b) { b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity, n: 0 }; boxes.set(c, b); }
      return b;
    };
    const pt = (c, x, y) => {
      if (!isFinite(x) || !isFinite(y)) return;
      const b = box(c);
      b.n++;
      if (x < b.x0) b.x0 = x;
      if (x > b.x1) b.x1 = x;
      if (y < b.y0) b.y0 = y;
      if (y > b.y1) b.y1 = y;
    };
    const wrap = (name, fn) => {
      const orig = proto[name];
      if (typeof orig !== 'function') return;
      proto[name] = function () {
        try { fn(this, arguments); } catch (e) {}
        return orig.apply(this, arguments);
      };
    };
    const origBegin = proto.beginPath;
    if (typeof origBegin === 'function') {
      proto.beginPath = function () {
        try { const b = box(this); b.x0 = Infinity; b.y0 = Infinity; b.x1 = -Infinity; b.y1 = -Infinity; b.n = 0; } catch (e) {}
        return origBegin.apply(this, arguments);
      };
    }
    wrap('moveTo', (c, a) => pt(c, a[0], a[1]));
    wrap('lineTo', (c, a) => pt(c, a[0], a[1]));
    wrap('quadraticCurveTo', (c, a) => { pt(c, a[0], a[1]); pt(c, a[2], a[3]); });
    wrap('bezierCurveTo', (c, a) => { pt(c, a[0], a[1]); pt(c, a[2], a[3]); pt(c, a[4], a[5]); });
    wrap('arcTo', (c, a) => { pt(c, a[0], a[1]); pt(c, a[2], a[3]); });
    wrap('rect', (c, a) => { pt(c, a[0], a[1]); pt(c, a[0] + a[2], a[1] + a[3]); });
    wrap('roundRect', (c, a) => { pt(c, a[0], a[1]); pt(c, a[0] + a[2], a[1] + a[3]); });
    wrap('arc', (c, a) => { pt(c, a[0] - a[2], a[1] - a[2]); pt(c, a[0] + a[2], a[1] + a[2]); });
    wrap('ellipse', (c, a) => {
      const r = Math.max(Math.abs(a[2]), Math.abs(a[3]));
      pt(c, a[0] - r, a[1] - r); pt(c, a[0] + r, a[1] + r);
    });
    const origFill = proto.fill;
    if (typeof origFill !== 'function') return;
    proto.fill = function () {
      try {
        rep.fills++;
        /* fill(path2d) draws a path this hook never saw; only the context's
           own current path is measurable here. A string argument is a fill
           rule and is fine. */
        const arg = arguments[0];
        const foreign = (arg && typeof arg === 'object');
        const b = box(this);
        if (!foreign && b.n > 0) {
          let site = '?';
          try { site = ((new Error()).stack.split('\\n')[2] || '?').trim(); } catch (e) {}
          site = site.replace(/^at\\s+/, '').replace(/file:\\/\\/\\S*?([^\\/]+:\\d+:\\d+)/, '$1').slice(0, 160);
          let s = rep.sites[site];
          if (!s) {
            if (Object.keys(rep.sites).length >= SITE_MAX) { rep.site_cap = true; s = null; }
            else s = rep.sites[site] = { n: 0, bad: 0, w: 0, h: 0 };
          }
          if (s) {
            s.n++;
            const w = b.x1 - b.x0, h = b.y1 - b.y0;
            if (Math.min(w, h) < FLAT) {
              s.bad++;
              s.w = Math.round(w * 100) / 100;
              s.h = Math.round(h * 100) / 100;
            }
          }
        }
      } catch (e) {}
      return origFill.apply(this, arguments);
    };
  } catch (e) {}
})();
"""

IN_PAGE_QA_JS = """
() => {
  const W = window.innerWidth, H = window.innerHeight;
  const out = { text_nodes: [], overflow_warnings: [], fonts_missing: [], body_overflow: false };
  const de = document.documentElement, b = document.body;
  // data-breather on <body> declares this slide a deliberate rest beat, which
  // demotes qa.py's frame-balance FAIL to a WARN. Not a free pass: the dossier
  // gate cross-checks that the storyboard actually declared this slide a
  // breather, so the attribute can only ratify a plan, never invent one.
  out.breather = !!(b && b.hasAttribute("data-breather"));
  if (de.scrollWidth > W + 1 || de.scrollHeight > H + 1 ||
      (b && (b.scrollWidth > W + 1 || b.scrollHeight > H + 1))) {
    out.body_overflow = true;
  }
  /* TYPE NOBODY SIZED (2026-08-21). Run No.39's slide 07 set its headline in an
     <h2> that carried position, width, family, weight, tracking and colour and
     NO font-size, on a page that never loaded aktype.js, so AK.fitText was never
     called on it and Chromium's own user-agent rule typeset the deck's display
     line at 1.5em of an unstyled 16px root: 24 px, the same size as the mono
     labels beside it, dissolved to 9.6 px at the 432 px feed width. It passed
     render, qa.py, dossier_check and copy_sync and reached a pixel critic before
     a human noticed. Every existing gate here measures a RENDERED value against
     a threshold or a declaration, and 24 px trips none of them: it clears the
     24 px mobile floor exactly, it collides with nothing, its contrast is
     excellent, and a slide that never calls fitText declares no fit record to
     grade.
     The defect is not the number, it is that NOBODY CHOSE IT. So this records,
     per text element, whether any author font-size applies anywhere on its
     ancestor chain: an inline style (which is what AK.fitText writes), an SVG
     presentation attribute, or any CSS rule in a readable stylesheet whose
     selector matches. When none does, the size came from the UA stylesheet and
     the 16 px initial value alone, and the browser picked the type size for a
     slide in a hand-built deck. qa.py grades it; unreadable stylesheets are
     counted rather than assumed innocent, so the check reports that it could
     not look instead of passing quietly. */
  const _SVG_NS = "http://www.w3.org/2000/svg";
  const _sizedSel = [];
  out.css_unreadable = 0;
  (() => {
    const visit = (rules) => {
      for (const r of rules) {
        if (r.selectorText !== undefined && r.style) {
          try {
            if (r.style.getPropertyValue("font-size")) _sizedSel.push(r.selectorText);
          } catch (e) {}
        }
        let inner = null;
        try { inner = r.cssRules; } catch (e) { inner = null; }
        if (inner) visit(inner);
      }
    };
    for (const sh of Array.from(document.styleSheets)) {
      let rules = null;
      try { rules = sh.cssRules; } catch (e) { rules = null; }
      if (!rules) { out.css_unreadable++; continue; }
      try { visit(rules); } catch (e) { out.css_unreadable++; }
    }
  })();
  const _authorSized = (e) => {
    try { if (e.style && e.style.fontSize) return true; } catch (e2) {}
    if (e.namespaceURI === _SVG_NS && e.hasAttribute && e.hasAttribute("font-size")) return true;
    for (const sel of _sizedSel) {
      try { if (e.matches(sel)) return true; } catch (e2) {}
    }
    return false;
  };
  const _sizedChain = (e) => {
    for (let p = e; p; p = p.parentElement) {
      if (_authorSized(p)) return true;
    }
    return false;
  };
  /* A <br> IS A SPACE, AND textContent DOES NOT KNOW THAT (2026-09-05).
     `el.textContent` concatenates its text nodes with nothing between them, so
     the authored `FOUR CERTIFIED<br>TICKETS.` -- two words a reader sees on two
     lines -- arrives in the record as `FOUR CERTIFIEDTICKETS`. Run No.51's
     slide 09 shipped exactly that and aggregate_check read it as the count FOUR
     asserted over a noun that does not exist, and hard-failed a line that was
     correct on the page. The gate was measuring a string the slide never drew.
     Every reader of this record (aggregate_check's count detector, copy_sync's
     blob, the QA messages) wants the RENDERED reading, so the glue is removed
     at the source rather than worked around one gate at a time.
     `innerText` would do this and much more besides: it is layout-dependent and
     applies text-transform, so an uppercased block would start arriving in a
     case the author never wrote and every downstream string comparison would
     shift under us. This is textContent with one rule added and nothing else
     changed: a <br> contributes a single space. */
  const _flatText = (el) => {
    let s = "";
    const dive = (n) => {
      for (let c = n.firstChild; c; c = c.nextSibling) {
        if (c.nodeType === 3) s += c.nodeValue;
        else if (c.nodeType === 1) {
          if ((c.tagName || "").toUpperCase() === "BR") s += " ";
          else dive(c);
        }
      }
    };
    dive(el);
    return s;
  };
  const seenFam = new Set();
  const recorded = new Map();   // element -> index in out.text_nodes (for ancestry)
  const walk = document.createTreeWalker(document.body || de, NodeFilter.SHOW_ELEMENT);
  let el;
  while ((el = walk.nextNode())) {
    const hasText = Array.from(el.childNodes).some(
      n => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (!hasText) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const txt = _flatText(el).trim().replace(/\\s+/g, " ").slice(0, 80);
    const fs = parseFloat(cs.fontSize);
    const fam = cs.fontFamily.split(",")[0].trim().replace(/["']/g, "");
    // For SVG text the ink is `fill`, not CSS `color`; the fill attribute or
    // computed fill is the real text color the contrast check must use.
    const isSvgText = el.namespaceURI === "http://www.w3.org/2000/svg";
    const inkColor = isSvgText ? (cs.fill || cs.getPropertyValue("fill") || cs.color) : cs.color;
    // Per-line rects of the element's DIRECT text nodes: the collision gate
    // compares line boxes, not block bboxes (block bboxes overlap on
    // whitespace and false-positive). SVG text keeps its bbox (single-line
    // labels; Range rects are unreliable in SVG).
    let lines = [];
    if (!isSvgText) {
      try {
        const range = document.createRange();
        for (const n of el.childNodes) {
          if (n.nodeType === 3 && n.textContent.trim().length > 0) {
            range.selectNodeContents(n);
            for (const lr of range.getClientRects()) {
              if (lr.width > 1 && lr.height > 1)
                lines.push([Math.round(lr.x), Math.round(lr.y),
                            Math.round(lr.width), Math.round(lr.height)]);
            }
          }
        }
      } catch (e) {}
    }
    const linesMeasured = lines.length > 0;
    if (!lines.length) lines = [[Math.round(r.x), Math.round(r.y),
                                 Math.round(r.width), Math.round(r.height)]];
    // WRAP DRIFT (2026-09-02). An author who writes <br> has DECLARED the line
    // structure of a block, and canvas furniture is routinely counted off that
    // declaration. Run No.48's slide 07 stamped four fields into a 330px plate
    // and placed four markers at py + 42 + f*39; the stamp then wrapped to five
    // rendered lines, every marker slid up one row, and the field deliberately
    // left unstruck (which is how the deck DRAWS "the ordinance carries no
    // fiscal analysis", C06/C31) landed on AMENDABLE . NO. The slide argued the
    // inverse of its own claims and every machine gate passed it, because
    // nothing anywhere compared the authored line count to the rendered one.
    // Record both. Only when the element's element-children are ALL <br> (a
    // <span> would not be reached by the Range walk above, so its lines would
    // undercount and the comparison would be meaningless), and only when the
    // per-line rects were genuinely measured rather than falling back to bbox.
    // A line break is DECLARED two ways in this house: a <br>, or a real
    // newline under a white-space that preserves it (slide 07's spec plate is
    // white-space:pre). Both are counted; anything else (a <span>, an inline
    // <b>) makes the Range walk above undercount, so the block is skipped
    // rather than measured wrong.
    let wrap = null;
    {
      let brs = 0, otherKids = 0;
      for (const k of el.children) {
        if ((k.tagName || "").toUpperCase() === "BR") brs++; else otherKids++;
      }
      const keepsNL = ["pre", "pre-wrap", "pre-line", "break-spaces"]
                        .includes(cs.whiteSpace);
      let authored = 0, cur = "";
      const flush = () => { if (cur.trim().length) authored++; cur = ""; };
      for (const n of el.childNodes) {
        if (n.nodeType === 1 && (n.tagName || "").toUpperCase() === "BR") {
          flush();
        } else if (n.nodeType === 3 && keepsNL) {
          const parts = (n.textContent || "").split("\\n");
          cur += parts[0];
          for (let q = 1; q < parts.length; q++) { flush(); cur = parts[q]; }
        } else {
          cur += n.textContent || "";
        }
      }
      flush();
      if (otherKids === 0 && linesMeasured && authored > 1) {
        wrap = { authored: authored, rendered: lines.length };
      }
    }
    // recorded ancestors, so nested text elements are never compared
    const anc = [];
    for (let p = el.parentElement; p; p = p.parentElement) {
      if (recorded.has(p)) anc.push(recorded.get(p));
    }
    // EVERY TEXT NODE, NOT THE FIRST 80 CHARACTERS OF THEIR JOIN (2026-08-16).
    // `text` above is the element's whole textContent squeezed onto one line
    // and cut at 80 chars, which is right for a QA message and wrong as the
    // record of what was drawn: run No.35's slide 09 set three fact lines in
    // one div with <br>s, the third line began past character 80, and
    // copy_sync_check could not see it at all and reported a FAIL on copy that
    // was on the page. The run split the div into three elements to get past
    // it. Better markup, but the reporting hole stayed open.
    // So record each DIRECT child text node separately (a <br>-separated block
    // is several of them), 200 chars each, 12 nodes max. Nothing downstream
    // that reads `text` changes; readers that need the whole string read
    // `texts`.
    const texts = [];
    for (const n of el.childNodes) {
      if (n.nodeType !== 3) continue;
      const t = n.textContent.trim().replace(/\\s+/g, " ");
      if (t.length && texts.length < 12) texts.push(t.slice(0, 200));
    }
    // THE WHOLE STRING, ONCE, WITH ITS SPANS IN IT (2026-08-27). Neither field
    // above is the string a reader sees. `text` is the whole node cut at 80
    // characters and `texts` is the DIRECT text children only, so a <span>
    // wrapping a unit is dropped from it. Run No.42 built copy.json off this
    // record twice and lost both ways: four bodies pasted in at exactly 80
    // characters, then four labels rebuilt from `texts` as "1 DOT = 0.1OF
    // SILVER IODIDE", the gram gone with its span. copy_sync_check passed both
    // times, because a truncated string IS present in the render and the
    // shredded one matched the space-join of the same `texts` it came from.
    // `full` is the element's whole one-line textContent at 400 characters:
    // the string to copy, and the string a sync check can compare against.
    const node = {
      text: txt,
      texts: texts,
      full: _flatText(el).trim().replace(/\\s+/g, " ").slice(0, 400),
      tag: (el.tagName || "").toLowerCase(),
      // TYPE NOBODY SIZED (2026-08-21): true when no author font-size applies
      // anywhere on this element's ancestor chain, so the UA stylesheet chose
      // the size. See the _sizedChain block above.
      unsized: !_sizedChain(el),
      x: Math.round(r.x), y: Math.round(r.y),
      w: Math.round(r.width), h: Math.round(r.height),
      font_px: Math.round(fs * 10) / 10,
      weight: cs.fontWeight,
      family: fam,
      color: inkColor,
      decorative: el.hasAttribute("data-decorative") ||
                  (el.closest && !!el.closest("[data-decorative]")),
      overlap_ok: el.hasAttribute("data-overlap-ok") ||
                  (el.closest && !!el.closest("[data-overlap-ok]")),
      lines: lines,
      wrap: wrap,
      anc: anc
    };
    recorded.set(el, out.text_nodes.length);
    out.text_nodes.push(node);
    if (!node.decorative) {
      if (r.x < -1 || r.y < -1 || r.right > W + 1 || r.bottom > H + 1) {
        out.overflow_warnings.push({ kind: "offscreen", text: txt,
          detail: `bbox ${Math.round(r.x)},${Math.round(r.y)} ${Math.round(r.width)}x${Math.round(r.height)} vs ${W}x${H}` });
      }
      if (el.scrollWidth > el.clientWidth + 2 && ["hidden","clip"].includes(cs.overflowX)) {
        out.overflow_warnings.push({ kind: "clipped-x", text: txt,
          detail: `scrollWidth ${el.scrollWidth} > clientWidth ${el.clientWidth}` });
      }
      if (el.scrollHeight > el.clientHeight + 2 && ["hidden","clip"].includes(cs.overflowY)) {
        out.overflow_warnings.push({ kind: "clipped-y", text: txt,
          detail: `scrollHeight ${el.scrollHeight} > clientHeight ${el.clientHeight}` });
      }
      if (fs < 24) {
        out.overflow_warnings.push({ kind: "tiny-text", text: txt,
          detail: `font-size ${fs}px < 24px mobile floor (mark data-decorative if intentional)` });
      }
    }
    // Probe the FACE ACTUALLY USED: include the computed font-style so an
    // italic-only display face (e.g. Instrument Serif italic, the SOFT voice)
    // is checked against its italic @font-face instead of a hardcoded
    // upright-400 that false-FAILs even when the used face is loaded
    // (2026-07-13 fix; the upright probe had forced hidden offscreen
    // upright-loader spans as a hack). Normalize "oblique 14deg" -> "oblique"
    // to keep the shorthand parseable, and key seenFam on style too so upright
    // AND italic of one family are each probed rather than deduped together.
    const styl = /^(italic|oblique)/.test(cs.fontStyle) ? cs.fontStyle.split(" ")[0] : "normal";
    const fkey = fam + "|" + cs.fontWeight + "|" + styl;
    if (!["serif","sans-serif","monospace","system-ui","cursive","fantasy"].includes(fam) &&
        !seenFam.has(fkey)) {
      seenFam.add(fkey);
      let spec = styl + " " + cs.fontWeight + " 32px \\"" + fam + "\\"";
      try {
        if (!document.fonts.check(spec)) out.fonts_missing.push({ family: fam, weight: cs.fontWeight, style: styl });
      } catch (e) {}
    }
  }
  /* TEXT OCCLUDED BY AN OPAQUE PLATE (2026-07-26). qa.py's text_collisions()
     compares GLYPH LINE BOXES only, so an opaque element's BACKGROUND is
     invisible to it: a padded plate can paint over the bottom third of a
     subtitle while every line-box pair stays under the 30% overlap ratio.
     That is exactly how the 2026-07-26 S06 and S02 hard fails (a DEAD plate
     over a subtitle; a note column run 62px past a callout plate) shipped
     past machine QA reporting zero fails and zero warns, twice.

     For each recorded text node, intersect its line boxes with every OPAQUE
     element box that is neither an ancestor nor a descendant of it, then
     confirm PAINT ORDER with elementFromPoint (a temporary
     pointer-events:auto sheet lets the hit test see decorative layers;
     pointer-events never affects pixels, and the sheet is removed before the
     screenshot). If the text paints ABOVE the plate the hit test returns the
     text and nothing is reported, so knockout plates and chips-on-plates stay
     legal. Deliberately conservative: canvas/SVG ink, blended layers, sub-0.9
     alpha and full-bleed ground planes are NOT treated as occluders, so the
     check only speaks when something opaque provably covers type. */
  const _alpha = (col) => {
    const m = /rgba?\(([^)]+)\)/.exec(col || "");
    if (!m) return 0;
    const p = m[1].split(",").map(parseFloat);
    return p.length > 3 ? p[3] : 1;
  };
  const peSheet = document.createElement("style");
  peSheet.textContent = "*{pointer-events:auto !important}";
  (document.head || de).appendChild(peSheet);
  try {
    const solids = [];
    for (const e of document.querySelectorAll("body *")) {
      if (e.namespaceURI === "http://www.w3.org/2000/svg") continue;
      const t = e.tagName;
      if (t === "CANVAS" || t === "SVG" || t === "SCRIPT" || t === "STYLE") continue;
      const cs3 = getComputedStyle(e);
      if (cs3.display === "none" || cs3.visibility === "hidden") continue;
      if (parseFloat(cs3.opacity) < 0.9) continue;
      if (cs3.mixBlendMode && cs3.mixBlendMode !== "normal") continue;
      const solid = _alpha(cs3.backgroundColor) >= 0.9 ||
                    (cs3.backgroundImage && cs3.backgroundImage !== "none") ||
                    t === "IMG";
      if (!solid) continue;
      const rr = e.getBoundingClientRect();
      if (rr.width < 4 || rr.height < 4) continue;
      if (rr.width >= W - 1 && rr.height >= H - 1) continue;  // full-bleed ground plane
      solids.push([e, rr]);
    }
    for (const [tel, idx] of recorded) {
      const tn = out.text_nodes[idx];
      let worst = null;
      for (const [se, sr] of solids) {
        if (se === tel || se.contains(tel) || tel.contains(se)) continue;
        for (const ln of tn.lines) {
          const ix = Math.min(ln[0] + ln[2], sr.right) - Math.max(ln[0], sr.left);
          const iy = Math.min(ln[1] + ln[3], sr.bottom) - Math.max(ln[1], sr.top);
          if (ix < 2 || iy < 2) continue;
          if (worst && ix * iy <= worst._px) continue;
          const x0 = Math.max(ln[0], sr.left), y0 = Math.max(ln[1], sr.top);
          let hits = 0, tries = 0;
          for (const fx of [0.2, 0.5, 0.8]) for (const fy of [0.3, 0.7]) {
            tries++;
            // elementsFromPoint returns the whole stack, TOPMOST FIRST. Compare
            // the plate's depth against the text's: a full-frame grain/edge
            // overlay sits above both and must not decide the answer, which
            // singular elementFromPoint would let it do.
            const stack = document.elementsFromPoint(x0 + ix * fx, y0 + iy * fy);
            let si = -1, ti = -1;
            for (let k = 0; k < stack.length; k++) {
              const nd = stack[k];
              if (si < 0 && (nd === se || se.contains(nd))) si = k;
              if (ti < 0 && (nd === tel || tel.contains(nd))) ti = k;
            }
            if (si >= 0 && (ti < 0 || si < ti)) hits++;
          }
          if (hits * 2 < tries) continue;   // the text paints above the plate: legible
          worst = {
            _px: ix * iy, w: Math.round(ix), h: Math.round(iy),
            frac: Math.round(1000 * (ix * iy) / Math.max(1, ln[2] * ln[3])) / 1000,
            by: (se.getAttribute("class") || se.id || se.tagName).slice(0, 40),
            by_text: (se.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40)
          };
        }
      }
      if (worst) { delete worst._px; tn.occluded = worst; }
    }
  } catch (e) {
    // never fail the render over the probe itself; surface it as a console
    // error, which render.py records and qa.py reports as a WARN.
    try { console.error("text-occlusion probe threw: " + e); } catch (e2) {}
  } finally {
    peSheet.remove();
  }
  /* SVG KNOCKOUT PLATES (2026-07-29). A <rect> painted before a <text> in the
     same <svg>, overlapping it, is that label's knockout plate, and the label
     must sit fully inside it. NOTHING in this file could see that before: SVG
     text has no line boxes (the Range path above is DOM-only), the plate is a
     SIBLING rather than an ancestor, and the occlusion probe hit-tests DOM
     text only. Run 2026-07-29 shipped six labels hanging off their own plates
     through two scoring cycles with machine_qa reporting 0 fails, including a
     chip border rule drawn straight through the 'T' of 'PERMITS'. The root
     cause is arithmetic: JetBrains Mono at 24px with 0.10em tracking advances
     16.8px per character, and the plate widths were hand-sized at roughly 14.
     Measure containment here; qa.py grades it. */
  out.svg_plates = [];
  for (const sv of document.querySelectorAll('svg')) {
    const kids = Array.from(sv.querySelectorAll('text, rect'));
    for (let i = 0; i < kids.length; i++) {
      const t = kids[i];
      if (t.tagName.toLowerCase() !== 'text') continue;
      if (!t.textContent.trim()) continue;
      const tb = t.getBoundingClientRect();
      if (tb.width < 1 || tb.height < 1) continue;
      let plate = null;
      for (let j = 0; j < i; j++) {
        const r = kids[j];
        if (r.tagName.toLowerCase() !== 'rect') continue;
        const rb = r.getBoundingClientRect();
        if (rb.width < 1 || rb.height < 1) continue;
        if (tb.left < rb.right && tb.right > rb.left &&
            tb.top < rb.bottom && tb.bottom > rb.top) plate = rb;
      }
      /* The mirror case, and the one that bit this run twice: a rect painted
         AFTER the text, overlapping it, is painting OVER the label. SVG has no
         z-index, only document order, so a plate appended for the block below
         silently eats the descender of the line above. The DOM occlusion probe
         cannot see it (elementsFromPoint reports the <svg>, not the <rect>). */
      let covered = null;
      for (let j = i + 1; j < kids.length; j++) {
        const r = kids[j];
        if (r.tagName.toLowerCase() !== 'rect') continue;
        const f = (r.getAttribute('fill') || '').trim();
        if (!f || f === 'none') continue;
        const m = f.match(/rgba?\(([^)]+)\)/);
        const alpha = m ? (parseFloat(m[1].split(',')[3]) || 1) : 1;
        if (alpha * (parseFloat(r.getAttribute('fill-opacity')) || 1) < 0.5) continue;
        const rb = r.getBoundingClientRect();
        const ox = Math.min(tb.right, rb.right) - Math.max(tb.left, rb.left);
        const oy = Math.min(tb.bottom, rb.bottom) - Math.max(tb.top, rb.top);
        if (ox > 1 && oy > 1) {
          const area = ox * oy;
          if (!covered || area > covered.area) covered = { area: area, w: Math.round(ox), h: Math.round(oy) };
        }
      }
      /* And the third way to bury an SVG label: a DOM element painted above
         the whole <svg>. The furniture layer is one positioned element, so a
         knockout-plated body div declared after it in the document eats any
         guard line it happens to overlap, with no SVG-level evidence at all.
         Ask the compositor what is actually on top of the label's own box. */
      let domHit = 0, domN = 0;
      const cy = (tb.top + tb.bottom) / 2;
      if (cy >= 0 && cy <= H) {
        for (let s = 0; s <= 10; s++) {
          const px = tb.left + (tb.width * s) / 10;
          if (px < 0 || px > W) continue;
          domN++;
          for (const e of document.elementsFromPoint(px, cy)) {
            if (e === sv || e.contains(sv)) break;
            if (e === t || sv.contains(e)) continue;
            const bg = getComputedStyle(e).backgroundColor || '';
            const mm = bg.match(/rgba?\(([^)]+)\)/);
            const a2 = mm ? (parseFloat(mm[1].split(',')[3]) || 1) : 0;
            if (a2 >= 0.5) { domHit++; break; }
          }
        }
      }
      const domFrac = domN ? domHit / domN : 0;
      if (covered || domFrac > 0.15) {
        out.svg_plates.push({
          text: t.textContent.trim().slice(0, 60),
          covered_px: covered ? [covered.w, covered.h] : null,
          dom_cover_frac: Math.round(domFrac * 100) / 100,
          overrun_px: 0, over: { left: 0, right: 0, top: 0, bottom: 0 },
          decorative: t.hasAttribute('data-decorative'),
          overlap_ok: t.hasAttribute('data-overlap-ok')
        });
      }
      if (!plate) continue;
      const over = {
        left: Math.round(plate.left - tb.left), right: Math.round(tb.right - plate.right),
        top: Math.round(plate.top - tb.top), bottom: Math.round(tb.bottom - plate.bottom)
      };
      const worst = Math.max(over.left, over.right, over.top, over.bottom);
      if (worst > 0) {
        out.svg_plates.push({
          text: t.textContent.trim().slice(0, 60), overrun_px: worst, over: over,
          decorative: t.hasAttribute('data-decorative'),
          overlap_ok: t.hasAttribute('data-overlap-ok')
        });
      }
    }
  }

  /* DECLARED ENCODINGS (2026-07-29). A slide may state, in machine-readable
     form, what its artwork is supposed to SAY without words:

       <body data-encodes='[{"claim":"material change at hour 7",
                             "reads":"differ",
                             "a":[[732,1052,82,98]], "b":[[736,500,74,540]]}]'>

     `reads` is REQUIRED as of 2026-08-08 and is one of "differ" (the two
     regions must be tellable apart) or "same" (an absence or sameness claim).
     qa.py FAILS a declaration that omits it, and FAILS a "differ" whose two
     regions are under 4.0 dE apart at feed scale. Run No.29 authored two probe
     rectangles from the storyboard's camera arithmetic instead of measuring
     them off a render; they landed on empty water 300px from the aperture,
     reported dE 0.9, and gated nothing. MEASURE THE RECTS OFF THE PNG.

     Every gate before this one judged LEGIBILITY. Nothing judged whether the
     picture carried its own argument, so the only reviewer who ever saw a
     failed encoding was the scorer, at the ship gate, too late to rebuild the
     art. Artwork craft was the weakest criterion in 16 of the first 19 runs.

     Two things are measured, because calibration showed one is not enough.
     Run 2026-07-29's hero declared steel below hour 7 and brass above, and
     the scorer said it read as one uniform amber extrusion. It did not fail
     on colour: where the steel is visible it sits 43 dE from the brass, so a
     pure separability check PASSES the defect it was built to catch. What
     actually failed is PROMINENCE: a knockout plate and the base shadow left
     only 29 percent of the declared steel section as visible art, so the
     material change read as a glassy plinth rather than as half the object.
     Hence art_visible_frac, sampled with elementsFromPoint per region. */
  out.encodings = [];
  try {
    const decl = (document.body && document.body.dataset.encodes) || "";
    const specs = decl ? JSON.parse(decl) : [];
    const rectsOf = (v) => {
      if (typeof v === "string") {
        return Array.from(document.querySelectorAll(v)).map(e => {
          const r = e.getBoundingClientRect();
          return [r.x, r.y, r.width, r.height];
        });
      }
      return (Array.isArray(v) && Array.isArray(v[0])) ? v : [v];
    };
    const visibleFrac = (rects) => {
      let hit = 0, n = 0;
      for (const [rx, ry, rw, rh] of rects) {
        const cols = Math.max(3, Math.min(24, Math.round(rw / 8)));
        const rows = Math.max(3, Math.min(24, Math.round(rh / 8)));
        for (let i = 0; i < cols; i++) {
          for (let j = 0; j < rows; j++) {
            const px = rx + (rw * (i + 0.5)) / cols;
            const py = ry + (rh * (j + 0.5)) / rows;
            if (px < 0 || px > W || py < 0 || py > H) continue;
            n++;
            const stack = document.elementsFromPoint(px, py);
            let blocked = false;
            for (const e of stack) {
              const tag = e.tagName.toLowerCase();
              if (tag === "canvas" || tag === "svg" || tag === "body" || tag === "html") break;
              if (e.namespaceURI === "http://www.w3.org/2000/svg") {
                // art drawn as SVG shapes is still the artwork, but an opaque
                // knockout rect is furniture
                const f = (e.getAttribute("fill") || "").trim();
                const m = f.match(/rgba?\(([^)]+)\)/);
                const al = m ? (parseFloat(m[1].split(",")[3]) || 1) : (f && f !== "none" ? 1 : 0);
                if (al >= 0.5 && tag === "rect") { blocked = true; break; }
                continue;
              }
              const bg = getComputedStyle(e).backgroundColor || "";
              const mm = bg.match(/rgba?\(([^)]+)\)/);
              const a2 = mm ? (parseFloat(mm[1].split(",")[3]) || 1) : 0;
              if (a2 >= 0.5) { blocked = true; break; }
            }
            if (!blocked) hit++;
          }
        }
      }
      return n ? hit / n : 0;
    };
    for (const sp of specs) {
      const ra = rectsOf(sp.a), rb = rectsOf(sp.b);
      out.encodings.push({
        claim: String(sp.claim || "").slice(0, 90),
        reads: sp.reads || "any",
        a: ra.map(r => r.map(Math.round)), b: rb.map(r => r.map(Math.round)),
        a_visible_frac: Math.round(visibleFrac(ra) * 100) / 100,
        b_visible_frac: Math.round(visibleFrac(rb) * 100) / 100
      });
    }
  } catch (e) {
    out.encodings.push({ error: String(e).slice(0, 140) });
  }

  /* DECLARED CONTACT SHADOWS (2026-08-05). A shadow is a SUBTRACTION and it
     needs something to subtract FROM. Run No.26 declared the contact corollary
     as its attack, built the two-part shadow exactly as specified in #1A0F08
     at alpha 0.55, and laid it on a table already rendering near #0B0906. The
     composite is a 1.2 L* change. FOUR pixel critics independently returned
     contact_edge_reads: no, the scorer called three of nine slides
     "floating-adjacent", and qa.py passed the deck with zero fails, because
     every gate in it judges legibility, collision or balance and none of them
     asks whether a declared depth cue survived compositing.

     A slide states, in machine-readable form, where its contact shadow is and
     what ground it is supposed to darken:

       <body data-contacts='[{"what":"the shut block on the table",
                              "shadow":[[236,1178,608,26]],
                              "ground":[[236,1246,608,26]]}]'>

     Rects are [x,y,w,h] in design px, a list of rects or a single rect, or a
     CSS selector resolved by getBoundingClientRect (same grammar as
     data-encodes). qa.py measures median L* of each region at feed scale and
     FAILs when the shadow is not meaningfully darker than its own ground.

     Unlike the encoding probe there is no elementsFromPoint pass here: a
     contact shadow is CANVAS PAINT, so occlusion by type is a legitimate
     composition and the only question is what the pixels do. */
  out.contacts = [];
  try {
    const cdecl = (document.body && document.body.dataset.contacts) || "";
    const cspecs = cdecl ? JSON.parse(cdecl) : [];
    const rectsOf2 = (v) => {
      if (typeof v === "string") {
        return Array.from(document.querySelectorAll(v)).map(e => {
          const r = e.getBoundingClientRect();
          return [r.x, r.y, r.width, r.height];
        });
      }
      return (Array.isArray(v) && Array.isArray(v[0])) ? v : [v];
    };
    for (const sp of cspecs) {
      out.contacts.push({
        what: String(sp.what || "").slice(0, 90),
        shadow: rectsOf2(sp.shadow).map(r => r.map(Math.round)),
        ground: rectsOf2(sp.ground).map(r => r.map(Math.round))
      });
    }
  } catch (e) {
    out.contacts.push({ error: String(e).slice(0, 140) });
  }

  /* THE AXIS CENSUS (2026-08-16). A MARK DRAWN ALONG A MEASURED AXIS IS READ
     AS A QUANTITY, whatever the author meant by it. Run No.35 did it twice in
     one deck and every machine gate passed both: slide 07 put three gold place
     ticks under a rail whose x axis means DOLLARS, so three REGIONS were
     printed at three dollar positions; slide 02 put thirteen division ticks on
     a money rail, implying twelve equal months over a budget period that is
     ten months long. Two pixel critics found them by reading; nothing
     mechanical could, because nothing in the run ever wrote down that the axis
     was quantitative or what the marks on it were.

     A slide with a measured axis now says so, and enumerates what sits on it:

       <body data-scale='[{"what":"the award rail","axis":"x","unit":"dollars",
                           "from":[150,0],"to":[930,272174856],
                           "band":[1120,1180],
                           "marks":[{"at":312,"means":"Kodiak, $4.6M"},
                                    {"at":688,"means":"the October close"}]}]'>

     `from`/`to` are [design px, value] on that axis, `band` is the strip the
     scale owns perpendicular to it, and every mark drawn inside that strip is
     listed with what it means. qa.py checks the arithmetic (a mark off its own
     span, a mark that means nothing) and takes a PIXEL CENSUS of the band,
     calibrated on the marks the slide admits to, so a tick nobody declared is
     found and printed with the value its position reads as. */
  out.scales = [];
  try {
    const sdecl = (document.body && document.body.dataset.scale) || "";
    const sspecs = sdecl ? JSON.parse(sdecl) : [];
    for (const sp of sspecs) {
      out.scales.push({
        what: String(sp.what || "").slice(0, 90),
        axis: String(sp.axis || "x").toLowerCase().slice(0, 1),
        unit: String(sp.unit || "").slice(0, 40),
        from: Array.isArray(sp.from) ? sp.from.slice(0, 2) : null,
        to: Array.isArray(sp.to) ? sp.to.slice(0, 2) : null,
        band: Array.isArray(sp.band) ? sp.band.slice(0, 2).map(Math.round) : null,
        marks: (Array.isArray(sp.marks) ? sp.marks : []).slice(0, 60).map(m => ({
          at: (m && typeof m.at === "number") ? Math.round(m.at) : null,
          means: (m && typeof m.means === "string") ? m.means.trim().slice(0, 90) : ""
        }))
      });
    }
  } catch (e) {
    out.scales.push({ error: String(e).slice(0, 140) });
  }

  /* A DECLARATION ON THE WRONG SURFACE (2026-08-27). The engine reads some
     declarations off the BODY as data attributes (data-scale, data-contacts,
     data-encodes) and others off WINDOW GLOBALS (__akAssert, __akMotifs,
     __akLeaders, __akFit). Nothing enforced which was which, so run No.42
     declared three measured axes as `window.__akScale`, generalising from the
     three globals beside it. The axis pixel census never ran on slides 02, 06
     and 07 and the row still read PASS, because an absent declaration is
     indistinguishable from a slide that has no axis. Converting the three
     immediately surfaced two undeclared marks on the hero, one of them a
     terrain crest drawn fifty metres above the datum it was measured from.
     A gate that is silently off is worse than one never written.

     So the near misses are enumerated on both surfaces, in both directions,
     with the singular/plural variant of each name. This looks only for the
     names the engine ALREADY OWNS on the OTHER surface: an unrelated global
     (a slide's own __akHero, __akProbes, __akStats) is not the machine's
     business and is never reported. qa.py FAILs on anything found here. */
  out.declaration_misses = [];
  try {
    const BODY_CONTRACTS = { contacts: "data-contacts", scale: "data-scale",
                             encodes: "data-encodes" };
    const GLOBAL_CONTRACTS = ["__akAssert", "__akMotifs", "__akLeaders", "__akFit"];
    const variants = (s) => (s.slice(-1) === "s" ? [s, s.slice(0, -1)] : [s, s + "s"]);
    const ds = (document.body && document.body.dataset) || {};
    for (const key of Object.keys(BODY_CONTRACTS)) {
      const pascal = "__ak" + key.charAt(0).toUpperCase() + key.slice(1);
      for (const g of variants(pascal)) {
        if (typeof window[g] !== "undefined" && window[g] !== null) {
          out.declaration_misses.push({
            found: "window." + g, want: BODY_CONTRACTS[key],
            how: "a body attribute, JSON in single quotes on <body>" });
        }
      }
    }
    for (const g of GLOBAL_CONTRACTS) {
      const key = g.slice(4, 5).toLowerCase() + g.slice(5);
      for (const k of variants(key)) {
        if (typeof ds[k] !== "undefined") {
          out.declaration_misses.push({
            found: "data-" + k.toLowerCase(), want: "window." + g,
            how: "a window global, assigned in the slide's own script" });
        }
      }
    }
  } catch (e) {
    out.declaration_misses.push({ error: String(e).slice(0, 140) });
  }

  /* CANVAS TELEMETRY (2026-07-11, the rendered-3D gates): per visible canvas,
     backing resolution vs CSS size (silent-1x detector) and a downsampled
     pixel sample (dead/black-frame detector: a GL context that failed or
     never painted screenshots as uniform ink). GL canvases need
     preserveDrawingBuffer (akthree sets it) for drawImage sampling; when
     sampling fails we report sample_ok:false rather than guessing. */
  out.canvases = [];
  for (const cv of document.querySelectorAll('canvas')) {
    const cs2 = getComputedStyle(cv);
    if (cs2.display === 'none' || cs2.visibility === 'hidden') continue;
    const r2 = cv.getBoundingClientRect();
    if (r2.width < 8 || r2.height < 8) continue;
    const entry = {
      x: Math.round(r2.x), y: Math.round(r2.y),
      w: Math.round(r2.width), h: Math.round(r2.height),
      bw: cv.width, bh: cv.height,
      area_frac: Math.round(1000 * Math.min(1,
        (Math.min(r2.width, W) * Math.min(r2.height, H)) / (W * H))) / 1000,
      backing_ratio: Math.round(100 * Math.min(cv.width / Math.max(1, r2.width),
                                               cv.height / Math.max(1, r2.height))) / 100,
      sample_ok: false, mean: -1, variance: -1
    };
    try {
      const sw = 48, sh = Math.max(8, Math.round(48 * r2.height / r2.width));
      const t = document.createElement('canvas');
      t.width = sw; t.height = sh;
      const tc = t.getContext('2d', { willReadFrequently: true });
      tc.drawImage(cv, 0, 0, sw, sh);
      const px = tc.getImageData(0, 0, sw, sh).data;
      let sum = 0, sum2 = 0, n = sw * sh;
      for (let i = 0; i < px.length; i += 4) {
        const v = (px[i] + px[i + 1] + px[i + 2]) / 3;
        sum += v; sum2 += v * v;
      }
      entry.mean = Math.round(sum / n * 10) / 10;
      entry.variance = Math.round((sum2 / n - (sum / n) * (sum / n)) * 10) / 10;
      entry.sample_ok = true;
    } catch (e) {}
    out.canvases.push(entry);
  }
  /* CANVAS TEXT (2026-07-19): deduped list of strings drawn via fillText/
     strokeText, captured by the add_init_script hook before slide scripts ran.
     qa.py WARNs on the meaningful ones (raster text ships in the vector PDF and
     is invisible to the ranker/copy_sync/a11y). Only present if the hook ran. */
  out.canvas_text = [];
  try {
    const seen = new Set();
    for (const e of (window.__akCanvasText || [])) {
      if (seen.has(e.text)) continue;
      seen.add(e.text);
      out.canvas_text.push(e);
    }
  } catch (e) {}
  /* EMPTY PAINTS (2026-09-01): the call sites whose fill() calls enclosed
     nothing, collected from PAINT_HOOK_JS. Only sites with at least one
     degenerate fill are carried out, capped, worst ratio first; qa.py holds the
     thresholds and does the judging. */
  out.paint = { fills: 0, sites: 0, site_cap: false, empty: [] };
  try {
    const pr = window.__akPaint;
    if (pr && pr.sites) {
      const names = Object.keys(pr.sites);
      out.paint.fills = pr.fills;
      out.paint.sites = names.length;
      out.paint.site_cap = !!pr.site_cap;
      out.paint.empty = names.filter((k) => pr.sites[k].bad > 0)
        .map((k) => ({ site: k, n: pr.sites[k].n, bad: pr.sites[k].bad,
                       w: pr.sites[k].w, h: pr.sites[k].h }))
        .sort((a, b) => (b.bad / b.n) - (a.bad / a.n) || b.bad - a.bad)
        .slice(0, 12);
    }
  } catch (e) {}

  /* ANNOTATION LEADERS (2026-08-07). A leader line that stops in open field
     looks exactly like a leader reaching something small, which is why run
     No.28's slide 06 shipped two detail-circle leaders pointing at void through
     TWO pixel critics and a flow critic: the tails were fixed pixel deltas from
     each circle's own centre (tail:[-70,-70,-150,-150]), so no reviewer and no
     gate could tell what they were supposed to arrive at. Pixels cannot answer
     it either (the leader's own landing tick puts ink at the terminus), so the
     slide DECLARES the arithmetic instead: for every drafting leader, where it
     ends and where the feature it points at actually is. qa.py then checks the
     two agree. Opt-in by construction -- a slide with no leaders declares
     nothing -- but SKILL.md makes the declaration part of the slide contract
     for any leader, callout or detail-circle annotation.

       window.__akLeaders = [{ target: '2024 sliver dimension line',
                               at: [BX + 2, 838],       // the FEATURE's own coords
                               to: [BX + 2, 838],       // where the leader ends
                               from: [420, 948],        // where it meets its LABEL
                               label: 'ONE TICK PER DAY' }];  // that label, verbatim

     BOTH ENDS, ADDED 2026-08-14. The 2026-08-07 contract checked the TARGET end
     only, so a leader could land perfectly on its feature and run back into bare
     sheet at the other end, carrying no value at all. Run No.33 shipped three of
     them and the scorer found all three by reading, S01's leader off the Rhode
     Island ring, S07's dimension call printing none of the values its own type
     spec declared, and S08's stamp leader descending into nothing. Every machine
     gate passed the deck at zero fails. A leader is a sentence with two ends,
     a feature and the words about it, so the declaration now names both and
     qa.py checks that the label was really drawn and really sits where the
     leader arrives. The authoring is again the point, you can't write `label`
     without having written the label.
  */
  out.leaders = [];
  try {
    const pt = (v) => Array.isArray(v) && v.length === 2 &&
      v.every((n) => typeof n === "number" && isFinite(n))
        ? [Math.round(v[0] * 10) / 10, Math.round(v[1] * 10) / 10] : null;
    for (const e of (Array.isArray(window.__akLeaders) ? window.__akLeaders : []).slice(0, 60)) {
      out.leaders.push({
        target: (e && typeof e.target === "string" && e.target.trim())
          ? e.target.trim().slice(0, 90) : null,
        to: pt(e && e.to),
        at: pt(e && e.at),
        from: pt(e && e.from),
        label: (e && typeof e.label === "string" && e.label.trim())
          ? e.label.trim().replace(/\\s+/g, " ").slice(0, 90) : null
      });
    }
  } catch (e) {}

  /* TEXT FITS (2026-08-12). AK.fitText records every call it was asked to make
     -- the declared {min, max, maxLines} and what the element actually rendered
     -- on window.__akFit. Collect it verbatim; qa.py grades it. A slide that
     never calls fitText reports an empty list and is never judged here. */
  out.fits = [];
  try {
    for (const f of (Array.isArray(window.__akFit) ? window.__akFit : []).slice(0, 200)) {
      out.fits.push(f);
    }
  } catch (e) {}

  /* SELF-ASSERTED MEASUREMENTS (2026-08-12). Run No.31's slide 05 printed an
     840px dimension that was exact to the pixel over a scene whose two masses
     were 266px apart, so the deck's one load-bearing measurement, twenty feet,
     was drawn as about six -- and every gate passed it, because every gate here
     judges legibility, collision, composition or a declared colour/depth
     relationship, and none of them can know what a printed number is supposed
     to mean. The same run printed two frame widths as typed constants that were
     wrong by 7 and 25 percent against the projections that actually drew the
     maps. Both are the same defect: a NUMBER IN TYPE and the GEOMETRY IT NAMES
     computed independently, in a slide where only one of them is measurable.

     The run also found the answer by accident. Slide 07 wrote its ISOTYPE count
     to window.__akMarkCount and console.error'd on a mismatch; that caught 189,
     then 196, before landing on an exact 200 -- but only because a human was
     reading the console, since a console.error is a WARN here. Generalise it and
     make it a FAIL:

       window.__akAssert = [{ what: "the 20 ft lock, printed as an 840px rule",
                              expect: 840,          // what the type/label claims
                              actual: 20 * FT_PX,   // what the drawing computed
                              tol: 2, unit: "px" }];

     Opt-in, same as the leader and encoding contracts, and the work it does is
     in the authoring: you cannot write `actual` without deriving it from the
     thing that actually drew, which is the step every one of these defects
     skipped. Pure arithmetic on two numbers the slide supplied, so it can never
     false-positive on art the machine does not understand. */
  /* A HOOK THAT IS A COUNT MUST SURVIVE BEING COUNTED (2026-08-25). Run No.40's
     cover printed 750 and drew 24 rows of 30, because row 0's centre sat 20px
     past the bottom edge of the canvas and never painted. Every machine gate
     passed the slide; a pixel critic counted the rows by hand. The 2026-08-12
     assertion contract could not see it either, since a slide that derives
     `actual` from its own loop bound gets 750 from arithmetic that never asks
     where the marks landed.

     So an assertion whose subject is a COUNT declares the marks themselves,
     and the frame does the counting:

       window.__akAssert = [{ what: "750 funded devices, one mark each",
                              expect: 750, points: pts, unit: "marks" }];

     `points` is the array of mark centres IN DESIGN PX that the drawing loop
     actually used (pass the same array to the drawing code; deriving both from
     one list is the whole point). `actual` becomes the number of those centres
     inside the frame, `tol` defaults to 0 because a count is exact, and any
     hand-written `actual` is ignored and reported so the author sees it. */
  /* ... AND COUNTED IN THE PICTURE, NOT ONLY IN THE ARRAY (2026-08-31). Run
     No.46's slide 03 declared eight proud leaves for the FCC's eight
     consecutive AI questions, drew eight, and SHIPPED SIX: the body copy's
     type reserve is applied as an evenodd clip, so the two leftmost leaves
     were never painted. The count above reported 8 of 8 the whole time,
     because "inside the frame" is arithmetic on the declared array and a
     clip erases ink without moving a coordinate. Every machine gate stayed
     green; a human found it by cropping the render and counting by eye.

     So the centres themselves are carried out to qa.py, which samples each
     one on the COMPOSITED png and asks whether a mark is still there. Only
     the centres are exported (the measuring lives in qa.py beside every other
     pixel instrument, on one implementation of _ink_spread rather than a
     second one written in JS), capped and evenly strided so a 750-mark
     census costs a bounded amount of report. */
  /* ... AND A COUNT THAT MEANS EXTENT SAYS SO (2026-09-04). Run No.50's slide
     08 lit 31 of 72 grid cells to stand for 31 sections of two townships whose
     LOCATION is not public, under a label reading EXTENT ONLY. NO BOUNDARY IS
     DRAWN. The build shuffled the 72 cells and took the first 31; they landed
     edge to edge in one township, so the frame drew a parcel with holes in it
     seventy pixels under that label. The count contract reported 31 of 31 and
     every gate was green, because the gate asked HOW MANY and the failure was
     about WHERE. Five pixel critics scored the slide 2.5.

       window.__akAssert = [{ what: "31 of 72 sections, extent only",
                              expect: 31, points: pts, dispersed: true,
                              unit: "marks" }];

     `dispersed: true` is the slide stating that these marks are a scatter
     standing for an extent rather than a drawn shape, and qa.py measures it on
     the same centres (marks_disperse). Opt-in, like everything else here: a
     rank, a row of tally marks and a bar are all legitimately contiguous and
     never carry the flag. */
  const MARK_PROBE_MAX = 240;
  out.asserts = [];
  try {
    const num = (v) => (typeof v === "number" && isFinite(v)) ? v : null;
    for (const a of (Array.isArray(window.__akAssert) ? window.__akAssert : []).slice(0, 60)) {
      const rec = {
        what: (a && typeof a.what === "string" && a.what.trim())
          ? a.what.trim().slice(0, 90) : null,
        expect: num(a && a.expect),
        actual: num(a && a.actual),
        tol: num(a && a.tol),
        unit: (a && typeof a.unit === "string") ? a.unit.trim().slice(0, 16) : "",
        /* A COUNT THAT CLAIMS EXTENT DECLARES IT (2026-09-04). `dispersed:true`
           on a `points` assertion says the marks are a SCATTER standing for an
           extent, not a drawn shape, and qa.py measures that off the same
           centres. See marks_disperse() there for why counting cannot see it. */
        dispersed: !!(a && a.dispersed === true)
      };
      const pts = (a && Array.isArray(a.points)) ? a.points.slice(0, 20000) : null;
      if (pts) {
        let inside = 0, n = 0, bad = 0;
        const xy = [];
        for (const p of pts) {
          const x = Array.isArray(p) ? +p[0] : (p && typeof p === "object" ? +p.x : NaN);
          const y = Array.isArray(p) ? +p[1] : (p && typeof p === "object" ? +p.y : NaN);
          if (!isFinite(x) || !isFinite(y)) { bad++; continue; }
          n++;
          if (x >= 0 && x <= W && y >= 0 && y <= H) {
            inside++;
            xy.push([Math.round(x * 10) / 10, Math.round(y * 10) / 10]);
          }
        }
        rec.points_n = n;
        rec.points_bad = bad;
        rec.offframe = n - inside;
        rec.actual_declared = rec.actual;
        rec.actual = inside;
        if (rec.tol === null) rec.tol = 0;
        /* the centres qa.py will probe: every one when there are few, and an
           even stride through them when there are many, so the sample stays
           spread over the whole field rather than over its first corner. */
        if (xy.length <= MARK_PROBE_MAX) {
          rec.points_xy = xy;
          rec.points_xy_stride = 1;
        } else {
          const step = Math.ceil(xy.length / MARK_PROBE_MAX);
          const s = [];
          for (let i = 0; i < xy.length; i += step) s.push(xy[i]);
          rec.points_xy = s;
          rec.points_xy_stride = step;
        }
      }
      out.asserts.push(rec);
    }
  } catch (e) {}

  /* DOM PAINTS OVER CANVAS (2026-08-25). Run No.40 lost THREE declared motifs
     across three slides and every machine gate stayed green on all three: the
     continuity cell was drawn correctly on slide 07 and then covered by a
     `.lane` plate, drawn on slide 03 and covered by a `.guard` plate, and on
     slide 06 painted out by the channel's own void fill on the very next
     drawing operation. Each time the CODE was right and the PICTURE was empty,
     and twice a repair note claimed the element was visible when nothing was
     on the slide at all. qa.py's "text under an opaque plate" and "label
     crossed by art" checks both look at TEXT; nothing looked at declared ART
     that a plate had buried.

     A slide names a drawn feature and the rect it occupies:

       window.__akMotifs = [{ what: "cell 0016, the continuity stencil",
                              rect: [812, 214, 96, 96] }];   // design px
                              // optional: canvas: "canvas.plate"

     What is recorded here is the evidence, not the verdict. For each motif:
       - `grid`, a small RGB grid read back OUT OF THE CANVAS ITSELF at that
         rect (the ink the slide's own drawing code actually left behind), and
       - `visible_frac` / `blocker`, an elementsFromPoint census of the same
         rect naming the topmost opaque DOM element standing on it.
     qa.py samples the SAME rect out of the composited PNG and compares: ink in
     the canvas and none on the page is a burial, and no ink in the canvas at
     all is a motif that was painted out or never drawn. The comparison is a
     RATIO between two measurements of one slide, so it needs no absolute ink
     threshold and no knowledge of what the motif depicts.

     LIMIT: the canvas readback is mapped through the element's bounding box,
     so a CSS-ROTATED canvas reports the wrong region (the axis-aligned bbox).
     Declare `canvas` explicitly or leave the motif undeclared in that case;
     the DOM census and the PNG side stay valid either way. */
  out.motifs = [];
  try {
    const MOTIF_CELL = 2;      // design px per grid cell, before clamping
    const MOTIF_GRID_MAX = 30; // cells per side (bounds the report size)
    const decl = (Array.isArray(window.__akMotifs) ? window.__akMotifs : []).slice(0, 8);
    const label = (el) => {
      if (!el || !el.tagName) return null;
      const t = el.tagName.toLowerCase();
      const id = el.id ? "#" + el.id : "";
      const cl = (typeof el.className === "string" && el.className.trim())
        ? "." + el.className.trim().split(/\\s+/)[0] : "";
      return (t + id + cl).slice(0, 60);
    };
    for (const m of decl) {
      const r = (m && Array.isArray(m.rect) && m.rect.length === 4 &&
                 m.rect.every((n) => typeof n === "number" && isFinite(n)))
        ? m.rect.map(Number) : null;
      const e = {
        what: (m && typeof m.what === "string" && m.what.trim())
          ? m.what.trim().slice(0, 90) : null,
        rect: r ? r.map(Math.round) : null,
        canvas: null, grid: null, gw: 0, gh: 0,
        visible_frac: null, blocker: null
      };
      if (!e.what || !r || r[2] < 3 || r[3] < 3) {
        e.error = "a motif declares {what, rect:[x,y,w,h]} in design px, w/h >= 3";
        out.motifs.push(e);
        continue;
      }
      const [mx, my, mw, mh] = r;
      /* the canvas the motif was drawn on: an explicit selector, else the
         LAST canvas in document order whose box contains the rect (last =
         painted on top of its siblings) */
      let cv = null;
      if (m.canvas && typeof m.canvas === "string") {
        cv = document.querySelector(m.canvas);
      } else {
        for (const c of document.querySelectorAll("canvas")) {
          const b2 = c.getBoundingClientRect();
          if (b2.width < 8 || b2.height < 8) continue;
          if (mx >= b2.x - 1 && my >= b2.y - 1 &&
              mx + mw <= b2.x + b2.width + 1 && my + mh <= b2.y + b2.height + 1) cv = c;
        }
      }
      /* THE DOM CENSUS: what stands on this rect, and how much of it */
      let hit = 0, n = 0;
      const blockers = {};
      const cols = Math.max(3, Math.min(16, Math.round(mw / 6)));
      const rows = Math.max(3, Math.min(16, Math.round(mh / 6)));
      for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
          const px = mx + (mw * (i + 0.5)) / cols;
          const py = my + (mh * (j + 0.5)) / rows;
          if (px < 0 || px > W || py < 0 || py > H) continue;
          n++;
          let blocked = null;
          for (const el of document.elementsFromPoint(px, py)) {
            if (cv && el === cv) break;
            const tag = el.tagName.toLowerCase();
            if (!cv && (tag === "canvas" || tag === "svg")) break;
            if (tag === "body" || tag === "html") break;
            if (el.namespaceURI === "http://www.w3.org/2000/svg") {
              const f = (el.getAttribute("fill") || "").trim();
              const mm0 = f.match(/rgba?\\(([^)]+)\\)/);
              const al = mm0 ? (parseFloat(mm0[1].split(",")[3]) || 1)
                             : (f && f !== "none" ? 1 : 0);
              if (al >= 0.5 && tag === "rect") { blocked = el; break; }
              continue;
            }
            const cs3 = getComputedStyle(el);
            const mm = (cs3.backgroundColor || "").match(/rgba?\\(([^)]+)\\)/);
            const a2 = mm ? (parseFloat(mm[1].split(",")[3]) || 1) : 0;
            if (a2 >= 0.5 && parseFloat(cs3.opacity || "1") >= 0.5) { blocked = el; break; }
          }
          if (blocked) {
            const k = label(blocked) || "?";
            blockers[k] = (blockers[k] || 0) + 1;
          } else hit++;
        }
      }
      if (n) {
        e.visible_frac = Math.round((hit / n) * 100) / 100;
        let best = null;
        for (const k in blockers) if (!best || blockers[k] > blockers[best]) best = k;
        e.blocker = best;
      }
      /* THE CANVAS READBACK: the ink the drawing code actually left */
      if (cv) {
        e.canvas = label(cv);
        try {
          const b3 = cv.getBoundingClientRect();
          const kx = cv.width / Math.max(1, b3.width), ky = cv.height / Math.max(1, b3.height);
          const sx = (mx - b3.x) * kx, sy = (my - b3.y) * ky;
          const sw = mw * kx, sh = mh * ky;
          const gw = Math.max(3, Math.min(MOTIF_GRID_MAX, Math.round(mw / MOTIF_CELL)));
          const gh = Math.max(3, Math.min(MOTIF_GRID_MAX, Math.round(mh / MOTIF_CELL)));
          const t = document.createElement("canvas");
          t.width = gw; t.height = gh;
          const tc = t.getContext("2d", { willReadFrequently: true });
          tc.imageSmoothingEnabled = true;
          tc.drawImage(cv, sx, sy, sw, sh, 0, 0, gw, gh);
          const px2 = tc.getImageData(0, 0, gw, gh).data;
          const g = [];
          for (let i = 0; i < px2.length; i += 4) g.push(px2[i], px2[i + 1], px2[i + 2]);
          e.grid = g; e.gw = gw; e.gh = gh;
        } catch (e2) {
          e.error = "canvas readback failed (" + String(e2).slice(0, 60) + ")";
        }
      }
      out.motifs.push(e);
    }
  } catch (e) {
    out.motifs.push({ error: String(e).slice(0, 140) });
  }
  /* Circular ramps poured into ellipses, collected by GRADIENT_CLIP_HOOK_JS
     while the slide drew. qa.py grades them. */
  out.gradient_clips = (Array.isArray(window.__akGradientClip)
                        ? window.__akGradientClip : []).slice(0, 40);
  return out;
}
"""


def _can_read_disk(browser):
    """Can this browser fetch() a committed asset over file://?

    The one capability the slide contract depends on and the one a headless
    shell silently lacks. Returns (ok, why). Any error at all is a "no": the
    point is to prefer a browser that demonstrably works, and a probe that
    cannot answer has not demonstrated anything.
    """
    target = REPO_ROOT / "assets" / "geo" / "alaska-state.geo.json"
    if not target.exists():
        cands = sorted((REPO_ROOT / "assets" / "geo").glob("*.json"))
        if not cands:
            return True, "no committed geodata to probe with"
        target = cands[0]
    page = None
    tmp = None
    try:
        tmp = Path(tempfile.mkdtemp(prefix="ak-fileprobe-"))
        probe = tmp / "probe.html"
        probe.write_text(
            "<!doctype html><meta charset=utf-8><script>window.__akProbe="
            "fetch(%r).then(r=>r.ok?'ok':'http '+r.status)"
            ".catch(e=>'fetch blocked: '+e.message);</script>" % target.as_uri())
        page = browser.new_page()
        page.goto(probe.as_uri(), wait_until="load", timeout=15000)
        verdict = page.evaluate("() => window.__akProbe")
        return (verdict == "ok"), str(verdict)
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, str(e)[:120])
    finally:
        try:
            if page is not None:
                page.close()
        except Exception:
            pass
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)


def launch_chromium(p):
    """Launch chromium, preferring the FULL browser over the headless shell.

    THE FULL BINARY FIRST, AND THE ORDER IS THE WHOLE FIX (2026-08-27).
    Playwright's default channel is `chrome-headless-shell`, and a recent shell
    (151.0.7922.34, pulled into this container as chromium_headless_shell-1234)
    refuses `fetch()` of a `file://` URL even with
    `--allow-file-access-from-files`, which the full Chromium still honours.
    Measured side by side on the same machine, same flags, same target file:
    full chromium returned the 29 borough features, the shell returned
    "Failed to fetch".

    That single difference silently breaks every slide that reads committed
    geodata, which is the house's own signature move: the SKILL contract
    documents `fetch("@@ASSETS@@/geo/alaska-state.geo.json")` as the way to get
    a map onto a slide, and examples/demo-deck/slide-02 does exactly that. On
    run No.42 the demo deck itself failed to render for this reason, so the
    reference deck the engine ships as its own proof was broken by a browser
    upgrade nothing in the repo asked for.

    The old code tried the default first and only fell back on a launch
    EXCEPTION, so a shell that launches perfectly well and then quietly cannot
    read the disk was never reached by the fallback. Preferring the full binary
    costs nothing when both are present and keeps working when only one is.

    THE ORDER IS NOT ENOUGH ON ITS OWN; PROBE THE CAPABILITY (2026-09-02).
    Playwright 1.57 stopped shipping Chromium and now manages Chrome for
    Testing, headed as `chrome` and headless as `chrome-headless-shell`
    (playwright.dev/docs/release-notes). Two things follow for this repo. The
    binary layout changes, so a glob written for `chromium-*/chrome-linux` can
    stop matching after a container refresh; and when it stops matching, the
    fallback below hands back whatever the default channel is, which since 1.57
    is the shell -- the exact binary that cannot read the disk. That failure is
    SILENT: the browser launches, the page loads, every gate is green, and only
    the geodata is missing.

    Measured on this machine, same flags, same target, 2026-09-02:
      chromium-1194 141.0.7390.37 chrome-linux/chrome         -> fetch OK
      chromium_headless_shell-1194 141.0.7390.37 headless_shell -> Failed to fetch

    So a candidate is not accepted because it launched. It is accepted because
    it launched AND fetched a real committed asset over file://. One extra page
    load per render invocation, roughly 200 ms, once. If NOTHING passes the
    probe the first launchable browser is used anyway with a loud warning,
    because a deck missing one map still beats no deck at all; the run is told
    what it is getting either way.
    """
    pats = ["/opt/pw-browsers/chromium-*/chrome-linux/chrome",
            # Chrome for Testing layouts, for after the 1.57 rename lands here
            "/opt/pw-browsers/chrome-*/chrome-linux64/chrome",
            "/opt/pw-browsers/chrome-*/chrome-linux/chrome"]
    candidates = []
    for pat in pats:
        candidates += sorted(glob.glob(pat))
    candidates += ["/opt/pw-browsers/chromium/chrome-linux/chrome", "/opt/pw-browsers/chromium"]
    fallback = None
    for c in candidates:
        if not Path(c).exists():
            continue
        try:
            b = p.chromium.launch(executable_path=c, args=CHROMIUM_ARGS)
        except Exception:
            continue
        ok, why = _can_read_disk(b)
        if ok:
            return b
        if fallback is None:
            fallback = (b, c, why)
        else:
            b.close()
    if fallback is not None:
        b, c, why = fallback
        print("WARN: %s launches but cannot fetch() a file:// asset (%s). Slides "
              "that read committed geodata will render without their maps. Using "
              "it anyway because a deck beats no deck; if a map is missing, this "
              "is why." % (c, why), file=sys.stderr)
        return b
    try:
        b = p.chromium.launch(args=CHROMIUM_ARGS)
    except Exception as exc:
        raise RuntimeError(
            "No launchable Chromium found (tried /opt/pw-browsers then the "
            "playwright default)") from exc
    ok, why = _can_read_disk(b)
    if not ok:
        print("WARN: the playwright default channel cannot fetch() a file:// "
              "asset (%s), which is what chrome-headless-shell does. Slides that "
              "read committed geodata will render without their maps." % why,
              file=sys.stderr)
    return b


# --- DETERMINISM SOURCE SCAN (2026-08-01) -----------------------------------
# SKILL.md's slide contract says "seed all noise (AK.reseed / AK.rng), derive
# the seed from the run date, same inputs must reproduce the same pixels", and
# nothing enforced it. On 2026-08-01 a stipple field shipped through five
# render rounds on Math.random() and was caught by a human running grep, on a
# deck whose subject was a public RECORD. An unseeded field cannot be
# re-rendered: a repair pass on slide 9 silently repaints every dot, so a pixel
# critic's note about one label stops describing the file it was written
# against, and the shipped PNG can never be reproduced from the committed HTML.
#
# The scan reads the slide SOURCE (this is a source-level contract, and the
# defect is invisible in a single screenshot), and only inside INLINE <script>
# blocks: vendored libraries under assets/js are loaded by src= and are not
# read, and a deck that PRINTS the string "Math.random" as body copy is DOM
# text, not script, so it never trips. Comments and their contents are stripped
# before matching.
#   HARD (qa.py FAIL): unseeded randomness. There is no legitimate use of it in
#     a slide; AK.rng(seed) is the drop-in replacement and takes one argument.
#   SOFT (qa.py WARN): clock reads. Usually a timing log, occasionally an
#     animation phase that does feed pixels; the author decides, the machine
#     just refuses to let it pass unseen.
NONDET_HARD = [
    ("Math.random()", re.compile(r"\bMath\s*\.\s*random\s*\(")),
    ("crypto.getRandomValues()", re.compile(r"\bcrypto\s*\.\s*getRandomValues\s*\(")),
    ("crypto.randomUUID()", re.compile(r"\bcrypto\s*\.\s*randomUUID\s*\(")),
]
NONDET_SOFT = [
    ("Date.now()", re.compile(r"\bDate\s*\.\s*now\s*\(")),
    ("new Date()", re.compile(r"\bnew\s+Date\s*\(\s*\)")),
    ("performance.now()", re.compile(r"\bperformance\s*\.\s*now\s*\(")),
]
SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script\s*>", re.S | re.I)
JS_TYPE_OK = ("", "text/javascript", "application/javascript", "module")


def _strip_js_comments(js: str) -> str:
    """Blank out // and /* */ comments, preserving length so offsets survive."""
    out = list(js)
    i, n = 0, len(js)
    while i < n:
        two = js[i:i + 2]
        if two == "//":
            j = js.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        elif two == "/*":
            j = js.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if js[k] != "\n":
                    out[k] = " "
            i = j
        else:
            i += 1
    return "".join(out)


def scan_nondeterminism(html: str, name: str) -> list:
    """Report unseeded-randomness / clock reads in a slide's inline scripts."""
    hits = []
    for m in SCRIPT_RE.finditer(html):
        attrs, body = m.group(1), m.group(2)
        if re.search(r"\bsrc\s*=", attrs, re.I):
            continue                      # external file: vendored, not ours
        tm = re.search(r"""\btype\s*=\s*["']?([^"'\s>]*)""", attrs, re.I)
        if tm and tm.group(1).strip().lower() not in JS_TYPE_OK:
            continue                      # text/template, application/json, ...
        body_start = m.start(2)
        clean = _strip_js_comments(body)
        for tier, table in (("hard", NONDET_HARD), ("soft", NONDET_SOFT)):
            for api, rx in table:
                for hit in rx.finditer(clean):
                    off = body_start + hit.start()
                    line = html.count("\n", 0, off) + 1
                    src_line = html.splitlines()[line - 1].strip()
                    hits.append({"tier": tier, "api": api, "line": line,
                                 "snippet": src_line[:120]})
    hits.sort(key=lambda h: (h["line"], h["api"]))
    if hits:
        print(f"    [determinism] {name}: "
              + ", ".join(f"{h['api']} line {h['line']}" for h in hits))
    return hits


# --- A PROJECTION FITTED TO A COLLAPSED BOX (2026-08-30) --------------------
# d3's fitExtent/fitSize PRESERVE ASPECT: they fit the SMALLER of the two
# dimensions and centre on the other. So fitting to a box one pixel tall does
# not produce a full-width band, it produces a one-pixel-tall picture, and the
# call succeeds silently. On run No.45 slide 08 declared a full-width grazing
# seam with .fitExtent([[110,0],[980,1]], mainland) and rendered a 27px sliver.
# It cost a hard fail and a whole review round, and nothing in the machine could
# see it: the render is not blank, the projection is valid, and the defect only
# exists relative to an intent that lives in the dossier.
#
# A literal box with a dimension under 8px is never what anyone meant -- there
# is no map, chart or inset that small -- so this is decidable from the source
# alone, with no threshold on taste. Only fully LITERAL boxes are read, so a box
# built from variables is not guessed at; that trades false negatives for the
# certainty that a hit is real. AKGeo.fitAxis() is the supported way to say
# "span this axis exactly and let the other fall where it falls", which is what
# a one-axis projection actually wants.
COLLAPSE_MIN = 8.0
_NUM = r"(-?\d+(?:\.\d+)?)"
FIT_EXTENT_RE = re.compile(
    r"\bfitExtent\s*\(\s*\[\s*\[\s*" + _NUM + r"\s*,\s*" + _NUM +
    r"\s*\]\s*,\s*\[\s*" + _NUM + r"\s*,\s*" + _NUM + r"\s*\]\s*\]")
FIT_SIZE_RE = re.compile(
    r"\bfitSize\s*\(\s*\[\s*" + _NUM + r"\s*,\s*" + _NUM + r"\s*\]")


def scan_collapsed_fit(html: str, name: str) -> list:
    """Report projections fitted to a box with a degenerate dimension."""
    hits = []
    for m in SCRIPT_RE.finditer(html):
        attrs, body = m.group(1), m.group(2)
        if re.search(r"\bsrc\s*=", attrs, re.I):
            continue
        tm = re.search(r"""\btype\s*=\s*["']?([^"'\s>]*)""", attrs, re.I)
        if tm and tm.group(1).strip().lower() not in JS_TYPE_OK:
            continue
        body_start = m.start(2)
        clean = _strip_js_comments(body)
        for api, rx in (("fitExtent", FIT_EXTENT_RE), ("fitSize", FIT_SIZE_RE)):
            for hit in rx.finditer(clean):
                g = [float(v) for v in hit.groups()]
                w, h = (abs(g[2] - g[0]), abs(g[3] - g[1])) if len(g) == 4 else (abs(g[0]), abs(g[1]))
                if min(w, h) >= COLLAPSE_MIN:
                    continue
                off = body_start + hit.start()
                line = html.count("\n", 0, off) + 1
                hits.append({"api": api, "line": line, "w": round(w, 1),
                             "h": round(h, 1), "axis": "height" if h < w else "width",
                             "snippet": html.splitlines()[line - 1].strip()[:120]})
    hits.sort(key=lambda h: h["line"])
    if hits:
        print(f"    [projection] {name}: "
              + ", ".join(f"{h['api']} box {h['w']}x{h['h']} line {h['line']}" for h in hits))
    return hits


# --- AN ASSERTION THAT CANNOT FAIL (2026-09-01) -----------------------------
# The 2026-08-12 __akAssert contract exists so a number printed in type and the
# geometry it names are compared by the machine instead of by eye, and its whole
# value is in the AUTHORING: "you cannot write `actual` without deriving it from
# the thing that actually drew". Nothing enforced that half. Run No.47's slide 08
# printed that two stamped tags carry the same seven struck rows, built the two
# tags SEPARATELY in 3D, shipped nine rows on one and eight on the other at
# different insets, and declared
#
#     window.__akAssert=[{what:"both tags carry the same seven struck rows",
#                         expect:7, actual:7, tol:0, unit:"rows"}];
#
# which passes for any picture whatsoever. The same run's slide 05 wrote
# `expect:+sidePx.toFixed(2), actual:+sidePx.toFixed(2)`, the same variable on
# both sides. Both read as green in render_report and in machine_qa; a pixel
# critic found the tags by reading the source beside the render.
#
# Two shapes, both decidable from the source with no threshold and no taste:
#   - `actual` is textually IDENTICAL to `expect` (same literal, same variable,
#     same call). x == x is not a measurement.
#   - `actual` is a bare numeric literal. A literal was typed by the author, so
#     it cannot have come from the drawing, which is the one thing this contract
#     asks of it.
# An assertion carrying `points` (the 2026-08-25 count contract) has its `actual`
# computed by the frame and is never read here.
#
# Measured before it was wired in, over the 16 assertions in the four slide sets
# on disk (out/2026-09-01, runs/2026-08-31, runs/2026-08-08, examples/demo-deck):
# 7 carry a hand-written `actual`, 5 of them derived (750-96, dx(139)-dx(49),
# Math.round(window.__G[2]) ...) and silent here, and exactly the 2 above fire.
# Deliberately NOT flagged, and left as SKILL.md guidance instead: an `actual`
# folded out of literals (`actual:750-96`), which is weak but does at least name
# the drawing's own numbers, and which fires on 2 of 7 known-good assertions.
VACUOUS_NUM_RE = re.compile(r"^[+-]?\s*(?:\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\.\d+)$")


def _js_obj_spans(clean: str, start: int):
    """Yield (s, e) for each top-level {...} in the array literal after `start`."""
    i = clean.find("[", start)
    if i < 0:
        return
    depth, obj_start, j, n = 0, None, 0, len(clean)
    j = i
    while j < n:
        c = clean[j]
        if c in "\"'`":
            q = c
            j += 1
            while j < n and clean[j] != q:
                if clean[j] == "\\":
                    j += 1
                j += 1
        elif c == "{":
            if depth == 0:
                obj_start = j
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and obj_start is not None:
                yield obj_start, j + 1
                obj_start = None
        elif c == "]" and depth == 0:
            return
        j += 1


def _js_obj_value(obj: str, key: str):
    """The SOURCE TEXT of `key`'s value in one object literal, whitespace
    normalised, or None when the key is absent."""
    m = re.search(r"[{,]\s*%s\s*:" % key, obj)
    if not m:
        return None
    j, n, depth, out = m.end(), len(obj), 0, []
    while j < n:
        c = obj[j]
        if c in "\"'`":
            q = c
            out.append(c)
            j += 1
            while j < n and obj[j] != q:
                out.append(obj[j])
                if obj[j] == "\\":
                    j += 1
                    out.append(obj[j])
                j += 1
            out.append(q)
        elif c in "([{":
            depth += 1
            out.append(c)
        elif c in ")]}":
            if depth == 0:
                break
            depth -= 1
            out.append(c)
        elif c == "," and depth == 0:
            break
        else:
            out.append(c)
        j += 1
    return " ".join("".join(out).split())


def scan_vacuous_asserts(html: str, name: str) -> list:
    """Report __akAssert entries whose `actual` cannot disagree with `expect`."""
    hits = []
    for m in SCRIPT_RE.finditer(html):
        attrs, body = m.group(1), m.group(2)
        if re.search(r"\bsrc\s*=", attrs, re.I):
            continue
        tm = re.search(r"""\btype\s*=\s*["']?([^"'\s>]*)""", attrs, re.I)
        if tm and tm.group(1).strip().lower() not in JS_TYPE_OK:
            continue
        body_start = m.start(2)
        clean = _strip_js_comments(body)
        for am in re.finditer(r"__akAssert\s*=", clean):
            for s, e in _js_obj_spans(clean, am.end()):
                obj = clean[s:e]
                if _js_obj_value(obj, "points") is not None:
                    continue          # the frame computes `actual` for a count
                actual = _js_obj_value(obj, "actual")
                if actual is None:
                    continue
                expect = _js_obj_value(obj, "expect")
                if expect is not None and actual == expect:
                    why = "same expression on both sides"
                elif VACUOUS_NUM_RE.match(actual):
                    why = "`actual` is a typed literal, not a measurement"
                else:
                    continue
                what = _js_obj_value(obj, "what") or ""
                hits.append({"why": why, "what": what.strip("\"'")[:90],
                             "expect": (expect or "")[:60], "actual": actual[:60],
                             "line": html.count("\n", 0, body_start + s) + 1})
    hits.sort(key=lambda h: h["line"])
    if hits:
        print(f"    [assert] {name}: "
              + ", ".join(f"vacuous at line {h['line']} ({h['why']})" for h in hits))
    return hits


def resolve_html(src: Path, resolved_dir: Path) -> Path:
    html = src.read_text()
    if re.search(r'src\s*=\s*["\']https?://|href\s*=\s*["\']https?://|url\(\s*["\']?https?://', html):
        raise ValueError(f"{src.name}: external http(s) reference found. Slides must be fully offline.")
    html = html.replace("@@ASSETS@@", ASSETS_DIR.as_uri())
    dst = resolved_dir / src.name
    dst.write_text(html)
    return dst


def source_sha1(p: Path) -> str:
    """Fingerprint the slide SOURCE that produced a PNG (2026-08-14).

    Run No.33 applied two projection-note repairs to source and then re-rendered
    a DIFFERENT slide subset, so both edits were silent no-ops and the flow
    critic reviewed a contact sheet that predated them and reported both repairs
    as still broken. `--only` is a sharp tool and nothing anywhere in the
    pipeline could tell a PNG that matched its source from one that did not.
    Recording the source hash next to the PNG makes that answerable by
    arithmetic, and qa.py FAILs on a mismatch, so a stale render can no longer
    reach a reviewer wearing a fresh render's verdict.
    """
    return hashlib.sha1(p.read_bytes()).hexdigest()


# --- THE CANVAS LAYER, ON ITS OWN (2026-08-30) ------------------------------
# Every collision check in qa.py that can see canvas ink reads the COMPOSITED
# screenshot, where the DOM text is painted on top of the art. That forces each
# of them to mask the glyph ink off before it can say anything about the art,
# and masking is lossy: it eats the pixels immediately around every stroke,
# which is exactly where a mark crossing a line of type lives. On 2026-08-30 a
# registration crosshair sat on top of slide 04's display headline and a row of
# register ticks ran through the last line of slide 08's body copy; machine QA
# reported 9/9 PASS with zero warns on both, and a human critic caught them.
#
# This exports the canvas layer BY ITSELF: every visible canvas composited, in
# DOM order, at its own place in the design frame, with nothing from the DOM on
# top. qa.py then measures a text line box against art that is not hiding under
# type, which is a measurement the composited PNG structurally cannot offer.
#
# Exported at DESIGN resolution, not the 2x backing store: the smallest mark
# this is meant to catch is a hairline rule, which is >= 1px in design space,
# and a 1080x1350 layer of mostly flat paper costs a few hundred KB instead of
# a few MB. Alpha is preserved, so "no canvas ink here" stays distinguishable
# from "canvas ink the colour of paper".
#
# Honesty over coverage: a canvas under a CSS rotation, a CSS filter or a blend
# mode cannot be re-composited faithfully from its bounding box, so the layer
# is marked approximate and qa.py declines to judge it rather than measuring a
# misregistered picture and calling the answer a FAIL.
CANVAS_LAYER_JS = r"""
(dim) => {
  const W = dim[0], H = dim[1];
  const t = document.createElement('canvas');
  t.width = W; t.height = H;
  const tc = t.getContext('2d', { willReadFrequently: true });
  let n = 0, approx = [];
  for (const cv of document.querySelectorAll('canvas')) {
    const cs = getComputedStyle(cv);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const op = parseFloat(cs.opacity);
    if (!(op > 0.02)) continue;
    const r = cv.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) continue;
    // A bounding box only reproduces the canvas's real placement when the
    // element is un-rotated, un-skewed, un-filtered and normally blended.
    const tr = cs.transform || 'none';
    if (tr !== 'none') {
      const m = tr.match(/^matrix\(([^)]*)\)$/);
      const p = m ? m[1].split(',').map(Number) : null;
      if (!p || Math.abs(p[1]) > 1e-3 || Math.abs(p[2]) > 1e-3) approx.push('transform');
    }
    if ((cs.filter || 'none') !== 'none') approx.push('filter');
    const bl = cs.mixBlendMode || 'normal';
    if (bl !== 'normal') approx.push('mix-blend-mode');
    try {
      tc.save();
      tc.globalAlpha = isFinite(op) ? op : 1;
      tc.drawImage(cv, r.x, r.y, r.width, r.height);
      tc.restore();
      n++;
    } catch (e) {
      return { ok: false, canvases: n, error: String(e).slice(0, 140) };
    }
  }
  if (!n) return { ok: true, canvases: 0, data: null };
  let data = null;
  try { data = t.toDataURL('image/png'); }
  catch (e) { return { ok: false, canvases: n, error: String(e).slice(0, 140) }; }
  return { ok: true, canvases: n, approx: Array.from(new Set(approx)), data: data };
}
"""


def render_slide(browser, path: Path, out_png: Path, width: int, height: int,
                 scale: float, timeout_ms: int) -> dict:
    rec = {"file": path.name, "png": out_png.name, "console_errors": [], "page_errors": [],
           "overflow_warnings": [], "fonts_missing": [], "text_nodes": [],
           "body_overflow": False, "canvas_text": [], "svg_plates": [],
           "encodings": [], "contacts": [], "scales": [], "nondeterminism": [],
           "collapsed_fits": [], "vacuous_asserts": [],
           "paint": {"fills": 0, "sites": 0, "empty": []},
           "fits": [], "asserts": [], "motifs": [], "css_unreadable": 0,
           "gradient_clips": [], "declaration_misses": [],
           "canvas_layer": {"ok": False, "reason": "not attempted"},
           "render_ms": 0, "ok": False}
    t0 = time.time()
    page = browser.new_page(viewport={"width": width, "height": height},
                            device_scale_factor=scale)
    page.add_init_script(CANVAS_TEXT_HOOK_JS)
    page.add_init_script(GRADIENT_CLIP_HOOK_JS)
    page.add_init_script(PAINT_HOOK_JS)
    page.on("console", lambda m: rec["console_errors"].append(m.text)
            if m.type in ("error",) else None)
    page.on("pageerror", lambda e: rec["page_errors"].append(str(e)))
    try:
        page.goto(path.as_uri(), wait_until="load", timeout=timeout_ms)
        page.evaluate("() => document.fonts.ready.then(() => true)")
        has_ready = page.evaluate("() => typeof window.renderReady !== 'undefined'")
        if has_ready:
            page.evaluate("() => Promise.race([window.renderReady, "
                          "new Promise((_, rej) => setTimeout(() => rej('renderReady timeout'), 30000))])")
        else:
            page.wait_for_timeout(400)
        qa = page.evaluate(IN_PAGE_QA_JS)
        rec.update({k: qa[k] for k in ("text_nodes", "overflow_warnings",
                                       "fonts_missing", "body_overflow", "canvases",
                                       "canvas_text", "breather", "svg_plates",
                                       "encodings", "contacts", "scales", "leaders",
                                       "fits", "asserts", "motifs", "css_unreadable",
                                       "gradient_clips", "declaration_misses",
                                       "paint")})
        page.screenshot(path=str(out_png), clip={"x": 0, "y": 0, "width": width, "height": height})
        rec["ok"] = out_png.exists() and out_png.stat().st_size > 10_000
        # the canvas layer on its own, for qa.py's canvas-over-text check
        try:
            cl = page.evaluate(CANVAS_LAYER_JS, [width, height])
            if not cl.get("ok"):
                rec["canvas_layer"] = {"ok": False, "reason": cl.get("error", "export failed")}
            elif not cl.get("canvases"):
                rec["canvas_layer"] = {"ok": True, "canvases": 0, "file": None}
            else:
                lay = out_png.with_suffix("")
                lay = lay.with_name(lay.name + ".canvas.png")
                head, _, b64 = (cl.get("data") or "").partition(",")
                if not b64 or "image/png" not in head:
                    rec["canvas_layer"] = {"ok": False, "reason": "no png payload"}
                else:
                    lay.write_bytes(base64.b64decode(b64))
                    rec["canvas_layer"] = {
                        "ok": True, "canvases": cl["canvases"], "file": lay.name,
                        "approx": cl.get("approx") or [],
                        "w": width, "h": height,
                    }
        except Exception as e:
            rec["canvas_layer"] = {"ok": False, "reason": f"exception: {e}"[:160]}
        if not rec["ok"]:
            rec["page_errors"].append("screenshot missing or suspiciously small")
    except Exception as e:
        rec["page_errors"].append(f"render exception: {e}")
    finally:
        page.close()
    rec["render_ms"] = int((time.time() - t0) * 1000)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--only", default="", help="comma-separated slide numbers to re-render, e.g. 2,5")
    ap.add_argument("--timeout", type=int, default=45000)
    args = ap.parse_args()

    slides_dir = Path(args.slides_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    resolved_dir = out_dir / ".resolved"
    resolved_dir.mkdir(exist_ok=True)

    slides = sorted(slides_dir.glob("slide-*.html"))
    if not slides:
        print(f"FAIL: no slide-*.html in {slides_dir}", file=sys.stderr)
        sys.exit(1)
    if args.only:
        keep = {int(x) for x in args.only.split(",")}
        slides = [s for s in slides
                  if int(re.search(r"slide-(\d+)", s.name).group(1)) in keep]

    report_path = out_dir / "render_report.json"
    prior = {}
    if report_path.exists():
        try:
            prior = {r["file"]: r for r in json.loads(report_path.read_text())["slides"]}
        except Exception:
            prior = {}

    results = []
    with sync_playwright() as p:
        browser = launch_chromium(p)
        for s in slides:
            resolved = resolve_html(s, resolved_dir)
            png = out_dir / (s.stem + ".png")
            rec = render_slide(browser, resolved, png, args.width, args.height,
                               args.scale, args.timeout)
            rec["nondeterminism"] = scan_nondeterminism(s.read_text(), s.name)
            rec["collapsed_fits"] = scan_collapsed_fit(s.read_text(), s.name)
            rec["vacuous_asserts"] = scan_vacuous_asserts(s.read_text(), s.name)
            rec["source"] = {"path": str(s), "sha1": source_sha1(s)}
            status = "OK " if rec["ok"] and not rec["page_errors"] else "FAIL"
            warn = len(rec["overflow_warnings"])
            print(f"[{status}] {s.name} -> {png.name}  {rec['render_ms']}ms"
                  f"  warnings={warn}  errors={len(rec['page_errors'])}")
            prior[s.name] = rec
            results.append(rec)
        browser.close()
    shutil.rmtree(resolved_dir, ignore_errors=True)

    merged = [prior[k] for k in sorted(prior.keys())]
    report = {
        "canvas": {"width": args.width, "height": args.height, "scale": args.scale,
                   "px": [int(args.width * args.scale), int(args.height * args.scale)]},
        "slides": merged,
    }
    report_path.write_text(json.dumps(report, indent=2))
    print(f"report -> {report_path}")

    # STALE PNGs (2026-08-14). Every record in the merged report names the
    # source that made it and that source's hash. Any slide whose file on disk
    # has moved on since is a PNG that no longer shows what its HTML says, which
    # is what a `--only` subset quietly produces after an edit lands outside the
    # subset. Announced here so the operator sees it at once; qa.py FAILs on it
    # so it can never reach a reviewer or a ship gate unseen.
    stale = []
    for r in merged:
        src = r.get("source") or {}
        sp, sha = src.get("path"), src.get("sha1")
        if not sp or not sha:
            continue
        try:
            if source_sha1(Path(sp)) != sha:
                stale.append(r["file"])
        except OSError:
            continue
    if stale:
        print("STALE: %s changed since its PNG was made. Re-render "
              "(drop --only, or add the slide to it) before any review or gate "
              "reads these images." % ", ".join(stale), file=sys.stderr)

    hard_fail = any((not r["ok"]) or r["page_errors"] or r["body_overflow"] for r in results)
    if hard_fail:
        print("HARD FAIL: at least one slide has render errors or body overflow "
              "(see render_report.json)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
