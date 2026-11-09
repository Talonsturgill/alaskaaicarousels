/* aklaid.js — one sheet of laid paper as a thickness field, read in two lights.
 *
 * Written 2026-11-08 for carousel No.109 ("A watermark is not a credit line"),
 * whose argument is the difference between REFLECTED light (what a reader of
 * the page sees) and TRANSMITTED light (what someone holding it to a light
 * table sees). Every paper frame of that deck reads ONE field through this
 * module so the sheet is the same object on every frame (No.104: a shared
 * ground's faults show on every frame at once, so it is reviewed on one frame
 * first).
 *
 * THE FIELD, T(u, v), in sheet coordinates (design px of the sheet, origin top
 * left), about 1.0 everywhere:
 *   - formation flocs: 3 octaves of value-noise fbm on a Math.imul hash (No.107:
 *     a hash multiplied past 2^53 streaks; imul never does), amplitude +-0.16
 *   - laid lines: horizontal, `laid` px pitch with +-8 percent jitter per line,
 *     the wire leaving the paper thinner (-0.06 at the line centre)
 *   - chain lines: vertical, `chain` px pitch, a thin core (-0.10) with a
 *     pulp-shadow flank either side (+0.04), the real look of a chain line
 *   - the watermark wire: an oval with the letters A and I, thinning the paper
 *     by `wmDepth` (default 0.22) within ~2 px of the wire
 *
 * READING IT:
 *   reflected  height = T * relief; Lambert against a key (dx, dy, el) plus
 *              ambient, mapped through a lo..hi colour ramp
 *   transmitted  L = panel * base * 10^(-tk * (T - 1)), so thinner paper
 *              (the wire, the laid lines, thin flocs) is brighter
 *
 * USAGE
 *   AKLAID.paint(ctx, {             // ctx: a 2x canvas context, scaled (2,2)
 *     sheet: {w: 940, h: 760, cx: 600, cy: 940, rot: -0.087, s: 1},
 *     field: {seed: 109001, laid: 7, chain: 72, wm: {u: 470, v: 640, s: 1}},
 *     mode: (x, y) => 0,            // 0 reflected, 1 transmitted, per design px
 *     key: {dx: -0.67, dy: -0.74, el: 18}, amb: 0.28, relief: 3.0,
 *     lo: '#6F7A86', hi: '#B7C0C9', panel: '#DDEBF5', tk: 0.9, base: 0.80,
 *     deckle: 5,                    // ragged edge amplitude, design px
 *     glow: 0,                      // transmitted only: brightening near the wire (0.6 to 1.2 reads)
 *     falloff: 0.24, flocTone: 0.10 // reflected: key ramp across the sheet, low-frequency floc tone
 *     cast: {parts, color},         // optional: a two-part cast drawn UNDER the sheet first
 *   }) -> {mask, bbox}              // mask: a device-res canvas of the sheet alpha
 *
 *   AKLAID.field(opts.field) -> {T(u, v)}     // the raw field, for GPU textures
 *   AKLAID.wmSegments(u, v, s)               // the wire, as [[x0,y0,x1,y1], ...]
 *
 * Deterministic: no Math.random anywhere.
 */
(function (global) {
  "use strict";
  const L = {};

  function hash(ix, iy, seed) {
    let h = (Math.imul(ix | 0, 374761393) + Math.imul(iy | 0, 668265263) + Math.imul(seed | 0, 1442695041)) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  }
  function vnoise(x, y, seed) {
    const ix = Math.floor(x), iy = Math.floor(y);
    const fx = x - ix, fy = y - iy;
    const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
    const a = hash(ix, iy, seed), b = hash(ix + 1, iy, seed);
    const c = hash(ix, iy + 1, seed), d = hash(ix + 1, iy + 1, seed);
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy;
  }
  function fbm3(x, y, seed) {
    return 0.55 * vnoise(x / 38, y / 38, seed) +
           0.30 * vnoise(x / 15 + 17.3, y / 15 - 4.1, seed + 101) +
           0.15 * vnoise(x / 6 - 9.7, y / 6 + 31.9, seed + 202);
  }
  L.hash = hash; L.vnoise = vnoise; L.fbm3 = fbm3;

  /* The watermark: an oval and the letters A and I, as line segments in sheet
   * px around (u, v), scaled by s. Hand authored, never a font. */
  L.wmSegments = function (u, v, s) {
    s = s || 1;
    const seg = [];
    const n = 72, rx = 75 * s, ry = 48 * s;
    for (let i = 0; i < n; i++) {
      const a0 = (i / n) * Math.PI * 2, a1 = ((i + 1) / n) * Math.PI * 2;
      seg.push([u + rx * Math.cos(a0), v + ry * Math.sin(a0), u + rx * Math.cos(a1), v + ry * Math.sin(a1)]);
    }
    const P = (x, y) => [u + x * s, v + y * s];
    const add = (a, b) => seg.push([a[0], a[1], b[0], b[1]]);
    add(P(-34, 28), P(-17, -28)); add(P(-17, -28), P(0, 28));      // A
    add(P(-27, 8), P(-7, 8));                                        // A bar
    add(P(24, -28), P(24, 28));                                      // I
    add(P(14, -28), P(34, -28)); add(P(14, 28), P(34, 28));          // I serifs
    return seg;
  };
  function segDist(px, py, s) {
    const vx = s[2] - s[0], vy = s[3] - s[1];
    const wx = px - s[0], wy = py - s[1];
    const t = Math.max(0, Math.min(1, (wx * vx + wy * vy) / (vx * vx + vy * vy || 1)));
    const dx = wx - t * vx, dy = wy - t * vy;
    return Math.sqrt(dx * dx + dy * dy);
  }

  L.field = function (f) {
    f = f || {};
    const seed = f.seed == null ? 109001 : f.seed;
    const laid = f.laid || 7, chain = f.chain || 72, chainOff = f.chainOff || 0;
    const flocAmp = f.floc == null ? 0.16 : f.floc;
    const laidAmp = f.laidAmp == null ? 0.022 : f.laidAmp;
    const chainAmp = f.chainAmp == null ? 0.075 : f.chainAmp;
    const wmDepth = f.wmDepth == null ? 0.22 : f.wmDepth;
    const fs = f.scale || 1;                      // field feature scale (macro frames > 1)
    const segs = f.wm ? L.wmSegments(f.wm.u, f.wm.v, f.wm.s || 1) : null;
    let bb = null;
    if (segs) {
      bb = [1e9, 1e9, -1e9, -1e9];
      for (const s of segs) {
        bb[0] = Math.min(bb[0], s[0], s[2]); bb[1] = Math.min(bb[1], s[1], s[3]);
        bb[2] = Math.max(bb[2], s[0], s[2]); bb[3] = Math.max(bb[3], s[1], s[3]);
      }
      const pad = 8 * (f.wm.s || 1); bb[0] -= pad; bb[1] -= pad; bb[2] += pad; bb[3] += pad;
    }
    const wmW = 1.6 * (f.wm && f.wm.s ? f.wm.s : 1);
    function T(u, v) {
      const x = u / fs, y = v / fs;
      let t = 1 + flocAmp * 2 * (fbm3(x, y, seed) - 0.5);
      // laid lines (horizontal), jittered per line
      const warp = 1.3 * (vnoise(x / 47, y / 9, seed + 404) - 0.5);
      const li = Math.floor((y + warp) / laid);
      const jit = (hash(li, 7, seed + 303) - 0.5) * 0.30 * laid;
      const ly = (y + warp - jit) / laid;
      const lf = ly - Math.floor(ly) - 0.5;
      const lmod = 0.55 + 0.9 * vnoise(x / 23 + li * 3.1, li * 0.7, seed + 505);
      t -= laidAmp * lmod * Math.exp(-(lf * lf) / 0.03);
      // chain lines (vertical): core plus pulp-shadow flanks
      const cx = (x - chainOff) / chain;
      const cd = (cx - Math.round(cx)) * chain;        // px from nearest chain line
      const ad = Math.abs(cd);
      t -= chainAmp * Math.exp(-(ad * ad) / 1.4);
      t += 0.04 * Math.exp(-((ad - 4.2) * (ad - 4.2)) / 5.0);
      if (segs && u >= bb[0] && u <= bb[2] && v >= bb[1] && v <= bb[3]) {
        let d = 1e9;
        for (const s of segs) { const q = segDist(u, v, s); if (q < d) d = q; }
        t -= wmDepth * Math.exp(-(d * d) / (wmW * wmW));
      }
      return t;
    }
    const glowW = 6.5 * (f.wm && f.wm.s ? f.wm.s : 1);
    function G(u, v) {             // 0..1, how close (u, v) is to the wire, wide falloff
      if (!segs || u < bb[0] - 10 || u > bb[2] + 10 || v < bb[1] - 10 || v > bb[3] + 10) return 0;
      let d = 1e9;
      for (const s of segs) { const q = segDist(u, v, s); if (q < d) d = q; }
      return Math.exp(-(d * d) / (glowW * glowW)) * 0.55 + Math.exp(-(d * d) / (wmW * wmW * 2.2)) * 0.45;
    }
    return { T: T, G: G, seed: seed };
  };

  function hex(c) {
    if (Array.isArray(c)) return c;
    const m = /^#?([0-9a-f]{6})$/i.exec(c);
    const n = parseInt(m[1], 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  L.hex = hex;

  L.paint = function (ctx, o) {
    const S = o.sheet, F = L.field(o.field);
    const tr = ctx.getTransform(); const k = tr.a || 2;     // device px per design px
    const W = ctx.canvas.width, H = ctx.canvas.height;
    const cr = Math.cos(S.rot || 0), sr = Math.sin(S.rot || 0), ss = S.s || 1;
    // bounding box of the rotated sheet in device px
    const corners = [[-S.w / 2, -S.h / 2], [S.w / 2, -S.h / 2], [S.w / 2, S.h / 2], [-S.w / 2, S.h / 2]].map(p => {
      const x = S.cx + (p[0] * cr - p[1] * sr) * ss, y = S.cy + (p[0] * sr + p[1] * cr) * ss;
      return [x * k, y * k];
    });
    const dk = (o.deckle == null ? 5 : o.deckle);
    let x0 = Math.floor(Math.min(...corners.map(c => c[0])) - dk * k - 2), x1 = Math.ceil(Math.max(...corners.map(c => c[0])) + dk * k + 2);
    let y0 = Math.floor(Math.min(...corners.map(c => c[1])) - dk * k - 2), y1 = Math.ceil(Math.max(...corners.map(c => c[1])) + dk * k + 2);
    if (o.clip) { x0 = Math.max(x0, o.clip[0] * k); y0 = Math.max(y0, o.clip[1] * k); x1 = Math.min(x1, (o.clip[0] + o.clip[2]) * k); y1 = Math.min(y1, (o.clip[1] + o.clip[3]) * k); }
    x0 = Math.max(0, x0); y0 = Math.max(0, y0); x1 = Math.min(W, x1); y1 = Math.min(H, y1);
    const bw = x1 - x0, bh = y1 - y0;
    if (bw <= 0 || bh <= 0) return { mask: null, bbox: [0, 0, 0, 0] };
    const Tb = new Float32Array(bw * bh), A = new Float32Array(bw * bh), Gb = new Float32Array(bw * bh), Eb = new Float32Array(bw * bh), Sb = new Int8Array(bw * bh), Kb = new Float32Array(bw * bh);
    const glow = o.glow || 0, falloff = o.falloff == null ? 0.42 : o.falloff, flocTone = o.flocTone == null ? 0.14 : o.flocTone;
    const kd = o.key || { dx: -0.67, dy: -0.74 }, kdn = Math.hypot(kd.dx, kd.dy) || 1;
    const seed = F.seed;
    for (let j = 0; j < bh; j++) {
      const y = (y0 + j + 0.5) / k;
      for (let i = 0; i < bw; i++) {
        const x = (x0 + i + 0.5) / k;
        const dx = (x - S.cx) / ss, dy = (y - S.cy) / ss;
        const u = dx * cr + dy * sr + S.w / 2, v = -dx * sr + dy * cr + S.h / 2;
        // deckle: a ragged edge distance
        const eu = Math.min(u, S.w - u), ev = Math.min(v, S.h - v);
        let e = Math.min(eu, ev);
        if (e > -dk - 2 && e < dk + 2) {
          const along = eu < ev ? v + (u > S.w / 2 ? 5000 : 0) : u + (v > S.h / 2 ? 9000 : 0);
          e += dk * (1.6 * (vnoise(along / 26, 3.1, seed + 909) - 0.5) + 0.7 * (vnoise(along / 6.5, 8.7, seed + 919) - 0.5));
        }
        const a = Math.max(0, Math.min(1, e * k * 0.5));
        const pi = j * bw + i;
        A[pi] = a;
        if (a > 0) {
          Tb[pi] = F.T(u, v);
          if (glow) Gb[pi] = F.G(u, v);
          Eb[pi] = e;
          Sb[pi] = (eu < ev) ? (u < S.w / 2 ? 0 : 2) : (v < S.h / 2 ? 1 : 3);   // 0 left, 1 top, 2 right, 3 bottom
          // where this point sits along the key direction across the sheet: 1 lit corner, 0 lee corner
          const along = ((u - S.w / 2) * kd.dx / kdn + (v - S.h / 2) * kd.dy / kdn) / (0.5 * Math.hypot(S.w, S.h));
          Kb[pi] = 0.5 + 0.5 * along;
          Kb[pi] += flocTone * 2 * (vnoise(u / 31, v / 31, seed + 606) - 0.5);
        }
      }
    }
    const mcanvas = document.createElement('canvas'); mcanvas.width = W; mcanvas.height = H;
    const mctx = mcanvas.getContext('2d'); const mimg = mctx.createImageData(bw, bh), md = mimg.data;
    for (let p = 0; p < bw * bh; p++) md[p * 4 + 3] = Math.round(A[p] * 255);
    mctx.putImageData(mimg, x0, y0);
    if (o.cast) L.cast(ctx, mcanvas, o.cast);
    const img = ctx.getImageData(x0, y0, bw, bh), d = img.data;
    const key = o.key || { dx: -0.67, dy: -0.74, el: 18 };
    const el = (key.el || 18) * Math.PI / 180, kn = Math.hypot(key.dx, key.dy) || 1;
    const lx = key.dx / kn * Math.cos(el), ly = key.dy / kn * Math.cos(el), lz = Math.sin(el);
    const amb = o.amb == null ? 0.28 : o.amb, relief = (o.relief == null ? 3.0 : o.relief) * ss;
    const lo = hex(o.lo || '#6F7A86'), hi = hex(o.hi || '#B7C0C9'), pn = hex(o.panel || '#DDEBF5');
    const tk = o.tk == null ? 0.9 : o.tk, base = o.base == null ? 0.80 : o.base;
    const flat = lz;
    const mode = o.mode || (() => 0);
    for (let j = 0; j < bh; j++) {
      for (let i = 0; i < bw; i++) {
        const p = j * bw + i, a = A[p];
        if (a <= 0) continue;
        const t = Tb[p];
        const tl = i > 0 && A[p - 1] > 0 ? Tb[p - 1] : t, trr = i < bw - 1 && A[p + 1] > 0 ? Tb[p + 1] : t;
        const tu = j > 0 && A[p - bw] > 0 ? Tb[p - bw] : t, tdn = j < bh - 1 && A[p + bw] > 0 ? Tb[p + bw] : t;
        const hx = (trr - tl) * 0.5 * k * relief * 0.45, hy = (tdn - tu) * 0.5 * k * relief * 0.45;
        const nl = 1 / Math.sqrt(hx * hx + hy * hy + 1);
        const lam = Math.max(0, (-hx * lx - hy * ly + lz) * nl);
        let b = amb + (1 - amb) * (lam / flat) * 0.78;
        b -= (1 - t) * 0.0;                                   // (thinner paper is not darker in reflection)
        b *= 1 + (t - 1) * 1.6;                               // floc and laid structure as tone: thicker paper reads a touch brighter
        b *= (1 - falloff) + falloff * 2 * Kb[p] * 0.85;
        const ed = Eb[p];
        if (ed < 2.6) {                 // a lit rim on the edges that face the key, a lee rim on the others
          const r = 1 - ed / 2.6, sd = Sb[p];
          b += (sd === 0 || sd === 1) ? 0.30 * r : -0.24 * r;
        }
        b = Math.max(0, Math.min(1.15, b));
        const rr = lo[0] + (hi[0] - lo[0]) * b, rg = lo[1] + (hi[1] - lo[1]) * b, rb = lo[2] + (hi[2] - lo[2]) * b;
        const x = (x0 + i + 0.5) / k, y = (y0 + j + 0.5) / k;
        const m = Math.max(0, Math.min(1, mode(x, y)));
        let R = rr, G = rg, B = rb;
        if (m > 0) {
          const tt = Math.min(1.3, base * Math.pow(10, -tk * (t - 1)) * (1 + glow * Gb[p]));
          R = R * (1 - m) + Math.min(255, pn[0] * tt) * m;
          G = G * (1 - m) + Math.min(255, pn[1] * tt) * m;
          B = B * (1 - m) + Math.min(255, pn[2] * tt) * m;
        }
        const q = p * 4;
        d[q] = d[q] * (1 - a) + R * a; d[q + 1] = d[q + 1] * (1 - a) + G * a; d[q + 2] = d[q + 2] * (1 - a) + B * a;
        d[q + 3] = 255;
      }
    }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.putImageData(img, x0, y0);
    ctx.restore();
    return { mask: mcanvas, bbox: [x0 / k, y0 / k, bw / k, bh / k] };
  };

  /* A two-part contact cast from a sheet mask: tight and wide, offset toward
   * the lower right (the deck's key is upper left), drawn UNDER the sheet. Call
   * it on the ground before painting the sheet, from a mask made by a first
   * dry run, or paint the cast from AKLAID.rectMask for a known quad. */
  L.cast = function (ctx, mask, o) {
    o = o || {};
    const tr = ctx.getTransform(); const k = tr.a || 2;
    const parts = o.parts || [[7, 9, 5, 0.55], [16, 20, 22, 0.25]];
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    for (const p of parts) {
      const off = document.createElement('canvas'); off.width = mask.width; off.height = mask.height;
      const g = off.getContext('2d');
      g.drawImage(mask, 0, 0);
      g.globalCompositeOperation = 'source-in'; g.fillStyle = o.color || '#05080D'; g.fillRect(0, 0, off.width, off.height);
      ctx.globalAlpha = p[3]; ctx.filter = 'blur(' + (p[2] * k) + 'px)';
      ctx.drawImage(off, p[0] * k, p[1] * k);
    }
    ctx.restore();
  };

  global.AKLAID = L;
})(typeof window !== "undefined" ? window : globalThis);
