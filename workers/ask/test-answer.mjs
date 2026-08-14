// Tests for the written answer lane. Run: node workers/ask/test-answer.mjs
//
// Every control gets a green case AND a red case. A check that cannot fail
// certifies nothing, and two of the controls here are the only things standing
// between a model's sentence and a claim published under the site's name, or
// between a busy week and a bill nobody chose.
//
// The model is never called for real. A stub stands in for both the pack fetch
// and the Messages API, so these run offline, cost nothing, and can assert the
// thing that actually matters about the ceiling: that no request went out.

// The module under test is configurable so the identical assertions can be run
// against bundled.js, the flattened copy pasted into the Cloudflare dashboard.
// A bundle that drifts from these modules would be a worker whose guard is not
// the guard anybody tested. See test-bundle.mjs.
const UNDER_TEST = process.env.ASK_MODULE || "./answer.js";
const {
  answer, cacheKey, capOf, monthKey, normaliseQuestion, verify,
} = await import(UNDER_TEST);

let failures = 0;
function check(label, cond, detail = "") {
  if (!cond) failures++;
  console.log(`  ${cond ? "PASS" : "FAIL"}  ${label}${detail ? "  " + detail : ""}`);
}
function section(name) { console.log(name); }

const PACK = {
  generated: "2026-08-14",
  system: "the rules",
  pack: "THE RECORD. Storage held 6.54 Bcf across 20 tracked decisions.",
  authorised_numerals: ["6.54", "20", "2026", "8", "14"],
  slugs: ["stak-lease", "enstar-cook-inlet-gas-storage"],
};

function fakeKV(seed = {}) {
  const store = new Map(Object.entries(seed));
  return {
    store,
    async get(k) { return store.has(k) ? store.get(k) : null; },
    async put(k, v) { store.set(k, v); },
  };
}

// Stands in for the pack fetch and the Messages API both, and counts each, so
// a test can assert that a request was NOT made.
function stubFetch({ reply = "ok.", apiStatus = 200, pack = PACK } = {}) {
  const calls = { pack: 0, api: 0, body: null };
  const fn = async (url, opts) => {
    if (String(url).includes("ask-pack.json")) {
      calls.pack++;
      return { ok: true, json: async () => pack };
    }
    calls.api++;
    calls.body = JSON.parse(opts.body);
    if (apiStatus !== 200) {
      return { ok: false, status: apiStatus, text: async () => "nope" };
    }
    return {
      ok: true,
      json: async () => ({ content: [{ type: "text", text: reply }], usage: {} }),
    };
  };
  fn.calls = calls;
  return fn;
}

function env(over = {}) {
  return { ANTHROPIC_API_KEY: "sk-test", ASK_KV: fakeKV(), ...over };
}

const NOW = "2026-08-14T20:00:00Z";

// ------------------------------------------------------------ the cache key
section("one spelling per question, so a repeat is free");
check("case and punctuation collapse",
  normaliseQuestion("What is the STAK lease?") === normaliseQuestion("what is the stak lease"),
  normaliseQuestion("What is the STAK lease?"));
check("runs of whitespace collapse",
  normaliseQuestion("who   decides\n\nthis") === "who decides this",
  normaliseQuestion("who   decides\n\nthis"));
// And it has to keep two real questions apart, or the cache answers the wrong one.
check("a different word is a different question",
  normaliseQuestion("who decides") !== normaliseQuestion("when decides"));

const k1 = await cacheKey("What is the STAK lease?", "2026-08-14");
const k2 = await cacheKey("what is the stak lease", "2026-08-14");
const k3 = await cacheKey("What is the STAK lease?", "2026-08-15");
const k4 = await cacheKey("what is the enstar filing", "2026-08-14");
check("the same question on the same pack is one key", k1 === k2);
check("a new pack retires yesterday's answers", k1 !== k3);
check("a different question is a different key", k1 !== k4);
check("the key carries the pack date, readable in a KV listing",
  k1.startsWith("a:2026-08-14:"), k1);

section("the month counter");
check("the counter is per calendar month",
  monthKey("2026-08-14T20:00:00Z") === "spend:2026-08" &&
  monthKey("2026-09-01T00:00:00Z") === "spend:2026-09");

// ----------------------------------------------------------------- the cap
section("the ceiling is configurable and fails safe");
check("default when unset", capOf({}) === 500, String(capOf({})));
check("an operator's number wins", capOf({ ASK_MONTHLY_CAP: "25" }) === 25);
check("zero switches the lane off", capOf({ ASK_MONTHLY_CAP: "0" }) === 0);
// Garbage in a variable must not read as "unlimited".
check("garbage falls back to the default rather than to no limit",
  capOf({ ASK_MONTHLY_CAP: "banana" }) === 500,
  String(capOf({ ASK_MONTHLY_CAP: "banana" })));
check("a negative falls back too", capOf({ ASK_MONTHLY_CAP: "-5" }) === 500);

// --------------------------------------------------------------- the guard
section("the guard, on a whole answer");
const guard = { allowed: new Set(PACK.authorised_numerals), slugs: new Set(PACK.slugs) };
const clean = verify("Storage held 6.54 Bcf. See [[stak-lease]].", guard);
check("an answer built from the record passes", !clean.withheld, clean.text);

// The failure this whole design exists to stop: a confident, well formed,
// completely invented figure.
const bad = verify("Storage held 6.54 Bcf. It fell to 3.11 Bcf overnight.", guard);
check("an invented figure is cut", bad.withheld && bad.reason === "numeral",
  JSON.stringify(bad.reason));
check("the sentences before it are kept", bad.text === "Storage held 6.54 Bcf.", bad.text);

const cite = verify("See [[a-decision-nobody-wrote]].", guard);
check("a citation to an item that does not exist is cut",
  cite.withheld && cite.reason === "citation");
const verdictCut = verify("There is enough gas for the winter.", guard);
check("a safety verdict is cut", verdictCut.withheld && verdictCut.reason === "verdict");
// A refusal necessarily contains the words of the call it declines to make.
const declines = verify("The record does not say whether there will be enough gas.", guard);
check("declining to make the call is NOT cut", !declines.withheld, declines.text);

// -------------------------------------------------------------- end to end
section("the route");
{
  const e = env();
  globalThis.fetch = stubFetch({ reply: "Storage held 6.54 Bcf." });
  const r = await answer("what is in storage", e, { now: NOW });
  check("a clean answer comes back", r.status === 200 && !r.body.withheld, r.body.text);
  check("it was not served from cache", r.body.cached === false);
  check("the call was counted", e.ASK_KV.store.get("spend:2026-08") === "1");
  check("the record and the rules went as two system blocks",
    Array.isArray(globalThis.fetch.calls.body.system) &&
    globalThis.fetch.calls.body.system.length === 2);
  check("temperature is pinned to zero",
    globalThis.fetch.calls.body.temperature === 0);

  // Asking again must not reach the model.
  const before = globalThis.fetch.calls.api;
  const again = await answer("What is in storage?", e, { now: NOW });
  check("a repeat is served from KV", again.body.cached === true, again.body.text);
  check("a repeat does not call the model",
    globalThis.fetch.calls.api === before, `api calls ${globalThis.fetch.calls.api}`);
  check("a repeat does not count against the month",
    e.ASK_KV.store.get("spend:2026-08") === "1");
}

{
  // A cut answer is still paid for, so it still counts, but it must not be
  // cached: re-asking should get another attempt, not a stored stub.
  const e = env();
  globalThis.fetch = stubFetch({ reply: "Storage was 3.11 Bcf." });
  const r = await answer("what is in storage", e, { now: NOW });
  check("an unverifiable answer is withheld", r.body.withheld === true, r.body.reason);
  check("a withheld answer still counts against the month",
    e.ASK_KV.store.get("spend:2026-08") === "1");
  const cached = [...e.ASK_KV.store.keys()].filter(k => k.startsWith("a:"));
  check("a withheld answer is NOT cached", cached.length === 0, JSON.stringify(cached));
}

section("the ceiling actually stops spending");
{
  const e = env({ ASK_MONTHLY_CAP: "2", ASK_KV: fakeKV({ "spend:2026-08": "2" }) });
  globalThis.fetch = stubFetch({ reply: "Storage held 6.54 Bcf." });
  const r = await answer("something new", e, { now: NOW });
  check("the reader is told, not shown an error", r.status === 200 && r.body.capped === true);
  check("no request reached the model", globalThis.fetch.calls.api === 0,
    `api calls ${globalThis.fetch.calls.api}`);
  check("the message points at the lanes that still work",
    /archive/i.test(r.body.error) && /record/i.test(r.body.error), r.body.error);
}
{
  // An answer already paid for this month is still served after the cap, so
  // turning off new spending does not blank out answers already bought.
  const e = env({ ASK_MONTHLY_CAP: "1", ASK_KV: fakeKV({ "spend:2026-08": "9" }) });
  const key = await cacheKey("what is in storage", PACK.generated);
  e.ASK_KV.store.set(key, JSON.stringify({ text: "Storage held 6.54 Bcf.", withheld: false }));
  globalThis.fetch = stubFetch();
  const r = await answer("what is in storage", e, { now: NOW });
  check("a cached answer is served even over the cap",
    r.body.cached === true && !r.body.capped, r.body.text);
  check("and still calls nothing", globalThis.fetch.calls.api === 0);
}

section("it fails closed, and quietly");
{
  const r = await answer("hello", { ASK_KV: fakeKV() }, { now: NOW });
  check("no key means the lane is simply off", r.status === 503, String(r.status));
}
{
  const e = env({ ASK_MONTHLY_CAP: "0" });
  globalThis.fetch = stubFetch();
  const r = await answer("hello", e, { now: NOW });
  check("cap of zero switches it off without a deploy", r.status === 503);
  check("and calls nothing", globalThis.fetch.calls.api === 0);
}
{
  const e = env();
  globalThis.fetch = stubFetch({ apiStatus: 500 });
  const r = await answer("hello", e, { now: NOW });
  check("an API failure is a 502, not a stack trace", r.status === 502, r.body.error);
  check("a failed call is not counted against the month",
    e.ASK_KV.store.get("spend:2026-08") === undefined,
    String(e.ASK_KV.store.get("spend:2026-08")));
}
{
  const e = env();
  globalThis.fetch = async () => ({ ok: false, status: 404 });
  const r = await answer("hello", e, { now: NOW });
  check("an unreachable record is a 502", r.status === 502, r.body.error);
}


// ------------------------------------------------------------- the stream
//
// The streaming path carries the guard and the spend counter too, so both get
// their own green and red case here. A streaming answer that forgot to count
// is the bug that shows up as a bill.
section("the stream");

const { answerStream } = await import(UNDER_TEST);

// Build an SSE body the way the API sends one, so the parser is tested against
// the real frame shape rather than a convenient one.
function sseFetch(chunks, { status = 200 } = {}) {
  const calls = { api: 0 };
  const fn = async (url) => {
    if (String(url).includes("ask-pack.json")) return { ok: true, json: async () => PACK };
    calls.api++;
    if (status !== 200) return { ok: false, status, text: async () => "no" };
    const enc = new TextEncoder();
    const frames = chunks.map(t => `event: content_block_delta\ndata: ${JSON.stringify(
      { type: "content_block_delta", delta: { type: "text_delta", text: t } })}\n\n`);
    let i = 0;
    return {
      ok: true,
      body: { getReader: () => ({ read: async () =>
        i < frames.length ? { done: false, value: enc.encode(frames[i++]) } : { done: true } }) },
    };
  };
  fn.calls = calls;
  return fn;
}
async function drain(stream) {
  const out = [];
  const rd = stream.getReader(), dec = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await rd.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    const lines = buf.split("\n"); buf = lines.pop() ?? "";
    for (const l of lines) if (l.trim()) out.push(JSON.parse(l));
  }
  return out;
}

{
  const e = env();
  // Deltas deliberately split mid-sentence, which is how they actually arrive.
  globalThis.fetch = sseFetch(["Storage held ", "6.54 Bcf. See ", "[[stak-lease]]."]);
  const ev = await drain(await answerStream("what is in storage", e, { now: NOW }));
  const sents = ev.filter(x => x.sentence).map(x => x.sentence);
  check("stages are emitted before any text",
    ev[0] && !!ev[0].stage, JSON.stringify(ev[0]));
  check("a sentence split across deltas is reassembled",
    sents[0] === "Storage held 6.54 Bcf.", JSON.stringify(sents[0]));
  check("the trailing fragment is emitted too",
    sents.join(" ").includes("[[stak-lease]]"), JSON.stringify(sents));
  check("it finishes", ev.some(x => x.done));
  check("the call was counted", e.ASK_KV.store.get("spend:2026-08") === "1");
  check("a clean streamed answer is cached",
    [...e.ASK_KV.store.keys()].some(k => k.startsWith("a:")));
}

{
  // The guard, mid-stream. Everything before the bad sentence must already
  // have been shown, and nothing after it may be.
  const e = env();
  globalThis.fetch = sseFetch(["Storage held 6.54 Bcf. ", "It fell to 3.11 Bcf. ", "Then more."]);
  const ev = await drain(await answerStream("q", e, { now: NOW }));
  const sents = ev.filter(x => x.sentence).map(x => x.sentence);
  check("the good sentence was already streamed",
    sents.length === 1 && sents[0] === "Storage held 6.54 Bcf.", JSON.stringify(sents));
  check("the invented figure stopped the stream",
    ev.some(x => x.withheld === "numeral"), JSON.stringify(ev.filter(x => x.withheld)));
  check("nothing after it was sent", !sents.some(s => /Then more/.test(s)));
  check("a withheld streamed answer still counts",
    e.ASK_KV.store.get("spend:2026-08") === "1");
  check("a withheld streamed answer is NOT cached",
    ![...e.ASK_KV.store.keys()].some(k => k.startsWith("a:")));
}

{
  // The ceiling must stop the stream before a request goes out.
  const e = env({ ASK_MONTHLY_CAP: "1", ASK_KV: fakeKV({ "spend:2026-08": "5" }) });
  globalThis.fetch = sseFetch(["anything"]);
  const ev = await drain(await answerStream("q", e, { now: NOW }));
  check("a capped month streams the notice, not an answer",
    ev.some(x => x.capped === true), JSON.stringify(ev[0]));
  check("and no request reached the model", globalThis.fetch.calls.api === 0);
}

{
  const e = env();
  globalThis.fetch = sseFetch(["x"], { status: 500 });
  const ev = await drain(await answerStream("q", e, { now: NOW }));
  check("an API failure streams an error and closes",
    ev.some(x => x.error) && ev.some(x => x.done));
  check("a failed stream is not counted",
    e.ASK_KV.store.get("spend:2026-08") === undefined);
}

console.log();
console.log(failures ? `${failures} FAILED` : "all good");
process.exit(failures ? 1 : 0);
