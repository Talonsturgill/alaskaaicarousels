/* akpillar.js — THE PRICE AS LIGHT, Carousel No.112's shared furniture (2026-11-11).
 *
 * DNR's Final Finding and Decision on ADL 422741 (STAK Energy, November 10th)
 * prices the lease with a five-tier Compute Power Sales Surcharge. This deck
 * draws that schedule as five Arctic light pillars standing over the empty
 * tundra west of the Dalton at Milepost 390: a pillar's WIDTH is the MWh inside
 * its tier and its HEIGHT is the rate, always on one frontal plane so the
 * ratios survive (perspective is never applied to the quantities).
 *
 * Deck furniture only, shared on purpose and kept in a module so bespoke_check
 * strips it as harness: the palette, the tier table, the deck scale, the
 * fixtures, and the way a pillar of light is built. Every slide composes its
 * own scene in its own file.
 *
 *   AKP.PAL                     the deck palette (storyboard PALETTE)
 *   AKP.TIERS                   the schedule, C22 to C26, marginal (C27)
 *   AKP.SCALE                   44 px per million MWh, 10 px per cent, x0 84
 *   AKP.edges(scale)            the tier edges in px for a scale {x0, pxPerM}
 *   AKP.fixtures(n, o)          wordmark + Polaris, counter, site, MP 390 stamp
 *   AKP.pillar(cx, o)           one pillar of light: halo, body, crystal streaks
 *   AKP.pool(cx, o)             its pool and reflection on the snow below
 *   AKP.cap(cx, o)              the gold cap hairline (call AFTER the grade)
 *   AKP.polarisPath(cx,x,y,r)   the 4-point star as a canvas path
 *
 * Gold #FFC72C means the lease and its price, nowhere else. Classic script,
 * global AKP; load after noise.js.
 */
(function (global) {
  "use strict";
  const AKP = {};

  AKP.PAL = {
    zenith: "#0B1A3A", upper: "#18305E", band: "#2B3F6E", rose: "#C79A9E",
    pale: "#E3D3CB", snowLit: "#CFDAEC", snowMid: "#8E9FC0", snowLee: "#4C5E86",
    snowDeep: "#26355A", nightGround: "#030710", nightSky: "#050C1C",
    ice: "#BFE3F2", fringe: "#5AC8F0", glint: "#F4F8FF", fmn: "#6EA5FF",
    aurora: "#3CE6B4", text: "#F4F8FF", body: "#C4CFDF", label: "#A9B8CC",
    site: "#5E6E86", gold: "#FFC72C", goldHalo: "#FFDA6E"
  };

  /* The schedule exactly as the decision prints it (C22 to C26). mwh0/mwh1 are
   * the tier's band in MWh per lease year, mw0/mw1 DNR's equivalent average
   * compute load, rate dollars per MWh. Marginal: each rate applies only to the
   * MWh inside its own tier (C27). */
  AKP.TIERS = [
    { n: 1, mwh0: 0,        mwh1: 876000,   mw0: 0,    mw1: 100,  rate: 0.00 },
    { n: 2, mwh0: 876000,   mwh1: 4380000,  mw0: 100,  mw1: 500,  rate: 0.20 },
    { n: 3, mwh0: 4380000,  mwh1: 8760000,  mw0: 500,  mw1: 1000, rate: 0.40 },
    { n: 4, mwh0: 8760000,  mwh1: 13140000, mw0: 1000, mw1: 1500, rate: 0.30 },
    { n: 5, mwh0: 13140000, mwh1: 20699880, mw0: 1500, mw1: 2363, rate: 0.16 }
  ];
  AKP.ALASKA_2024_MWH = 6690506;   /* C55 */

  AKP.SCALE = { x0: 84, pxPerM: 44, pxPerCent: 10 };

  AKP.edges = function (s) {
    s = s || AKP.SCALE;
    return AKP.TIERS.map(t => ({
      n: t.n, rate: t.rate,
      x0: s.x0 + t.mwh0 / 1e6 * s.pxPerM,
      x1: s.x0 + t.mwh1 / 1e6 * s.pxPerM,
      h: t.rate * 100 * (s.pxPerCent != null ? s.pxPerCent : AKP.SCALE.pxPerCent)
    }));
  };

  function rgb(h) {
    const v = parseInt(h.slice(1), 16);
    return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
  }
  function rgba(h, a) { const c = rgb(h); return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")"; }
  AKP.rgba = rgba;

  /* The Polaris: a 4-point star with a slim waist, the house glyph. */
  AKP.polarisPath = function (cx, x, y, r) {
    const w = r * 0.22;
    cx.moveTo(x, y - r);
    cx.quadraticCurveTo(x + w * 0.5, y - w * 0.5, x + r, y);
    cx.quadraticCurveTo(x + w * 0.5, y + w * 0.5, x, y + r);
    cx.quadraticCurveTo(x - w * 0.5, y + w * 0.5, x - r, y);
    cx.quadraticCurveTo(x - w * 0.5, y - w * 0.5, x, y - r);
    cx.closePath();
  };
  function polarisSVG(size, color) {
    const r = size / 2, w = r * 0.22, c = r;
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '" aria-hidden="true">' +
      '<path fill="' + color + '" d="M' + c + ' 0 Q' + (c + w * 0.5) + ' ' + (c - w * 0.5) + ' ' + size + ' ' + c +
      ' Q' + (c + w * 0.5) + ' ' + (c + w * 0.5) + ' ' + c + ' ' + size +
      ' Q' + (c - w * 0.5) + ' ' + (c + w * 0.5) + ' 0 ' + c +
      ' Q' + (c - w * 0.5) + ' ' + (c - w * 0.5) + ' ' + c + ' 0Z"/></svg>';
  }

  /* Fixtures on every frame. Everything is positioned and z-indexed ABOVE any
   * art canvas (SKILL.md: an element appended after a z-indexed canvas paints
   * under it otherwise). o.big puts the large wordmark on the close. */
  AKP.fixtures = function (n, o) {
    o = o || {};
    const d = document;
    const css = d.createElement("style");
    css.textContent =
      ".akp-fx{position:absolute;z-index:20;font-family:'JetBrains Mono',monospace;font-weight:500;letter-spacing:0.06em}" +
      ".akp-wm{left:80px;top:80px;display:flex;align-items:center;gap:12px;font-family:'Space Grotesk',sans-serif;" +
      "font-weight:700;font-size:26px;letter-spacing:0.08em;color:" + AKP.PAL.text + "}" +
      ".akp-ct{right:80px;top:84px;font-size:22px;color:" + AKP.PAL.label + "}" +
      ".akp-site{left:80px;bottom:44px;font-size:20px;color:" + AKP.PAL.site + "}" +
      ".akp-loc{right:80px;bottom:44px;font-size:20px;color:" + AKP.PAL.site + "}" +
      ".akp-big{left:80px;bottom:110px;display:flex;align-items:center;gap:18px;font-family:'Space Grotesk',sans-serif;" +
      "font-weight:700;font-size:44px;letter-spacing:0.08em;color:" + AKP.PAL.text + "}";
    d.head.appendChild(css);
    const add = (cls, html, deco) => {
      const e = d.createElement("div");
      e.className = "akp-fx " + cls;
      if (deco) e.setAttribute("data-decorative", "");
      e.innerHTML = html;
      d.body.appendChild(e);
      return e;
    };
    if (!o.big) add("akp-wm", polarisSVG(26, AKP.PAL.gold) + "<span>ALASKA.AI</span>");
    add("akp-ct", String(n).padStart(2, "0") + " / 09", true);
    add("akp-site", "alaskaaihq.com", true);
    add("akp-loc", "DALTON HWY MP 390", true);
    if (o.big) add("akp-big", polarisSVG(40, AKP.PAL.gold) + "<span>ALASKA.AI</span>");
  };

  /* One pillar of light. (x, base) is the bottom-left of the data rectangle in
   * design px, w and h its size. The data edge is a hard hairline; the halo
   * lives OUTSIDE it and the body fades upward past the cap so the column reads
   * as light, not as a filled bar. The cap itself is gold and is drawn by
   * AKP.cap after the grade. h may be 0 (Tier 1): then a lit line only. */
  AKP.pillar = function (cx, o) {
    const x = o.x, b = o.base, w = o.w, h = o.h;
    const a = o.alpha == null ? 1 : o.alpha;
    if (!(global.AK && AK.rng)) throw new Error("AKP.pillar: load noise.js first (seeded streaks)");
    const rnd = AK.rng(o.seed || 1);
    const W = cx.canvas.width, H = cx.canvas.height;
    const sc = W / (o.designW || 1080);
    cx.save();
    cx.globalCompositeOperation = "lighter";
    if (h <= 0.5) {
      /* the zero-height pillar: a line of light lying on the ground */
      const g = cx.createLinearGradient(0, b - 10, 0, b + 10);
      g.addColorStop(0, rgba(AKP.PAL.ice, 0));
      g.addColorStop(0.5, rgba(AKP.PAL.ice, 0.55 * a));
      g.addColorStop(1, rgba(AKP.PAL.ice, 0));
      cx.fillStyle = g; cx.fillRect(x - 4, b - 10, w + 8, 20);
      cx.fillStyle = rgba(AKP.PAL.glint, 0.9 * a); cx.fillRect(x, b - 1.2, w, 2.4);
      cx.restore();
      return;
    }
    /* halo: an offscreen blur so it falls off softly on every side */
    const pad = Math.max(28, w * 0.35);
    const off = document.createElement("canvas");
    off.width = Math.ceil((w + pad * 2) * sc); off.height = Math.ceil((h * 1.35 + pad * 2) * sc);
    const oc = off.getContext("2d");
    oc.scale(sc, sc);
    oc.filter = "blur(" + (o.haloBlur || 16) * sc + "px)";
    const hg = oc.createLinearGradient(0, pad + h * 1.35, 0, pad);
    hg.addColorStop(0, rgba(AKP.PAL.fringe, 0.26));
    hg.addColorStop(0.6, rgba(AKP.PAL.fringe, 0.16));
    hg.addColorStop(1, rgba(AKP.PAL.fringe, 0));
    oc.fillStyle = hg;
    oc.fillRect(pad - 6, pad, w + 12, h * 1.35);
    cx.globalAlpha = 0.55 * a;
    cx.drawImage(off, 0, 0, off.width, off.height, x - pad, b - h * 1.35 - pad, off.width / sc, off.height / sc);
    cx.globalAlpha = 1;
    /* body: vertical gradient, brightest at the base, through the cap */
    const bg = cx.createLinearGradient(0, b, 0, b - h * 1.18);
    bg.addColorStop(0, rgba(AKP.PAL.ice, 0.34 * a));
    bg.addColorStop(0.55, rgba(AKP.PAL.ice, 0.26 * a));
    bg.addColorStop(0.85, rgba(AKP.PAL.ice, 0.18 * a));
    bg.addColorStop(1, rgba(AKP.PAL.ice, 0));
    cx.fillStyle = bg;
    cx.fillRect(x, b - h * 1.18, w, h * 1.18);
    /* the soft edge falloff across the column (plate crystals bunch to the axis) */
    const sg = cx.createLinearGradient(x, 0, x + w, 0);
    sg.addColorStop(0, rgba(AKP.PAL.ice, 0));
    sg.addColorStop(0.5, rgba(AKP.PAL.ice, 0.16 * a));
    sg.addColorStop(1, rgba(AKP.PAL.ice, 0));
    cx.fillStyle = sg;
    cx.fillRect(x, b - h, w, h);
    /* crystal streaks: thin vertical glints of uneven length */
    const nS = o.streaks != null ? o.streaks : Math.max(6, Math.round(w / 5));
    for (let i = 0; i < nS; i++) {
      const sx = x + 2 + rnd() * (w - 4);
      const len = h * (0.25 + rnd() * 0.85);
      const sy = b - rnd() * (h - len * 0.5);
      const lg = cx.createLinearGradient(0, sy, 0, sy - len);
      const al = (0.10 + rnd() * 0.18) * a;
      lg.addColorStop(0, rgba(AKP.PAL.glint, 0));
      lg.addColorStop(0.5, rgba(AKP.PAL.glint, al));
      lg.addColorStop(1, rgba(AKP.PAL.glint, 0));
      cx.fillStyle = lg;
      cx.fillRect(sx, sy - len, 0.7 + rnd() * 0.6, len);
    }
    /* data edges: hairlines on the two sides, faint, so the width is exact */
    cx.fillStyle = rgba(AKP.PAL.glint, 0.38 * a);
    cx.fillRect(x, b - h, 1, h);
    cx.fillRect(x + w - 1, b - h, 1, h);
    cx.restore();
  };

  /* Pool on the snow under a pillar, and its soft reflection. (x, base, w) as
   * the pillar; depth px how far the pool spreads toward the viewer. */
  AKP.pool = function (cx, o) {
    const x = o.x, b = o.base, w = o.w;
    const a = o.alpha == null ? 1 : o.alpha;
    const depth = o.depth || 60, spread = o.spread || 1.6;
    cx.save();
    cx.globalCompositeOperation = "lighter";
    const cxm = x + w / 2, R = 100;
    cx.translate(cxm, b + depth * 0.18);
    cx.scale((w * spread) / (2 * R), depth / R);
    const g = cx.createRadialGradient(0, 0, 0, 0, 0, R);
    g.addColorStop(0, rgba(AKP.PAL.ice, 0.14 * a));
    g.addColorStop(0.45, rgba(AKP.PAL.ice, 0.12 * a));
    g.addColorStop(1, rgba(AKP.PAL.ice, 0));
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(0, 0, R, 0, Math.PI * 2); cx.fill();
    cx.restore();
    if (o.reflect !== false && o.h > 0) {
      cx.save();
      cx.globalCompositeOperation = "lighter";
      const rl = Math.min(o.h * 0.7, depth * 1.6);
      const rg = cx.createLinearGradient(0, b, 0, b + rl);
      rg.addColorStop(0, rgba(AKP.PAL.ice, 0.14 * a));
      rg.addColorStop(1, rgba(AKP.PAL.ice, 0));
      cx.fillStyle = rg;
      cx.fillRect(x + w * 0.12, b, w * 0.76, rl);
      cx.restore();
    }
  };

  /* The gold cap: the lease's price, a hairline on the data top. AFTER the grade. */
  AKP.cap = function (cx, o) {
    if (o.h <= 0.5) return;
    cx.save();
    cx.fillStyle = AKP.PAL.gold;
    cx.fillRect(o.x, o.base - o.h - (o.t || 2) / 2, o.w, o.t || 2);
    cx.restore();
  };

  /* AKP.march(cx, o): a per-device-pixel COLUMN MARCH of a heightfield (the
   * voxel-space method): for each device column, a ray walks out over the
   * ground at geometric steps, each step's projected top fills the column
   * upward from the last, shaded from the landform normal under one key and a
   * hemisphere fill, with exp2 fog to the horizon colour. Deterministic.
   *   o.height(x, z)  metres, the camera looks along -z (yaw turns it west)
   *   o.camH metres above the ground at the camera, o.horizonY design px,
   *   o.fov vertical degrees, o.near/o.far metres, o.yaw degrees,
   *   o.key {az, el, color [r,g,b] 0..1, i}, o.sky [r,g,b], o.ground [r,g,b],
   *   o.hemi, o.albedo(x, z) -> [r,g,b] 0..1, o.fog [r,g,b], o.fogD,
   *   o.y0 the top device row it may paint (the sky above stays untouched).
   * Writes ImageData at the device pixel under an identity transform. */
  AKP.march = function (cx, o) {
    const W = cx.canvas.width, Hh = cx.canvas.height;
    const sc = W / 1080;
    const img = cx.getImageData(0, 0, W, Hh), D = img.data;
    const f = (Hh / 2) / Math.tan(o.fov * Math.PI / 360);
    const hy = o.horizonY * sc;
    const yaw = (o.yaw || 0) * Math.PI / 180;
    const ka = (o.key.az) * Math.PI / 180, ke = o.key.el * Math.PI / 180;
    const L = [Math.sin(ka) * Math.cos(ke), Math.sin(ke), Math.cos(ka) * Math.cos(ke)];   /* x east, y up, z north */
    const near = o.near || 0.8, far = o.far || 4000, steps = o.steps || 900;
    const gamma = 1 / 2.2;
    const camY = o.height(0, 0) + o.camH;
    for (let col = 0; col < W; col++) {
      const sx = (col + 0.5 - W / 2) / f;                         /* screen x over focal */
      let yb = Hh;                                                  /* lowest unfilled row + 1 */
      for (let k = 0; k < steps && yb > (o.y0 || 0) * sc; k++) {
        const d = near * Math.pow(far / near, k / (steps - 1));
        const lx = sx * d, lz = -d;
        const x = lx * Math.cos(yaw) + lz * Math.sin(yaw), z = -lx * Math.sin(yaw) + lz * Math.cos(yaw);
        const h = o.height(x, z);
        const y = hy + (camY - h) / d * f;
        if (y >= yb) continue;
        const e = Math.max(0.02, d * 0.004);
        const hx = (o.height(x + e, z) - o.height(x - e, z)) / (2 * e);
        const hz = (o.height(x, z + e) - o.height(x, z - e)) / (2 * e);
        let nx = -hx, ny = 1, nz = -hz; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
        const lam = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
        const up = ny * 0.5 + 0.5;
        const al = o.albedo ? o.albedo(x, z, d) : [0.85, 0.89, 0.95];
        const fg = 1 - Math.exp(-Math.pow(d * o.fogD, 2));
        const c = [0, 1, 2].map(i => {
          const lin = al[i] * (o.key.color[i] * o.key.i * lam + o.hemi * (o.sky[i] * up + o.ground[i] * (1 - up)));
          const tm = lin / (1 + lin);                                 /* soft rolloff */
          return Math.pow(tm, gamma) * (1 - fg) + o.fog[i] * fg;
        });
        const top = Math.max(Math.floor(y), 0);
        for (let r = top; r < yb; r++) {
          const p = (r * W + col) * 4;
          D[p] = c[0] * 255; D[p + 1] = c[1] * 255; D[p + 2] = c[2] * 255; D[p + 3] = 255;
        }
        yb = top;
      }
    }
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); cx.putImageData(img, 0, 0); cx.restore();
  };

  global.AKP = AKP;
})(typeof window !== "undefined" ? window : this);
