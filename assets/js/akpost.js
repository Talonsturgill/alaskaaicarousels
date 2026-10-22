/* akpost.js — film-grade post-processing for slide canvases (no deps, CPU).
 *
 * The finishing pass that separates "drawn shapes" from "a graded still".
 * Implements the researched minimal grading stack (Hable's op order + ACES
 * Narkowicz fit + IGN dither + luminance-masked grain + output sharpening):
 *
 *   bloom (linear, brights only)
 *     -> exposure -> saturation -> log-contrast (pivot 0.18)
 *     -> ACES filmic -> display gamma -> lift/gain split-tone
 *     -> luminance-masked soft-light grain
 *     -> IGN dither (LAST grading op: kills 8-bit banding)
 *     -> unsharp mask (output sharpening, optional)
 *
 * ORDER IS NOT OPTIONAL (research-verified): contrast before the filmic curve,
 * dither after all grading, sharpening last. Call grade() ONCE on the ART
 * canvas after all drawing; DOM text sits above and is never touched. All ops
 * deterministic (seeded); single read + single write of ImageData.
 *
 * USAGE (inside renderReady, after drawing the art):
 *   <script src="@@ASSETS@@/js/akpost.js"></script>
 *   AKPOST.grade(cx, {
 *     w: 1080, h: 1350,
 *     exposure: 0.0,                    // stops; art slightly under-exposed (-0.15) gives rolloff headroom
 *     saturation: 1.08,
 *     contrast: 1.12,                   // log-space, pivot 0.18
 *     filmic: true,                     // ACES fit; per-channel (film-like hue shifts by design)
 *     lift: [0.010, 0.014, 0.024],      // shadow tint (cool) 0..~0.05
 *     gain: [1.015, 1.0, 0.975],        // highlight tint (warm)
 *     vignette: 0.2,                    // radial multiply toward a cooler edge, felt not seen
 *     bloom: { threshold: 0.72, strength: 0.35, radius: 8 },
 *     grain: { amount: 0.05, size: 2, seed: 20260711 },  // soft-light, shadows/mids only
 *     aberration: 0,                    // px RGB fringe at corners; hero-art slides ONLY, never data/text
 *     dither: true,                     // IGN, +-1 LSB
 *     sharpen: 0.35                     // unsharp amount; skip on halftone regions (moire)
 *   });
 *
 * EVERY GRADING OPTION IS STICKY. THERE IS NO "JUST THE DITHER" CALL.
 * (2026-09-20, run No.64, and it cost a whole render cycle.) The block above
 * is a FULL options object, so it reads like a list of what you are passing.
 * It is not: it is a list of what you get whether you pass it or not. Omit an
 * option and grade() supplies its own default, and the defaults are not
 * identities:
 *
 *     filmic      true    <- the ACES curve. `o.filmic !== false`
 *     saturation  1.06
 *     contrast    1.10    <- log-space, pivot 0.18
 *     exposure    0.0     (this one IS an identity)
 *
 * So `AKPOST.grade(cx, {w, h, dither: true})` does NOT dither a frame and
 * leave it otherwise alone. It runs the full tone chain over every pixel. Run
 * No.64's risk register named IGN dither as the mitigation for a 900 px sky
 * ramp; adding what looked like a dither-only call moved every value in every
 * frame, took slide 06 from clean to nine label-crossing failures in ONE
 * render, and silently invalidated the contact, contrast and encoding numbers
 * already measured off the previous render. A grade is not additive to a
 * finished frame; it REPLACES that frame's tone.
 *
 * To add dither and nothing else, say so:
 *     AKPOST.grade(cx, {w, h, dither: true, filmic: false,
 *                       saturation: 1, contrast: 1});
 *
 * THE SHAPES ABOVE ARE ENFORCED (2026-07-26): a wrong option shape THROWS
 * (contrast is a NUMBER, lift/gain are TOP-LEVEL 3-element arrays), and an
 * unknown key is reported via console.error rather than silently ignored.
 *
 * HOUSE GRADE for the dark-arctic register: the defaults above. Brand-exact
 * marks (gold Polaris, wordmark) should be DOM/SVG so the grade never shifts
 * them. Budget total texture (grain + dither + any feTurbulence) <= ~10%.
 */
(function (global) {
  "use strict";
  const P = {};

  function getScale(ctx) {
    const t = ctx.getTransform ? ctx.getTransform() : { a: 1 };
    return t.a || 1;
  }

  /* ---- ARGUMENT VALIDATION (2026-07-26) --------------------------------
   * Added after a slide called grade() with contrast as an OBJECT
   * ({amount, pivot}) and lift/gain as HEX STRINGS inside an undocumented
   * `split` wrapper. Every arithmetic op downstream produced NaN, the whole
   * ImageData wrote 0, and the slide rendered a fully black art canvas with
   * errors=0: nothing in the engine complained, because grade() coerced
   * whatever it was handed. A wrong option shape is a bug, not a style, so it
   * now THROWS (render.py records the page error and hard-fails the slide)
   * rather than silently blanking a canvas. Unknown keys are reported via
   * console.error (qa.py surfaces it as a WARN) because a silently ignored
   * option is how the `split` wrapper hid the real problem.
   */
  const NUM_OPTS = ["w", "h", "exposure", "saturation", "contrast", "vignette",
                    "aberration", "sharpen"];
  /* EXPOSURE IS IN STOPS AND THE COMMENT SAYING SO IS NOT A GUARD (2026-08-12).
   * Runs No.30 (2026-08-08) and No.31 (2026-08-12) each authored exposure as a
   * MULTIPLIER on all nine slides -- 1.0 to 1.06, meaning "about three percent"
   * -- and got 2^1.03 = 2.04x, a full stop over, on eighteen consecutive slides
   * that nothing in the engine questioned. The root cause is a shared word with
   * two meanings in two libraries this deck uses side by side: AKPOST.grade's
   * exposure is STOPS, akthree's AKT.setup({exposure}) is a MULTIPLIER on
   * three.js toneMappingExposure. On No.31 the over-exposure bloomed copper
   * #B8703C until five independent critics could not separate it from gold
   * #FFC72C at 432px, and each of them reported it as a different fault on a
   * different slide, which is what a deck-wide silent defect looks like from
   * inside a review round.
   *
   * The threshold is the house grade, not a guess. Every shipped AKPOST.grade
   * call in the corpus that was AUTHORED AS STOPS sits in -0.15..+0.06; the
   * defect band is 1.00..1.06. 0.75 stops is a 1.68x lift on an already-graded
   * canvas, five times the largest deliberate value this studio has ever used
   * and comfortably under every instance of the defect. Nothing in this house's
   * register wants it, so it is refused rather than warned about: the 2026-07-26
   * precedent in this file is that a wrong option SHAPE throws, and a wrong
   * option UNIT that doubles the whole frame is not a milder mistake. If a slide
   * genuinely wants a stop of lift, paint it brighter. Raising this ceiling is
   * the maintainer's call. */
  const EXPOSURE_MAX_STOPS = 0.75;
  const TRIPLE_OPTS = ["lift", "gain"];
  const OBJ_OPTS = { bloom: ["threshold", "strength", "radius"],
                     grain: ["amount", "size", "seed"] };
  const BOOL_OPTS = ["filmic", "dither"];
  const KNOWN = NUM_OPTS.concat(TRIPLE_OPTS, BOOL_OPTS, Object.keys(OBJ_OPTS));

  function bad(where, got, want) {
    throw new TypeError("AKPOST.grade: " + where + " must be " + want +
      ", got " + (Array.isArray(got) ? "array[" + got.length + "]" : typeof got) +
      " " + JSON.stringify(got));
  }

  function validate(o) {
    for (const k of NUM_OPTS) {
      if (o[k] == null) continue;
      if (typeof o[k] !== "number" || !isFinite(o[k])) bad(k, o[k], "a finite number");
    }
    if (typeof o.exposure === "number" && isFinite(o.exposure) &&
        Math.abs(o.exposure) > EXPOSURE_MAX_STOPS) {
      throw new RangeError(
        "AKPOST.grade: exposure is in STOPS, and " + o.exposure + " stops is " +
        Math.pow(2, o.exposure).toFixed(2) + "x the whole frame, past the " +
        EXPOSURE_MAX_STOPS + "-stop ceiling. If you meant a multiplier, you are " +
        "thinking of akthree's AKT.setup({exposure}), which IS one; here " +
        (o.exposure > 0.9 && o.exposure < 1.2
           ? "a value near 1.0 is the units mistake that shipped on 2026-08-08 " +
             "and 2026-08-12 -- for '" +
             Math.round((o.exposure - 1) * 100) + " percent' write " +
             (Math.log(o.exposure) / Math.LN2).toFixed(3) + ", and the house " +
             "grade lives in -0.15..+0.06. "
           : "") +
        "0 is unchanged, +1 is twice as bright, -1 is half.");
    }
    for (const k of TRIPLE_OPTS) {
      if (o[k] == null) continue;
      const v = o[k];
      if (!Array.isArray(v) || v.length !== 3 ||
          !v.every((n) => typeof n === "number" && isFinite(n)))
        bad(k, v, "a 3-element array of finite numbers, e.g. [0.010, 0.014, 0.024]");
    }
    for (const k of Object.keys(OBJ_OPTS)) {
      if (o[k] == null) continue;
      const v = o[k];
      if (typeof v !== "object" || Array.isArray(v))
        bad(k, v, "an object of {" + OBJ_OPTS[k].join(", ") + "}");
      for (const f of OBJ_OPTS[k]) {
        if (v[f] == null) continue;
        if (typeof v[f] !== "number" || !isFinite(v[f]))
          bad(k + "." + f, v[f], "a finite number");
      }
    }
    for (const k of BOOL_OPTS) {
      if (o[k] == null) continue;
      if (typeof o[k] !== "boolean") bad(k, o[k], "true or false");
    }
    for (const k of Object.keys(o)) {
      if (KNOWN.indexOf(k) === -1) {
        try {
          console.error("AKPOST.grade: unknown option '" + k + "' is being IGNORED " +
            "(known options: " + KNOWN.join(", ") + "). Check the contract in " +
            "akpost.js: lift/gain are top-level 3-element arrays, contrast is a number.");
        } catch (e) {}
      }
    }
  }

  P.grade = function (ctx, o) {
    o = o || {};
    validate(o);
    const scale = getScale(ctx);
    const W = Math.round((o.w || ctx.canvas.width / scale) * scale);
    const H = Math.round((o.h || ctx.canvas.height / scale) * scale);
    const img = ctx.getImageData(0, 0, W, H);
    const d = img.data;

    /* ---- srgb<->linear tables ---- */
    const toLin = new Float32Array(256);
    for (let i = 0; i < 256; i++) toLin[i] = Math.pow(i / 255, 2.2);

    /* ---- bloom in linear (downsampled box blur of thresholded brights) ---- */
    if (o.bloom && o.bloom.strength > 0) {
      const bt = o.bloom.threshold != null ? o.bloom.threshold : 0.72;
      const bs = o.bloom.strength != null ? o.bloom.strength : 0.35;
      const ds = 4, bw = Math.ceil(W / ds), bh = Math.ceil(H / ds);
      const rad = Math.max(1, Math.round((o.bloom.radius || 8) / ds));
      // AREA-MEAN DOWNSAMPLE, BILINEAR UPSAMPLE (2026-10-11, weekly machine
      // pass). The bloom used to take ONE pixel per 4 x 4 block and write each
      // block back as a flat 4 px square, so an emitter smaller than a block was
      // either caught whole or missed, and every caught one printed a square:
      // No.83 slide 05's 15,141 one-pixel beads bloomed into 4 to 6 px
      // quantised tiles the critic named, and the run dropped bloom by hand.
      // Every pixel past the threshold now contributes its share to its block,
      // and the blurred blocks are read back between their centres
      // (tests/akpost_verify.mjs, the dot-lattice fixture).
      let buf = new Float32Array(bw * bh * 3);
      const inv = 1 / (ds * ds);
      for (let y = 0; y < H; y++) {
        const by0 = ((y / ds) | 0) * bw;
        for (let x = 0; x < W; x++) {
          const si = (y * W + x) * 4;
          const r = toLin[d[si]], g = toLin[d[si + 1]], b = toLin[d[si + 2]];
          const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
          if (lum > bt * bt) {  // threshold approx in linear
            const k = Math.min(1, (Math.sqrt(lum) - bt) / (1 - bt)) * inv;
            if (k > 0) {
              const bi = (by0 + ((x / ds) | 0)) * 3;
              buf[bi] += r * k; buf[bi + 1] += g * k; buf[bi + 2] += b * k;
            }
          }
        }
      }
      // separable box blur x2
      for (let pass = 0; pass < 2; pass++) {
        const out = new Float32Array(bw * bh * 3);
        const dx = pass === 0 ? 1 : bw, len = pass === 0 ? bw : bh, lines = pass === 0 ? bh : bw;
        for (let l = 0; l < lines; l++) {
          const base = pass === 0 ? l * bw : l;
          for (let c = 0; c < 3; c++) {
            let acc = 0;
            for (let i = -rad; i <= rad; i++) acc += buf[(base + Math.min(len - 1, Math.max(0, i)) * dx) * 3 + c];
            for (let i = 0; i < len; i++) {
              out[(base + i * dx) * 3 + c] = acc / (2 * rad + 1);
              acc += buf[(base + Math.min(len - 1, i + rad + 1) * dx) * 3 + c]
                   - buf[(base + Math.max(0, i - rad) * dx) * 3 + c];
            }
          }
        }
        buf = out;
      }
      const half = (ds - 1) / 2;
      for (let y = 0; y < H; y++) {
        const gy = Math.min(bh - 1, Math.max(0, (y - half) / ds));
        const y0 = gy | 0, y1 = Math.min(bh - 1, y0 + 1), ty = gy - y0;
        for (let x = 0; x < W; x++) {
          const gx = Math.min(bw - 1, Math.max(0, (x - half) / ds));
          const x0 = gx | 0, x1 = Math.min(bw - 1, x0 + 1), tx = gx - x0;
          const b00 = (y0 * bw + x0) * 3, b01 = (y0 * bw + x1) * 3;
          const b10 = (y1 * bw + x0) * 3, b11 = (y1 * bw + x1) * 3;
          const i4 = (y * W + x) * 4;
          for (let c = 0; c < 3; c++) {
            const top = buf[b00 + c] + (buf[b01 + c] - buf[b00 + c]) * tx;
            const bot = buf[b10 + c] + (buf[b11 + c] - buf[b10 + c]) * tx;
            const s = toLin[d[i4 + c]], add = (top + (bot - top) * ty) * bs;
            // additive in linear, encode back
            d[i4 + c] = 255 * Math.pow(Math.min(1, s + add), 1 / 2.2);
          }
        }
      }
    }

    /* ---- the tone chain as a LUT over post-saturation LINEAR values ---- */
    const expMul = Math.pow(2, o.exposure || 0);
    const sat = o.saturation != null ? o.saturation : 1.06;
    const con = o.contrast != null ? o.contrast : 1.1;
    const filmic = o.filmic !== false;
    const lift = o.lift || [0, 0, 0];
    const gain = o.gain || [1, 1, 1];
    const NL = 1024, LMAX = 2.0;
    const lut = [new Float32Array(NL), new Float32Array(NL), new Float32Array(NL)];
    const log2 = Math.log2 || ((x) => Math.log(x) / Math.LN2);
    for (let c = 0; c < 3; c++) {
      for (let i = 0; i < NL; i++) {
        // SQUARE-ROOT INDEXED (2026-10-11, No.84). The table used to be indexed
        // linearly in LINEAR light, 1024 bins over 0..2, so every value under
        // about sRGB 10 fell in bin 0 and the next bin up landed at sRGB 15:
        // a dark gradient graded into hard steps (slide 08's teal seam and the
        // striped header of the same frame). Indexing by sqrt spends the bins
        // where the eye resolves them, and the lookup below interpolates.
        const u = i / (NL - 1);
        let x = u * u * LMAX;                  // linear in
        // log-space contrast, pivot 0.18 (never clamps blacks)
        x = Math.pow(2, (log2(x + 1e-5) - log2(0.18)) * con + log2(0.18));
        // ACES Narkowicz fit (per-channel: film-like hue shifts by design)
        if (filmic) x = (x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14);
        x = Math.min(1, Math.max(0, x));
        // display gamma
        x = Math.pow(x, 1 / 2.2);
        // lift/gain split-tone in display space
        x = lift[c] + x * (gain[c] - lift[c] * 0.5);
        lut[c][i] = Math.min(1, Math.max(0, x));
      }
    }
    /* NaN SENTINEL (2026-07-26): the tone LUT is where every scalar option
     * lands, so one non-finite entry here means the grade would write a black
     * (or garbage) frame over the art. Throw instead: a dead canvas that
     * reports errors=0 is the worst outcome of all. Costs 3 lookups. */
    for (let c = 0; c < 3; c++) {
      if (!isFinite(lut[c][0]) || !isFinite(lut[c][NL >> 1]) || !isFinite(lut[c][NL - 1]))
        throw new Error("AKPOST.grade: tone LUT is non-finite (channel " + c +
          ") -- a grade option produced NaN; the graded frame would be blank");
    }

    const look = (t, v) => {
      const f = Math.min(NL - 1, Math.sqrt(Math.max(0, v) / LMAX) * (NL - 1)), i0 = f | 0, i1 = Math.min(NL - 1, i0 + 1);
      return t[i0] + (t[i1] - t[i0]) * (f - i0);
    };
    const vig = o.vignette || 0;
    const cxm = W / 2, cym = H / 2, maxR2 = cxm * cxm + cym * cym;

    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const i4 = (y * W + x) * 4;
        // to linear + exposure
        let r = toLin[d[i4]] * expMul, g = toLin[d[i4 + 1]] * expMul, b = toLin[d[i4 + 2]] * expMul;
        // saturation in linear
        if (sat !== 1) {
          const l = 0.25 * r + 0.5 * g + 0.25 * b;
          r = l + (r - l) * sat; g = l + (g - l) * sat; b = l + (b - l) * sat;
          r = r < 0 ? 0 : r; g = g < 0 ? 0 : g; b = b < 0 ? 0 : b;
        }
        // LUT chain
        let R = look(lut[0], r), G = look(lut[1], g), B = look(lut[2], b);
        // vignette: multiply toward a slightly COOLER edge (corners stay alive)
        if (vig > 0) {
          const dx = x - cxm, dy = y - cym;
          const f = vig * ((dx * dx + dy * dy) / maxR2);
          R *= 1 - f; G *= 1 - f * 0.96; B *= 1 - f * 0.88;
        }
        d[i4] = 255 * R; d[i4 + 1] = 255 * G; d[i4 + 2] = 255 * B;
      }
    }

    /* ---- chromatic aberration (radial, edges only; hero art ONLY) ---- */
    const aber = (o.aberration || 0) * scale;
    if (aber > 0) {
      const src = new Uint8ClampedArray(d);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
        const dx = (x - cxm) / cxm, dy = (y - cym) / cym;
        const r2 = dx * dx + dy * dy;
        if (r2 < 0.25) continue;
        const k = (r2 - 0.25) / 0.75 * aber;
        const i4 = (y * W + x) * 4;
        d[i4] = src[(Math.min(H - 1, Math.max(0, Math.round(y + dy * k))) * W
                   + Math.min(W - 1, Math.max(0, Math.round(x + dx * k)))) * 4];
        d[i4 + 2] = src[(Math.min(H - 1, Math.max(0, Math.round(y - dy * k))) * W
                       + Math.min(W - 1, Math.max(0, Math.round(x - dx * k)))) * 4 + 2];
      }
    }

    /* ---- luminance-masked soft-light film grain (shadows/mids only) ---- */
    if (o.grain && o.grain.amount > 0) {
      const ga = o.grain.amount, gs = Math.max(1, o.grain.size || 2);
      let seed = (o.grain.seed || 11) >>> 0;
      const gw = Math.ceil(W / gs) + 2, gh = Math.ceil(H / gs) + 2;
      const gn = new Float32Array(gw * gh);
      for (let i = 0; i < gn.length; i++) {   // seeded LCG
        seed = (seed * 1664525 + 1013904223) >>> 0;
        gn[i] = seed / 4294967296;
      }
      for (let y = 0; y < H; y++) {
        const gy = y / gs, gy0 = gy | 0, fy = gy - gy0;
        for (let x = 0; x < W; x++) {
          const gx = x / gs, gx0 = gx | 0, fx = gx - gx0;
          // bilinear value noise (clumpy, filmic)
          const a = gn[gy0 * gw + gx0], b2 = gn[gy0 * gw + gx0 + 1];
          const c2 = gn[(gy0 + 1) * gw + gx0], e = gn[(gy0 + 1) * gw + gx0 + 1];
          const nv = (a + (b2 - a) * fx) + ((c2 + (e - c2) * fx) - (a + (b2 - a) * fx)) * fy;
          const i4 = (y * W + x) * 4;
          const lum = (0.2126 * d[i4] + 0.7152 * d[i4 + 1] + 0.0722 * d[i4 + 2]) / 255;
          const mask = 1 - Math.min(1, Math.max(0, (lum - 0.05) / 0.45)); // fades in highlights
          const gEff = ga * (0.35 + 0.65 * mask);
          const t = (nv - 0.5) * 2;
          for (let c = 0; c < 3; c++) {
            const s = d[i4 + c] / 255;
            // soft-light-ish: brighten/darken proportional to distance from extremes
            const sl = t < 0 ? s * (1 + t * gEff) : s + (1 - s) * t * gEff;
            d[i4 + c] = 255 * Math.min(1, Math.max(0, sl));
          }
        }
      }
    }

    /* ---- IGN dither: THE banding killer, exactly +-1 LSB, LAST grade op ---- */
    if (o.dither !== false) {
      for (let y = 0; y < H; y++) {
        for (let x = 0; x < W; x++) {
          const f = 52.9829189 * ((0.06711056 * x + 0.00583715 * y) % 1);
          const t2 = (f - Math.floor(f)) - 0.5;
          const i4 = (y * W + x) * 4;
          for (let c = 0; c < 3; c++) {
            const v = d[i4 + c] + t2;
            d[i4 + c] = v < 0 ? 0 : v > 255 ? 255 : v;
          }
        }
      }
    }

    /* ---- unsharp mask (output sharpening; skip on halftone regions) ---- */
    if (o.sharpen && o.sharpen > 0) {
      const amt = o.sharpen, thr = 3;
      const src = new Uint8ClampedArray(d);
      for (let y = 1; y < H - 1; y++) {
        for (let x = 1; x < W - 1; x++) {
          const i4 = (y * W + x) * 4;
          for (let c = 0; c < 3; c++) {
            const center = src[i4 + c];
            const blur = (src[i4 + c - 4] + src[i4 + c + 4]
                        + src[i4 + c - W * 4] + src[i4 + c + W * 4] + center * 4) / 8;
            const diff = center - blur;
            if (Math.abs(diff) > thr) {
              const v = center + diff * amt;
              d[i4 + c] = v < 0 ? 0 : v > 255 ? 255 : v;
            }
          }
        }
      }
    }

    /* ---- write once ---- */
    const t = ctx.getTransform();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.putImageData(img, 0, 0);
    ctx.setTransform(t);
    return true;
  };

  /* ---- RESERVE: a feathered quiet ground under type (2026-10-21, weekly pass) ----
   *
   *   AKPOST.reserve(cx, rects, {color: '#070B11', feather: 20, strength: 0.9});
   *   AKPOST.reserve(off, rects, {erase: true});      // punch out of an offscreen field
   *
   * A BLURRED BOX IS STILL A BOX UNTIL ITS FEATHER IS WIDE, and four decks in a
   * row learned that by hand: No.89 (03, 04, 05, "a blurred box is still a
   * box"), No.90 (06, "a knockout is a box unless it is a feather"), No.91 (the
   * flow critic: "type reserve findable as vertical hatch bands"), No.92 (02,
   * 03, 04, slabs until the blur reached 40). Each wrote its own helper and each
   * met the same root cause, measured on 2026-10-21 in the engine's Chromium
   * 141: ctx.filter's blur radius is in BITMAP px and ignores the transform, so
   * on the house's 2x canvas `blur(10px)` is a 5 design px sigma (10 to 90
   * percent edge: 24 device px at scale 1 AND at scale 2). Every reserve helper
   * in assets/js typed its blur as if it were design px and got half of it.
   * The feather that stopped printing as a slab on textured art was 40 bitmap
   * px on No.92, a 20 design px sigma, a 10-to-90 edge of about 51 design px;
   * No.89's 60 px and No.90's 70 px smoothstep feathers sit on the same width.
   *
   * So here `feather` is the Gaussian sigma in DESIGN px (converted through the
   * context's own scale), defaulting to that measured 20. `pad` (default 1.28
   * sigma) grows each rect so the TYPE's own box sits at the 90 percent contour
   * and the half-strength line lies outside it: the long fall-off with its
   * centre toward the dark side that Material's scrim guidance asks for
   * (https://css-tricks.com/easing-linear-gradients/). The rects are filled as
   * ONE opaque union on an offscreen and blurred once, so overlapping line boxes
   * do not stack into a darker seam. Paint mode needs the GROUND's own colour
   * (`color`, required): a reserve in a different tone from the ground around
   * it is a plate however soft its edge. Call it BEFORE AKPOST.grade so the
   * reserve and the ground are graded as one tone (No.92, AKK.punch).
   * `erase: true` punches with destination-out instead, for an offscreen field.
   * A wrong option shape throws, as grade() does. Returns the bitmap px blur
   * and the pad used. tests/akpost_reserve_verify.py holds the numbers. */
  const RESERVE_FEATHER = 20;
  const RESERVE_OPTS = ["feather", "color", "erase", "strength", "pad"];
  function badR(where, got, want) {
    throw new TypeError("AKPOST.reserve: " + where + " must be " + want + ", got " +
      (Array.isArray(got) ? "array[" + got.length + "]" : typeof got) + " " + JSON.stringify(got));
  }
  P.reserve = function (ctx, rects, o) {
    o = o || {};
    for (const k of Object.keys(o)) {
      if (RESERVE_OPTS.indexOf(k) === -1)
        throw new TypeError("AKPOST.reserve: unknown option '" + k + "' (known: " +
                            RESERVE_OPTS.join(", ") + ")");
    }
    if (!Array.isArray(rects)) badR("rects", rects, "an array of [x, y, w, h]");
    for (const r of rects) {
      if (!Array.isArray(r) || r.length < 4 || !r.slice(0, 4).every((n) => typeof n === "number" && isFinite(n)))
        badR("rect", r, "[x, y, w, h] in design px");
    }
    const feather = o.feather != null ? o.feather : RESERVE_FEATHER;
    if (typeof feather !== "number" || !isFinite(feather) || feather < 0)
      badR("feather", feather, "a sigma in design px, 0 or more");
    const strength = o.strength != null ? o.strength : 0.9;
    if (typeof strength !== "number" || !(strength >= 0 && strength <= 1))
      badR("strength", strength, "a number from 0 to 1");
    const pad = o.pad != null ? o.pad : 1.28 * feather;
    if (typeof pad !== "number" || !isFinite(pad)) badR("pad", pad, "design px");
    if (!o.erase && typeof o.color !== "string")
      badR("color", o.color, "the ground's own colour as a string (or erase: true)");
    const t = ctx.getTransform();
    const s = Math.hypot(t.a, t.b) || 1;
    const cv = ctx.canvas, off = document.createElement("canvas");
    off.width = cv.width; off.height = cv.height;
    const g = off.getContext("2d");
    g.setTransform(t);
    g.fillStyle = o.erase ? "#000" : o.color;
    for (const r of rects) g.fillRect(r[0] - pad, r[1] - pad, r[2] + 2 * pad, r[3] + 2 * pad);
    const px = feather * s;
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = strength;
    ctx.globalCompositeOperation = o.erase ? "destination-out" : "source-over";
    ctx.filter = px > 0 ? "blur(" + px + "px)" : "none";
    ctx.drawImage(off, 0, 0);
    ctx.restore();
    return { blurBitmapPx: px, pad: pad };
  };

  /* ---- HOLD INK: put a drifted brand ink back on its own hue (2026-10-21) ----
   *
   *   AKPOST.grade(cx, {...});      // and any sill, vignette or GPU snapshot
   *   AKPOST.holdInk(cx, {hex: '#FFC72C'});            // LAST, on the art canvas
   *
   * THE HOUSE GRADE TURNS THE FLAG GOLD LEMON. Measured 2026-10-21 in the
   * engine's Chromium: a flat #FFC72C patch through AKPOST.grade's defaults
   * (no bloom, grain, dither, vignette or sharpen) comes out rgb(236, 217, 0),
   * dE76 19.9, Lab hue 84.9 to 97.3 degrees; #FFDA6E goes 89.6 to 100.8. The
   * per-channel ACES curve compresses red, which is already near the top, harder
   * than green, and saturation drives blue to zero. No.92's critics called the
   * gold lemon on 04, 05 and 09 for three rounds: 09 drew its crest before the
   * grade, 05's line was a three.js tube under the renderer's own tone mapping,
   * fog and a sill, which read lemon and then olive. Drawing the ink after the
   * grade is the first cure; this is the one for gold that has to live inside
   * the graded or rendered picture.
   *
   * Every pixel whose Lab hue lies in [ink - below, ink + above] degrees and
   * whose chroma is at least `minChroma` (default 0.45 of the ink's own, so an
   * olive ground or a grey edge is never touched) has its hue turned back to the
   * ink's, keeping its own L* and chroma (the light and the shading stay; only
   * the drift goes), with chroma reduced only as far as the sRGB gamut needs.
   * Where the gamut can't hold that L* and chroma at the ink's hue (a lifted
   * gold near the yellow cusp), the pixel gives up the difference toward the
   * ink's own L* and chroma, by the least fraction that fits.
   * The window (below 2, above 15 by default) is lopsided on purpose: the
   * drift runs toward yellow, and an olive ground (graded hue about 104) or a
   * salmon or copper below gold's hue stays where it is. A supporting amber
   * that the grade has ALSO carried to within a few degrees of gold is in the
   * family by then and moves with it; pass `rect` to keep it out.
   * Both window edges and the chroma floor feather over `soft` degrees and
   * chroma units, so nothing draws a seam. `rect` [x, y, w, h] in design px
   * limits it to a region. Returns {px, meanShift}: the pixels moved and their
   * mean hue turn in degrees. tests/akpost_holdink_verify.py holds the numbers. */
  const HOLD_OPTS = ["hex", "below", "above", "minChroma", "soft", "rect"];
  P.holdInk = function (ctx, o) {
    o = o || {};
    for (const k of Object.keys(o)) {
      if (HOLD_OPTS.indexOf(k) === -1)
        throw new TypeError("AKPOST.holdInk: unknown option '" + k + "' (known: " +
                            HOLD_OPTS.join(", ") + ")");
    }
    const m = /^#?([0-9a-fA-F]{6})$/.exec(String(o.hex || ""));
    if (!m) throw new TypeError("AKPOST.holdInk: hex must be a #RRGGBB string, got " + JSON.stringify(o.hex));
    const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    const LT = new Float32Array(256);
    for (let i = 0; i < 256; i++) LT[i] = lin(i);
    const fx = (t) => (t > 0.008856451679 ? Math.cbrt(t) : t / 0.12841854934 + 4 / 29);
    const fxi = (t) => (t > 6 / 29 ? t * t * t : 0.12841854934 * (t - 4 / 29));
    const enc = (v) => (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055);
    const toLab = (r, g, b) => {
      const X = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047;
      const Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b;
      const Z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883;
      const fX = fx(X), fY = fx(Y), fZ = fx(Z);
      return [116 * fY - 16, 500 * (fX - fY), 200 * (fY - fZ)];
    };
    const toRgb = (L, a, b) => {            // linear rgb, unclamped
      const fY = (L + 16) / 116, X = 0.95047 * fxi(fY + a / 500), Y = fxi(fY), Z = 1.08883 * fxi(fY - b / 200);
      return [3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z,
              -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z,
              0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z];
    };
    const ink = toLab(LT[parseInt(m[1].slice(0, 2), 16)], LT[parseInt(m[1].slice(2, 4), 16)],
                      LT[parseInt(m[1].slice(4, 6), 16)]);
    const inkC = Math.hypot(ink[1], ink[2]);
    const inkH = Math.atan2(ink[2], ink[1]) * 180 / Math.PI;
    const below = o.below != null ? o.below : 2, above = o.above != null ? o.above : 15;
    const minC = o.minChroma != null ? o.minChroma : 0.45 * inkC;
    const soft = o.soft != null ? o.soft : 3;
    for (const [k, v] of [["below", below], ["above", above], ["minChroma", minC], ["soft", soft]])
      if (typeof v !== "number" || !isFinite(v) || v < 0)
        throw new TypeError("AKPOST.holdInk: " + k + " must be a number 0 or more, got " + JSON.stringify(v));
    const ramp = (x) => (soft > 0 ? Math.min(1, Math.max(0, x / soft)) : (x >= 0 ? 1 : 0));
    const sc = getScale(ctx);
    let x0 = 0, y0 = 0, x1 = ctx.canvas.width, y1 = ctx.canvas.height;
    if (o.rect) {
      const r = o.rect;
      if (!Array.isArray(r) || r.length !== 4 || !r.every((n) => typeof n === "number" && isFinite(n)))
        throw new TypeError("AKPOST.holdInk: rect must be [x, y, w, h] in design px");
      x0 = Math.max(0, Math.floor(r[0] * sc)); y0 = Math.max(0, Math.floor(r[1] * sc));
      x1 = Math.min(x1, Math.ceil((r[0] + r[2]) * sc)); y1 = Math.min(y1, Math.ceil((r[1] + r[3]) * sc));
    }
    if (x1 <= x0 || y1 <= y0) return { px: 0, meanShift: 0 };
    const img = ctx.getImageData(x0, y0, x1 - x0, y1 - y0), d = img.data;
    let n = 0, turn = 0;
    for (let i = 0; i < d.length; i += 4) {
      const R = d[i], G = d[i + 1], B = d[i + 2];
      if (Math.max(R, G) - B < 24) continue;          // no warm chroma to speak of
      const lab = toLab(LT[R], LT[G], LT[B]);
      const C = Math.hypot(lab[1], lab[2]);
      if (C < minC - soft) continue;
      let dh = Math.atan2(lab[2], lab[1]) * 180 / Math.PI - inkH;
      dh = ((dh + 540) % 360) - 180;
      if (dh < -below - soft || dh > above + soft) continue;
      const w = ramp(C - minC + soft) * ramp(dh + below + soft) * ramp(above + soft - dh);
      if (w <= 0) continue;
      const h = (inkH + dh * (1 - w)) * Math.PI / 180, ch = Math.cos(h), sh = Math.sin(h);
      const inG = (q) => q[0] >= -1e-4 && q[1] >= -1e-4 && q[2] >= -1e-4 &&
                         q[0] <= 1.0001 && q[1] <= 1.0001 && q[2] <= 1.0001;
      // keep the pixel's own L* and chroma; where the gamut refuses them at the
      // ink's hue, give up the difference TOWARD THE INK'S OWN (L*, C), which is
      // in gamut by definition, by the least fraction that fits (bisection)
      let rgb = toRgb(lab[0], C * ch, C * sh);
      if (!inG(rgb)) {
        let lo = 0, hi = 1;
        for (let it = 0; it < 14; it++) {
          const t = (lo + hi) / 2, L2 = lab[0] + (ink[0] - lab[0]) * t, C2 = C + (inkC - C) * t;
          const q = toRgb(L2, C2 * ch, C2 * sh);
          if (inG(q)) { hi = t; rgb = q; } else lo = t;
        }
        // no feasible point on that line (the ink's (L*, C) need not be in gamut at a partly
        // turned hue): keep the pixel's own L* and give up chroma instead, which reaches the
        // in-gamut grey at C = 0, so a shadow can never clamp to bright gold (Codex, PR #446)
        if (!inG(rgb)) {
          let cl = 0, chi = C;
          for (let it = 0; it < 14; it++) {
            const c2 = (cl + chi) / 2, q = toRgb(lab[0], c2 * ch, c2 * sh);
            if (inG(q)) cl = c2; else chi = c2;
          }
          rgb = toRgb(lab[0], cl * ch, cl * sh);
        }
      }
      d[i] = Math.round(255 * enc(Math.min(1, Math.max(0, rgb[0]))));
      d[i + 1] = Math.round(255 * enc(Math.min(1, Math.max(0, rgb[1]))));
      d[i + 2] = Math.round(255 * enc(Math.min(1, Math.max(0, rgb[2]))));
      n++; turn += Math.abs(dh * w);
    }
    ctx.putImageData(img, x0, y0);
    return { px: n, meanShift: n ? turn / n : 0 };
  };

  /* Atmospheric-perspective depth grade for LAYERED 2D scenes: call per layer
   * BEFORE drawing it, with its depth d in [0,1]. Returns {fill hints}. This is
   * a recipe helper (math only), the layer code applies it:
   *   const g = AKPOST.depthGrade(d, {atmo:[0.62,0.68,0.76]});
   *   // lerp your layer colors toward g.atmo by g.mix; multiply contrast by
   *   // g.contrast; multiply chroma by g.chroma; ctx.filter = g.blur
   */
  P.depthGrade = function (depth, o) {
    o = o || {};
    const d2 = Math.min(1, Math.max(0, depth));
    return {
      mix: 0.15 + 0.45 * Math.pow(d2, 1.4),            // toward atmosphere color
      contrast: 1 - 0.5 * d2,
      chroma: 1 - 0.6 * d2,
      blur: 'blur(' + (4 * d2 * d2) + 'px)',
      atmo: o.atmo || [0.62, 0.68, 0.76],
    };
  };

  global.AKPOST = P;
})(typeof window !== "undefined" ? window : globalThis);
