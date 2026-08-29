# The ask box

Three lanes behind one box on the docket page, in the order they are reached.

| Lane | Where it runs | Answers from | Speed | Costs |
|---|---|---|---|---|
| **the engine** | the reader's browser | the record shipped inside the page | the same frame | nothing |
| **the answerer** | this worker, one model call | the whole record, in one prompt | seconds, streamed | model tokens, cached and capped monthly |
| **the archive** | this worker, via a fired routine | the whole repository | minutes | a slot from the daily routine cap |

**No retrieval anywhere in this.** Not vectors, not grep. The August 28th
self-test estimates the published record at about 68,000 rough tokens against
a 200,000 token context, so the answerer is
handed the whole thing on every question. Retrieval exists to work around a
corpus that will not fit, and this one fits. Skipping it deletes the single
largest source of wrong answers in a retrieval chatbot, which is retrieving the
wrong passage, rather than leaving it to be tuned.

The archive lane is the one place retrieval is genuinely needed, because the
repository is about 3.5 million tokens. It is a Claude Code session with a
shell, which is to say an agent that greps. That is the right tool at that
size and the wrong tool at this one.

**The engine is the classifier and safety net.** It needs no worker, no key and
no network. On a first turn it recognizes record vocabulary, entities, date
windows and Docket-level questions; an obvious off-record question is refused
locally before it can spend or improvise. Follow-ups always pass because their
subject may live in the earlier exchange. On phones the engine's live result
cards are hidden. A deliberate on-record submit is therefore always answered
by the written agent, while the deterministic answer remains available as the
same-thread fallback if the monthly model ceiling has been reached.

Its code is `scripts/ask_answers.py`, which builds the payload, and `ASK_JS`
in `scripts/site_build.py`, which resolves a question against it. Its tests
are `scripts/ask_answers.py --self-test` and `tests/ask_engine.mjs`.

**This worker writes the submitted answer.** Typing stays in the free browser
engine; pressing Enter or the arrow classifies the first turn, then sends an
on-record conversation to `/answer` for a short written response. The
full-archive button remains the heavier escalation
shown on a no-match. Both remote lanes are optional and the box works without
them. Until `ASK_ENDPOINT` is set, submitting falls back to the local engine.

Neither fires on its own. Typing never sends or spends; a deliberate submit or
archive press does. On phones, a submit opens a full-height conversation sheet
with a pinned composer. The progress trace is fed by real Worker events
(`record`, `draft`, `verify`), and reports verified sentence counts. It never
simulates private model reasoning.

```
a submitted question
   |
   v
POST /answer              the whole record in one prompt, answer returned
   |                      Turnstile gates it, ASK_MONTHLY_CAP bounds it, and
   |                      every sentence passes checks.js before it is
   |                      returned. Over the cap, this steps aside and the
   |                      deterministic answer is rendered in the same thread.
   |
   | still not it
   v
POST /deep                fires the routine, returns a request id
   |                      Turnstile gates this, because each one spends a
   |                      slot from the account's daily routine cap
   v
the routine               a whole Claude Code session, reading the repository
   |
   v
POST /deliver             behind DELIVER_SECRET, verified sentence by sentence
   |                      against docs/ask-corpus.json before it is stored
   v
GET /result?id=...        the page has been polling for it
```

## What each lane costs, and why the bill has a ceiling

**The archive lane has no API key.** The routine trigger's token is a
`sk-ant-oat01-` bearer generated in one click at
[claude.ai/code/routines](https://claude.ai/code/routines), and it draws on the
claude.ai subscription rather than on Console credit. No card, no separate
account, no metered call.

**The answerer does have one, and it is the only metered thing here.**
`ANTHROPIC_API_KEY`, a Console key. The default model is pinned in `answer.js`;
the current value is Sonnet 5. The August 28th corpus self-test estimates a
request carries roughly 68,000 input tokens of
record plus a short answer. Two things keep the month bounded, in this order:

1. An identical question is served from KV, keyed by the question and the pack
   date, so a repeat costs nothing and a new pack retires yesterday's answers.
   This is never announced in the UI; cached and fresh replies share the same
   sentence protocol and provenance surface.
2. `ASK_MONTHLY_CAP` counts calls that reached the model. Over it, the lane
   steps aside and the box falls back to the engine and the archive button,
   with the reader told why. The default is 500. Set it to 0 to switch the lane
   off without a deploy. Recalculate the maximum from current model pricing
   before changing either the model or cap.

**The record block is prompt-cacheable.** This is Anthropic prompt caching,
separate from the KV answer cache above. The stable record is a separate
system block marked with one ephemeral cache breakpoint; per-question rules
remain above it. Tests assert the byte-stable prefix and the single marker so a
request-specific value cannot silently destroy cache reuse.

This reverses the call made on August 9th, 2026, when the paid Messages API
lane was removed because free was a requirement. What makes it safe now and did
not then is the ceiling: the bill has a maximum the operator sets, not a
maximum the internet sets.

What it costs instead is time. A fired routine starts a whole Claude Code
session, so an answer takes minutes, and each one spends a slot from the
account's daily run cap that the daily carousel also draws on. That trade is
the reason the page calls this searching the archive and says how long it
takes.

The in-page engine and both remote lanes share the same published record and
sentence guard. `checks.js` is the release boundary for every model-written
sentence, whether it came from the seconds-long answerer or the minutes-long
archive run.

## Why there is no vector database here

The current record is about 68,000 rough tokens. Retrieval, embeddings, reranking and a
vector index exist to choose what to show a model that cannot see everything.
Anything reading this record can see all of it, so that machinery would add
latency, cost, and a class of failure the corpus size otherwise deletes: a
retriever that fetches the wrong passage answers confidently from the wrong
source, and no reranker recovers that.

The published guidance for 2026 puts the crossover at roughly 500,000 tokens.
This record is about fourteen percent of that, and it would have to grow by a factor
of roughly seven before retrieval started paying for itself.

## Setting it up

Three things, in this order. Nothing renders on the site until the last one.

### 1. The routine

`prompts/ASK_ROUTINE.md` carries the prompt to paste and, more importantly,
the environment to put it in. **Read the warning at the top of that file
before you create the routine.** It is the only thing in this project that
runs on text a stranger typed, and the default is that every connector on your
account is attached to it.

Create it at [claude.ai/code/routines](https://claude.ai/code/routines), add
an API trigger, and keep the `sk-ant-oat01-` token and the `trig_...` id. Put
`DELIVER_SECRET` into the routine's cloud environment variables with the same
value you are about to give the worker.

### 2. The worker

```bash
npm install -g wrangler          # once
wrangler login                   # same Cloudflare account as Turnstile

cd workers/ask
wrangler kv namespace create ASK_KV       # paste the printed id into wrangler.toml

wrangler secret put ROUTINE_TOKEN         # sk-ant-oat01-... from the API trigger
wrangler secret put ROUTINE_TRIGGER_ID    # trig_... from the same modal
wrangler secret put DELIVER_SECRET        # the same long random string the routine has
wrangler secret put TURNSTILE_SECRET      # from the Turnstile widget's settings

wrangler deploy
```

`wrangler deploy` prints the URL, which looks like
`https://alaskaai-ask.<your-subdomain>.workers.dev`.

No DNS change is needed. The site stays on GitHub Pages and calls the
workers.dev URL cross-origin, the same shape as the existing scanner calls.

### 3. The site

Set the URL and rebuild. It can come from the environment, so turning the lane
on does not have to be a code change:

```bash
ASK_ENDPOINT=https://alaskaai-ask.<your-subdomain>.workers.dev \
  python3 scripts/site_build.py --date "$(TZ=America/Anchorage date +%F)" --out docs
```

To make it permanent, put the same URL in `ASK_ENDPOINT` at the top of
`scripts/site_build.py`. The environment wins over the constant when both are
set, so a one-off build can point at a staging worker without editing
anything.

## Turnstile

The secret belongs to the same widget whose sitekey is already in
`site_build.py` (`0x4AAAAAAD7e1lYKOUSxa5sV`). Find it at
<https://dash.cloudflare.com> under **Turnstile**, the widget's **Settings**,
then **Secret key**.

If `TURNSTILE_SECRET` is unset, the Worker fails closed. A missing secret,
missing browser token, failed verification request, or negative Cloudflare
response is refused before either paid lane runs.

## Watching it

```bash
wrangler tail                    # live log
```

Two things are logged. `withheld` records every sentence a check refused, with
the question, the sentence, and which control caught it; those are worth
reading because they are either the guard working or the guard misfiring, and
you cannot tell which without looking. `fire failed` records a routine that
would not start.

Nothing else is stored. Questions are not persisted beyond the in-flight
entry, which expires by itself, so the log is the only record and it rolls
off.

## Tests

```bash
node test.mjs                                     # the answer checks
node test-deep.mjs                                # delivery auth and the poll state machine
node test-answer.mjs                              # answer protocol, cache, cap and human gate
node test-bundle.mjs                              # deployed bundle equals its modules
python3 ../../scripts/ask_corpus.py --self-test   # the corpus and its allow-list
```

All three run in CI on any change under `workers/ask/`, to the corpus builder,
or to the routine prompt, alongside the in-page engine's own two suites.
