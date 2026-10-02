/* akmetrology.js — the inspection-room furniture for Carousel No.75 (2026-10-02).
 *
 * One metrology room: a lapped black granite surface plate, ground-steel instruments coated in layout blue,
 * graduations scribed through the lacquer to bright steel, all under ONE overhead softbox. Every slide composes its
 * own instrument in its own file; this holds only what is the SAME because it is the same room: the light, the
 * granite, the softbox environment, the steel and lacquer materials, the scribed groove, and the grade. It is a
 * classic script (render.py resolves slides into render/.resolved, where a relative module import can't reach).
 *
 *   AKMET.LIGHT              {azDeg: 0, elDeg: 55}: from the top of the frame, casts travel straight down.
 *   AKMET.KEY_DIR            world direction from the subject toward the softbox, (0, 0.86, -0.5) normalised.
 *   AKMET.graniteCanvas(n, seed)       a square granite albedo canvas: blue-noise flecks, sparse mica.
 *   AKMET.softboxEnv(THREE, R, o)      PMREM environment: one large overhead softbox behind the subject, cool room.
 *   AKMET.mats(THREE, R, o)            {steel, lapped, granite, lacquer(texture), glass}
 *   AKMET.groove(cx, x0, y0, x1, y1, o)  one scribed groove through lacquer: lit floor, dark lee lip, burr, jitter.
 *   AKMET.lacquer(cx, x, y, w, h, o)   layout-blue lacquer with Lambert-lit orange peel and a worn chamfer.
 *   AKMET.grade(cx, exposure, o)       the deck's one grade; exposure (stops) is the only thing that moves.
 */
(function (global) {
  "use strict";
  const M = {};
  M.LIGHT = {azDeg: 0, elDeg: 55};
  M.KEY_DIR = (function () { const v = [0, 0.86, -0.5], l = Math.hypot(v[0], v[1], v[2]); return [v[0] / l, v[1] / l, v[2] / l]; })();
  function rng(seed) { let s = seed >>> 0; return function () { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  M.rng = rng;

  M.graniteCanvas = function (n, seed) {
    const c = document.createElement('canvas'); c.width = c.height = n; const x = c.getContext('2d');
    const r = rng(seed || 7);
    x.fillStyle = '#141A22'; x.fillRect(0, 0, n, n);
    const img = x.getImageData(0, 0, n, n), d = img.data;
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const k = (j * n + i) * 4, g = (global.AK && AK.fbm2) ? AK.fbm2(i * 0.012, j * 0.012, {octaves: 4}) : 0;
      const v = 0.92 + 0.10 * g + (r() - 0.5) * 0.10;
      d[k] = 20 * v; d[k + 1] = 26 * v; d[k + 2] = 34 * v; d[k + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    // flecks: dark feldspar and grey quartz, then sparse mica glints
    for (let f = 0; f < n * n * 0.010; f++) { const px = r() * n, py = r() * n, s = 0.6 + r() * 1.8;
      x.fillStyle = r() < 0.55 ? 'rgba(5,7,10,0.85)' : 'rgba(58,69,82,0.75)'; x.beginPath(); x.ellipse(px, py, s, s * (0.5 + r() * 0.6), r() * 3.14, 0, 6.283); x.fill(); }
    for (let f = 0; f < n * n * 0.0006; f++) { const px = r() * n, py = r() * n; x.fillStyle = 'rgba(217,226,234,' + (0.5 + r() * 0.5).toFixed(2) + ')'; x.fillRect(px, py, 1, 1); }
    return c;
  };

  M.softboxEnv = function (THREE, R, o) {
    o = o || {};
    const env = new THREE.Scene();
    env.add(new THREE.Mesh(new THREE.BoxGeometry(40, 20, 40), new THREE.MeshBasicMaterial({color: 0x070A10, side: THREE.BackSide})));
    const panel = (w, h, col, k, pos, rot) => { const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({color: col, side: THREE.DoubleSide})); p.material.color.multiplyScalar(k); p.position.set(...pos); p.rotation.set(...rot); env.add(p); };
    panel(9, 6, 0xF2F4F6, o.softbox || 9, [0, 8.5, -4.5], [Math.PI / 2 + 0.5, 0, 0]);   // the softbox, overhead and behind
    panel(30, 6, 0x3A5274, o.front == null ? 0.55 : o.front, [0, 1.5, 12], [0, Math.PI, 0]);                        // cool room in front
    { const gc = document.createElement('canvas'); gc.width = 8; gc.height = 256; const g = gc.getContext('2d'), gr = g.createLinearGradient(0, 0, 0, 256);
      gr.addColorStop(0, '#05070A'); gr.addColorStop(0.35, '#8C96A4'); gr.addColorStop(0.55, '#5A6676'); gr.addColorStop(1, '#0A0E14'); g.fillStyle = gr; g.fillRect(0, 0, 8, 256);
      const tx = new THREE.CanvasTexture(gc); const m = new THREE.MeshBasicMaterial({map: tx, side: THREE.DoubleSide}); m.color.multiplyScalar(o.backdrop == null ? 1.0 : o.backdrop);
      const p = new THREE.Mesh(new THREE.PlaneGeometry(24, 9), m); p.position.set(0, 2.6, -10); env.add(p); }   // the far wall, lit by the softbox: what lapped tops reflect
    panel(20, 10, 0x0C1016, 0.8, [0, -4, 0], [-Math.PI / 2, 0, 0]);                     // floor bounce
    const pm = new THREE.PMREMGenerator(R.renderer); R.scene.environment = pm.fromScene(env, 0.03).texture; pm.dispose();
    R.scene.environmentIntensity = o.intensity || 1.0;
    // the shadow-casting key along the softbox direction, and a cool hemisphere fill at one sixth
    const key = new THREE.DirectionalLight(0xF4F1EA, o.key || 3.2), D = M.KEY_DIR, dist = o.dist || 8;
    key.position.set(D[0] * dist, D[1] * dist, D[2] * dist); key.castShadow = true; key.shadow.mapSize.set(4096, 4096);
    const sc = o.shadowBox || 3; Object.assign(key.shadow.camera, {left: -sc, right: sc, top: sc, bottom: -sc, near: 0.5, far: 30});
    key.shadow.bias = -0.0003; key.shadow.normalBias = 0.02; key.shadow.radius = o.shadowRadius || 6; R.scene.add(key);
    R.scene.add(new THREE.HemisphereLight(0x2B4A6F, 0x0C1016, (o.key || 3.2) / 6));
    // the room's cool bounce off the front, so faces turned to the reader carry their own material instead of black
    const fill = new THREE.DirectionalLight(0xB8CCE4, o.fill == null ? (o.key || 3.2) / 4 : o.fill); fill.position.set(0.3, 1.2, 6); R.scene.add(fill);
    return key;
  };

  M.mats = function (THREE, R, o) {
    o = o || {};
    const gc = M.graniteCanvas(1024, o.seed || 75), gt = new THREE.CanvasTexture(gc);
    gt.colorSpace = THREE.SRGBColorSpace; gt.wrapS = gt.wrapT = THREE.RepeatWrapping; gt.repeat.set(o.graniteRepeat || 3, o.graniteRepeat || 3);
    gt.anisotropy = R.renderer.capabilities.getMaxAnisotropy();
    return {
      granite: new THREE.MeshPhysicalMaterial({map: gt, roughness: 0.4, metalness: 0, clearcoat: 0.3, clearcoatRoughness: 0.22}),
      steel: new THREE.MeshPhysicalMaterial({color: 0x9AA6B2, metalness: 1, roughness: 0.34}),
      lapped: (function () {   // lapped steel: fine overlapping arcs from the lapping plate, in albedo and roughness
        const c = document.createElement('canvas'); c.width = c.height = 1024; const x = c.getContext('2d'), r = rng((o.seed || 75) + 3);
        x.fillStyle = '#B4BECA'; x.fillRect(0, 0, 1024, 1024);
        for (let i = 0; i < 2600; i++) { const cx0 = r() * 1024, cy0 = r() * 1024, rad = 60 + r() * 260, a0 = r() * 6.283;
          x.strokeStyle = r() < 0.5 ? 'rgba(232,238,244,0.10)' : 'rgba(70,80,92,0.10)'; x.lineWidth = 0.6 + r() * 0.8;
          x.beginPath(); x.arc(cx0, cy0, rad, a0, a0 + 0.5 + r() * 0.9); x.stroke(); }
        const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
        tex.anisotropy = R.renderer.capabilities.getMaxAnisotropy();
        return new THREE.MeshPhysicalMaterial({map: tex, roughnessMap: tex, color: 0xFFFFFF, metalness: 1, roughness: 0.42});
      })(),
      glass: new THREE.MeshPhysicalMaterial({color: 0xDDE6EE, metalness: 0, roughness: 0.04, transparent: true, opacity: 0.18, clearcoat: 1, envMapIntensity: 3, depthWrite: false}),
      lacquer: function (tex) { return new THREE.MeshPhysicalMaterial({map: tex, color: 0xFFFFFF, metalness: 0.15, roughness: 0.42, clearcoat: 0.6, clearcoatRoughness: 0.3}); },
      graniteCanvas: gc
    };
  };

  // one scribed groove: a bright floor, a dark lip on the side away from the key (below, since the key is above),
  // and a thin burr catching light on the lit side. Width jitters per segment from a seeded generator.
  M.groove = function (cx, x0, y0, x1, y1, o) {
    o = o || {};
    const r = rng(o.seed || 1), w = o.w || 1.25, L = Math.hypot(x1 - x0, y1 - y0), n = Math.max(2, Math.round(L / 6));
    const ux = (x1 - x0) / L, uy = (y1 - y0) / L, nx = -uy, ny = ux;          // normal; lee side is +y on screen
    const lee = ny >= 0 ? 1 : -1;
    for (let pass = 0; pass < 3; pass++) {
      cx.beginPath();
      for (let i = 0; i <= n; i++) {
        const t = i / n, jw = w * (1 + (r() - 0.5) * 0.12) * (o.taper ? Math.sin(Math.PI * Math.min(1, Math.max(0.05, t))) ** 0.25 : 1);
        const off = pass === 0 ? 0 : pass === 1 ? lee * (jw * 0.5 + 0.55) : -lee * (jw * 0.5 + 0.45);
        const px = x0 + (x1 - x0) * t + nx * off, py = y0 + (y1 - y0) * t + ny * off;
        if (i === 0) cx.moveTo(px, py); else cx.lineTo(px, py);
      }
      cx.lineCap = 'butt';
      if (pass === 0) { cx.strokeStyle = o.floor || '#E3ECF6'; cx.lineWidth = w; }
      else if (pass === 1) { cx.strokeStyle = o.lip || 'rgba(11,28,64,0.95)'; cx.lineWidth = 0.8; }
      else { cx.strokeStyle = o.burr || 'rgba(190,214,240,0.55)'; cx.lineWidth = 0.6; }
      cx.stroke();
    }
  };

  // layout-blue lacquer: a smooth orange-peel heightfield lit by the declared key, thinning to bright steel at a
  // worn chamfer along one edge. Drawn per device pixel into the rect (design px), backing scale sc.
  M.lacquer = function (cx, x, y, w, h, o) {
    o = o || {};
    const sc = o.scale || 2, X0 = Math.round(x * sc), Y0 = Math.round(y * sc), W = Math.round(w * sc), H = Math.round(h * sc);
    const img = cx.createImageData(W, H), d = img.data, cham = (o.chamfer || 0) * sc, side = o.chamferSide || 'bottom';
    const base = o.base || [31, 74, 150], deep = o.deep || [19, 48, 106], steel = [200, 209, 219];
    const el = 55 * Math.PI / 180, L = [0, -Math.cos(el), Math.sin(el)];
    const f = (i, j) => (global.AK && AK.fbm2) ? AK.fbm2((X0 + i) * 0.03 / sc, (Y0 + j) * 0.03 / sc, {octaves: 4}) : 0;
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const k = (j * W + i) * 4;
      const gx = (f(i + 1, j) - f(i - 1, j)) * (o.peel || 5.5), gy = (f(i, j + 1) - f(i, j - 1)) * (o.peel || 5.5);
      let nx = -gx, ny = -gy, nz = 1; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
      const lam = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
      const v = (o.ambient || 0.55) + 0.5 * lam + (o.falloff ? o.falloff((X0 + i) / sc, (Y0 + j) / sc) : 0);
      let c = [0, 1, 2].map(q => deep[q] + (base[q] - deep[q]) * Math.min(1, Math.max(0, v)));
      // worn chamfer: the lacquer thins to steel over the last `cham` device px of the chosen edge
      const dist = side === 'bottom' ? H - 1 - j : side === 'top' ? j : side === 'left' ? i : W - 1 - i;
      if (cham > 0 && dist < cham) {   // a crisp worn bevel: bright steel line at the lacquer's edge, falling darker toward the arris
        const s = dist / cham, edge = cham - dist < 2 * sc ? 1.18 : 1, lit = (side === 'bottom' ? 0.42 + 0.4 * s : 0.7 + 0.3 * s) * edge;
        c = steel.map(sv => Math.min(255, sv * lit)); }
      d[k] = c[0]; d[k + 1] = c[1]; d[k + 2] = c[2]; d[k + 3] = 255;
    }
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); cx.putImageData(img, X0, Y0); cx.restore();
  };

  M.grade = function (cx, exposure, o) {
    o = o || {};
    if (!global.AKPOST) return;
    AKPOST.grade(cx, {w: 1080, h: 1350, exposure: exposure || 0, saturation: 0.92, contrast: 1.08, filmic: o.filmic !== false,
      lift: [0.008, 0.012, 0.022], gain: [1.012, 1.0, 0.985], vignette: o.vignette == null ? 0.14 : o.vignette,
      bloom: o.bloom ? {threshold: 0.82, strength: 0.10, radius: 8} : null,
      grain: {amount: 0.035, size: 2, seed: o.seed || 75}, aberration: 0, dither: true, sharpen: o.sharpen == null ? 0.25 : o.sharpen});
  };

  global.AKMET = M;
})(typeof window !== "undefined" ? window : globalThis);
