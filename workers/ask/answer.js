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

import { checkSentence, splitSentences } from "./checks.js";

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
