// GENERATED FILE. Do not edit.
//
// The ask worker's four modules flattened into one, so it can be created by
// pasting into the Cloudflare dashboard without a terminal. Regenerate with:
//
//   node workers/ask/bundle.mjs
//
// Edit checks.js, deep.js, answer.js or worker.js instead. The tests run
// against those; test-bundle.mjs runs the same assertions against this, so the
// two cannot drift without something going red.

// ==================================================================
// checks.js
// ==================================================================

// Verification for answers the ask box is about to publish.
//
// These run on the model's output BEFORE a word of it reaches the page, one
// sentence at a time, so nothing unverified is ever shown and the reader still
// sees text appear progressively. Four controls, weakest last:
//
//   1. numerals    A reply may only contain numbers that appear in the record.
//                  This is the page's own numeral lint (gaswatch_build.py)
//                  moved from build time to answer time, and it is the
//                  strongest control here: an invented figure is arithmetically
//                  incapable of passing.
//   2. citations   Every [[slug]] must be a docket item that exists. A
//                  plausible-looking link to an item nobody wrote cannot ship.
//   3. verdict     No adequacy call on the gas position, in either direction.
//                  CLAUDE.md: "It NEVER publishes a safety verdict. Not a
//                  shortfall prediction, not an all clear, not a blackout call."
//   4. corpus      Not enforced here, but the reason the others hold: the
//                  record contains measured past readings and no forecast at
//                  all, so there is nothing for a forecast to be built out of.
//
// HONEST LIMIT. Controls 1 and 2 are set-membership tests and hold absolutely.
// Control 3 is a pattern match on free text and is the weakest of the four:
// it is a backstop for a model that has already been told not to, not a proof.
// It is written to catch assertions rather than topic words, because a reader
// asking "what does the gas watch actually measure?" deserves an answer that
// is allowed to contain the word shortfall.

// One spelling per number. Must agree exactly with normalise() in
// scripts/ask_corpus.py, which builds the allow-list this checks against; a
// divergence between the two would reject true figures. Pinned by a test that
// compares both implementations over the same inputs.
export function normalise(tok) {
  tok = tok.replace(/^0+/, "") || "0";
  if (tok.includes(".")) {
    tok = tok.replace(/0+$/, "").replace(/\.$/, "") || "0";
  }
  return tok;
}

const NUMERAL_RE = /\d+(?:\.\d+)?/g;

export function numerals(text) {
  return (text.match(NUMERAL_RE) || []).map(normalise);
}

// An assertion about whether the gas holds out, in either direction. Ordered
// roughly most to least specific. Each one targets a predicate, not a noun, so
// mentioning a shortfall is fine and calling one is not.
const VERDICT = [
  /\b(?:will|wo n't|won'?t|will not|going to|gonna)\s+(?:\w+\s+){0,2}?(?:run\s+out|run\s+short|be\s+enough|have\s+enough)/i,
  /\bthere\s+(?:is|are|will\s+be)\s+(?:\w+\s+){0,2}?(?:enough|sufficient|adequate|plenty)\b/i,
  /\b(?:enough|sufficient|adequate|plenty\s+of)\s+(?:gas|supply|storage|fuel|inventory)\b/i,
  /\b(?:supply|storage|inventory|the\s+region|southcentral|alaska)\s+(?:is|are|will\s+be)\s+(?:\w+\s+){0,1}?(?:adequate|sufficient|fine|safe|secure|okay|ok)\b/i,
  /\ball\s+clear\b/i,
  /\bblack\s?outs?\b/i,
  /\bno\s+(?:risk|danger)\s+of\b/i,
  /\b(?:we|you|alaskans?)\s+(?:will|should|wo n't|won'?t|will not)\s+(?:\w+\s+){0,2}?(?:make it|be fine|be okay|be ok|freeze|run out)/i,
  /\b(?:shortfall|shortage|curtailment)\s+(?:is|will\s+be|of)\s+(?:\w+\s+){0,2}?(?:likely|coming|expected|certain|imminent|unlikely)\b/i,
  /\b(?:is|are|will\s+be)\s+(?:not\s+)?safe\b/i,
];

// A sentence that DECLINES to make the call necessarily contains the words of
// the call it is declining to make. "The record does not say whether there
// will be enough gas" trips the first pattern above and is exactly the
// sentence we want the model to write. Without this exemption the guard would
// block its own correct refusal, which is how a safety check ends up teaching
// a model to answer instead.
const DISCLAIMED =
  /\b(?:does\s+not|doesn'?t|do\s+not|don'?t|cannot|can'?t|could\s+not|couldn'?t|will\s+not|wo\s?n'?t|no\s+one|nobody)\s+(?:\w+\s+){0,2}?(?:say|says|state|publish|publishes|predict|predicts|forecast|forecasts|tell|know|answer|claim)\b/i;
const NO_SUCH_THING =
  /\bn(?:o|ot\s+a)\s+(?:public\s+)?(?:forecast|prediction|projection|verdict|guarantee|assurance)\b/i;

export function checkVerdict(text) {
  if (DISCLAIMED.test(text) || NO_SUCH_THING.test(text)) return { ok: true };
  for (const re of VERDICT) {
    const m = text.match(re);
    if (m) return { ok: false, reason: "verdict", hit: m[0].trim() };
  }
  return { ok: true };
}

const CITE_RE = /\[\[([^\]]+)\]\]/g;

export function checkCitations(text, slugs) {
  const unknown = [];
  for (const m of text.matchAll(CITE_RE)) {
    if (!slugs.has(m[1])) unknown.push(m[1]);
  }
  return unknown.length ? { ok: false, reason: "citation", unknown } : { ok: true };
}

export function checkNumerals(text, allowed) {
  // Citation slugs can carry digits (eo-14318, adl-422741). They are checked
  // as slugs, so stripping them here stops a valid citation from being read as
  // an unauthorised figure.
  const prose = text.replace(CITE_RE, " ");
  const bad = numerals(prose).filter((n) => !allowed.has(n));
  return bad.length ? { ok: false, reason: "numeral", offending: bad } : { ok: true };
}

// The composite the streaming loop calls. Cheapest and strictest first, so a
// failure reports the most actionable cause.
export function checkSentence(text, { allowed, slugs }) {
  const c = checkCitations(text, slugs);
  if (!c.ok) return c;
  const n = checkNumerals(text, allowed);
  if (!n.ok) return n;
  return checkVerdict(text);
}

// Split on sentence ends only where a space follows, so decimals (6.54 Bcf)
// and abbreviated dockets stay whole. A trailing fragment is returned as the
// remainder for the next chunk rather than checked early.
export function splitSentences(buffer) {
  const parts = buffer.split(/(?<=[.!?])\s+/);
  const remainder = parts.pop() ?? "";
  return { sentences: parts, remainder };
}

// ==================================================================
// deep.js
// ==================================================================

// The archive lane. A question that needs the actual repository rather than
// the published record, answered by firing a Claude Code routine.
//
// WHY THIS EXISTS AT ALL. The in-page engine answers from the record shipped
// inside the docket page, which is every field of every tracked decision, and
// that covers almost everything anyone asks. Some questions need more: the run
// archive, the ledgers, the history of how an item changed, a cross reference
// nothing on the site exposes. A routine runs as a full Claude Code session
// with the repository cloned, so it can read all of it.
//
// WHAT IT COSTS. Latency, and a lot of it. POSTing to a routine's /fire
// endpoint STARTS A NEW SESSION: provision a container, clone the repos, run
// the setup script, then begin. Minutes, not seconds. It also draws on the
// account's daily routine run cap and the same subscription usage the daily
// carousel spends, so this lane is deliberately a button someone chooses
// rather than the default path.
//
// WHY THERE IS STORAGE HERE AT ALL. /fire returns a session id, not an
// answer. The routine finishes later and has to put the
// answer somewhere the page can poll. The Cache API cannot do this job: a
// cache write in one Cloudflare datacentre is not readable from another, so
// the routine's delivery and the visitor's poll could land in different places
// and the answer would simply vanish. KV is the smallest durable thing that
// works, it is part of the Workers platform rather than a separate service,
// and it does not pause when idle.

const FIRE = "https://api.anthropic.com/v1/claude_code/routines";
const BETA = "experimental-cc-routine-2026-04-01";

// A question waits at most this long before the page gives up on it. A routine
// run that has not delivered in twenty minutes is not coming.
const TTL = 60 * 25;

export function newId() {
  return crypto.randomUUID().replace(/-/g, "").slice(0, 20);
}

/**
 * Fire the routine. The payload carries the request id as well as the
 * question, because the routine has to know where to deliver the answer and
 * the fire text is the only channel into the run.
 *
 * The routine's saved prompt must opt in to reading this. Fire text arrives
 * wrapped in a <routine-fire-payload> block that labels it untrusted and tells
 * the model not to follow instructions inside it, which is the correct default
 * when anyone on the internet can put words in that block.
 */
export async function fire(question, id, env) {
  const r = await fetch(`${FIRE}/${env.ROUTINE_TRIGGER_ID}/fire`, {
    method: "POST",
    headers: {
      "authorization": `Bearer ${env.ROUTINE_TOKEN}`,
      "anthropic-beta": BETA,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      text: `request_id: ${id}\nquestion: ${question}`,
    }),
  });
  if (!r.ok) {
    const detail = await r.text().catch(() => "");
    throw new Error(`fire ${r.status}: ${detail.slice(0, 200)}`);
  }
  return r.json();
}

/**
 * Verify an answer the routine delivered, using the same checks that guard
 * runs. A slower answer is not a more trusted one: it came from a model too,
 * and it had a whole repository to invent numbers from rather than one file.
 *
 * Returns the accepted prefix. Nobody is waiting on a stream here, so the
 * whole answer is checked at once and truncated at the first sentence that
 * fails.
 */
export function verifyArchiveAnswer(answer, { allowed, slugs }) {
  const { sentences, remainder } = splitSentences(answer.trim());
  const all = remainder.trim() ? [...sentences, remainder] : sentences;
  const kept = [];
  for (const s of all) {
    const verdict = checkSentence(s, { allowed, slugs });
    if (!verdict.ok) {
      return { text: kept.join(" "), withheld: true, reason: verdict.reason, sentence: s };
    }
    kept.push(s.trim());
  }
  return { text: kept.join(" "), withheld: false };
}

export async function start(question, env) {
  const id = newId();
  await env.ASK_KV.put(`q:${id}`, JSON.stringify({ question, state: "running" }),
    { expirationTtl: TTL });
  try {
    await fire(question, id, env);
  } catch (e) {
    await env.ASK_KV.put(`q:${id}`, JSON.stringify({
      question, state: "failed", error: "the research run could not be started",
    }), { expirationTtl: TTL });
    throw e;
  }
  return id;
}

export async function deliver(body, env, corpus) {
  // The routine authenticates with a shared secret it reads from its cloud
  // environment's variables. Without this anyone who guesses a request id
  // could write the answer, which is a worse hole than the one Turnstile
  // closes, because this text publishes under the site's name.
  if (!env.DELIVER_SECRET || body.secret !== env.DELIVER_SECRET) {
    return { status: 403, body: { error: "no" } };
  }
  const id = String(body.id ?? "");
  if (!/^[a-f0-9]{20}$/.test(id)) return { status: 400, body: { error: "bad id" } };

  const existing = await env.ASK_KV.get(`q:${id}`);
  if (!existing) return { status: 404, body: { error: "unknown or expired request" } };

  const answer = String(body.answer ?? "").trim();
  if (!answer) {
    await env.ASK_KV.put(`q:${id}`, JSON.stringify({
      state: "failed", error: "the research run returned nothing",
    }), { expirationTtl: TTL });
    return { status: 200, body: { ok: true, stored: "empty" } };
  }

  const checked = verifyArchiveAnswer(answer, {
    allowed: new Set(corpus.authorised_numerals),
    slugs: new Set(corpus.slugs),
  });
  await env.ASK_KV.put(`q:${id}`, JSON.stringify({
    state: "done",
    text: checked.text,
    withheld: checked.withheld,
    reason: checked.reason ?? null,
  }), { expirationTtl: TTL });

  if (checked.withheld) {
    console.log("deep withheld", JSON.stringify({ id, reason: checked.reason, sentence: checked.sentence }));
  }
  return { status: 200, body: { ok: true, withheld: checked.withheld } };
}

export async function result(id, env) {
  if (!/^[a-f0-9]{20}$/.test(id)) return { status: 400, body: { error: "bad id" } };
  const raw = await env.ASK_KV.get(`q:${id}`);
  if (!raw) return { status: 404, body: { state: "expired" } };
  const rec = JSON.parse(raw);
  // The question is not echoed back. The page already has it, and not
  // returning it means a guessed id leaks nothing.
  return {
    status: 200,
    body: {
      state: rec.state,
      text: rec.text ?? null,
      withheld: rec.withheld ?? false,
      reason: rec.reason ?? null,
      error: rec.error ?? null,
    },
  };
}

// ==================================================================
// answer.js
// ==================================================================

// The answerer. The middle lane of the ask box.
//
// WHAT THIS IS FOR. The in-page engine (scripts/ask_answers.py) answers almost
// everything, because almost every question about a docket is a filter, a field
// read, a sort or a count. It costs nothing, it answers in the same frame, and
// nothing is generated so nothing can be invented. It stays the default path
// and this lane never runs ahead of it.
//
// This is for the remainder: the plain English question the engine has no field
// for. "Why did the Assembly vote it down", "what changed on the STAK lease
// since June", "what does days of cover actually mean". Those need a sentence
// written, not a row returned.
//
// WHY THE WHOLE RECORD GOES IN EVERY PROMPT. Because it fits. docs/ask-pack.json
// is about 21,000 tokens against a 200,000 token context, so there is no
// retrieval step of any kind here: no embeddings, no vector store, no chunking,
// no top-k, no similarity threshold. The largest single source of wrong answers
// in a retrieval chatbot is retrieving the wrong passage, and a record this size
// lets us delete that failure mode rather than tune it. Every answer is written
// with the entire docket in view.
//
// WHY IT CANNOT INVENT A FIGURE. Every sentence passes checks.js before it is
// returned, against the numeral allow-list built from the exact text the model
// was shown. An invented number is arithmetically incapable of passing. This is
// the same guard the archive lane uses, and it is the reason a cheap model is
// the right model here: an answer that cannot state a number the record does
// not contain is worth more than a cleverer answer that can.
//
// WHAT IT COSTS, AND WHY THAT CANNOT RUN AWAY. Roughly two cents a question at
// Haiku 4.5 rates. Three things keep the month bounded: the engine absorbs most
// questions before this lane is reached, identical questions are served from KV
// for nothing, and a monthly call ceiling degrades the box back to the engine
// and the archive button rather than spending past a number the operator set.
// The bill has a maximum you choose, not a maximum the internet chooses.

const API = "https://api.anthropic.com/v1/messages";
const PACK_URL = "https://alaskaaihq.com/ask-pack.json";

// Pinned to a dated snapshot rather than a moving alias, so an answer the
// guard accepted today is produced by the same model tomorrow. Overridable for
// a staging deploy without a code change.
const DEFAULT_MODEL = "claude-haiku-4-5-20251001";

// Three or four sentences. The guard checks sentence by sentence and the page
// shows a short answer, so a long generation is spend with nowhere to go.
const MAX_TOKENS = 600;

// The ceiling, in model calls per calendar month.
//
// Cached repeats and engine answers do not count against it, so this is a
// count of DISTINCT questions that reached the model. At today's pack size a
// call is about $0.024, so 500 is roughly twelve dollars of worst case in a
// month where every one of them is used. Expected spend is far below that: the
// engine takes most questions and the cache takes the repeats.
//
// Set ASK_MONTHLY_CAP in the worker's variables to change it. Set it to 0 to
// turn the lane off without redeploying.
const DEFAULT_CAP = 500;

// Answers live until the pack they were written from is replaced. The cache key
// already carries the pack's generated date, so this is a floor for cleanup
// rather than a correctness control: a stale key can never be read, because a
// new pack produces a different key.
const ANSWER_TTL = 60 * 60 * 36;

export function capOf(env) {
  const raw = env.ASK_MONTHLY_CAP;
  if (raw === undefined || raw === null || raw === "") return DEFAULT_CAP;
  const n = Number(raw);
  return Number.isFinite(n) && n >= 0 ? Math.floor(n) : DEFAULT_CAP;
}

/**
 * One spelling per question, so "What is the STAK lease?" and "what is the
 * stak lease" are one cache entry rather than two model calls. Punctuation and
 * runs of whitespace go; nothing else is touched, because two questions that
 * differ by a real word are two questions.
 */
export function normaliseQuestion(q) {
  return String(q).toLowerCase().replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ").trim();
}

export async function cacheKey(question, packDate) {
  const data = new TextEncoder().encode(`${packDate}\n${normaliseQuestion(question)}`);
  const digest = await crypto.subtle.digest("SHA-256", data);
  const hex = [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, "0")).join("");
  // The pack date rides in the key as well as in the hash so a human reading
  // the KV listing can see which day an entry belongs to.
  return `a:${packDate}:${hex.slice(0, 32)}`;
}

export function monthKey(nowISO) {
  return `spend:${nowISO.slice(0, 7)}`;
}

/**
 * Check a whole answer and return the accepted prefix.
 *
 * Nobody is waiting on a stream, so this checks the answer at once and cuts it
 * at the first sentence that fails rather than quietly repairing it. A reader
 * seeing an answer stop short, and being told why, is better served than a
 * reader shown a smoothed over sentence nobody verified.
 */
export function verify(answer, { allowed, slugs }) {
  const { sentences, remainder } = splitSentences(String(answer).trim());
  const all = remainder.trim() ? [...sentences, remainder] : sentences;
  const kept = [];
  for (const s of all) {
    const verdict = checkSentence(s, { allowed, slugs });
    if (!verdict.ok) {
      return { text: kept.join(" "), withheld: true, reason: verdict.reason, sentence: s };
    }
    kept.push(s.trim());
  }
  return { text: kept.join(" "), withheld: false };
}

export async function loadPack(env) {
  const url = env.ASK_PACK_URL || PACK_URL;
  // Held at Cloudflare's edge, so answering does not pay a round trip to
  // GitHub Pages to read a file that changes once a day.
  const r = await fetch(url, { cf: { cacheTtl: 900, cacheEverything: true } });
  if (!r.ok) throw new Error(`pack fetch failed: ${r.status}`);
  return r.json();
}

export async function callModel(question, pack, env, fetchImpl = fetch) {
  const r = await fetchImpl(API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: env.ASK_MODEL || DEFAULT_MODEL,
      max_tokens: MAX_TOKENS,
      // Zero, because this is a lookup rather than a piece of writing. It also
      // makes the KV cache mean something and makes a guard failure
      // reproducible when investigating one.
      temperature: 0,
      // Two blocks rather than one string. The rules are stable and the record
      // changes daily, and keeping them apart is what lets a cache_control
      // marker be added to the record block later without touching anything
      // else. Caching is deliberately NOT on yet: a cache write costs more
      // than a plain read, so it only pays once questions arrive in clusters,
      // and at this traffic it would raise the bill rather than lower it.
      system: [
        { type: "text", text: pack.system },
        { type: "text", text: pack.pack },
      ],
      messages: [{ role: "user", content: question }],
    }),
  });
  if (!r.ok) {
    const detail = await r.text().catch(() => "");
    throw new Error(`messages ${r.status}: ${detail.slice(0, 200)}`);
  }
  const out = await r.json();
  const text = (out.content || [])
    .filter(b => b.type === "text").map(b => b.text).join("").trim();
  return { text, usage: out.usage || null };
}

/**
 * Stream the model's reply, calling onDelta with each text fragment.
 *
 * The guard already works a sentence at a time, so streaming is not a
 * cosmetic addition here: a sentence can be checked the moment it is complete
 * and shown immediately, and one that fails ends the answer there. Waiting for
 * the whole reply before checking any of it was never necessary.
 */
export async function streamModel(question, pack, env, onDelta, fetchImpl = fetch) {
  const r = await fetchImpl(API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: env.ASK_MODEL || DEFAULT_MODEL,
      max_tokens: MAX_TOKENS,
      temperature: 0,
      stream: true,
      system: [
        { type: "text", text: pack.system },
        { type: "text", text: pack.pack },
      ],
      messages: [{ role: "user", content: question }],
    }),
  });
  if (!r.ok || !r.body) {
    const detail = await r.text().catch(() => "");
    throw new Error(`messages ${r.status}: ${String(detail).slice(0, 200)}`);
  }

  const reader = r.body.getReader();
  const dec = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    // SSE frames are separated by a blank line. Anything after the last one is
    // a partial frame and waits for more bytes.
    const frames = buf.split("\n\n");
    buf = frames.pop() ?? "";
    for (const frame of frames) {
      for (const line of frame.split("\n")) {
        if (!line.startsWith("data:")) continue;
        let ev;
        try { ev = JSON.parse(line.slice(5).trim()); } catch { continue; }
        if (ev.type === "content_block_delta" && ev.delta?.type === "text_delta") {
          onDelta(ev.delta.text);
        }
      }
    }
  }
}

/**
 * Everything both paths must agree on: is the lane on, is this already
 * answered, is the month spent. Factored out because the streaming path
 * forgetting to count a call is exactly the bug that would not show up until
 * a bill did.
 */
async function preflight(question, env, now) {
  if (!env.ANTHROPIC_API_KEY || !env.ASK_KV) {
    return { stop: { status: 503, body: { error: "the answerer is not configured" } } };
  }
  const cap = capOf(env);
  if (cap === 0) {
    return { stop: { status: 503, body: { error: "the answerer is switched off" } } };
  }

  let pack;
  try {
    pack = await loadPack(env);
  } catch {
    return { stop: { status: 502, body: { error: "the record is unreachable" } } };
  }

  const key = await cacheKey(question, pack.generated);
  const hit = await env.ASK_KV.get(key);
  if (hit) return { cached: { ...JSON.parse(hit), cached: true }, pack, key };

  // Read AFTER the cache, so a question already answered this month is still
  // served once the budget is spent. Turning off new spending should not blank
  // out answers already paid for.
  const mk = monthKey(now || new Date().toISOString());
  const spent = Number(await env.ASK_KV.get(mk)) || 0;
  if (spent >= cap) {
    return {
      stop: {
        status: 200,
        body: {
          text: "", withheld: false, capped: true,
          error: "The written answer lane has reached this month's limit. " +
                 "The box above still answers from the record, and the full " +
                 "archive search below still works.",
        },
      },
    };
  }
  return { pack, key, mk, spent };
}

/**
 * The streaming route. Emits newline delimited JSON, one event per line, so
 * the page can render as it arrives without a parser of its own:
 *
 *   {"stage":"..."}          what is happening, and each one is true
 *   {"sentence":"..."}       one verified sentence, safe to show
 *   {"withheld":"numeral"}   the answer stopped here and why
 *   {"done":true}            finished
 *   {"error":"..."}          nothing to show
 */
export async function answerStream(question, env, { now, fetchImpl } = {}) {
  const pre = await preflight(question, env, now);
  const enc = new TextEncoder();
  const line = (o) => enc.encode(JSON.stringify(o) + "\n");

  if (pre.stop) {
    return new ReadableStream({
      start(c) { c.enqueue(line(pre.stop.body)); c.enqueue(line({ done: true })); c.close(); },
    });
  }
  if (pre.cached) {
    // Replayed a sentence at a time, so a cached answer arrives the same way a
    // fresh one does rather than snapping in and looking like a different
    // feature. It is instant either way; this only keeps the shape honest.
    const { sentences, remainder } = splitSentences(String(pre.cached.text).trim());
    const all = remainder.trim() ? [...sentences, remainder] : sentences;
    return new ReadableStream({
      start(c) {
        c.enqueue(line({ stage: "Answered this one already" }));
        for (const s of all) c.enqueue(line({ sentence: s.trim() }));
        c.enqueue(line({ done: true, cached: true }));
        c.close();
      },
    });
  }

  const { pack, key, mk, spent } = pre;
  const allowed = new Set(pack.authorised_numerals);
  const slugs = new Set(pack.slugs);

  return new ReadableStream({
    async start(c) {
      c.enqueue(line({ stage: "Reading the record" }));
      let buf = "", kept = [], withheld = null, opened = false;
      try {
        await streamModel(question, pack, env, (delta) => {
          if (!opened) {
            opened = true;
            c.enqueue(line({ stage: "Checking every figure against the record" }));
          }
          if (withheld) return;
          buf += delta;
          const { sentences, remainder } = splitSentences(buf);
          buf = remainder;
          for (const s of sentences) {
            const v = checkSentence(s, { allowed, slugs });
            if (!v.ok) { withheld = v.reason; return; }
            kept.push(s.trim());
            c.enqueue(line({ sentence: s.trim() }));
          }
        }, fetchImpl || fetch);

        // Whatever is left over after the last sentence end.
        if (!withheld && buf.trim()) {
          const v = checkSentence(buf, { allowed, slugs });
          if (!v.ok) withheld = v.reason;
          else { kept.push(buf.trim()); c.enqueue(line({ sentence: buf.trim() })); }
        }
      } catch (e) {
        console.log("answer stream failed", String(e));
        c.enqueue(line({ error: "that answer did not come back" }));
        c.enqueue(line({ done: true }));
        c.close();
        return;
      }

      // Counted whether or not the guard kept the text. A refused answer costs
      // the same as an accepted one.
      await env.ASK_KV.put(mk, String(spent + 1), { expirationTtl: 60 * 60 * 24 * 70 });

      if (withheld) {
        c.enqueue(line({ withheld }));
        console.log("answer withheld", JSON.stringify({ reason: withheld }));
      } else if (kept.length) {
        // Only a clean answer is cached, so a cut one gets another attempt
        // rather than a stored stub.
        await env.ASK_KV.put(key, JSON.stringify({ text: kept.join(" "), withheld: false }),
          { expirationTtl: ANSWER_TTL });
      } else {
        c.enqueue(line({ error: "The record did not produce an answer to that." }));
      }
      c.enqueue(line({ done: true }));
      c.close();
    },
  });
}

/**
 * The route. Turnstile has already been checked by the caller, because that is
 * the worker's job for every expensive path and not this module's.
 */
export async function answer(question, env, { now, fetchImpl } = {}) {
  if (!env.ANTHROPIC_API_KEY || !env.ASK_KV) {
    return { status: 503, body: { error: "the answerer is not configured" } };
  }
  const cap = capOf(env);
  if (cap === 0) return { status: 503, body: { error: "the answerer is switched off" } };

  let pack;
  try {
    pack = await loadPack(env);
  } catch {
    return { status: 502, body: { error: "the record is unreachable" } };
  }

  const key = await cacheKey(question, pack.generated);
  const hit = await env.ASK_KV.get(key);
  if (hit) {
    const rec = JSON.parse(hit);
    return { status: 200, body: { ...rec, cached: true } };
  }

  // The ceiling is read AFTER the cache, so a question already answered today
  // is served even in a month that has spent its budget. Turning the lane off
  // should stop new spending, not blank out answers already paid for.
  const mk = monthKey(now || new Date().toISOString());
  const spent = Number(await env.ASK_KV.get(mk)) || 0;
  if (spent >= cap) {
    return {
      status: 200,
      body: {
        text: "", withheld: false, capped: true,
        error: "The written answer lane has reached this month's limit. " +
               "The box above still answers from the record, and the full " +
               "archive search below still works.",
      },
    };
  }

  let out;
  try {
    out = await callModel(question, pack, env, fetchImpl || fetch);
  } catch (e) {
    console.log("answer failed", String(e));
    return { status: 502, body: { error: "that answer did not come back" } };
  }

  // Counted on every call that reached the model, whether or not the guard
  // kept the text. A refused answer costs the same as an accepted one.
  await env.ASK_KV.put(mk, String(spent + 1), { expirationTtl: 60 * 60 * 24 * 70 });

  if (!out.text) {
    return { status: 200, body: { text: "", withheld: false,
                                  error: "The record did not produce an answer to that." } };
  }

  const checked = verify(out.text, {
    allowed: new Set(pack.authorised_numerals),
    slugs: new Set(pack.slugs),
  });
  const rec = {
    text: checked.text,
    withheld: checked.withheld,
    reason: checked.reason ?? null,
  };
  if (checked.withheld) {
    console.log("answer withheld", JSON.stringify({
      reason: checked.reason, sentence: checked.sentence,
    }));
  }

  // Only a clean answer is cached. Re-asking a question the guard cut should
  // get another attempt rather than a stored stub, and an empty accepted
  // prefix is not worth a KV write.
  if (!checked.withheld && checked.text) {
    await env.ASK_KV.put(key, JSON.stringify(rec), { expirationTtl: ANSWER_TTL });
  }
  return { status: 200, body: { ...rec, cached: false } };
}

// ==================================================================
// worker.js
// ==================================================================

// The archive lane behind alaskaaihq.com/docket.
//
// WHAT THIS IS FOR, AND WHAT IT IS NOT FOR. Almost every question a person
// brings to a docket is a field read, a filter, a sort or a count, and all of
// those are answered inside the page by the engine in scripts/ask_answers.py
// with no request at all. This worker exists for the remainder: the
// open-ended question the published record does not have a field for. It is a
// link under a no-match, not the box's main path.
//
// WHY A WORKER AND NOT A DATABASE. This endpoint holds a few secrets and
// forwards one call. The only thing it stores is an in-flight request waiting
// for its answer, which expires by itself. There is no schema to migrate, no
// project to pause, and no row that can go stale. Cloudflare is already a
// dependency for Turnstile and a workers.dev URL needs no DNS change, so this
// adds a file rather than a vendor.
//
// WHY IT COSTS NOTHING NEW. Firing a routine spends a slot from the account's
// daily run cap and draws on the claude.ai subscription already being paid
// for. There is no Console key here and no metered API call. What it costs
// instead is time, because a fired routine starts a whole Claude Code session,
// so an answer takes minutes rather than a second. That trade is the reason
// the page treats this as an archive search and says so.
//
// WHAT MAKES IT HONEST. Nothing the routine writes reaches a reader unchecked.
// Every sentence of a delivered answer passes checks.js against the published
// corpus before it is stored, and a sentence that fails ends the answer there,
// visibly, rather than being quietly repaired.


const CORPUS_URL = "https://alaskaaihq.com/ask-corpus.json";
const MAX_QUESTION = 400;

const CORS = {
  "access-control-allow-origin": "https://alaskaaihq.com",
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers": "content-type",
  "access-control-max-age": "86400",
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...CORS },
  });
}

async function verifyTurnstile(token, secret, ip) {
  if (!secret) return true; // not configured; the deploy notes call this out
  if (!token) return false;
  const body = new FormData();
  body.append("secret", secret);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify",
    { method: "POST", body });
  const out = await r.json().catch(() => ({ success: false }));
  return out.success === true;
}

async function loadCorpus() {
  // cf.cacheTtl keeps the corpus at Cloudflare's edge, so verifying a
  // delivered answer does not pay a round trip to GitHub Pages to read a file
  // that changes once a day.
  const r = await fetch(CORPUS_URL, { cf: { cacheTtl: 900, cacheEverything: true } });
  if (!r.ok) throw new Error(`corpus fetch failed: ${r.status}`);
  return r.json();
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, { headers: CORS });

    const path = new URL(request.url).pathname.replace(/\/+$/, "");

    // A presence check. Booleans only, never a value, so this leaks nothing an
    // error message does not already imply.
    //
    // It exists because "the answerer is not configured" cannot say WHICH of
    // the three is missing without printing secrets, and the alternative is
    // asking a person to re-read a settings page and taking their word for it.
    // That went several rounds and got nowhere. One request answers it.
    if (path === "/_config") {
      return json({
        kv_binding: !!env.ASK_KV,
        anthropic_key: !!env.ANTHROPIC_API_KEY,
        turnstile_secret: !!env.TURNSTILE_SECRET,
        routine_token: !!env.ROUTINE_TOKEN,
        monthly_cap: capOf(env),
        model: env.ASK_MODEL || "(default)",
        pack_url: env.ASK_PACK_URL || "(default)",
        // Every name the worker can actually see, so a typo shows up as the
        // wrong string rather than as a missing one.
        visible: Object.keys(env).sort(),
      });
    }

    // Polling is a GET because it happens every few seconds for minutes and
    // has no body; everything else is a POST.
    if (path === "/result") {
      const id = new URL(request.url).searchParams.get("id") || "";
      const out = await result(id, env);
      return json(out.body, out.status);
    }

    if (request.method !== "POST") return json({ error: "POST only" }, 405);

    // The routine delivering a finished answer. Not from a browser, so it is
    // outside the Turnstile path and behind a shared secret instead.
    if (path === "/deliver") {
      let body;
      try { body = await request.json(); } catch { return json({ error: "invalid JSON" }, 400); }
      let corpus;
      try { corpus = await loadCorpus(); } catch { return json({ error: "corpus unreachable" }, 502); }
      const out = await deliver(body, env, corpus);
      return json(out.body, out.status);
    }

    if (path !== "/deep" && path !== "/answer") {
      return json({ error: "not found" }, 404);
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return json({ error: "invalid JSON" }, 400);
    }

    const question = String(payload.question ?? "").trim();
    if (!question) return json({ error: "ask a question" }, 400);
    if (question.length > MAX_QUESTION) {
      return json({ error: `keep it under ${MAX_QUESTION} characters` }, 400);
    }

    const ip = request.headers.get("cf-connecting-ip") || "";
    const human = await verifyTurnstile(payload.turnstile_token, env.TURNSTILE_SECRET, ip);
    if (!human) return json({ error: "finish the human check first" }, 403);

    // The written answer. Costs a metered model call, so it sits behind the
    // same human check the archive lane does, and behind a monthly ceiling of
    // its own inside answer(). It returns the answer directly rather than an
    // id to poll, because it takes about two seconds rather than minutes.
    if (path === "/answer") {
      // Streamed by default. The guard checks a sentence at a time anyway, so
      // a verified sentence can be shown the moment it is complete rather than
      // after the whole reply lands, which is most of why the wait feels long.
      // A client can still ask for the whole thing at once.
      if (payload.stream === false) {
        const out = await answer(question, env);
        return json(out.body, out.status);
      }
      return new Response(await answerStream(question, env), {
        headers: {
          "content-type": "application/x-ndjson; charset=utf-8",
          "cache-control": "no-store",
          ...CORS,
        },
      });
    }

    // Starting a research run spends a slot from the account's daily routine
    // cap and draws on the same subscription usage the carousel spends, so it
    // sits behind a human check and returns an id the page polls rather than
    // an answer.
    if (!env.ROUTINE_TOKEN || !env.ROUTINE_TRIGGER_ID || !env.ASK_KV) {
      return json({ error: "research is not configured" }, 503);
    }
    try {
      return json({ id: await start(question, env) });
    } catch (e) {
      console.log("fire failed", String(e));
      return json({ error: "could not start the research run" }, 502);
    }
  },
};
