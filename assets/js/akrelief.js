/* akrelief.js — 2.5D relit-heightfield form-shading (offline, ZERO dependencies
 * beyond the committed noise.js). No network, deterministic per seed.
 *
 * WHY THIS EXISTS. Artwork-craft scored 7 for two runs straight (2026-07-21
 * "beluga", 2026-07-22 "raised cadastral plate") for the same reason: the ONE
 * dimensional hero beat was a FLAT fill. A flat SVG polygon does not read as a
 * raised solid even under two stacked drop-shadows, and a Canvas-2D fallback
 * silhouette reads as a blob. akthree.objectHero solves this on the GPU path
 * (a rim light carves a dark subject off a dark ground); this is its 2D analogue
 * for the CPU / SVG-adjacent path: it turns a flat filled region into a shaded,
 * dimensional FORM with real highlights and self-shadow, using nothing but
 * ImageData math over the noise.js primitives already committed.
 *
 * THE TECHNIQUE (the settled offline way to fake sculpted volume, all over the
 * frontier: mattdesl ShaderLesson6; the pixel-art normal-map survey arXiv
 * 2212.09692; the web 2.5D dynamic-paintings pipeline arXiv 2311.15354):
 *   1. build a procedural HEIGHTFIELD H(x,y) in [0,1] (noise.js fbm2/warp2 by
 *      default, or any height(nx,ny) callback -- a dome, a plate bevel, a ridge);
 *   2. derive a per-pixel surface NORMAL from a 3x3 SOBEL of H:
 *         N = normalize(-dH/dx, -dH/dy, 1/strength)
 *      (strength is the relief exaggeration multiplier; bigger = taller relief);
 *   3. LAMBERT-shade in 2D against one or more lights:
 *         shade = ambient + Σ w_i * max(dot(N, L_i), 0) * diffuse
 *      each light L_i built from a compass AZIMUTH + ELEVATION; the light-Z
 *      (elevation) is the depth that gives the form its roundness;
 *   4. map shade -> a two-stop color ramp (shadow -> lit) and write ImageData,
 *      optionally clipped by a silhouette MASK so only the subject is shaded.
 *
 * FRONTIER DEFAULT (editorial-cartography scan 2026-07-22): terrain/relief reads
 * richer under MULTIDIRECTIONAL OBLIQUE-WEIGHTED hillshade (MDOW) than a single
 * harsh light -- combine azimuths ~225/270/315/360 aspect-weighted rather than
 * one lamp. Pass { multidirectional: true } to use that light set; the default is
 * a single NW key (az 315, el 35) which is what an OBJECT hero wants for roundness.
 * Sources: https://www.maptiler.com/news/2026/02/multidirectional-hillshades-and-terrain-color-ramps-for-web-maps/ ,
 * https://gist.github.com/maning/28ad9ebb1dcb1ea85440 ,
 * https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson6
 *
 * USAGE (slide code; needs noise.js loaded first for the default heightfield):
 *   <script src="@@ASSETS@@/js/noise.js"></script>
 *   <script src="@@ASSETS@@/js/akrelief.js"></script>
 *   const cx = canvas.getContext('2d');        // 2x backing store per the contract
 *   AK.reliefShade(cx, {
 *     x: 120, y: 300, w: 840, h: 840,          // region in CSS px (pre-scale)
 *     scale: 2,                                 // canvas backing scale (cx.scale(2,2))
 *     seed: 20260722,
 *     noiseScale: 0.010, octaves: 5, warp: 0.6, // heightfield character
 *     strength: 3,                              // relief exaggeration (bigger = taller)
 *     low:  '#241d15', high: '#e6d2a6',         // shadow -> lit ramp, REQUIRED,
 *                                               // from the slide's own palette
 *     ambient: 0.22, diffuse: 0.95,
 *     mask: AK.reliefDome                       // optional silhouette (a raised dome)
 *   });
 *
 * THE OPTION CONTRACT (2026-08-20, run No.38). An option this function does not
 * know is now a THROW plus a console.error, never a silent no-op, and the ramp
 * is REQUIRED. Both halves were bought with a whole deck. Two slides passed
 * `mix: 0.30` / `mix: 0.34`, which is not an option here and was dropped on the
 * floor: reliefShade writes ImageData with putImageData, so it REPLACES the
 * region it covers and there is no blend, alpha, opacity or composite operation
 * in it at all. What the author intended as a 30 percent form-shading finish was
 * a 100 percent overwrite. Slide 05's cold white bond printed as kraft with
 * every printed line on both sheets erased, so the gold marker highlighting one
 * clause of a proclamation was highlighting a blank sheet; slide 07's bead-
 * blasted anodize printed as a cardboard carton. Both also passed `light: [x,y,z]`
 * (the option is `lights: [{az,el,w}]`), so the lighting they wrote was ignored
 * too. Nine pixel critics found the result; the render gate, machine QA and the
 * style lint could not, because a silently ignored option leaves no trace.
 * The ramp is required for the same reason at one remove: `low`/`high` used to
 * default to a WARM STONE, and an unset ramp is not neutral. On a deck whose
 * palette reserves the entire warm channel for one token, the default put the
 * largest region in frame outside the palette.
 *
 * SO: reliefShade is the SUBSTRATE. Lay it down FIRST, before any printed
 * detail, and name `low`/`high` from the slide's own palette. If you want a
 * FINISH rather than a substrate, render it to an offscreen canvas and
 * composite that yourself with an explicit globalAlpha (the surface pass,
 * knowledge/FIELD_NOTES.md 2026-08-20).
 *
 * NOTES
 * - Deterministic: uses AK.reseed(seed) + the noise.js field, never Math.random.
 * - Text stays DOM/SVG. This shades ART only.
 * - Data honesty: this is FORM shading, not a quantity encoding. A shaded volume
 *   is illustration; never read magnitude off the relief.
 * - Cost: one fbm eval per pixel (the height buffer is built once, the Sobel then
 *   reads neighbours from the buffer, not re-evaluating noise). A 900x900 CSS-px
 *   hero at scale 2 is ~3.2M px; keep hero regions bounded and inside render's 30s.
 */
(function (global) {
  "use strict";
  var AK = global.AK || (global.AK = {});

  /* THE OPTION CONTRACT. A helper that accepts an option it has never heard of
   * is a helper that ships the wrong material through every gate (see the block
   * at the top of this file). optionContract() is exported so any other AK
   * helper can adopt the same rule; it deliberately has no dependencies, so
   * copying these lines into a helper that loads on its own is also fine.
   *
   * It does BOTH things on purpose: console.error, then throw. The throw is the
   * loud half, but real slide code wraps art calls in try/catch ("form shading
   * is a finish, never the structure"), and a swallowed throw is a silent no-op
   * again. The console.error survives the catch, render.py records it, and
   * qa.py FAILS on the "AK CONTRACT:" prefix rather than warning.
   */
  var CONTRACT_TAG = "AK CONTRACT: ";

  function nearest(key, allowed) {
    // cheap edit distance, only to say "did you mean" -- never to accept a key
    var best = null, bestD = 1e9, lk = String(key).toLowerCase(), i;
    for (i = 0; i < allowed.length; i++) {
      var a = allowed[i].toLowerCase(), m = [], j, k;
      for (j = 0; j <= lk.length; j++) m[j] = [j];
      for (k = 0; k <= a.length; k++) m[0][k] = k;
      for (j = 1; j <= lk.length; j++)
        for (k = 1; k <= a.length; k++)
          m[j][k] = Math.min(m[j - 1][k] + 1, m[j][k - 1] + 1,
                             m[j - 1][k - 1] + (lk[j - 1] === a[k - 1] ? 0 : 1));
      var d = m[lk.length][a.length];
      if (d < bestD) { bestD = d; best = allowed[i]; }
    }
    return (bestD <= Math.max(2, Math.ceil(lk.length / 3))) ? best : null;
  }

  function optionContract(fnName, opts, allowed, notes) {
    var o = opts || {}, bad = [], k;
    for (k in o) {
      if (!Object.prototype.hasOwnProperty.call(o, k)) continue;
      if (allowed.indexOf(k) < 0) bad.push(k);
    }
    if (!bad.length) return;
    var msg = CONTRACT_TAG + fnName + ": unknown option" + (bad.length > 1 ? "s " : " ")
      + bad.map(function (b) {
          var n = (notes && notes[b]) ? " -- " + notes[b] : "";
          var guess = nearest(b, allowed);
          if (!n && guess) n = " -- did you mean `" + guess + "`?";
          return "`" + b + "`" + n;
        }).join("; ")
      + ". This option is NOT applied and never was; it is refused rather than "
      + "ignored so it can't ship. Known options: " + allowed.join(", ") + ".";
    try { console.error(msg); } catch (e) {}
    throw new Error(msg);
  }

  function hexToRGB(s) {
    var m = String(s).match(/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i);
    if (!m) return [0, 0, 0];
    return [parseInt(m[1], 16), parseInt(m[2], 16), parseInt(m[3], 16)];
  }

  // Compass azimuth (deg, clockwise from north/up) + elevation (deg) -> unit
  // light vector in screen space (+x right, +y down, +z toward viewer).
  function lightVec(azDeg, elDeg) {
    var az = azDeg * Math.PI / 180, el = elDeg * Math.PI / 180;
    var ch = Math.cos(el);
    return [ch * Math.sin(az), -ch * Math.cos(az), Math.sin(el)];
  }

  // Built-in silhouette masks: (u,v) in [0,1] within the region -> alpha 0..1.
  // A raised dome/plate: full coverage with a soft edge falloff.
  function reliefDome(u, v) {
    var dx = (u - 0.5) * 2, dy = (v - 0.5) * 2;
    var r = Math.sqrt(dx * dx + dy * dy);
    if (r >= 1) return 0;
    return Math.min(1, (1 - r) / 0.14);   // ~14% soft rim
  }
  function reliefRect(u, v) {
    // soft-cornered rectangle (a bevelled plate)
    var m = 0.04;
    var ax = Math.min(u, 1 - u), ay = Math.min(v, 1 - v);
    return Math.min(1, Math.min(ax, ay) / m);
  }

  /* reliefShade(cx, opts) -> { x, y, w, h }
   * Shades a rectangular region of the canvas as a lit heightfield. Returns the
   * region rect (device px) it touched. Opts (all optional except cx):
   *   x,y,w,h        region in CSS px (default: whole canvas / scale).
   *   scale          backing-store scale factor (default 2).
   *   seed           heightfield seed (default 1337).
   *   height(u,v)    custom height fn, u,v in [0,1] -> [0,1]; default fbm/warp.
   *   noiseScale     default-field frequency in device px (default 0.012).
   *   octaves,warp   default-field fbm octaves (5) and domain-warp strength (0.5).
   *   strength       relief exaggeration (gradient multiplier, default 3;
   *                  noise fields ~2-6, smooth macro dome/bevel ~60-200).
   *   lights         [{az,el,w}] override; else single NW key or MDOW set.
   *   multidirectional  use the 4-azimuth MDOW light set (default false).
   *   ambient,diffuse   Lambert terms (default 0.22, 0.95).
   *   low,high       shadow->lit ramp hex. REQUIRED, both of them, named from
   *                  the slide's own palette (see THE OPTION CONTRACT above).
   *   gamma          shade gamma (default 1.0).
   *   mask(u,v)      silhouette alpha 0..1; default full opaque rect.
   *
   * Any other key THROWS. There is no blend/alpha/mix: this REPLACES its region.
   */
  var RELIEF_OPTS = ["x", "y", "w", "h", "scale", "seed", "height", "noiseScale",
                     "octaves", "warp", "strength", "lights", "multidirectional",
                     "ambient", "diffuse", "low", "high", "gamma", "mask"];
  var NO_BLEND = "reliefShade writes ImageData and REPLACES the region it "
    + "covers; it has no blend, alpha or composite of any kind. Lay it down as "
    + "the SUBSTRATE first, before the printed detail, or render the finish to "
    + "an offscreen canvas and composite that with an explicit globalAlpha";
  var RELIEF_NOTES = {
    mix: NO_BLEND, alpha: NO_BLEND, opacity: NO_BLEND, blend: NO_BLEND,
    composite: NO_BLEND, globalAlpha: NO_BLEND, globalCompositeOperation: NO_BLEND,
    light: "the option is `lights`, an ARRAY of {az, el, w} compass lights "
      + "(azimuth degrees clockwise from north, elevation degrees), not a "
      + "direction vector; or pass `multidirectional: true` for the MDOW set"
  };

  function reliefShade(cx, opts) {
    var o = opts || {};
    optionContract("AK.reliefShade", o, RELIEF_OPTS, RELIEF_NOTES);
    if (!o.low || !o.high) {
      var m = CONTRACT_TAG + "AK.reliefShade: `low` and `high` are REQUIRED and "
        + "must be named from this slide's own palette. The ramp used to default "
        + "to a warm stone (#241d15 -> #e6d2a6), which is how a cold white bond "
        + "printed as kraft and an anodized shell printed as cardboard; an unset "
        + "ramp is not neutral, it is a decision nobody made.";
      try { console.error(m); } catch (e) {}
      throw new Error(m);
    }
    var scale = o.scale || 2;
    var cv = cx.canvas;
    var X = Math.round((o.x || 0) * scale);
    var Y = Math.round((o.y || 0) * scale);
    var W = Math.round((o.w != null ? o.w * scale : cv.width - X));
    var H = Math.round((o.h != null ? o.h * scale : cv.height - Y));
    if (W <= 2 || H <= 2) return { x: X, y: Y, w: 0, h: 0 };

    var seed = (o.seed != null) ? o.seed : 1337;
    if (typeof AK.reseed === "function") AK.reseed(seed);

    var ns = (o.noiseScale != null) ? o.noiseScale : 0.012;
    var oct = o.octaves || 5;
    var warp = (o.warp != null) ? o.warp : 0.5;
    var customH = (typeof o.height === "function") ? o.height : null;
    var haveNoise = (typeof AK.fbm2 === "function");

    // 1) height buffer H(x,y) in [0,1], built ONCE.
    var hbuf = new Float32Array(W * H);
    var i, x, y, u, v, h;
    for (y = 0; y < H; y++) {
      for (x = 0; x < W; x++) {
        u = x / (W - 1); v = y / (H - 1);
        if (customH) {
          h = customH(u, v);
        } else if (haveNoise) {
          var gx = (X + x) * ns, gy = (Y + y) * ns;
          var n = (warp > 0) ? AK.warp2(gx, gy, warp, { octaves: oct })
                             : AK.fbm2(gx, gy, { octaves: oct });
          h = n * 0.5 + 0.5;              // [-1,1] -> [0,1]
        } else {
          h = 0.5;                         // flat fallback (still lets mask/ramp run)
        }
        hbuf[y * W + x] = h;
      }
    }

    // 2) lights
    var lights;
    if (o.lights && o.lights.length) {
      lights = o.lights.map(function (L) {
        return { v: lightVec(L.az != null ? L.az : 315, L.el != null ? L.el : 50), w: (L.w != null ? L.w : 1) };
      });
    } else if (o.multidirectional) {
      // MDOW: azimuths 225/270/315/360, slight weight toward the classic NW.
      lights = [
        { v: lightVec(315, 45), w: 1.10 },
        { v: lightVec(270, 45), w: 0.90 },
        { v: lightVec(360, 45), w: 0.90 },
        { v: lightVec(225, 45), w: 0.85 }
      ];
    } else {
      lights = [{ v: lightVec(315, 35), w: 1 }];   // single NW key (object roundness)
    }
    var wsum = 0; for (i = 0; i < lights.length; i++) wsum += lights[i].w;

    // strength is a DIRECT gradient multiplier: bigger strength = more relief.
    // Its useful magnitude scales with the heightfield's per-pixel slope, so it
    // depends on frequency content: high-frequency noise fields want strength
    // ~2-6, smooth macro forms (a dome / bevel spanning the whole region) want
    // ~60-200. The built-in noise field pairs with the default 3.
    var strength = (o.strength != null) ? o.strength : 3;
    var ambient = (o.ambient != null) ? o.ambient : 0.22;
    var diffuse = (o.diffuse != null) ? o.diffuse : 0.95;
    var gamma = o.gamma || 1.0;
    var low = hexToRGB(o.low);
    var high = hexToRGB(o.high);
    var mask = (typeof o.mask === "function") ? o.mask : null;

    // 3+4) Sobel normal -> Lambert -> ramp -> ImageData
    var img = cx.createImageData(W, H);
    var d = img.data;
    var sample = function (px, py) {
      if (px < 0) px = 0; else if (px >= W) px = W - 1;
      if (py < 0) py = 0; else if (py >= H) py = H - 1;
      return hbuf[py * W + px];
    };
    for (y = 0; y < H; y++) {
      for (x = 0; x < W; x++) {
        // 3x3 Sobel over the height buffer
        var tl = sample(x - 1, y - 1), t = sample(x, y - 1), tr = sample(x + 1, y - 1);
        var l = sample(x - 1, y), r = sample(x + 1, y);
        var bl = sample(x - 1, y + 1), b = sample(x, y + 1), br = sample(x + 1, y + 1);
        var dHdx = ((tr + 2 * r + br) - (tl + 2 * l + bl)) * strength;
        var dHdy = ((bl + 2 * b + br) - (tl + 2 * t + tr)) * strength;
        // normal = normalize(-dHdx, -dHdy, 1)
        var nx = -dHdx, ny = -dHdy, nzz = 1;
        var inv = 1 / Math.sqrt(nx * nx + ny * ny + nzz * nzz);
        nx *= inv; ny *= inv; nzz *= inv;

        var lit = 0;
        for (i = 0; i < lights.length; i++) {
          var L = lights[i].v;
          var dp = nx * L[0] + ny * L[1] + nzz * L[2];
          if (dp > 0) lit += lights[i].w * dp;
        }
        lit /= wsum;
        var shade = ambient + diffuse * lit;
        if (shade > 1) shade = 1; else if (shade < 0) shade = 0;
        if (gamma !== 1.0) shade = Math.pow(shade, gamma);

        var idx = (y * W + x) * 4;
        d[idx]     = low[0] + (high[0] - low[0]) * shade;
        d[idx + 1] = low[1] + (high[1] - low[1]) * shade;
        d[idx + 2] = low[2] + (high[2] - low[2]) * shade;
        var a = 255;
        if (mask) {
          var ma = mask(x / (W - 1), y / (H - 1));
          a = Math.round(255 * (ma < 0 ? 0 : ma > 1 ? 1 : ma));
        }
        d[idx + 3] = a;
      }
    }
    cx.putImageData(img, X, Y);
    return { x: X, y: Y, w: W, h: H };
  }

  AK.reliefShade = reliefShade;
  AK.optionContract = optionContract;
  AK.reliefLightVec = lightVec;
  AK.reliefDome = reliefDome;
  AK.reliefRect = reliefRect;
})(typeof window !== "undefined" ? window : globalThis);
