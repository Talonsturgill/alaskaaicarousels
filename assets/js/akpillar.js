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
      ".akp-site{left:80px;bottom:44px;font-size:20px;color:#8292AE;text-shadow:0 0 4px rgba(5,10,24,0.9),0 0 2px rgba(5,10,24,0.9)}" +
      ".akp-loc{right:80px;bottom:44px;font-size:20px;color:#8292AE;text-shadow:0 0 4px rgba(5,10,24,0.9),0 0 2px rgba(5,10,24,0.9)}" +
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
      /* the zero-height pillar: a thin line of light lying on the ground, its glow scaled to its
       * own width so a 15 px Tier 1 on a far plane is a glint and never a sprite */
      const gh = Math.max(3, Math.min(10, w * 0.12)), core = Math.max(0.8, Math.min(2.4, w * 0.04));
      const lg2 = cx.createLinearGradient(x, 0, x + w, 0);
      lg2.addColorStop(0, rgba(AKP.PAL.glint, 0)); lg2.addColorStop(0.12, rgba(AKP.PAL.glint, 0.85 * a));
      lg2.addColorStop(0.88, rgba(AKP.PAL.glint, 0.85 * a)); lg2.addColorStop(1, rgba(AKP.PAL.glint, 0));
      const g = cx.createLinearGradient(0, b - gh, 0, b + gh);
      g.addColorStop(0, rgba(AKP.PAL.ice, 0));
      g.addColorStop(0.5, rgba(AKP.PAL.ice, 0.40 * a));
      g.addColorStop(1, rgba(AKP.PAL.ice, 0));
      cx.fillStyle = g; cx.fillRect(x, b - gh, w, gh * 2);
      cx.fillStyle = lg2; cx.fillRect(x, b - core / 2, w, core);
      cx.restore();
      return;
    }
    /* halo: an offscreen blur so it falls off softly on every side */
    const pad = Math.max(40, w * 0.4, (o.haloBlur || 16) * 5);
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
    /* the column fades out above its cap at a height that varies across it (seeded), so the top
     * of the light is ragged like real crystal pillars and never a flat ceiling */
    const strip = Math.max(2, w / 48);
    /* the ragged top is bounded to 30 design px whatever the height, and its noise is low frequency,
     * so a tall pillar's crown reads as crystal light thinning out and never as an equalizer spike */
    const rag = Math.min(0.22, 30 / Math.max(1, h));
    /* footFade (px): the body fades to nothing over its last px at the base so it ends IN its pool on
     * snow and never as a pale rectangle; baseA caps the brightest stop so a pillar over a lit horizon
     * belt can't add up to a white slab under 'lighter' */
    const ff = Math.min(h * 0.3, o.footFade || 0), ba = o.baseA == null ? 0.30 : o.baseA;
    /* the strips are painted source-over on their own canvas and composited ONCE, because adjacent
     * strips overlapping by a sub-pixel under 'lighter' doubled the alpha at every seam and printed a
     * regular comb of pinstripes down every body (No.112, three critics) */
    const kMax = 1.03 + rag, bh = h * kMax;
    const bc = document.createElement("canvas");
    bc.width = Math.ceil((w + 2) * sc); bc.height = Math.ceil((bh + 2) * sc);
    const bx = bc.getContext("2d");
    bx.scale(sc, sc);
    for (let sx = 0; sx < w; sx += strip) {
      const k = 1.03 + rag * (0.5 + 0.5 * AK.simplex2((x + sx) * 0.012, (o.seed || 1) * 0.37));
      const top = bh - h * k;
      const cg = bx.createLinearGradient(0, bh, 0, top);
      const edge = Math.min(1, Math.min(sx, w - sx) / Math.max(6, w * 0.14));   /* lateral feather */
      const m = a * (0.35 + 0.65 * edge);
      cg.addColorStop(0, rgba(AKP.PAL.ice, ff > 0 ? 0 : ba * m));
      if (ff > 0) cg.addColorStop(Math.min(0.5, ff / (h * k)), rgba(AKP.PAL.ice, ba * m));
      cg.addColorStop(0.55, rgba(AKP.PAL.ice, 0.24 * m));
      cg.addColorStop(0.86, rgba(AKP.PAL.ice, 0.13 * m));
      cg.addColorStop(1, rgba(AKP.PAL.ice, 0));
      bx.fillStyle = cg;
      bx.fillRect(1 + sx, top, Math.min(strip + 0.75, w - sx), h * k);
    }
    cx.drawImage(bc, 0, 0, bc.width, bc.height, x - 1, b - bh, bc.width / sc, bc.height / sc);
    /* the soft edge falloff across the column (plate crystals bunch to the axis) */
    const sg = cx.createLinearGradient(x, 0, x + w, 0);
    sg.addColorStop(0, rgba(AKP.PAL.ice, 0));
    sg.addColorStop(0.5, rgba(AKP.PAL.ice, 0.12 * a));
    sg.addColorStop(1, rgba(AKP.PAL.ice, 0));
    cx.fillStyle = sg;
    cx.fillRect(x, b - h, w, h - ff);
    /* crystal streaks: thin vertical glints of uneven length */
    /* fewer streaks of uneven width and strength, so the body never reads as a regular comb */
    const nS = o.streaks != null ? o.streaks : Math.max(5, Math.round(w / 10));
    for (let i = 0; i < nS; i++) {
      const sx = x + 2 + rnd() * (w - 4);
      const len = h * (0.25 + rnd() * 0.85);
      const sy = b - rnd() * (h - len * 0.5);
      const lg = cx.createLinearGradient(0, sy, 0, sy - len);
      const al = (0.05 + Math.pow(rnd(), 2) * 0.24) * a;
      lg.addColorStop(0, rgba(AKP.PAL.glint, 0));
      lg.addColorStop(0.5, rgba(AKP.PAL.glint, al));
      lg.addColorStop(1, rgba(AKP.PAL.glint, 0));
      cx.fillStyle = lg;
      cx.fillRect(sx, sy - len, 0.5 + Math.pow(rnd(), 2) * 2.2, len);
    }
    /* data edges: hairlines on the two sides, faint, so the width is exact without reading as a box */
    cx.fillStyle = rgba(AKP.PAL.glint, (o.edgeA == null ? 0.12 : o.edgeA) * a);
    cx.fillRect(x, b - h, 1, h - ff);
    cx.fillRect(x + w - 1, b - h, 1, h - ff);
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
    g.addColorStop(0, rgba(AKP.PAL.ice, 0.34 * a));
    g.addColorStop(0.45, rgba('#E9D6DE', 0.14 * a));
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
    /* No.112: each step used to fill its rows with ONE flat colour, which printed a stair-step along
     * every crest (one tooth per device column) and terraces in depth. Now the rows between two
     * visible steps are interpolated between their colours, and each device column is the mean of
     * o.ss sub-columns (default 2), so ridges resolve as shaded slopes, not sawteeth. */
    const ss = Math.max(1, o.ss || 2);
    const acc = new Float32Array(W * Hh * 3), cnt = new Uint8Array(W * Hh);
    const y0 = (o.y0 || 0) * sc;
    const shade = (x, z, d) => {
      const e = Math.max(0.04, d * 0.008);   /* a wider difference low-passes the normal at range */
      const hx = (o.height(x + e, z) - o.height(x - e, z)) / (2 * e);
      const hz = (o.height(x, z + e) - o.height(x, z - e)) / (2 * e);
      let nx = -hx, ny = 1, nz = -hz; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
      const lam = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]);
      const up = ny * 0.5 + 0.5;
      const al = o.albedo ? o.albedo(x, z, d) : [0.85, 0.89, 0.95];
      const fg = 1 - Math.exp(-Math.pow(d * o.fogD, 2));
      return [0, 1, 2].map(i => {
        const lin = al[i] * (o.key.color[i] * o.key.i * lam + o.hemi * (o.sky[i] * up + o.ground[i] * (1 - up)));
        const tm = lin / (1 + lin);
        return Math.pow(tm, gamma) * (1 - fg) + o.fog[i] * fg;
      });
    };
    for (let col = 0; col < W; col++) {
      for (let k2 = 0; k2 < ss; k2++) {
        const sx = (col + (k2 + 0.5) / ss - W / 2) / f;
        let yb = Hh, cPrev = null, yPrev = Hh, wasVis = false, dPrev = near;
        for (let k = 0; k < steps && yb > y0; k++) {
          const d = near * Math.pow(far / near, k / (steps - 1));
          const lx = sx * d, lz = -d;
          const x = lx * Math.cos(yaw) + lz * Math.sin(yaw), z = -lx * Math.sin(yaw) + lz * Math.cos(yaw);
          const h = o.height(x, z);
          const y = hy + (camY - h) / d * f;
          if (y >= yb) {
            /* the step just went behind a crest: the true crest lies between the last visible step and
             * this one, and missing it is what printed a staircase along every silhouette. Bisect it. */
            if (wasVis && cPrev) {
              let best = yb;
              for (let j = 1; j <= 6; j++) {
                const dd = dPrev + (d - dPrev) * j / 7;
                const lx2 = sx * dd, lz2 = -dd;
                const x2 = lx2 * Math.cos(yaw) + lz2 * Math.sin(yaw), z2 = -lx2 * Math.sin(yaw) + lz2 * Math.cos(yaw);
                const y2 = hy + (camY - o.height(x2, z2)) / dd * f;
                if (y2 < best) best = y2;
              }
              const top2 = Math.max(Math.floor(best), 0);
              for (let r = top2; r < yb; r++) {
                const q = r * W + col, p3 = q * 3;
                acc[p3] += cPrev[0]; acc[p3 + 1] += cPrev[1]; acc[p3 + 2] += cPrev[2]; cnt[q]++;
              }
              if (top2 < yb) { yb = top2; yPrev = best; }
            }
            wasVis = false; dPrev = d;
            continue;
          }
          const c = shade(x, z, d);
          let cb = cPrev || c, yRef = yPrev;
          if (!wasVis && cPrev) {
            /* emerging from behind a crest: the rows just under the silhouette belong to THIS surface
             * at the point where it crosses the silhouette, not to the crest in front, so find that
             * point and interpolate from it (blending from the crest is what stepped every lee) */
            let lo = dPrev, hi = d;
            for (let j = 0; j < 7; j++) {
              const mid = (lo + hi) / 2, lx2 = sx * mid, lz2 = -mid;
              const x2 = lx2 * Math.cos(yaw) + lz2 * Math.sin(yaw), z2 = -lx2 * Math.sin(yaw) + lz2 * Math.cos(yaw);
              const y2 = hy + (camY - o.height(x2, z2)) / mid * f;
              if (y2 < yb) hi = mid; else lo = mid;
            }
            const lx3 = sx * hi, lz3 = -hi;
            cb = shade(lx3 * Math.cos(yaw) + lz3 * Math.sin(yaw), -lx3 * Math.sin(yaw) + lz3 * Math.cos(yaw), hi);
            yRef = yb;
          }
          wasVis = true; dPrev = d;
          const top = Math.max(Math.floor(y), 0);
          const span = Math.max(1, yRef - y);
          for (let r = top; r < yb; r++) {
            const t = Math.min(1, Math.max(0, (r + 0.5 - y) / span));   /* 0 at this step, 1 at the previous */
            const q = r * W + col, p3 = q * 3;
            acc[p3] += c[0] + (cb[0] - c[0]) * t; acc[p3 + 1] += c[1] + (cb[1] - c[1]) * t; acc[p3 + 2] += c[2] + (cb[2] - c[2]) * t;
            cnt[q]++;
          }
          yb = top; cPrev = c; yPrev = y;
        }
      }
    }
    for (let q = 0; q < W * Hh; q++) {
      const n = cnt[q]; if (!n) continue;
      const p = q * 4, p3 = q * 3;
      if (n < ss) {   /* a sub-column that stopped above this row: blend with what was there (the sky) */
        const w = n / ss;
        D[p] = D[p] * (1 - w) + acc[p3] / n * 255 * w; D[p + 1] = D[p + 1] * (1 - w) + acc[p3 + 1] / n * 255 * w; D[p + 2] = D[p + 2] * (1 - w) + acc[p3 + 2] / n * 255 * w;
      } else { D[p] = acc[p3] / n * 255; D[p + 1] = acc[p3 + 1] / n * 255; D[p + 2] = acc[p3 + 2] / n * 255; }
      D[p + 3] = 255;
    }
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); cx.putImageData(img, 0, 0); cx.restore();
  };

  global.AKP = AKP;
})(typeof window !== "undefined" ? window : this);
