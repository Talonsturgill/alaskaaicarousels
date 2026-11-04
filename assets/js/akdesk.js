/* akdesk.js -- THE LAMP LEFT ON: one desk, one lamp (2026-11-03, No.104).
 *
 * A classic script (window.AKDESK). Load AFTER noise.js. It holds the parts of
 * that deck's world that every frame shares, so nine frames can show ONE desk
 * from nine cameras and nine renderers without nine re-inventions of it:
 *
 *   - the seeded GROUNDS: walnut grain and oxblood leather as canvases, at any
 *     size. The GPU frames wrap them on meshes as CanvasTextures; the Canvas 2D
 *     frames paint them as the ground and light them per pixel. Same seed, same
 *     grain, so the desk is the same desk on every frame.
 *   - the LAMP: one tungsten key fixed in WORLD space (metres; the desk top is
 *     the plane y = 0, +x right, +z toward the visitor's chair). A GPU frame
 *     gets a SpotLight; a 2D frame gets the same light as a function, through a
 *     top-down mapping from desk metres to design px.
 *   - the SET for GPU frames: the desk top, the blotter, the back wall, the fill.
 *
 * It draws no frame's subject. Each slide models its own object, frames its own
 * camera and writes its own type; what is here is the room it stands in.
 *
 * The light: LAMP = (0.70, 0.62, -0.42) aimed at (0.05, 0, 0.05). From any
 * camera in front of the desk the key comes from the right and the back, so
 * every cast falls toward the lower left. In a top-down frame (screen up is the
 * desk's back, -z) the lamp is off the upper right.
 */
(function (global) {
  "use strict";
  const D = {};
  D.LAMP = [0.70, 0.62, -0.42];
  D.AIM = [0.05, 0.0, 0.05];
  D.TUNGSTEN = [1.0, 0.706, 0.353];       // #FFB45A
  D.FILL = [0.169, 0.290, 0.400];         // #2B4A66, the night window on the left
  D.INK = {
    room: "#05080F", wall: "#0C1320", moulding: "#1A2230",
    walnut: ["#140C08", "#24160F", "#3A2418", "#58371F", "#8A5C35"],
    oxblood: ["#2A0F0F", "#3E1717", "#552020", "#6E2A24"],
  };

  function hex(h) { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function ramp(stops, t) {
    t = Math.max(0, Math.min(1, t)) * (stops.length - 1);
    const i = Math.min(stops.length - 2, Math.floor(t)), f = t - i;
    const a = hex(stops[i]), b = hex(stops[i + 1]);
    return [lerp(a[0], b[0], f), lerp(a[1], b[1], f), lerp(a[2], b[2], f)];
  }
  D.ramp = ramp; D.hex = hex;

  /* ---- grounds ------------------------------------------------------------ */
  // Walnut, quarter-sawn: long figure along x, warped by low-frequency fbm so the
  // grain flows round a slow cathedral, with fine pore streaks and medullary
  // flecks. `scale` is px per metre of desk, so the grain is the same physical
  // size in every frame whatever its canvas size; `offset` [x, y] in metres puts
  // a frame's window onto the one desk.
  D.walnut = function (w, h, o) {
    o = o || {};
    const s = o.scale || 2000, ox = (o.offset || [0, 0])[0], oy = (o.offset || [0, 0])[1];
    const c = document.createElement("canvas"); c.width = w; c.height = h;
    const g = c.getContext("2d"), img = g.createImageData(w, h), d = img.data;
    AK.reseed(o.seed || 2026110300);
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const X = ox + x / s, Y = oy + y / s;             // metres on the desk
        const warp = AK.fbm2(X * 1.1, Y * 2.4, { octaves: 3 }) * 0.035;
        const v = (Y + warp) * 140;                      // ~140 growth lines per metre
        const band = 0.5 + 0.5 * Math.sin(v * Math.PI * 2 + AK.fbm2(X * 0.6, Y * 14, { octaves: 2 }) * 1.6);
        const pores = AK.simplex2(X * 1400, Y * 60) * 0.5 + 0.5;
        const slow = AK.fbm2(X * 0.8, Y * 1.6, { octaves: 3 }) * 0.5 + 0.5;
        const fleck = Math.pow(Math.max(0, AK.simplex2(X * 40, Y * 400)), 8);
        let t = 0.32 + 0.06 * Math.pow(band, 1.4) + 0.20 * slow - 0.10 * Math.pow(pores, 5) + 0.05 * fleck;
        const col = ramp(D.INK.walnut, t);
        const i = (y * w + x) * 4;
        d[i] = col[0]; d[i + 1] = col[1]; d[i + 2] = col[2]; d[i + 3] = 255;
      }
    }
    g.putImageData(img, 0, 0);
    return c;
  };

  // Oxblood blotter leather: a pebble grain (two octaves of cellular-looking
  // simplex ridges at about 1.2 mm), slow mottling, and a darker worn border.
  // Returns {albedo, height} canvases; height is the pebble relief for a normal
  // map or for per-pixel lighting.
  D.leather = function (w, h, o) {
    o = o || {};
    const s = o.scale || 2000, ox = (o.offset || [0, 0])[0], oy = (o.offset || [0, 0])[1];
    const a = document.createElement("canvas"); a.width = w; a.height = h;
    const hh = document.createElement("canvas"); hh.width = w; hh.height = h;
    const ga = a.getContext("2d"), gh = hh.getContext("2d");
    const ia = ga.createImageData(w, h), ih = gh.createImageData(w, h);
    AK.reseed(o.seed || 2026110310);
    const border = o.border || 0;    // px of worn darker edge, 0 for none
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const X = ox + x / s, Y = oy + y / s;
        const p1 = 1 - Math.abs(AK.simplex2(X * 820, Y * 820));
        const p2 = 1 - Math.abs(AK.simplex2(X * 1900 + 7.1, Y * 1900 - 3.3));
        const peb = Math.pow(p1, 3) * 0.7 + Math.pow(p2, 3) * 0.3;
        const mot = AK.fbm2(X * 4, Y * 4, { octaves: 4 }) * 0.5 + 0.5;
        let t = 0.30 + 0.30 * mot + 0.18 * peb;
        if (border) {
          const e = Math.min(x, y, w - 1 - x, h - 1 - y) / border;
          if (e < 1) t *= 0.62 + 0.38 * e;
        }
        const col = ramp(D.INK.oxblood, t);
        const i = (y * w + x) * 4;
        ia.data[i] = col[0]; ia.data[i + 1] = col[1]; ia.data[i + 2] = col[2]; ia.data[i + 3] = 255;
        const hv = Math.round(peb * 255);
        ih.data[i] = ih.data[i + 1] = ih.data[i + 2] = hv; ih.data[i + 3] = 255;
      }
    }
    ga.putImageData(ia, 0, 0); gh.putImageData(ih, 0, 0);
    return { albedo: a, height: hh };
  };

  /* ---- the lamp as a function, for Canvas 2D frames -------------------------- */
  // map: { s: design px per metre, o: [x0, y0] design px of desk origin } for a
  // top-down frame (screen x = x0 + X*s, screen y = y0 + Z*s). Returns
  // light(x, y, hgt) with x, y in DESIGN px and hgt the surface height in metres:
  //   { L: unit vector from the point to the lamp in screen space (x right,
  //        y down, z up), E: illuminance factor 0..~1.4 (inverse square, the
  //        spot's cone with a soft penumbra), F: the cool fill factor }
  D.light2d = function (map, o) {
    o = o || {};
    const s = map.s, x0 = map.o[0], y0 = map.o[1];
    const LX = D.LAMP[0], LY = D.LAMP[1], LZ = D.LAMP[2];
    const ax = D.AIM[0] - LX, ay = D.AIM[1] - LY, az = D.AIM[2] - LZ;
    const al = Math.hypot(ax, ay, az);
    const cosOuter = Math.cos(o.angle || 0.45), cosInner = Math.cos((o.angle || 0.45) * (1 - (o.penumbra || 0.55)));
    const d0 = Math.hypot(ax, ay, az);
    return function (x, y, hgt) {
      const X = (x - x0) / s, Z = (y - y0) / s, Y = hgt || 0;
      let vx = LX - X, vy = LY - Y, vz = LZ - Z;
      const dist = Math.hypot(vx, vy, vz);
      vx /= dist; vy /= dist; vz /= dist;
      const cosA = -(vx * ax + vy * ay + vz * az) / al;
      let cone = (cosA - cosOuter) / (cosInner - cosOuter);
      cone = cone <= 0 ? 0 : cone >= 1 ? 1 : cone * cone * (3 - 2 * cone);
      const E = cone * Math.pow(d0 / dist, 1.6);
      // screen space: x right = +X, y down = +Z, z up = +Y
      return { L: [vx, vz, vy], E, F: 1 };
    };
  };

  /* ---- the desk at a point, for Canvas 2D frames --------------------------- */
  // The same figure as D.walnut / D.leather, evaluated at one point (metres),
  // so a 2D frame can light it per DEVICE pixel without a texture lookup.
  D.walnutAt = function (X, Y) {
    const warp = AK.fbm2(X * 1.1, Y * 2.4, { octaves: 3 }) * 0.035;
    const v = (Y + warp) * 140;
    const band = 0.5 + 0.5 * Math.sin(v * Math.PI * 2 + AK.fbm2(X * 0.6, Y * 14, { octaves: 2 }) * 1.6);
    const pores = AK.simplex2(X * 1400, Y * 60) * 0.5 + 0.5;
    const slow = AK.fbm2(X * 0.8, Y * 1.6, { octaves: 3 }) * 0.5 + 0.5;
    const fleck = Math.pow(Math.max(0, AK.simplex2(X * 40, Y * 400)), 8);
    return ramp(D.INK.walnut, 0.32 + 0.06 * Math.pow(band, 1.4) + 0.20 * slow - 0.10 * Math.pow(pores, 5) + 0.05 * fleck);
  };
  D.leatherH = function (X, Y) {
    const p1 = 1 - Math.abs(AK.simplex2(X * 820, Y * 820));
    const p2 = 1 - Math.abs(AK.simplex2(X * 1900 + 7.1, Y * 1900 - 3.3));
    return Math.pow(p1, 3) * 0.7 + Math.pow(p2, 3) * 0.3;
  };
  D.BLOTTER = { x0: -0.36, x1: 0.26, z0: -0.19, z1: 0.23, edge: 0.024 };

  // Paints the lit desk into a 2x art canvas for a top-down frame. map = {s:
  // design px per metre, o: [x0, y0] design px of the world origin}. The lamp
  // lights it (inverse square, the spot's cone), the walnut takes a broad
  // clearcoat sheen, the leather's pebble is lit from its own normals, and the
  // blotter's edge steps down onto the walnut with a fine dark seam. Returns
  // the ImageData it wrote so the frame can keep shading into it.
  D.desk2d = function (cx, map, o) {
    o = o || {};
    const W = cx.canvas.width, H = cx.canvas.height, k = W / 1080;
    const img = cx.createImageData(W, H), d = img.data;
    const light = D.light2d(map);
    const B = D.BLOTTER, gain = o.gain != null ? o.gain : 1.0, amb = o.ambient != null ? o.ambient : 0.10;
    AK.reseed(o.seed || 2026110300);
    const eps = 0.25 / (map.s * k);
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const dx = x / k, dy = y / k;
        const X = (dx - map.o[0]) / map.s, Z = (dy - map.o[1]) / map.s;
        const Lt = light(dx, dy, 0);
        let col, nx = 0, ny = 0, nz = 1, spec = 0, shade = 1;
        const inB = X > B.x0 && X < B.x1 && Z > B.z0 && Z < B.z1;
        if (inB) {
          const h0 = D.leatherH(X, Z), hx = D.leatherH(X + eps, Z), hy = D.leatherH(X, Z + eps);
          nx = -(hx - h0) * 0.9; ny = -(hy - h0) * 0.9;
          const nl = Math.hypot(nx, ny, 1); nx /= nl; ny /= nl; nz = 1 / nl;
          const mot = AK.fbm2(X * 4, Z * 4, { octaves: 4 }) * 0.5 + 0.5;
          const e = Math.min(X - B.x0, B.x1 - X, Z - B.z0, B.z1 - Z) / B.edge;
          col = ramp(D.INK.oxblood, (0.30 + 0.30 * mot + 0.18 * h0) * (e < 1 ? 0.62 + 0.38 * e : 1));
          spec = 0.10;
        } else {
          col = D.walnutAt(X, Z);
          // the blotter's thickness casts a hairline onto the walnut, down-left of it
          const sx = X + 0.0035, sz = Z - 0.0025;
          if (sx > B.x0 && sx < B.x1 && sz > B.z0 && sz < B.z1) shade = 0.55;
          spec = 0.30;
        }
        const L = Lt.L;
        const diff = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
        const hxv = L[0], hyv = L[1], hzv = L[2] + 1, hl = Math.hypot(hxv, hyv, hzv);
        const nh = Math.max(0, (nx * hxv + ny * hyv + nz * hzv) / hl);
        const sp = spec * Math.pow(nh, inB ? 18 : 60) * Lt.E;
        const e = Lt.E * gain * shade;
        const i = (y * W + x) * 4;
        d[i]     = Math.min(255, col[0] * (amb + 0.169 * 0.35 + e * diff * 1.0 * 1.35) + 255 * sp * 1.0);
        d[i + 1] = Math.min(255, col[1] * (amb + 0.290 * 0.35 + e * diff * 0.84 * 1.35) + 255 * sp * 0.84);
        d[i + 2] = Math.min(255, col[2] * (amb + 0.400 * 0.35 + e * diff * 0.66 * 1.35) + 255 * sp * 0.66);
        d[i + 3] = 255;
      }
    }
    cx.putImageData(img, 0, 0);
    return img;
  };

  // A two-part cast for a 2D frame: a tight seam and a wide ambient, both
  // offset AWAY from the lamp (toward the lower left of a top-down frame).
  // `mask` is a canvas the size of the art canvas whose alpha is the object's
  // footprint; `lift` is the object's height in design px (it sets the offset).
  D.cast2d = function (cx, mask, o) {
    o = o || {};
    const W = cx.canvas.width, H = cx.canvas.height, k = W / 1080;
    const dir = o.dir || [-0.80, 0.60], lift = o.lift || 4;
    const parts = o.parts || [
      { off: lift * 0.6, blur: 2.0, alpha: 0.78 },
      { off: lift * 2.2, blur: Math.max(8, lift * 3), alpha: 0.45 }];
    const tmp = document.createElement("canvas"); tmp.width = W; tmp.height = H;
    const tg = tmp.getContext("2d");
    for (const p of parts) {
      tg.clearRect(0, 0, W, H);
      tg.filter = "blur(" + (p.blur * k).toFixed(1) + "px)";
      tg.drawImage(mask, dir[0] * p.off * k, dir[1] * p.off * k);
      tg.filter = "none";
      tg.globalCompositeOperation = "source-in";
      tg.fillStyle = o.color || "#0a0604"; tg.fillRect(0, 0, W, H);
      tg.globalCompositeOperation = "source-over";
      cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
      cx.globalAlpha = p.alpha; cx.globalCompositeOperation = "multiply";
      cx.drawImage(tmp, 0, 0); cx.restore();
    }
  };

  /* ---- the set, for GPU frames --------------------------------------------- */
  // Every function takes THREE and the AKT renderer bundle R.
  D.lamp3 = function (THREE, R, o) {
    o = o || {};
    const spot = new THREE.SpotLight(0xffb45a, o.intensity != null ? o.intensity : 7.5,
      o.distance || 0, o.angle || 0.45, o.penumbra != null ? o.penumbra : 0.55, o.decay != null ? o.decay : 1.6);
    spot.position.set(D.LAMP[0], D.LAMP[1], D.LAMP[2]);
    spot.target.position.set(D.AIM[0], D.AIM[1], D.AIM[2]);
    spot.castShadow = true;
    spot.shadow.mapSize.set(2048, 2048);
    spot.shadow.bias = -0.0002;
    spot.shadow.normalBias = 0.002;
    spot.shadow.radius = o.radius != null ? o.radius : 6;
    spot.shadow.camera.near = 0.05; spot.shadow.camera.far = 3;
    R.scene.add(spot); R.scene.add(spot.target);
    const fill = new THREE.DirectionalLight(0x2b4a66, o.fill != null ? o.fill : 0.55);
    fill.position.set(-2, 1.5, 1.5);
    R.scene.add(fill);
    R.scene.add(new THREE.AmbientLight(0x0c1320, o.ambient != null ? o.ambient : 0.9));
    return { spot, fill };
  };

  // Reflections that agree with the lamp: a dark room whose only bright things
  // are the lamp's shade (warm, up and behind on the right, where the key is)
  // and the night window (cool, on the left). Metals then reflect the light that
  // actually lights them instead of the bench's default softbox room.
  D.env3 = function (THREE, R, o) {
    o = o || {};
    const env = new THREE.Scene();
    env.add(new THREE.Mesh(new THREE.BoxGeometry(12, 8, 12),
      new THREE.MeshBasicMaterial({ color: 0x06090f, side: THREE.BackSide })));
    function panel(w, h, color, i, pos) {
      const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide }));
      p.material.color.multiplyScalar(i);
      p.position.set(pos[0], pos[1], pos[2]); p.lookAt(0, 0, 0);
      env.add(p); return p;
    }
    panel(1.6, 1.0, 0xffcf8a, o.lamp != null ? o.lamp : 9.0, [D.LAMP[0] * 4, D.LAMP[1] * 4, D.LAMP[2] * 4]);
    panel(3.0, 1.2, 0xffb45a, 1.4, [3.2, 0.4, -2.2]);            // the lamp's spill on the wall
    panel(1.4, 2.2, 0x2b4a66, o.window != null ? o.window : 2.2, [-4.5, 1.6, 2.5]);
    panel(10, 10, 0x1a1210, 0.8, [0, -4.5, 0]);                  // the desk's own warm bounce
    // the lamp's spill on the wall BEHIND the visitor: what a face turned to the
    // camera actually mirrors in a room lit by one lamp
    {
      // a graded wall: dark at the floor, a warm lit band at lamp height, falling
      // off toward the ceiling, so a mirror-like face shows a gradient and a band
      const gc = document.createElement("canvas"); gc.width = 8; gc.height = 256;
      const gg = gc.getContext("2d"), gr = gg.createLinearGradient(0, 0, 0, 256);
      gr.addColorStop(0.00, "#2a1d14"); gr.addColorStop(0.30, "#c9a57a");
      gr.addColorStop(0.42, "#fff1da"); gr.addColorStop(0.55, "#b88a5c");
      gr.addColorStop(1.00, "#140e0a");
      gg.fillStyle = gr; gg.fillRect(0, 0, 8, 256);
      const t = new THREE.CanvasTexture(gc); t.colorSpace = THREE.SRGBColorSpace;
      const m = new THREE.MeshBasicMaterial({ map: t, side: THREE.DoubleSide });
      m.color.setScalar(o.front != null ? o.front : 1.1);
      const p = new THREE.Mesh(new THREE.PlaneGeometry(9.0, 7.0), m);
      p.position.set(-0.5, 3.2, 4.6); p.lookAt(0, 0, 0); env.add(p);
    }
    const pm = new THREE.PMREMGenerator(R.renderer);
    const tex = pm.fromScene(env, 0.03).texture;
    R.scene.environment = tex;
    if ("environmentIntensity" in R.scene) R.scene.environmentIntensity = o.intensity != null ? o.intensity : 0.5;
    pm.dispose();
    return tex;
  };

  // The room: a back wall with a faint panel moulding, and a floor far below.
  D.room3 = function (THREE, R) {
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(8, 4),
      new THREE.MeshStandardMaterial({ color: 0x0c1320, roughness: 0.95 }));
    wall.position.set(0, 0.6, -1.25); wall.receiveShadow = true; R.scene.add(wall);
    const rail = new THREE.Mesh(new THREE.BoxGeometry(8, 0.03, 0.02),
      new THREE.MeshStandardMaterial({ color: 0x1a2230, roughness: 0.8 }));
    rail.position.set(0, 0.32, -1.23); R.scene.add(rail);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(10, 10),
      new THREE.MeshStandardMaterial({ color: 0x070b12, roughness: 0.9 }));
    floor.rotation.x = -Math.PI / 2; floor.position.y = -0.76; floor.receiveShadow = true; R.scene.add(floor);
    return { wall, floor };
  };

  // The desk top (1.8 x 1.2 m, a partner desk, its top face at y = 0) in walnut with a light
  // clearcoat, and optionally the oxblood blotter (0.62 x 0.42 m) laid on it.
  D.desk3 = function (THREE, R, o) {
    o = o || {};
    const S = o.texScale || 1100;                  // texture px per metre
    const wc = D.walnut(Math.round(1.8 * S), Math.round(1.2 * S), { scale: S, seed: 2026110300 });
    const wt = new THREE.CanvasTexture(wc);
    wt.colorSpace = THREE.SRGBColorSpace; wt.anisotropy = 8;
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.04, 1.2, 1, 1, 1),
      new THREE.MeshPhysicalMaterial({ map: wt, roughness: 0.55, clearcoat: 0.35, clearcoatRoughness: 0.38 }));
    top.position.set(0, -0.02, 0);
    top.receiveShadow = true; top.castShadow = true;
    R.scene.add(top);
    let blotter = null;
    if (o.blotter) {
      const L = D.leather(Math.round(0.62 * S), Math.round(0.42 * S), { scale: S, seed: 2026110310, border: 26 });
      const at = new THREE.CanvasTexture(L.albedo); at.colorSpace = THREE.SRGBColorSpace; at.anisotropy = 8;
      const bt = new THREE.CanvasTexture(L.height);
      blotter = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.003, 0.42),
        new THREE.MeshStandardMaterial({ map: at, bumpMap: bt, bumpScale: 0.6, roughness: 0.72 }));
      blotter.position.set(-0.05, 0.0015, 0.02);
      blotter.receiveShadow = true; blotter.castShadow = true;
      R.scene.add(blotter);
    }
    return { top, blotter };
  };

  global.AKDESK = D;
})(typeof window !== "undefined" ? window : this);
