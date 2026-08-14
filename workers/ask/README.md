# The ask box

Three lanes behind one box on the docket page, in the order they are reached.

| Lane | Where it runs | Answers from | Speed | Costs |
|---|---|---|---|---|
| **the engine** | the reader's browser | the record shipped inside the page | the same frame | nothing |
| **the answerer** | this worker, one model call | the whole record, in one prompt | about two seconds | about two cents, capped monthly |
| **the archive** | this worker, via a fired routine | the whole repository | minutes | a slot from the daily routine cap |

**No retrieval anywhere in this.** Not vectors, not grep. The published record
is about 21,000 tokens against a 200,000 token context, so the answerer is
handed the whole thing on every question. Retrieval exists to work around a
corpus that will not fit, and this one fits. Skipping it deletes the single
largest source of wrong answers in a retrieval chatbot, which is retrieving the
wrong passage, rather than leaving it to be tuned.

The archive lane is the one place retrieval is genuinely needed, because the
repository is about 3.5 million tokens. It is a Claude Code session with a
shell, which is to say an agent that greps. That is the right tool at that
size and the wrong tool at this one.

**The engine is the box.** It needs no worker, no key and no network, and it
answers almost everything, because almost every question about a docket is a
filter, a field read, a sort or a count rather than an act of reasoning. Who
decides the STAK lease is a field. What can I comment on is a filter. How many
does DNR have is a count. Answering those in the page is not a cheaper
approximation of a model answer, it is a better one, because nothing is
generated so nothing can be invented, and it is rebuilt from the ledger on
every build so it is exactly current.

Its code is `scripts/ask_answers.py`, which builds the payload, and `ASK_JS`
in `scripts/site_build.py`, which resolves a question against it. Its tests
are `scripts/ask_answers.py --self-test` and `tests/ask_engine.mjs`.

**This worker is the remainder.** Two buttons under a no-match, for the
open-ended question the published record has no field for. Both are optional
and the box works without either. Until `ASK_ENDPOINT` is set, neither button
renders at all, so a half-finished deploy shows the docket exactly as it looks
today rather than a broken form.

Neither fires on its own. The no-match panel appears while a reader is still
typing, so auto-firing would spend on every typo, and both buttons send the
reader's words off the page. The line above them says so before the press.

```
a question the engine cannot answer
   |
   v
POST /answer              the whole record in one prompt, answer returned
   |                      Turnstile gates it, ASK_MONTHLY_CAP bounds it, and
   |                      every sentence passes checks.js before it is
   |                      returned. Over the cap, this steps aside and the
   |                      reader is told, rather than being shown an error.
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
`ANTHROPIC_API_KEY`, a Console key, at about two cents a question: roughly
21,000 input tokens of record plus a short answer, on a dated Haiku 4.5
snapshot. Three things keep the month bounded, in the order they apply:

1. The engine answers most questions in the page for nothing, so this lane only
   ever sees the remainder.
2. An identical question is served from KV, keyed by the question and the pack
   date, so a repeat costs nothing and a new pack retires yesterday's answers.
3. `ASK_MONTHLY_CAP` counts calls that reached the model. Over it, the lane
   steps aside and the box falls back to the engine and the archive button,
   with the reader told why. The default is 500, so the worst case is roughly
   twelve dollars in a month where every call is used. Set it to 0 to switch
   the lane off without a deploy.

**Prompt caching is deliberately off.** A cached read is about a tenth of base
input, which looks free, but a cache write is 1.25x to 2x it, so caching only
pays once a second question arrives before the cache expires. At this box's
traffic most requests would pay a write and never see a read, and the bill
would go up. The rules and the record already go as two separate system blocks,
so turning it on later is one `cache_control` marker and nothing else.

This reverses the call made on August 9th, 2026, when the paid Messages API
lane was removed because free was a requirement. What makes it safe now and did
not then is the ceiling: the bill has a maximum the operator sets, not a
maximum the internet sets.

What it costs instead is time. A fired routine starts a whole Claude Code
session, so an answer takes minutes, and each one spends a slot from the
account's daily run cap that the daily carousel also draws on. That trade is
the reason the page calls this searching the archive and says how long it
takes.

A paid Messages API lane used to sit in front of this one. It was removed on
2026-08-09, because free was a hard requirement and it could never be turned
on, and because the in-page engine that shipped the same day answers what it
was actually for. `checks.js` survived it and now guards this lane.

## Why there is no vector database here

The record is about 29,000 tokens. Retrieval, embeddings, reranking and a
vector index exist to choose what to show a model that cannot see everything.
Anything reading this record can see all of it, so that machinery would add
latency, cost, and a class of failure the corpus size otherwise deletes: a
retriever that fetches the wrong passage answers confidently from the wrong
source, and no reranker recovers that.

The published guidance for 2026 puts the crossover at roughly 500,000 tokens.
This record is about six percent of that, and it would have to grow by a factor
of seventeen before retrieval started paying for itself.

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

If `TURNSTILE_SECRET` is unset the worker still runs and skips verification.
That is convenient for a first deploy and wrong to leave in place: every
request spends a routine run, and an unprotected endpoint is a daily cap
someone else can exhaust.

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
python3 ../../scripts/ask_corpus.py --self-test   # the corpus and its allow-list
```

All three run in CI on any change under `workers/ask/`, to the corpus builder,
or to the routine prompt, alongside the in-page engine's own two suites.
