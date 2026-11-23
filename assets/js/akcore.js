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
        r = 96 + 18 * k; gg = 140 + 16 * k; b = 160 + 14 * k;   // clear ice reads dark and deep
      }
      g.fillStyle = `rgb(${r|0},${gg|0},${b|0})`; g.fillRect(0, H - 1 - y, W, 1);
    }
    // dust bands, seeded widths and densities, only in the dated ice
    let y = 30;
    while (y < datedPx - 20) {
      const w = 2 + R() * 9, a = 0.10 + R() * 0.34;
      g.fillStyle = `rgba(70,86,96,${a.toFixed(3)})`;
      g.fillRect(0, H - y - w, W, w);
      y += w + 16 + R() * 54;
    }
    // tephra layers (umber), positions as fractions of the dated length
    (o.tephra || []).forEach((f, i) => {
      const yy = Math.round(f * datedPx), w = 26 + i * 6;
      const grd = g.createLinearGradient(0, H - yy - w, 0, H - yy);
      grd.addColorStop(0, 'rgba(90,63,44,0)'); grd.addColorStop(0.25, 'rgba(90,63,44,0.85)');
      grd.addColorStop(0.75, 'rgba(110,80,58,0.8)'); grd.addColorStop(1, 'rgba(90,63,44,0)');
      g.fillStyle = grd; g.fillRect(0, H - yy - w, W, w);
      for (let k = 0; k < 260; k++) {             // coarse grains
        g.fillStyle = R() < 0.5 ? 'rgba(60,40,28,0.9)' : 'rgba(150,128,104,0.8)';
        g.fillRect(R() * W, H - yy - R() * w, 1 + R() * 2, 1 + R() * 2);
      }
    });
    // the signing band: a pale dense deposit at the start of the dated ice
    g.fillStyle = 'rgba(236,244,248,0.9)'; g.fillRect(0, H - 52, W, 40);
    g.fillStyle = 'rgba(120,140,150,0.6)'; g.fillRect(0, H - 56, W, 3); g.fillRect(0, H - 12, W, 3);
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
    for (let k = 0; k < 4200; k++) {
      const yy = R() * datedPx, xx = R() * W, r = 0.9 + R() * 2.6;
      g.fillStyle = 'rgba(250,253,255,0.62)';
      g.beginPath(); g.arc(xx, H - yy, r, 0, Math.PI * 2); g.fill();
      g.fillStyle = 'rgba(70,96,108,0.35)'; g.fillRect(xx - r, H - yy + r * 0.6, r * 2, 0.8);
    }
    // a few refraction streaks in the clear ice
    for (let k = 0; k < 18; k++) {
      const yy = datedPx + R() * (H - datedPx), xx = R() * W;
      g.fillStyle = 'rgba(220,240,248,0.5)'; g.fillRect(xx, H - yy - 60, 1.6, 60 + R() * 160);
    }
    return { canvas: c, datedPx, H };
  };

  CORE.build = function (Rr, o) {
    o = Object.assign({ length: 9, radius: 0.5, ringAt: 0.78, seed: 20261122,
      dated: { days: 490, marks: [] }, tephra: [0.22, 0.31], blue: [],
      emissive: 0.32, cradle: true, ring: true }, o || {});
    const L = o.length, r = o.radius;
    const group = new THREE.Group();
    const sc = CORE.strataCanvas(o);
    const tex = new THREE.CanvasTexture(sc.canvas);
    tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    const iceMat = new THREE.MeshPhysicalMaterial({
      map: tex, color: 0xffffff, roughness: 0.2, metalness: 0,
      clearcoat: 1, clearcoatRoughness: 0.08, sheen: 0.25, sheenColor: new THREE.Color(0xbfe9ff),
      emissive: new THREE.Color(0x3e7e94), emissiveMap: tex, emissiveIntensity: o.emissive,
      envMapIntensity: 0.9 });
    const geo = new THREE.CylinderGeometry(r, r, L, 160, 1, false);
    const capMat = new THREE.MeshPhysicalMaterial({ color: 0xd8ecf2, roughness: 0.1,
      clearcoat: 1, emissive: new THREE.Color(0x4f93aa), emissiveIntensity: 0.28, envMapIntensity: 1.0 });
    const core = new THREE.Mesh(geo, [iceMat, capMat, capMat]);
    core.rotation.z = Math.PI / 2;          // axis to x; v=0 end (-y) goes to +x, so flip:
    core.rotation.y = Math.PI;              // v=0 (signing) at -x, ring toward +x
    group.add(core);
    const xFrom = -L / 2, xRing = xFrom + o.ringAt * L;
    const xForDay = d => xFrom + (d / o.dated.days) * (xRing - xFrom);
    let ring = null;
    if (o.ring) {
      ring = new THREE.Mesh(new THREE.TorusGeometry(r * 1.045, r * 0.07, 32, 220),
        new THREE.MeshStandardMaterial({ color: 0xffc72c, metalness: 0.92, roughness: 0.22, envMapIntensity: 1.4 }));
      ring.rotation.y = Math.PI / 2; ring.position.x = xRing; group.add(ring);
    }
    let cradle = null;
    if (o.cradle) {
      cradle = new THREE.Group();
      const al = new THREE.MeshStandardMaterial({ color: 0xb8c3ca, metalness: 0.88, roughness: 0.34, envMapIntensity: 1.2 });
      const sh = new THREE.Shape();
      const ro = r * 1.16, ri = r * 1.08;
      sh.absarc(0, 0, ro, Math.PI * 1.08, Math.PI * 1.92, false);
      sh.absarc(0, 0, ri, Math.PI * 1.92, Math.PI * 1.08, true);
      const pipe = new THREE.Mesh(new THREE.ExtrudeGeometry(sh, { depth: L * 0.94, bevelEnabled: true,
        bevelSize: 0.008, bevelThickness: 0.008, bevelSegments: 2, curveSegments: 64 }), al);
      pipe.rotation.y = Math.PI / 2; pipe.position.x = -L * 0.47; cradle.add(pipe);
      const feetX = [-0.36, -0.12, 0.12, 0.36].map(f => f * L);
      feetX.forEach(fx => {
        const foot = new THREE.Mesh(new THREE.BoxGeometry(0.16, r * 0.62, r * 1.5), al);
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

  return CORE;
}
