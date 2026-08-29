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
  const request = JSON.parse(route.request().postData());
  answers.push(request);
  const latest = request.messages.at(-1)?.content || '';
  const lines = /what is open right now/i.test(latest)
    ? [{ capped: true }, { done: true, verified: 0 }]
    : answers.length === 1
    ? [{ stage: "Opening today's published record", step: 'record', progress: 1, total: 3 },
       { stage: 'Drafting only from the published record', step: 'draft', progress: 2, total: 3 },
       { stage: 'Verifying figures and source links', step: 'verify', progress: 3, total: 3 },
       { sentence: 'The Air Force decides it, with Defense Logistics Agency Energy.' },
       { sentence: 'Want the note on why the schedule moved?' },
       { done: true, verified: 2 }]
    : [{ stage: "Opening today's published record", step: 'record', progress: 1, total: 3 },
       { stage: 'Drafting only from the published record', step: 'draft', progress: 2, total: 3 },
       { stage: 'Verifying figures and source links', step: 'verify', progress: 3, total: 3 },
       { sentence: 'No date is published for it yet.' },
       { withheld: 'numeral' },
       { done: true, verified: 1 }];
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

head('B. classifier keeps the agent on the record');
const buckets = await page.evaluate(() => [
  window.__askClassify('how do I bake sourdough', 0),
  window.__askClassify('who decides the eielson microreactor', 0),
  window.__askClassify('are you sure?', 2),
]);
ok('an obviously off-record first turn is refused', buckets[0].bucket === 'refuse', JSON.stringify(buckets[0]));
ok('an Alaska record question goes to the written agent', buckets[1].bucket === 'written', JSON.stringify(buckets[1]));
ok('a vocabulary-light follow-up stays with the written agent', buckets[2].bucket === 'written', JSON.stringify(buckets[2]));

await type('how do I bake sourdough');
await page.click('#qgo');
await page.waitForSelector('.qreply');
ok('the off-record boundary is rendered inside the conversation',
  (await page.locator('.qreply').textContent()).includes('published record'));
ok('the local refusal spends no Worker request', answers.length === 0, `${answers.length} requests`);
ok('the refusal explains that nothing was sent',
  (await page.locator('.qfrom').textContent()).includes('Nothing was sent'));
await page.getByRole('button', { name: 'Start over' }).click();

// ------------------------------------------------------------- C. archive off
head('C. the archive lane, switched off');
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
ok('the unavailable archive lane restores the page around it', await page.evaluate(() =>
  !document.getElementById('qagent').classList.contains('chatting') &&
  !document.querySelector('nav').inert && !document.querySelector('[data-qchat-inert]')));

await type('qqzzvvwwx');
await page.waitForTimeout(150);
ok('a later no-match still panels', await page.locator('.qnone').count() === 1);
ok('but the dead door is not offered again',
  await page.locator('#qdeep').count() === 0);
ok('and it was pressed exactly once', deepHits === 1, String(deepHits));

// ---------------------------------------------------------------- D. the chip
head('D. the closing offer, as one press');
await page.setViewportSize({ width: 390, height: 844 });
/* The widget the way Cloudflare drives it, with the network taken out. The
   box arms on focus and only then hands render() a callback, so focusing
   first is not incidental: without it there is no qTurnstileReady to call. */
await page.focus('#qq');
/* reset() has to hand back a fresh token, because the real one does. A token
   is single use and the box spends it on every send, so a stub whose reset is
   a no-op leaves the second question waiting fifteen seconds for a token that
   is never coming, which is a stub bug that reads exactly like a page bug. */
await page.evaluate(() => {
  if (!document.getElementById('qbox').getAttribute('data-sitekey')) return;
  let cb = null, resets = 0;
  window.turnstile = {
    /* A fast first submit arrives before the automatic callback. Production
       must restart the ready widget itself instead of posting an empty token. */
    render: (el, opt) => { cb = opt.callback; return 1; },
    reset: () => { resets++; setTimeout(() => cb && cb('test-token'), 5); },
  };
  window.__testTurnstileResets = () => resets;
  window.qTurnstileReady();
});
await page.waitForTimeout(60);
await type('who decides the eielson microreactor');
ok('mobile composition shows the free instant answer while typing',
  await page.locator('#qres').isVisible());
ok('the mobile instant answer contains an answer card and a record result',
  await page.locator('#qres .qans').count() === 1 &&
  await page.locator('#qres .qhit').count() >= 1);
await page.click('#qgo');
await page.waitForSelector('.qnext', { timeout: 8000 });
ok('a fast submit restarts the human check instead of posting an empty token',
  await page.evaluate(() => window.__testTurnstileResets() >= 1));

ok('mobile submit opens the dedicated conversation sheet',
  await page.locator('#qagent').evaluate(el => getComputedStyle(el).position === 'fixed'));
ok('the sheet is modal and the covered Docket is inert', await page.evaluate(() => {
  const a = document.getElementById('qagent');
  return a.getAttribute('role') === 'dialog' && a.getAttribute('aria-modal') === 'true' &&
    document.querySelector('nav').inert &&
    Array.from(a.parentElement.children).filter(el => el !== a).every(el => el.inert);
}));
ok('the conversation owns exactly the dynamic viewport height',
  await page.locator('#qagent').evaluate(el => Math.abs(el.getBoundingClientRect().height - innerHeight) < 2));
/* The sheet enters over 250ms. The stub can finish before that animation does,
   so wait for the settled layout instead of sampling a composer that is still
   translated a few pixels below the viewport. */
await page.waitForFunction(() => {
  const composer = document.getElementById('qbox');
  return composer && composer.getBoundingClientRect().bottom <= innerHeight + 1;
});
const mobileLayout = await page.evaluate(() => {
  const out = document.getElementById('qout'), composer = document.getElementById('qbox');
  const s = getComputedStyle(out), r = composer.getBoundingClientRect();
  return { ok: /auto|scroll/.test(s.overflowY) && r.bottom <= innerHeight + 1 &&
      r.bottom > innerHeight - 120,
    overflowY: s.overflowY, composerBottom: Math.round(r.bottom), viewportHeight: innerHeight };
});
ok('the thread scrolls while the composer remains pinned', mobileLayout.ok,
  JSON.stringify(mobileLayout));
ok('the trace completes all three real stages', await page.evaluate(() => {
  const trace = document.querySelector('.qtrace.done');
  return !!trace && trace.querySelectorAll('.qsteps i.on').length === 3 &&
    trace.textContent.includes('2 SENTENCES') &&
    trace.textContent.includes("Verified against today's published record");
}));
ok('the mobile header exposes one explicit way to reset',
  await page.locator('#qagentreset').isVisible());

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

// ------------------------------------------------------------ E. a cut answer
head('E. an answer the guard cut');
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
await page.click('#qagentreset');
ok('start over restores the Docket and accessibility tree', await page.evaluate(() => {
  const a = document.getElementById('qagent');
  return !a.classList.contains('chatting') && !a.hasAttribute('role') &&
    !document.querySelector('nav').inert && document.getElementById('qout').hidden &&
    !document.querySelector('[data-qchat-inert]');
}));

head('F. monthly cap falls back inside the same conversation');
await type('what is open right now?');
await page.click('#qgo');
await page.waitForFunction(() => document.querySelector('.qreply')?.textContent.includes('open to public comment'));
ok('the deterministic fallback answers directly in the thread',
  (await page.locator('.qreply').textContent()).includes('open to public comment'));
ok('the fallback provenance names the limit without calling it a cache', await page.evaluate(() => {
  const text = document.querySelector('.qfrom')?.textContent || '';
  return text.includes('monthly written-answer limit') && !/cache|cached/i.test(text);
}));
ok('the fallback leaves no fake Worker progress receipt', await page.locator('.qtrace').count() === 0);
await page.click('#qagentreset');

head('G. nothing threw across any of that');
ok('clean console', errs.length === 0, errs.join(' | '));

console.log('');
console.log(fail === 0 ? `docket lanes clean, ${pass} checks`
                       : `docket lanes FAILED, ${fail} of ${pass + fail}`);
await b.close();
process.exit(fail ? 1 : 0);
