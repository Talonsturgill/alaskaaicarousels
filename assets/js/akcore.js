/* akcore.js — the dated ice core, a shared GPU object (added 2026-11-22, No.122).
 *
 * One cylinder of glacial ice whose length is time: the signing band at the
 * left end, strata laid down by day, a gold ring at the hinge date, clear ice
 * past it with no strata. Three frames of No.122 render it (01, 08, 09) from
 * their own cameras, so the object lives here and each slide owns its camera,
 * light, crop and 2D finish. ES module, like akthree:
 *
 *   const CORE = (await import('@@ASSETS@@/js/akcore.js')).init(THREE, AKT);
 *   const core = CORE.build(R, { length: 9, radius: 0.5, ringAt: 0.78,
 *                                dated: { days: 490, marks: [{ day: 471, kind: 'fresh' }] },
 *                                tephra: [0.22, 0.31], seed: 20261122 });
 *   core.group           the THREE.Group, axis along +x, centred on the origin
 *   core.ringX           world x of the gold ring's centre
 *   core.xForDay(d)      world x of day d on the dated length
 *   core.cradle          the aluminium half-pipe and its feet (in the group)
 *
 * Strata are painted into a CanvasTexture along the cylinder's height (v) and
 * also feed a dim emissive map, so light from the table reads as passing
 * through the ice rather than reflecting off a painted tube. No transmission:
 * SwiftShader's transmission is slow and noisy, and an emissive lift from below
 * reads as transillumination at a fraction of the cost.
 */
export function init(THREE, AKT) {
  const CORE = {};

  function rng(seed) {
    let s = seed >>> 0;
    return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }

  /* The strata map. Canvas is W (around) x H (along). v=0 is one end of
   * three's CylinderGeometry (its -y end, which build() turns to -x). */
  CORE.strataCanvas = function (o) {
    const W = 256, H = 4096, R = rng(o.seed || 20261122);
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d');
    const ringV = o.ringAt;                       // fraction of length where the ring sits
    const datedPx = Math.round(ringV * H);
    // base ice: a cool blue-white with a slow downcore greying (older ice dustier)
    for (let y = 0; y < H; y++) {
      const u = y / H;
      let r, gg, b;
      if (y < datedPx) {
        const age = 1 - y / datedPx;               // 1 at the signing end, 0 at the ring
        r = 176 - 30 * age; gg = 202 - 26 * age; b = 214 - 18 * age;
      } else {                                     // clear ice past the ring
        const k = (y - datedPx) / (H - datedPx);
        r = 196 + 10 * k; gg = 216 + 8 * k; b = 224 + 6 * k;    // clear ice: pale, unlayered
      }
      g.fillStyle = `rgb(${r|0},${gg|0},${b|0})`; g.fillRect(0, H - 1 - y, W, 1);
    }
    // dust bands, seeded widths and densities, only in the dated ice
    for (let k = 0; k < 8; k++) {                      // wide dust bands, varied
      const yy = 80 + R() * (datedPx - 160), w = 24 + R() * 60, a = 0.12 + R() * 0.22;
      const gd = g.createLinearGradient(0, H - yy - w, 0, H - yy);
      gd.addColorStop(0, 'rgba(78,96,104,0)'); gd.addColorStop(0.5, `rgba(78,96,104,${a.toFixed(2)})`); gd.addColorStop(1, 'rgba(78,96,104,0)');
      g.fillStyle = gd; g.fillRect(0, H - yy - w, W, w);
    }
    let y = 30;
    while (y < datedPx - 20) {
      const w = 1.5 + R() * R() * 22, a = 0.05 + R() * 0.18;
      g.fillStyle = `rgba(70,86,96,${a.toFixed(3)})`;
      g.fillRect(0, H - y - w, W, w);
      y += w + 30 + R() * 110;
    }
    // tephra layers (umber), positions as fractions of the dated length
    (o.tephra || []).forEach((f, i) => {
      const yy = Math.round(f * datedPx), w = 34 + i * 6;
      const grd = g.createLinearGradient(0, H - yy - w, 0, H - yy);
      grd.addColorStop(0, 'rgba(90,63,44,0)'); grd.addColorStop(0.3, 'rgba(110,80,58,0.5)');
      grd.addColorStop(0.7, 'rgba(110,80,58,0.46)'); grd.addColorStop(1, 'rgba(90,63,44,0)');
      g.fillStyle = grd; g.fillRect(0, H - yy - w, W, w);
      for (let k = 0; k < 90; k++) {              // coarse grains
        g.fillStyle = R() < 0.5 ? 'rgba(60,40,28,0.9)' : 'rgba(150,128,104,0.8)';
        g.fillRect(R() * W, H - yy - R() * w, 1 + R() * 2, 1 + R() * 2);
      }
    });
    // the signing band: a pale dense deposit at the start of the dated ice
    g.fillStyle = 'rgba(236,244,248,0.92)'; g.fillRect(0, H - 150, W, 110);
    g.fillStyle = 'rgba(120,140,150,0.6)'; g.fillRect(0, H - 154, W, 3); g.fillRect(0, H - 40, W, 3);
    // marked days (a fresh frost-white band)
    const days = (o.dated && o.dated.days) || 490;
    ((o.dated && o.dated.marks) || []).forEach(m => {
      const yy = Math.round((m.day / days) * datedPx);
      g.fillStyle = 'rgba(244,250,252,0.95)'; g.fillRect(0, H - yy - 18, W, 18);
      g.fillStyle = 'rgba(150,176,186,0.7)'; g.fillRect(0, H - yy - 20, W, 2);
    });
    // AI strata (ice blue, quiet) when asked
    ((o.blue) || []).forEach(f => {
      const yy = Math.round(f * datedPx);
      g.fillStyle = 'rgba(90,200,240,0.55)'; g.fillRect(0, H - yy - 7, W, 7);
    });
    // bubbles: bright voids with a dark lower lip, dated ice only
    for (let k = 0; k < 3000; k++) {
      const yy = R() * datedPx, xx = R() * W, r = 0.7 + Math.pow(R(), 2) * 3.4;
      g.fillStyle = 'rgba(250,253,255,0.62)';
      g.beginPath(); g.arc(xx, H - yy, r, 0, Math.PI * 2); g.fill();
      g.fillStyle = 'rgba(70,96,108,0.35)'; g.fillRect(xx - r, H - yy + r * 0.6, r * 2, 0.8);
    }
    // a few soft refraction streaks in the clear ice, running with the long axis
    for (let k = 0; k < 14; k++) { const yy = datedPx + 40 + R() * (H - datedPx - 80), xx = R() * W, len = 120 + R() * 260;
      const gs = g.createLinearGradient(0, H - yy - len, 0, H - yy); gs.addColorStop(0, 'rgba(240,250,252,0)'); gs.addColorStop(0.5, 'rgba(240,250,252,0.28)'); gs.addColorStop(1, 'rgba(240,250,252,0)');
      g.fillStyle = gs; g.fillRect(xx, H - yy - len, 3, len); }
    return { canvas: c, datedPx, H };
  };

  CORE.build = function (Rr, o) {
    o = Object.assign({ length: 9, radius: 0.5, ringAt: 0.78, seed: 20261122,
      dated: { days: 490, marks: [] }, tephra: [0.22, 0.31], blue: [],
      emissive: 0.32, cradle: true, ring: true, transmit: 0.38, bubbles: 1600 }, o || {});
    const L = o.length, r = o.radius;
    const group = new THREE.Group();
    const sc = CORE.strataCanvas(o);
    const emc = document.createElement('canvas'); emc.width = sc.canvas.width; emc.height = sc.canvas.height;
    { const eg = emc.getContext('2d'); eg.drawImage(sc.canvas, 0, 0);
      eg.fillStyle = 'rgba(0,0,0,0.72)'; eg.fillRect(0, 0, emc.width, emc.height - sc.datedPx); }
    const emTex = new THREE.CanvasTexture(emc); emTex.colorSpace = THREE.SRGBColorSpace;
    const tex = new THREE.CanvasTexture(sc.canvas);
    tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    const iceMat = new THREE.MeshPhysicalMaterial({
      map: tex, color: 0xffffff, roughness: 0.2, metalness: 0,
      clearcoat: 1, clearcoatRoughness: 0.08, sheen: 0.25, sheenColor: new THREE.Color(0xbfe9ff),
      emissive: new THREE.Color(0x3e7e94), emissiveMap: emTex, emissiveIntensity: o.emissive,
      envMapIntensity: 0.9 });
    const geo = new THREE.CylinderGeometry(r, r, L, 160, 1, false);
    const capC = document.createElement('canvas'); capC.width = capC.height = 512;
    { const cg = capC.getContext('2d'); const Rc = rng((o.seed || 1) + 5); const gg = cg.createRadialGradient(200, 190, 20, 256, 256, 300);
      gg.addColorStop(0, '#eef6f9'); gg.addColorStop(1, '#9fbcc6'); cg.fillStyle = gg; cg.fillRect(0, 0, 512, 512);
      for (let k = 0; k < 260; k++) { const a = Rc() * 6.28, d = Math.sqrt(Rc()) * 240, br = 1 + Rc() * 5;
        cg.strokeStyle = 'rgba(255,255,255,0.7)'; cg.lineWidth = 1.2; cg.beginPath(); cg.arc(256 + Math.cos(a) * d, 256 + Math.sin(a) * d, br, 0, 6.28); cg.stroke(); }
      for (let k = 0; k < 3; k++) { cg.strokeStyle = 'rgba(255,255,255,0.45)'; cg.lineWidth = 1; cg.beginPath(); cg.moveTo(Rc() * 512, Rc() * 512); cg.lineTo(Rc() * 512, Rc() * 512); cg.stroke(); }
      cg.strokeStyle = 'rgba(255,255,255,0.9)'; cg.lineWidth = 10; cg.beginPath(); cg.arc(256, 256, 250, 3.4, 5.6); cg.stroke(); }
    const capTex = new THREE.CanvasTexture(capC); capTex.colorSpace = THREE.SRGBColorSpace;
    const capMat = new THREE.MeshPhysicalMaterial({ map: capTex, color: 0xffffff, roughness: 0.45, clearcoat: 1, clearcoatRoughness: 0.2,
      emissive: new THREE.Color(0x4f93aa), emissiveMap: capTex, emissiveIntensity: 0.1, envMapIntensity: 1.0 });
    if (o.transmit) {                       // true ice: light passes through, bubbles sit inside
      Object.assign(iceMat, { transmission: o.transmit, thickness: r * 2, ior: 1.31,
        attenuationColor: new THREE.Color(0xdceef4), attenuationDistance: 2.4, roughness: 0.34,
        clearcoat: 0.6, clearcoatRoughness: 0.16 });
      iceMat.emissive = new THREE.Color(0x5f8fa0);
      iceMat.emissiveIntensity = o.emissive * 0.6;
    }
    const core = new THREE.Mesh(geo, [iceMat, capMat, capMat]);
    core.rotation.z = Math.PI / 2;          // axis to x; v=0 end (-y) goes to +x, so flip:
    core.rotation.y = Math.PI;              // v=0 (signing) at -x, ring toward +x
    group.add(core);
    const xFrom = -L / 2, xRing = xFrom + o.ringAt * L;
    if (o.bubbles) {                        // seeded bubbles INSIDE the dated ice, seen through it
      const Rb = rng((o.seed || 1) + 77), n = o.bubbles;
      const bg = new THREE.SphereGeometry(1, 10, 8);
      const bm = new THREE.MeshStandardMaterial({ color: 0xf4fbfe, roughness: 0.1, metalness: 0,
        emissive: new THREE.Color(0x9fd3e6), emissiveIntensity: 0.35 });
      const inst = new THREE.InstancedMesh(bg, bm, n); const m4 = new THREE.Matrix4();
      for (let i = 0; i < n; i++) {
        const x = xFrom + Rb() * (xRing - xFrom - 0.05), a = Rb() * Math.PI * 2, d = Math.sqrt(Rb()) * r * 0.86;
        const s = 0.006 + Math.pow(Rb(), 3) * 0.03;
        m4.makeScale(s, s, s); m4.setPosition(x, Math.sin(a) * d, Math.cos(a) * d); inst.setMatrixAt(i, m4);
      }
      inst.castShadow = false; inst.receiveShadow = false; group.add(inst);
    }
    const xForDay = d => xFrom + (d / o.dated.days) * (xRing - xFrom);
    let ring = null;
    if (o.ring) {
      ring = new THREE.Mesh(new THREE.TorusGeometry(r * 1.05, r * 0.095, 32, 220),
        new THREE.MeshStandardMaterial({ color: 0xffc72c, metalness: 0.9, roughness: 0.2, envMapIntensity: 1.8, emissive: new THREE.Color(0xffc72c), emissiveIntensity: 0.12 }));
      ring.rotation.y = Math.PI / 2; ring.position.x = xRing; group.add(ring);
    }
    let cradle = null;
    if (o.cradle) {
      cradle = new THREE.Group();
      const al = new THREE.MeshStandardMaterial({ color: 0xd5dce0, metalness: 0.55, roughness: 0.38, envMapIntensity: 1.6 });
      const sh = new THREE.Shape();
      const ro = r * 1.14, ri = r * 1.04;
      sh.absarc(0, 0, ro, Math.PI * 0.98, Math.PI * 2.02, false);
      sh.absarc(0, 0, ri, Math.PI * 2.02, Math.PI * 0.98, true);
      const pipe = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: L * 0.94, bevelEnabled: true,
        bevelSize: 0.008, bevelThickness: 0.008, bevelSegments: 2, curveSegments: 64 }), al);
      pipe.rotation.y = Math.PI / 2; pipe.position.x = -L * 0.47; cradle.add(pipe);
      const feetX = [-0.36, -0.12, 0.12, 0.36].map(f => f * L);
      feetX.forEach(fx => {
        const foot = new THREE.Mesh(new THREE.BoxGeometry(0.12, r * 0.62, r * 1.2), al);
        foot.position.set(fx, -r * 1.12 - r * 0.24, 0); cradle.add(foot);
        const pad = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.03, r * 1.9), al);
        pad.position.set(fx, -r * 1.12 - r * 0.55, 0); cradle.add(pad);
      });
      group.add(cradle);
    }
    group.position.y = r * 1.12 + r * 0.565;   // pads sit on y = 0
    return { group, core, ring, cradle, iceMat, ringX: xRing, xFrom, xForDay,
             baseY: group.position.y, radius: r, length: L };
  };

  /* The lit freezer table: a glossy dark plane with an emissive pool under the
   * core, so every foot and cast sits on a brightness transition. */
  CORE.table = function (Rr, o) {
    o = Object.assign({ size: 40, pool: [0, 0], poolW: 6, poolD: 2.6, poolHex: '#5F98AC', baseHex: '#0C1C28', intensity: 0.9 }, o || {});
    const N = 1024, c = document.createElement('canvas'); c.width = N; c.height = N;
    const g = c.getContext('2d');
    g.fillStyle = '#000'; g.fillRect(0, 0, N, N);
    const cx = N / 2 + (o.pool[0] / o.size) * N, cy = N / 2 + (o.pool[1] / o.size) * N;
    g.save(); g.translate(cx, cy); g.scale((o.poolW / o.size) * N / 2, (o.poolD / o.size) * N / 2);
    const grd = g.createRadialGradient(0, 0, 0, 0, 0, 1);
    grd.addColorStop(0, o.poolHex); grd.addColorStop(0.45, 'rgba(62,113,134,0.55)');
    grd.addColorStop(0.8, 'rgba(30,58,72,0.18)'); grd.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = grd; g.beginPath(); g.arc(0, 0, 1, 0, Math.PI * 2); g.fill(); g.restore();
    const em = new THREE.CanvasTexture(c); em.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.MeshStandardMaterial({ color: new THREE.Color(o.baseHex), roughness: 0.16, metalness: 0.1,
      emissive: new THREE.Color(0xffffff), emissiveMap: em, emissiveIntensity: o.intensity, envMapIntensity: 0.6 });
    const plane = new THREE.Mesh(new THREE.PlaneGeometry(o.size, o.size), m);
    plane.rotation.x = -Math.PI / 2; plane.receiveShadow = true;
    return plane;
  };

  CORE.caliper = function (o) {
    o = Object.assign({ length: 2.0, open: 0.5 }, o || {});
    const sc = document.createElement('canvas'); sc.width = 1024; sc.height = 64; const g = sc.getContext('2d');
    const gr = g.createLinearGradient(0, 0, 0, 64); gr.addColorStop(0, '#e6ecef'); gr.addColorStop(1, '#9aa6ae'); g.fillStyle = gr; g.fillRect(0, 0, 1024, 64);
    for (let k = 0; k < 100; k++) { const x = 12 + k * 10; g.fillStyle = '#10161a'; g.fillRect(x, 0, k % 5 ? 2 : 3, k % 5 ? 20 : 40); }
    for (let k = 0; k < 400; k++) { g.fillStyle = 'rgba(255,255,255,0.08)'; g.fillRect(0, (k * 7.3) % 64, 1024, 0.6); }
    const st = new THREE.CanvasTexture(sc); st.colorSpace = THREE.SRGBColorSpace; st.anisotropy = 8;
    const steel = new THREE.MeshStandardMaterial({ color: 0xd8dfe3, metalness: 0.82, roughness: 0.3, envMapIntensity: 1.7 });
    const face = new THREE.MeshStandardMaterial({ map: st, metalness: 0.7, roughness: 0.32, envMapIntensity: 1.5 });
    const grp = new THREE.Group();
    const bev = (w, d, h) => { const s2 = new THREE.Shape(); s2.moveTo(-w / 2, -d / 2); s2.lineTo(w / 2, -d / 2); s2.lineTo(w / 2, d / 2); s2.lineTo(-w / 2, d / 2); s2.closePath();
      const geo = new THREE.ExtrudeGeometry(s2, { depth: h, bevelEnabled: true, bevelSize: 0.008, bevelThickness: 0.008, bevelSegments: 2 }); geo.rotateX(-Math.PI / 2); return geo; };
    const beam = new THREE.Mesh(bev(o.length, 0.17, 0.05), [face, steel]); beam.position.y = 0.0; grp.add(beam);
    const jawShape = (dir) => { const s3 = new THREE.Shape(); s3.moveTo(0, 0); s3.lineTo(0.09 * dir, 0); s3.lineTo(0.05 * dir, 0.46); s3.lineTo(0.0, 0.5); s3.closePath();
      const geo = new THREE.ExtrudeGeometry(s3, { depth: 0.05, bevelEnabled: true, bevelSize: 0.006, bevelThickness: 0.006, bevelSegments: 2 }); geo.rotateX(-Math.PI / 2); return geo; };
    const j1 = new THREE.Mesh(jawShape(1), steel); j1.position.set(-o.length / 2 + 0.06, 0, 0.08); grp.add(j1);
    const j2 = new THREE.Mesh(jawShape(-1), steel); j2.position.set(-o.length / 2 + 0.16 + o.open, 0, 0.08); grp.add(j2);
    const vb = new THREE.Mesh(bev(0.24, 0.24, 0.075), steel); vb.position.set(-o.length / 2 + 0.2 + o.open, 0, 0); grp.add(vb);
    return grp;
  };

  return CORE;
}
