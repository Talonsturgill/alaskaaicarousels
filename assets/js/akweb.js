/* akweb.js -- THE DOLLAR WEB, run No.110 (2026-11-09). The deck's shared OBJECT.
 *
 * Alaska's Year 1 Rural Health Transformation award, $272,174,855.72 (claim C30),
 * drawn as ONE continuous thermoformed blister web: one pocket per award (254, C27),
 * sorted largest first, each pocket's LENGTH its preliminary dollars from the state's
 * Notice of Intent to Award workbook (C48), at one scale on every frame. The web runs
 * as a panorama spine along a shelf rail on slides 02 to 09: 8 frames x 1080 px =
 * 8,640 px for the whole award, so $31,501.72 per design px. Awards fill 7,903.6 px;
 * the last 736.4 px is flat unformed foil, the remainder the state says pays for
 * administration, evaluation and oversight (C24, C75).
 *
 * Global x = (slide - 2) * 1080 + local x, so every seam is exact.
 *
 * This file draws ONE object and nothing else. Each slide composes its own picture
 * around it. Shading is per DEVICE pixel (2x backing), lit by the deck's one skylight
 * (from above and slightly behind the viewer, so dome crowns light and the lee is below).
 *
 *   AKWEB.rail(cx, slide, o)  draw the rail band (design y 1086..1244) onto a 2x canvas
 *                             whose context is scaled by 2. Opaque in its band.
 *   AKWEB.pocketsOn(slide)    [{i, id, x0, x1, amt, gold}] in LOCAL design px.
 *   AKWEB.ticker(el, state)   the seven-pocket gold ticker as inline SVG into el.
 *   AKWEB.pocketShade(...)    the shading kernel, for slides that draw a pocket larger.
 *
 * Data: [amount, flag] per award, flag 1 = includes an AI tool (C68), 2 = a machine
 * that is not AI (robotic surgery, drones; C59, C63, C64), 0 = everything else.
 */
(function (G) {
  "use strict";
  var DATA = [[16009453.33,0],[6967728.14,2],[6349886.26,0],[5781079.29,0],[5000000.0,0],[5000000.0,0],[4978914.0,0],[4570000.0,0],[4559450.53,0],[4272636.0,0],[4171115.0,2],[3882215.82,0],[3850279.0,0],[3781074.4,0],[3653844.52,0],[3635988.0,0],[3606476.0,0],[3156626.0,1],[3151600.0,0],[3134278.0,0],[3015900.0,0],[2985000.0,0],[2900000.0,0],[2726680.0,0],[2706276.0,0],[2636272.39,0],[2617260.0,0],[2412784.0,0],[2361188.0,0],[2294194.67,0],[2129485.0,0],[2125312.32,0],[2016025.0,0],[2000000.0,0],[2000000.0,0],[2000000.0,0],[2000000.0,0],[1950030.0,0],[1920730.0,0],[1866368.0,0],[1845863.21,0],[1804994.0,0],[1741243.0,0],[1625408.0,0],[1570650.0,0],[1557975.0,0],[1550852.0,0],[1547223.0,0],[1509019.17,0],[1500000.0,0],[1443165.0,0],[1374000.0,0],[1350027.0,0],[1313360.0,0],[1291355.0,0],[1241085.55,1],[1207552.47,0],[1195000.0,0],[1173721.0,0],[1172759.64,0],[1151900.0,0],[1090860.21,0],[1086793.17,0],[1080000.0,0],[1002299.65,0],[1000000.0,0],[993347.45,0],[987787.0,0],[987204.7,0],[967641.74,0],[965836.0,0],[958193.0,0],[954143.18,0],[927247.0,0],[919975.0,0],[901589.45,0],[862939.0,0],[853955.58,0],[850000.0,0],[828892.8,0],[820093.65,0],[792431.0,0],[772500.0,0],[738619.0,0],[727091.29,0],[726400.0,0],[704880.0,0],[694200.0,0],[678460.0,0],[658631.52,0],[650748.21,0],[650190.0,0],[649662.0,0],[638555.0,0],[627180.0,0],[618916.24,0],[616438.23,0],[612529.66,0],[609517.0,0],[608672.0,0],[604017.75,0],[600000.0,0],[600000.0,0],[593100.0,0],[588617.0,0],[574513.0,0],[558105.35,0],[550000.0,0],[525450.0,0],[510307.3,0],[507909.94,0],[500000.0,0],[500000.0,0],[487022.0,0],[478643.99,0],[474967.0,0],[464506.9,0],[452047.99,0],[450000.0,0],[446453.0,0],[442800.0,0],[437542.0,0],[435769.79,0],[434202.0,0],[430000.0,1],[422500.0,0],[421467.0,0],[415000.0,0],[414798.1,0],[414400.0,0],[413001.91,0],[400282.0,0],[398666.23,0],[398605.0,0],[390334.08,0],[383737.0,0],[381512.34,0],[374051.38,0],[370511.6,0],[364764.4,0],[358271.87,0],[351125.0,0],[350000.0,0],[350000.0,0],[347018.0,0],[341943.0,0],[341274.0,0],[331115.61,0],[323420.0,0],[318604.43,0],[318319.27,0],[317111.0,0],[300000.0,0],[300000.0,0],[296179.86,0],[296017.0,0],[292246.28,0],[292006.0,0],[281295.1,0],[279270.0,0],[274477.0,0],[272689.0,0],[259820.8,0],[259551.0,0],[256985.33,0],[250000.0,0],[250000.0,0],[250000.0,0],[250000.0,1],[250000.0,2],[250000.0,0],[249958.4,0],[249948.0,0],[249828.66,0],[249806.42,0],[249653.52,0],[249208.8,0],[249197.0,0],[248622.0,0],[247499.74,0],[247051.27,0],[246050.0,0],[244568.0,0],[242719.0,0],[242531.68,0],[242000.0,0],[241655.17,0],[240033.48,0],[236031.0,0],[233922.68,0],[231669.0,0],[231623.0,0],[226546.03,0],[225852.0,0],[225436.6,0],[222333.0,0],[221824.85,0],[221801.8,0],[220481.0,0],[219980.0,0],[219343.0,0],[218964.0,0],[210115.0,0],[209919.0,0],[209237.62,0],[203091.53,0],[200767.66,0],[190556.0,1],[188131.0,0],[181093.27,0],[180602.63,0],[180000.0,0],[178766.5,0],[178579.0,0],[176359.0,0],[159947.0,0],[155000.0,0],[154343.5,0],[141702.7,1],[132300.0,0],[128987.0,0],[116261.59,0],[110500.0,0],[109500.0,0],[107985.0,0],[101584.0,0],[100253.18,0],[100000.0,0],[100000.0,0],[100000.0,0],[95000.0,0],[89118.0,0],[88871.0,0],[82691.88,0],[79141.0,0],[76554.0,0],[75000.0,0],[74263.0,0],[72787.0,0],[70021.25,0],[67290.33,0],[64787.11,0],[60047.0,0],[51992.33,0],[50000.0,0],[50000.0,0],[43000.0,0],[42627.0,0],[40750.0,0],[25492.5,1],[18980.0,0],[13990.29,0],[10000.0,0],[6354.5,0]];
  var IDS = ["BP1-IA-339","BP1-IA-254","BP1-IA-137","BP1-IA-308","BP1-IA-203","BP1-IA-178","BP1-IA-234","BP1-INT-24","BP1-IA-265","BP1-INT-17","BP1-IA-284","BP1-INT-11","BP1-IA-191","BP1-IA-129","BP1-IA-169","BP1-IA-301","BP1-IA-244","BP1-IA-042","BP1-IA-030","BP1-IA-038","BP1-IA-218","BP1-INT-10","BP1-INT-22","BP1-IA-362","BP1-IA-214","BP1-IA-360","BP1-IA-141","BP1-IA-151","BP1-IA-330","BP1-IA-345","BP1-IA-004","BP1-IA-320","BP1-IA-087","BP1-IA-024","BP1-IA-051","BP1-IA-054","BP1-INT-13","BP1-IA-083","BP1-IA-216","BP1-IA-101","BP1-IA-210","BP1-IA-018","BP1-IA-341","BP1-IA-331","BP1-IA-005","BP1-IA-026","BP1-IA-225","BP1-IA-305","BP1-IA-135","BP1-IA-048","BP1-IA-306","BP1-INT-02","BP1-IA-310","BP1-IA-138","BP1-IA-113","BP1-IA-200","BP1-IA-174","BP1-IA-029","BP1-IA-328","BP1-IA-198","BP1-IA-197","BP1-IA-017","BP1-IA-264","BP1-IA-268","BP1-IA-155","BP1-IA-008","BP1-IA-079","BP1-IA-132","BP1-INT-23","BP1-IA-201","BP1-IA-219","BP1-IA-295","BP1-IA-081","BP1-IA-329","BP1-IA-002","BP1-IA-181","BP1-IA-039","BP1-IA-266","BP1-INT-01","BP1-IA-195","BP1-IA-080","BP1-IA-324","BP1-IA-267","BP1-IA-247","BP1-IA-172","BP1-IA-130","BP1-INT-28","BP1-INT-25","BP1-IA-068","BP1-IA-246","BP1-IA-242","BP1-IA-040","BP1-IA-366","BP1-IA-035","BP1-IA-088","BP1-INT-03","BP1-IA-316","BP1-IA-280","BP1-IA-353","BP1-IA-332","BP1-IA-157","BP1-IA-227","BP1-IA-248","BP1-IA-006","BP1-IA-073","BP1-IA-323","BP1-IA-361","BP1-IA-094","BP1-IA-355","BP1-IA-011","BP1-IA-015","BP1-PL-007","BP1-IA-055","BP1-INT-21","BP1-IA-289","BP1-IA-255","BP1-PL-017","BP1-INT-26","BP1-IA-226","BP1-IA-260","BP1-IA-166","BP1-IA-258","BP1-IA-097","BP1-IA-224","BP1-IA-194","BP1-IA-007","BP1-IA-256","BP1-IA-290","BP1-IA-344","BP1-IA-359","BP1-IA-075","BP1-IA-158","BP1-IA-236","BP1-IA-207","BP1-IA-281","BP1-IA-019","BP1-IA-269","BP1-PL-006","BP1-IA-117","BP1-IA-235","BP1-IA-021","BP1-IA-077","BP1-IA-100","BP1-IA-179","BP1-IA-208","BP1-IA-066","BP1-IA-351","BP1-IA-318","BP1-IA-109","BP1-IA-275","BP1-IA-354","BP1-PL-001","BP1-INT-27","BP1-INT-07","BP1-IA-013","BP1-IA-033","BP1-IA-074","BP1-IA-237","BP1-IA-299","BP1-IA-286","BP1-IA-262","BP1-IA-211","BP1-IA-091","BP1-IA-239","BP1-IA-291","BP1-PL-010","BP1-PL-018","BP1-PL-020","BP1-IA-202","BP1-PL-026","BP1-IA-076","BP1-PL-002","BP1-IA-142","BP1-IA-349","BP1-IA-044","BP1-PL-008","BP1-IA-143","BP1-PL-003","BP1-IA-001","BP1-IA-114","BP1-IA-156","BP1-PL-011","BP1-IA-106","BP1-PL-021","BP1-IA-046","BP1-INT-16","BP1-IA-189","BP1-IA-144","BP1-IA-022","BP1-PL-015","BP1-IA-064","BP1-IA-312","BP1-IA-027","BP1-IA-104","BP1-PL-019","BP1-IA-325","BP1-IA-229","BP1-PL-005","BP1-IA-297","BP1-IA-232","BP1-IA-010","BP1-IA-199","BP1-IA-313","BP1-IA-300","BP1-IA-095","BP1-IA-186","BP1-IA-253","BP1-IA-272","BP1-IA-063","BP1-IA-183","BP1-IA-184","BP1-INT-09","BP1-IA-333","BP1-IA-025","BP1-PL-004","BP1-PL-023","BP1-IA-111","BP1-IA-314","BP1-IA-319","BP1-INT-04","BP1-IA-163","BP1-IA-125","BP1-PL-013","BP1-IA-078","BP1-IA-121","BP1-IA-089","BP1-IA-003","BP1-IA-146","BP1-IA-147","BP1-PL-016","BP1-IA-288","BP1-IA-145","BP1-IA-162","BP1-PL-025","BP1-IA-045","BP1-PL-012","BP1-IA-069","BP1-IA-105","BP1-IA-209","BP1-IA-240","BP1-IA-092","BP1-IA-245","BP1-IA-108","BP1-IA-277","BP1-PL-009","BP1-PL-022","BP1-PL-014","BP1-IA-160","BP1-PL-024","BP1-IA-187","BP1-IA-352","BP1-IA-072","BP1-IA-148","BP1-IA-185"];
  var TOTAL = 272174855.72;
  var SPAN = 8640;
  var PX = SPAN / TOTAL;          // design px per dollar
  var N = DATA.length;
  var X0 = new Float64Array(N + 1);
  for (var i = 0; i < N; i++) X0[i + 1] = X0[i] + DATA[i][0] * PX;
  var END = X0[N];                // 7903.6

  var Y = { top: 1036, web0: 1090, dome0: 1100, dome1: 1182, web1: 1192,
            lip0: 1194, lip1: 1240, tab0: 1122, tab1: 1160 };

  function find(g) {               // pocket index containing global x, or -1
    if (g < 0 || g >= END) return -1;
    var lo = 0, hi = N - 1;
    while (lo < hi) { var m = (lo + hi + 1) >> 1; if (X0[m] <= g) lo = m; else hi = m - 1; }
    return lo;
  }
  function sdRound(px, py, hx, hy, r) {   // signed distance to a rounded rect (negative inside)
    var qx = Math.abs(px) - hx + r, qy = Math.abs(py) - hy + r;
    var ox = Math.max(qx, 0), oy = Math.max(qy, 0);
    return Math.min(Math.max(qx, qy), 0) + Math.sqrt(ox * ox + oy * oy) - r;
  }
  function hash(n) { n = Math.imul(n ^ 0x9E3779B9, 0x85EBCA6B); n ^= n >>> 13;
    n = Math.imul(n, 0xC2B2AE35); n ^= n >>> 16; return (n >>> 0) / 4294967296; }
  function vnoise1(x, seed) {      // smooth 1D value noise
    var i = Math.floor(x), f = x - i, a = hash(i * 374761 + seed), b = hash((i + 1) * 374761 + seed);
    f = f * f * (3 - 2 * f); return a + (b - a) * f;
  }
  // Height of the formed web at design point (gx, y) in pocket k. Returns
  // {h, mat}: mat 0 foil, 1 inside dome (foil seen through PET), 2 tablet/gelcap.
  function heightAt(k, gx, y, out) {
    out.h = 0; out.mat = 0; out.dome = 0;
    if (k < 0) return out;
    var L = X0[k + 1] - X0[k];
    var inset = Math.min(1.6, L * 0.18);
    var hx = L / 2 - inset, cxp = X0[k] + L / 2;
    if (hx <= 0.05) return out;
    var hy = (Y.dome1 - Y.dome0) / 2, cy = (Y.dome0 + Y.dome1) / 2;
    var r = Math.min(30, hx, hy);
    var d = sdRound(gx - cxp, y - cy, hx, hy, r);
    if (d >= 0) return out;
    var ramp = Math.min(13, hx * 0.9);
    var t = Math.min(-d / ramp, 1);
    var H = 8.5 * Math.min(1, hx / 6 + 0.25);
    out.h = H * Math.sqrt(t * (2 - t)); out.mat = 1; out.dome = t;
    var thx = hx - Math.min(7, hx * 0.35), thy = (Y.tab1 - Y.tab0) / 2;
    if (thx > 0.08) {
      var tr = Math.min(thy, thx);
      var dt = sdRound(gx - cxp, y - cy, thx, thy, tr);
      if (dt < 0) {
        var tt = Math.min(-dt / tr, 1);                      // full round: a capsule in section
        out.h = Math.max(out.h, 1.5 + 9.0 * Math.sqrt(tt * (2 - tt)) * Math.min(1, thx / 5 + 0.3));
        out.mat = 2; out.tab = tt;
      }
    }
    return out;
  }
  var LX = 0.16, LY = -0.80, LZ = 0.58;   // the skylight in screen terms (x right, y down, z out)
  (function () { var n = Math.hypot(LX, LY, LZ); LX /= n; LY /= n; LZ /= n; })();
  var HX = LX, HY = LY, HZ = LZ + 1; (function () { var n = Math.hypot(HX, HY, HZ); HX /= n; HY /= n; HZ /= n; })();

  function srgb(c) { return Math.max(0, Math.min(255, Math.round(c))); }
  var FOIL = [199, 205, 211], FOIL_IN = [178, 186, 194], CHALK = [230, 226, 218],
      GOLD = [255, 199, 44], GOLD_LEE = [168, 120, 26], STEEL = [142, 154, 165], STEEL_SH = [60, 71, 82];

  function shadePixel(k, gx, y, flag, tmp, rgb) {
    var e = 0.5;
    heightAt(k, gx, y, tmp); var h0 = tmp.h, mat = tmp.mat, dome = tmp.dome;
    heightAt(k, gx + e, y, tmp); var hxp = tmp.h;
    heightAt(k, gx - e, y, tmp); var hxm = tmp.h;
    heightAt(k, gx, y + e, tmp); var hyp = tmp.h;
    heightAt(k, gx, y - e, tmp); var hym = tmp.h;
    var nx = -(hxp - hxm) / (2 * e), ny = -(hyp - hym) / (2 * e), nz = 1;
    var nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
    var diff = Math.max(0, nx * LX + ny * LY + nz * LZ);
    var nh = Math.max(0, nx * HX + ny * HY + nz * HZ);
    var streak = 0.92 + 0.16 * vnoise1(gx * 0.9, 7) * vnoise1(y * 0.02 + gx * 0.004, 3);
    var base, spec = 0, amb = 0.34;
    if (mat === 0) {
      base = FOIL; var f = (amb + 0.66 * diff) * streak; spec = Math.pow(nh, 24) * 0.25;
      // the tablet casts down onto the foil inside the pocket is handled in mat 1
      rgb[0] = base[0] * f; rgb[1] = base[1] * f; rgb[2] = base[2] * f;
    } else if (mat === 1) {
      var sh = 1;
      heightAt(k, gx - LX * 7, y - LY * 7, tmp); if (tmp.mat === 2) sh = 0.62;   // tablet cast under the dome
      base = FOIL_IN; var f1 = (amb + 0.5 * diff) * streak * sh;
      rgb[0] = base[0] * f1; rgb[1] = base[1] * f1; rgb[2] = base[2] * f1;
      var rim = dome < 0.22 ? (1 - dome / 0.22) * 0.55 : 0;     // the PET wall, seen edge-on at the shoulder
      var sky = 0.10 * Math.max(0, -ny) + 0.05 * (1 - (y - Y.dome0) / (Y.dome1 - Y.dome0));   // reflected skylight
      rgb[0] = rgb[0] * (1 - rim) + 70 * rim + 240 * sky; rgb[1] = rgb[1] * (1 - rim) + 78 * rim + 246 * sky; rgb[2] = rgb[2] * (1 - rim) + 88 * rim + 252 * sky;
      spec = Math.pow(nh, 90) * 1.1 + Math.pow(nh, 12) * 0.08;   // clear PET crown
    } else {
      var gold = flag === 1;
      var t = 0.30 + 0.70 * diff;
      if (gold) {
        var tg = Math.min(1, 0.15 + 1.05 * diff);
        for (var c = 0; c < 3; c++) rgb[c] = GOLD_LEE[c] * 0.7 + (GOLD[c] - GOLD_LEE[c] * 0.7) * tg;
        spec = Math.pow(nh, 60) * 0.9 + Math.pow(nh, 6) * 0.06;
      } else {
        var f2 = 0.38 + 0.66 * diff;
        rgb[0] = CHALK[0] * f2; rgb[1] = CHALK[1] * f2; rgb[2] = CHALK[2] * f2;
        spec = Math.pow(nh, 90) * 0.85;                          // PET over the tablet
      }
    }
    rgb[0] += 255 * spec; rgb[1] += 255 * spec; rgb[2] += 255 * spec;
  }

  function rail(cx, slide, o) {
    o = o || {};
    var base = (slide - 2) * 1080;
    var T = cx.getTransform(), S = T.a || 2;
    var y0 = Y.top, y1 = Y.lip1 + 4;
    var W = Math.round(1080 * S), r0 = Math.round(y0 * S), r1 = Math.round(y1 * S);
    var img = cx.getImageData(0, r0, W, r1 - r0), D = img.data;
    var tmp = {}, rgb = [0, 0, 0];
    var kcache = new Int32Array(W);
    for (var px = 0; px < W; px++) kcache[px] = find(base + (px + 0.5) / S);
    for (var row = r0; row < r1; row++) {
      var y = (row + 0.5) / S;
      for (var px = 0; px < W; px++) {
        var gx = base + (px + 0.5) / S, k = kcache[px], idx = ((row - r0) * W + px) * 4;
        if (y < Y.web0) {                                   // the rail's dark slot: a steel channel the web hangs in
          var sy = y - Y.top, SH = Y.web0 - Y.top;
          var vv = 13 + 6 * Math.exp(-(SH - sy) / 6);          // lit a little where the web meets it
          if (sy < 1.5) vv = 70 + 30 * vnoise1(gx * 0.5, 13);  // the channel's lit top lip
          else if (sy < 4) vv = 30;
          D[idx] = srgb(vv * 0.92); D[idx + 1] = srgb(vv * 1.0); D[idx + 2] = srgb(vv * 1.14); D[idx + 3] = 255;
          continue;
        }
        if (y < Y.web1) {
          var flag = k >= 0 ? DATA[k][1] : 0;
          shadePixel(k, gx, y, flag, tmp, rgb);
          // seal edges of the web: a darker crimp line at top and bottom
          var edge = Math.min(y - Y.web0, Y.web1 - y);
          if (edge < 2.2) { var m = 0.55 + 0.45 * edge / 2.2; rgb[0] *= m; rgb[1] *= m; rgb[2] *= m; }
          D[idx] = srgb(rgb[0]); D[idx + 1] = srgb(rgb[1]); D[idx + 2] = srgb(rgb[2]); D[idx + 3] = 255;
          continue;
        }
        if (y < Y.lip0) { D[idx] = 18; D[idx + 1] = 22; D[idx + 2] = 28; D[idx + 3] = 255; continue; }
        // the steel lip: lit top bevel, brushed face, the web's soft cast on its top
        var ly = y - Y.lip0, LH = Y.lip1 - Y.lip0;
        var bev = ly < 3 ? 1.0 : (ly < 5 ? 0.55 : 0);
        var face = 0.42 + 0.30 * Math.exp(-ly / 12) - 0.18 * (ly / LH);
        var br = 0.94 + 0.12 * vnoise1(gx * 0.6 + 11, 5) * vnoise1(gx * 0.05, 9);
        var cast = ly > 3 ? 1 - 0.55 * Math.exp(-(ly - 3) / 7) : 1;
        var v = (face * br * cast);
        var cr = STEEL_SH[0] + (STEEL[0] - STEEL_SH[0]) * v, cg = STEEL_SH[1] + (STEEL[1] - STEEL_SH[1]) * v, cb = STEEL_SH[2] + (STEEL[2] - STEEL_SH[2]) * v;
        if (bev) { cr += (210 - cr) * bev * 0.8; cg += (222 - cg) * bev * 0.8; cb += (232 - cb) * bev * 0.8; }
        if (ly > LH - 2) { cr *= 0.45; cg *= 0.45; cb *= 0.45; }
        D[idx] = srgb(cr); D[idx + 1] = srgb(cg); D[idx + 2] = srgb(cb); D[idx + 3] = 255;
      }
    }
    cx.putImageData(img, 0, r0);
    return { pockets: pocketsOn(slide), band: [Y.web0, Y.web1], lip: [Y.lip0, Y.lip1] };
  }

  function pocketsOn(slide) {
    var base = (slide - 2) * 1080, out = [];
    for (var k = 0; k < N; k++) {
      var a = X0[k] - base, b = X0[k + 1] - base;
      if (b <= 0 || a >= 1080) continue;
      out.push({ i: k, id: IDS[k], x0: a, x1: b, amt: DATA[k][0], gold: DATA[k][1] === 1, flag: DATA[k][1] });
    }
    return out;
  }

  // The seven-pocket ticker (D2). state: 'sealed' | 'bracket' | 'grouped' | 'first-open' |
  // 'all-open' | 'boxed' | 'stubs' | 'chip'. Drawn as SVG after the grade, so the gold is exact.
  function ticker(el, state) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', '150'); svg.setAttribute('height', '40'); svg.setAttribute('viewBox', '0 0 150 40');
    var xs = [0, 18, 36, 54, 72, 90, 108];
    if (state === 'grouped') xs = [0, 18, 46, 64, 82, 110, 128];
    if (state === 'boxed') xs = [0, 18, 36, 64, 82, 100, 118];
    var opened = state === 'all-open' || state === 'stubs' || state === 'chip' || state === 'boxed';
    function add(tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); svg.appendChild(e); return e; }
    for (var i = 0; i < 7; i++) {
      var x = 4 + xs[i], open = opened || (state === 'first-open' && i === 0);
      add('rect', { x: x, y: 4, width: 13, height: 22, rx: 6.5, fill: open ? 'none' : '#FFC72C',
                    stroke: '#FFC72C', 'stroke-width': open ? 1.4 : 0 });
      if (open) add('path', { d: 'M' + (x + 2) + ' 8 L' + (x + 6.5) + ' 14 L' + (x + 11) + ' 8', fill: 'none', stroke: '#FFC72C', 'stroke-width': 1.2 });
      if (state === 'stubs') add('line', { x1: x + 6.5, y1: 30, x2: x + 6.5, y2: 38, stroke: '#B9C6D6', 'stroke-width': 1.2, 'stroke-dasharray': '2 2' });
    }
    if (state === 'bracket') add('path', { d: 'M4 32 V36 H125 V32', fill: 'none', stroke: '#B9C6D6', 'stroke-width': 1.2 });
    if (state === 'boxed') add('rect', { x: 1, y: 1, width: 38, height: 28, fill: 'none', stroke: '#B9C6D6', 'stroke-width': 1.2 });
    if (state === 'chip') add('rect', { x: 132, y: 4, width: 13, height: 22, rx: 2, fill: 'none', stroke: '#B9C6D6', 'stroke-width': 1.2, 'stroke-dasharray': '3 2' });
    el.appendChild(svg);
    return svg;
  }

  G.AKWEB = { DATA: DATA, IDS: IDS, TOTAL: TOTAL, SPAN: SPAN, PX: PX, X0: X0, END: END, Y: Y,
              rail: rail, pocketsOn: pocketsOn, ticker: ticker, heightAt: heightAt,
              shadePixel: shadePixel, find: find, LIGHT: [LX, LY, LZ] };
})(window);
