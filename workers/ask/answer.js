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
// WHAT IT COSTS, AND WHY THAT CANNOT RUN AWAY.
//
// This paragraph used to name THREE things holding the month down, and the
// first of them stopped being true on 2026-08-15. It said the engine absorbs
// most questions before this lane is reached. It does not any more. Submitting
// a question on the docket page calls this lane every time, deliberately,
// because routing a submit to the engine's top hit is exactly what made the
// written answer unreachable: the engine nearly always has SOME match, so the
// reader never got past it. The engine is still free and still instant, but it
// is now what you get while TYPING, and typing is not what spends money.
//
// So TWO things bound the month, and both are real:
//   identical questions are served from KV for nothing
//   a monthly call ceiling degrades the box back to the engine and the archive
//   button rather than spending past a number the operator set
//
// At Sonnet 5's introductory rate and this pack size a question is about 4.3
// cents, so the default 500 call ceiling is about 21 dollars a month. When the
// introductory rate ends on 2026-08-31 the same ceiling is about 32 dollars.
// The bill has a maximum you choose, not a maximum the internet chooses, and
// ASK_MONTHLY_CAP is where you choose it.

import { checkSentence, splitSentences } from "./checks.js";

const API = "https://api.anthropic.com/v1/messages";
const PACK_URL = "https://alaskaaihq.com/ask-pack.json";

// The model, pinned here rather than left to a variable.
//
// ASK_MODEL still wins if it is set, but it is not how this gets changed any
// more. Setting that variable in the Cloudflare dashboard and deploying twice
// never made it visible to the running worker: Object.keys(env) listed the
// other three every time and never this one. Rather than keep asking a person
// to click Deploy again, the choice lives in code, where it is reviewable and
// where changing it is the same one paste as any other worker change.
//
// Sonnet 5 while its behaviour is being compared against Haiku 4.5 on the
// standing eval set. Haiku answered the hardest question on that set well, so
// this is a measurement and not a conclusion. Switching back is one line.
//
// NOTE ON PRICE: Sonnet 5's introductory rate ends 2026-08-31, after which
// input goes $2 to $3 per million and output $10 to $15. At this pack size
// that moves a question from about 4.3 cents to about 6.4 cents.
const DEFAULT_MODEL = "claude-sonnet-5";

// Three or four sentences. The guard checks sentence by sentence and the page
// shows a short answer, so a long generation is spend with nowhere to go.
const MAX_TOKENS = 1024;

/**
 * Models that REJECT a non-default temperature, top_p or top_k with a 400 on
 * every request, thinking or not.
 *
 * This is what broke the box the moment it moved off Haiku. The request sent
 * temperature 0, which is fine on Haiku 4.5 and an instant 400 on Sonnet 5, so
 * every answer came back as "that answer did not come back" and three rounds
 * went into guessing at the key, the model name and the account.
 *
 * A list rather than a try-and-retry, because a 400 costs a round trip and
 * this is knowable up front. From the thinking docs, sampling parameters
 * section: Fable 5, Mythos 5, Opus 5, Opus 4.8, Opus 4.7 and Sonnet 5.
 */
const NO_SAMPLING = /^claude-(fable-5|mythos-5|mythos-preview|opus-5|opus-4-8|opus-4-7|sonnet-5)/;

/**
 * Models with thinking ON by default. Their thinking tokens are billed as
 * output and count against max_tokens, which for a three sentence answer is
 * paying to deliberate about a lookup. Turned off where the docs say it can
 * be, left alone everywhere else.
 */
const THINKS_BY_DEFAULT = /^claude-(opus-5|sonnet-5|fable-5|mythos-5|mythos-preview)/;

/**
 * The parts of a request that depend on which model is answering. One place,
 * so the streaming path and the plain one cannot drift into disagreeing about
 * what the model will accept.
 */
export function modelParams(model) {
  const out = {};
  if (!NO_SAMPLING.test(model)) out.temperature = 0;
  if (THINKS_BY_DEFAULT.test(model)) out.thinking = { type: "disabled" };
  return out;
}

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

// How much of the conversation goes back with a follow-up, counted in
// messages so four exchanges. A docket conversation that has run longer than
// that has usually moved on to a new subject, and every turn kept is input
// paid for again on the next question. At about 150 tokens a turn against a
// 21,000 token record this is a rounding error either way, which is the point:
// it is bounded on purpose rather than growing until someone notices a bill.
const MAX_TURNS = 8;

/**
 * The conversation, cleaned. Anything the page sends is untrusted: only the
 * two roles exist, content is a string, empty turns go, and the tail is what
 * survives. It must end on the reader, because a model answering its own last
 * answer is not a conversation.
 */
export function turnsOf(payload) {
  const raw = Array.isArray(payload.messages) ? payload.messages : null;
  if (!raw) {
    const q = String(payload.question ?? "").trim();
    return q ? [{ role: "user", content: q }] : [];
  }
  const clean = [];
  for (const m of raw) {
    const role = m && m.role === "assistant" ? "assistant" : "user";
    const content = String((m && m.content) ?? "").trim().slice(0, 4000);
    if (content) clean.push({ role, content });
  }
  while (clean.length && clean[clean.length - 1].role !== "user") clean.pop();
  return clean.slice(-MAX_TURNS);
}

/**
 * Ask the API one trivial question and report what came back.
 *
 * This exists because "that answer did not come back" is true of a rejected
 * model name, an unfunded key, a key from the wrong organisation, a rate limit
 * and a network fault, and telling those apart from outside took several
 * rounds of asking a person to change a setting and try again. One request
 * settles it instead.
 *
 * Deliberately tiny: two tokens in, one token out, no record attached. It
 * spends a hundredth of a cent, so leaving it reachable is cheaper than the
 * time it saves. It returns the API's own status and error type, never the
 * key and never a full response body.
 */
export async function probe(env, fetchImpl = fetch) {
  if (!env.ANTHROPIC_API_KEY) return { ok: false, why: "no ANTHROPIC_API_KEY" };
  const model = effectiveModel(env);
  try {
    const r = await fetchImpl(API, {
      method: "POST",
      headers: {
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({ model, max_tokens: 1, ...modelParams(model),
                             messages: [{ role: "user", content: "hi" }] }),
    });
    const raw = await r.text().catch(() => "");
    let type = null, message = null;
    try {
      const j = JSON.parse(raw);
      type = j?.error?.type ?? null;
      message = j?.error?.message ?? null;
    } catch { message = raw.slice(0, 160); }
    return { ok: r.ok, status: r.status, model, error_type: type, error_message: message };
  } catch (e) {
    return { ok: false, model, threw: String(e).slice(0, 200) };
  }
}

/** The model a request will actually use. One source, so the diagnostic and
 *  the call can never disagree about it. */
export function effectiveModel(env) {
  return env.ASK_MODEL || DEFAULT_MODEL;
}

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

/**
 * The key covers the WHOLE conversation, not the latest question. "What about
 * the other one" means something different after every first question, so
 * keying on the last message alone would serve one thread's answer into
 * another's. Follow-ups mostly miss the cache and that is correct.
 */
export async function cacheKey(turns, packDate) {
  const thread = (Array.isArray(turns) ? turns : [{ role: "user", content: String(turns) }])
    .map(m => m.role + ":" + normaliseQuestion(m.content)).join("\n");
  const data = new TextEncoder().encode(`${packDate}\n${thread}`);
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

export async function callModel(turns, pack, env, fetchImpl = fetch) {
  const r = await fetchImpl(API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: effectiveModel(env),
      max_tokens: MAX_TOKENS,
      ...modelParams(effectiveModel(env)),
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
      messages: turns,
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
export async function streamModel(turns, pack, env, onDelta, fetchImpl = fetch) {
  const r = await fetchImpl(API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: effectiveModel(env),
      max_tokens: MAX_TOKENS,
      ...modelParams(effectiveModel(env)),
      stream: true,
      system: [
        { type: "text", text: pack.system },
        { type: "text", text: pack.pack },
      ],
      messages: turns,
    }),
  });
  if (!r.ok || !r.body) {
    const detail = await r.text().catch(() => "");
    const e = new Error(`messages ${r.status}: ${String(detail).slice(0, 300)}`);
    e.status = r.status;
    throw e;
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
async function preflight(turns, env, now) {
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

  const key = await cacheKey(turns, pack.generated);
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
export async function answerStream(turns, env, { now, fetchImpl } = {}) {
  const pre = await preflight(turns, env, now);
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
        await streamModel(turns, pack, env, (delta) => {
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
        /* Say WHICH failure it was. "That answer did not come back" covers a
           rejected model name, an unfunded key, a rate limit and a network
           blip, and telling a reader nothing also told the person debugging
           it nothing. The status is not sensitive; the body is never shown. */
        const st = e && e.status;
        c.enqueue(line({ error:
          st === 400 ? "The model rejected that request. This is a configuration fault, not your question." :
          st === 401 || st === 403 ? "The answer service is not authorised. Its API key needs checking." :
          st === 404 ? "The configured model does not exist. Check ASK_MODEL." :
          st === 429 ? "Too many questions at once. Give it a few seconds." :
          st >= 500 ? "The model is having a moment. Try again shortly." :
          "That answer did not come back.",
          status: st || null }));
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
export async function answer(turns, env, { now, fetchImpl } = {}) {
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

  const key = await cacheKey(turns, pack.generated);
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
    out = await callModel(turns, pack, env, fetchImpl || fetch);
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
