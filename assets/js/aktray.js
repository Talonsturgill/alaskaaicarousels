/* aktray.js — drilled ballot-tray builder for the aksdf CPU raymarcher. (Alaska.Ai, No.74, 2026-10-01)
 *
 * A mahogany slab of cols x rows drilled cups, each cup holding one ball whose
 * material comes from a cell-state table, standing on a table plane, plus an
 * optional nickel inlay strip between two rows. It exists so two slides (the
 * Senate tray and the House tray) share one builder rather than two copies,
 * and it is a classic script because render.py resolves slides into
 * render/.resolved, where a relative module import cannot reach.
 *
 * DISTANCE CORRECTNESS. Equal spheres on a full grid are exact under
 * nearest-cell repetition (a point is nearer its own cell's centre than any
 * other's). An EMPTY cell breaks that, so the ball term checks the 3x3
 * neighbourhood. Points outside the grid clamp to the nearest cell.
 *
 *   const T = AKTRAY.build({cols:10, rows:10, pitch:1, state:(i)=>'ivory'|'ebony'|'gold'|'empty',
 *                            inlayAfterRow: 5});
 *   AKSDF.render(ctx, {scene: T.scene, mats: T.mats, ...});
 *   T.cellCenter(i) -> [x, y, z] world centre of the ball in cell i (0-based, fill order)
 *   AKTRAY.project(cam, box, internal, [x,y,z]) -> [px, py] page px, the same camera
 *     basis AKSDF.render uses, so every label sits on the ball it names.
 */
(function (global) {
  "use strict";
  const S = global.AKSDF;
  const MAT = {slab: 1, ivory: 2, ebony: 3, gold: 4, nickel: 5, table: 6, cup: 7, table2: 8};
  function build(o) {
    const cols = o.cols, rows = o.rows, P = o.pitch || 1;
    const br = (o.ballR != null ? o.ballR : 0.4) * P, cr = br * 1.06;
    const hx = cols * P / 2 + 0.4 * P, hz = rows * P / 2 + 0.4 * P, slabH = 0.5 * P, tableY = -2 * slabH;
    const cupY = 0.1 * P, ballY = cupY + 0.02 * P;
    const x0 = -(cols - 1) * P / 2, z0 = -(rows - 1) * P / 2;
    // fill order: rank i (0-based) -> row from the back, column from the right unless o.leftToRight
    const cellOf = i => { const r = Math.floor(i / cols), c = i % cols; return [o.leftToRight ? c : cols - 1 - c, r]; };
    const grid = new Array(cols * rows);
    for (let i = 0; i < cols * rows; i++) { const [c, r] = cellOf(i); grid[r * cols + c] = o.state(i); }
    const matOf = st => st === 'gold' ? MAT.gold : st === 'ebony' ? MAT.ebony : MAT.ivory;
    const inlayZ = o.inlayAfterRow != null ? z0 + (o.inlayAfterRow + 0.5) * P : null;
    function ballAt(p, c, r) {
      if (c < 0 || r < 0 || c >= cols || r >= rows) return [1e9, 0];
      const st = grid[r * cols + c]; if (st === 'empty') return [1e9, 0];
      const q = [p[0] - (x0 + c * P), p[1] - ballY, p[2] - (z0 + r * P)];
      return [S.len(q) - br, matOf(st)];
    }
    function scene(p) {
      // table, its grain running along x in two tones of mahogany
      let d = p[1] - tableY, m = MAT.table;
      if (Math.sin(p[2] * 9.0 / P + 3.0 * S.noise3(p[0] * 0.2 / P, 0.5, p[2] * 1.2 / P)) > 0.55) m = MAT.table2;
      // slab with a small round, minus the cup of the nearest cell
      const c = Math.max(0, Math.min(cols - 1, Math.round((p[0] - x0) / P))), r = Math.max(0, Math.min(rows - 1, Math.round((p[2] - z0) / P)));
      let slab = S.sdRoundBox([p[0], p[1] + slabH, p[2]], [hx - 0.06 * P, slabH - 0.06 * P, hz - 0.06 * P], 0.06 * P);
      const cup = S.len([p[0] - (x0 + c * P), p[1] - cupY, p[2] - (z0 + r * P)]) - cr;
      slab = Math.max(slab, -cup);
      let sm = MAT.slab;
      if (cup > -0.02 * P && cup < 0.03 * P && slab < 0.02 * P) sm = MAT.cup;     // the drilled lip, and every cup's well, read dark
      if (cup > -0.03 * P && p[1] < -0.005 * P && slab < 0.02 * P) sm = MAT.cup;
      if (slab < d) { d = slab; m = sm; }
      // the inlay: a nickel bar standing proud of the slab between two rows, run past both tray edges
      if (inlayZ != null) { const bar = S.sdRoundBox([p[0], p[1] - 0.035 * P, p[2] - inlayZ], [hx + 0.35 * P, 0.03 * P, 0.07 * P], 0.012 * P); if (bar < d) { d = bar; m = MAT.nickel; } }
      // balls: own cell, or the 3x3 neighbourhood when this cell is empty
      let b = ballAt(p, c, r);
      if (grid[r * cols + c] === 'empty') for (let dc = -1; dc <= 1; dc++) for (let dr = -1; dr <= 1; dr++) { const t = ballAt(p, c + dc, r + dr); if (t[0] < b[0]) b = t; }
      if (b[0] < d) { d = b[0]; m = b[1]; }
      return [d, m];
    }
    function cellCenter(i) { const [c, r] = cellOf(i); return [x0 + c * P, ballY, z0 + r * P]; }
    function cellTop(i) { const q = cellCenter(i); return [q[0], q[1] + br, q[2]]; }
    const mats = {
      [MAT.slab]: {color: [0.30, 0.10, 0.055], spec: 0.55, rim: 0.25},
      [MAT.cup]: {color: [0.10, 0.035, 0.02], spec: 0.1, rim: 0.1},
      [MAT.ivory]: {color: [0.86, 0.82, 0.72], spec: 0.7, rim: 0.4},
      [MAT.ebony]: {color: [0.075, 0.08, 0.095], spec: 0.95, rim: 0.95},
      [MAT.gold]: {color: [1.0, 0.60, 0.04], spec: 0.8, rim: 0.15},
      [MAT.nickel]: {color: [0.78, 0.81, 0.84], spec: 1.4, rim: 0.4},
      [MAT.table]: {color: [0.24, 0.085, 0.045], spec: 0.3, rim: 0.0},
      [MAT.table2]: {color: [0.19, 0.066, 0.036], spec: 0.25, rim: 0.0},
    };
    return {scene, mats, cellCenter, cellTop, inlayZ, hx, hz, tableY, P, br, x0, z0, cellOf};
  }
  function project(cam, box, internal, P) {
    const ro = cam.pos, look = cam.look, fov = cam.fov * Math.PI / 180;
    const fw = S.norm(S.sub(look, ro)), fr = S.norm(S.cross(fw, [0, 1, 0])), fu = S.cross(fr, fw), fl = 1 / Math.tan(fov / 2);
    const v = S.sub(P, ro), z = S.dot(v, fw), sx = S.dot(v, fr) / z * fl, sy = S.dot(v, fu) / z * fl;
    const W = internal[0], H = internal[1];
    const px = (sx + 1) / 2 * W, py = (1 - sy * W / H) * H / 2;
    return [box[0] + px / W * box[2], box[1] + py / H * box[3]];
  }
  global.AKTRAY = {build, project, MAT};
})(typeof window !== "undefined" ? window : globalThis);
