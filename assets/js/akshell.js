/* akshell.js — one illustrated warehouse-type building for No.108 (2026-11-07).
 *
 * The deck's GPU frames (01, 06, 09) film ONE building from three stations, so
 * the building lives here once rather than as three private copies (the
 * akdesk/akdrone pattern). It is house furniture for this deck: each slide
 * still owns its camera, its lights, its 2D passes and its composition.
 *
 * WORLD: feet. x runs west (0) to east (250); z runs north (0) to south (200);
 * y up. 250 x 200 ft = 50,000 sq ft [design]. Eave 32 ft. The dock door is in
 * the east wall at z = 100. A gold floor stripe crosses the slab at x = 200,
 * so 40,000 sq ft lie west of it and 10,000 east of it [design].
 * Interior: rack rows run east-west in pairs about aisles centred on
 * z = 110 + 32k. 16 ft racks x 110..200 with their ends on the stripe, mixed
 * (cabinets denser westward), server cabinet rows x 6..106, and the staging
 * floor east of the stripe with loaded pallets set down on the slab.
 *
 * ES module: const SH = (await import('@@ASSETS@@/js/akshell.js')).init(THREE, AKT);
 * Needs window.AK (noise.js) for the seeded textures.
 */
export function init(THREE, AKT) {
  const SH = {};
  const AK = window.AK;
  SH.W = 250; SH.D = 200; SH.EAVE = 32; SH.STRIPE_X = 200;
  SH.DOOR = { x: 250, z: 100, w: 14, h: 16 };
  SH.AISLES = [14, 46, 78, 110, 142, 174];   // aisle centre z values
  SH.RACK_END = 196;                          // rack ends face the stripe

  /* ---- canvas textures ------------------------------------------------- */
  function canvasTex(w, h, draw, o) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d'); draw(g, w, h);
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    if (o && o.srgb) t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    return t;
  }
  // ribbed steel: a rounded rib profile, written as a normal map
  SH.ribNormal = function (ribs) {
    return canvasTex(512, 64, (g, w, h) => {
      const img = g.createImageData(w, h);
      // a rounded rib: the normal turns continuously through the light, so a rib
      // reads as a lit crest falling to a lee trough with width, never as a
      // one-texel flash (round 2: an eased trapezoid still printed hairlines,
      // because only its slopes changed the normal and pans and crests matched)
      const tilt = (u) => 0.85 * Math.sin(2 * Math.PI * ((u * ribs) % 1));
      for (let x = 0; x < w; x++) {
        const d = tilt(x / w);
        const n = Math.hypot(d, 1), nx = -d / n, nz = 1 / n;
        for (let y = 0; y < h; y++) {
          const i = (y * w + x) * 4;
          img.data[i] = (nx * 0.5 + 0.5) * 255; img.data[i + 1] = 128;
          img.data[i + 2] = nz * 255; img.data[i + 3] = 255;
        }
      }
      g.putImageData(img, 0, 0);
    });
  };
  // weathering for steel: low-frequency value variation, seeded
  SH.grime = function (seed, base, amt) {
    AK.reseed(seed);
    return canvasTex(512, 256, (g, w, h) => {
      const img = g.createImageData(w, h);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const n = AK.fbm2(x / 90, y / 40, 4) * 0.5 + AK.fbm2(x / 13, y / 160, 2) * 0.25;
        const v = Math.max(0, Math.min(255, base + n * amt));
        const i = (y * w + x) * 4;
        img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255;
      }
      g.putImageData(img, 0, 0);
    });
  };
  // sealed concrete slab: trowel swirl in roughness, saw-cut joints in colour
  SH.slabMaps = function (seed) {
    AK.reseed(seed);
    const rough = canvasTex(1024, 1024, (g, w, h) => {
      const img = g.createImageData(w, h);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const a = AK.warp2 ? AK.fbm2(x / 70 + AK.fbm2(x / 160, y / 160, 2) * 2.2, y / 70, 4) : AK.fbm2(x / 70, y / 70, 4);
        const sw = Math.sin((x * 0.6 + y * 0.8) / 9 + a * 6) * 0.5 + 0.5;
        const v = 70 + a * 60 + sw * 26;
        const i = (y * w + x) * 4;
        img.data[i] = img.data[i + 1] = img.data[i + 2] = Math.max(20, Math.min(235, v)); img.data[i + 3] = 255;
      }
      g.putImageData(img, 0, 0);
    });
    const color = canvasTex(1024, 1024, (g, w, h) => {
      const img = g.createImageData(w, h);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const n = AK.fbm2(x / 220, y / 220, 4) * 0.6 + AK.fbm2(x / 30, y / 30, 3) * 0.25;
        const v = 139 + n * 22;
        const i = (y * w + x) * 4;
        img.data[i] = v; img.data[i + 1] = v * 0.965; img.data[i + 2] = v * 0.9; img.data[i + 3] = 255;
      }
      g.putImageData(img, 0, 0);
      // saw-cut joints every 25 ft (texture spans 50 ft): two lines each way
      g.strokeStyle = 'rgba(40,36,32,0.55)'; g.lineWidth = 2.2;
      for (const p of [0, 512]) { g.beginPath(); g.moveTo(p + 1, 0); g.lineTo(p + 1, h); g.stroke();
        g.beginPath(); g.moveTo(0, p + 1); g.lineTo(w, p + 1); g.stroke(); }
    }, { srgb: true });
    return { rough, color };
  };
  // cabinet door: perforation dots as a bump map
  SH.perfTex = function () {
    return canvasTex(256, 256, (g, w, h) => {
      g.fillStyle = '#ffffff'; g.fillRect(0, 0, w, h);
      g.fillStyle = '#000000';
      for (let y = 4; y < h; y += 8) for (let x = (y / 8 % 2) * 4 + 4; x < w; x += 8) {
        g.beginPath(); g.arc(x, y, 2.1, 0, Math.PI * 2); g.fill();
      }
    });
  };

  /* ---- instancing helper --------------------------------------------- */
  function boxes(R, list, mat, o) {
    o = o || {};
    if (!list.length) return null;
    const geo = new THREE.BoxGeometry(1, 1, 1);
    const im = new THREE.InstancedMesh(geo, mat, list.length);
    const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
    list.forEach((b, i) => {
      p.set(b[0], b[1], b[2]); s.set(b[3], b[4], b[5]);
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), b[6] || 0);
      m.compose(p, q, s); im.setMatrixAt(i, m);
    });
    im.castShadow = o.cast !== false; im.receiveShadow = o.receive !== false;
    R.scene.add(im);
    return im;
  }
  SH.boxes = boxes;

  /* ---- materials ------------------------------------------------------- */
  SH.mats = function () {
    const M = {};
    M.upright = new THREE.MeshStandardMaterial({ color: 0x2c4f86, metalness: 0.45, roughness: 0.42 });
    M.beam = new THREE.MeshStandardMaterial({ color: 0xd8642a, metalness: 0.3, roughness: 0.38 });
    M.pine = new THREE.MeshStandardMaterial({ color: 0xc9a26a, roughness: 0.86 });
    M.carton = new THREE.MeshPhysicalMaterial({ color: 0xa98457, roughness: 0.82, clearcoat: 0.55, clearcoatRoughness: 0.32 });
    M.cartonB = new THREE.MeshPhysicalMaterial({ color: 0x9c7a50, roughness: 0.84, clearcoat: 0.45, clearcoatRoughness: 0.38 });
    M.cabinet = new THREE.MeshStandardMaterial({ color: 0x15181d, metalness: 0.62, roughness: 0.36 });
    M.ledG = new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x3ce6b4, emissiveIntensity: 2.6 });
    M.ledB = new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x5ac8f0, emissiveIntensity: 2.6 });
    M.gold = new THREE.MeshStandardMaterial({ color: 0xffc72c, roughness: 0.5, metalness: 0.0, emissive: 0xffc72c, emissiveIntensity: SH.goldGlow || 0 });
    M.aisle = new THREE.MeshStandardMaterial({ color: 0xd9d4c8, roughness: 0.6 });
    return M;
  };

  /* ---- the interior ---------------------------------------------------- */
  // Returns {mats, hybrid:{x,y,z}} so a slide can aim at the hybrid cabinet.
  SH.interior = function (R, o) {
    o = o || {};
    const M = SH.mats();
    const rnd = AK.rng(o.seed || 108106);
    const slab = SH.slabMaps((o.seed || 108106) + 1);
    slab.color.repeat.set(SH.W / 50, SH.D / 50); slab.rough.repeat.set(SH.W / 50, SH.D / 50);
    const floorM = new THREE.MeshPhysicalMaterial({ map: slab.color, roughnessMap: slab.rough,
      roughness: 0.62, clearcoat: 0.28, clearcoatRoughness: 0.22, color: 0xffffff });
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(SH.W, SH.D), floorM);
    floor.rotation.x = -Math.PI / 2; floor.position.set(SH.W / 2, 0, SH.D / 2); floor.receiveShadow = true;
    R.scene.add(floor);
    // gold stripe across the slab at x = 200, 12 in wide
    const st = new THREE.Mesh(new THREE.PlaneGeometry(1.0, SH.D - 2), M.gold);
    st.rotation.x = -Math.PI / 2; st.position.set(SH.STRIPE_X, 0.02, SH.D / 2); st.receiveShadow = true;
    R.scene.add(st); SH.stripeMesh = st;
    // aisle edge lines (pale, 4 in)
    for (const za of SH.AISLES) for (const dz of [-5.6, 5.6]) {
      const l = new THREE.Mesh(new THREE.PlaneGeometry(SH.W - 12, 0.33), M.aisle);
      l.rotation.x = -Math.PI / 2; l.position.set(SH.W / 2 + 2, 0.015, za + dz); l.receiveShadow = true; R.scene.add(l);
    }
    // walls: liner panels with ribs, interior side
    const ribN = SH.ribNormal(10); ribN.repeat.set(SH.W / 30, 1);
    const wallM = new THREE.MeshStandardMaterial({ color: 0x5c636b, roughness: 0.55, metalness: 0.5,
      normalMap: ribN, normalScale: new THREE.Vector2(1.2, 1.2) });
    const wallMs = wallM.clone(); wallMs.normalMap = ribN.clone(); wallMs.normalMap.repeat.set(SH.D / 30, 1); wallMs.normalMap.needsUpdate = true;
    const wN = new THREE.Mesh(new THREE.PlaneGeometry(SH.W, SH.EAVE), wallM); wN.position.set(SH.W / 2, SH.EAVE / 2, 0); R.scene.add(wN);
    const wS = new THREE.Mesh(new THREE.PlaneGeometry(SH.W, SH.EAVE), wallM); wS.rotation.y = Math.PI; wS.position.set(SH.W / 2, SH.EAVE / 2, SH.D); R.scene.add(wS);
    const wW = new THREE.Mesh(new THREE.PlaneGeometry(SH.D, SH.EAVE), wallMs); wW.rotation.y = Math.PI / 2; wW.position.set(0, SH.EAVE / 2, SH.D / 2); R.scene.add(wW);
    // east wall in pieces around the dock opening
    { const D0 = SH.DOOR, zA = D0.z - D0.w / 2, zB = D0.z + D0.w / 2;
      for (const pc of [[zA, SH.EAVE, zA / 2, SH.EAVE / 2], [SH.D - zB, SH.EAVE, (zB + SH.D) / 2, SH.EAVE / 2], [D0.w, SH.EAVE - D0.h, D0.z, D0.h + (SH.EAVE - D0.h) / 2]]) {
        const m = new THREE.Mesh(new THREE.PlaneGeometry(pc[0], pc[1]), wallMs); m.rotation.y = -Math.PI / 2; m.position.set(SH.W, pc[3], pc[2]); R.scene.add(m);
      } }
    // roof deck: dark, with joists every 6 ft across x and girders every 50 ft
    const deck = new THREE.Mesh(new THREE.PlaneGeometry(SH.W, SH.D), new THREE.MeshStandardMaterial({ color: 0x1a1d22, roughness: 0.8, metalness: 0.3 }));
    deck.rotation.x = Math.PI / 2; deck.position.set(SH.W / 2, SH.EAVE + 1.5, SH.D / 2); R.scene.add(deck);
    const joists = [], girders = [];
    for (let x = 3; x < SH.W; x += 6) joists.push([x, SH.EAVE + 0.8, SH.D / 2, 0.25, 1.4, SH.D]);
    for (let z = 0; z <= SH.D; z += 32) girders.push([SH.W / 2, SH.EAVE - 0.4, z + 30, SH.W, 2.6, 0.6]);
    boxes(R, joists, new THREE.MeshStandardMaterial({ color: 0x2a2e35, roughness: 0.6, metalness: 0.5 }), { cast: false });
    boxes(R, girders, new THREE.MeshStandardMaterial({ color: 0x30353d, roughness: 0.55, metalness: 0.5 }), { cast: false });

    // racks
    const ups = [], beams = [], pallets = [], cartons = [], cartonsB = [], cabs = [], ledG = [], ledB = [];
    const BAYL = 9, LEVELS = [0, 5.5, 11], RD = 4, UPH = 16;
    let hybrid = null;
    for (const za of SH.AISLES) {
      if (o.skipAisles && o.skipAisles.indexOf(za) >= 0) continue;
      for (const side of [-1, 1]) {
        const zc = za + side * (6 + RD / 2);           // row centre
        // rack bays x0 = 110 .. 191, their ends facing the stripe at x = 200.
        // Mixed bays: cabinets more likely the further west. The hybrid sits
        // in the end bay (191), beam level 1, the slot nearest the stripe.
        for (let x0 = 106; x0 + BAYL <= 196; x0 += BAYL) {
          const pCab = 0.06 + 0.7 * (187 - x0) / 81;
          for (const dz of [-RD / 2, RD / 2]) ups.push([x0, UPH / 2, zc + dz, 0.28, UPH, 0.28]);
          for (let li = 1; li < LEVELS.length; li++) for (const dz of [-RD / 2 + 0.1, RD / 2 - 0.1])
            beams.push([x0 + BAYL / 2, LEVELS[li], zc + dz, BAYL, 0.42, 0.18]);
          for (let li = 0; li < LEVELS.length; li++) {
            const y = LEVELS[li] + (li ? 0.21 : 0);
            for (const px of [x0 + 2.3, x0 + 6.7]) {
              const isHybrid = (x0 === 187 && li === 1 && px > x0 + 4 && side === (o.hybridSide || 1) && za === (o.hybridAisle || 110));
              if (isHybrid) { hybrid = { x: px, y: y, z: zc, face: px + 1.8 }; continue; }   // the slide builds it
              const isCab = !(x0 === 187 && li === 1) && rnd() < pCab;
              if (isCab) {
                cabs.push([px, y + 2.5, zc, 3.6, 5.0, 3.4]);
                for (const face of [zc - 1.72, zc + 1.72]) for (let k = 0; k < 4; k++)
                  (rnd() < 0.72 ? ledG : ledB).push([px - 1.4 + rnd() * 2.8, y + 0.6 + rnd() * 4.0, face, 0.14, 0.09, 0.05]);
                // and on the end face toward the stripe
                for (let k = 0; k < 4; k++) (rnd() < 0.72 ? ledG : ledB).push([px + 1.82, y + 0.6 + rnd() * 4.0, zc - 1.3 + rnd() * 2.6, 0.05, 0.09, 0.14]);
                continue;
              }
              if (rnd() < 0.08 && li > 0) continue;       // a few empty slots
              pallets.push([px, y + 0.25, zc, 3.4, 0.5, 3.8]);
              const hh = 2.4 + rnd() * 1.5;
              (rnd() < 0.5 ? cartons : cartonsB).push([px, y + 0.5 + hh / 2, zc, 3.3, hh, 3.7]);
            }
          }
        }
        for (const dz of [-RD / 2, RD / 2]) ups.push([196, UPH / 2, zc + dz, 0.28, UPH, 0.28]);
        // server cabinet rows x 6..106, contiguous 2 ft cabinets, 7.5 ft tall
        for (let x = 6; x < 106; x += 2.05) {
          cabs.push([x + 1, 3.75, zc, 2.0, 7.5, 3.6]);
          const face = zc - side * 1.82;
          const n = 2 + Math.floor(rnd() * 3);
          for (let k = 0; k < n; k++) (rnd() < 0.7 ? ledG : ledB).push([x + 0.3 + rnd() * 1.4, 0.8 + rnd() * 6, face, 0.12, 0.08, 0.05]);
        }
      }
    }
    // the staging floor east of the stripe: loaded pallets set down on the slab
    for (let k = 0; k < 26; k++) {
      const px = 206 + rnd() * 36, pz = 12 + rnd() * 176;
      if (Math.abs(pz - SH.DOOR.z) < 14 && px > 228) continue;   // keep the dock lane clear
      if (o.clear && o.clear(px, pz)) continue;
      const rot = (rnd() - 0.5) * 0.3, hh = 2.6 + rnd() * 1.8;
      pallets.push([px, 0.25, pz, 3.4, 0.5, 3.8, rot]);
      (rnd() < 0.5 ? cartons : cartonsB).push([px, 0.5 + hh / 2, pz, 3.3, hh, 3.7, rot]);
    }
    boxes(R, ups, M.upright); boxes(R, beams, M.beam); boxes(R, pallets, M.pine);
    boxes(R, cartons, M.carton); boxes(R, cartonsB, M.cartonB);
    const cabMesh = boxes(R, cabs, M.cabinet);
    boxes(R, ledG, M.ledG, { cast: false }); boxes(R, ledB, M.ledB, { cast: false });
    return { M, hybrid, cabMesh, floor };
  };

  /* pendant high-bays: emissive discs everywhere, real lights only near
     the camera (SwiftShader pays per light per fragment) */
  SH.pendants = function (R, o) {
    o = o || {};
    const near = o.near || [206, 110], maxLights = o.maxLights || 8;
    const discM = new THREE.MeshStandardMaterial({ color: 0x111111, emissive: 0xeef3fa, emissiveIntensity: o.disc || 2.2 });
    const hoodM = new THREE.MeshStandardMaterial({ color: 0x3a3f46, metalness: 0.7, roughness: 0.4 });
    const spots = [];
    const xmax = o.xmax != null ? o.xmax : SH.W;
    for (const za of SH.AISLES) for (let x = 12; x < xmax; x += 25) if (!(o.skip && o.skip(x, za))) spots.push([x, za]);
    spots.sort((a, b) => Math.hypot(a[0] - near[0], a[1] - near[1]) - Math.hypot(b[0] - near[0], b[1] - near[1]));
    spots.forEach((s, i) => {
      const hood = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.4, 1.2, 24, 1, true), hoodM);
      hood.position.set(s[0], 28.6, s[1]); R.scene.add(hood);
      const disc = new THREE.Mesh(new THREE.CircleGeometry(1.25, 24), discM);
      disc.rotation.x = Math.PI / 2; disc.position.set(s[0], 28.0, s[1]); R.scene.add(disc);
      if (i < maxLights) {
        const L = new THREE.PointLight(0xeef3fa, o.intensity || 900, 80, 1.6);
        L.position.set(s[0], 27.4, s[1]); R.scene.add(L);
      }
    });
    return spots;
  };

  /* the dock door in the east wall: steel jambs, a slatted roll-up panel
     raised `open` ft, rubber bumpers. side 'in' faces west into the hall,
     'out' faces east onto the lot. Returns the panel for a slide's own light. */
  SH.dock = function (R, o) {
    o = o || {};
    const D = SH.DOOR, open = o.open || 0, g = new THREE.Group();
    const steel = new THREE.MeshStandardMaterial({ color: 0x8d96a0, metalness: 0.7, roughness: 0.34 });
    const ribN = SH.ribNormal(1); ribN.rotation = Math.PI / 2; ribN.repeat.set(1, 18);
    const panelM = new THREE.MeshStandardMaterial({ color: 0xb9c0c8, metalness: 0.5, roughness: 0.4, normalMap: ribN });
    const ph = D.h - open;
    const panel = new THREE.Mesh(new THREE.BoxGeometry(0.25, ph, D.w), panelM);
    panel.position.set(D.x + (o.side === 'out' ? 0.3 : -0.3), open + ph / 2, D.z); g.add(panel);
    for (const dz of [-D.w / 2 - 0.35, D.w / 2 + 0.35]) {
      const j = new THREE.Mesh(new THREE.BoxGeometry(0.6, D.h + 0.6, 0.5), steel); j.position.set(D.x, (D.h + 0.6) / 2, D.z + dz); g.add(j);
    }
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.4, D.w + 1.4), steel); head.position.set(D.x, D.h + 0.9, D.z); g.add(head);
    const rub = new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: 0.9 });
    for (const dz of [-D.w / 2 + 1, D.w / 2 - 1]) {
      const b = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.6, 1.0), rub);
      b.position.set(D.x + (o.side === 'out' ? 0.6 : -0.6), 0.9, D.z + dz); g.add(b);
    }
    g.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
    R.scene.add(g);
    return { group: g, panel, open };
  };

  /* ---- the exterior ---------------------------------------------------- */
  // Ribbed steel walls with the dock opening cut in the east wall, a 1:12 gable
  // roof with its ridge along x, a snow lot with plow ridges and tire ruts
  // (displaced, seeded), and sodium poles. Returns {poles, lot}.
  SH.exterior = function (R, o) {
    o = o || {};
    const rnd = AK.rng(o.seed || 108101);
    const D = SH.DOOR;
    const ribN = SH.ribNormal(8);
    const grime = SH.grime((o.seed || 108101) + 3, 150, 70);
    const wallMat = (len) => {
      const n = ribN.clone(); n.needsUpdate = true; n.repeat.set(len / 11, 1);   // 8 ribs per 11 ft, a 1.4 ft pitch that holds at long range without beating
      const r = grime.clone(); r.needsUpdate = true; r.repeat.set(len / 120, 1);
      return new THREE.MeshStandardMaterial({ color: 0xa4acb5, metalness: 0.3, roughness: 0.52,
        normalMap: n, normalScale: new THREE.Vector2(1.0, 1.0), roughnessMap: r });
    };
    const wall = (w, h, pos, rotY) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), wallMat(w));
      m.position.set(pos[0], pos[1], pos[2]); m.rotation.y = rotY; m.castShadow = true; m.receiveShadow = true;
      R.scene.add(m); return m;
    };
    wall(SH.W, SH.EAVE, [SH.W / 2, SH.EAVE / 2, SH.D], 0);                 // south, faces +z
    wall(SH.W, SH.EAVE, [SH.W / 2, SH.EAVE / 2, 0], Math.PI);              // north
    wall(SH.D, SH.EAVE, [0, SH.EAVE / 2, SH.D / 2], -Math.PI / 2);         // west
    // east wall in pieces around the door opening
    const zA = D.z - D.w / 2, zB = D.z + D.w / 2;
    wall(zA, SH.EAVE, [SH.W, SH.EAVE / 2, zA / 2], Math.PI / 2);
    wall(SH.D - zB, SH.EAVE, [SH.W, SH.EAVE / 2, (zB + SH.D) / 2], Math.PI / 2);
    wall(D.w, SH.EAVE - D.h, [SH.W, D.h + (SH.EAVE - D.h) / 2, D.z], Math.PI / 2);
    // gable roof, ridge along x at z = 100, 1:12
    const rise = (SH.D / 2) / 12, roofM = new THREE.MeshStandardMaterial({ color: 0x5f666e, metalness: 0.5, roughness: 0.55 });
    const slope = Math.hypot(SH.D / 2, rise);
    for (const s of [-1, 1]) {
      const r = new THREE.Mesh(new THREE.PlaneGeometry(SH.W + 2, slope + 1.5), roofM);
      r.rotation.x = -Math.PI / 2 + s * Math.atan2(rise, SH.D / 2) * -1;
      r.position.set(SH.W / 2, SH.EAVE + rise / 2, SH.D / 2 + s * SH.D / 4);
      r.castShadow = true; R.scene.add(r);
    }
    // gable end triangles
    const tri = new THREE.Shape([new THREE.Vector2(0, 0), new THREE.Vector2(SH.D, 0), new THREE.Vector2(SH.D / 2, rise)]);
    for (const x of [0, SH.W]) {
      const t = new THREE.Mesh(new THREE.ShapeGeometry(tri), wallMat(SH.D));
      t.rotation.y = x ? -Math.PI / 2 : -Math.PI / 2; t.position.set(x, SH.EAVE, x ? 0 : 0);
      if (x) { t.rotation.y = -Math.PI / 2; t.position.set(x, SH.EAVE, 0); t.scale.z = 1; }
      t.material.side = THREE.DoubleSide; R.scene.add(t);
    }
    // eave and corner trim
    const trimM = new THREE.MeshStandardMaterial({ color: 0x2b3036, metalness: 0.6, roughness: 0.4 });
    for (const b of [[SH.W / 2, SH.EAVE + 0.3, SH.D + 0.3, SH.W + 1, 0.8, 0.7], [SH.W / 2, SH.EAVE + 0.3, -0.3, SH.W + 1, 0.8, 0.7],
                     [SH.W + 0.3, SH.EAVE / 2, SH.D + 0.3, 0.7, SH.EAVE, 0.7], [SH.W + 0.3, SH.EAVE / 2, -0.3, 0.7, SH.EAVE, 0.7]]) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(b[3], b[4], b[5]), trimM); m.position.set(b[0], b[1], b[2]); m.castShadow = true; R.scene.add(m);
    }
    // the lot: a coarse displaced snow plane, plus a fine near-field patch where
    // the tire ruts and plow ridges are resolved (0.5 ft cells)
    const tracks = o.tracks || [];
    // inside the near patch the coarse lot is sunk out of sight, and the ruts
    // fade to nothing at the patch edge, so the two meshes never interpenetrate
    // (round 1: the coarse triangles poked through the rut troughs and drew a
    // saw-tooth line along every rut on 01 and 09)
    const nr = o.near, EDGE = 6;
    const inner = (x, z) => {
      if (!nr) return 0;
      const d = Math.min(x - nr[0], nr[1] - x, z - nr[2], nr[3] - z);
      if (d <= 0) return 0; const t = Math.min(1, d / EDGE); return t * t * (3 - 2 * t);
    };
    const heightAt = (x, z, fine) => {
      let h = AK.fbm2(x / 60, z / 60, 4) * 0.35 + AK.fbm2(x / 9, z / 9, 2) * 0.08;
      const wIn = inner(x, z);
      if (!fine && wIn > 0) h -= 0.9 * wIn;
      if (fine) h += AK.fbm2(x / 4.5, z / 4.5, 2) * 0.04;
      const dx = Math.max(-x, x - SH.W, 0), dz = Math.max(-z, z - SH.D, 0), dw = Math.hypot(dx, dz);
      if (dw > 0) h += 1.6 * Math.exp(-Math.pow((dw - 7) / 3.2, 2));
      if (fine) for (const t of tracks) {
        let best = 1e9;
        for (let k = 0; k < t.length - 1; k++) {
          const ax = t[k][0], az = t[k][1], bx = t[k + 1][0], bz = t[k + 1][1];
          const vx = bx - ax, vz = bz - az, L2 = vx * vx + vz * vz;
          const u = Math.max(0, Math.min(1, ((x - ax) * vx + (z - az) * vz) / L2));
          best = Math.min(best, Math.hypot(ax + u * vx - x, az + u * vz - z));
        }
        for (const off of [3, -3]) {
          const e = Math.abs(best - Math.abs(off));
          if (e < 1.2) h -= wIn * 0.3 * (0.5 + 0.5 * Math.cos(Math.PI * e / 1.2));          // the rut, smooth
          else if (e < 2.6) h += wIn * 0.09 * Math.sin((e - 1.2) / 1.4 * Math.PI);          // its thrown lip
        }
      }
      if (x > SH.W - 1 && x < SH.W + 30 && Math.abs(z - D.z) < 14) h *= 0.15;   // the swept apron
      return h;
    };
    const build = (x0, x1, z0, z1, nx, nz, lift, fine) => {
      const geo = new THREE.PlaneGeometry(x1 - x0, z1 - z0, nx, nz);
      geo.rotateX(-Math.PI / 2); geo.translate((x0 + x1) / 2, 0, (z0 + z1) / 2);
      const P = geo.attributes.position;
      for (let i = 0; i < P.count; i++) P.setY(i, heightAt(P.getX(i), P.getZ(i), fine) + lift);
      geo.computeVertexNormals();
      return geo;
    };
    const snowM = new THREE.MeshStandardMaterial({ color: 0xc8d0da, roughness: 0.78, metalness: 0 });
    const lot = new THREE.Mesh(build(-200, 1100, -200, 700, 420, 300, 0, false), snowM); lot.receiveShadow = true; R.scene.add(lot);
    if (o.near) {
      const n = o.near;    // [x0, x1, z0, z1]
      const near = new THREE.Mesh(build(n[0], n[1], n[2], n[3], Math.round((n[1] - n[0]) * 4), Math.round((n[3] - n[2]) * 4), 0.03, true), snowM);   // 0.25 ft cells: a rut wall gets five vertices, not two
      near.receiveShadow = true; near.castShadow = false; R.scene.add(near);
    }
    // poles
    const poles = [];
    for (const p of (o.poles || [])) {
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.45, p[2], 12), new THREE.MeshStandardMaterial({ color: 0x3a3e44, metalness: 0.6, roughness: 0.5 }));
      pole.position.set(p[0], p[2] / 2, p[1]); pole.castShadow = true; R.scene.add(pole);
      const head = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.7, 1.4), new THREE.MeshStandardMaterial({ color: 0x24272c, metalness: 0.5, roughness: 0.5 }));
      head.position.set(p[0] - 1.2, p[2] + 0.2, p[1]); R.scene.add(head);
      const lens = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 1.0), new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0xffb45a, emissiveIntensity: 6 }));
      lens.rotation.x = Math.PI / 2; lens.position.set(p[0] - 1.2, p[2] - 0.16, p[1]); R.scene.add(lens);
      poles.push({ x: p[0] - 1.2, y: p[2] - 0.3, z: p[1] });
    }
    return { poles, lot, snowM };
  };

  return SH;
}
