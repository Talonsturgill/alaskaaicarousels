/* tests/beacon_fires.js
 *
 * Does the reader counter actually count a reader?
 *
 * WHY THIS EXISTS
 *   The counter shipped, was verified with curl, and recorded zero from every
 *   real visit for the better part of an hour. curl cannot catch the bug,
 *   because the bug was a CORS preflight and curl never sends one. The beacon
 *   declared application/json, which is not a CORS-safelisted content type, so
 *   browsers sent an OPTIONS preflight first, and sendBeacon has no headers API
 *   and cannot complete the negotiation that follows. The edge log showed twelve
 *   OPTIONS from real visits with not one POST behind them.
 *
 *   Every check that passed during that hour passed because it was not a
 *   browser. So this is a browser. It loads the built page, lets the real
 *   site.js run, and asserts what arrives at a stand-in collector on a DIFFERENT
 *   ORIGIN, which is what makes the browser apply the same CORS rules it applies
 *   in production.
 *
 *   It deliberately does NOT talk to Supabase. The server half is testable with
 *   curl and is tested that way; this covers the half that curl is blind to, and
 *   staying local means it runs in CI with no key, no network and no live rows.
 *
 * RUN
 *   node tests/beacon_fires.js
 *   node tests/beacon_fires.js --self-test    # regress the bug, expect red
 *
 *   --self-test rewrites the served site.js back to application/json and
 *   requires this file to fail. A gate that cannot fail certifies nothing, and
 *   this particular gate exists because the last set of checks could not fail.
 *
 * Exits non-zero on any failure, so CI can gate on it.
 */
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const SELF_TEST = process.argv.includes('--self-test');

/* The beacon refuses to count localhost, which is correct and which means a test
   served from 127.0.0.1 measures nothing at all (the first version of this file
   did exactly that and reported zero requests). So the page is served under a
   hostname that is not localhost, mapped back to the loopback interface inside
   the browser with --host-resolver-rules. Nothing leaves the machine.
   A separate host for the collector keeps the request cross-origin, which is
   what makes the browser apply the CORS rules this gate is here to check. */
const SITE_HOST = 'site.beacon-gate.test';
const COLL_HOST = 'collector.beacon-gate.test';

/* Same rule as tests/mobile_docket_map.js: this repo's dev container ships a
   preinstalled Chromium at a fixed path and forbids downloading another, while
   CI installs its own and has no such path. */
function exePath() {
  if (process.env.CHROMIUM) return process.env.CHROMIUM;
  const pinned = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
  return fs.existsSync(pinned) ? pinned : undefined;
}

let failed = 0;
function check(name, ok, detail) {
  if (!ok) failed++;
  console.log('  %s %s  %s', ok ? 'ok  ' : 'FAIL', name.padEnd(44), detail);
}

/* The collector stand-in. Records what the browser really sent rather than
   asserting inline, so a missing POST is reported as a missing POST instead of
   as a timeout with no explanation.
 *
 * The CORS headers here mirror the real function on purpose. Widening them
 * would let a preflight bug through: if this replied
 * Access-Control-Allow-Headers: * the browser would happily negotiate a
 * non-safelisted content type over fetch, and the test would pass on a beacon
 * that cannot work with sendBeacon in production. */
function collector(seen) {
  return http.createServer((req, res) => {
    const origin = req.headers.origin || null;
    const cors = {
      'Access-Control-Allow-Origin': origin || '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'content-type',
      'Access-Control-Max-Age': '86400',
    };
    if (req.method === 'OPTIONS') {
      seen.push({ method: 'OPTIONS', ct: req.headers['content-type'] || null });
      res.writeHead(204, cors); res.end(); return;
    }
    let body = '';
    req.on('data', d => { body += d; });
    req.on('end', () => {
      seen.push({
        method: req.method,
        ct: req.headers['content-type'] || null,
        ua: req.headers['user-agent'] || null,
        body,
      });
      res.writeHead(204, cors); res.end();
    });
  });
}

function listen(server, port) {
  return new Promise((ok, bad) => {
    server.once('error', bad);
    server.listen(port, '127.0.0.1', () => ok());
  });
}

async function main() {
  const root = path.resolve(__dirname, '..');
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'beacon-'));

  /* Build the site rather than serving committed docs/, so a correct builder
     with a stale commit is still tested, matching how the dates gate works. */
  console.log('building the site');
  execFileSync('python3', [path.join(root, 'scripts/site_build.py'),
                           '--date', '2026-07-25', '--out', out],
               { cwd: root, stdio: 'pipe' });

  const jsPath = path.join(out, 'site.js');
  let js = fs.readFileSync(jsPath, 'utf8');

  const TRACK_RE = /https:\/\/[a-z0-9]+\.supabase\.co\/functions\/v1\/track/g;
  const hits = js.match(TRACK_RE) || [];
  /* One counter, not two. A squash merge once landed the beacon twice and every
     pageview was double counted, so the count is asserted, not assumed. */
  check('exactly one collector call in site.js', hits.length === 1,
        `${hits.length} found`);
  if (!hits.length) { console.log('\nno beacon in the page at all'); process.exit(1); }

  js = js.replace(TRACK_RE, `http://${COLL_HOST}:8905/track`);
  if (SELF_TEST) {
    /* Reintroduce exactly the shipped bug: a non-safelisted content type. */
    js = js.replace(/text\/plain;charset=UTF-8/g, 'application/json');
  }
  fs.writeFileSync(jsPath, js);

  const seen = [];
  const coll = collector(seen);
  const site = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]);
    let f = path.join(out, rel);
    if (f.endsWith('/')) f = path.join(f, 'index.html');
    if (!f.startsWith(out) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
      res.writeHead(404); res.end('no'); return;
    }
    const type = f.endsWith('.js') ? 'text/javascript'
      : f.endsWith('.css') ? 'text/css'
      : f.endsWith('.html') ? 'text/html' : 'application/octet-stream';
    res.writeHead(200, { 'content-type': type });
    fs.createReadStream(f).pipe(res);
  });
  /* Different port means different origin, which is the entire point: the
     browser applies real CORS rules to the beacon exactly as in production. */
  await listen(site, 8904);
  await listen(coll, 8905);

  const browser = await chromium.launch({
    headless: true,
    executablePath: exePath(),
    args: [`--host-resolver-rules=MAP ${SITE_HOST} 127.0.0.1,MAP ${COLL_HOST} 127.0.0.1`],
  });
  const ctx = await browser.newContext({
    /* The collector drops /headless/ on purpose and that guard is correct, so
       present as an ordinary desktop reader to exercise the reader path. */
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      + '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 900 },
  });
  const page = await ctx.newPage();
  const pageErrors = [];
  page.on('pageerror', e => pageErrors.push(e.message));

  await page.goto(`http://${SITE_HOST}:8904/?c=gatetest`, { waitUntil: 'load' });

  /* The opt-out check decides whether a beacon is sent at all, so read what the
     page itself sees. A CI browser with DNT on would otherwise look identical to
     a broken beacon, which is the confusion this whole gate exists to end. */
  const signals = await page.evaluate(() => ({
    dnt: navigator.doNotTrack, gpc: navigator.globalPrivacyControl,
    winDnt: window.doNotTrack, beacon: typeof navigator.sendBeacon === 'function',
  }));
  const optedOut = signals.dnt === '1' || signals.gpc === true || signals.winDnt === '1';
  check('this browser is not itself opted out', !optedOut, JSON.stringify(signals));

  /* sendBeacon is fire and forget; closing the page is what forces a flush. */
  for (let i = 0; i < 40 && !seen.some(s => s.method === 'POST'); i++) {
    await page.waitForTimeout(100);
  }
  await page.close();
  for (let i = 0; i < 20 && !seen.some(s => s.method === 'POST'); i++) {
    await new Promise(r => setTimeout(r, 100));
  }
  await ctx.close();
  await browser.close();
  site.close(); coll.close();

  const posts = seen.filter(s => s.method === 'POST');
  const opts = seen.filter(s => s.method === 'OPTIONS');

  check('the beacon reached the collector', posts.length > 0,
        `${posts.length} POST, ${opts.length} OPTIONS`);
  /* The failure signature of the shipped bug, named so a regression reads as
     itself rather than as a mystery. */
  check('no preflight-without-POST (the shipped bug)',
        !(opts.length > 0 && posts.length === 0),
        opts.length && !posts.length
          ? `${opts.length} preflight(s) and no POST: every reader counts as zero`
          : 'clean');
  check('counted exactly once, not twice', posts.length <= 1,
        `${posts.length} POST`);

  if (posts.length) {
    const p = posts[0];
    check('content type is CORS safelisted',
          /^text\/plain/.test(p.ct || ''), String(p.ct));
    let payload = null;
    try { payload = JSON.parse(p.body); } catch (_e) { /* reported below */ }
    check('body is JSON the collector can parse', payload !== null,
          payload ? JSON.stringify(payload) : `unparseable: ${p.body.slice(0, 80)}`);
    if (payload) {
      check('path is the page that was read', payload.p === '/', String(payload.p));
      check('campaign tag survives the round trip', payload.c === 'gatetest',
            String(payload.c));
      /* The privacy promise is part of the contract, so it is asserted rather
         than trusted: nothing may ride along that identifies a reader. */
      const allowed = new Set(['p', 'r', 'c']);
      const extra = Object.keys(payload).filter(k => !allowed.has(k));
      check('nothing rides along that identifies a reader',
            extra.length === 0, extra.length ? `unexpected: ${extra}` : 'p, r, c only');
    }
  }

  check('no page errors', pageErrors.length === 0,
        pageErrors.length ? pageErrors[0] : 'clean');

  fs.rmSync(out, { recursive: true, force: true });

  if (SELF_TEST) {
    if (failed > 0) {
      console.log('\nself-test: the gate goes red on the shipped bug, as designed');
      process.exit(0);
    }
    console.log('\nself-test: THE GATE PASSED A BROKEN BEACON. It proves nothing.');
    process.exit(1);
  }
  if (failed) { console.log(`\n${failed} failed`); process.exit(1); }
  console.log('\nthe beacon fires, once, and counts a reader');
}

main().catch(e => { console.error('HARNESS FAILED:', e.stack || e.message); process.exit(1); });
