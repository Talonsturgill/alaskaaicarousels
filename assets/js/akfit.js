/* akfit.js — MEASURE, THEN DRAW. The fitted-container bench.  (Alaska.Ai)
 * Committed 2026-09-12 for Carousel No. 57.
 *
 * WHAT THIS IS. Three small functions and one assertion, for the case where a
 * box, plate, chip, bracket or dashed container has to hold a string that the
 * author does not know the width of. The box is built FROM the laid-out text
 * rather than beside it, and the assertion at the end of renderReady refuses to
 * let a container ship narrower than what it contains.
 *
 * WHY IT EXISTS, and the number is specific. "Legibility and platform fitness"
 * scored 4 of 10 on No.56, the lowest single criterion score in the visible
 * record, and trend_check reports it weakest in 2 of the last 10 runs at a 6.6
 * mean with no upgrade ever aimed at it. The whole 4 was earned by one
 * mechanism. On slide 08 the class label LARGE COMMERCIAL AND INDUSTRIAL
 * wrapped to a second line, its dashed container did not grow with it, the
 * container's own border struck through the word INDUSTRIAL, and the group ran
 * past the 80 px right safe zone. A repair had lengthened the string minutes
 * earlier and nothing resized the box, because the box was two hand-typed
 * numbers.
 *
 * That is not a taste failure and it is not new. It is the same defect as
 * aktype's `AK.svgPlate` note from 2026-07-29, where six labels shipped off
 * their own plates because "the plate width and the label were two separately
 * hand-typed numbers", and it is the mechanism behind three of the six
 * recurring machine warn classes: art touching glyphs, canvas mark near
 * reserved text, outside safe zone. Every one of them is a container whose
 * geometry was decided before the text inside it was measured.
 *
 * `AK.svgPlate` already solved this for SVG `<text>`. Nothing solved it for a
 * DOM element, which is where this house sets nearly all of its type.
 *
 * THE RULE THE WHOLE FILE ENFORCES. No box, plate, chip, dashed container,
 * bracket or rule gets a hand-typed size. Lay the type out, await
 * `document.fonts.ready`, measure, then build the container from the
 * measurement plus a declared padding. A wrap then grows the box by
 * construction and a string edit can never leave a box stale.
 *
 * WHAT IT DELIBERATELY DOES NOT DO. It does not judge composition and it does
 * not check anything a reasonable design could legitimately violate. The
 * safe-zone and overflow checks are OPT IN, on `data-fit`, because plenty of
 * house slides put decorative type outside the margin on purpose and a guard
 * that cries wolf costs a review round, which is exactly what the five-round
 * cap was written about. The plate check is not opt in, because a container
 * narrower than its own contents is never a decision.
 *
 * FAILURE MODE. Every breach console.errors with the "AK CONTRACT: " prefix and
 * then throws, the akrelief pattern. The throw is the loud half and slide code
 * legitimately wraps art in try/catch, so the message is what survives the
 * catch. render.py records it and qa.py FAILS on the prefix.
 *
 * NO DEPENDENCIES, on purpose. Load it in any order. It touches no canvas, no
 * colour helper and no random source, so it cannot trip the determinism gate.
 */
(function (global) {
  "use strict";

  var W = 1080, H = 1350, SAFE = 80;
  var CONTRACT_TAG = "AK CONTRACT: ";
  var plates = [];   /* {plate, text, padX, padY, note} */

  /* ---------------- the contract guard, same shape as akrelief ---------------- */

  function nearest(key, allowed) {
    var best = null, bestD = 1e9, lk = String(key).toLowerCase(), i;
    for (i = 0; i < allowed.length; i++) {
      var a = allowed[i].toLowerCase(), m = [], j, k;
      for (j = 0; j <= lk.length; j++) m[j] = [j];
      for (k = 0; k <= a.length; k++) m[0][k] = k;
      for (j = 1; j <= lk.length; j++)
        for (k = 1; k <= a.length; k++)
          m[j][k] = Math.min(m[j - 1][k] + 1, m[j][k - 1] + 1,
                             m[j - 1][k - 1] + (lk[j - 1] === a[k - 1] ? 0 : 1));
      var d = m[lk.length][a.length];
      if (d < bestD) { bestD = d; best = allowed[i]; }
    }
    return (bestD <= Math.max(2, Math.ceil(lk.length / 3))) ? best : null;
  }

  function optionContract(fnName, opts, allowed) {
    var o = opts || {}, bad = [], k;
    for (k in o) {
      if (!Object.prototype.hasOwnProperty.call(o, k)) continue;
      if (allowed.indexOf(k) < 0) bad.push(k);
    }
    if (!bad.length) return;
    var msg = CONTRACT_TAG + fnName + ": unknown option" + (bad.length > 1 ? "s " : " ")
      + bad.map(function (b) {
          var guess = nearest(b, allowed);
          return "`" + b + "`" + (guess ? " -- did you mean `" + guess + "`?" : "");
        }).join(", ")
      + ". Allowed: " + allowed.join(", ") + ".";
    if (global.console && console.error) console.error(msg);
    throw new TypeError(msg);
  }

  function breach(msg) {
    var m = CONTRACT_TAG + msg;
    if (global.console && console.error) console.error(m);
    throw new Error(m);
  }

  /* ---------------- measurement ---------------- */

  function els(sel) {
    if (!sel) return [];
    if (typeof sel === "string") return Array.prototype.slice.call(document.querySelectorAll(sel));
    if (sel.length != null && typeof sel !== "function") return Array.prototype.slice.call(sel);
    return [sel];
  }

  /* An element's own laid-out box in design px. The page IS 1080x1350 design px
   * with no transforms on the root, so a client rect is already design px; this
   * exists so every caller reads the same four names and so a rect is never
   * assembled from style values, which are the author's intent rather than the
   * browser's result. */
  function rectOf(el) {
    var r = el.getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height,
             right: r.left + r.width, bottom: r.top + r.height };
  }

  /* The INK box rather than the element box. A block element is as wide as its
   * width property whatever the text does, so measuring the element tells you
   * about the CSS and not about the string. A Range over the text nodes gives
   * the line boxes the glyphs actually occupy, which is the thing a container
   * has to enclose. Falls back to the element box for an element with no text,
   * and unions the per-line rects so a ragged block is measured at its longest
   * line rather than at its declared width. */
  function inkRect(el) {
    var rng, rects, i, x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9, n = 0;
    try {
      rng = document.createRange();
      rng.selectNodeContents(el);
      rects = rng.getClientRects();
      for (i = 0; i < rects.length; i++) {
        var r = rects[i];
        if (r.width <= 0 || r.height <= 0) continue;
        x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top);
        x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
        n++;
      }
    } catch (e) { n = 0; }
    if (!n) return rectOf(el);
    return { x: x0, y: y0, w: x1 - x0, h: y1 - y0, right: x1, bottom: y1 };
  }

  /* Per-LINE ink rects, for a reserve or a veil that has to follow the rag.
   * Same reasoning aknight's `reserve` gives: measuring the block reserves the
   * paragraph's bounding rectangle, which is the plate this idiom exists to
   * avoid. */
  function lineRects(el) {
    var out = [], rng, rects, i;
    try {
      rng = document.createRange();
      rng.selectNodeContents(el);
      rects = rng.getClientRects();
      for (i = 0; i < rects.length; i++) {
        var r = rects[i];
        if (r.width <= 0.5 || r.height <= 0.5) continue;
        out.push({ x: r.left, y: r.top, w: r.width, h: r.height,
                   right: r.right, bottom: r.bottom });
      }
    } catch (e) { /* fall through */ }
    if (!out.length) out.push(inkRect(el));
    return out;
  }

  /* The measured union of a cluster, which is what a bracket or a clamp needs.
   * Uses INK boxes, so a 900px-wide block holding a 300px line contributes 300. */
  function union(sel, pad) {
    var list = els(sel), p = pad || 0, i, x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (i = 0; i < list.length; i++) {
      var r = inkRect(list[i]);
      if (!(r.w > 0 && r.h > 0)) continue;
      x0 = Math.min(x0, r.x); y0 = Math.min(y0, r.y);
      x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
    }
    if (x0 > x1) return null;
    return { x: x0 - p, y: y0 - p, w: (x1 - x0) + 2 * p, h: (y1 - y0) + 2 * p,
             right: x1 + p, bottom: y1 + p };
  }

  /* ---------------- the fitted container ---------------- */

  /* AKFIT.plate(textEl, opts) builds a DOM container sized from the MEASURED
   * ink box of `textEl` plus padding, inserts it as the element's previous
   * sibling (so it paints under the type without touching stacking context),
   * and registers it so `guard()` can prove it still encloses its text.
   *
   * Call it AFTER `await document.fonts.ready` and after any AK.fitText, or the
   * measurement is of the fallback face and the box is the wrong size. That is
   * the same requirement AK.svgPlate documents, and for the same reason: two
   * measured-at-the-wrong-moment guards were built on 2026-07-29 and both cried
   * wolf on correct usage, so the discipline is the author's and the gate on
   * the shipped pixels is what actually catches it.
   *
   * `grow` is the point of the whole function. A container built here is as big
   * as the string is, so a wrap or a late edit cannot leave a border running
   * through a word. */
  function plate(textEl, opts) {
    var o = opts || {};
    optionContract("AKFIT.plate", o, ["padX", "padY", "padTop", "padBottom",
      "fill", "stroke", "strokeWidth", "dash", "radius", "className", "minWidth",
      "minHeight", "zIndex", "note", "opacity"]);
    if (!textEl || !textEl.getBoundingClientRect)
      breach("AKFIT.plate: first argument must be an element, got " + typeof textEl);

    var r = inkRect(textEl);
    if (!(r.w > 0 && r.h > 0))
      breach("AKFIT.plate: `" + (textEl.className || textEl.tagName) +
             "` measured zero ink, so there is nothing to size a container from. " +
             "Call this after document.fonts.ready and after the element has text.");

    var padX = o.padX == null ? 14 : o.padX;
    var padY = o.padY == null ? 8 : o.padY;
    var padTop = o.padTop == null ? padY : o.padTop;
    var padBottom = o.padBottom == null ? padY : o.padBottom;
    var sw = o.strokeWidth == null ? (o.stroke ? 1.25 : 0) : o.strokeWidth;

    var w = r.w + 2 * padX, h = r.h + padTop + padBottom;
    var x = r.x - padX, y = r.y - padTop;
    /* minWidth grows the box symmetrically, so a centred label stays centred.
     * Same behaviour as AK.svgPlate's minWidth, deliberately. */
    if (o.minWidth && w < o.minWidth) { x -= (o.minWidth - w) / 2; w = o.minWidth; }
    if (o.minHeight && h < o.minHeight) { y -= (o.minHeight - h) / 2; h = o.minHeight; }

    var d = document.createElement("div");
    if (o.className) d.className = o.className;
    d.style.position = "absolute";
    /* the stroke is drawn INSIDE the declared box via box-sizing, so the border
     * never eats into the padding the text was measured for */
    d.style.boxSizing = "border-box";
    d.style.left = x.toFixed(2) + "px";
    d.style.top = y.toFixed(2) + "px";
    d.style.width = w.toFixed(2) + "px";
    d.style.height = h.toFixed(2) + "px";
    if (o.fill) d.style.background = o.fill;
    if (o.stroke) {
      d.style.border = sw.toFixed(2) + "px " + (o.dash ? "dashed" : "solid") + " " + o.stroke;
    }
    if (o.radius) d.style.borderRadius = (+o.radius).toFixed(2) + "px";
    if (o.opacity != null) d.style.opacity = String(o.opacity);
    if (o.zIndex != null) d.style.zIndex = String(o.zIndex);
    /* A container is not type and carries no reading of its own, so it is
     * decorative to every text gate. It is also never the text's occluder,
     * because render.py exempts an element the text paints above and this one is
     * inserted BEFORE the text in document order. */
    d.setAttribute("data-decorative", "");
    textEl.parentNode.insertBefore(d, textEl);

    plates.push({ plate: d, text: textEl, padX: padX, padTop: padTop,
                  padBottom: padBottom, note: o.note || "" });
    return { x: x, y: y, w: w, h: h, right: x + w, bottom: y + h, el: d };
  }

  /* ---------------- the clamp ---------------- */

  /* AKFIT.clamp(sel, opts) measures a cluster's ink union and translates the
   * whole cluster by whole pixels until it sits inside the safe box. Returns
   * the delta it applied, so a dossier's reconciliation section can record it.
   *
   * This is the second half of the No.56 defect. Growing the box fixes the
   * border through the word; it also makes the group WIDER, which is how the
   * same repair pushed the cluster past the right margin. The two have to be
   * fixed together or the first fix causes the second.
   *
   * It moves the ELEMENTS, not the container, and it moves them by setting
   * `left`/`top`, so an element positioned any other way is refused rather than
   * silently left behind. */
  function clamp(sel, opts) {
    var o = opts || {};
    optionContract("AKFIT.clamp", o, ["safe", "left", "right", "top", "bottom", "note"]);
    var s = o.safe == null ? SAFE : o.safe;
    var L = o.left == null ? s : o.left;
    var R = o.right == null ? W - s : o.right;
    var T = o.top == null ? s : o.top;
    var B = o.bottom == null ? H - s : o.bottom;

    var list = els(sel);
    var u = union(list, 0);
    if (!u) return { dx: 0, dy: 0 };

    var dx = 0, dy = 0;
    if (u.right > R) dx = -(u.right - R);
    if (u.x + dx < L) dx = L - u.x;
    if (u.bottom > B) dy = -(u.bottom - B);
    if (u.y + dy < T) dy = T - u.y;
    dx = Math.round(dx); dy = Math.round(dy);
    if (!dx && !dy) return { dx: 0, dy: 0 };

    for (var i = 0; i < list.length; i++) {
      var el = list[i], cs = global.getComputedStyle(el);
      if (cs.position !== "absolute" && cs.position !== "fixed")
        breach("AKFIT.clamp: `" + (el.className || el.tagName) + "` is " +
               cs.position + ", not absolutely positioned, so moving it by left/top " +
               "would do nothing. Position the cluster absolutely or clamp it by hand.");
      var r = rectOf(el);
      el.style.left = (r.x + dx).toFixed(2) + "px";
      el.style.top = (r.y + dy).toFixed(2) + "px";
    }
    return { dx: dx, dy: dy };
  }

  /* ---------------- the assertion ---------------- */

  /* AKFIT.guard() is what makes this different from care. Call it as the LAST
   * thing inside renderReady, after every plate, fit and clamp.
   *
   * THREE CHECKS, and the split between mandatory and opt in is deliberate.
   *
   * 1. EVERY REGISTERED PLATE ENCLOSES ITS TEXT. Not opt in and not tunable: a
   *    container narrower or shorter than the string inside it is never a
   *    design decision. Re-measures both at guard time, so a plate built
   *    correctly and then invalidated by a later string edit, a later fitText,
   *    or a later clamp of the text alone is caught here rather than by a
   *    scorer. One design px of tolerance, for subpixel layout only.
   *
   * 2. EVERY `data-fit` ELEMENT SITS INSIDE THE SAFE BOX. Opt in, because this
   *    house deliberately bleeds decorative type past the margin and a guard
   *    that forbids it would be wrong more often than right. Put `data-fit` on
   *    the blocks that carry the slide's reading, which is the same set a
   *    dossier already names.
   *
   * 3. NO `data-fit` ELEMENT OVERFLOWS ITS OWN BOX. Opt in, same reasoning.
   *    Catches the fixed-height block whose text grew past it, which renders as
   *    a clipped last line and is invisible in a screenshot when the clip is
   *    clean.
   */
  function guard(opts) {
    var o = opts || {};
    optionContract("AKFIT.guard", o, ["safe", "tol", "quiet"]);
    var s = o.safe == null ? SAFE : o.safe;
    var tol = o.tol == null ? 1.0 : o.tol;
    var bad = [], i;

    for (i = 0; i < plates.length; i++) {
      var p = plates[i];
      var pr = rectOf(p.plate), tr = inkRect(p.text);
      var over = [];
      if (tr.x < pr.x - tol) over.push("left by " + (pr.x - tr.x).toFixed(1) + "px");
      if (tr.right > pr.right + tol) over.push("right by " + (tr.right - pr.right).toFixed(1) + "px");
      if (tr.y < pr.y - tol) over.push("top by " + (pr.y - tr.y).toFixed(1) + "px");
      if (tr.bottom > pr.bottom + tol) over.push("bottom by " + (tr.bottom - pr.bottom).toFixed(1) + "px");
      if (over.length) {
        bad.push("a fitted container no longer holds its text. '" +
          String(p.text.textContent || "").trim().slice(0, 46) +
          "' spills " + over.join(" and ") + (p.note ? " (" + p.note + ")" : "") +
          ". The container was measured before something changed the string, the " +
          "font size or the position. Rebuild the plate after that change, or " +
          "narrow the measure so the line fits.");
      }
    }

    var fit = els("[data-fit]");
    for (i = 0; i < fit.length; i++) {
      var el = fit[i], r = inkRect(el);
      var out = [];
      if (r.x < s - tol) out.push((s - r.x).toFixed(1) + "px past the left margin");
      if (r.right > W - s + tol) out.push((r.right - (W - s)).toFixed(1) + "px past the right margin");
      if (r.y < s - tol) out.push((s - r.y).toFixed(1) + "px above the top margin");
      if (r.bottom > H - s + tol) out.push((r.bottom - (H - s)).toFixed(1) + "px below the bottom margin");
      if (out.length) {
        bad.push("`" + (el.className || el.tagName) + "` carries the slide's reading and " +
          "sits " + out.join(" and ") + ". Text marked data-fit belongs inside the " +
          s + "px safe zone. Move it, or narrow it, and do NOT shrink the type to " +
          "win the fight (body floor is 32px).");
      }
      /* an overflow of two design px or less is subpixel layout, not a clip */
      if (el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0) {
        bad.push("`" + (el.className || el.tagName) + "` overflows its own box by " +
          (el.scrollHeight - el.clientHeight) + "px of height, so its last line is " +
          "clipped. A clean clip is invisible in a screenshot. Grow the box or " +
          "shorten the string.");
      }
      if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) {
        bad.push("`" + (el.className || el.tagName) + "` overflows its own box by " +
          (el.scrollWidth - el.clientWidth) + "px of width.");
      }
    }

    global.__akFit = { plates: plates.length, fitted: fit.length, breaches: bad.slice() };
    if (bad.length) breach("AKFIT.guard: " + bad.length + " fit breach" +
      (bad.length > 1 ? "es" : "") + ". " + bad.join("  ||  "));
    return global.__akFit;
  }

  global.AKFIT = {
    W: W, H: H, SAFE: SAFE,
    rectOf: rectOf, inkRect: inkRect, lineRects: lineRects, union: union,
    plate: plate, clamp: clamp, guard: guard,
    /* the reserve set every canvas field should punch, measured not guessed */
    reserveBoxes: function (sel) {
      var list = els(sel), out = [], i, j;
      for (i = 0; i < list.length; i++) {
        var lr = lineRects(list[i]);
        for (j = 0; j < lr.length; j++) out.push([lr[j].x, lr[j].y, lr[j].w, lr[j].h]);
      }
      return out;
    }
  };
})(window);
