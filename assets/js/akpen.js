/* akpen.js — one fountain pen, rendered (No.68, 2026-09-25). ES module.
 *
 * The deck's single physical object: black resin barrel, gold band and clip,
 * a gold nib, lying on or hovering over a flat map. Rendered with three.js
 * (rung 1 of the rendered ladder) into a TRANSPARENT canvas with its own cast
 * shadow on a shadow catcher, so the slide composites it over Canvas-2D art.
 * The key light is the deck's key (azimuth clockwise from up, elevation), the
 * same one akscribe lights the relief with, so the pen's shadow and the lit
 * flanks agree.
 *
 * WORLD UNITS ARE DESIGN PX. The ground plane z = 0 is the slide, x right,
 * y DOWN in design px, so a pose is written in the slide's own coordinates and
 * the nib tip lands exactly where the slide says (AKPEN.render returns the
 * projected tip for __akLeaders / data-contacts).
 *
 *   const AKPEN = (await import('@@ASSETS@@/js/akpen.js')).init(THREE);
 *   const shot = await AKPEN.render(canvas, {
 *     W:1080, H:1350, tip:[600,700], angle:-35, lift:0, capped:false,
 *     keyAz:330, keyEl:46, length:620 });
 *   // shot = {ok, tip:[x,y], tail:[x,y], canvas}
 */
export function init(THREE) {
  const AKPEN = {};

  function lightDir(az, el) {
    const a = az * Math.PI / 180, e = el * Math.PI / 180;
    // screen: +x right, +y down (world +y down), +z toward viewer (up off map)
    return new THREE.Vector3(Math.cos(e) * Math.sin(a), -Math.cos(e) * Math.cos(a), Math.sin(e));
  }

  // Barrel profile along its own axis (x = radius, y = position from nib end).
  function barrelProfile(L, R) {
    const p = [];
    p.push([0.001, 0]);
    p.push([R * 0.62, L * 0.004]);
    p.push([R * 0.70, L * 0.02]);          // section taper toward the nib
    p.push([R * 0.78, L * 0.10]);
    p.push([R * 0.84, L * 0.20]);
    p.push([R * 0.96, L * 0.235]);          // thread step
    p.push([R * 1.00, L * 0.26]);
    p.push([R * 1.00, L * 0.90]);
    p.push([R * 0.92, L * 0.97]);
    p.push([R * 0.55, L * 0.995]);
    p.push([0.001, L]);
    return p;
  }

  AKPEN.render = async function (canvas, o) {
    const W = o.W || 1080, H = o.H || 1350;
    // VIEW: render only the pen's own box, so the canvas is not a mostly empty
    // full-frame layer (qa reads a near-uniform full-frame canvas as dead GL).
    // The slide positions the canvas at view[0], view[1] with view[2] x view[3] CSS px.
    const V = o.view || [0, 0, W, H];
    if (o.view) {
      canvas.style.left = V[0] + "px"; canvas.style.top = V[1] + "px";
      canvas.style.width = V[2] + "px"; canvas.style.height = V[3] + "px";
      canvas.width = V[2] * 2; canvas.height = V[3] * 2;
    }
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true,
      preserveDrawingBuffer: true, premultipliedAlpha: false });
    renderer.setPixelRatio(2);                  // BEFORE size (akthree rule)
    renderer.setSize(V[2], V[3], false);
    renderer.setClearColor(0x000000, 0);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = o.exposure || 1.0;

    const scene = new THREE.Scene();
    // Orthographic camera looking straight down the -z axis: world px = screen px.
    const cam = new THREE.OrthographicCamera(V[0], V[0] + V[2], -V[1], -(V[1] + V[3]), -4000, 4000);
    cam.position.set(0, 0, 2000); cam.up.set(0, 1, 0); cam.lookAt(0, 0, 0);
    // world y is DOWN in design px, three's y is up: flip with a root group
    const root = new THREE.Group(); root.scale.set(1, -1, 1); scene.add(root);

    // IBL: a soft studio so the resin and gold have something to reflect
    const pm = new THREE.PMREMGenerator(renderer);
    const env = new THREE.Scene();
    const panel = (c, i, pos, s) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(s[0], s[1]),
        new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(i), side: THREE.DoubleSide }));
      m.position.set(...pos); m.lookAt(0, 0, 0); env.add(m);
    };
    env.background = new THREE.Color(0x05080d);
    panel(0xdfeefa, 5.0, [-4, 6, 5], [9, 4]);     // softbox, upper left
    panel(0xcfe4f4, 2.2, [5, -3, 4], [2, 9]);      // strip light for the resin rim
    panel(0x9fc6e0, 1.2, [0, -6, 2], [10, 2]);     // table glow from below
    panel(0xffd9a0, 0.8, [6, 2, -3], [3, 3]);
    scene.environment = pm.fromScene(env, 0.04).texture;
    scene.environmentIntensity = o.envI || 0.9;

    const L = lightDir(o.keyAz == null ? 330 : o.keyAz, o.keyEl == null ? 46 : o.keyEl);
    const key = new THREE.DirectionalLight(0xfff1dc, o.keyI || 2.6);
    // light position in root space (y down): convert
    const tipX = o.tip[0], tipY = o.tip[1];
    key.position.set(tipX + L.x * 1500, -(tipY + L.y * 1500), L.z * 1500);
    key.target.position.set(tipX, -tipY, 0);
    key.castShadow = true;
    key.shadow.mapSize.set(4096, 4096);
    const sz = (o.length || 620) * 1.1;
    Object.assign(key.shadow.camera, { left: -sz, right: sz, top: sz, bottom: -sz, near: 1, far: 4000 });
    key.shadow.bias = -0.0006; key.shadow.radius = o.shadowSoft || 6;
    scene.add(key); scene.add(key.target);
    scene.add(new THREE.HemisphereLight(0x9fc6e0, 0x05080d, 0.35));

    // shadow catcher over the whole slide
    const catcher = new THREE.Mesh(new THREE.PlaneGeometry(W * 3, H * 3),
      new THREE.ShadowMaterial({ color: new THREE.Color(o.shadowColor || 0x02050a), opacity: o.shadowOpacity || 0.62 }));
    catcher.position.set(W / 2, -H / 2, 0); catcher.receiveShadow = true; scene.add(catcher);

    // --- the pen, built nib at local origin pointing along +X (in root space)
    const len = o.length || 620, R = len * 0.052;
    const resin = new THREE.MeshPhysicalMaterial({ color: 0x0a0c10, roughness: 0.22, metalness: 0.0,
      clearcoat: 1.0, clearcoatRoughness: 0.06 });
    const gold = new THREE.MeshStandardMaterial({ color: 0xffc72c, metalness: 0.95, roughness: 0.22 });
    const pen = new THREE.Group();
    const barrel = new THREE.Mesh(new THREE.LatheGeometry(
      barrelProfile(len, R).map(p => new THREE.Vector2(p[0], p[1])), 96), resin);
    barrel.rotation.z = -Math.PI / 2;         // lathe axis +y -> pen axis +x (nib end at 0)
    pen.add(barrel);
    // gold band where the cap would close
    const band = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.015, R * 1.015, len * 0.035, 96, 1, true), gold);
    band.rotation.z = Math.PI / 2; band.position.x = len * 0.27; pen.add(band);
    // nib: a tapered gold leaf with a slit, lying on the section's axis
    const nibShape = new THREE.Shape();
    const nL = len * 0.13, nW = R * 0.82;
    nibShape.moveTo(0, 0);
    nibShape.quadraticCurveTo(nL * 0.45, nW * 0.62, nL, nW * 0.62);
    nibShape.lineTo(nL, -nW * 0.62);
    nibShape.quadraticCurveTo(nL * 0.45, -nW * 0.62, 0, 0);
    const nibGeo = new THREE.ExtrudeGeometry(nibShape, { depth: R * 0.1, bevelEnabled: true,
      bevelThickness: R * 0.05, bevelSize: R * 0.04, bevelSegments: 2 });
    const nib = new THREE.Mesh(nibGeo, gold);
    nib.position.set(-nL * 0.72, 0, R * 0.12); pen.add(nib);
    // breather hole
    const hole = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.09, R * 0.09, R * 0.4, 24), resin);
    hole.rotation.x = Math.PI / 2; hole.position.set(nL * 0.1, 0, R * 0.2); pen.add(hole);
    let tipLocalX = -nL * 0.72;
    if (o.capped) {
      // cap covers the nib and section; gold clip along the top
      const capL = len * 0.34;
      const cap = new THREE.Mesh(new THREE.CylinderGeometry(R * 1.08, R * 1.08, capL, 96), resin);
      cap.rotation.z = Math.PI / 2; cap.position.x = capL / 2 - len * 0.07; pen.add(cap);
      const capEnd = new THREE.Mesh(new THREE.SphereGeometry(R * 1.08, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), resin);
      capEnd.rotation.z = Math.PI / 2; capEnd.position.x = -len * 0.07; capEnd.scale.set(1, 0.35, 1); pen.add(capEnd);
      const clip = new THREE.Mesh(new THREE.BoxGeometry(capL * 0.8, R * 0.34, R * 0.16), gold);
      clip.position.set(capL * 0.52 - len * 0.07, 0, R * 1.12); pen.add(clip);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(R * 1.08, R * 0.08, 16, 96), gold);
      ring.rotation.y = Math.PI / 2; ring.position.x = capL - len * 0.07; pen.add(ring);
      tipLocalX = -len * 0.07 - R * 0.35;
    }
    pen.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });

    // pose: tip at (tipX, tipY) on the map, barrel toward `angle` (deg, screen,
    // 0 = pointing right, clockwise positive because y is down), lifted so the
    // barrel rests on the map (lift 0) or hovers (lift in px).
    const holder = new THREE.Group();
    pen.position.x = -tipLocalX;                 // tip at holder origin
    holder.add(pen);
    const ang = (o.angle || 0) * Math.PI / 180;
    holder.rotation.z = ang;
    const rest = Math.asin(Math.min(0.2, (R * 1.0) / len * 2));  // tail up on its own radius
    holder.rotation.y = -(o.tilt == null ? rest : o.tilt * Math.PI / 180);
    holder.position.set(tipX, tipY, (o.lift || 0) + (o.capped ? R * 1.08 : R * 0.35));
    root.add(holder);

    renderer.render(scene, cam);
    await new Promise(r => requestAnimationFrame(r));
    // projected points in design px (orthographic, so identical to world x,y)
    const tailW = new THREE.Vector3(); pen.localToWorld(tailW.set(len, 0, 0));
    return { ok: true, tip: [tipX, tipY], tail: [tailW.x, -tailW.y], radius: R, canvas };
  };
  return AKPEN;
}
