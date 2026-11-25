/* akcouple.js — the three-coupling data hall module, a shared GPU object
 * (added 2026-11-24, No.123, Petersburg Ordinance 2026-24).
 *
 * One schematic data hall module and its three connections to a town: a
 * copper feeder into a service entrance on its left face (the grid), a
 * generator skid with an exhaust stack on its right (generators), and a dry
 * cooler on its roof with glycol risers (cooling). Slides 01 and 09 render it
 * from their own cameras; slide 05 renders a cooler bank with bank(). Each
 * slide owns its camera, light, crop and 2D finish. ES module, like akthree:
 *
 *   const CPL = (await import('@@ASSETS@@/js/akcouple.js')).init(THREE, AKT);
 *   const m = CPL.module(R, { seed: 20261124, frost: 0.0 });
 *   m.group            THREE.Group, footprint centred on the origin, y up
 *   m.points.grid      world [x,y,z] of the feeder clamp point
 *   m.points.gen       world [x,y,z] of the generator breaker
 *   m.points.cool      world [x,y,z] of the glycol header tee
 *   m.hull             array of world [x,y,z] points for an envelope outline
 *   const b = CPL.bank(R, { fins: 180, fans: 4, seed: 20261124 });
 *
 * Deterministic: a local mulberry32, never Math.random(). It builds geometry
 * and materials only; it adds no lights and renders nothing.
 */
export function init(THREE, AKT) {
  const CPL = {};

  function rng(seed) {
    let s = seed >>> 0;
    return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }

  /* Enamel panel map: vertical seams every `pitch` of the face, a louver band,
   * faint weathering streaks, optional frost along the top edge. Painted in
   * sRGB on a canvas and used as both colour and a roughness variation. */
  function panelTexture(o) {
    const W = 1024, H = 512, R = rng(o.seed || 1);
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d');
    const base = o.base || '#a3aaa6';
    g.fillStyle = base; g.fillRect(0, 0, W, H);
    // weathering: soft vertical streaks below seams and fasteners
    for (let i = 0; i < 90; i++) {
      const x = R() * W, w = 2 + R() * 10, a = 0.025 + R() * 0.05;
      const gr = g.createLinearGradient(0, 0, 0, H);
      gr.addColorStop(0, `rgba(40,46,46,${a})`); gr.addColorStop(1, 'rgba(40,46,46,0)');
      g.fillStyle = gr; g.fillRect(x, R() * H * 0.3, w, H);
    }
    const n = o.panels || 8;
    for (let i = 1; i < n; i++) {
      const x = Math.round(i * W / n);
      g.fillStyle = 'rgba(30,34,34,0.55)'; g.fillRect(x - 2, 0, 3, H);
      g.fillStyle = 'rgba(235,240,238,0.35)'; g.fillRect(x + 1, 0, 2, H);
      for (let y = 30; y < H; y += 64) {           // fastener heads
        g.fillStyle = 'rgba(30,34,34,0.5)'; g.beginPath(); g.arc(x - 12, y, 3, 0, Math.PI * 2); g.fill();
        g.fillStyle = 'rgba(240,244,242,0.4)'; g.beginPath(); g.arc(x - 13, y - 1, 1.4, 0, Math.PI * 2); g.fill();
      }
    }
    if (o.louver) {                                  // louver band, lower third
      const y0 = H * 0.62, y1 = H * 0.86;
      g.fillStyle = 'rgba(20,24,24,0.55)'; g.fillRect(W * 0.08, y0, W * 0.84, y1 - y0);
      for (let y = y0 + 4; y < y1 - 4; y += 11) {
        g.fillStyle = 'rgba(205,212,208,0.55)'; g.fillRect(W * 0.09, y, W * 0.82, 4);
        g.fillStyle = 'rgba(15,18,18,0.6)'; g.fillRect(W * 0.09, y + 4, W * 0.82, 3);
      }
    }
    if (o.frost) {                                   // frost along the top edge
      for (let i = 0; i < 2600 * o.frost; i++) {
        const x = R() * W, y = Math.pow(R(), 3) * H * 0.16;
        g.fillStyle = `rgba(240,248,250,${0.15 + R() * 0.45})`;
        g.fillRect(x, y, 1 + R() * 2.5, 1 + R() * 1.5);
      }
    }
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
    return t;
  }

  function enamel(o) {
    return new THREE.MeshStandardMaterial({ map: panelTexture(o), roughness: 0.52, metalness: 0.12 });
  }
  const copper = () => new THREE.MeshStandardMaterial({ color: 0xb8733f, metalness: 0.88, roughness: 0.34 });
  const galv = () => new THREE.MeshStandardMaterial({ color: 0x8e9ba3, metalness: 0.75, roughness: 0.45 });
  const dark = () => new THREE.MeshStandardMaterial({ color: 0x2a3236, metalness: 0.3, roughness: 0.6 });
  const glycol = () => new THREE.MeshStandardMaterial({ color: 0x2f9cc8, metalness: 0.15, roughness: 0.22 });

  function box(w, h, d, mat, x, y, z) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    m.position.set(x, y, z); return m;
  }
  function cyl(r, h, mat, x, y, z, seg) {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg || 40), mat);
    m.position.set(x, y, z); return m;
  }

  /* A fan shroud: a short ring with a five-blade fan and a hub, axis +y. */
  function fan(r, mat, bladeMat) {
    const g = new THREE.Group();
    const ring = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.12, 48, 1, true), mat);
    ring.material.side = THREE.DoubleSide; g.add(ring);
    const lip = new THREE.Mesh(new THREE.TorusGeometry(r, 0.025, 10, 48), mat);
    lip.rotation.x = Math.PI / 2; lip.position.y = 0.06; g.add(lip);
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.16, r * 0.16, 0.08, 24), bladeMat);
    g.add(hub);
    for (let i = 0; i < 5; i++) {
      const b = new THREE.Mesh(new THREE.BoxGeometry(r * 0.78, 0.012, r * 0.26), bladeMat);
      b.position.set(Math.cos(i * 1.2566) * r * 0.47, 0, Math.sin(i * 1.2566) * r * 0.47);
      b.rotation.y = -i * 1.2566; b.rotation.x = 0.28; g.add(b);
    }
    const guard = new THREE.Mesh(new THREE.TorusGeometry(r * 0.55, 0.008, 6, 40), mat);
    guard.rotation.x = Math.PI / 2; guard.position.y = 0.07; g.add(guard);
    return g;
  }

  CPL.module = function (R, o) {
    o = o || {};
    const seed = o.seed || 20261124;
    const g = new THREE.Group();
    const L = 4.0, H = 2.2, D = 2.4, skidH = 0.16;
    // skid rails
    const rail = dark();
    g.add(box(L + 0.3, skidH, 0.18, rail, 0, skidH / 2, D / 2 - 0.15));
    g.add(box(L + 0.3, skidH, 0.18, rail, 0, skidH / 2, -D / 2 + 0.15));
    // body: six faces, front and back with louvers, ends plain
    const front = enamel({ seed, panels: 8, louver: true, frost: o.frost || 0 });
    const end = enamel({ seed: seed + 1, panels: 4, frost: o.frost || 0 });
    const top = new THREE.MeshStandardMaterial({ color: 0x9aa19d, roughness: 0.6, metalness: 0.1 });
    const mats = [end, end, top, top, front, front];
    const body = new THREE.Mesh(new THREE.BoxGeometry(L, H, D), mats);
    body.position.y = skidH + H / 2; g.add(body);
    // roof trim and a door on the front face
    g.add(box(L + 0.06, 0.06, D + 0.06, galv(), 0, skidH + H + 0.03, 0));
    g.add(box(0.9, 1.7, 0.03, new THREE.MeshStandardMaterial({ color: 0x8f9793, roughness: 0.5, metalness: 0.15 }),
      -0.9, skidH + 0.86, D / 2 + 0.016));
    g.add(box(0.04, 0.22, 0.05, galv(), -0.55, skidH + 0.9, D / 2 + 0.04));

    // ---- coupling one: the grid. Service entrance box on the left end face,
    // a meter ring, and a copper feeder running down and away along -x.
    const seX = -L / 2 - 0.14, seY = skidH + 1.25, seZ = 0.35;
    g.add(box(0.26, 0.86, 0.6, new THREE.MeshStandardMaterial({ color: 0x6f7874, roughness: 0.45, metalness: 0.35 }),
      seX, seY, seZ));
    const meter = cyl(0.17, 0.12, new THREE.MeshStandardMaterial({ color: 0xdde6ea, roughness: 0.08, metalness: 0.0,
      transparent: true, opacity: 0.85 }), seX - 0.16, seY - 0.08, seZ, 40);
    meter.rotation.z = Math.PI / 2; g.add(meter);
    const feeder = AKT.tube([[seX, seY + 0.43, seZ], [seX, seY + 0.9, seZ], [seX - 0.4, seY + 1.0, seZ],
      [seX - 1.3, 0.55, seZ + 0.2], [seX - 3.4, 0.12, seZ + 0.5], [seX - 9, 0.12, seZ + 1.3]], 0.065, copper(),
      { segments: 160, radial: 16, tension: 0.4 });
    g.add(feeder);
    const gridPt = [seX, seY + 0.72, seZ];

    // ---- coupling two: generators. A skid on the right with an enclosure,
    // an exhaust stack with a rain cap, and a breaker box facing the camera.
    const gx = L / 2 + 0.95;
    g.add(box(1.5, 0.12, 1.7, rail, gx, 0.06, 0.1));
    g.add(box(1.3, 0.9, 1.3, enamel({ seed: seed + 2, panels: 3, louver: true }), gx, 0.57, 0.1));
    const stack = cyl(0.11, 1.9, galv(), gx + 0.3, 1.95, -0.25, 32); g.add(stack);
    const silencer = cyl(0.22, 0.6, galv(), gx + 0.3, 1.35, -0.25, 40); g.add(silencer);
    const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.02, 32), galv());
    cap.position.set(gx + 0.3, 2.95, -0.18); cap.rotation.x = 0.5; g.add(cap);
    const brk = box(0.42, 0.5, 0.18, new THREE.MeshStandardMaterial({ color: 0x7a827e, roughness: 0.45, metalness: 0.3 }),
      gx - 0.2, 0.62, 0.84); g.add(brk);
    const genPt = [gx - 0.2, 0.92, 0.84];
    // cable from the skid to the body
    g.add(AKT.tube([[gx - 0.7, 0.3, 0.6], [L / 2 + 0.05, 0.35, 0.6], [L / 2 + 0.02, 0.9, 0.6]], 0.045, dark(), { segments: 40 }));

    // ---- coupling three: cooling. A dry cooler frame on the roof with four
    // fan shrouds, finned sides, and glycol risers down the back corner.
    const roofY = skidH + H + 0.06;
    const cg = new THREE.Group();
    const frame = galv();
    const cw = 3.3, cd = 1.5, ch = 0.55;
    cg.add(box(cw, 0.06, cd, frame, 0, ch, 0));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) cg.add(box(0.07, ch, 0.07, frame, sx * cw / 2, ch / 2, sz * cd / 2));
    const finMat = new THREE.MeshStandardMaterial({ color: 0xb8c0c2, metalness: 0.7, roughness: 0.42 });
    const finGeo = new THREE.BoxGeometry(0.012, ch - 0.1, cd - 0.08);
    const nf = 120, fins = new THREE.InstancedMesh(finGeo, finMat, nf);
    const mtx = new THREE.Matrix4();
    for (let i = 0; i < nf; i++) { mtx.makeTranslation(-cw / 2 + 0.06 + i * (cw - 0.12) / (nf - 1), ch / 2, 0); fins.setMatrixAt(i, mtx); }
    cg.add(fins);
    const blade = dark();
    for (let i = 0; i < 4; i++) {
      const f = fan(0.34, galv(), blade); f.position.set(-cw / 2 + cw * (i + 0.5) / 4, ch + 0.06, 0); cg.add(f);
    }
    cg.position.set(0.1, roofY, -0.15); g.add(cg);
    // glycol supply (blue) and return (copper toned) headers along the roof front
    const hz = -0.15 + cd / 2 + 0.12, hy = roofY + 0.18;
    g.add(AKT.tube([[-1.6, hy, hz], [1.8, hy, hz]], 0.05, glycol(), { segments: 40 }));
    g.add(AKT.tube([[-1.6, hy + 0.14, hz], [1.8, hy + 0.14, hz]], 0.05,
      new THREE.MeshStandardMaterial({ color: 0xc0784a, metalness: 0.4, roughness: 0.3 }), { segments: 40 }));
    // risers down the right front corner into the body
    g.add(AKT.tube([[1.8, hy, hz], [1.95, hy - 0.1, hz], [L / 2 - 0.08, roofY - 0.5, D / 2 + 0.08]], 0.05, glycol(), { segments: 30 }));
    g.add(AKT.tube([[1.8, hy + 0.14, hz], [2.02, hy, hz], [L / 2 - 0.02, roofY - 0.4, D / 2 + 0.1]], 0.05,
      new THREE.MeshStandardMaterial({ color: 0xc0784a, metalness: 0.4, roughness: 0.3 }), { segments: 30 }));
    const tee = cyl(0.075, 0.2, glycol(), 0.2, hy, hz, 24); tee.rotation.x = Math.PI / 2; g.add(tee);
    const coolPt = [0.2, hy, hz + 0.1];

    AKT.add(R, g);
    const hull = [];
    const bb = new THREE.Box3().setFromObject(new THREE.Group().add(body.clone()));
    const add8 = (x0, x1, y0, y1, z0, z1) => { for (const x of [x0, x1]) for (const y of [y0, y1]) for (const z of [z0, z1]) hull.push([x, y, z]); };
    add8(-L / 2 - 0.3, L / 2 + 0.1, 0, roofY + 0.7, -D / 2, D / 2);            // body plus cooler
    add8(gx - 0.75, gx + 0.75, 0, 0.12, -0.75, 0.95);                          // skid
    hull.push([gx + 0.3, 2.98, -0.25], [gx + 0.3, 2.98, -0.1]);                 // stack top
    return { group: g, body, points: { grid: gridPt, gen: genPt, cool: coolPt }, hull, dims: { L, H, D, skidH, roofY } };
  };

  /* The cooler bank for the close-up frame: a long finned coil bank on a
   * galvanized frame with a row of fan shrouds and two glycol headers along
   * its front with a tee. Axis along +x, front face toward +z. */
  CPL.bank = function (R, o) {
    o = o || {};
    const g = new THREE.Group();
    const len = o.length || 9, depth = 1.6, hgt = 1.3;
    const frame = galv();
    for (const z of [-depth / 2, depth / 2]) {
      g.add(box(len, 0.08, 0.08, frame, 0, 0.45, z));
      g.add(box(len, 0.08, 0.08, frame, 0, 0.45 + hgt, z));
    }
    for (let x = -len / 2; x <= len / 2 + 1e-6; x += len / 6)
      for (const z of [-depth / 2, depth / 2]) g.add(box(0.1, 0.45 + hgt, 0.1, frame, x, (0.45 + hgt) / 2, z));
    const finMat = new THREE.MeshStandardMaterial({ color: 0xc2c9cb, metalness: 0.78, roughness: 0.38 });
    const nf = o.fins || 180;
    const fins = new THREE.InstancedMesh(new THREE.BoxGeometry(0.014, hgt - 0.12, depth - 0.12), finMat, nf);
    const m = new THREE.Matrix4();
    for (let i = 0; i < nf; i++) { m.makeTranslation(-len / 2 + 0.1 + i * (len - 0.2) / (nf - 1), 0.45 + hgt / 2, 0); fins.setMatrixAt(i, m); }
    g.add(fins);
    // coil tubes threading the fins (the copper return bends on the front)
    const tubeMat = new THREE.MeshStandardMaterial({ color: 0xb8733f, metalness: 0.85, roughness: 0.3 });
    for (let r = 0; r < 6; r++) {
      const y = 0.58 + r * (hgt - 0.26) / 5;
      const t = cyl(0.022, len - 0.2, tubeMat, 0, y, depth / 2 - 0.05, 12); t.rotation.z = Math.PI / 2; g.add(t);
    }
    const blade = dark(), nfan = o.fans || 4;
    for (let i = 0; i < nfan; i++) {
      const f = fan(0.62, galv(), blade); f.position.set(-len / 2 + len * (i + 0.5) / nfan, 0.45 + hgt + 0.08, 0); g.add(f);
    }
    g.add(box(len, 0.03, depth, frame, 0, 0.45 + hgt + 0.02, 0));
    // headers along the front, on saddles
    const hz = depth / 2 + 0.32, sy = 0.62, ry = 0.9;
    g.add(AKT.tube([[-len / 2 - 3, sy, hz], [len / 2 + 3, sy, hz]], 0.09, glycol(), { segments: 60 }));
    g.add(AKT.tube([[-len / 2 - 3, ry, hz], [len / 2 + 3, ry, hz]], 0.09,
      new THREE.MeshStandardMaterial({ color: 0xc0784a, metalness: 0.4, roughness: 0.28 }), { segments: 60 }));
    for (let x = -len / 2; x <= len / 2 + 1e-6; x += len / 4) {
      g.add(box(0.14, sy - 0.08, 0.2, frame, x, (sy - 0.08) / 2, hz));
      g.add(box(0.06, ry - sy, 0.06, frame, x, (sy + ry) / 2, hz - 0.12));
    }
    const teeX = o.teeX != null ? o.teeX : 0.6;
    const tee = cyl(0.13, 0.38, glycol(), teeX, sy, hz + 0.1, 32); tee.rotation.x = Math.PI / 2; g.add(tee);
    const flange = cyl(0.17, 0.04, galv(), teeX, sy, hz + 0.3, 32); flange.rotation.x = Math.PI / 2; g.add(flange);
    for (let i = 0; i < 8; i++) {
      const bolt = cyl(0.016, 0.06, galv(), teeX + Math.cos(i * 0.785) * 0.145, sy + Math.sin(i * 0.785) * 0.145, hz + 0.32, 8);
      bolt.rotation.x = Math.PI / 2; g.add(bolt);
    }
    AKT.add(R, g);
    return { group: g, tee: [teeX, sy, hz + 0.32], header: { supplyY: sy, returnY: ry, z: hz }, len };
  };

  return CPL;
}
