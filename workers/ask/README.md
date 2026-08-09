# The ask box

Two lanes behind one box on the docket page.

| Lane | Route | Answers from | Speed | Billed to |
|---|---|---|---|---|
| **fast** | `POST /` | `ask-corpus.json`, the published record | about a second | a paid Console key |
| **deep** | `POST /deep` then poll `GET /result` | the whole repository, via a fired routine | minutes | the claude.ai subscription |

The fast lane is the default and the box's main path. The deep lane is a link
under it, for a question the published record cannot answer.

**The two lanes are independent.** Deploy either without the other. With no
`ANTHROPIC_API_KEY` the fast lane returns 503 and the deep lane still works,
which is the configuration to use if you want this to cost nothing beyond the
subscription you already pay for.

Answers from both lanes go through the same checks before they are displayed.
A slower answer is not a more trusted one.

```
docs/ask-corpus.json      the whole public record, built by scripts/ask_corpus.py
   |                      and published by GitHub Pages like every other page
   v
worker.js                 holds the key, calls the Messages API with the record
   |                      in a cached prompt prefix, streams the answer back
   v
checks.js + stream.js     every sentence is verified before it is displayed
```

## Why there is no vector database here

The record is about 29,000 tokens. Retrieval, embeddings, reranking and a
vector index exist to choose what to show a model that cannot see everything.
This model sees everything, every time, so that machinery would add latency,
cost, and a class of failure the corpus size otherwise deletes: a retriever
that fetches the wrong passage answers confidently from the wrong source, and
no reranker recovers that.

The published guidance for 2026 puts the crossover at roughly 500,000 tokens.
This record is about six percent of that, and it would have to grow by a factor
of seventeen before retrieval started paying for itself.

## Getting an API key

The key is for the **Claude Developer Platform**, which is billed separately
from a claude.ai Pro or Max subscription. A subscription does not include API
credit and its login will not authenticate this endpoint.

1. Go to <https://platform.claude.com> and sign in. Use the same email as the
   claude.ai account if you want them under one identity, but it is a separate
   account with separate billing.
2. **Billing** in the left sidebar, then add a payment method and buy credit.
   Start with the smallest amount; see the cost note below for why that lasts.
3. **API keys** in the left sidebar, then **Create key**. Name it
   `alaskaai-ask` so it can be revoked without touching anything else.
4. Copy the key. It starts with `sk-ant-api03-` and is shown once.

If the key ever leaks, revoke it on that same page. Nothing else in this repo
uses it, so revoking it stops the ask box and breaks nothing else.

## The deep lane needs no key at all

The routine trigger's token is a `sk-ant-oat01-` bearer generated in one click
at [claude.ai/code/routines](https://claude.ai/code/routines), and it draws on
the claude.ai subscription rather than on Console credit. No card, no separate
account. What it costs instead is time (a fired routine starts a whole Claude
Code session, so minutes) and a slot from the account's daily routine run cap,
which is shared with the daily carousel.

Setting it up is `prompts/ASK_ROUTINE.md`, which carries the prompt to paste
and, more importantly, the environment to put it in. Read the warning at the
top of that file before you create the routine: it is the only thing in this
project that runs on text a stranger typed, and the default is that every
connector on your account is attached to it.

## Deploy

```bash
npm install -g wrangler          # once
wrangler login                   # opens a browser, same Cloudflare account as Turnstile

cd workers/ask
wrangler kv namespace create ASK_KV       # paste the printed id into wrangler.toml

wrangler secret put TURNSTILE_SECRET      # from the Turnstile widget's settings

# deep lane
wrangler secret put ROUTINE_TOKEN         # sk-ant-oat01-... from the API trigger
wrangler secret put ROUTINE_TRIGGER_ID    # trig_... from the same modal
wrangler secret put DELIVER_SECRET        # any long random string; the routine gets it too

# fast lane, optional
wrangler secret put ANTHROPIC_API_KEY     # sk-ant-api03-... from platform.claude.com

wrangler deploy
```

`wrangler deploy` prints the URL, which looks like
`https://alaskaai-ask.<your-subdomain>.workers.dev`. Put that URL into
`ASK_ENDPOINT` in `scripts/site_build.py` and rebuild the site. Until it is
set, the ask box does not render at all, so a half-finished deploy shows the
docket exactly as it looks today rather than a broken form.

No DNS change is needed. The site stays on GitHub Pages and calls the
workers.dev URL cross-origin, the same shape as the existing scanner calls.

## Turnstile

The secret belongs to the same widget whose sitekey is already in
`site_build.py` (`0x4AAAAAAD7e1lYKOUSxa5sV`). Find it at
<https://dash.cloudflare.com> under **Turnstile**, the widget's **Settings**,
then **Secret key**.

If `TURNSTILE_SECRET` is unset the worker still runs and skips verification.
That is convenient for a first deploy and wrong to leave in place: every
question costs money and an unprotected endpoint is a bill someone else can
run up.

## Watching it

```bash
wrangler tail                    # live log
```

Two things are logged. `withheld` records every answer a check refused, with
the question, the sentence, and which control caught it; those are worth
reading because they are either the guard working or the guard misfiring, and
you cannot tell which without looking. `upstream error` records API failures.

Nothing else is stored. Questions are not persisted anywhere, so the log is
the only record and it rolls off.

## Cost

Roughly 3 cents a question when the prompt cache is warm, and about 20 cents
for the first question after a gap, since that one pays to write the cache. The
answer cache means a repeated question costs nothing at all.

The corpus changes daily when the gas watch collector runs, which retires both
caches. That is deliberate: a cached answer about an open comment window is
worse than a slow one.

Bounds worth knowing: `MAX_TOKENS` caps each answer at 900 tokens, and
`MAX_QUESTION` rejects anything over 400 characters before it reaches the API.
Turnstile is what stops the volume. For a hard ceiling, add a rate-limiting
rule in the Cloudflare dashboard against the worker's route.

## Tests

```bash
node test.mjs                                     # the checks and the release gate
node test-deep.mjs                                # delivery auth and the poll state machine
python3 ../../scripts/ask_corpus.py --self-test   # the corpus and its allow-list
```

All three run in CI on any change under `workers/ask/`, to the corpus builder,
or to the routine prompt.
