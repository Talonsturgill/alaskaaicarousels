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

// HOW THE HOUSE PUNCTUATES, APPLIED TO A MACHINE THAT DOES NOT.
//
// Em dashes, en dashes, semicolons and colons are the four marks that make a
// sentence read as written by a language model rather than said by a person,
// and the first two are already banned everywhere else this repo publishes
// (CLAUDE.md, config/brand.yaml, scripts/caption_check.py). The model is told
// all four in the prompt. This is what happens when it forgets.
//
// REPAIRED, NOT REJECTED, AND THAT IS A DELIBERATE LINE. The checks above cut
// an answer at the first sentence that fails, because a wrong number and an
// invented citation are claims about the world and a smoothed over one is
// worse than a visible stop. A semicolon is not a claim about anything. Ending
// an answer over a punctuation mark would punish the reader for the model's
// typing, so this rewrites and says nothing.
//
// The rewrite runs BEFORE the sentence is checked and before it is sent, so
// the text a reader sees is the exact text that passed. There is no window in
// which a checked sentence is edited.
//
// Nothing here can touch a figure. Every rule below either replaces a mark
// with another mark or lifts a letter to a capital. The one rule that goes
// near digits, a dash between two numbers, keeps them both and leaves a
// hyphen, because turning 2024-2025 into "2024, 2025" would change what it
// says and this file's whole job is that nothing does.
const FILLER = [
  // Whole sentences that carry no content. Removed entirely.
  /^(?:great|good|excellent|interesting)\s+question[.!]?\s*/i,
  /^(?:certainly|absolutely|sure thing|sure|of course|indeed)[,.!]\s*/i,
  /^i hope (?:this|that) helps[.!]?\s*/i,
  /^happy to help[.!]?\s*/i,
  // Throat clearing in front of a real sentence. The clause goes, what
  // follows it is lifted to a capital and keeps its meaning intact.
  /^(?:it'?s |it is )?(?:worth |important |also worth )?(?:noting|mentioning|pointing out) that\s+/i,
  /^(?:please )?(?:do )?note that\s+/i,
  /^to (?:be clear|answer your question|directly answer)[,:]?\s+/i,
  /^in (?:conclusion|summary|short)[,:]?\s+/i,
  /^at its core[,:]?\s+/i,
  /^that (?:being )?said[,:]?\s+/i,
];

export function plainly(text) {
  let t = String(text)
    // House straight quotes, same rule the site builder enforces on itself.
    .replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/…/g, "...")
    // A range keeps its reading. This is the only rule that sees a digit.
    .replace(/(\d)\s*[—–]\s*(\d)/g, "$1-$2")
    // Any other dash was standing in for a comma, so it becomes one. The
    // leading [,\s]* absorbs a comma already sitting there, which is how
    // ", and, then" would otherwise happen.
    .replace(/[,\s]*[—–]\s*/g, ", ")
    // A semicolon joins two sentences that wanted to be two sentences.
    .replace(/;\s+([a-z])/g, (_, c) => ". " + c.toUpperCase())
    .replace(/;(?=\s)/g, ".")
    // A colon reads as a slide heading. A comma reads as a person talking.
    // Only when whitespace follows, which is what keeps 12:30 and https://
    // whole, and what makes this safe to run on a half arrived stream: a
    // colon at the end of the buffer is left until its next character lands.
    .replace(/:(?=\s)/g, ",")
    // Tidying after the two rules above, which can leave a comma doubled, a
    // comma in front of a full stop, or a comma opening the answer when the
    // model started a line with a dash.
    .replace(/,\s*,/g, ",")
    .replace(/,\s*([.!?])/g, "$1")
    .replace(/^[,\s]+/, "");
  for (const re of FILLER) {
    const before = t;
    t = t.replace(re, "");
    if (t !== before) t = t.charAt(0).toUpperCase() + t.slice(1);
  }
  return t;
}

// Split on sentence ends only where a space follows, so decimals (6.54 Bcf)
// and abbreviated dockets stay whole. A trailing fragment is returned as the
// remainder for the next chunk rather than checked early.
//
// The house rewrite runs here rather than at the three call sites, because
// three places to remember is three places to forget, and a sentence that
// reached a reader unrewritten would be the one nobody noticed.
export function splitSentences(buffer) {
  const parts = plainly(buffer).split(/(?<=[.!?])\s+/);
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
 * Where the month stands against its ceiling.
 *
 * The counter has always existed, because the cap is enforced by reading it.
 * What did not exist was any way to LOOK at it. The only signal that the month
 * was nearly spent was a reader hitting the wall, which is finding out from
 * the person you least wanted to find out from. This reports the same number
 * the gate reads, so it cannot disagree with enforcement.
 *
 * A count of model calls, not dollars. Repeats served from KV never increment
 * it, so this is distinct questions that reached the model, which is exactly
 * what the ceiling counts. The dollar figure is that count times the per
 * question cost, and it is left to the reader rather than hardcoded here,
 * because a rate that changes on 2026-08-31 would go stale in the one place
 * nobody would think to check.
 */
export async function spendOf(env, nowISO) {
  const cap = capOf(env);
  if (!env.ASK_KV) return { cap, spent: null, left: null, note: "no KV bound" };
  const key = monthKey(nowISO || new Date().toISOString());
  const spent = Number(await env.ASK_KV.get(key)) || 0;
  return { month: key.slice(6), cap, spent, left: Math.max(0, cap - spent) };
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

/**
 * The system blocks, with the record marked cacheable.
 *
 * WHY THIS IS ON NOW WHEN IT WAS DELIBERATELY OFF BEFORE. A cache write costs
 * 1.25x a plain read, so caching LOSES money on a question that arrives alone
 * and wins 90 percent on one that arrives behind another. At the traffic this
 * box had when the two blocks were first split apart, alone was the normal
 * case and turning this on would have raised the bill.
 *
 * What changed is not the traffic estimate, it is the SHAPE of a question.
 * This box holds conversations now, on two pages. Every follow-up turn re-sends
 * the same 21,800 token prefix seconds after the last one, which is inside the
 * five minute window by construction, not by luck. A four turn conversation
 * pays 1.25x once and 0.1x three times: about 61 percent less than four full
 * reads.
 *
 * The arithmetic, so nobody has to re-derive it. Caching pays when more than
 * (w - 1) / (w - 0.1) of questions land inside the window, w being the write
 * multiplier. At 1.25 that is 22 percent. Follow-ups alone should clear it.
 * The downside if they do not is 25 percent on an isolated question, which is
 * the smaller half of a bet worth taking.
 *
 * ONE MARKER, ON THE SECOND BLOCK. The rules are stable and the record changes
 * daily, and a marker on the last block caches everything before it, so this
 * covers both. The two-block split has been sitting here waiting for exactly
 * this line since the day it was written.
 *
 * Nothing per-request may ever be added above this marker. The prefix is a
 * byte match, so one interpolated timestamp or reader id would silently make
 * every request a fresh write, and the bill would go up 25 percent with
 * nothing in the logs to say why. usage.cache_read_input_tokens is how you
 * check; /_config reports the month's spend beside it.
 */
export function systemBlocks(pack) {
  return [
    { type: "text", text: pack.system },
    { type: "text", text: pack.pack, cache_control: { type: "ephemeral" } },
  ];
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
      system: systemBlocks(pack),
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
      system: systemBlocks(pack),
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

// ==================================================================
// worker.js
// ==================================================================

// The archive lane behind alaskaaihq.com/docket.
//
// WHAT THIS IS FOR. Two lanes, and they are reached differently, which was
// not always true and is worth stating plainly because the cost follows it.
//
//   /answer   the written sentence. This is what SUBMITTING a question does,
//             on the docket page and on the homepage both. It is the box's
//             main path now, not a fallback. It stopped being a fallback on
//             2026-08-15: it used to hang off the no-match panel, the engine
//             nearly always had SOME match, so the panel nearly never rendered
//             and the lane was reachable in principle and unreachable in fact.
//   /deep     the archive search, which reads the whole repository. Still a
//             button under a no-match, because reading everything only makes
//             sense once the record itself has come up empty.
//
// The engine in scripts/ask_answers.py has not gone anywhere and still answers
// every field read, filter, sort and count with no request at all. That is the
// live list under the field while a person TYPES, and it is free and instant.
// Pressing the button is the part that asks a model, and the page says so
// above the button, before the press.
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
        // Where the month actually stands. Reported here because the only
        // other way to learn it was a reader hitting the wall.
        spend: await spendOf(env),
        // Whether the archive lane can run, from the same function the gate
        // uses. routine_token above answers a narrower question and answering
        // it alone once read as "nearly configured" when the lane was off.
        research: ready(env),
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

    // Does the API actually answer this worker? /_config reports what is
    // configured; this reports whether the configuration WORKS, which is a
    // different question and the one that matters when an answer fails.
    if (path === "/_probe") {
      return json(await probe(env));
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
    // 503 specifically, and the page reads the status rather than this string:
    // a lane that is switched off is a permanent condition, not a request that
    // went wrong, so it must not be offered again or answered with "try again".
    if (!ready(env)) {
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
