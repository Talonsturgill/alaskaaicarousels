// Tests for the deep lane. Run: node workers/ask/test-deep.mjs
//
// The lane's whole risk is that a slower answer feels like a more trusted one.
// It is not: it came from a model too, and it had a whole repository to invent
// figures from rather than one file. So the same checks run on delivery, and
// the cases below are mostly about proving that.
//
// KV is faked with a Map. The point is the verification and the state machine,
// neither of which cares what the store is.

import { newId, verify, deliver, result } from "./deep.js";

let failures = 0;
function check(label, cond, detail = "") {
  console.log(`  ${cond ? "PASS" : "FAIL"}  ${label}${detail ? "  " + detail : ""}`);
  if (!cond) failures++;
}
function section(n) { console.log(n); }

function fakeKV() {
  const m = new Map();
  return {
    async get(k) { return m.has(k) ? m.get(k) : null; },
    async put(k, v) { m.set(k, v); },
    _map: m,
  };
}

const corpus = {
  authorised_numerals: ["6.54", "50.3", "2026", "7"],
  slugs: ["aidea-houston-industrial-park", "bradley-lake-dixon-diversion"],
};
const sets = {
  allowed: new Set(corpus.authorised_numerals),
  slugs: new Set(corpus.slugs),
};

section("request ids");
{
  const a = newId(), b = newId();
  check("an id is 20 lowercase hex characters", /^[a-f0-9]{20}$/.test(a), a);
  check("two ids differ", a !== b);
}

section("the same checks run on a delivered answer");
{
  const clean = verify(
    "Comments are open [[aidea-houston-industrial-park]]. Storage was 6.54 Bcf.", sets);
  check("a clean answer survives whole", !clean.withheld && clean.text.includes("6.54"),
    JSON.stringify(clean.text));

  // The failure this lane is most exposed to. A routine reads the entire
  // repository, so it has far more raw material to derive an unpublished
  // figure from than the fast lane ever sees.
  const bad = verify("Storage was 6.54 Bcf. It will hit 12.75 Bcf by November.", sets);
  check("an invented figure truncates the answer", bad.withheld && bad.reason === "numeral",
    JSON.stringify(bad));
  check("the verified opening is kept", bad.text === "Storage was 6.54 Bcf.",
    JSON.stringify(bad.text));

  const verdict = verify("There is enough gas for the winter.", sets);
  check("a verdict is refused here too", verdict.withheld && verdict.reason === "verdict");
  check("and nothing is kept when the first sentence fails", verdict.text === "",
    JSON.stringify(verdict.text));

  const cite = verify("See [[not-a-real-item]].", sets);
  check("an invented citation is refused", cite.withheld && cite.reason === "citation");
}

section("delivery is authenticated");
{
  const env = { ASK_KV: fakeKV(), DELIVER_SECRET: "s3cret" };
  const id = "a".repeat(20);
  await env.ASK_KV.put(`q:${id}`, JSON.stringify({ state: "running" }));

  let out = await deliver({ id, answer: "Storage was 6.54 Bcf.", secret: "wrong" }, env, corpus);
  check("a wrong secret is refused", out.status === 403, String(out.status));

  out = await deliver({ id, answer: "Storage was 6.54 Bcf." }, env, corpus);
  check("a missing secret is refused", out.status === 403, String(out.status));

  // The hole this closes: without a secret, anyone who guessed a request id
  // could publish text under the site's name.
  const noSecret = { ASK_KV: fakeKV(), DELIVER_SECRET: "" };
  out = await deliver({ id, answer: "x", secret: "" }, noSecret, corpus);
  check("an unconfigured worker refuses delivery rather than accepting it",
    out.status === 403, String(out.status));

  out = await deliver({ id: "nope", answer: "x", secret: "s3cret" }, env, corpus);
  check("a malformed id is refused", out.status === 400, String(out.status));

  out = await deliver({ id: "b".repeat(20), answer: "x", secret: "s3cret" }, env, corpus);
  check("an unknown id is refused", out.status === 404, String(out.status));
}

section("the state machine a page polls");
{
  const env = { ASK_KV: fakeKV(), DELIVER_SECRET: "s3cret" };
  const id = "c".repeat(20);
  await env.ASK_KV.put(`q:${id}`,
    JSON.stringify({ question: "what can I comment on?", state: "running" }));

  let r = await result(id, env);
  check("it reads as running before delivery", r.body.state === "running", JSON.stringify(r.body));
  check("the question is not echoed back to a guessed id",
    !("question" in r.body), JSON.stringify(Object.keys(r.body)));

  await deliver({ id, secret: "s3cret",
    answer: "Comments are open [[bradley-lake-dixon-diversion]]." }, env, corpus);
  r = await result(id, env);
  check("it reads as done after delivery", r.body.state === "done", JSON.stringify(r.body.state));
  check("the answer comes back", r.body.text.includes("bradley-lake"), r.body.text);
  check("and it is not marked withheld", r.body.withheld === false);

  r = await result("d".repeat(20), env);
  check("an id that was never issued reads as expired",
    r.status === 404 && r.body.state === "expired", JSON.stringify(r.body));

  r = await result("!!", env);
  check("a malformed id is refused", r.status === 400);
}

section("an empty delivery is a failure, not an answer");
{
  const env = { ASK_KV: fakeKV(), DELIVER_SECRET: "s3cret" };
  const id = "e".repeat(20);
  await env.ASK_KV.put(`q:${id}`, JSON.stringify({ state: "running" }));
  await deliver({ id, secret: "s3cret", answer: "   " }, env, corpus);
  const r = await result(id, env);
  check("a blank answer records a failure", r.body.state === "failed", JSON.stringify(r.body));
  check("and says so rather than showing nothing", !!r.body.error, String(r.body.error));
}

console.log();
console.log(failures === 0 ? "deep lane clean" : `deep lane FAILED (${failures})`);
process.exit(failures === 0 ? 0 : 1);
