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

import { checkSentence, splitSentences } from "./checks.js";

const FIRE = "https://api.anthropic.com/v1/claude_code/routines";
const BETA = "experimental-cc-routine-2026-04-01";

// A question waits at most this long before the page gives up on it. A routine
// run that has not delivered in twenty minutes is not coming.
const TTL = 60 * 25;

export function newId() {
  return crypto.randomUUID().replace(/-/g, "").slice(0, 20);
}

/**
 * Whether this lane can actually run.
 *
 * One function, read by the gate that turns a request away AND by /_config
 * that reports it, so enforcement and diagnosis can never drift apart. They
 * had drifted: /_config reported routine_token by itself, and the page decided
 * whether to show the button from whether an endpoint existed, which is a
 * different question. The result was a button offered on a site where the lane
 * had never been configured, answering every press with a 503.
 */
export function ready(env) {
  return !!(env.ROUTINE_TOKEN && env.ROUTINE_TRIGGER_ID && env.ASK_KV);
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
export function verify(answer, { allowed, slugs }) {
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

  const checked = verify(answer, {
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
