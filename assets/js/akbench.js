/* akbench.js — multi-material digital bas-relief, lit by one raking key. (Alaska.Ai, No.74, 2026-10-01)
 *
 * akrelief.js shades ONE material with ONE ramp and no specular and no cast, which is right for a substrate and
 * wrong for a still life of several materials on one bench: wood, ivory, ebony and nickel each need their own
 * albedo and their own sheen, and a raised object needs to throw a shadow on the surface it stands on. This is
 * the bench for that. Plan view, height in CSS px out of the table.
 *
 *   AKBENCH.relief(cx, {x, y, w, h, scale: 2,
 *     height: (X, Y) => px,            // CSS-px coordinates on the page, height in CSS px
 *     material: (X, Y) => id,          // integer material id
 *     albedo: (X, Y, id) => [r, g, b], // linear 0..1, may vary (grain)
 *     spec: {id: [strength, shininess]},
 *     light: {azDeg, elDeg},           // azimuth 0 = toward the top of the frame, clockwise
 *     ambient: 0.22, diffuse: 0.95, ao: 0.9, shadow: 0.85, softness: 10});
 *
 * Height is evaluated once per device pixel into a buffer. Normals are a Sobel of that buffer. Cavity occlusion
 * compares each height with a box-blurred copy. The cast is a march from each pixel toward the key across the
 * buffer, with a penumbra from the closest miss. Everything is deterministic. Text never goes here.
 */
(function (global) {
  "use strict";
  function boxBlur(src, W, H, r) {
    const tmp = new Float32Array(W * H), out = new Float32Array(W * H);
    for (let y = 0; y < H; y++) { let s = 0; const o = y * W;
      for (let x = -r; x <= r; x++) s += src[o + Math.max(0, Math.min(W - 1, x))];
      for (let x = 0; x < W; x++) { tmp[o + x] = s / (2 * r + 1); s += src[o + Math.min(W - 1, x + r + 1)] - src[o + Math.max(0, x - r)]; } }
    for (let x = 0; x < W; x++) { let s = 0;
      for (let y = -r; y <= r; y++) s += tmp[Math.max(0, Math.min(H - 1, y)) * W + x];
      for (let y = 0; y < H; y++) { out[y * W + x] = s / (2 * r + 1); s += tmp[Math.min(H - 1, y + r + 1) * W + x] - tmp[Math.max(0, y - r) * W + x]; } }
    return out;
  }
  function relief(cx, o) {
    const sc = o.scale || 2, X0 = Math.round(o.x * sc), Y0 = Math.round(o.y * sc), W = Math.round(o.w * sc), H = Math.round(o.h * sc);
    const hb = new Float32Array(W * H), mb = new Uint8Array(W * H);
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const X = (X0 + i + 0.5) / sc, Y = (Y0 + j + 0.5) / sc;
      hb[j * W + i] = o.height(X, Y) * sc; mb[j * W + i] = o.material(X, Y);
    }
    const az = (o.light && o.light.azDeg != null ? o.light.azDeg : 135) * Math.PI / 180, el = (o.light && o.light.elDeg != null ? o.light.elDeg : 26) * Math.PI / 180;
    const L = [Math.sin(az) * Math.cos(el), -Math.cos(az) * Math.cos(el), Math.sin(el)];   // screen x right, y down, z up
    const Hv = (() => { const h = [L[0], L[1], L[2] + 1], l = Math.hypot(h[0], h[1], h[2]); return [h[0] / l, h[1] / l, h[2] / l]; })();
    const blur = boxBlur(hb, W, H, Math.round((o.aoRadius || 7) * sc));
    const amb = o.ambient != null ? o.ambient : 0.22, dif = o.diffuse != null ? o.diffuse : 0.95, aoK = o.ao != null ? o.ao : 0.9, shK = o.shadow != null ? o.shadow : 0.85;
    const soft = (o.softness || 10) * sc, tanEl = Math.tan(el), stepLen = 1.5, maxLen = (o.castLength || 140) * sc;
    const lx = L[0] / Math.hypot(L[0], L[1]), ly = L[1] / Math.hypot(L[0], L[1]);
    const img = cx.createImageData(W, H), d = img.data, spec = o.spec || {};
    const at = (i, j) => hb[Math.max(0, Math.min(H - 1, j)) * W + Math.max(0, Math.min(W - 1, i))];
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const k = j * W + i, h0 = hb[k];
      const gx = (at(i + 1, j - 1) + 2 * at(i + 1, j) + at(i + 1, j + 1) - at(i - 1, j - 1) - 2 * at(i - 1, j) - at(i - 1, j + 1)) / 8;
      const gy = (at(i - 1, j + 1) + 2 * at(i, j + 1) + at(i + 1, j + 1) - at(i - 1, j - 1) - 2 * at(i, j - 1) - at(i + 1, j - 1)) / 8;
      let nx = -gx, ny = -gy, nz = 1; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
      const lam = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
      // the cast: march toward the key; the penumbra is the closest miss over distance
      let vis = 1;
      for (let t = stepLen; t < maxLen; t += stepLen * (1 + t / 120)) {
        const hh = at(Math.round(i + lx * t), Math.round(j + ly * t)), ray = h0 + t * tanEl;
        const over = hh - ray; if (over > 0) { vis = 0; break; }
        vis = Math.min(vis, -over / (soft * (0.15 + t / maxLen)) );
      }
      vis = Math.max(0, Math.min(1, vis));
      const cav = Math.max(0, blur[k] - h0) / sc, ao = Math.max(0, 1 - aoK * Math.min(1, cav / 6));
      const m = mb[k], X = (X0 + i + 0.5) / sc, Y = (Y0 + j + 0.5) / sc, a = o.albedo(X, Y, m);
      const sh = 1 - shK * (1 - vis);
      const sp = spec[m] ? spec[m][0] * Math.pow(Math.max(0, nx * Hv[0] + ny * Hv[1] + nz * Hv[2]), spec[m][1]) * sh : 0;
      const lightT = amb * ao + dif * lam * sh;
      for (let c = 0; c < 3; c++) { let v = a[c] * lightT + sp; v = v / (1 + v * 0.35); d[k * 4 + c] = 255 * Math.pow(Math.max(0, Math.min(1, v)), 1 / 2.2); }
      d[k * 4 + 3] = 255;
    }
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); cx.putImageData(img, X0, Y0); cx.restore();
    return {x: X0, y: Y0, w: W, h: H};
  }
  global.AKBENCH = {relief};
})(typeof window !== "undefined" ? window : globalThis);
