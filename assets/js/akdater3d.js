/* akdater3d.js — the band dater as a PBR model (Carousel No.125, 2026-11-26).
 *
 * ES module. buildDater(THREE, AKT, o) returns a THREE.Group, standing on y = 0,
 * about 1.95 units tall, its print face toward the felt and its bands' index
 * face toward +z. Ten rubber bands on knurled wheels between two nickel side
 * plates, a nickel bridge and collar, a turned walnut knob.
 *
 *   o.date     the ten characters the bands show at the front ("2028-06-30");
 *              "" or null leaves the bands rolled between characters (blurred
 *              frames roll them by o.roll)
 *   o.roll     0..1 extra band rotation per wheel, seeded (for the blur frame)
 *   o.blur     px of motion blur on the band glyphs (a band caught turning)
 *   o.plate    material overrides for the side plates, e.g. {metalness, envMapIntensity, color}
 *   o.seed     wear seed
 *
 * Also: feltMaterial(THREE, o) and sheetTexture(THREE, o) (bond paper tooth with
 * an optional impression). Composition, cameras, lights and windows stay in the
 * slides.
 */
const MONO = "500 72px 'JetBrains Mono', monospace";

function mulberry(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6D2B79F5) >>> 0; let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* One band's rubber texture: the band alphabet around the wheel, the shown
 * character centred at u = 0.5 (theta 0, facing +z). Canvas x = u (around),
 * canvas y = along the axle; glyphs are turned so they read upright at the front. */
function bandTexture(THREE, ch, alphabet, seed, roll, blur) {
  const W = 1024, H = 128, c = document.createElement("canvas");
  c.width = W; c.height = H;
  const g = c.getContext("2d");
  const rnd = mulberry(seed);
  // rubber: near-black with a fine tooth and ink worked into it
  g.fillStyle = "#231d1a"; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 2600; i++) {
    const x = rnd() * W, y = rnd() * H, v = 22 + rnd() * 26;
    g.fillStyle = "rgba(" + (v + 10) + "," + v + "," + (v - 4) + "," + (0.25 + rnd() * 0.3) + ")";
    g.fillRect(x, y, 1.6, 1.6);
  }
  const bump = document.createElement("canvas"); bump.width = W; bump.height = H;
  const b = bump.getContext("2d");
  b.fillStyle = "#3a3a3a"; b.fillRect(0, 0, W, H);
  const n = alphabet.length;
  let k0 = ch ? alphabet.indexOf(ch) : 0; if (k0 < 0) k0 = 0;
  const step = W / n;                      // one character per slot around the band
  const shift = (roll || 0) * W;
  for (let j = 0; j < n; j++) {
    const k = (k0 + j) % n;
    let x = W * 0.5 + j * step + shift;
    x = ((x % W) + W) % W;
    for (const ctx of [g, b]) {
      ctx.save();
      ctx.translate(x, H / 2);
      ctx.rotate(Math.PI / 2);
      ctx.font = MONO; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      if (ctx === g) {
        if (blur) ctx.filter = "blur(" + blur + "px)";   // a band caught turning
        // raised character: its top face picks up dried ink, its shoulder darker
        ctx.fillStyle = "#120e0d"; ctx.fillText(alphabet[k], 2, 2);
        ctx.fillStyle = "#8a7766"; ctx.fillText(alphabet[k], 0, 0);
      } else {
        ctx.fillStyle = "#f0f0f0"; ctx.fillText(alphabet[k], 0, 0);
      }
      ctx.restore();
    }
  }
  // the band's two edges are worn a little lighter
  g.fillStyle = "rgba(90,80,72,0.35)"; g.fillRect(0, 0, W, 6); g.fillRect(0, H - 6, W, 6);
  const map = new THREE.CanvasTexture(c); map.colorSpace = THREE.SRGBColorSpace;
  const bm = new THREE.CanvasTexture(bump);
  map.anisotropy = bm.anisotropy = 8;
  return { map, bump: bm };
}

function knurlTexture(THREE) {
  const c = document.createElement("canvas"); c.width = 256; c.height = 32;
  const g = c.getContext("2d");
  g.fillStyle = "#808080"; g.fillRect(0, 0, 256, 32);
  for (let x = 0; x < 256; x += 4) {
    g.fillStyle = "#d8d8d8"; g.fillRect(x, 0, 2, 32);
    g.fillStyle = "#3a3a3a"; g.fillRect(x + 2, 0, 1, 32);
  }
  const t = new THREE.CanvasTexture(c); t.wrapS = THREE.RepeatWrapping; t.repeat.set(6, 1);
  return t;
}

function grainWood(THREE, seed) {
  const W = 512, H = 512, c = document.createElement("canvas"); c.width = W; c.height = H;
  const g = c.getContext("2d"), rnd = mulberry(seed);
  const img = g.createImageData(W, H), d = img.data;
  const ph = []; for (let i = 0; i < 6; i++) ph.push(rnd() * 6.28);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const u = x / W, v = y / H;
    const w = Math.sin(v * 40 + Math.sin(u * 6.28 * 2 + ph[0]) * 2.2 + Math.sin(u * 6.28 * 5 + ph[1]) * 0.6);
    const fine = Math.sin(v * 260 + Math.sin(u * 30 + ph[2]) * 3) * 0.5 + 0.5;
    const t = 0.5 + 0.32 * w + 0.12 * fine;
    const r = 58 + 46 * t, gg = 34 + 28 * t, bb = 20 + 16 * t;
    const i = (y * W + x) * 4; d[i] = r; d[i + 1] = gg; d[i + 2] = bb; d[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

export function buildDater(THREE, AKT, o) {
  o = o || {};
  const date = (o.date || "").padEnd(10, " ").slice(0, 10);
  const seed = o.seed || 20261126;
  const rnd = mulberry(seed);
  const G = new THREE.Group();
  const nickel = new THREE.MeshStandardMaterial({ color: 0xd4dadd, metalness: 0.88, roughness: 0.30,
    envMapIntensity: 1.6 });
  const nickelWorn = new THREE.MeshStandardMaterial({ color: 0xc0c6c9, metalness: 0.82, roughness: 0.40,
    envMapIntensity: 1.5 });
  // nickel plate: a real metal, lit mostly by what it reflects, with a brushed lay so the
  // environment smears along the plate instead of printing as a flat painted face
  const brush = (() => { const c = document.createElement("canvas"); c.width = 512; c.height = 64;
    const g = c.getContext("2d"); const r = mulberry(seed + 3); g.fillStyle = "#808080"; g.fillRect(0, 0, 512, 64);
    for (let i = 0; i < 900; i++) { const y = r() * 64, v = 90 + r() * 80; g.fillStyle = "rgb(" + v + "," + v + "," + v + ")"; g.fillRect(0, y, 512, 0.6 + r()); }
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; })();
  const plateMat = new THREE.MeshStandardMaterial({ color: 0xc3cbcf, metalness: 0.72, roughness: 0.34,
    envMapIntensity: 2.4, bumpMap: brush, bumpScale: 0.35, roughnessMap: brush });
  if (o.plate) { for (const k of Object.keys(o.plate)) { if (k === "color") plateMat.color.set(o.plate.color); else plateMat[k] = o.plate[k]; } }
  const steelDark = new THREE.MeshStandardMaterial({ color: 0x6b7276, metalness: 0.9, roughness: 0.38,
    bumpMap: knurlTexture(THREE), bumpScale: 0.6, envMapIntensity: 1.0 });
  const walnut = new THREE.MeshStandardMaterial({ color: 0xffffff, map: grainWood(THREE, seed + 7),
    roughness: 0.42, metalness: 0.0 });

  const NB = 10, BW = 0.105, GAP = 0.014, R = 0.30, AX = 0.47;
  const span = NB * BW + (NB - 1) * GAP;          // 1.176
  const x0 = -span / 2 + BW / 2;
  // side plates: a tapered frame seen edge on, extruded along x
  const plate = [[-0.46, 0.0], [0.46, 0.0], [0.46, 0.10], [0.36, 0.20], [0.22, 1.10], [0.14, 1.18],
                 [-0.14, 1.18], [-0.22, 1.10], [-0.36, 0.20], [-0.46, 0.10]];
  for (const sx of [-1, 1]) {
    const m = AKT.extrude(plate.map(p => [p[0], p[1]]), 0.06, plateMat,
      { bevelThickness: 0.012, bevelSize: 0.012, bevelSegments: 4 });
    m.rotation.y = Math.PI / 2;                    // shape x -> world -z, extrude -> world x
    m.position.x = sx * (span / 2 + 0.03) - (sx > 0 ? 0 : 0.06);
    m.name = "side plate";
    G.add(m);
    // axle boss
    const boss = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.03, 48), nickel);
    boss.rotation.z = Math.PI / 2; boss.position.set(sx * (span / 2 + 0.095), AX, 0); G.add(boss);
  }
  // bridge across the top of the plates
  const bridge = new THREE.Mesh(new THREE.BoxGeometry(span + 0.2, 0.08, 0.30), nickel);
  bridge.position.set(0, 1.20, 0); G.add(bridge);
  // collar and neck (lathe), then the walnut knob
  const collar = AKT.lathe([[0.0, 1.24], [0.16, 1.24], [0.17, 1.27], [0.10, 1.31], [0.085, 1.42], [0.11, 1.45], [0.0, 1.45]], nickel, { segments: 96 });
  G.add(collar);
  const knobC = [[0.0, 1.44], [0.12, 1.44], [0.19, 1.50], [0.24, 1.60], [0.30, 1.72], [0.33, 1.82], [0.32, 1.89],
                 [0.27, 1.94], [0.16, 1.975], [0.0, 1.985]];
  // a smooth turned profile: the ten control points through a Catmull-Rom spline, 64 samples
  const kc = new THREE.CatmullRomCurve3(knobC.map(p => new THREE.Vector3(p[0], p[1], 0)), false, "centripetal");
  const knobP = kc.getPoints(64).map(v => [Math.max(0, v.x), v.y]);
  const knob = AKT.lathe(knobP, walnut, { segments: 160 }); knob.name = "walnut knob"; G.add(knob);
  // axle
  const axle = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, span + 0.16, 32), steelDark);
  axle.rotation.z = Math.PI / 2; axle.position.y = AX; G.add(axle);
  // ten bands on knurled wheels
  const alphabet = "0123456789-";
  G.userData.bands = [];
  for (let i = 0; i < NB; i++) {
    const ch = date[i] === " " ? null : date[i];
    const roll = o.roll ? (rnd() - 0.5) * o.roll : 0;
    const tex = bandTexture(THREE, ch, alphabet, seed + 31 * i, roll, o.blur || 0);
    const rub = new THREE.MeshStandardMaterial({ color: 0xffffff, map: tex.map, bumpMap: tex.bump,
      bumpScale: 2.2, roughness: 0.74, metalness: 0.0 });
    const cyl = new THREE.Mesh(new THREE.CylinderGeometry(R, R, BW, 96, 1, true, -Math.PI, Math.PI * 2), rub);
    cyl.rotation.z = Math.PI / 2;
    cyl.position.set(x0 + i * (BW + GAP), AX, 0);
    cyl.name = "band " + i;
    G.add(cyl);
    // the band's straight run down to the print face (front and back faces)
    const run = new THREE.Mesh(new THREE.BoxGeometry(BW * 0.98, AX - 0.035, 2 * R * 0.985),
      new THREE.MeshStandardMaterial({ color: 0x241e1b, roughness: 0.8 }));
    run.position.set(x0 + i * (BW + GAP), (AX - 0.035) / 2 + 0.035, 0);
    G.add(run);
    // the knurled wheel hub showing between bands
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(R * 0.78, R * 0.78, GAP * 0.9, 64), steelDark);
    hub.rotation.z = Math.PI / 2; hub.position.set(x0 + i * (BW + GAP) + (BW + GAP) / 2, AX, 0);
    if (i < NB - 1) G.add(hub);
    G.userData.bands.push(cyl);
  }
  // the print face: a thin rubber platen at the bottom of the bands
  const face = new THREE.Mesh(new THREE.BoxGeometry(span, 0.035, 0.30),
    new THREE.MeshStandardMaterial({ color: 0x1b1614, roughness: 0.6 }));
  face.position.y = 0.0175; G.add(face);
  G.userData.bandCenterY = AX; G.userData.bandRadius = R; G.userData.span = span;
  return G;
}

export function feltMaterial(THREE, o) {
  o = o || {};
  const W = 512, c = document.createElement("canvas"); c.width = c.height = W;
  const g = c.getContext("2d"), rnd = mulberry(o.seed || 77);
  g.fillStyle = "#808080"; g.fillRect(0, 0, W, W);
  for (let i = 0; i < 26000; i++) {
    const x = rnd() * W, y = rnd() * W, a = rnd() * 6.28, l = 2 + rnd() * 5;
    const v = 100 + rnd() * 70;
    g.strokeStyle = "rgba(" + v + "," + v + "," + v + ",0.35)"; g.lineWidth = 0.8;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
  }
  const bump = new THREE.CanvasTexture(c); bump.wrapS = bump.wrapT = THREE.RepeatWrapping;
  bump.repeat.set(o.repeat || 8, o.repeat || 8);
  return new THREE.MeshStandardMaterial({ color: o.color != null ? o.color : 0x1b3a30, roughness: 0.96,
    metalness: 0, bumpMap: bump, bumpScale: 0.8 });
}

/* Bond paper with tooth and an optional dater impression (text, ink, x, y in
 * 0..1 of the sheet, size). The ink is drawn starved at the edges like a real
 * stamp; gold is held back to #FFC72C after the frame's grade by the slide. */
export function sheetTexture(THREE, o) {
  o = o || {};
  const W = o.px || 1024, H = Math.round(W * (o.aspect || 1.294));
  const c = document.createElement("canvas"); c.width = W; c.height = H;
  const g = c.getContext("2d"), rnd = mulberry(o.seed || 91);
  // bond in lamplight: lit toward the upper left, falling off across the sheet
  const pf = g.createLinearGradient(0, 0, W, H); pf.addColorStop(0, o.paper || "#d9d8cf"); pf.addColorStop(1, o.paperLee || "#a9a89f");
  g.fillStyle = pf; g.fillRect(0, 0, W, H);
  for (let i = 0; i < W * H / 30; i++) {
    const x = rnd() * W, y = rnd() * H, v = rnd();
    g.fillStyle = v < 0.5 ? "rgba(120,118,110,0.10)" : "rgba(255,255,250,0.14)";
    g.fillRect(x, y, 1.5, 1.5);
  }
  if (o.impression) {
    const im = o.impression;
    const cx = im.x * W, cy = im.y * H, s = (im.size || 0.42) * W;
    g.save(); g.translate(cx, cy); g.rotate(im.rot || -0.03);
    const ink = im.ink || "#FFC72C";
    const lw = s * (im.weight >= 700 ? 0.034 : 0.018);
    g.font = (im.weight || 500) + " " + Math.round(s * 0.15) + "px 'JetBrains Mono', monospace";
    g.textAlign = "center"; g.textBaseline = "middle";
    // pressed ink: a dark deboss edge under the gold, offset away from the lamp, so a pale ink on
    // pale paper still reads as a mark
    g.strokeStyle = "rgba(60,40,10,0.55)"; g.lineWidth = lw; g.strokeRect(-s / 2 + 2, -s * 0.17 + 2, s, s * 0.34);
    g.fillStyle = "rgba(60,40,10,0.55)"; g.fillText(im.text, 2.5, s * 0.01 + 2.5);
    g.strokeStyle = ink; g.lineWidth = lw; g.strokeRect(-s / 2, -s * 0.17, s, s * 0.34);
    g.fillStyle = ink; g.fillText(im.text, 0, s * 0.01);
    g.restore();
    // starve the ink: knock out tooth-sized flecks inside the impression box
    g.save(); g.globalCompositeOperation = "destination-over"; g.restore();
    for (let i = 0; i < s * s * 0.012; i++) {
      const x = cx + (rnd() - 0.5) * s * 1.05, y = cy + (rnd() - 0.5) * s * 0.4;
      g.fillStyle = o.paper || "#d9d8cf"; g.globalAlpha = 0.55 * rnd();
      g.fillRect(x, y, 1.6, 1.6);
    }
    g.globalAlpha = 1;
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}

/* The desk's own reflection environment (round 1, 2026-11-26). akthree's studio
 * environment carries a cool blue bounce panel to the right, and a nickel plate
 * facing that way mirrored it as a flat navy face on every frame. This room has
 * the lamp as a warm softbox high on the left, a dim warm wall in front of the
 * desk (where the camera is), a cool window strip behind, and a dark felt floor. */
export function deskEnvironment(THREE, R, o) {
  o = o || {};
  const env = new THREE.Scene();
  env.add(new THREE.Mesh(new THREE.BoxGeometry(20, 14, 20), new THREE.MeshBasicMaterial({ color: 0x141412, side: THREE.BackSide })));
  function panel(w, h, color, i, pos, rot) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide }));
    p.material.color.multiplyScalar(i); p.position.set(...pos); if (rot) p.rotation.set(...rot); env.add(p); return p;
  }
  panel(6, 4, 0xffe2b8, o.lamp != null ? o.lamp : 7.0, [-5, 5.5, 3], [Math.PI / 3.2, 0.6, 0]);   // the lamp
  panel(16, 6, 0xc8beae, o.room != null ? o.room : 0.9, [0, 2.5, 9], [0, Math.PI, 0]);         // the room in front
  panel(6, 3, o.windowColor != null ? o.windowColor : 0x2c4a6c, o.window != null ? o.window : 1.2, [3, 3, -9], null); // the window
  panel(14, 8, 0xd9cfbf, o.side != null ? o.side : 1.5, [9.5, 2.5, -1], [0, -Math.PI / 2, 0]);  // the lit side wall the plates mirror
  panel(16, 16, 0x1b2a22, 0.6, [0, -6.9, 0], [-Math.PI / 2, 0, 0]);                              // felt floor
  const pm = new THREE.PMREMGenerator(R.renderer);
  const tex = pm.fromScene(env, 0.03).texture;
  R.scene.environment = tex;
  if ('environmentIntensity' in R.scene) R.scene.environmentIntensity = o.intensity != null ? o.intensity : 1.0;
  pm.dispose();
  return tex;
}
