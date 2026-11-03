/* aksawnblock.js -- THE SAWN INLET, No.103's block scene (2026-11-02). ES module.
 *
 * One physiographic block of upper Cook Inlet from the committed DEM
 * (ak-cookinlet-dem), sawn along AEA's CIPLink corridor from the Beluga shore
 * toward the Nikiski shore (bearing 202.4, a SCHEMATIC line between two named
 * shores; the RFI's route is preliminary and not published as geometry). The
 * cut wall is the section: glacial flour water over laminated sediment, depths
 * exaggerated more than heights so a 25 m inlet reads under 100 m bluffs, and
 * both exaggerations are printed by the slides.
 *
 * Deck furniture shared by 01 (the cover) and 09 (the close): the same block,
 * the same moon key, different cameras and compositions. Owns no composition.
 *
 *   import { sawnScene } from '@@ASSETS@@/js/aksawnblock.js';
 *   const S = await sawnScene(THREE, AKT, AKBLOCK, assetsBase, {from, look, fov});
 *   S.R, S.blk, S.seabed: [[u, metres]] along the cut, S.project(u, metres, v)
 *
 * ONE KEY: the deck's az 315 el 28 cartographer's light, here a clear November
 * moon from camera left and above, never in frame. No noise touches a height.
 */
export const BLOCK = {
  origin: [-151.02, 61.17], bearing: 202.4, u: [-6, 62], v: [0, 40],
  step: 0.14, ve: 12, veSea: 200, base: 10.5, seaLevel: 0.5, wallSpan: 13.0
};

function paintSection(seabed, o) {
  /* the wall's uv: x = s along u0..u1, y = (worldY + base) / wallSpan, flipY */
  const W = 4096, H = 1536, c = document.createElement('canvas');
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  const base = o.base, span = o.wallSpan, veL = o.ve, veS = o.veSea;
  const Y = (m) => m / 1000 * (m < 0 ? veS : veL);
  const row = (y) => (1 - (y + base) / span) * H;
  const n = seabed.length;
  /* strata: level bands keyed to world height, edges warped by a seeded sine sum */
  let seed = 103091;
  const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
  const bands = []; let yy = -base;
  const tones = ['#3A3B35', '#4D4538', '#3F3B33', '#6A5D4B', '#36352F', '#584D3E', '#4A453B', '#7A6C57'];
  /* bed thickness over a 6:1 range: runs of thin laminae broken by massive units */
  while (yy < 3) { const massive = rnd() < 0.18, h = massive ? 0.9 + rnd() * 0.9 : 0.08 + rnd() * 0.22;
    bands.push([yy, yy + h, tones[Math.floor(rnd() * tones.length)], rnd() * 6.28]); yy += h; }
  const warp = (s, ph) => 0.05 * Math.sin(s * 23 + ph) + 0.03 * Math.sin(s * 71 + ph * 1.7) + 0.015 * Math.sin(s * 191 + ph * 0.3);
  for (let x = 0; x < W; x++) {
    const s = x / (W - 1), q = Math.min(n - 1, Math.round(s * (n - 1)));
    const m = seabed[q][1];
    const top = m <= 0.5 ? Y(Math.min(m, 0)) : Y(m);
    const sea = m <= 0.5;
    /* sediment below the surface: a ground tone first, so the warped band
     * edges never open onto black (the slivers No.103's critics read as grain) */
    g.fillStyle = '#433F36'; g.fillRect(x, row(top), 1, row(-base) - row(top) + 1);
    for (const b of bands) {
      const y0 = b[0] + warp(s, b[3]), y1 = b[1] + warp(s, b[3] + 1.3);
      const yt = Math.min(y1, top);
      if (yt <= y0) continue;
      g.fillStyle = b[2];
      g.fillRect(x, row(yt), 1, row(y0) - row(yt) + 1);
    }
    /* the lit lip at the surface: brightest on the seabed, a soil line on land */
    g.fillStyle = sea ? '#8A8574' : '#5C5440';
    g.fillRect(x, row(top) - 1, 1, 5);
    if (sea) {
      /* the water column, flour with exponential extinction toward the seabed */
      const ySurf = Y(o.seaLevel);
      const r0 = row(ySurf), r1 = row(top);
      const grd = g.createLinearGradient(0, r0, 0, r1);
      /* glacial flour: a moonlit skin, then exponential extinction toward the seabed */
      grd.addColorStop(0, '#B6B098'); grd.addColorStop(0.03, '#8E8A76'); grd.addColorStop(0.12, '#77786A');
      grd.addColorStop(0.35, '#566058'); grd.addColorStop(0.7, '#3A4440'); grd.addColorStop(1, '#262E2C');
      g.fillStyle = grd; g.fillRect(x, r0, 1, r1 - r0);
    }
  }
  /* the moon key on the wall: lit toward the Beluga end, lee toward Nikiski,
   * and an occlusion darkening into the foot (the wall is a plane, so its
   * modelling is painted into the albedo once, from the deck's one light) */
  g.save(); g.globalCompositeOperation = 'multiply';
  const lh = g.createLinearGradient(0, 0, W, 0);
  lh.addColorStop(0, '#FFFFFF'); lh.addColorStop(0.55, '#E2E2E2'); lh.addColorStop(1, '#9C9C9C');
  g.fillStyle = lh; g.fillRect(0, 0, W, H);
  const lv = g.createLinearGradient(0, row(-base * 0.55), 0, H);
  lv.addColorStop(0, '#FFFFFF'); lv.addColorStop(1, '#8A8A8A');
  g.fillStyle = lv; g.fillRect(0, row(-base * 0.55), W, H - row(-base * 0.55));
  g.restore();
  /* suspended flour motes in the water, a few hundred, deterministic */
  seed = 103077;
  for (let i = 0; i < 6000; i++) {
    const x = rnd() * W, s = x / (W - 1), q = Math.min(n - 1, Math.round(s * (n - 1))), m = seabed[q][1];
    if (m > 0.5) continue;
    const yS = Y(o.seaLevel), yB = Y(Math.min(m, 0));
    const y = yB + (yS - yB) * Math.pow(rnd(), 0.7);
    const up = (y - yB) / Math.max(1e-6, yS - yB);   /* motes thicker and brighter near the lit surface */
    g.fillStyle = 'rgba(196,190,166,' + (0.12 + up * 0.22 + rnd() * 0.14).toFixed(2) + ')';
    const ms = 2 + rnd() * 3; g.fillRect(x, row(y), ms, ms * 0.8);
  }
  return c;
}

function poolTexture(THREE) {
  const c = document.createElement('canvas'); c.width = c.height = 512;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(256, 256, 0, 256, 256, 256);
  grd.addColorStop(0, '#5A6E80'); grd.addColorStop(0.6, '#4A5C6C');
  grd.addColorStop(0.84, '#18242E'); grd.addColorStop(1, '#060D13');
  g.fillStyle = grd; g.fillRect(0, 0, 512, 512);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export async function sawnScene(THREE, AKT, AKBLOCK, assets, cam) {
  const B = BLOCK;
  const dem = await AKBLOCK.loadDEM(assets + '/geo/ak-cookinlet-dem');
  /* land only: a 3x3 median then a 3x3 mean, so 12x exaggeration prints no single-cell pyramids */
  (function smoothLand() {
    const C = dem.meta.cols, Rr = dem.meta.rows, z = dem.z, src = Float32Array.from(z), w = new Float32Array(9);
    const med = new Float32Array(z.length);
    for (let j = 1; j < Rr - 1; j++) for (let i = 1; i < C - 1; i++) {
      const k = j * C + i; if (!(src[k] > 0.5)) { med[k] = src[k]; continue; }
      let n = 0; for (let b = -1; b <= 1; b++) for (let a = -1; a <= 1; a++) w[n++] = src[k + b * C + a];
      med[k] = Array.from(w).sort((p, q) => p - q)[4];
    }
    for (let j = 1; j < Rr - 1; j++) for (let i = 1; i < C - 1; i++) {
      const k = j * C + i; if (!(src[k] > 0.5)) continue;
      let s = 0, n = 0; for (let b = -1; b <= 1; b++) for (let a = -1; a <= 1; a++) { const v = med[k + b * C + a]; if (v > 0.5) { s += v; n++; } }
      z[k] = Math.max(0.6, s / n);
    }
  })();
  /* the seabed profile along the cut, before building, to paint the wall */
  const F = AKBLOCK.frame(B.origin, B.bearing), S = AKBLOCK.sampler(dem);
  const seabed = [];
  for (let q = 0; q <= 1200; q++) {
    const u = B.u[0] + (B.u[1] - B.u[0]) * q / 1200, ll = F.toLL(u, 0);
    seabed.push([u, S(ll[0], ll[1])]);
  }
  const secCanvas = paintSection(seabed, B);
  const secTex = new THREE.CanvasTexture(secCanvas); secTex.colorSpace = THREE.SRGBColorSpace;
  secTex.anisotropy = 8;
  const sectionMaterial = new THREE.MeshStandardMaterial({ map: secTex, roughness: 0.86, metalness: 0 });
  /* a far camera sees the wall small and dark: let the painted albedo carry itself (its key falloff is painted in) */
  if (cam.wallGlow) { sectionMaterial.emissiveMap = secTex; sectionMaterial.emissive = new THREE.Color(0xffffff); sectionMaterial.emissiveIntensity = cam.wallGlow; }
  const seaMaterial = new THREE.MeshPhysicalMaterial({ color: 0x4f5149, roughness: 0.34, metalness: 0,
    clearcoat: 0.55, clearcoatRoughness: 0.22, envMapIntensity: 0.9 });
  /* land ramp in the deck palette: mudflat at the shore, spruce, then snow */
  const ramp = (e) => {
    const st = [[0, [0.29, 0.25, 0.20]], [6, [0.20, 0.21, 0.17]], [25, [0.075, 0.115, 0.095]],
                [200, [0.13, 0.18, 0.15]], [500, [0.30, 0.34, 0.36]], [800, [0.78, 0.83, 0.86]]];
    if (e <= st[0][0]) return st[0][1].slice();
    for (let k = 1; k < st.length; k++) if (e <= st[k][0]) {
      const t = (e - st[k - 1][0]) / (st[k][0] - st[k - 1][0]);
      return st[k - 1][1].map((c, i) => c + (st[k][1][i] - c) * t);
    }
    return st[st.length - 1][1].slice();
  };
  const blk = AKBLOCK.build(dem, Object.assign({}, B, { sectionEdge: 'v0', sectionMaterial, seaMaterial, ramp,
    rock: [0.22, 0.24, 0.24], wallMaterial: new THREE.MeshStandardMaterial({ color: 0x2a2c28, roughness: 0.95 }) }));

  const R = AKT.setup(cam.canvas, { w: 1080, h: 1350, bg: 0x050b10, exposure: cam.exposure || 1.05 });
  R.scene.fog = new THREE.FogExp2(0x050b10, cam.fog != null ? cam.fog : 0.0062);
  AKT.environment(R, { intensity: 0.42 });
  /* the moon key from camera left and above (the deck's az 315, el 28) */
  const cx0 = (B.u[0] + B.u[1]) / 2;
  const key = new THREE.DirectionalLight(0xdce6ee, cam.keyI || 2.7);
  key.position.set(cx0 - 46, 34, 40); key.target.position.set(cx0, -2, -18);
  key.castShadow = true; key.shadow.mapSize.set(4096, 4096);
  const sc = key.shadow.camera; sc.left = -60; sc.right = 60; sc.top = 60; sc.bottom = -60; sc.near = 1; sc.far = 220;
  key.shadow.bias = -0.0006; key.shadow.radius = 6;
  R.scene.add(key); R.scene.add(key.target);
  const fill = new THREE.DirectionalLight(0x35507a, 0.55); fill.position.set(cx0 + 40, 14, 30); R.scene.add(fill);
  R.scene.add(new THREE.AmbientLight(0x0d1c28, 1.0));
  /* the water top tinted by the DEM's own depth: shallows pale flour, the
   * channel darker, so the inlet's structure reads from above (no invented depth) */
  if (blk.sea) {
    const g = blk.sea.geometry, n = blk.NU * blk.NV, col = new Float32Array(n * 3);
    const sh = [0.24, 0.24, 0.21], dp = [0.085, 0.10, 0.105];
    for (let k = 0; k < n; k++) {
      const dpt = Math.max(0, Math.min(1, -blk.hm[k] / 30));
      const f = Math.pow(dpt, 0.7);
      col[k * 3] = sh[0] + (dp[0] - sh[0]) * f; col[k * 3 + 1] = sh[1] + (dp[1] - sh[1]) * f; col[k * 3 + 2] = sh[2] + (dp[2] - sh[2]) * f;
    }
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    seaMaterial.vertexColors = true; seaMaterial.color.set(0xffffff); seaMaterial.needsUpdate = true;
  }
  AKT.add(R, blk.group);
  /* the plinth: a dark table with a lit pool under the block's foot */
  const table = new THREE.Mesh(new THREE.PlaneGeometry(1400, 1400),
    new THREE.MeshStandardMaterial({ color: 0x060d13, roughness: 0.95, metalness: 0 }));
  table.rotation.x = -Math.PI / 2;
  table.position.set(cx0, -B.base - 0.03, -(B.v[0] + B.v[1]) / 2);
  table.receiveShadow = false; R.scene.add(table);   /* the key's cast falls behind the block as a hard map polygon; the painted seam is the contact */
  /* the lit pool under the block's foot, wider than the block so its foot sits
   * on a brightness transition and the cast has light to subtract from */
  const pool = new THREE.Mesh(new THREE.PlaneGeometry(B.u[1] - B.u[0] + 30, B.v[1] - B.v[0] + 22),
    new THREE.MeshStandardMaterial({ map: poolTexture(THREE), roughness: 0.9, metalness: 0, transparent: true, opacity: 1 }));
  pool.rotation.x = -Math.PI / 2;
  /* centred toward the near foot, so the brightest table sits where the wall meets it */
  pool.position.set(cx0, -B.base + 0.02, -(B.v[0] + B.v[1]) / 2 + 14);
  pool.receiveShadow = false; R.scene.add(pool);
  /* the occlusion seam: the key sits in front of the section wall, so its cast
   * falls behind the block and the near foot needs its own attached darkening,
   * strongest at the foot and gone within about 3 km of table */
  const sc2 = document.createElement('canvas'); sc2.width = 8; sc2.height = 128;
  const sg = sc2.getContext('2d'), sgr = sg.createLinearGradient(0, 0, 0, 128);
  sgr.addColorStop(0, 'rgba(2,5,8,0.92)'); sgr.addColorStop(0.25, 'rgba(2,5,8,0.55)'); sgr.addColorStop(1, 'rgba(2,5,8,0)');
  sg.fillStyle = sgr; sg.fillRect(0, 0, 8, 128);
  const seamTex = new THREE.CanvasTexture(sc2); seamTex.colorSpace = THREE.SRGBColorSpace;
  const seam = new THREE.Mesh(new THREE.PlaneGeometry(B.u[1] - B.u[0] + 1.2, 3.2),
    new THREE.MeshBasicMaterial({ map: seamTex, transparent: true, depthWrite: false }));
  seam.rotation.x = -Math.PI / 2;
  seam.position.set(cx0, -B.base + 0.04, 1.6);
  R.scene.add(seam);
  AKT.frame(R, { from: cam.from, look: cam.look, fov: cam.fov });
  R.camera.near = 3; R.camera.far = 2400; R.camera.updateProjectionMatrix();
  const Yw = (m) => m / 1000 * (m < 0 ? B.veSea : B.ve);
  return {
    R, blk, seabed, dem, B,
    /* screen point of (u along the cut, metres, v off the cut) */
    project(u, m, v) { return AKT.projectPoint(R, u, Yw(m), -(v || 0)); },
    worldY: Yw
  };
}
