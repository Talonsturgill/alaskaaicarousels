/* akdrone.js (2026-11-04, No.105): a small FPV quadcopter built for akthree.
 * ES module. build(THREE, AKT, opts) returns a THREE.Group, metres, origin at
 * the frame's centre, +z forward (camera pod), +y up. Parts are named so a
 * slide can find them (userData.part). Props are drawn as motion discs when
 * opts.spin is true (a translucent swept disc plus two faint blades), and as
 * three still blades otherwise.
 * Materials are passed in or default to carbon, anodised aluminium, a soft
 * pack wrap and copper motor windings. Nothing here draws a weapon: a payload
 * is a plain strapped box with a tether, named "payload". */
export function build(THREE, AKT, opts) {
  opts = opts || {};
  const g = new THREE.Group();
  const S = opts.scale || 1;
  /* carbon twill: a 2x2 twill drawn once into a canvas, used as the albedo and
   * the roughness map, so the plates read as woven fibre under a raking key and
   * not as black plastic. Deterministic: no randomness. */
  function twill() {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const x = c.getContext('2d');
    x.fillStyle = '#1a1d22'; x.fillRect(0, 0, 256, 256);
    const t = 16;
    for (let j = 0; j < 256 / t; j++) for (let i = 0; i < 256 / t; i++) {
      const warp = ((i + j) >> 1) % 2 === 0;
      const gx = x.createLinearGradient(i * t, j * t, warp ? i * t + t : i * t, warp ? j * t : j * t + t);
      gx.addColorStop(0, warp ? '#2b3038' : '#121418'); gx.addColorStop(0.5, warp ? '#3a414b' : '#1c2026'); gx.addColorStop(1, warp ? '#22262c' : '#0e1013');
      x.fillStyle = gx; x.fillRect(i * t + 0.5, j * t + 0.5, t - 1, t - 1);
    }
    const tex = new THREE.CanvasTexture(c); tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(opts.weaveRepeat || 40, opts.weaveRepeat || 40);
    tex.anisotropy = 8; tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }
  const weave = opts.weave === false ? null : twill();
  const carbon = opts.carbon || new THREE.MeshStandardMaterial({ color: 0xffffff, map: weave, roughness: 0.38, metalness: 0.3 });
  const carbonEdge = new THREE.MeshStandardMaterial({ color: 0x2a2f36, roughness: 0.5, metalness: 0.4 });
  const alu = opts.alu || new THREE.MeshStandardMaterial({ color: opts.aluColor || 0xb8c2cc, roughness: 0.28, metalness: 0.92 });
  const bell = opts.bell || new THREE.MeshStandardMaterial({ color: opts.bellColor || 0x3c4651, roughness: 0.3, metalness: 0.85 });
  const copper = new THREE.MeshStandardMaterial({ color: 0xb06a3a, roughness: 0.35, metalness: 0.9 });
  const wrap = opts.wrap || new THREE.MeshStandardMaterial({ color: opts.packColor || 0x1d2a36, roughness: 0.62, metalness: 0.05 });
  const strap = new THREE.MeshStandardMaterial({ color: opts.strapColor || 0x0d0f12, roughness: 0.85 });
  const lens = new THREE.MeshStandardMaterial({ color: 0x05070a, roughness: 0.06, metalness: 0.2 });
  const tag = (m, part) => { m.userData.part = part; return m; };
  const L = 0.115 * S;            // arm reach (motor centre from frame centre), a 5 inch class quad
  const armW = 0.016 * S, plate = 0.004 * S;
  // bottom plate: a body plus four arms at 45 degrees (true X)
  const body = new THREE.Shape();
  const bw = 0.034 * S, bl = 0.06 * S;
  body.moveTo(-bw, -bl); body.lineTo(bw, -bl); body.lineTo(bw, bl); body.lineTo(-bw, bl); body.closePath();
  const bodyGeo = new THREE.ExtrudeGeometry(body, { depth: plate, bevelEnabled: true, bevelThickness: 0.0008 * S, bevelSize: 0.0008 * S, bevelSegments: 2 });
  const bodyM = tag(new THREE.Mesh(bodyGeo, carbon), 'frame');
  bodyM.rotation.x = -Math.PI / 2; bodyM.position.y = 0; g.add(bodyM);
  const motors = [];
  for (let k = 0; k < 4; k++) {
    const a = Math.PI / 4 + k * Math.PI / 2;
    const mx = Math.sin(a) * L, mz = Math.cos(a) * L;
    // arm: a tapered bar from the body to the motor mount
    const len = L - 0.01 * S;
    const arm = new THREE.Shape();
    arm.moveTo(-armW * 0.62, 0); arm.lineTo(armW * 0.62, 0); arm.lineTo(armW * 0.5, len); arm.lineTo(-armW * 0.5, len); arm.closePath();
    const ag = new THREE.ExtrudeGeometry(arm, { depth: plate * 1.4, bevelEnabled: true, bevelThickness: 0.0007 * S, bevelSize: 0.0007 * S, bevelSegments: 2 });
    const am = tag(new THREE.Mesh(ag, carbon), 'arm');
    am.rotation.x = -Math.PI / 2; am.rotation.z = -a; am.position.y = -0.0005 * S; g.add(am);
    // motor mount disc
    const mount = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.014 * S, 0.014 * S, plate * 1.4, 32), carbonEdge), 'mount');
    mount.position.set(mx, plate * 0.7, mz); g.add(mount);
    // motor: stator ring (copper peeking), bell, shaft
    const mg = new THREE.Group(); mg.position.set(mx, plate * 1.4, mz);
    const stator = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0115 * S, 0.0115 * S, 0.004 * S, 36), copper), 'stator');
    stator.position.y = 0.002 * S; mg.add(stator);
    const bellM = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0128 * S, 0.0138 * S, 0.012 * S, 48, 1, false), bell), 'bell');
    bellM.position.y = 0.0105 * S; mg.add(bellM);
    // cooling slots on the bell top: six small dark wedges
    for (let s = 0; s < 6; s++) {
      const sl = new THREE.Mesh(new THREE.BoxGeometry(0.0035 * S, 0.0006 * S, 0.006 * S), strap);
      const sa = s * Math.PI / 3; sl.position.set(Math.sin(sa) * 0.0075 * S, 0.0168 * S, Math.cos(sa) * 0.0075 * S); sl.rotation.y = sa; mg.add(sl);
    }
    const nut = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0035 * S, 0.0035 * S, 0.005 * S, 6), alu), 'nut');
    nut.position.y = 0.022 * S; mg.add(nut);
    // propeller
    const pg = new THREE.Group(); pg.position.y = 0.0195 * S; pg.userData.part = 'prop';
    const R = 0.064 * S;
    /* a motion disc is a glass-like shell: near-black albedo so it does not
     * milk what is behind it, read carried by the environment, and out of the
     * shadow pass both ways (the AKT.mat.glass rules, No.82). */
    const discMat = (op) => { const m = new THREE.MeshStandardMaterial({ color: opts.propColor || 0x161c22,
      roughness: 0.25, metalness: 0.2, transparent: true, opacity: op, side: THREE.DoubleSide, depthWrite: false, envMapIntensity: 1.6 });
      m.userData.aktNoShadow = true; return m; };
    if (opts.spin) {
      const disc = new THREE.Mesh(new THREE.RingGeometry(0.008 * S, R, 64, 1),
        discMat(0.16));
      disc.rotation.x = -Math.PI / 2; pg.add(disc);
      const rim = new THREE.Mesh(new THREE.RingGeometry(R * 0.93, R, 64, 1),
        discMat(0.3));
      rim.rotation.x = -Math.PI / 2; rim.position.y = 0.0002 * S; pg.add(rim);
    } else {
      const bladeMat = new THREE.MeshStandardMaterial({ color: opts.propColor || 0x4a5866, roughness: 0.3, metalness: 0.1 });
      for (let b = 0; b < 3; b++) {
        const sh = new THREE.Shape();
        sh.moveTo(0, -0.004 * S);
        sh.bezierCurveTo(R * 0.35, -0.011 * S, R * 0.8, -0.009 * S, R, -0.002 * S);
        sh.bezierCurveTo(R * 0.98, 0.006 * S, R * 0.6, 0.007 * S, 0, 0.004 * S);
        const bg = new THREE.ExtrudeGeometry(sh, { depth: 0.0012 * S, bevelEnabled: false });
        const bm = tag(new THREE.Mesh(bg, bladeMat), 'blade');
        bm.rotation.x = -Math.PI / 2 + 0.16; bm.rotation.z = 0;
        const holder = new THREE.Group(); holder.rotation.y = b * 2 * Math.PI / 3 + k * 0.7; holder.add(bm); pg.add(holder);
      }
    }
    mg.add(pg); g.add(mg); motors.push(mg);
  }
  // standoffs and top plate
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
    const so = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0022 * S, 0.0022 * S, 0.026 * S, 12), alu), 'standoff');
    so.position.set(sx * bw * 0.8, plate + 0.013 * S, sz * bl * 0.8); g.add(so);
  }
  const top = tag(new THREE.Mesh(new THREE.BoxGeometry(bw * 2, plate * 0.8, bl * 2.05), carbon), 'top');
  top.position.y = plate + 0.026 * S; g.add(top);
  // flight stack between the plates: two boards on nylon posts, gold pads, and
  // motor leads running along each arm (so the frame reads as wired, not toy)
  const pcb = new THREE.MeshStandardMaterial({ color: 0x0c1410, roughness: 0.55, metalness: 0.2 });
  const pad = new THREE.MeshStandardMaterial({ color: 0xc9a24a, roughness: 0.3, metalness: 0.95 });
  for (let b = 0; b < 2; b++) {
    const board = tag(new THREE.Mesh(new THREE.BoxGeometry(0.03 * S, 0.0016 * S, 0.03 * S), pcb), 'board');
    board.position.y = plate + 0.007 * S + b * 0.009 * S; g.add(board);
    for (let q = 0; q < 8; q++) {
      const pd = new THREE.Mesh(new THREE.BoxGeometry(0.0028 * S, 0.0006 * S, 0.0018 * S), pad);
      const side = q < 4 ? -1 : 1; pd.position.set(side * 0.0128 * S, board.position.y + 0.001 * S, (-0.0105 + (q % 4) * 0.007) * S); g.add(pd);
    }
  }
  const wireMat = new THREE.MeshStandardMaterial({ color: 0x101214, roughness: 0.7 });
  for (let k = 0; k < 4; k++) {
    const a = Math.PI / 4 + k * Math.PI / 2;
    for (let w = -1; w <= 1; w++) {
      const off = w * 0.0022 * S, ox = Math.cos(a) * off, oz = -Math.sin(a) * off;
      const p0 = new THREE.Vector3(Math.sin(a) * 0.02 * S + ox, plate * 1.6, Math.cos(a) * 0.02 * S + oz);
      const p1 = new THREE.Vector3(Math.sin(a) * (L - 0.016 * S) + ox, plate * 1.6, Math.cos(a) * (L - 0.016 * S) + oz);
      const wire = tag(new THREE.Mesh(new THREE.TubeGeometry(new THREE.LineCurve3(p0, p1), 4, 0.0007 * S, 6, false), wireMat), 'wire');
      g.add(wire);
    }
  }
  // battery pack on top with a strap
  const packH = 0.026 * S, packW = 0.036 * S, packL = 0.075 * S;
  const ps = new THREE.Shape(); const pr = 0.005 * S, hw = packW / 2, hh = packH / 2;
  ps.moveTo(-hw + pr, -hh); ps.lineTo(hw - pr, -hh); ps.quadraticCurveTo(hw, -hh, hw, -hh + pr);
  ps.lineTo(hw, hh - pr); ps.quadraticCurveTo(hw, hh, hw - pr, hh); ps.lineTo(-hw + pr, hh);
  ps.quadraticCurveTo(-hw, hh, -hw, hh - pr); ps.lineTo(-hw, -hh + pr); ps.quadraticCurveTo(-hw, -hh, -hw + pr, -hh);
  const pgeo = new THREE.ExtrudeGeometry(ps, { depth: packL, bevelEnabled: true, bevelThickness: 0.002 * S, bevelSize: 0.0015 * S, bevelSegments: 3, curveSegments: 6 });
  pgeo.translate(0, 0, -packL / 2);
  const pack = tag(new THREE.Mesh(pgeo, wrap), 'battery');
  pack.position.y = plate + 0.026 * S + packH / 2 + 0.0015 * S; g.add(pack);
  // soften the pack: a bevel is faked by a slightly larger rounded cap
  const st = tag(new THREE.Mesh(new THREE.BoxGeometry(packW + 0.0045 * S, packH + 0.0045 * S, 0.01 * S), strap), 'strap');
  st.position.copy(pack.position); g.add(st);
  const lead = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0022 * S, 0.0022 * S, 0.05 * S, 10), new THREE.MeshStandardMaterial({ color: 0x8a1b1b, roughness: 0.5 })), 'lead');
  lead.rotation.x = Math.PI / 2.4; lead.position.set(0.008 * S, pack.position.y - 0.004 * S, -packL / 2 - 0.012 * S); g.add(lead);
  // camera pod at the front, tilted up 25 degrees, with a lens
  const cam = new THREE.Group(); cam.position.set(0, plate + 0.013 * S, bl * 0.92); cam.rotation.x = -0.44;
  const camBody = tag(new THREE.Mesh(new THREE.BoxGeometry(0.019 * S, 0.019 * S, 0.016 * S), carbonEdge), 'camera'); cam.add(camBody);
  const barrel = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0065 * S, 0.0075 * S, 0.008 * S, 32), alu), 'lens');
  barrel.rotation.x = Math.PI / 2; barrel.position.z = 0.011 * S; cam.add(barrel);
  const glass = tag(new THREE.Mesh(new THREE.CircleGeometry(0.0055 * S, 32), lens), 'glass');
  glass.position.z = 0.0152 * S; cam.add(glass); g.add(cam);
  // antenna at the back: a short mast and a clover cap
  const mast = tag(new THREE.Mesh(new THREE.CylinderGeometry(0.0012 * S, 0.0012 * S, 0.045 * S, 8), strap), 'antenna');
  mast.position.set(0, plate + 0.05 * S, -bl * 1.05); mast.rotation.x = -0.6; g.add(mast);
  const cap = tag(new THREE.Mesh(new THREE.SphereGeometry(0.0052 * S, 16, 12), new THREE.MeshStandardMaterial({ color: opts.capColor || 0xd84a1b, roughness: 0.55 })), 'antenna_cap');
  cap.position.set(0, plate + 0.068 * S, -bl * 1.05 - 0.0135 * S); g.add(cap);
  // optional payload: a plain strapped box slung under the body
  if (opts.payload) {
    const pl = tag(new THREE.Mesh(new THREE.BoxGeometry(0.03 * S, 0.034 * S, 0.05 * S), opts.payloadMat || new THREE.MeshStandardMaterial({ color: 0x3f4a33, roughness: 0.8 })), 'payload');
    pl.position.y = -0.024 * S; g.add(pl);
    const band = new THREE.Mesh(new THREE.BoxGeometry(0.032 * S, 0.036 * S, 0.006 * S), strap); band.position.copy(pl.position); g.add(band);
  }
  g.userData.motors = motors;
  g.userData.armReach = L;
  return g;
}

/* explode(group, e, opts): move each named part along the build axis by its
 * assembly layer times e (0 = assembled, 1 = fully exploded). Layers are the
 * order a builder stacks a quad: bottom plate and arms (0), motor mounts and
 * motors (1, outward along the arm as well), propellers (2.2), flight boards
 * (1.1), standoffs (1.6), top plate (2.4), battery and strap (3.4), antenna
 * (2.9, and back), camera (1.2, and forward). `gap` is metres per layer at
 * e = 1. Base positions are recorded on first call, so explode can be called
 * again with any e. Returns the group. */
export function explode(group, e, opts) {
  opts = opts || {};
  const gap = (opts.gap != null ? opts.gap : 0.05);
  const out = (opts.outward != null ? opts.outward : 0.25);
  const LAYER = { frame: 0, arm: 0, mount: 1, board: 1.1, wire: 0.4, camera: 1.2, lens: 0, glass: 0,
    standoff: 1.6, top: 2.4, battery: 3.4, strap: 3.4, lead: 3.4, antenna: 2.9, antenna_cap: 2.9 };
  group.traverse(m => {
    if (!m.isMesh && !(m.isGroup && m.userData.part === 'prop')) return;
    if (!m.userData.base) m.userData.base = m.position.clone();
    const p = m.userData.part;
    if (p === 'prop') { m.position.copy(m.userData.base); m.position.y += 1.2 * gap * e; return; }
    if (m.parent && m.parent !== group) return;   // children of motor or camera groups move with them
    const L = LAYER[p]; if (L == null) return;
    m.position.copy(m.userData.base); m.position.y += L * gap * e;
    if (p === 'antenna' || p === 'antenna_cap') m.position.z -= 0.6 * gap * e;
  });
  (group.userData.motors || []).forEach(mg => {
    if (!mg.userData.base) mg.userData.base = mg.position.clone();
    const b = mg.userData.base; mg.position.copy(b);
    mg.position.y += 1 * gap * e; mg.position.x += b.x * out * e; mg.position.z += b.z * out * e;
  });
  group.children.forEach(c => { if (c.isGroup && c.userData.motors == null && c !== group && !(group.userData.motors || []).includes(c)) {
    if (!c.userData.base) c.userData.base = c.position.clone();
    c.position.copy(c.userData.base); c.position.y += 1.2 * gap * e; c.position.z += 0.5 * gap * e; } });
  return group;
}
