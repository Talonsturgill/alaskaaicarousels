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
  const carbon = opts.carbon || new THREE.MeshStandardMaterial({ color: 0x14171b, roughness: 0.42, metalness: 0.35 });
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
    if (opts.spin) {
      const disc = new THREE.Mesh(new THREE.RingGeometry(0.008 * S, R, 64, 1),
        new THREE.MeshStandardMaterial({ color: opts.propColor || 0x8fa6b8, roughness: 0.4, metalness: 0.1, transparent: true, opacity: 0.13, side: THREE.DoubleSide, depthWrite: false }));
      disc.rotation.x = -Math.PI / 2; pg.add(disc);
      const rim = new THREE.Mesh(new THREE.RingGeometry(R * 0.93, R, 64, 1),
        new THREE.MeshStandardMaterial({ color: opts.propColor || 0x8fa6b8, roughness: 0.4, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false }));
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
