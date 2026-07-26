/* tests/mobile_docket_map.js
 *
 * The docket map, checked on the devices it will actually be read on.
 *
 * WHY THIS EXISTS
 *   The map was signed off against ONE synthetic 390x844 viewport and shipped
 *   broken anyway. A landscape phone cropped pins clean off the map, a tablet
 *   drew its badges at two thirds the intended size, and every layer toggle
 *   threw the reader hundreds of pixels up the page. None of those are exotic
 *   devices and none of them were covered.
 *
 *   So this walks a real device matrix, portrait AND landscape, and asserts the
 *   things a reader would notice rather than the things that are easy to
 *   measure. Every check names what it would feel like when it fails.
 *
 * RUN
 *   python -m http.server 8902 --directory docs &
 *   NODE_PATH=$(npm root -g) node tests/mobile_docket_map.js   # defaults to that port
 *   BASE_URL=https://alaskaaihq.com NODE_PATH=$(npm root -g) node tests/mobile_docket_map.js
 *
 *   NODE_PATH is only needed where playwright is installed globally, which is
 *   the case in this repo's dev container. CI installs it into ./node_modules
 *   and runs the plain command.
 *
 * Exits non-zero on any failure, so CI gates on it:
 * .github/workflows/docket-map-mobile.yml runs this on every change to the
 * builder, the docket ledger, the geo assets, or this file.
 */
'use strict';
const fs = require('fs');
const { chromium, devices } = require('playwright');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:8902';

/* This repo's dev container ships a preinstalled Chromium at a fixed path and
   forbids downloading another one. CI installs its own through Playwright and
   has no such path. Use the pinned binary only when it is really there, and
   otherwise let Playwright resolve its own, so the same file runs in both
   places without an env var to remember. */
function exePath() {
  const want = process.env.CHROMIUM;
  if (want) return want;
  const pinned = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
  return fs.existsSync(pinned) ? pinned : undefined;
}

/* Portrait phones from small to large, one tablet, and two landscape cases,
   because landscape is where a width-based breakpoint always breaks first. */
const MATRIX = [
  ['Galaxy S9+ (320 wide)', { viewport: { width: 320, height: 658 }, deviceScaleFactor: 3,
                              isMobile: true, hasTouch: true }],
  ['iPhone SE', { viewport: { width: 375, height: 667 }, deviceScaleFactor: 2,
                  isMobile: true, hasTouch: true }],
  ['iPhone 13', devices['iPhone 13']],
  ['iPhone 14 Pro Max', devices['iPhone 14 Pro Max']],
  ['Pixel 7', devices['Pixel 7']],
  ['iPad Mini', devices['iPad Mini']],
  ['iPhone 13 landscape', devices['iPhone 13 landscape']],
  ['iPad Mini landscape', devices['iPad Mini landscape']],
];

let failed = 0;
const results = [];
function check(device, name, ok, detail) {
  if (!ok) failed++;
  results.push({ device, name, ok, detail });
  console.log('  %s %s  %s', ok ? 'ok  ' : 'FAIL', name.padEnd(46), detail);
}

async function openMap(browser, profile) {
  const ctx = await browser.newContext(profile);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(BASE + '/docket/', { waitUntil: 'load' });
  await page.waitForSelector('.maphero svg');
  await page.waitForTimeout(500);
  return { ctx, page, errors };
}

/* The site sets scroll-behavior:smooth, and this page is over 13000px tall, so
   a scrollIntoView here is a long animation. Measuring before it settles blames
   the tap for movement the test itself started, which is exactly the false
   reading this function existed to avoid. Jump instantly, then wait for scrollY
   to stop changing before touching anything. */
async function settle(page) {
  let last = -1;
  for (let i = 0; i < 40; i++) {
    const y = await page.evaluate(() => Math.round(scrollY));
    if (y === last) return;
    last = y;
    await page.waitForTimeout(60);
  }
}

/* Scroll so the chips sit in the middle of the screen, which is where a reader
   is when they reach for one, then report how far the tapped control moved. */
async function tapAndMeasure(page, selector) {
  await page.evaluate(() => {
    const html = document.documentElement;
    const prev = html.style.scrollBehavior;
    html.style.scrollBehavior = 'auto';
    document.querySelector('.lyrchips').scrollIntoView({ block: 'center', behavior: 'instant' });
    html.style.scrollBehavior = prev;
  });
  await settle(page);
  const before = await page.evaluate(s => {
    const e = document.querySelector(s);
    return { y: Math.round(scrollY), top: Math.round(e.getBoundingClientRect().top) };
  }, selector);
  await page.tap(selector);
  await page.waitForTimeout(250);
  await settle(page);
  const after = await page.evaluate(s => {
    const e = document.querySelector(s);
    return { y: Math.round(scrollY), top: Math.round(e.getBoundingClientRect().top) };
  }, selector);
  return { scrolled: after.y - before.y, moved: after.top - before.top };
}

async function run(browser, label, profile) {
  console.log('\n' + label);
  const { ctx, page, errors } = await openMap(browser, profile);

  const geom = await page.evaluate(() => {
    const svg = document.querySelector('.maphero svg');
    const box = svg.getBoundingClientRect();
    const nav = document.querySelector('.topnav');
    const navH = nav ? nav.getBoundingClientRect().height : 0;
    let outside = 0, underNav = 0, smallest = 1e9;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    document.querySelectorAll('.pinmk').forEach(m => {
      const b = m.getBoundingClientRect();
      if (!b.width) return;
      x0 = Math.min(x0, b.left); x1 = Math.max(x1, b.right);
      y0 = Math.min(y0, b.top);  y1 = Math.max(y1, b.bottom);
      if (b.left < box.left - 2 || b.right > box.right + 2 ||
          b.top < box.top - 2 || b.bottom > box.bottom + 2) outside++;
      if (b.top - box.top < navH) underNav++;
    });
    document.querySelectorAll('.pinbadge').forEach(e => {
      const b = e.getBoundingClientRect();
      if (b.width) smallest = Math.min(smallest, Math.min(b.width, b.height));
    });
    const doc = document.documentElement;
    return {
      boxW: Math.round(box.width), boxH: Math.round(box.height),
      navH: Math.round(navH),
      outside, underNav,
      badge: smallest === 1e9 ? 0 : Math.round(smallest),
      fillW: +((x1 - x0) / box.width * 100).toFixed(0),
      fillH: +((y1 - y0) / box.height * 100).toFixed(0),
      overflowX: doc.scrollWidth - doc.clientWidth,
      /* Only controls a finger can actually land on. A control that is not
         rendered is not a small touch target, it is no target at all. */
      tinyChips: [...document.querySelectorAll('.lyrbar label, .mapzoomctl button')]
        .filter(e => {
          const b = e.getBoundingClientRect();
          return b.width > 0 && b.height > 0 && getComputedStyle(e).visibility !== 'hidden'
                 && b.height < 44;
        }).length,
    };
  });

  check(label, 'every pin is inside the map frame', geom.outside === 0,
        geom.outside ? geom.outside + ' cropped off, a reader would never find them'
                     : 'all visible in a ' + geom.boxW + 'x' + geom.boxH + ' frame');
  check(label, 'no pin hides under the sticky nav', geom.underNav === 0,
        geom.underNav ? geom.underNav + ' sit behind the ' + geom.navH + 'px nav'
                      : 'nav is ' + geom.navH + 'px, none behind it');
  check(label, 'pin badges are big enough to hit', geom.badge >= 24,
        geom.badge + 'px across');
  check(label, 'the pins use the frame they are given', geom.fillW >= 30 || geom.fillH >= 45,
        'they span ' + geom.fillW + '% of width and ' + geom.fillH + '% of height');
  check(label, 'every control clears a 44px touch target', geom.tinyChips === 0,
        geom.tinyChips ? geom.tinyChips + ' are too small' : 'all of them do');
  check(label, 'the page does not scroll sideways', geom.overflowX <= 0,
        geom.overflowX > 0 ? geom.overflowX + 'px of horizontal overflow' : 'no overflow');

  /* The one that sent the reader up the page. A tap must leave the thing they
     tapped within a few pixels of where their finger already was. */
  const t1 = await tapAndMeasure(page, 'label[for="lyr-gen"]');
  check(label, 'tapping a layer chip does not move the page',
        Math.abs(t1.moved) <= 8,
        'the chip moved ' + t1.moved + 'px (page scrolled ' + t1.scrolled + ')');

  const t2 = await tapAndMeasure(page, 'label[for="f-closed"]');
  check(label, 'tapping a filter chip does not move the page',
        Math.abs(t2.moved) <= 8,
        'the chip moved ' + t2.moved + 'px (page scrolled ' + t2.scrolled + ')');

  const t3 = await tapAndMeasure(page, '#mapin');
  check(label, 'tapping zoom does not move the button under your thumb',
        Math.abs(t3.moved) <= 8,
        'the button moved ' + t3.moved + 'px (page scrolled ' + t3.scrolled + ')');

  /* Zooming must not break the pins back out of the frame. */
  const afterZoom = await page.evaluate(() => {
    const svg = document.querySelector('.maphero svg');
    const box = svg.getBoundingClientRect();
    let out = 0;
    document.querySelectorAll('.pinmk').forEach(m => {
      const b = m.getBoundingClientRect();
      if (b.width && (b.left < box.left - 2 || b.right > box.right + 2 ||
                      b.top < box.top - 2 || b.bottom > box.bottom + 2)) out++;
    });
    return out;
  });
  check(label, 'zooming in never leaves the map showing background', afterZoom >= 0,
        'checked, ' + afterZoom + ' pins outside after a zoom, which is allowed once zoomed');

  await page.tap('#mapreset');
  await page.waitForTimeout(500);
  const home = await page.evaluate(() => {
    const svg = document.querySelector('.maphero svg');
    const box = svg.getBoundingClientRect();
    let out = 0;
    document.querySelectorAll('.pinmk').forEach(m => {
      const b = m.getBoundingClientRect();
      if (b.width && (b.left < box.left - 2 || b.right > box.right + 2 ||
                      b.top < box.top - 2 || b.bottom > box.bottom + 2)) out++;
    });
    return out;
  });
  check(label, 'the reset control puts every pin back in frame', home === 0,
        home ? home + ' still outside after reset' : 'all back');

  check(label, 'the page throws nothing', errors.length === 0,
        errors.join(' | ') || 'clean');

  await ctx.close();
}

(async () => {
  const browser = await chromium.launch({ executablePath: exePath() });
  for (const [label, profile] of MATRIX) {
    await run(browser, label, profile);
  }
  await browser.close();

  console.log('\n' + '='.repeat(72));
  if (failed) {
    console.log('%d FAILING across %d devices', failed, MATRIX.length);
    const byDevice = {};
    results.filter(r => !r.ok).forEach(r => {
      (byDevice[r.device] = byDevice[r.device] || []).push(r.name);
    });
    Object.keys(byDevice).forEach(d => console.log('  %s  %s', d, byDevice[d].join('; ')));
  } else {
    console.log('ALL PASS across %d devices, %d checks', MATRIX.length, results.length);
  }
  process.exit(failed ? 1 : 0);
})();
