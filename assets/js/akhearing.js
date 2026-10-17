/* akhearing.js — the witness table, its gooseneck microphone and the witness chair, as one PBR room.
 * (Alaska.Ai, No.88, 2026-10-16.) An ES module for akthree slides: the same room, same camera and same
 * light on the two frames that bookend the deck, so the only things that change are the microphone's
 * state and the chair's, which is the point of the bookend.
 *
 *   const THREE = await import('@@ASSETS@@/js/three.module.min.js');
 *   const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
 *   const H = (await import('@@ASSETS@@/js/akhearing.js')).init(THREE, AKT);
 *   const R = AKT.setup(canvas, {w:1080, h:1350, bg:0x070a11, exposure:1.0});
 *   const room = H.build(R, {mic: 'folded' | 'raised', chair: 'tucked' | 'out', seed});
 *   H.camera(R);                   // the locked camera both frames share
 *
 * Units are metres. The table top is at y 0.76, its witness-side edge at z 0.2, x from -1.2 to 1.2.
 * Every texture is drawn on a canvas from a seed, nothing is loaded, nothing calls Math.random.
 * Text never goes in here; type stays DOM.
 */
export function init(THREE, AKT) {
  const H = {};
  function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  // a satin walnut top: long fine figure along x, a few broad darker streaks, wear near the witness edge
  function walnutTexture(seed) {
    const c = document.createElement('canvas'); c.width = 2048; c.height = 1024; const x = c.getContext('2d');
    const r = rng(seed);
    x.fillStyle = '#3a2b21'; x.fillRect(0, 0, 2048, 1024);
    for (let i = 0; i < 900; i++) {
      const y = r() * 1024, a = 0.03 + r() * 0.07, w = 0.6 + r() * 2.4, amp = 2 + r() * 10, ph = r() * 6.28, f = 0.002 + r() * 0.004;
      x.strokeStyle = r() < 0.5 ? `rgba(12,8,6,${a})` : `rgba(74,56,42,${a * 0.8})`; x.lineWidth = w;
      x.beginPath(); for (let px = -10; px <= 2058; px += 16) { const py = y + Math.sin(px * f + ph) * amp + Math.sin(px * f * 3.1 + ph * 2) * amp * 0.3; px === -10 ? x.moveTo(px, py) : x.lineTo(px, py); } x.stroke();
    }
    const g = x.createLinearGradient(0, 1024, 0, 700); g.addColorStop(0, 'rgba(90,70,54,0.18)'); g.addColorStop(1, 'rgba(90,70,54,0)');
    x.fillStyle = g; x.fillRect(0, 700, 2048, 324);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping; return t;
  }
  // roughness: satin overall, a little glossier where hands and papers have polished it
  function walnutRough(seed) {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const x = c.getContext('2d'); const r = rng(seed + 7);
    x.fillStyle = 'rgb(92,92,92)'; x.fillRect(0, 0, 1024, 512);
    for (let i = 0; i < 260; i++) { const cx = r() * 1024, cy = 300 + r() * 212, rr = 20 + r() * 90; const g = x.createRadialGradient(cx, cy, 0, cx, cy, rr); g.addColorStop(0, 'rgba(60,60,60,0.35)'); g.addColorStop(1, 'rgba(60,60,60,0)'); x.fillStyle = g; x.fillRect(cx - rr, cy - rr, rr * 2, rr * 2); }
    for (let i = 0; i < 400; i++) { x.strokeStyle = `rgba(140,140,140,${0.05 + r() * 0.08})`; x.lineWidth = 0.5 + r(); const y = r() * 512, x0 = r() * 1024; x.beginPath(); x.moveTo(x0, y); x.lineTo(x0 + 30 + r() * 140, y + (r() - 0.5) * 6); x.stroke(); }
    const t = new THREE.CanvasTexture(c); return t;
  }
  // the microphone grille: fine perforation as a bump
  function grilleBump() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256; const x = c.getContext('2d');
    x.fillStyle = '#ffffff'; x.fillRect(0, 0, 256, 256); x.fillStyle = '#000000';
    for (let j = 0; j < 32; j++) for (let i = 0; i < 32; i++) { x.beginPath(); x.arc(i * 8 + (j % 2) * 4 + 4, j * 8 + 4, 2.2, 0, 6.283); x.fill(); }
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 2); return t;
  }
  // upholstery: a fine twill as albedo variation
  function twill(seed) {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512; const x = c.getContext('2d'); const r = rng(seed + 31);
    x.fillStyle = '#2b2f38'; x.fillRect(0, 0, 512, 512);
    // a fine, low contrast weave with no single lay: one constant diagonal at 4 px read as scratches across the form (No.88 round 1)
    for (let i = -512; i < 1024; i += 2) { x.strokeStyle = `rgba(${r() < 0.5 ? '30,33,40' : '50,55,66'},${0.06 + r() * 0.06})`; x.lineWidth = 1; x.beginPath(); x.moveTo(i, 0); x.lineTo(i + 512, 512); x.stroke(); }
    for (let i = 0; i < 9000; i++) { const v = 34 + r() * 22; x.fillStyle = `rgba(${v},${v + 3},${v + 10},0.35)`; x.fillRect(r() * 512, r() * 512, 1.5, 1.5); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(6, 6); return t;
  }
  function carpet(seed) {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512; const x = c.getContext('2d'); const r = rng(seed + 47);
    x.fillStyle = '#23262e'; x.fillRect(0, 0, 512, 512);
    for (let i = 0; i < 26000; i++) { const v = 10 + r() * 22; x.fillStyle = `rgba(${v},${v + 2},${v + 8},0.5)`; x.fillRect(r() * 512, r() * 512, 1.2, 1.2); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(10, 10); return t;
  }

  function roundedSlab(w, h, d, r, mat) {
    // a box with rounded vertical edges along x (the front and back lips of a table top), by extruding a rounded rectangle in y-z
    const s = new THREE.Shape(); const hw = d / 2, hh = h / 2;
    s.moveTo(-hw + r, -hh); s.lineTo(hw - r, -hh); s.quadraticCurveTo(hw, -hh, hw, -hh + r); s.lineTo(hw, hh - r); s.quadraticCurveTo(hw, hh, hw - r, hh);
    s.lineTo(-hw + r, hh); s.quadraticCurveTo(-hw, hh, -hw, hh - r); s.lineTo(-hw, -hh + r); s.quadraticCurveTo(-hw, -hh, -hw + r, -hh);
    const g = new THREE.ExtrudeGeometry(s, { depth: w, bevelEnabled: true, bevelThickness: 0.006, bevelSize: 0.006, bevelSegments: 4, curveSegments: 10 });
    g.translate(0, 0, -w / 2); g.rotateY(Math.PI / 2);   // extrusion along x
    // UVs for the top: planar from x,z
    const pos = g.attributes.position, uv = g.attributes.uv;
    for (let i = 0; i < pos.count; i++) uv.setXY(i, (pos.getX(i) + w / 2) / w, (pos.getZ(i) + d / 2) / d);
    return new THREE.Mesh(g, mat);
  }

  H.build = function (R, o) {
    o = o || {}; const seed = o.seed || 881600;
    const made = {};
    // floor
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(14, 14), new THREE.MeshStandardMaterial({ map: carpet(seed), roughness: 0.96, metalness: 0 }));
    floor.rotation.x = -Math.PI / 2; AKT.add(R, floor, { cast: false });
    // the far wall, dark panelling, far enough to fall into fog
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(14, 5), new THREE.MeshStandardMaterial({ color: 0x0c0f15, roughness: 0.7 }));
    wall.position.set(0, 2.5, -3.4); AKT.add(R, wall, { cast: false });
    // the dais rail behind the table: a long low bench front that the focus throws into bokeh
    const dais = new THREE.Mesh(new THREE.BoxGeometry(6, 0.9, 0.12), new THREE.MeshStandardMaterial({ color: 0x15110e, roughness: 0.45 }));
    dais.position.set(0, 0.45, -2.3); AKT.add(R, dais);
    // the witness table
    const topMat = new THREE.MeshPhysicalMaterial({ map: walnutTexture(seed), roughnessMap: walnutRough(seed), roughness: 0.42, metalness: 0, clearcoat: 0.45, clearcoatRoughness: 0.22, envMapIntensity: 1.0 });
    const top = roundedSlab(2.4, 0.05, 0.8, 0.018, topMat); top.position.set(0, 0.735, -0.2); AKT.add(R, top);
    const apron = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.12, 0.7), new THREE.MeshStandardMaterial({ color: 0x15100c, roughness: 0.6 }));
    apron.position.set(0, 0.65, -0.22); AKT.add(R, apron);
    const legMat = new THREE.MeshStandardMaterial({ color: 0x1a130e, roughness: 0.5 });
    [[-1.1, 0.12], [1.1, 0.12], [-1.1, -0.52], [1.1, -0.52]].forEach(([lx, lz]) => { const l = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.7, 0.06), legMat); l.position.set(lx, 0.35, lz); AKT.add(R, l); });
    made.table = top;
    // the ceiling panel the satin reflects: an emissive rectangle above the frame
    const panel = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.9), new THREE.MeshBasicMaterial({ color: 0xfff1dc }));
    panel.material.color.multiplyScalar(o.panel != null ? o.panel : 2.2); panel.rotation.x = Math.PI / 2; panel.position.set(-0.4, 3.3, -0.4); R.scene.add(panel);
    // the dais: a row of small practical lights (members' microphone tally lamps, unlit grey; a few warm reading lamps)
    const lamps = [];
    for (let i = 0; i < 11; i++) { const lx = -2.6 + i * 0.52, warm = (i % 3 === 1);
      const m = new THREE.Mesh(new THREE.SphereGeometry(warm ? 0.035 : 0.018, 16, 10), new THREE.MeshBasicMaterial({ color: warm ? 0xffc98a : 0x7d8fa6 }));
      m.material.color.multiplyScalar(warm ? (o.lamps != null ? o.lamps : 1.4) : 0.6); m.position.set(lx, 0.96, -2.36); R.scene.add(m); lamps.push(m); }
    made.lamps = lamps;
    // the gooseneck microphone
    const metal = new THREE.MeshStandardMaterial({ color: 0x2a2e33, metalness: 0.9, roughness: 0.38, envMapIntensity: 1.5 });
    const mic = new THREE.Group();
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.085, 0.022, 64), metal); base.position.y = 0.011; mic.add(base);
    const collar = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.016, 0.03, 32), metal); collar.position.y = 0.036; mic.add(collar);
    const pts = o.mic === 'raised'
      ? [[0, 0.05, 0], [0, 0.13, 0.0], [0.0, 0.2, 0.03], [0.0, 0.245, 0.09], [0.0, 0.255, 0.15]]
      : [[0, 0.05, 0], [0.0, 0.06, 0.07], [0.02, 0.035, 0.15], [0.05, 0.022, 0.24], [0.08, 0.02, 0.31]];
    const curve = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p)));
    const neck = new THREE.Mesh(new THREE.TubeGeometry(curve, 200, 0.0065, 24, false), new THREE.MeshStandardMaterial({ color: 0x1d2024, metalness: 0.85, roughness: 0.5, envMapIntensity: 1.2 }));
    mic.add(neck);
    // ribbing on the gooseneck: thin tori along the curve
    for (let i = 1; i < 60; i++) { const t = i / 60, p = curve.getPointAt(t), tg = curve.getTangentAt(t); const rib = new THREE.Mesh(new THREE.TorusGeometry(0.0068, 0.0011, 6, 20), metal); rib.position.copy(p); rib.lookAt(p.clone().add(tg)); mic.add(rib); }
    const end = curve.getPointAt(1), dir = curve.getTangentAt(1);
    const head = new THREE.Group();
    const bump = grilleBump();
    const capsule = new THREE.Mesh(new THREE.CylinderGeometry(0.019, 0.016, 0.075, 48, 1, false), new THREE.MeshStandardMaterial({ color: 0x24282d, metalness: 0.8, roughness: 0.46, bumpMap: bump, bumpScale: 1.4, envMapIntensity: 1.4 }));
    capsule.rotation.x = Math.PI / 2; head.add(capsule);
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.019, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x24282d, metalness: 0.8, roughness: 0.46, bumpMap: bump, bumpScale: 1.4 }));
    cap.rotation.x = Math.PI / 2; cap.position.z = 0.0375; head.add(cap);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.0172, 0.0022, 10, 48), new THREE.MeshStandardMaterial({ color: 0x7d8590, metalness: 1, roughness: 0.3 }));   // steel: gold is spent only on the answer owed
    ring.position.z = -0.03; head.add(ring);
    head.position.copy(end).add(dir.clone().multiplyScalar(0.036)); head.lookAt(end.clone().add(dir.clone().multiplyScalar(2)));
    mic.add(head);
    mic.position.set(o.micX != null ? o.micX : 0.05, 0.76, o.micZ != null ? o.micZ : -0.08);
    mic.rotation.y = o.micYaw != null ? o.micYaw : 0.5;
    mic.scale.setScalar(o.micScale || 1.6); AKT.add(R, mic); made.mic = mic; made.micHead = head;
    // the witness chair
    const fabric = new THREE.MeshPhysicalMaterial({ map: twill(seed), roughness: 0.86, sheen: 0.6, sheenRoughness: 0.5, sheenColor: new THREE.Color(0x56607a) });
    if (o.chairTone != null) fabric.color.setScalar(o.chairTone);   // < 1 darkens the upholstery where the chair must stay secondary
    const frame = new THREE.MeshStandardMaterial({ color: 0x1b1e23, metalness: 0.7, roughness: 0.4, envMapIntensity: 1.2 });
    const chair = new THREE.Group();
    function cushion(w, h, d, r) {
      // a rounded-rectangle pad with a deep bevel, extruded along its thickness, crowned slightly on top
      const s = new THREE.Shape(), hw = w / 2 - r, hd = d / 2 - r, rr = Math.min(r, w / 2, d / 2);
      s.moveTo(-w / 2 + rr, -d / 2); s.lineTo(w / 2 - rr, -d / 2); s.quadraticCurveTo(w / 2, -d / 2, w / 2, -d / 2 + rr); s.lineTo(w / 2, d / 2 - rr);
      s.quadraticCurveTo(w / 2, d / 2, w / 2 - rr, d / 2); s.lineTo(-w / 2 + rr, d / 2); s.quadraticCurveTo(-w / 2, d / 2, -w / 2, d / 2 - rr); s.lineTo(-w / 2, -d / 2 + rr); s.quadraticCurveTo(-w / 2, -d / 2, -w / 2 + rr, -d / 2);
      const g = new THREE.ExtrudeGeometry(s, { depth: h - 0.03, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.014, bevelSegments: 6, curveSegments: 14 });
      g.rotateX(-Math.PI / 2); g.translate(0, -(h - 0.03) / 2, 0);
      const p = g.attributes.position;
      for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i); if (y > 0) { const ex = x / (w / 2), ez = z / (d / 2); p.setY(i, y + Math.max(0, 1 - ex * ex) * Math.max(0, 1 - ez * ez) * 0.012); } }
      g.computeVertexNormals(); return g;
    }
    const seat = new THREE.Mesh(cushion(0.5, 0.075, 0.48, 0.06), fabric); seat.position.y = 0.47; chair.add(seat);
    const back = new THREE.Mesh(cushion(0.48, 0.065, 0.46, 0.07), fabric); back.rotation.x = Math.PI / 2 - 0.14; back.position.set(0, 0.8, -0.235); chair.add(back);
    // a tubular steel frame: arms of the backrest run down into the rear legs
    const legPts = [[-0.215, 0.19], [0.215, 0.19], [-0.215, -0.2], [0.215, -0.2]];
    legPts.forEach(([lx, lz]) => { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.009, 0.44, 20), frame); l.position.set(lx, 0.22, lz); chair.add(l); const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.008, 16), new THREE.MeshStandardMaterial({ color: 0x0b0c0e, roughness: 0.8 })); foot.position.set(lx, 0.004, lz); chair.add(foot); });
    const rail = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.028, 0.44), frame); rail.position.y = 0.425; chair.add(rail);
    [[-0.215], [0.215]].forEach(([lx]) => { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.011, 0.56, 16), frame); p.position.set(lx, 0.7, -0.215); p.rotation.x = -0.14; chair.add(p); });
    if (o.chair === 'out') { chair.position.set(o.chairX != null ? o.chairX : 0.1, 0, o.chairZ != null ? o.chairZ : 0.95); chair.rotation.y = o.chairYaw != null ? o.chairYaw : Math.PI + 0.42; }
    else { chair.position.set(o.chairX != null ? o.chairX : -0.55, 0, o.chairZ != null ? o.chairZ : 0.02); chair.rotation.y = Math.PI + (o.chairYaw != null ? o.chairYaw : 0.08); }
    AKT.add(R, chair); made.chair = chair; made.seat = seat;
    return made;
  };

  // the locked camera both frames share: standing behind and to the right of the witness place
  H.CAMERA = { from: [2.55, 2.05, 4.75], look: [-0.12, 0.98, -0.15], fov: 30 };
  H.camera = function (R, o) { const c = Object.assign({}, H.CAMERA, o || {}); AKT.frame(R, c); return c; };

  // one overhead ceiling panel (the key), a weak cool fill, a forget-me-not rim from behind the dais
  H.light = function (R, o) {
    o = o || {};
    const key = new THREE.SpotLight(0xfff1dc, o.key != null ? o.key : 60, 12, o.cone != null ? o.cone : 0.5, 0.55, 1.6);
    key.position.set(-0.9, 4.4, 1.6); key.castShadow = true; key.shadow.mapSize.set(4096, 4096);
        key.shadow.camera.near = 0.5; key.shadow.camera.far = 12; key.shadow.bias = -0.0003; key.shadow.normalBias = 0.01; key.shadow.radius = 6;
    key.target.position.set(o.tx != null ? o.tx : 0.15, 0.3, o.tz != null ? o.tz : 0.35); R.scene.add(key); R.scene.add(key.target);
    const fill = new THREE.DirectionalLight(0x35507a, o.fill != null ? o.fill : 0.5); fill.position.set(3, 1.6, 3); R.scene.add(fill);
    const rim = new THREE.DirectionalLight(0x6ea5ff, o.rim != null ? o.rim : 0.7); rim.position.set(-1.0, 1.4, -4); R.scene.add(rim);
    R.scene.add(new THREE.AmbientLight(0x1c2230, o.ambient != null ? o.ambient : 0.35));
    return { key, fill, rim };
  };
  return H;
}
