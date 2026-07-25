#!/usr/bin/env python3
"""build_slides.py — Carousel No. 17 (2026-07-25) "On File, Off Record."

Emits the ten bespoke slide HTML files for the MILLED REGISTER chassis. One
bone slab, one orthographic camera, one key light that rotates a few degrees
per slide. Every geometric position in the deck comes from the projection
constants below, so the art and the numbers cannot drift apart.

Why a generator rather than ten hand-typed files: the deck IS one continuous
object seen ten times, so the camera math, the zone system and the money scale
must be byte-identical across slides. Per-slide art is still bespoke (each
slide's WELLS / SCORED / TABS / mode differ and several slides have their own
draw hooks); the generator only guarantees the shared chassis.

Ships into runs/<date>/ so the deck is reproducible.
"""
import json
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geom import sx, sy, wend, W_PER_M, WELL_X0

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out/2026-07-25/slides")
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260725

# ---------------------------------------------------------------- palette ----
P = dict(
    lit="#F4EFE4", mid="#E6DECE", shadow="#CFC4AF",
    groove="#3A3128", grooveDeep="#17130F", grooveWall="#4A4038",
    ink="#15110D", body="#3A342C", label="#5F5849", hair="#8A8375",
    fireweed="#C0246B", navy="#0E2138", snow="#F4F8FF",
    gold="#FFC72C", shade="#6F6353",
)

# ------------------------------------------------------- shared head / css ---
HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
  html,body{margin:0;padding:0;width:1080px;height:1350px;overflow:hidden;
    background:%(lit)s;-webkit-font-smoothing:antialiased}
  #art{position:absolute;left:0;top:0;width:1080px;height:1350px;display:block}
  svg{display:block}
  .z{position:absolute}
  .keyline{left:44px;top:44px;width:990px;height:1260px;
    border:1.25px solid %(ink)s;opacity:.55;pointer-events:none}
  .kicker{position:absolute;left:80px;top:88px;width:900px;font-family:"JetBrains Mono";
    font-weight:500;font-size:24px;letter-spacing:.10em;text-transform:uppercase;
    color:%(label)s;line-height:1.3}
  .display{position:absolute;left:74px;top:170px;font-family:"Fraunces";color:%(ink)s;
    font-variation-settings:"SOFT" 60,"WONK" 1,"opsz" 144;font-weight:850;
    line-height:.98;letter-spacing:-.025em;margin:0}
  .base{position:absolute;left:80px;top:1192px;width:910px;font-family:"Bricolage Grotesque";
    font-weight:400;font-size:30px;line-height:1.34;color:%(body)s}
  .basemono{position:absolute;left:80px;top:1200px;width:900px;font-family:"JetBrains Mono";
    font-weight:500;font-size:24px;letter-spacing:.10em;text-transform:uppercase;
    color:%(label)s}
  .lab{position:absolute;font-family:"JetBrains Mono";font-weight:500;
    font-size:24px;letter-spacing:.08em;text-transform:uppercase;
    font-variant-numeric:tabular-nums lining-nums;color:%(ink)s;
    line-height:1.25;white-space:nowrap}
  .lab.dk{color:%(label)s}
  .lab.sm{font-size:24px}
  .plate{background:rgba(244,239,228,.90);padding:2px 7px;border-radius:1px}
  .chip{position:absolute;font-family:"JetBrains Mono";font-weight:500;
    font-size:24px;letter-spacing:.07em;text-transform:uppercase;color:%(label)s;
    border-top:1.25px solid %(hair)s;padding-top:7px;line-height:1.35}
  .chip.fw{border-top:2.5px solid %(fireweed)s;color:%(body)s}
  .navychip{position:absolute;background:%(navy)s;color:%(gold)s;
    font-family:"JetBrains Mono";font-weight:500;font-size:26px;
    letter-spacing:.08em;padding:12px 18px 11px}
  .wm{position:absolute;font-family:"Fraunces";font-weight:800;font-size:26px;
    font-variation-settings:"opsz" 36;letter-spacing:.02em;color:%(ink)s}
  .site{position:absolute;font-family:"JetBrains Mono";font-weight:400;
    font-size:24px;letter-spacing:.06em;color:%(label)s}
  .ctr{position:absolute;font-family:"JetBrains Mono";font-weight:500;
    font-size:24px;letter-spacing:.10em;color:%(body)s;
    font-variant-numeric:tabular-nums lining-nums}
  .coord{position:absolute;font-family:"JetBrains Mono";font-weight:400;
    font-size:17px;letter-spacing:.08em;color:%(hair)s}
</style></head><body>
<canvas id="art" width="2160" height="2700"></canvas>
<div class="z keyline" data-decorative></div>
""" % P

TAIL_SCRIPTS = """
<script src="@@ASSETS@@/js/noise.js"></script>
<script src="@@ASSETS@@/js/akrelief.js"></script>
<script src="@@ASSETS@@/js/akcolor.js"></script>
<script src="@@ASSETS@@/js/akpost.js"></script>
<script src="@@ASSETS@@/js/aktype.js"></script>
"""

# ------------------------------------------------------------- chassis JS ----
# The shared milled-register renderer. All geometry derives from the
# orthographic projection stated in the storyboard header.
CHASSIS = r"""
const SEED = %(seed)d;
const P = %(palette)s;
const CFG = %(cfg)s;

/* ---- the one projection: AXONOMETRIC orthographic, az 14 deg, pitch 31.75.
   Azimuth 0 rendered the slab as a flat rectangle (first build, rejected on the
   contact sheet). With azimuth every face is a parallelogram, so the solid gains
   a second visible side face and every recess shows TWO interior walls. Still a
   parallel projection, so cut lengths keep encoding dollars honestly.
     screen_x = 540 + 259.1*(0.9703x - 0.2419z)
     screen_y = 905 + 259.1*(0.1273x + 0.5106z - 0.8505y)                    */
const S = 259.1, CX = 540, ACY = 872;
const KX = 0.9703, KZ = -0.2419, MX = 0.1273, MZ = 0.5106, MY = 0.8505;
const PX = (x, z) => CX + S * (KX * x + KZ * z);
const PY = (x, y, z) => ACY + S * (MX * x + MZ * z - MY * y);
/* back-compat shims for the label maths */
const px = (x) => PX(x, 0);
const py = (y, z) => PY(0, y, z);
const dep = (d) => S * d * MY;
const SLABX = 1.50, SLABZ = 1.15, SLABTH = 0.30, RECESS = 0.09;
const PPM = 165.6, WPERM = 0.6530, WX0 = -1.42;

function quad(cx, pts, fill) {
  cx.beginPath();
  cx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) cx.lineTo(pts[i][0], pts[i][1]);
  cx.closePath();
  if (fill) { cx.fillStyle = fill; cx.fill(); }
}
/* a horizontal face at height y over the x-z rect */
const face = (x0, x1, z0, z1, y) => [
  [PX(x0, z0), PY(x0, y, z0)], [PX(x1, z0), PY(x1, y, z0)],
  [PX(x1, z1), PY(x1, y, z1)], [PX(x0, z1), PY(x0, y, z1)]];
/* a vertical wall spanning x0..x1 at constant z, from y0 down to y1 */
const wallZ = (x0, x1, z, y0, y1) => [
  [PX(x0, z), PY(x0, y0, z)], [PX(x1, z), PY(x1, y0, z)],
  [PX(x1, z), PY(x1, y1, z)], [PX(x0, z), PY(x0, y1, z)]];
/* a vertical wall spanning z0..z1 at constant x */
const wallX = (z0, z1, x, y0, y1) => [
  [PX(x, z0), PY(x, y0, z0)], [PX(x, z1), PY(x, y0, z1)],
  [PX(x, z1), PY(x, y1, z1)], [PX(x, z0), PY(x, y1, z0)]];

function mix(a, b, t) { return AKC.mixOklab(a, b, t); }
function lerpG(cx, x0, y0, x1, y1, stops) {
  const g = cx.createLinearGradient(x0, y0, x1, y1);
  stops.forEach(s => g.addColorStop(s[0], s[1]));
  return g;
}
const AZ = CFG.az, SHMUL = CFG.shmul;
const GOLDPASS = [];

/* ---------------------------------------------------- two-part shadow ----- */
function slabShadow(cx) {
  const len = SLABTH * SHMUL;
  const off = S * MZ * len * 3.4;
  cx.save();
  cx.globalAlpha = 0.20; cx.fillStyle = P.shade; cx.filter = 'blur(30px)';
  const f = face(-SLABX, SLABX, -SLABZ, SLABZ, -SLABTH);
  quad(cx, f.map(q => [q[0] - 8, q[1] + off * 0.9]), P.shade);
  cx.filter = 'none';
  cx.globalAlpha = 0.46; cx.filter = 'blur(5px)';
  quad(cx, f.map(q => [q[0] - 3, q[1] + off * 0.28]), P.shade);
  cx.filter = 'none';
  cx.restore();
}

/* ---------------------------------------------------------- the slab ----- */
function slabBody(cx) {
  const T = face(-SLABX, SLABX, -SLABZ, SLABZ, 0);
  /* the two side faces the azimuth makes visible: front (+z) and right (+x) */
  quad(cx, wallZ(-SLABX, SLABX, SLABZ, 0, -SLABTH),
    lerpG(cx, T[3][0], T[3][1], T[2][0], T[2][1] + 66,
      [[0, '#9C8F76'], [1, '#B4A88E']]));
  quad(cx, wallX(-SLABZ, SLABZ, SLABX, 0, -SLABTH),
    lerpG(cx, T[1][0], T[1][1], T[2][0], T[2][1],
      [[0, '#D3C7AE'], [1, '#BCAF95']]));
  /* top face, lit from the azimuth side */
  quad(cx, T, lerpG(cx, T[0][0], T[0][1], T[2][0], T[2][1],
    [[0, '#F8F3E9'], [0.5, P.lit], [1, mix(P.mid, P.shadow, 0.35)]]));
  /* chamfers: a lit hairline along each top edge that faces the key */
  cx.save();
  cx.strokeStyle = mix(P.lit, '#ffffff', 0.55); cx.lineWidth = 2;
  cx.beginPath(); cx.moveTo(T[3][0], T[3][1]); cx.lineTo(T[2][0], T[2][1]);
  cx.lineTo(T[1][0], T[1][1]); cx.stroke();
  cx.strokeStyle = mix(P.mid, P.shadow, 0.8); cx.lineWidth = 1.5;
  cx.beginPath(); cx.moveTo(T[0][0], T[0][1]); cx.lineTo(T[1][0], T[1][1]); cx.stroke();
  cx.restore();
}

/* stone tooth: real Sobel-lit micro relief, soft-light over the slab so it
   reads as milled stone rather than a flat fill */
function stoneTooth(cx) {
  const T = face(-SLABX, SLABX, -SLABZ, SLABZ, 0);
  const x0 = Math.min(...T.map(q => q[0])), x1 = Math.max(...T.map(q => q[0]));
  const y0 = Math.min(...T.map(q => q[1])), y1 = Math.max(...T.map(q => q[1])) + 70;
  const w = Math.round(x1 - x0), h = Math.round(y1 - y0);
  const off = document.createElement('canvas');
  off.width = w * 2; off.height = h * 2;
  const ox = off.getContext('2d'); ox.scale(2, 2);
  ox.fillStyle = '#808080'; ox.fillRect(0, 0, w, h);
  AK.reliefShade(ox, { x: 0, y: 0, w: w, h: h, scale: 2, seed: SEED,
    noiseScale: 0.06, octaves: 4, warp: 0.35, strength: 2.6,
    low: '#645d54', high: '#a49b90', ambient: 0.40, diffuse: 0.78 });
  cx.save();
  cx.globalAlpha = 0.40; cx.globalCompositeOperation = 'soft-light';
  cx.drawImage(off, x0, y0, w, h);
  cx.restore();
}

/* ------------------------------------------------------------- a well ---- */
function well(cx, w) {
  const d = -(w.d == null ? RECESS : w.d);
  const F = face(w.x0, w.x1, w.z0, w.z1, d);
  const O = face(w.x0, w.x1, w.z0, w.z1, 0);      /* the OPENING */
  const floor = w.fill || P.groove;
  /* everything inside a recess is seen THROUGH the opening, so clip to it */
  cx.save();
  quad(cx, O); cx.clip();
  /* the two interior walls the azimuth reveals: far (-z) and left (-x) */
  quad(cx, wallZ(w.x0, w.x1, w.z0, 0, d), mix(floor, '#000000', 0.30));
  quad(cx, wallX(w.z0, w.z1, w.x0, 0, d), mix(floor, '#000000', 0.48));
  /* floor, with AO pooling toward the two walls */
  quad(cx, F, lerpG(cx, F[0][0], F[0][1], F[2][0], F[2][1],
    [[0, mix(floor, '#000000', 0.42)], [0.55, floor], [1, mix(floor, '#000000', 0.12)]]));
  /* the lip: a dark score on the near/right edges, a lit chamfer on far/left */
  cx.save();
  const T = face(w.x0, w.x1, w.z0, w.z1, 0);
  cx.restore();                                   /* end opening clip */
  /* FAR and LEFT edges: the surface breaks away, so a dark crease */
  cx.strokeStyle = mix(P.groove, P.shadow, 0.25); cx.lineWidth = 2.2;
  cx.beginPath(); cx.moveTo(T[3][0], T[3][1]); cx.lineTo(T[0][0], T[0][1]);
  cx.lineTo(T[1][0], T[1][1]); cx.stroke();
  /* NEAR and RIGHT edges: the lit chamfer of the opening */
  cx.strokeStyle = mix(P.lit, '#ffffff', 0.55); cx.lineWidth = 2.0;
  cx.beginPath(); cx.moveTo(T[1][0], T[1][1]); cx.lineTo(T[2][0], T[2][1]);
  cx.lineTo(T[3][0], T[3][1]); cx.stroke();
  cx.restore();
  /* fireweed inlay, seated INSIDE the groove and occluded by its far wall */
  if (w.fw) {
    cx.save(); quad(cx, O); cx.clip();
    quad(cx, face(w.x0 + 0.012, w.fwx1, w.z0 + 0.012, w.z1 - 0.012, d + 0.004), P.fireweed);
    quad(cx, wallZ(w.x0 + 0.012, w.fwx1, w.z0 + 0.012, d + 0.004, d),
      mix(P.fireweed, '#000000', 0.42));
    cx.restore();
  }
  /* the deck's gold carrier: one specular line where the floor meets the light */
  if (w.gold) {
    GOLDPASS.push(w);
    cx.save();
    const gx0 = F[0][0] + (F[1][0] - F[0][0]) * 0.06, gy0 = F[0][1] + (F[1][1] - F[0][1]) * 0.06;
    const gx1 = F[0][0] + (F[1][0] - F[0][0]) * 0.42, gy1 = F[0][1] + (F[1][1] - F[0][1]) * 0.42;
    const iy = (F[3][1] - F[0][1]) * 0.46;
    cx.save(); quad(cx, O); cx.clip();
    cx.strokeStyle = P.gold; cx.lineWidth = 2.6; cx.globalAlpha = 0.92;
    cx.beginPath(); cx.moveTo(gx0, gy0 + iy); cx.lineTo(gx1, gy1 + iy); cx.stroke();
    cx.globalAlpha = 0.22; cx.lineWidth = 7; cx.filter = 'blur(5px)'; cx.stroke();
    cx.restore(); cx.restore();
  }
}

/* a SCORED outline: ruled, never cut. No interior colour, ever. */
function scored(cx, r) {
  const T = face(r.x0, r.x1, r.z0, r.z1, 0);
  cx.save();
  cx.strokeStyle = r.phantom ? P.hair : mix(P.hair, P.body, 0.55);
  cx.lineWidth = r.phantom ? 1.5 : 2.0;
  cx.setLineDash(r.phantom ? [30, 5, 6, 5, 6, 5] : []);
  quad(cx, T); cx.stroke();
  cx.restore();
  if (r.dot) {
    cx.fillStyle = P.body;
    cx.beginPath(); cx.arc(T[0][0], T[0][1] + (T[3][1] - T[0][1]) / 2, 4.6, 0, 6.2832); cx.fill();
  }
}

/* a raised TAB: proud of the surface. Somebody else's decision on our stone. */
function tab(cx, r) {
  const h = 0.07;
  const T = face(r.x0, r.x1, r.z0, r.z1, h);
  cx.save();
  cx.globalAlpha = 0.30; cx.filter = 'blur(8px)';
  quad(cx, face(r.x0, r.x1, r.z0, r.z1, 0).map(q => [q[0] - 5, q[1] + 13]), P.shade);
  cx.filter = 'none'; cx.restore();
  quad(cx, wallZ(r.x0, r.x1, r.z1, h, 0), '#B4A88E');
  quad(cx, wallX(r.z0, r.z1, r.x1, h, 0), '#CCC0A6');
  quad(cx, T, lerpG(cx, T[0][0], T[0][1], T[2][0], T[2][1],
    [[0, '#F8F3E9'], [1, P.mid]]));
  cx.save();
  cx.strokeStyle = mix(P.lit, '#ffffff', 0.5); cx.lineWidth = 1.8;
  cx.beginPath(); cx.moveTo(T[0][0], T[0][1]); cx.lineTo(T[1][0], T[1][1]); cx.stroke();
  cx.restore();
}

/* ------------------------------------------------------------- compose --- */
async function paint() {
  const cv = document.getElementById('art');
  const cx = cv.getContext('2d');
  cx.scale(2, 2);
  /* ground: the room the slab sits in */
  cx.fillStyle = lerpG(cx, 0, 0, 0, 1350,
    [[0, '#F6F1E7'], [0.46, '#EFE8DA'], [1, mix('#CDC1AA', '#B3A68C', CFG.late)]]);
  cx.fillRect(0, 0, 1080, 1350);

  if (CFG.mode !== 'gl') { slabShadow(cx); slabBody(cx); stoneTooth(cx); }

  if (CFG.mode === 'gl') { await glBays(cx); stoneTooth(cx); }

  (CFG.wells || []).forEach(w => well(cx, w));
  (CFG.scored || []).forEach(r => scored(cx, r));
  (CFG.tabs || []).forEach(r => tab(cx, r));
  if (typeof extraArt === 'function') extraArt(cx);

  AKPOST.grade(cx, {
    w: 1080, h: 1350, exposure: 0.02, saturation: 0.98, contrast: 1.04,
    filmic: true, lift: [0.008, 0.006, 0.003], gain: [1.010, 1.003, 0.992],
    vignette: 0.10, bloom: { threshold: 0.86, strength: 0.16, radius: 7 },
    grain: { amount: 0.05, size: 2, seed: SEED }, aberration: 0,
    dither: true, sharpen: 0.32
  });
  /* flag gold AFTER the grade: #FFC72C is a brand role, and the ACES curve was
     pushing it to an acid yellow-green next to the ungraded SVG Polaris. */
  GOLDPASS.forEach(w => {
    const d = -(w.d == null ? RECESS : w.d);
    const F = face(w.x0, w.x1, w.z0, w.z1, d);
    const gx0 = F[0][0] + (F[1][0] - F[0][0]) * 0.06, gy0 = F[0][1] + (F[1][1] - F[0][1]) * 0.06;
    const gx1 = F[0][0] + (F[1][0] - F[0][0]) * 0.42, gy1 = F[0][1] + (F[1][1] - F[0][1]) * 0.42;
    const iy = (F[3][1] - F[0][1]) * 0.46;
    cx.save();
    quad(cx, face(w.x0, w.x1, w.z0, w.z1, 0)); cx.clip();
    cx.strokeStyle = '#FFC72C'; cx.lineWidth = 2.6; cx.globalAlpha = 0.95;
    cx.beginPath(); cx.moveTo(gx0, gy0 + iy); cx.lineTo(gx1, gy1 + iy); cx.stroke();
    cx.restore();
  });
  if (typeof afterGrade === 'function') afterGrade(cx);
}

window.renderReady = new Promise(async (resolve) => {
  try {
    await document.fonts.ready;
    document.querySelectorAll('[data-fit]').forEach(el => {
      const o = JSON.parse(el.getAttribute('data-fit'));
      AK.fitText(el, o);
    });
    await paint();
  } catch (e) {
    document.title = 'RENDER ERROR ' + e.message;
    console.error(e);
  }
  resolve(true);
});
"""

# --------------------------------------------------- the GL hero (slide 6) ---
GL_HERO = r"""
/* Slide 06 hero. akthree GPU PBR under an OrthographicCamera so the milled
   register keeps real materials, real soft shadows and real IBL while every
   quantity in the deck stays parallel-projected. Doctrine forbids perspective
   on quantities; this is how a rendered hero stays honest.

   Frustum derived from the shared projection, not eyeballed:
     px per world unit s = 259.1, canvas 1080 x 1350
     half-width  = 540 / 259.1 = 2.0841
     half-height = 675 / 259.1 = 2.6052
     world origin must land at screen_y 905, i.e. 230 px below canvas centre,
     so the camera looks at (0, 230/259.1/0.8505, 0) = (0, 1.0437, 0)
     view dir = (0, sin 31.75, cos 31.75) = (0, 0.5262, 0.8505), dist 12
     => camera at (0, 7.358, 10.206)                                        */
async function glBays(cx) {
  const off = document.createElement('canvas');
  off.width = 2160; off.height = 2700;
  let ok = false;
  try {
    const THREE = await import('@@ASSETS@@/js/three.module.min.js');
    const { init } = await import('@@ASSETS@@/js/akthree.js');
    const AKT = init(THREE);
    if (!AKT.webglOK()) throw new Error('no webgl');
    const R = AKT.setup(off, { w: 1080, h: 1350, exposure: 1.02, bg: 0xf4efe4 });
    const HW = 540 / 259.1, HH = 675 / 259.1;
    R.camera = new THREE.OrthographicCamera(-HW, HW, HH, -HH, 0.1, 100);
    /* azimuth 14 deg, pitch 31.75 deg, matching geom.py exactly. The look-at
       point puts world origin at screen_y 905, i.e. 230 px below canvas centre. */
    const LY = 230 / 259.1 / 0.8505;            /* 1.0437 */
    const d = 12, ca = Math.cos(14 * Math.PI / 180), sa = Math.sin(14 * Math.PI / 180);
    const cp = Math.cos(31.75 * Math.PI / 180), sp = Math.sin(31.75 * Math.PI / 180);
    R.camera.position.set(d * cp * sa, LY + d * sp, d * cp * ca);
    R.camera.lookAt(0, LY, 0);
    AKT.environment(R, { intensity: 0.30 });
    /* the room the slab sits in, so the cast shadow is a real PBR shadow */
    AKT.ground(R, { size: 90, color: 0xded3bf, roughness: 0.95, y: -0.31 });

    const stone = AKT.mat.clay(0xf3ede1, { roughness: 0.88 });
    const side  = AKT.mat.clay(0xcfc4af, { roughness: 0.90 });
    const wall  = AKT.mat.clay(0x6b6253, { roughness: 0.94 });
    const deep  = AKT.mat.clay(0x3a3128, { roughness: 0.95 });
    const G = new THREE.Group();
    const plane = (w, h, mat, pos, rot) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
      m.position.set(pos[0], pos[1], pos[2]);
      if (rot) m.rotation.set(rot[0], rot[1], rot[2]);
      m.castShadow = true; m.receiveShadow = true; G.add(m); return m;
    };
    const D = -Math.PI / 2, H = Math.PI / 2;
    /* The slab is a PLANE SHELL, not a solid box, because the left bay has to be
       a genuine hole. A box would show its own lid where the bay should be. */
    /* top plate, four strips tiling AROUND the left bay. The right bay is NOT
       recessed, so it is simply top face, which is the entire argument. */
    plane(3.00, 0.53, stone, [0, 0, -0.885], [D, 0, 0]);
    plane(3.00, 0.53, stone, [0, 0, 0.885], [D, 0, 0]);
    plane(0.10, 1.24, stone, [-1.45, 0, 0], [D, 0, 0]);
    plane(1.56, 1.24, stone, [0.72, 0, 0], [D, 0, 0]);
    /* the two outer side faces the azimuth makes visible */
    plane(3.00, 0.30, side, [0, -0.15, 1.15], null);
    plane(2.30, 0.30, side, [1.50, -0.15, 0], [0, H, 0]);
    /* the bay: a dark floor, the two interior walls this camera sees, and two
       occluders that exist so the key light cannot leak through the recess */
    plane(1.34, 1.24, deep, [-0.73, -0.26, 0], [D, 0, 0]);
    plane(1.34, 0.26, wall, [-0.73, -0.13, -0.62], null);
    plane(1.24, 0.26, wall, [-1.40, -0.13, 0], [0, H, 0]);
    plane(1.34, 0.26, wall, [-0.73, -0.13, 0.62], [0, Math.PI, 0]);
    plane(1.24, 0.26, wall, [-0.06, -0.13, 0], [0, -H, 0]);
    AKT.add(R, G);
    /* one key light for the whole deck, azimuth 151 deg, elevation 35 deg */
    AKT.rig(R, {
      key: { color: 0xfff3e0, i: 3.6, pos: [3.4, 7.6, 4.2], radius: 8, shadowSize: 6 },
      fill: { color: 0xdcd6c8, i: 0.42, pos: [4.0, 2.2, 6.0] },
      ambient: { color: 0xa89f8d, i: 0.75 }
    });
    const snap = await AKT.snapshot(R);
    ok = !!snap.ok;
    document.title = 'S6 gl ok=' + snap.ok + ' lit=' + snap.litCount;
  } catch (e) {
    ok = false;
    document.title = 'S6 gl fallback ' + e.message;
  }
  if (ok) {
    cx.drawImage(off, 0, 0, 1080, 1350);
  } else {
    /* DESIGNED fallback, geometrically identical because the camera is
       orthographic: the same bay, relit on the CPU by akrelief. */
    slabShadow(cx); slabBody(cx);
    well(cx, { x0: -1.40, x1: -0.06, z0: -0.62, z1: 0.62, d: 0.26 });
  }
  /* the SCORED right bay is drawn in the SVG overlay so it stays vector in the
     PDF; nothing is ever filled inside it. */
}
"""


def wm(n, coord):
    wmx = 80
    if n == 10:
        return (f'<div class="wm" data-decorative style="left:80px;top:1288px">ALASKA.AI</div>'
                f'<div class="ctr" data-decorative style="left:894px;top:1292px">{n:02d} / 10</div>')
    """footer block: wordmark, site on the close only, counter, coordinates."""
    return f"""
<div class="wm" data-decorative style="left:{wmx}px;top:1288px">ALASKA.AI</div>
<div class="ctr" data-decorative style="left:894px;top:1292px">{n:02d} / 10</div>
<div class="coord" data-decorative style="left:560px;top:1298px">{coord}</div>
"""


SLIDES = []


def slide(n, *, az, shmul, late, mode="canvas", cfg_extra=None, dom="",
          extra_js="", coord="61 deg 13'N 149 deg 54'W"):
    cfg = dict(az=az, shmul=shmul, late=late, mode=mode)
    cfg.update(cfg_extra or {})
    chassis = CHASSIS % dict(seed=SEED, palette=json.dumps(P), cfg=json.dumps(cfg))
    gl = GL_HERO if mode == "gl" else ""
    body = HEAD + dom + wm(n, coord) + TAIL_SCRIPTS
    if mode == "gl":
        body += "<script type=\"module\">\n" + gl + extra_js + chassis + "\n</script>\n"
    else:
        body += "<script>\n" + extra_js + chassis + "\n</script>\n"
    body += "</body></html>\n"
    SLIDES.append((n, body))


# =============================================================== SLIDE 01 ====


def L(x, z, dx=0, dy=0, cls="lab dk sm", txt="", plate=False):
    """place a label at a world point on the slab's top face."""
    inner = f'<span class="plate">{txt}</span>' if plate else txt
    return (f'<div class="{cls}" style="left:{sx(x, z) + dx:.0f}px;'
            f'top:{sy(x, 0, z) + dy:.0f}px">{inner}</div>\n')


# Cover. Two cuts of IDENTICAL length. The difference between them is DEPTH,
# not size, which is the thesis stated before a word of argument.
W18 = wend(1.80)
W372 = wend(0.372)
slide(
    1, az=118, shmul=0.53, late=0.20, coord="58 deg 18'N 134 deg 25'W",
    cfg_extra=dict(
        wells=[dict(x0=WELL_X0, x1=W18, z0=-0.86, z1=-0.56, d=0.16,
                    fw=True, fwx1=W372, gold=True)],
        scored=[dict(x0=WELL_X0, x1=W18, z0=0.14, z1=0.44, phantom=True)],
    ),
    dom=f"""
<div class="z kicker" style="width:660px">Alaska governor 2026, 24 days to the primary</div>
<div class="navychip" style="left:740px;top:80px">AUG 18 2026</div>
<h1 class="display" style="width:900px;font-size:126px"
    data-fit='{{"min":92,"max":126,"maxLines":4}}'>THE MONEY<br>IS ON FILE.<br>THE AI POLICY<br>IS NOT.</h1>
""" + L(W18, -0.71, 20, -14, txt="Cut to the dollar")
      + L(W18, 0.29, 20, -14, txt="Ruled, never cut")
      + """<div class="basemono" style="width:940px">Campaign finance reports made public the week of July 20</div>
""")

# =============================================================== SLIDE 02 ====
slide(
    2, az=124, shmul=0.72, late=0.24, coord="60 deg 29'N 151 deg 03'W",
    cfg_extra=dict(
        wells=[dict(x0=WELL_X0, x1=W18, z0=-0.92, z1=-0.62, d=0.16,
                    fw=True, fwx1=W372, gold=True)],
    ),
    extra_js=r"""
function extraArt(cx) {
  /* dimension call on the fireweed segment: 4 px gap, 6 px overshoot, 3:1 heads */
  const zc = -0.50;
  const a = PX(WX0, zc), ay = PY(WX0, 0, zc);
  const b = PX(WX0 + 0.372 * WPERM, zc), by = PY(WX0 + 0.372 * WPERM, 0, zc);
  cx.save();
  cx.strokeStyle = P.body; cx.lineWidth = 1.25;
  cx.beginPath(); cx.moveTo(a, ay - 26); cx.lineTo(a, ay + 6);
  cx.moveTo(b, by - 26); cx.lineTo(b, by + 6);
  cx.moveTo(a, ay); cx.lineTo(b, by); cx.stroke();
  const head = (x, y, dir) => { cx.beginPath(); cx.moveTo(x, y);
    cx.lineTo(x + dir * 10, y - 3.3); cx.lineTo(x + dir * 10, y + 3.3);
    cx.closePath(); cx.fillStyle = P.body; cx.fill(); };
  head(a, ay, 1); head(b, by, -1);
  cx.restore();

  /* the drilled POINT. 100,000 dollars is 16.6 px at this deck's money scale,
     too short to read as a cut, so it is a POINT and never a stub. Its leader
     exits the right edge, which is the edge-tease slide 03 receives. */
  const dpx = PX(0.30, 0.74), dpy = PY(0.30, 0, 0.74);
  cx.save();
  quad(cx, [[dpx - 17, dpy], [dpx, dpy - 9], [dpx + 17, dpy], [dpx, dpy + 9]],
    mix(P.groove, '#000000', 0.25));
  cx.strokeStyle = mix(P.lit, '#ffffff', 0.4); cx.lineWidth = 1.6;
  cx.beginPath(); cx.moveTo(dpx - 17, dpy); cx.lineTo(dpx, dpy + 9);
  cx.lineTo(dpx + 17, dpy); cx.stroke();
  cx.strokeStyle = P.body; cx.lineWidth = 1.25;
  cx.beginPath(); cx.moveTo(dpx + 14, dpy - 4); cx.lineTo(dpx + 34, dpy - 24);
  cx.lineTo(dpx + 40, dpy - 24); cx.stroke();
  cx.beginPath(); cx.moveTo(dpx + 14, dpy + 4); cx.lineTo(dpx + 34, dpy + 4);
  cx.lineTo(1036, dpy + 4); cx.stroke();
  cx.fillStyle = P.body; cx.beginPath(); cx.arc(dpx, dpy, 3.4, 0, 6.2832); cx.fill();
  cx.restore();

  /* THE UNMEASURED BRACE. A dimension call with ONE extension line missing and
     its open terminus dissolving into hachure. The in-state share does not
     exist in the record, so it is drawn as a measurement that could not be
     taken. No fill, no midpoint, no percentage, ever. */
  const uz = 0.30, ua = PX(WX0, uz), uay = PY(WX0, 0, uz);
  const ub = PX(-0.30, uz), uby = PY(-0.30, 0, uz);
  cx.save();
  cx.strokeStyle = P.hair; cx.lineWidth = 1.25;
  cx.beginPath(); cx.moveTo(ua, uay - 26); cx.lineTo(ua, uay + 8); cx.stroke();
  const t0 = 0.52;
  cx.beginPath(); cx.moveTo(ua, uay);
  cx.lineTo(ua + (ub - ua) * t0, uay + (uby - uay) * t0); cx.stroke();
  for (let i = 0; i < 15; i++) {
    const t = t0 + i * 0.032;
    const x = ua + (ub - ua) * t, y = uay + (uby - uay) * t;
    cx.globalAlpha = 1 - i / 16;
    cx.beginPath(); cx.moveTo(x, y - 9); cx.lineTo(x + 10, y + 9); cx.stroke();
  }
  cx.restore();
}
""",
    dom=f"""
<div class="z kicker">What the law required</div>
<h1 class="display" style="width:820px;font-size:84px;font-variation-settings:'SOFT' 60,'WONK' 0,'opsz' 96;font-weight:800;line-height:1.02"
    data-fit='{{"min":62,"max":84,"maxLines":3}}'>Six people at one AI company, about a fifth of the biggest haul in the field.</h1>
<div class="chip fw" style="left:80px;top:470px;width:900px">This deck runs on a model built by Anthropic. Full disclosure, slide 09.</div>
""" + L(W18, -0.92, 22, -16, cls="lab dk sm", txt="1.8 M reported since February")
      + L(WELL_X0, -0.92, 10, -84, cls="lab", txt="372,000")
      + L(WELL_X0, -0.92, 10, -54, cls="lab dk sm", txt="Six Anthropic employees")
      + L(W372, -0.50, 22, 16, txt="About a fifth")
      + L(W372, -0.50, 22, 44, txt="Alaska.Ai arithmetic")
      + L(WELL_X0, 0.30, 6, 14, txt="In state share, not disclosed")
      + L(0.30, 0.74, 44, -34, txt="100,000 largest single gift")
      + L(0.30, 0.74, 44, -6, txt="Soldotna to Berkeley")
      + """<div class="z base">The majority came from Lower 48 donors, per Anchorage Daily News. No in state split is disclosed, so none is drawn.</div>
""")

# =============================================================== SLIDE 03 ====
STOPX = W18 - 0.24
slide(
    3, az=130, shmul=0.91, late=0.28, coord="58 deg 18'N 134 deg 25'W",
    cfg_extra=dict(wells=[dict(x0=WELL_X0, x1=STOPX, z0=-0.30, z1=0.00, d=0.16)]),
    extra_js=r"""
function extraArt(cx) {
  /* the raw, unfinished STOP FACE. The cut is 62 px short of the 1.8 M length
     the same object carried on slide 2, so the record visibly stops early. */
  const sxx = %(stopx)s, z0 = -0.30, z1 = 0.00, d = -0.16;
  const Wq = wallX(z0, z1, sxx, 0, d);
  cx.save();
  quad(cx, Wq, lerpG(cx, Wq[0][0], Wq[0][1], Wq[2][0], Wq[2][1],
    [[0, '#6A5C50'], [1, '#4A4038']]));
  /* seeded chisel chatter on the raw face */
  const rng = AK.rng(SEED + 3);
  cx.strokeStyle = 'rgba(255,246,230,.30)'; cx.lineWidth = 0.75;
  for (let i = 0; i < 18; i++) {
    const t = i / 18;
    const ax = Wq[0][0] + (Wq[1][0] - Wq[0][0]) * t, ay = Wq[0][1] + (Wq[1][1] - Wq[0][1]) * t;
    cx.beginPath(); cx.moveTo(ax, ay + 4); cx.lineTo(ax + 5 + rng() * 7, ay + 22 + rng() * 8); cx.stroke();
  }
  /* one gold glint down the stop face */
  cx.globalAlpha = 0.92; cx.strokeStyle = P.gold; cx.lineWidth = 2.6;
  cx.beginPath(); cx.moveTo(Wq[0][0] + 2, Wq[0][1] + 3); cx.lineTo(Wq[3][0] + 2, Wq[3][1] - 2); cx.stroke();
  cx.restore();
  /* edge-tease landing from slide 2 */
  cx.save();
  cx.strokeStyle = P.hair; cx.lineWidth = 1.25;
  cx.beginPath(); cx.moveTo(44, 262); cx.lineTo(88, 262); cx.stroke();
  cx.fillStyle = P.hair; cx.beginPath(); cx.arc(88, 262, 4.5, 0, 6.2832); cx.fill();
  cx.restore();
}
""" % dict(stopx=f"{STOPX:.4f}"),
    dom=f"""
<div class="z kicker">What he says he would do</div>
<h1 class="display" style="left:106px;width:820px;font-size:68px;font-style:italic;font-weight:600;font-variation-settings:'SOFT' 60,'WONK' 0,'opsz' 96;line-height:1.10;letter-spacing:-.015em"
    data-fit='{{"min":52,"max":68,"maxLines":3}}'>"I worry the AI industry has downplayed the risks posed to the public."</h1>
<div class="lab dk sm" style="left:106px;top:452px">Jonathan Kreiss-Tomkins</div>
<div class="chip" style="left:106px;top:500px;width:790px">Candidate survey, Northern Journal, June 2026. Background, outside the 10 day window.</div>
""" + L(WELL_X0, -0.30, 6, -40, txt="The record stops here")
      + """<div class="z base">On data centers he told the Anchorage Daily News that until Alaska has "a process and a policy", nothing should happen.</div>
""")

# =============================================================== SLIDE 04 ====
ROWS = [("Kreiss-Tomkins 1.8 M", 1.80), ("Heilala 1.6 M, 1.4 M of it his own", 1.60),
        ("Begich 1.1 M", 1.10), ("Taylor 1.0 M", 1.00), ("Crum 940,000", 0.94)]
Z0, ZH, ZG = -1.02, 0.34, 0.10
s4_wells = [dict(x0=WELL_X0, x1=wend(m), z0=Z0 + i * (ZH + ZG),
                 z1=Z0 + i * (ZH + ZG) + ZH, d=0.09)
            for i, (nm, m) in enumerate(ROWS)]
# the trench: 1.4 M from himself, cut DEEPER inside Heilala's own well. The
# deepest single cut anywhere in the deck is a candidate writing to himself.
HZ = Z0 + 1 * (ZH + ZG)
s4_wells.append(dict(x0=WELL_X0, x1=wend(1.40), z0=HZ + 0.07, z1=HZ + ZH - 0.07,
                     d=0.20, fill="#17130F", gold=True))
slide(
    4, az=137, shmul=1.10, late=0.32, coord="61 deg 13'N 149 deg 54'W",
    cfg_extra=dict(wells=s4_wells),
    dom=f"""
<div class="z kicker">The same record, the same depth</div>
<h1 class="display" style="width:830px;font-size:64px;font-variation-settings:'SOFT' 60,'WONK' 0,'opsz' 96;font-weight:750;line-height:1.06"
    data-fit='{{"min":48,"max":64,"maxLines":4}}'>"Most of our national donors, I think, actually, their only agenda is, 'can you win?'"</h1>
<div class="lab dk sm" style="left:80px;top:452px">Kreiss-Tomkins to the Anchorage Daily News, July 2026</div>
<div class="chip" style="left:80px;top:502px;width:900px">No wrongdoing is alleged in this reporting</div>
""" + "".join(
    L(wend(m), Z0 + i * (ZH + ZG) + ZH / 2, 20, -22, cls="lab dk sm", txt=nm)
    for i, (nm, m) in enumerate(ROWS)
) + """<div class="z base">Heilala reported nearly 1.6 million dollars, more than 1.4 million of it his own, which is more than all six Anthropic employees gave.</div>
""")

# =============================================================== SLIDE 05 ====
# a rack of four slots. Three are filled by somebody else's decision, proud of
# our stone. The fourth is dashed and empty: no award has been announced.
TABS = [("JBER", -0.86), ("Eielson AFB", -0.44), ("Clear SFS", -0.02)]
slide(
    5, az=144, shmul=1.40, late=0.38, coord="64 deg 40'N 147 deg 06'W",
    cfg_extra=dict(
        tabs=[dict(x0=-1.40, x1=0.16, z0=z, z1=z + 0.28) for _n, z in TABS],
        scored=[dict(x0=-1.40, x1=0.16, z0=0.40, z1=0.68, phantom=True)],
    ),
    extra_js=r"""
function afterGrade(cx) {
  /* the slide's one motivated gold glint, on the empty slot's near lip, so the
     specular carrier is present on all ten slides as the deck header claims */
  const A = PX(-1.40, 0.68), Ay = PY(-1.40, 0, 0.68);
  const B = PX(-0.86, 0.68), By = PY(-0.86, 0, 0.68);
  cx.save(); cx.strokeStyle = '#FFC72C'; cx.lineWidth = 2.2; cx.globalAlpha = 0.85;
  cx.beginPath(); cx.moveTo(A, Ay); cx.lineTo(B, By); cx.stroke(); cx.restore();
}
""",
    dom=f"""
<div class="z kicker">What is already in motion</div>
<h1 class="display" style="width:800px;font-size:84px;font-variation-settings:'SOFT' 60,'WONK' 0,'opsz' 96;font-weight:800;line-height:1.02"
    data-fit='{{"min":62,"max":84,"maxLines":3}}'>About 4,700 acres at three Alaska bases, offered for AI data centers.</h1>
<div class="chip" style="left:80px;top:470px;width:430px">Background, federal solicitation</div>
<div class="chip" style="left:550px;top:470px;width:430px">Aug 18 primary per news reporting, not the Division of Elections</div>
""" + "".join(L(0.16, z + 0.14, 22, -16, txt=n) for n, z in TABS)
  + L(0.16, 0.54, 22, -30, txt="Award")
  + L(0.16, 0.54, 22, -2, txt="Not announced")
  + """<div class="z base">Offers were due June 29 2026. No award has been announced. The next governor inherits this already in motion.</div>
""")

# =============================================================== SLIDE 06 ====
slide(
    6, az=151, shmul=1.72, late=0.44, mode="gl", coord="58 deg 18'N 134 deg 25'W",
    cfg_extra=dict(wells=[], scored=[]),
    extra_js=r"""
function extraArt(cx) {
  /* one fireweed inlay on the CUT bay's floor. Fireweed has meant the compulsory
     record since the cover, so the bay labelled COMPELLED BY LAW must carry it. */
  cx.save();
  quad(cx, face(-1.40, -0.06, -0.62, 0.62, 0)); cx.clip();
  quad(cx, face(-1.30, -0.72, -0.30, -0.10, -0.255), P.fireweed);
  cx.restore();
  /* the SCORED right bay, ruled and never cut. No interior colour of any kind. */
  cx.save();
  cx.strokeStyle = mix(P.body, P.ink, 0.35); cx.lineWidth = 2.4;
  cx.setLineDash([26, 6, 5, 6]);
  quad(cx, face(0.06, 1.40, -0.62, 0.62, 0)); cx.stroke();
  cx.setLineDash([]);
  /* crop-mark corner Ls: a line somebody ruled and never followed */
  const C = face(0.06, 1.40, -0.62, 0.62, 0);
  cx.lineWidth = 2.4; cx.globalAlpha = 0.9;
  C.forEach((q, i) => {
    const n = C[(i + 1) % 4], pv = C[(i + 3) % 4];
    const ux = (n[0] - q[0]) * 0.10, uy = (n[1] - q[1]) * 0.10;
    const vx = (pv[0] - q[0]) * 0.10, vy = (pv[1] - q[1]) * 0.10;
    cx.beginPath(); cx.moveTo(q[0] + ux, q[1] + uy); cx.lineTo(q[0], q[1]);
    cx.lineTo(q[0] + vx, q[1] + vy); cx.stroke();
  });
  cx.restore();
}
""",
    dom=f"""
<div class="z kicker">The asymmetry</div>
<h1 class="display" style="width:890px;font-size:96px"
    data-fit='{{"min":70,"max":96,"maxLines":3}}'>Alaska requires the money on the record. It does not require the policy.</h1>
""" + L(-1.40, 0.62, 4, 16, cls="lab dk", txt="On file")
      + L(-1.40, 0.62, 4, 46, txt="Compelled by law")
      + L(0.06, 0.62, 6, 52, cls="lab dk", txt="AI policy")
      + L(0.06, 0.62, 6, 82, txt="Voluntary")
      + """<div class="z base">Every number in this deck exists because a law required it. Nothing required any of the 17 candidates to state a position on AI.</div>
""")

# =============================================================== SLIDE 07 ====
BLANKS = [("Bernadette Wilson", None), ("Treg Taylor", 1.00),
          ("Adam Crum", 0.94), ("Meda DeWitt", None)]
ANSWERS = [("Gilbert, refuses AI outright",), ("DeVries, used AI to answer",)]
Z7, ZH7, ZG7 = -1.03, 0.26, 0.10
s7_scored, s7_wells = [], []
for i, (nm, money) in enumerate(BLANKS):
    z = Z7 + i * (ZH7 + ZG7)
    s7_scored.append(dict(x0=-1.34, x1=-0.60, z0=z, z1=z + ZH7, dot=True))
    if money:
        s7_wells.append(dict(x0=-0.50, x1=-0.50 + money * W_PER_M, z0=z + 0.04,
                             z1=z + ZH7 - 0.05, d=0.09, gold=True))
for i, (t,) in enumerate(ANSWERS):
    z = Z7 + (4 + i) * (ZH7 + ZG7)
    s7_wells.append(dict(x0=-1.34, x1=-0.30, z0=z, z1=z + ZH7, d=0.05,
                         fill="#4A4038"))
slide(
    7, az=158, shmul=2.02, late=0.50, coord="61 deg 34'N 149 deg 15'W",
    cfg_extra=dict(wells=s7_wells, scored=s7_scored),
    dom=f"""
<div class="z kicker">Named answers and named blanks</div>
<h1 class="display" style="width:890px;font-size:76px;font-variation-settings:'SOFT' 60,'WONK' 0,'opsz' 96;font-weight:800;line-height:1.02"
    data-fit='{{"min":54,"max":76,"maxLines":2}}'>Four candidates did not answer. Two raised about a million each.</h1>
<div class="chip" style="left:80px;top:400px;width:900px">Not a count of the field. The named answers and non answers in one June 2026 survey.</div>
<div class="chip" style="left:80px;top:486px;width:900px">Background, Northern Journal, June 2026</div>
""" + "".join(
    L(-1.34, Z7 + i * (ZH7 + ZG7), 8, -40, txt=nm)
    for i, (nm, money) in enumerate(BLANKS)
) + "".join(
    L(-0.50 + money * W_PER_M, Z7 + i * (ZH7 + ZG7) + ZH7 / 2, 34, -16,
      txt="1.0 M on file" if money == 1.00 else "940,000 on file")
    for i, (nm, money) in enumerate(BLANKS) if money
) + "".join(
    L(-0.30, Z7 + (4 + i) * (ZH7 + ZG7) + ZH7 / 2, 20, -16, cls="lab dk sm", txt=t)
    for i, (t,) in enumerate(ANSWERS)
) + """<div class="z base">Others did answer, and two of those answers are shown. Not answering a reporter is not misconduct, it is a missing answer.</div>
""")

# =============================================================== SLIDE 08 ====
RULES = ["Liability for harms", "A deepfake ban", "AI disclosed in political ads",
         "An AI fraud crackdown", "Children protected from AI", "A human behind state decisions"]
Z8, ZH8, ZG8 = -1.03, 0.20, 0.145
s8_wells = [dict(x0=-1.44, x1=-1.14, z0=Z8 + i * (ZH8 + ZG8),
                 z1=Z8 + i * (ZH8 + ZG8) + ZH8, d=0.09, fw=True, fwx1=-1.16)
            for i in range(6)]
s8_scored = [dict(x0=1.06, x1=1.50, z0=Z8 + i * (ZH8 + ZG8),
                  z1=Z8 + i * (ZH8 + ZG8) + ZH8) for i in range(6)]
slide(
    8, az=165, shmul=2.28, late=0.56, coord="61 deg 13'N 149 deg 54'W",
    cfg_extra=dict(wells=s8_wells, scored=s8_scored),
    extra_js=r"""
function extraArt(cx) {
  /* the YOUR CANDIDATE column runs off the right frame edge, unfinished. The
     thing left unfinished is the reader's job. */
  cx.save();
  cx.strokeStyle = P.hair; cx.lineWidth = 1.25;
  for (let i = 0; i < 6; i++) {
    const z = -1.03 + i * 0.345 + 0.10;
    cx.beginPath(); cx.moveTo(PX(1.50, z), PY(1.50, 0, z));
    cx.lineTo(1080, PY(1.50, 0, z) + 8); cx.stroke();
  }
  cx.restore();
}
""",
    dom=f"""
<div class="z kicker">The sheet</div>
<h1 class="display" style="width:860px;font-size:76px;font-variation-settings:'SOFT' 60,'WONK' 0,'opsz' 96;font-weight:800;line-height:1.02"
    data-fit='{{"min":58,"max":76,"maxLines":2}}'>Six AI rules one candidate has proposed. Six blanks for yours.</h1>
<div class="navychip" style="left:700px;top:384px">AUG 18 2026</div>
<div class="chip" style="left:80px;top:466px;width:400px">On the record</div>
<div class="chip" style="left:620px;top:466px;width:360px">Your candidate</div>
""" + "".join(
    f"""<div style="position:absolute;left:{sx(-1.10, Z8 + i * (ZH8 + ZG8) + ZH8 / 2) + 8:.0f}px;top:{sy(-1.10, 0, Z8 + i * (ZH8 + ZG8) + ZH8 / 2) - 22:.0f}px;font-family:'Bricolage Grotesque';font-weight:600;font-size:32px;color:{P['ink']};white-space:nowrap;letter-spacing:.005em">{r}</div>\n"""
    for i, r in enumerate(RULES)
) + """<div class="lab dk sm" style="left:80px;top:1150px">Source, Alaska Public Media, July 24 2026</div>
<div class="z base">These six are one candidate's stated positions, not law. Ask any of the 17 candidates the same six questions before August 18.</div>
""")

# =============================================================== SLIDE 09 ====
slide(
    9, az=172, shmul=2.48, late=0.60, coord="58 deg 18'N 134 deg 25'W",
    cfg_extra=dict(
        wells=[dict(x0=-1.42, x1=-0.10, z0=-0.30, z1=0.34, d=0.16, fill="#EDE6D8"),
               dict(x0=0.10, x1=1.42, z0=-0.30, z1=0.34, d=0.16, fill="#EDE6D8")],
    ),
    extra_js=r"""
function extraArt(cx) {
  /* fireweed inlay border on the CONFLICT pocket only. Fireweed has meant the
     compulsory record all deck, so the studio files its own conflict WITH
     everything else rather than footnoting it beneath. Drawn on the pocket's own
     rim polygon so it can never read as a crooked sticker. */
  cx.save();
  cx.strokeStyle = P.fireweed; cx.lineWidth = 3.5;
  quad(cx, face(0.14, 1.38, -0.26, 0.30, -0.16)); cx.stroke();
  cx.restore();
  /* scotch rule under each pocket head */
  [[-1.42, -0.10], [0.10, 1.42]].forEach(([a, b]) => {
    const A = PX(a + 0.05, -0.18), Ay = PY(a + 0.05, -0.16, -0.18);
    const B = PX(b - 0.05, -0.18), By = PY(b - 0.05, -0.16, -0.18);
    cx.save(); cx.strokeStyle = P.hair; cx.lineWidth = 1.25;
    cx.beginPath(); cx.moveTo(A, Ay + 34); cx.lineTo(B, By + 34); cx.stroke();
    cx.restore();
  });
}
function afterGrade(cx) {
  /* the gold Polaris in the seam, after the grade so the flag gold stays #FFC72C */
  cx.save(); cx.translate(PX(0, 0.02), PY(0, 0, 0.02));
  cx.beginPath();
  for (let i = 0; i < 8; i++) {
    const ang = i * Math.PI / 4, r = (i % 2 === 0) ? 23 : 6.9;
    i ? cx.lineTo(Math.sin(ang) * r, -Math.cos(ang) * r)
      : cx.moveTo(Math.sin(ang) * r, -Math.cos(ang) * r);
  }
  cx.closePath(); cx.fillStyle = '#FFC72C'; cx.fill();
  cx.strokeStyle = P.ink; cx.lineWidth = 1.5; cx.stroke();
  cx.restore();
}
""",
    dom=f"""
<h1 class="display" style="top:150px;width:890px;font-size:96px"
    data-fit='{{"min":72,"max":96,"maxLines":1}}'>Who is telling you this.</h1>
<div style="position:absolute;left:80px;top:300px;width:420px;font-family:'Bricolage Grotesque';font-weight:400;font-size:30px;line-height:1.36;color:{P['body']}">One article by one reporter, published July 23 2026 by the Anchorage Daily News and republished July 24 by Alaska Public Media. One reporting source, not two. The candidate AI positions come from a separate June questionnaire and are labelled background.</div>
<div style="position:absolute;left:560px;top:300px;width:420px;font-family:'Bricolage Grotesque';font-weight:400;font-size:30px;line-height:1.36;color:{P['body']}">This deck was made with a Claude model built by Anthropic. Six Anthropic employees are the donors in this story. No source reports any donor's motive. This deck claims no causation, and no wrongdoing has been alleged in this reporting.</div>
<div class="lab dk" style="left:{sx(-1.37, -0.24) + 8:.0f}px;top:{sy(-1.37, -0.16, -0.24) + 4:.0f}px">The sourcing</div>
<div class="lab dk" style="left:{sx(0.15, -0.24) + 8:.0f}px;top:{sy(0.15, -0.16, -0.24) + 4:.0f}px">The conflict</div>
<div class="basemono">This disclosure also rides in the first comment.</div>
""")

# =============================================================== SLIDE 10 ====
slide(
    10, az=179, shmul=2.61, late=0.64, coord="58 deg 18'N 134 deg 25'W",
    cfg_extra=dict(
        wells=[dict(x0=-1.48, x1=1.48, z0=0.56, z1=0.76, d=0.10, gold=True)],
    ),
    extra_js=r"""
function afterGrade(cx) {
  /* the gold Polaris beside the wordmark, after the grade and inside the margin */
  cx.save(); cx.translate(262, 1300);
  cx.beginPath();
  for (let i = 0; i < 8; i++) {
    const ang = i * Math.PI / 4, r = (i % 2 === 0) ? 15 : 4.5;
    i ? cx.lineTo(Math.sin(ang) * r, -Math.cos(ang) * r)
      : cx.moveTo(Math.sin(ang) * r, -Math.cos(ang) * r);
  }
  cx.closePath(); cx.fillStyle = P.gold; cx.fill();
  cx.strokeStyle = P.ink; cx.lineWidth = 1.25; cx.stroke();
  cx.restore();
}
""",
    dom=f"""
<h1 class="display" style="width:880px;font-size:96px"
    data-fit='{{"min":72,"max":96,"maxLines":2}}'>Save slide 08. Take it to a candidate before August 18.</h1>
<div class="navychip" style="left:80px;top:470px">AUG 18 2026</div>
<div class="site" data-decorative style="left:300px;top:1292px">alaskaaihq.com</div>
<!-- coordinates omitted on the close: the brand block owns this row -->
<div class="basemono">Sources in comments</div>
""")

# ------------------------------------------------------------------ write ----
for n, html in SLIDES:
    (OUT / f"slide-{n:02d}.html").write_text(html)
print(f"wrote {len(SLIDES)} slides to {OUT}")
