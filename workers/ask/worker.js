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

import * as deep from "./deep.js";
import { answer, answerStream, capOf, effectiveModel, turnsOf } from "./answer.js";

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
        // The model actually in use, not the variable. Reporting the variable
        // and calling it "(default)" when unset told a debugger nothing about
        // which model that resolved to, which is the one question the endpoint
        // existed to answer.
        model: effectiveModel(env),
        model_from: env.ASK_MODEL ? "ASK_MODEL variable" : "pinned in code",
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
      const out = await deep.result(id, env);
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
      const out = await deep.deliver(body, env, corpus);
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

    // The conversation, not just the latest line. A follow-up like "what about
    // the other one" only means anything with what came before it.
    const turns = turnsOf(payload);
    if (!turns.length) return json({ error: "ask a question" }, 400);
    const question = turns[turns.length - 1].content;
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
        const out = await answer(turns, env);
        return json(out.body, out.status);
      }
      return new Response(await answerStream(turns, env), {
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
      return json({ id: await deep.start(question, env) });
    } catch (e) {
      console.log("fire failed", String(e));
      return json({ error: "could not start the research run" }, 502);
    }
  },
};
