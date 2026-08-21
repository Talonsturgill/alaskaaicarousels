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
import glob
import hashlib
import json
import re
import shutil
import sys
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
    const txt = el.textContent.trim().replace(/\\s+/g, " ").slice(0, 80);
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
    if (!lines.length) lines = [[Math.round(r.x), Math.round(r.y),
                                 Math.round(r.width), Math.round(r.height)]];
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
    const node = {
      text: txt,
      texts: texts,
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
  out.asserts = [];
  try {
    const num = (v) => (typeof v === "number" && isFinite(v)) ? v : null;
    for (const a of (Array.isArray(window.__akAssert) ? window.__akAssert : []).slice(0, 60)) {
      out.asserts.push({
        what: (a && typeof a.what === "string" && a.what.trim())
          ? a.what.trim().slice(0, 90) : null,
        expect: num(a && a.expect),
        actual: num(a && a.actual),
        tol: num(a && a.tol),
        unit: (a && typeof a.unit === "string") ? a.unit.trim().slice(0, 16) : ""
      });
    }
  } catch (e) {}
  return out;
}
"""


def launch_chromium(p):
    """Launch chromium, falling back to the pre-installed browser binary."""
    try:
        return p.chromium.launch(args=CHROMIUM_ARGS)
    except Exception:
        candidates = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
        candidates += ["/opt/pw-browsers/chromium/chrome-linux/chrome", "/opt/pw-browsers/chromium"]
        for c in candidates:
            if Path(c).exists():
                try:
                    return p.chromium.launch(executable_path=c, args=CHROMIUM_ARGS)
                except Exception:
                    continue
        raise RuntimeError("No launchable Chromium found (tried default + /opt/pw-browsers)")


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


def render_slide(browser, path: Path, out_png: Path, width: int, height: int,
                 scale: float, timeout_ms: int) -> dict:
    rec = {"file": path.name, "png": out_png.name, "console_errors": [], "page_errors": [],
           "overflow_warnings": [], "fonts_missing": [], "text_nodes": [],
           "body_overflow": False, "canvas_text": [], "svg_plates": [],
           "encodings": [], "contacts": [], "scales": [], "nondeterminism": [],
           "fits": [], "asserts": [], "css_unreadable": 0,
           "render_ms": 0, "ok": False}
    t0 = time.time()
    page = browser.new_page(viewport={"width": width, "height": height},
                            device_scale_factor=scale)
    page.add_init_script(CANVAS_TEXT_HOOK_JS)
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
                                       "fits", "asserts", "css_unreadable")})
        page.screenshot(path=str(out_png), clip={"x": 0, "y": 0, "width": width, "height": height})
        rec["ok"] = out_png.exists() and out_png.stat().st_size > 10_000
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
