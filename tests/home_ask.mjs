/* THE HOMEPAGE ASK BOX, DRIVEN FOR REAL.
 *
 * The docket box has tests/ask_engine.mjs, which asks every catalogued
 * question in a live page. This is the other box: no engine, no index, one
 * field on the front page that talks to the worker.
 *
 * The WORKER is stubbed with canned ndjson and nothing below the fetch is.
 * The streaming reader, the sentence rendering, the citation links, the
 * withheld wording, the conversation memory and the growth from one field to
 * a thread are all the code that ships. What is deliberately NOT tested here
 * is whether the model writes a good answer, because that is not this file's
 * to know and workers/ask has its own suite for the guard.
 *
 * The two things most likely to break it quietly, and so the two things
 * asserted hardest:
 *   the follow-up sends the WHOLE conversation, not just the new line
 *   only text that survived the guard goes back to the model
 *
 * Needs a built site.
 *   python3 scripts/site_build.py --date $(date +%F) --out /tmp/site
 *   SITE=/tmp/site node tests/home_ask.mjs
 */
import { chromium } from 'playwright';
const SITE = process.env.SITE;
if (!SITE) { console.error('set SITE to a built site directory'); process.exit(2); }
// The pre-installed browser when there is one, whatever playwright resolves
// otherwise, so this runs the same on a runner as on a workstation.
const exe = process.env.PLAYWRIGHT_CHROMIUM || '/opt/pw-browsers/chromium';
const b = await chromium.launch((await import('node:fs')).existsSync(exe) ? { executablePath: exe } : {});
let fail = 0, pass = 0;
const ok = (l, c, d = '') => { if (c) { pass++; return; } fail++; console.log(`  FAIL  ${l}${d ? '  ' + d : ''}`); };

const page = await b.newPage({ viewport: { width: 430, height: 900 }, deviceScaleFactor: 2, timezoneId: 'America/Anchorage' });
const errs = [];
page.on('pageerror', e => { if (!/turnstile/i.test(String(e))) errs.push(String(e)); });
// A file:// page cannot fetch, and the homepage's video section fetches
// videos/videos.json on scroll. That failure is this harness, not the page:
// on the real site it is an ordinary request to a file that is right there.
// Same reasoning as the turnstile exclusion above, and the same list
// tests/ask_engine.mjs keeps for the same reason.
const HARNESS = /CORS|ERR_|URL scheme|font|turnstile|challenges\.cloudflare/i;
page.on('console', m => {
  if (m.type() === 'error' && !HARNESS.test(m.text())) errs.push(m.text());
});
await page.route('**://challenges.cloudflare.com/**', r => r.abort());

// The worker, stubbed. Two turns, so conversation memory is observable.
let seen = [];
await page.route('**/answer', async (route) => {
  seen.push(JSON.parse(route.request().postData()));
  const lines = seen.length === 1
    ? [{ stage: 'Reading the record' },
       { sentence: 'The Air Force decides it, with Defense Logistics Agency Energy.' },
       { sentence: 'See [[eielson-oklo-microreactor]] for the filings.' },
       { sentence: 'Want the date it lands?' },
       { done: true }]
    : [{ stage: 'Reading the record' },
       { sentence: 'No date is published for it yet.' },
       { withheld: 'numeral' }];
  await route.fulfill({ status: 200, contentType: 'application/x-ndjson',
    body: lines.map(l => JSON.stringify(l)).join('\n') + '\n' });
});

await page.goto('file://' + SITE + '/index.html');
await page.waitForTimeout(400);

// ---- collapsed
const shellBox = await page.locator('.hask').boundingBox();
ok('the box starts small', shellBox.height < 190, `${Math.round(shellBox.height)}px tall`);
ok('the thread is hidden until asked', await page.locator('#haskout').isHidden());
await page.screenshot({ path: process.env.OUT1 || '/tmp/hask-collapsed.png' });

// ---- ask
// The widget, stubbed the way Cloudflare drives it: the box arms on focus and
// hands render() a callback, so this is the real token path with the network
// taken out. (With no widget at all the client waits its 15s fallback and
// then posts without a token, which is a separate case and not this one.)
await page.focus('#haskq');
await page.evaluate(() => {
  window.turnstile = {
    render: (el, o) => { setTimeout(() => o.callback('test-token'), 5); return 1; },
    reset: () => { setTimeout(() => window.__tscb && window.__tscb('test-token'), 5); },
  };
  const o = { callback: null };
  window.turnstile.render = (el, opt) => { window.__tscb = opt.callback;
    setTimeout(() => opt.callback('test-token'), 5); return 1; };
  window.haskTurnstileReady();
});
await page.waitForTimeout(60);
await page.fill('#haskq', 'who decides the eielson microreactor');
await page.click('#haskgo');
await page.waitForSelector('.haskfrom', { timeout: 8000 });

ok('the question is shown back', (await page.locator('.haskq').first().textContent()).includes('eielson'));
const ans = await page.locator('.haska').first().textContent();
ok('every sentence landed', ans.includes('Air Force') && ans.includes('Want the date'), ans);
ok('the citation became a docket link',
  (await page.locator('.haska a.cite').first().getAttribute('href')) === 'docket/eielson-oklo-microreactor/');
ok('the starter line stepped aside', await page.locator('.hasknote').isHidden());
ok('provenance appears', (await page.locator('.haskfrom').textContent()).includes('Every figure checked'));
ok('the field is ready again', (await page.inputValue('#haskq')) === '');
ok('it sent only the question the first time', seen[0].messages.length === 1, JSON.stringify(seen[0].messages));

// ---- the closing offer, as one press
ok('the offer became a chip',
  (await page.locator('.hasknext').textContent()) === 'Yes, show me');
await page.click('.hasknext');
await page.waitForTimeout(120);
ok('pressing it loads the question',
  (await page.inputValue('#haskq')) === 'Show me the date it lands.',
  await page.inputValue('#haskq'));
/* Two presses on purpose. Sending is the metered call, and this page says so
   above the button, so a chip that sent by itself would spend on a mis-tap. */
ok('but does not send it', seen.length === 1, `${seen.length} requests`);
ok('the chip goes once it has been taken up',
  await page.locator('.hasknext').count() === 0);

// ---- follow up
await page.fill('#haskq', 'when');
await page.click('#haskgo');
await page.waitForSelector('.haskstop', { timeout: 8000 });
ok('the follow-up carried the whole conversation', seen[1].messages.length === 3,
  JSON.stringify(seen[1].messages.map(m => m.role)));
// The assistant turn the model is handed back is the text that PASSED the
// guard, sentence for sentence. A sentence the reader never saw must not be
// one the model can build its next answer on.
ok('only text that survived the guard went back to the model',
  seen[1].messages[1].role === 'assistant' &&
  seen[1].messages[1].content ===
    'The Air Force decides it, with Defense Logistics Agency Energy. ' +
    'See [[eielson-oklo-microreactor]] for the filings. Want the date it lands?',
  JSON.stringify(seen[1].messages[1]));
ok('the withheld reason is named',
  (await page.locator('.haskstop').textContent()).includes('stated a figure the record does not carry'),
  await page.locator('.haskstop').textContent());
ok('two exchanges are on screen', (await page.locator('.haskq').count()) === 2);
/* The offer is always the answer's last sentence, so a cut answer never has
   one. Inventing a follow-up here would offer to answer something the record
   never offered. */
ok('a cut answer gets no chip', (await page.locator('.hasknext').count()) === 0);
const grown = await page.locator('.hask').boundingBox();
ok('the box grew with the conversation', grown.height > shellBox.height + 150,
  `${Math.round(shellBox.height)} -> ${Math.round(grown.height)}`);
// Settled, not mid-flight: the second ask starts a smooth scroll and a
// screenshot taken during it shows the page halfway between two positions.
await page.waitForTimeout(900);
await page.evaluate(() => document.getElementById('hask')
  .scrollIntoView({ block: 'center' }));
await page.waitForTimeout(300);
await page.screenshot({ path: process.env.OUT2 || '/tmp/hask-open.png' });

// ---- the month's ceiling
// This path fires at most once a month and is therefore the one nobody sees
// until it matters. The worker's capped body names the engine above the field
// and the archive button below it, and the front page has neither, so what
// must NOT happen here is the worker's sentence reaching a reader.
await page.click('.haskagain');
await page.waitForTimeout(150);
await page.unroute('**/answer');
await page.route('**/answer', async (route) => {
  await route.fulfill({ status: 200, contentType: 'application/x-ndjson',
    body: JSON.stringify({ text: '', withheld: false, capped: true,
      error: 'The written answer lane has reached this month\'s limit. ' +
             'The box above still answers from the record, and the full ' +
             'archive search below still works.' }) + '\n' });
});
await page.fill('#haskq', 'anything at all');
await page.click('#haskgo');
await page.waitForSelector('.haskfrom', { timeout: 8000 });
{
  const said = await page.locator('.haska').first().textContent();
  ok('the cap is explained', said.includes("this month's last written answer"), said);
  ok('and NOT with the worker\'s docket-shaped copy',
    !said.includes('box above') && !said.includes('archive search'), said);
  ok('it points at the page that still answers free',
    (await page.locator('.haska a').first().getAttribute('href')) === 'docket/');
}

// ---- start over
await page.click('.haskagain');
await page.waitForTimeout(200);
ok('start over clears the thread', await page.locator('#haskout').isHidden());
ok('and brings the starter line back', await page.locator('.hasknote').isVisible());

// Everything the page does lazily, done, before the last assertion. The
// video section loads on scroll, so a test that never reached it was passing
// on a page that had not finished being itself. It went red on CI and green
// here for exactly that reason, which is a flaky test rather than a lucky one.
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
await page.waitForTimeout(700);

// ---- feedback
// The note under the field used to describe the box to somebody who had not used it yet. What
// a reader can act on is that the model is still being worked on, and a way to say when it is
// wrong. The dialog is driven from ASK_COMMON_JS and shared with the docket box, so each
// client hands it that page's own last exchange.
let fbSent = null;
await page.route('**/formsubmit.co/**', async (r) => {
  fbSent = JSON.parse(r.request().postData());
  await r.fulfill({ status: 200, contentType: 'application/json', body: '{"success":"true"}' });
});
ok('the note names the model',
  (await page.locator('.hasknote').textContent()).includes('Model in training'));
// Start over has already run above, so the box is at rest and the note is back.
await page.click('[data-askfb]');
await page.waitForTimeout(250);
ok('the dialog opens', await page.locator('#askfb').isVisible());
await page.fill('#askfbtext', 'it missed a filing');
await page.click('#askfbsend');
await page.waitForTimeout(400);
ok('feedback reaches the forwarder', fbSent && fbSent.feedback === 'it missed a filing',
  JSON.stringify(fbSent));
ok('and is labelled for this product', fbSent && /Alaska AI/.test(fbSent._subject),
  fbSent && fbSent._subject);

ok('nothing threw', errs.length === 0, errs.join(' | '));
console.log(`\n${fail ? fail + ' FAILED of ' : ''}${pass + fail} checks${fail ? '' : ' clean'}`);
await b.close();
process.exit(fail ? 1 : 0);
