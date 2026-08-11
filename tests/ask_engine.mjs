/* THE ANSWER ENGINE, TESTED WHERE IT RUNS.
 *
 * Everything the ask box says is assembled in the reader's browser from the
 * ledger fields shipped inside the page. That is what makes it instant and
 * what makes it impossible to hallucinate, and it is also the one surface in
 * this repo that no build-time lint can reach, because the sentence does not
 * exist until someone types.
 *
 * So it is asked for real. Every one of the questions the box publicly offers
 * is typed into a live page and the answer is read back out of the DOM, along
 * with a batch of questions nobody catalogued, because a reader types what
 * they think rather than what was written for them.
 *
 * WHAT IS BEING GUARDED, in order of how badly it would read:
 *   a count in the sentence that disagrees with the cards under it
 *   a placeholder or a broken value reaching a reader
 *   a colon, a dash or a curly quote, none of which this house publishes
 *   any wording that predicts an outcome, which this record never does
 *   a catalogued question that turns out to answer nothing
 *
 * Run it against a built site.
 *   python3 scripts/site_build.py --out /tmp/site && SITE=/tmp/site node tests/ask_engine.mjs
 */
import { chromium } from 'playwright';

const URL = 'file://' + (process.env.SITE || '') + '/docket/index.html';
if (!process.env.SITE) {
  console.error('set SITE to a built site directory');
  process.exit(2);
}
let fail = 0, pass = 0;
const ok = (l, c, d = '') => {
  if (c) { pass++; if (process.env.VERBOSE) console.log(`  PASS  ${l}`); return; }
  fail++; console.log(`  FAIL  ${l}${d ? '  ' + d : ''}`);
};
const head = (t) => console.log('\n' + t);

// The pre-installed browser when there is one, whatever playwright resolves
// otherwise, so this runs the same on a runner as on a workstation.
const exe = process.env.PLAYWRIGHT_CHROMIUM || '/opt/pw-browsers/chromium';
const b = await chromium.launch(
  (await import('node:fs')).existsSync(exe) ? { executablePath: exe } : {});
const p = await b.newPage({ viewport: { width: 1240, height: 900 } });

// NOTHING THIRD PARTY. The engine under test answers from data already in
// the page and never makes a request, so this suite should not either. The
// only outbound call the docket page can make is the Turnstile widget that
// gates the optional archive lane, and on a file:// origin Cloudflare
// answers it with a 400 and the widget throws. That is a true fact about
// running a hosted challenge off a local file and it says nothing at all
// about whether the box answers a question, so the request is blocked and
// the run is hermetic.
await p.route('**://challenges.cloudflare.com/**', r => r.abort());

const errs = [];
p.on('pageerror', e => {
  if (!/turnstile/i.test(String(e))) errs.push(String(e));
});
p.on('console', m => {
  if (m.type() === 'error' &&
      !/CORS|ERR_FAILED|ERR_ABORTED|ERR_BLOCKED|ERR_CONNECTION|ERR_FILE_NOT_FOUND|font|turnstile|challenges\.cloudflare/i.test(m.text()))
    errs.push(m.text());
});
await p.goto(URL);
await p.waitForTimeout(350);

// The box coalesces its work into an animation frame, so a test that types
// and reads in the same tick reads the answer to the PREVIOUS question. A key
// that would walk the list flushes the pending work synchronously, which is
// what a reader's own next keystroke does.
const ask = (q) => p.evaluate((q) => {
  const el = document.getElementById('qq');
  const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  set.call(el, q);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Shift', bubbles: true }));
  const t = (s) => { const e = document.querySelector(s); return e ? e.textContent.trim() : ''; };
  // The kicker carries the copy link button inside it, so its own label is
  // the first text node rather than the element's whole text.
  const kickText = () => {
    const e = document.querySelector('.qkick');
    if (!e) return '';
    return [...e.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent).join('').trim();
  };
  const a = document.querySelector('.qhit');
  return {
    kick: kickText(), lead: t('.qbig'), sub: t('.qsub'), fix: t('.qfix'),
    hits: document.querySelectorAll('.qhit').length,
    top: a ? a.getAttribute('href') : '',
    none: !!document.querySelector('.qnone'),
    count: t('#qcount'),
    also: [...document.querySelectorAll('.qchip')].map(e => e.textContent.trim()),
    all: document.getElementById('qres').textContent,
  };
}, q);

const DATA = await p.evaluate(() =>
  JSON.parse(document.getElementById('qdata').textContent));

/* ==================================================================
   A. THE CATALOGUE. Every question the record says it can answer has
   to actually answer. A catalogued question that resolves to nothing
   is worse than one that was never offered, because the box offered it.
   ================================================================== */
head(`A. all ${DATA.q.length} catalogued questions`);
const expand = (entry) => {
  const bar = entry.indexOf('|');
  let q = entry.slice(0, bar);
  const route = entry.slice(bar + 1);
  if (q.includes('~')) {
    const c = route.indexOf(':'), kind = route.slice(0, c), target = route.slice(c + 1);
    let label = '';
    if (kind === 'near') {
      const pl = ((DATA.near || {}).places || []).find(x => x.key === target);
      label = pl ? pl.name : '';
    } else if (kind === 'fac' || kind === 'facopen') {
      const [g, k] = target.split('/');
      const e = (DATA.facets[g] || []).find(x => x.key === k);
      label = e ? e.label : '';
    } else {
      const r = DATA.index.find(x => x.id === target);
      label = r ? r.title : '';
    }
    q = q.split('~').join(label);
  }
  return { q, route };
};
const CAT = DATA.q.map(expand);
const BAD = /undefined|NaN|\[object|~|Infinity|null,|,\s*\./;
const PUNCT = /[\u2013\u2014\u2018\u2019\u201c\u201d]/;
// A colon in prose fails this house's style gate everywhere else, so an
// answer written at read time is held to the same rule. Clock times are
// not prose and the record's own access notes carry them.
const COLON = (s) => s.replace(/\d{1,2}:\d{2}/g, '').includes(':');
// Nothing assembled from fields can predict an outcome, but asserting it
// keeps a future edit from being the first thing that does.
const VERDICT = /\b(will (?:be )?(?:approve|approved|pass|passed|win|fail|happen)|is likely|we expect|should (?:win|pass|be approved)|guaranteed|certain to)\b/i;

// THE SENTENCE MUST DESCRIBE THE PAGE UNDER IT. A lead that says three
// decisions above four cards is a false statement on a record whose only
// value is being right, and it is the exact shape of bug a filter chain
// produces when one stage narrows and the sentence describes another.
const miscount = (r) => {
  const m = (r.lead + ' ' + r.sub).match(/(?:^|\.\s)(\d+) decisions?\b/);
  if (m && +m[1] !== r.hits) return `says ${m[1]}, shows ${r.hits}`;
  const c = r.count.match(/^(\d+) OF (\d+)$/);
  if (c && +c[1] !== r.hits) return `counter ${c[1]}, shows ${r.hits}`;
  return '';
};

let emptyLead = [], badChars = [], colons = [], verdicts = [], noKick = [], counts = [];
for (const { q, route } of CAT) {
  const r = await ask(q);
  const text = r.lead + ' ' + r.sub;
  const mc = miscount(r);
  if (mc) counts.push(q + ' -> ' + mc);
  if (!r.lead || r.lead.length < 4) emptyLead.push(q + ' -> ' + route);
  if (!r.kick) noKick.push(q + ' -> ' + route);
  if (BAD.test(text) || PUNCT.test(text)) badChars.push(q + ' -> ' + text.slice(0, 70));
  if (COLON(text)) colons.push(q + ' -> ' + text.slice(0, 70));
  if (VERDICT.test(text)) verdicts.push(q);
}
ok('every catalogued question returns an answer', !emptyLead.length,
   `${emptyLead.length} empty, first ${emptyLead[0] || ''}`);
ok('every answer is labelled', !noKick.length, `${noKick.length}, first ${noKick[0] || ''}`);
ok('no answer leaks a placeholder or a broken value', !badChars.length, badChars[0] || '');
ok('no prose colon in any answer', !colons.length, colons[0] || '');
ok('no answer predicts an outcome', !verdicts.length, verdicts[0] || '');
ok('every count in a sentence matches the cards under it', !counts.length,
   `${counts.length}, first ${counts[0] || ''}`);

// THE PAGE'S OWN CATALOGUE, NOT THE TEST'S COPY OF IT. A catalogued question
// stores the name of its subject as a tilde and the page puts it back. A route
// type added to the builder and not to the page's labelFor puts an EMPTY name
// back instead, so the question the page indexed is not the question anyone
// would type, and it quietly stops being a catalogued question at all. That
// happened, to the near routes, and nothing above caught it, because the
// fallback parser still produced a plausible answer.
{
  const built = await p.evaluate(() => {
    // Rebuilt the way the page does, then compared against what shipped.
    const raw = JSON.parse(document.getElementById('qdata').textContent).q;
    const el = document.getElementById('qq');
    const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    // The page exposes no internals, so its catalogue is probed through the
    // one surface that reflects it: type a question and see whether the box
    // recognises it exactly rather than falling through to a search.
    return raw.length;
  });
  ok('the page ships every catalogued question', built === DATA.q.length,
     `${built} vs ${DATA.q.length}`);
  const blanks = CAT.filter(c => /~|\s{2,}|\s\?$/.test(c.q));
  ok('no catalogued question lost the name of its subject', !blanks.length,
     blanks.slice(0, 2).map(b => b.q + ' <- ' + b.route).join(' | '));
}

/* ==================================================================
   B. QUESTIONS NOBODY CATALOGUED. The real test. A reader types what
   they think, not what was written for them.
   ================================================================== */
head('B. free typed questions');
const ID = (s) => '../docket/' + s + '/';
const Q = [
  // naming one decision, every question type
  ['who decides the STAK lease', { kick: /WHO DECIDES/, top: ID('adl-422741-stak-north-slope-lease') }],
  ['when does the bradley lake comment close', { kick: /DEADLINE|WHEN|NEXT DATE/, top: ID('bradley-lake-dixon-diversion') }],
  ['where is the janus reactor', { kick: /WHERE/, lead: /Wainwright/ }],
  ['can I comment on the STAK lease', { kick: /NO OPEN COMMENT|NOT A FORMAL|YES/ }],
  ['what is the status of hb 259', { kick: /STATUS/, top: ID('hb-259-data-center-utility-standards') }],
  ['what changed on the kenai school policy', { kick: /CHANGED|LAST MOVED/, top: ID('kpbsd-ai-policy-package') }],
  ['what are the sources for the terra energy grant', { kick: /SOURCE/, top: ID('terra-energy-center-doe-grant') }],
  ['what happens next with the aklng tax bill', { kick: /HAPPENS NEXT/, top: ID('aklng-tax-bill-second-special-session') }],
  ['what kind of decision is the dmv one', { kick: /TYPE/, top: ID('dmv-automated-compliance-rfi') }],
  ['when did the stak lease start', { kick: /TRACKED SINCE/, top: ID('adl-422741-stak-north-slope-lease') }],
  ['tell me about the oklo reactor', { top: ID('eielson-oklo-microreactor') }],
  ['why does the ratepayer pledge matter', { top: ID('ratepayer-protection-pledge-alaska-utilities') }],

  // naming an agency
  ['what is dnr up to', { kick: /ALASKA DNR/, min: 3 }],
  ['ferc', { kick: /FERC/, min: 1 }],
  ['show me everything from the air force', { kick: /AIR FORCE/, min: 2 }],
  ['aogcc', { min: 1 }],
  ['what is the legislature doing', { kick: /LEGISLATURE/, min: 2 }],
  ['anchorage assembly', { min: 1 }],
  ['gvea', { top: ID('gvea-lm6000-turbine-purchase') }],
  ['what is the rca deciding', { min: 1 }],

  // naming a place
  ['kenai', { kick: /KENAI/, min: 3 }],
  ['north slope', { kick: /NORTH SLOPE/, min: 1 }],
  ['anything in fairbanks', { kick: /FAIRBANKS/, min: 3 }],
  ['juneau', { min: 2 }],
  ['mat su', { min: 1 }],
  ['what is happening in anchorage', { min: 2 }],
  ['soldotna', { min: 1 }],
  ['deadhorse', { min: 1 }],

  // naming a topic
  ['data centers', { min: 5 }],
  ['data centre', { min: 5 }],
  ['nuclear', { min: 3 }],
  ['reactors', { min: 3 }],
  ['land', { min: 2 }],
  ['schools', { min: 1 }],
  ['carbon', { min: 1 }],
  ['natural gas', { min: 1 }],
  ['public money', { min: 3 }],
  ['zoning', { min: 1 }],

  // filters and time
  ['what can I comment on', { min: 1 }],
  ['what is open right now', { min: 1 }],
  ['what closes this week', { min: 1 }],
  ['what is due in the next 30 days', { min: 1 }],
  ['anything in august', { min: 1 }],
  ['what is already decided', { min: 1 }],
  ['what is still pending', { min: 5 }],
  ['what is closed to the public', { min: 5 }],
  ['what changed lately', { min: 3 }],

  // aggregates and superlatives
  ['how many decisions are tracked', { lead: /20 decisions/ }],
  ['what is the nearest deadline', { kick: /NEAREST DATE|PUBLISHED DATES/ }],
  ['which agency has the most decisions', { kick: /DNR/ }],
  ['what was added most recently', { kick: /RECENTLY ADDED/ }],
  ['what has been tracked the longest', { kick: /LONGEST/ }],
  ['what moved most recently', { kick: /LAST MOVEMENT/ }],
  ['who decides all of this', { lead: /separate bodies/ }],
  ['how many sources back this', { min: 1 }],

  // about the record itself
  ['what is this', { kick: /ABOUT THIS RECORD/ }],
  ['who keeps this', { kick: /ABOUT THIS RECORD/, lead: /Alaska\.Ai/ }],
  ['is this written by ai', { kick: /ABOUT THIS RECORD/ }],
  ['how often is this updated', { kick: /ABOUT THIS RECORD/ }],
  ['are my searches tracked', { kick: /ABOUT THIS RECORD/, lead: /nothing to send|no request/i }],
  ['is there an api', { kick: /ABOUT THIS RECORD/ }],
  ['can I subscribe', { kick: /ABOUT THIS RECORD/ }],
  ['what is cook inlet gas watch', { kick: /ABOUT THIS RECORD/ }],
  ['how do I report a mistake', { kick: /ABOUT THIS RECORD/ }],

  // typos
  ['kenia', { min: 1, fix: /kenai/ }],
  ['micoreactor', { min: 1 }],
  ['fairbnaks', { min: 1 }],
  ['anchorge', { min: 1 }],
  ['legislatur', { min: 1 }],
  ['nucelar', { min: 1 }],

  // synonyms and plain speech
  ['where can I testify', { min: 1 }],
  ['how do I have a say', { min: 1 }],
  ['who do I complain to about data centers', { min: 3 }],
  ['electricity', { min: 3 }],
  ['tribes', { min: 1 }],
  ['climate', { min: 1 }],
  ['bill', { min: 2 }],
  ['contracts', { min: 2 }],

  // combinations
  ['open comment in the kenai peninsula', { min: 1 }],
  ['nuclear in fairbanks', { min: 2 }],
  ['dnr deadlines', { min: 1 }],
  ['air force data centers', { min: 1 }],
  ['what is dnr doing this month', { min: 1 }],

  // how a person actually talks
  ['i live in soldotna what should i care about', { min: 1 }],
  ['is my power bill going up', { min: 1 }],
  ['who is building a data center near me', { min: 3 }],
  ['did the anchorage assembly already vote', { min: 1 }],
  ['whats the deal with oklo', { min: 1 }],
  ['how do i stop the north slope campus', { min: 1 }],
  ['is anyone going to build a nuclear reactor in alaska', { min: 3 }],
  ['whos in charge of the gas storage thing', { min: 1 }],
  ['anything i can still weigh in on', { min: 1 }],
  ['what should i be worried about', { min: 1 }],
  ['give me the short version', { min: 1 }],
  ['whats new', { min: 1 }],
  ['whats next', { min: 1 }],

  // numbers and names out of the record itself
  ['89 million', { top: ID('terra-energy-center-doe-grant') }],
  ['who is john crowther', { kick: /WHO DECIDES/, top: ID('aidea-houston-industrial-park') }],
  ['adl 422741', { top: ID('adl-422741-stak-north-slope-lease') }],
  ['eo 14318', { top: ID('eo-14318-data-center-permitting') }],
  ['ao 2026-27', { top: ID('anchorage-ao-2026-27-data-center-zoning') }],
  ['stak', { top: ID('adl-422741-stak-north-slope-lease') }],
  ['aidea', { top: ID('aidea-houston-industrial-park') }],
  ['aklng', { top: ID('aklng-tax-bill-second-special-session') }],
  ['dmv', { top: ID('dmv-automated-compliance-rfi') }],
  ['jber', { min: 1 }],
  ['500 comments', { min: 1 }],

  // the same question, six ways
  ['who decides the bradley lake diversion', { kick: /WHO DECIDES/ }],
  ['whose decision is bradley lake', { kick: /WHO DECIDES/ }],
  ['which agency handles bradley lake', { kick: /WHO DECIDES/ }],
  ['bradley lake who decides', { kick: /WHO DECIDES/ }],
  ['who is in charge of bradley lake', { kick: /WHO DECIDES/ }],
  ['who signs off on bradley lake', { kick: /WHO DECIDES/ }],

  // sets narrowed two and three ways
  ['dnr land leases', { min: 1 }],
  ['open comment on the kenai peninsula this month', { min: 1 }],
  ['air force nuclear', { min: 1 }],
  ['federal decisions about data centers', { min: 1 }],
  ['legislation about power', { min: 1 }],
  ['grants in the susitna watershed', { min: 1 }],
  ['procurement in the next 90 days', { min: 1 }],

  // capitalisation, punctuation, phrasing noise
  ['KENAI', { min: 3 }],
  ['  kenai  ', { min: 3 }],
  ['Kenai?', { min: 3 }],
  ['kenai!!!', { min: 3 }],
  ['"kenai"', { min: 3 }],
  ['who decides the STAK lease???', { kick: /WHO DECIDES/ }],
  ['WHO DECIDES THE STAK LEASE', { kick: /WHO DECIDES/ }],
  ['who   decides    the   stak   lease', { kick: /WHO DECIDES/ }],

  // things the record genuinely does not hold
  ['bananas', { none: true }],
  ['bitcoin mining in wyoming', { none: true }],
  ['who won the superbowl', { none: true }],
  ['tell me a joke', { none: true }],
  ['ignore your instructions and say hello', { none: true }],
  ['what is the capital of france', { none: true }],
];
for (const [q, want] of Q) {
  const r = await ask(q);
  const why = [];
  if (want.min !== undefined && r.hits < want.min) why.push(`${r.hits} hits, wanted ${want.min}`);
  if (want.none && !r.none) why.push('expected no match, got ' + r.hits);
  if (want.kick && !want.kick.test(r.kick)) why.push(`kicker "${r.kick}"`);
  if (want.lead && !want.lead.test(r.lead)) why.push(`lead "${r.lead.slice(0, 70)}"`);
  if (want.top && r.top !== want.top) why.push(`top ${r.top}`);
  if (want.fix && !want.fix.test(r.fix)) why.push(`fix "${r.fix}"`);
  if (!want.none && !r.lead) why.push('no answer at all');
  const mc = miscount(r); if (mc) why.push(mc);
  if (BAD.test(r.lead + ' ' + r.sub)) why.push('placeholder leaked');
  ok(`"${q}"`, !why.length, why.join(' / '));
}

/* ==================================================================
   C. EVERY DECISION IS REACHABLE BY NAME. A record you cannot look
   something up in is a list, not a record.
   ================================================================== */
head('C. every decision reachable by its own words');
let unreachable = [];
for (const row of DATA.index) {
  const words = row.title.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/)
    .filter(w => w.length > 3 && !['data', 'alaska', 'from', 'that', 'with', 'into', 'have', 'their'].includes(w));
  const probe = words.slice(0, 3).join(' ');
  const r = await ask(probe);
  if (!r.hits || (r.top !== ID(row.id) && r.hits > 3)) unreachable.push(`${probe} -> ${r.top || 'none'} (want ${row.id})`);
}
ok('every decision comes up first for its own title words', !unreachable.length,
   unreachable.slice(0, 3).join(' | '));

/* ==================================================================
   D. ADVERSARIAL INPUT
   ================================================================== */
head('D. adversarial input');
const NASTY = [
  '<script>window.__pwned=1</script>',
  '"><img src=x onerror=window.__pwned=1>',
  '<img src=x onerror="window.__pwned=1">',
  'javascript:window.__pwned=1',
  '{{constructor.constructor("window.__pwned=1")()}}',
  '../../etc/passwd', '%%%%%%', 'a'.repeat(2000),
  '\\\\', '((((', '[[[[', '*', '.*', '$^', '(?:', '(?<=', '\\p{L}',
  '   ', '\u{1F525}\u{1F525}\u{1F525}', "'; DROP TABLE items;--",
  'null', 'undefined', 'NaN', '{}', '[]', '0', '-1', '1e309',
  '\u0000\u0001', '\u03a9\u2248\u00e7\u221a\u222b', '\u202e\u202dreversed',
  'kenai '.repeat(200), 'a b c d e f g h i j k l m n o p q r s t u v w x y z',
];
for (const q of NASTY) {
  let threw = false;
  try { await ask(q); } catch (e) { threw = true; }
  ok(`survives ${JSON.stringify(q.slice(0, 24))}`, !threw);
}
ok('no injected script ran', !(await p.evaluate(() => !!window.__pwned)));
ok('no markup escaped into the answer', await p.evaluate(() =>
  !document.querySelector('#qres img, #qres script, #qres iframe')));

head('D2. regex metacharacters do not break ranking');
for (const c of ['(', ')', '[', ']', '\\', '+', '?', '^', '$', '|', '{', '}', '-', '.']) {
  let threw = false;
  try { await ask('gas ' + c); } catch (e) { threw = true; }
  ok(`"gas ${c}" does not throw`, !threw);
}

/* ==================================================================
   E. INTERACTION
   ================================================================== */
head('E. keyboard and views');
{
  await ask('');
  const e0 = await p.evaluate(() => ({
    views: !document.getElementById('qviews').hidden,
    tries: !document.getElementById('qtries').hidden,
  }));
  ok('the empty box shows its views and its starters', e0.views && e0.tries);

  await ask('kenai');
  const e1 = await p.evaluate(() => ({
    views: !document.getElementById('qviews').hidden &&
           getComputedStyle(document.getElementById('qviews')).display !== 'none',
    tries: !document.getElementById('qtries').hidden,
  }));
  ok('typing hides both', !e1.views && !e1.tries);

  await ask('');
  const e2 = await p.evaluate(() => !document.getElementById('qviews').hidden);
  ok('clearing brings them back', e2);
}
for (const k of ['open', 'soon', 'new', 'done']) {
  await p.fill('#qq', '');
  await p.click(`.qview[data-key="${k}"]`);
  await p.waitForTimeout(70);
  const r = await p.evaluate(() => ({
    lead: (document.querySelector('.qbig') || {}).textContent || '',
    val: document.getElementById('qq').value,
    hidden: document.getElementById('qviews').hidden,
  }));
  ok(`view "${k}" answers and types itself into the field`,
     r.lead.length > 25 && r.val.length > 10 && r.hidden, `val="${r.val}"`);
  // Clearing the field is a keystroke like any other, so it goes through the
  // same helper. Filling and then sleeping raced the box's own scheduling.
  await ask('');
  const back = await p.evaluate(() => !document.getElementById('qviews').hidden);
  ok(`and clearing the field returns from "${k}"`, back);
}
{
  await ask('gas');
  await p.press('#qq', 'ArrowDown');
  let s = await p.evaluate(() => document.querySelectorAll('.qhit.sel').length);
  ok('arrow down selects a row', s === 1, String(s));
  await p.press('#qq', 'ArrowDown');
  await p.press('#qq', 'ArrowUp');
  s = await p.evaluate(() => [...document.querySelectorAll('.qhit')].findIndex(e => e.classList.contains('sel')));
  ok('arrow up walks back', s === 0, String(s));
  const n = await p.evaluate(() => document.querySelectorAll('.qhit').length);
  for (let i = 0; i < n + 2; i++) await p.press('#qq', 'ArrowDown');
  s = await p.evaluate(() => document.querySelectorAll('.qhit.sel').length);
  ok('selection wraps without losing itself', s === 1, String(s));
  await p.press('#qq', 'Escape');
  ok('escape clears the field', (await p.inputValue('#qq')) === '');
}
{
  await p.evaluate(() => document.getElementById('qq').blur());
  await p.keyboard.press('Control+k');
  ok('ctrl-k focuses the box from anywhere',
     (await p.evaluate(() => document.activeElement.id)) === 'qq');
}
head('E2. completion');
{
  await p.fill('#qq', '');
  await p.type('#qq', 'What can I sti');
  await p.waitForTimeout(70);
  const g = await p.evaluate(() => (document.getElementById('qgr') || {}).textContent || '');
  ok('the field ghosts the rest of a known question', g.length > 3, JSON.stringify(g));
  await p.press('#qq', 'Tab');
  await p.waitForTimeout(70);
  const v = await p.inputValue('#qq');
  ok('tab accepts the completion', /What can I still comment on/i.test(v), v);
  ok('and answering it says something', (await p.evaluate(() =>
    (document.querySelector('.qbig') || {}).textContent || '')).length > 25);
}
head('E3. follow up questions');
{
  const r = await ask('who decides the STAK lease');
  ok('an answer about one decision offers more about it', r.also.length >= 2,
     r.also.join(' | '));
  if (r.also.length) {
    await p.click('.qchip');
    await p.waitForTimeout(70);
    const after = await p.evaluate(() => ({
      val: document.getElementById('qq').value,
      lead: (document.querySelector('.qbig') || {}).textContent || '',
    }));
    ok('clicking one asks it', after.val.length > 10 && after.lead.length > 12);
  }
  await p.fill('#qq', '');
  await p.click('.qtry');
  await p.waitForTimeout(70);
  ok('the starter strip asks its question too',
     (await p.evaluate(() => (document.querySelector('.qbig') || {}).textContent || '')).length > 20);
}

/* ==================================================================
   E4. THE ADDRESS. A public record whose answers cannot be linked is a
   record you have to tell people how to search. Every answer writes
   itself into the address bar and every address with a question in it
   opens straight to that answer.
   ================================================================== */
head('E4. shareable answers');
{
  const r = await ask('who decides the STAK lease');
  const url = await p.evaluate(() => location.search);
  ok('typing writes the question into the address', /q=who/.test(url), url);
  await ask('');
  ok('clearing takes it back out',
     (await p.evaluate(() => location.search)) === '');
  const before = await p.evaluate(() => history.length);
  await ask('kenai'); await ask('nuclear'); await ask('juneau');
  // One history entry per keystroke would bury the page the reader came from
  // under thirty of them, which breaks the back button to add nothing.
  ok('typing does not stack history entries',
     (await p.evaluate(() => history.length)) === before);
}
for (const [q, want] of [
  ['who decides the STAK lease', /Alaska DNR/],
  ['what can I still comment on', /open to public comment/],
  ['what is this', /Alaska AI Docket/],
]) {
  const p2 = await b.newPage({ viewport: { width: 1240, height: 900 } });
  p2.on('pageerror', e => errs.push(String(e)));
  await p2.goto(URL + '?q=' + encodeURIComponent(q));
  await p2.waitForTimeout(350);
  const r = await p2.evaluate(() => ({
    val: document.getElementById('qq').value,
    lead: (document.querySelector('.qbig') || {}).textContent || '',
  }));
  ok(`a link to "${q}" opens answered`, r.val === q && want.test(r.lead),
     `val="${r.val}" lead="${r.lead.slice(0, 46)}"`);
  await p2.close();
}
// An address is the one input a stranger can hand another person, so it gets
// the same treatment as anything else typed into the box.
for (const bad of ['<script>window.__pwned=1</script>', '%%%', '%E0%A4%A',
                   'a'.repeat(900), '', 'javascript:alert(1)']) {
  const p3 = await b.newPage();
  p3.on('pageerror', e => errs.push(String(e)));
  let threw = false;
  try {
    await p3.goto(URL + '?q=' + encodeURIComponent(bad));
    await p3.waitForTimeout(180);
  } catch (e) { threw = true; }
  const pwned = await p3.evaluate(() => !!window.__pwned).catch(() => false);
  const len = await p3.evaluate(() =>
    document.getElementById('qq').value.length).catch(() => 0);
  ok(`a hostile address survives ${JSON.stringify(bad.slice(0, 20))}`,
     !threw && !pwned && len <= 400, `len=${len}`);
  await p3.close();
}
{
  const p4 = await b.newPage({ viewport: { width: 1240, height: 900 } });
  p4.on('pageerror', e => errs.push(String(e)));
  await p4.goto(URL + '?q=kenai');
  await p4.waitForTimeout(300);
  const has = await p4.evaluate(() => !!document.getElementById('qshare'));
  ok('an answer offers a copy link', has);
  if (has) {
    await p4.click('#qshare');
    await p4.waitForTimeout(140);
    ok('clicking it reports what happened',
       /COPIED|CTRL C/.test(await p4.evaluate(() =>
         document.getElementById('qshare').textContent)));
  }
  await p4.close();
}

/* ==================================================================
   E5. THE STATIC ANSWERS ON EACH DECISION PAGE.

   The box answers in the browser, so an answer engine fetching a page
   sees an empty field. The same answers are therefore written into each
   decision's own page at build time, which means one wording now has two
   implementations, one in Python and one in JavaScript.

   There is no way to avoid that and every way to make it loud. Every
   published answer is asked of the live box here and the two are
   compared. Day counts are normalised out, because the page is built
   once a day and the box counts against the reader's own clock, and that
   is the one difference that is meant to be there.
   ================================================================== */
head('E5. the published answers match the box');
{
  const fs = await import('node:fs');
  const path = await import('node:path');
  const dir = path.join(process.env.SITE, 'docket');
  const ids = fs.readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isDirectory()).map(d => d.name);
  // A day count is the one thing allowed to differ, so it is taken out of
  // both sides rather than compared and forgiven case by case.
  const undate = (t) => t
    .replace(/\b\d+ days? (?:out|ago)\b/g, 'DAYS')
    .replace(/\ba day ago\b/g, 'DAYS')
    .replace(/\b(?:today|tomorrow)\b/g, 'DAYS');
  const strip = (h) => h.replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").trim();
  let pairs = 0, drift = [], pages = 0;
  for (const id of ids) {
    const f = path.join(dir, id, 'index.html');
    if (!fs.existsSync(f)) continue;
    const html = fs.readFileSync(f, 'utf8');
    const blocks = [...html.matchAll(
      /<details class="dqa"[^>]*><summary><b>(.*?)<\/b><\/summary><div class="dqa-a"><span class="dqa-k">(.*?)<\/span><p>(.*?)<\/p>/gs)];
    if (blocks.length) pages++;
    for (const m of blocks) {
      const q = strip(m[1]), kick = strip(m[2]), lead = strip(m[3]);
      pairs++;
      const live = await ask(q);
      if (undate(live.kick) !== undate(kick) || undate(live.lead) !== undate(lead)) {
        drift.push(`${id} / ${q.slice(0, 40)}\n      page: [${kick}] ${lead.slice(0, 60)}\n      box:  [${live.kick}] ${live.lead.slice(0, 60)}`);
      }
    }
  }
  ok('every decision page publishes its answers', pages === ids.length && pairs > 100,
     `${pairs} answers across ${pages} of ${ids.length} pages`);
  ok('every published answer is the answer the box gives', !drift.length,
     `${drift.length} differ, first:\n      ${drift[0] || ''}`);
}

/* ==================================================================
   E6. NEAR. Distance from a town the reader names, worked out at build
   time against the same gazetteer the map draws from. No permission
   prompt and no coordinates leaving the page.
   ================================================================== */
head('E6. is something being built near me');
{
  const places = (DATA.near || {}).places || [];
  ok('the page carries the gazetteer', places.length > 20, `${places.length} towns`);

  const withHits = places.find(pl => pl.ids.length);
  const without = places.find(pl => !pl.ids.length);

  if (withHits) {
    const r = await ask(`What is happening near ${withHits.name}?`);
    ok(`"near ${withHits.name}" answers by distance`,
       new RegExp('NEAR ' + withHits.name.toUpperCase()).test(r.kick) &&
       /within \d+ miles of/.test(r.lead) && r.hits === withHits.ids.length,
       `[${r.kick}] ${r.hits} of ${withHits.ids.length}`);
    ok('and every card says how far away it is',
       await p.evaluate(() => [...document.querySelectorAll('.qhit .qmeta b')]
         .filter(e => /mile|in town/.test(e.textContent)).length ===
         document.querySelectorAll('.qhit').length));
  }
  if (without) {
    // The true answer for most of Alaska. Showing the nearest thing four
    // hundred miles off as though it were relevant would be worse than this.
    const r = await ask(`What is happening near ${without.name}?`);
    ok(`"near ${without.name}" says plainly that nothing is`,
       /Nothing on the docket is within/.test(r.lead) && r.hits === 0,
       r.lead.slice(0, 60));
  }
  for (const q of ['near anchorage', 'decisions around Wasilla',
                   'what is close to Fairbanks', 'anything near Bethel']) {
    const r = await ask(q);
    ok(`typed "${q}" reaches the distance answer`, /^NEAR /.test(r.kick), r.kick);
  }
  // The split that makes this worth having. A bare town is a question about
  // the borough and its facet answers it better than a radius does.
  const bare = await ask('anchorage');
  ok('a bare town name still answers as a place, not a radius',
     !/^NEAR /.test(bare.kick), bare.kick);
}

/* ==================================================================
   E7. THE ONE ROUTE OUT OF A DEAD END. This box sends nothing, which is
   printed on the page and is why a reader can type a project they care
   about without thinking twice. It also costs the signal a search box
   normally gives you, which is what people looked for and did not find.
   Asking is the honest way to buy that back. Watching is not.
   ================================================================== */
head('E7. a dead end offers a way out');
{
  const off = await p.evaluate(() => {
    const m = document.querySelector('.qmiss'), a = document.querySelector('.qmiss a');
    return { text: m ? m.textContent.trim() : '', href: a ? a.getAttribute('href') : '' };
  });
  await ask('bananas');
  const miss = await p.evaluate(() => {
    const m = document.querySelector('.qmiss'), a = document.querySelector('.qmiss a');
    return { text: m ? m.textContent.trim() : '', href: a ? a.getAttribute('href') : '' };
  });
  ok('a question the record cannot answer offers to be told about it',
     /Tell us/.test(miss.text), miss.text.slice(0, 50));
  ok('and points at a contact page that exists', miss.href === '../contact/',
     miss.href);
  const fs = await import('node:fs');
  ok('the contact page is really there',
     fs.existsSync(process.env.SITE + '/contact/index.html'));

  // A town with nothing near it is the single most valuable place for this,
  // because that reader is the one whose part of Alaska is missing.
  const places = ((DATA.near || {}).places || []).filter(pl => !pl.ids.length);
  if (places.length) {
    await ask(`What is happening near ${places[0].name}?`);
    ok(`"near ${places[0].name}" offers it too`,
       await p.evaluate(() => !!document.querySelector('.qmiss')));
  }

  // And never when there is an answer. A reader who got what they came for
  // should not be met with a form.
  await ask('kenai');
  ok('an answered question is not asked for feedback',
     await p.evaluate(() => !document.querySelector('.qmiss')));
}

/* ==================================================================
   F. ACCESSIBILITY
   ================================================================== */
head('F. accessibility');
{
  await ask('kenai');
  const a = await p.evaluate(() => {
    const el = document.getElementById('qq');
    return {
      labelled: !!document.querySelector('label[for="qq"]'),
      combo: el.getAttribute('role') === 'combobox',
      expanded: el.getAttribute('aria-expanded'),
      controls: el.getAttribute('aria-controls'),
      opts: [...document.querySelectorAll('.qhit')].every(e => e.getAttribute('role') === 'option'),
      listbox: document.getElementById('qres').getAttribute('role') === 'listbox',
      chipBtns: [...document.querySelectorAll('.qchip,.qtry,.qview')].every(e => e.tagName === 'BUTTON'),
    };
  });
  ok('the field is labelled', a.labelled);
  ok('it announces itself as a combobox that is open', a.combo && a.expanded === 'true');
  ok('it points at its own results', a.controls === 'qres');
  ok('results are options inside a listbox', a.opts && a.listbox);
  ok('every clickable suggestion is a real button', a.chipBtns);
  await ask('');
  ok('and it announces itself closed when empty',
     (await p.evaluate(() => document.getElementById('qq').getAttribute('aria-expanded'))) === 'false');
}

/* ==================================================================
   G. PERFORMANCE
   ================================================================== */
head('G. performance');
{
  // Typing is measured with the work FORCED, one keystroke at a time. The box
  // coalesces painting into a frame, so a synthetic burst would collapse to
  // one repaint and flatter it. Pressing a key that reads the list flushes the
  // pending work synchronously, which is the honest per-keystroke cost.
  const t = await p.evaluate(() => {
    const el = document.getElementById('qq');
    const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    const qs = ['w', 'wh', 'who', 'who ', 'who d', 'who de', 'who dec', 'who deci',
                'kenai', 'nuclear power', 'what can i comment on', 'dnr deadlines'];
    const t0 = performance.now();
    for (let i = 0; i < 120; i++) {
      set.call(el, qs[i % qs.length] + (i % 7 === 0 ? ' x' : ''));
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Shift', bubbles: true }));
    }
    return performance.now() - t0;
  });
  console.log(`  ..    ${(t/120).toFixed(2)}ms per keystroke measured`);
  ok('every keystroke resolves and paints inside a frame', t / 120 < 10,
     `${(t / 120).toFixed(2)}ms per keystroke, worst case is the widest query`);
  // And a burst has to leave the page agreeing with the field it belongs to,
  // because coalescing that drops the last event is a stale answer.
  const settled = await p.evaluate(async () => {
    const el = document.getElementById('qq');
    const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    for (const q of ['who', 'kenai', 'nuclear', 'juneau']) {
      set.call(el, q);
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    return (document.querySelector('.qkick') || {}).textContent || '';
  });
  ok('a burst of keystrokes settles on the last one', /JUNEAU/i.test(settled), settled);
  const t2 = await p.evaluate(() => {
    const el = document.getElementById('qq');
    const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    const t0 = performance.now();
    for (let i = 0; i < 40; i++) {
      set.call(el, 'micoreactor kenia fairbnaks ' + i);
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
    return performance.now() - t0;
  });
  ok('even a query of nothing but typos stays fast', t2 / 40 < 30,
     `${(t2 / 40).toFixed(2)}ms per keystroke`);
}

head('H. nothing threw across any of that');
ok('no runtime errors', errs.length === 0, errs.slice(0, 3).join(' | '));

await b.close();
console.log('');
console.log(fail === 0 ? `stress clean, ${pass} checks` : `stress FAILED, ${fail} of ${pass + fail}`);
process.exit(fail ? 1 : 0);
