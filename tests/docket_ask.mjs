/* The docket box's two OUTBOUND lanes, driven for real.
 *
 * ask_engine.mjs covers the engine that answers while a reader types, which
 * sends nothing and is most of what the box does. This covers the other half:
 * the written answer and the archive search, the two things that leave the
 * page. The worker is stubbed with canned ndjson and canned failures, so
 * everything below the fetch is the client that ships.
 *
 * Needs a built site: SITE=/tmp/site node tests/docket_ask.mjs
 */
import { chromium } from 'playwright';
const SITE = process.env.SITE;
const exe = process.env.PLAYWRIGHT_CHROMIUM || '/opt/pw-browsers/chromium';
const b = await chromium.launch(
  (await import('node:fs')).existsSync(exe) ? { executablePath: exe } : {});
let fail = 0, pass = 0;
const ok = (l, c, d = '') => {
  if (c) { pass++; return; }
  fail++; console.log(`  FAIL  ${l}${d ? '  ' + d : ''}`);
};
const head = (t) => console.log('\n' + t);

const page = await b.newPage({ viewport: { width: 1240, height: 900 },
                               timezoneId: 'America/Anchorage' });
const errs = [];
page.on('pageerror', e => { if (!/turnstile/i.test(String(e))) errs.push(String(e)); });
page.on('console', m => {
  /* The 503 is this file's own stub answering the way the deployed worker
     does. Chromium logs every failed request whether or not the page handles
     it, so leaving it in would fail the suite on the exact condition the
     suite exists to prove is handled. */
  if (m.type() === 'error' &&
      !/CORS|URL scheme|ERR_|font|turnstile|challenges\.cloudflare/i.test(m.text()) &&
      !/status of 503/.test(m.text())) {
    errs.push(m.text());
  }
});
await page.route('**://challenges.cloudflare.com/**', r => r.abort());

/* The archive lane, switched off. This is the deployed state: the worker has
   no routine token, so /deep answers 503 and always will. */
let deepHits = 0;
await page.route('**/deep', async (route) => {
  deepHits++;
  await route.fulfill({ status: 503, contentType: 'application/json',
    body: JSON.stringify({ error: 'research is not configured' }) });
});

/* The written lane. Turn one closes with an offer, turn two is cut by the
   guard before any offer arrives. */
let answers = [];
await page.route('**/answer', async (route) => {
  answers.push(JSON.parse(route.request().postData()));
  const lines = answers.length === 1
    ? [{ stage: 'Reading the record' },
       { sentence: 'The Air Force decides it, with Defense Logistics Agency Energy.' },
       { sentence: 'Want the note on why the schedule moved?' },
       { done: true }]
    : [{ stage: 'Reading the record' },
       { sentence: 'No date is published for it yet.' },
       { withheld: 'numeral' }];
  await route.fulfill({ status: 200, contentType: 'application/x-ndjson',
    body: lines.map(l => JSON.stringify(l)).join('\n') + '\n' });
});

await page.goto('file://' + SITE + '/docket/index.html');
await page.waitForTimeout(400);

const type = (q) => page.evaluate((q) => {
  const el = document.getElementById('qq');
  const set = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
  set.call(el, q);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Shift', bubbles: true }));
}, q);

// ---------------------------------------------------------------- A. shapes
/* The rewrite from the model's offer to the reader's question. This is the
   part that can go wrong quietly: a regex that swallows a word turns a good
   offer into a sentence nobody would have typed, and it ships in a button. */
head('A. the offer becomes a question');
const shapes = await page.evaluate(() => [
  'Want the note on why the schedule moved?',
  'Want the date it lands?',
  'Want me to break down the filings?',
  'Do you want the timeline?',
  'Do you want me to pull the order?',
  'Would you like the full list?',
  'Should I list them?',
  'Shall I pull the docket entry?',
  'The record does not answer that.',
  'What counts as a decision here?',
  'Want?',
  '',
].map(s => [s, window.askFollowUp(s)]));
const want = {
  'Want the note on why the schedule moved?': 'Show me the note on why the schedule moved.',
  'Want the date it lands?': 'Show me the date it lands.',
  'Want me to break down the filings?': 'Yes, break down the filings.',
  'Do you want the timeline?': 'Show me the timeline.',
  'Do you want me to pull the order?': 'Yes, pull the order.',
  'Would you like the full list?': 'Yes, the full list.',
  'Should I list them?': 'Yes, list them.',
  'Shall I pull the docket entry?': 'Yes, pull the docket entry.',
  /* Not offers. A trailing question that was part of the answer, and a
     sentence that is not a question at all, both get no chip: a button that
     guesses is worse than no button. */
  'The record does not answer that.': null,
  'What counts as a decision here?': null,
  'Want?': null,
  '': null,
};
for (const [input, got] of shapes) {
  ok(`"${input.slice(0, 42)}"`, got === want[input], `got ${JSON.stringify(got)}`);
}

// ------------------------------------------------------------- B. archive off
head('B. the archive lane, switched off');
await type('zzqqxvwk');
await page.waitForTimeout(120);
ok('gibberish reaches the no-match panel', await page.locator('.qnone').count() === 1);
ok('and the archive is offered there', await page.locator('#qdeep').count() === 1);

await page.click('#qdeep');
await page.waitForTimeout(300);
const off = await page.locator('.qlaneoff').textContent().catch(() => '');
ok('a 503 is answered in a sentence', off.includes('not running right now'), off);
ok('and not with the deploy note',
  !off.includes('not configured'), off);
ok('and it says what does work', off.includes('Press Enter'), off);
ok('the button is gone rather than saying TRY AGAIN',
  await page.locator('#qdeep').count() === 0);
ok('the thread was not opened to hold an error',
  await page.locator('#qout').isHidden());

await type('qqzzvvwwx');
await page.waitForTimeout(150);
ok('a later no-match still panels', await page.locator('.qnone').count() === 1);
ok('but the dead door is not offered again',
  await page.locator('#qdeep').count() === 0);
ok('and it was pressed exactly once', deepHits === 1, String(deepHits));

// ---------------------------------------------------------------- C. the chip
head('C. the closing offer, as one press');
/* The widget the way Cloudflare drives it, with the network taken out. The
   box arms on focus and only then hands render() a callback, so focusing
   first is not incidental: without it there is no qTurnstileReady to call. */
await page.focus('#qq');
/* reset() has to hand back a fresh token, because the real one does. A token
   is single use and the box spends it on every send, so a stub whose reset is
   a no-op leaves the second question waiting fifteen seconds for a token that
   is never coming, which is a stub bug that reads exactly like a page bug. */
await page.evaluate(() => {
  let cb = null;
  window.turnstile = {
    render: (el, opt) => { cb = opt.callback;
      setTimeout(() => cb('test-token'), 5); return 1; },
    reset: () => { setTimeout(() => cb && cb('test-token'), 5); },
  };
  window.qTurnstileReady();
});
await page.waitForTimeout(60);
await type('who decides the eielson microreactor');
await page.click('#qgo');
await page.waitForSelector('.qnext', { timeout: 8000 });

ok('the chip carries a label, not the whole offer',
  (await page.locator('.qnext').textContent()) === 'Yes, show me');
ok('it sits under the answer and above the provenance',
  await page.evaluate(() => {
    const n = document.querySelector('.qnext'), f = document.querySelector('.qfrom');
    return !!(n && f) &&
      (n.compareDocumentPosition(f) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
  }));
ok('the field is empty before the press', (await page.inputValue('#qq')) === '');

await page.click('.qnext');
await page.waitForTimeout(150);
ok('pressing it loads the question',
  (await page.inputValue('#qq')) === 'Show me the note on why the schedule moved.',
  await page.inputValue('#qq'));
/* The whole point of two presses. Submitting is a metered model call and the
   page promises, above the button, that pressing is what sends. A chip that
   sent on its own would spend on a mis-tap and make that promise false. */
ok('but does NOT send it', answers.length === 1, `${answers.length} requests`);
ok('the field has focus, ready for enter',
  await page.evaluate(() => document.activeElement.id === 'qq'));
ok('the caret is at the end so it can be added to',
  await page.evaluate(() => {
    const el = document.getElementById('qq');
    return el.selectionStart === el.value.length;
  }));
ok('the chip goes once it has been taken up',
  await page.locator('.qnext').count() === 0);

// ------------------------------------------------------------ D. a cut answer
head('D. an answer the guard cut');
await page.click('#qgo');
await page.waitForSelector('.qstop', { timeout: 8000 });
ok('the second question was sent', answers.length === 2);
ok('the cut is explained', (await page.locator('.qstop').textContent())
  .includes('stated a figure the record does not carry'));
/* The offer is always the last sentence, so a cut answer never has one.
   Inventing a follow-up here would be the page offering to answer something
   the record never offered. */
ok('no chip is invented for it', await page.locator('.qnext').count() === 0);
ok('both exchanges are on screen', await page.locator('.qturn').count() === 2);

head('E. nothing threw across any of that');
ok('clean console', errs.length === 0, errs.join(' | '));

console.log('');
console.log(fail === 0 ? `docket lanes clean, ${pass} checks`
                       : `docket lanes FAILED, ${fail} of ${pass + fail}`);
await b.close();
process.exit(fail ? 1 : 0);
