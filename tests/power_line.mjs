// The power line, read the way a reader actually reads it.
//
// WHY THIS EXISTS. The line shipped with one pointerenter listener per month,
// which is a mouse design wearing pointer events. On touch the pointer is
// captured by whatever element received the press, so every later move goes to
// THAT rect and the eleven rects a finger crosses hear nothing. The reading
// changed where you tapped and then froze, and the maintainer found it on a
// phone because no check here had ever put a finger on the page.
//
// So this drags one. It presses, moves without lifting, and asserts the value
// changed at every step and moved forward in time, which is the assertion the
// old design fails and the hit tested one passes. Then it checks the mouse
// still reads on hover with no button held, because fixing touch by requiring
// a press everywhere would have been the easy wrong answer.
//
// Needs a built site:  SITE=/tmp/site node tests/power_line.mjs

import { chromium } from 'playwright';
const URL = 'file://' + process.env.SITE + '/gas-watch/index.html';
// The pre-installed browser when there is one, whatever playwright resolves
// otherwise, so this runs the same on a runner as on a workstation. Pinning
// the workstation path outright is what took this job down the first time it
// ran in CI, where playwright installs to its own cache and nothing sits at
// /opt/pw-browsers. Copied from tests/ask_engine.mjs, which already knew.
const exe = process.env.PLAYWRIGHT_CHROMIUM || '/opt/pw-browsers/chromium';
const b = await chromium.launch(
  (await import('node:fs')).existsSync(exe) ? { executablePath: exe } : {});
let fails = 0;
const ck = (l, c, d = '') => { if (!c) fails++; console.log(`  ${c ? 'PASS' : 'FAIL'}  ${l}${d ? '  ' + d : ''}`); };

const read = (p) => p.evaluate(() => ({
  m: document.querySelector('.pwread-m').textContent,
  v: document.querySelector('.pwread-v b').textContent,
  ruleX: document.querySelector('.pwrule').getAttribute('x1'),
  op: document.querySelector('.pwrule').getAttribute('opacity'),
}));

// ---------------------------------------------------------------- touch
const phone = await b.newContext({
  viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true,
  deviceScaleFactor: 3,
});
let p = await phone.newPage();
const errs = [];
p.on('pageerror', (e) => errs.push(String(e)));
await p.goto(URL);
await p.waitForTimeout(400);
await p.locator('.pwchart').scrollIntoViewIfNeeded();
await p.waitForTimeout(200);

console.log('a finger dragged along the line reads every month it crosses');
const box = await p.locator('.pwspark').boundingBox();
const y = box.y + box.height / 2;
const seen = [];
// A real drag: press once, then move across without lifting. This is exactly
// what per-rect pointerenter could not see.
await p.touchscreen.tap(box.x + 10, y);
await p.waitForTimeout(60);
seen.push(await read(p));
for (const frac of [0.15, 0.3, 0.45, 0.6, 0.75, 0.9]) {
  await p.evaluate(({ x, y }) => {
    const svg = document.querySelector('.pwspark');
    const ev = (t, extra) => svg.dispatchEvent(new PointerEvent(t, {
      pointerId: 1, pointerType: 'touch', isPrimary: true, bubbles: true,
      clientX: x, clientY: y, ...extra,
    }));
    if (!window.__down) { ev('pointerdown'); window.__down = 1; }
    ev('pointermove');
  }, { x: box.x + box.width * frac, y });
  await p.waitForTimeout(30);
  seen.push(await read(p));
}
const months = seen.map((s) => s.m);
ck('the reading changed at every step of the drag',
  new Set(months).size === months.length, months.join(' -> '));
ck('the months move forward in time across the drag',
  months.every((m, i) => i === 0 || Date.parse(m + ' 1') > Date.parse(months[i - 1] + ' 1')),
  months.join(' -> '));
ck('the crosshair followed the finger',
  new Set(seen.map((s) => s.ruleX)).size === seen.length);
ck('every value read back is a price', seen.every((s) => /^\d+\.\d{2}$/.test(s.v)));

console.log('lifting the finger leaves the reading up, because touch has no hover');
await p.evaluate(({ x, y }) => {
  document.querySelector('.pwspark').dispatchEvent(new PointerEvent('pointerup', {
    pointerId: 1, pointerType: 'touch', isPrimary: true, bubbles: true, clientX: x, clientY: y,
  }));
}, { x: box.x + box.width * 0.9, y });
await p.waitForTimeout(80);
const held = await read(p);
ck('the month a finger stopped on is still readable', held.m === seen[seen.length - 1].m,
  `${held.m} vs ${seen[seen.length - 1].m}`);

console.log('a phone is not told to press keys it does not have');
const vis = await p.evaluate(() => ({
  touch: getComputedStyle(document.querySelector('.pwtouch')).display,
  point: getComputedStyle(document.querySelector('.pwpoint')).display,
  // innerText, not textContent: only innerText honours display:none, and
  // "what does the reader actually see" is the whole question here.
  text: document.querySelector('.pwnote').innerText.replace(/\s+/g, ' '),
}));
ck('the touch instruction is the one shown', vis.touch !== 'none' && vis.point === 'none',
  `touch ${vis.touch}, point ${vis.point}`);
ck('and it says drag, not tab', /Drag a finger/.test(vis.text) && !/arrow keys/.test(vis.text));

console.log('nothing threw on touch');
ck('no runtime errors', errs.length === 0, errs.join(' | '));
await phone.close();

// ---------------------------------------------------------------- mouse
console.log('a mouse still reads on hover, with no button held');
const desk = await b.newContext({ viewport: { width: 1200, height: 900 } });
p = await desk.newPage();
const derrs = [];
p.on('pageerror', (e) => derrs.push(String(e)));
await p.goto(URL);
await p.waitForTimeout(300);
await p.locator('.pwchart').scrollIntoViewIfNeeded();
await p.waitForTimeout(200);
const dbox = await p.locator('.pwspark').boundingBox();
const dy = dbox.y + dbox.height / 2;
const mseen = [];
for (const frac of [0.1, 0.35, 0.6, 0.85]) {
  await p.mouse.move(dbox.x + dbox.width * frac, dy);
  await p.waitForTimeout(40);
  mseen.push(await read(p));
}
ck('hover alone moves the reading', new Set(mseen.map((s) => s.m)).size === 4,
  mseen.map((s) => s.m).join(' -> '));
ck('the reading matches the nearest hit target\'s label', await p.evaluate(() => {
  const m = document.querySelector('.pwread-m').textContent;
  const v = document.querySelector('.pwread-v b').textContent;
  return [...document.querySelectorAll('.pwhit')]
    .some((e) => e.getAttribute('aria-label') === `${m}, ${v} cents per kilowatthour`);
}));

console.log('a mouse leaving resets to the latest month');
await p.mouse.move(5, 5);
await p.waitForTimeout(80);
const back = await read(p);
ck('reset on leave', back.op === '0', `opacity ${back.op}`);
ck('and the desktop instruction is the one shown', await p.evaluate(() =>
  getComputedStyle(document.querySelector('.pwpoint')).display !== 'none'
  && getComputedStyle(document.querySelector('.pwtouch')).display === 'none'));
ck('no runtime errors', derrs.length === 0, derrs.join(' | '));

console.log(fails ? `\n${fails} FAILED` : '\nall clean');
await b.close();
process.exit(fails ? 1 : 0);
