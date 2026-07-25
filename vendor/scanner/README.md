# vendor/scanner

Two files vendored from the backend repo, with two different jobs. Neither is
edited here and neither is ever served. They exist so
`scripts/scanner_sync_check.py` has something local to check the live page
against.

## scan_routine.md, the specification

This is the source of record. The routine literally executes it at fire time,
so it is the authority on the contract, not a description of it.

`scanner_sync_check.py` reads the phase list and the note kinds out of its
THE PROGRESS FEED section.

| field | value |
| --- | --- |
| repo | `Talonsturgill/alaska-ai-scanner` |
| path | `prompts/scan_routine.md` |
| last changed at | `c60a5e3b851ec92bc312c6cc28fa969975918f8d` (branch `main`) |
| landed by | PR #10, "make the live feed dense, and fix the two bugs that would have hidden it" |
| sha256 | `7c7b548693b1c14d0fa28f99823476b2132b7b03aaa9417c44b08cf73fb192bf` |
| bytes | 29323 |

The commit row is the commit that last CHANGED the file, not whatever main
happens to be at. The two files move independently, and pinning both to the
same tip commit would say a file changed when it did not.

## scan.html, four wiring constants and nothing else

**This file is NOT a specification and must never be copied over the live
page.** It is a reference implementation of the same flow, maintained by hand
alongside ours, and the two have drifted in both directions before.

As of this snapshot they agree on everything that governs a run. Scanner PR
#12 brought the reference in line on the poll loop (a steady 5s with no give-up
on a slow run, and a two hour net for a hung one), the counters (decided per
note, so a mixed feed does not drop its kind-less half), the null and non array
guards on `progress`, the dropped-request guard, and the modal teardown. The
feed freeze at note six was fixed upstream in PR #10 before this file was ever
vendored. None of that needs re-fixing on either side.

What still differs is small and cosmetic. Escape closes the modal here and not
there. Our reduced-motion block covers more. The finished-with-no-html message
is worded differently. And the chrome, which is the whole point, see below.

That paragraph is prose and prose goes stale, which is how this README came to
carry two false claims about the live page in the first place. Trust it as a
pointer, never as the contract. The contract is the part the check reads.

This file is vendored for exactly four values that have no better machine readable
home in that repo, and the check reads nothing else from it.

- the Supabase function base URL
- the publishable key
- the Cloudflare Turnstile sitekey
- the `/scan-*` endpoint names, taken only from real `FN + "/scan-..."` call
  sites, so a mention in a comment is not mistaken for a call

| field | value |
| --- | --- |
| repo | `Talonsturgill/alaska-ai-scanner` |
| path | `web/scan.html` |
| last changed at | `18fe7e9d045fd1cf07891d2b3552742ca8f40d91` (branch `main`) |
| landed by | PR #12, "stop giving up on a slow scan, and seven other things a run can hit" |
| sha256 | `a35a630fe317e9e11729ab45532f8440ff7f3f5333764e261a862c3ec593a6f5` |
| bytes | 40102 |

Those sha256 rows are not decoration. The check recomputes both and fails if
either file has been edited here, because a vendored snapshot nobody can trust
is worse than no snapshot.

## Why the live page is a separate implementation

The page a visitor loads at https://alaskaaihq.com/scan/ is emitted by
`scan_page()` in `scripts/site_build.py`. It wears this site's shell, Fraunces
and JBMono, the `--panel` and `--line` tokens, the gold `.cta`, the shared nav
and footer, and it has to clear this repo's build gates. The backend repo's
copy is a plain standalone dark page with its own type and its own tokens.

Making either a copy of the other forces one to carry the other's chrome, which
is how they drifted in both directions in the first place. They are meant to
look nothing alike. What they are not allowed to disagree about is the
contract, and that is the only thing checked.

## What is guarded and what is not

Guarded by `scripts/scanner_sync_check.py`:

- the ordered phase list, from `scan_routine.md`
- the note kinds, from `scan_routine.md`, including that a new kind fails until
  someone counts it or ignores it on purpose
- that the live counters report the truth. The counter block is cut out of
  `site_build.py` between its `sync:counters` markers and RUN against probe
  feeds whose right answers are known. This is behaviour, not pattern
  matching: rewrite the loop however you like and it passes, transpose two
  tiles and it fails.
- that every phase has a ring percentage, that those climb in phase order, and
  that no agent watches for a phase the routine never writes
- the function base URL, the publishable key, the Turnstile sitekey and the
  endpoint names, from `scan.html`
- that both vendored files still hash to the sha256 recorded above

Deliberately NOT compared, ever:

- markup, class names, fonts, colors, spacing, copy, animation
- the artwork, the quips, the section order

The check is a contract check, not a diff. Two pages that look nothing alike
pass it. Two pages that agree on every pixel but disagree on a note kind fail
it.

What it still cannot tell you on its own: whether this snapshot is current.
The hashes prove nobody edited these copies locally, not that the backend repo
still has them. `--fetch` asks that question directly, and needs
`SCANNER_REPO_TOKEN` or `GH_TOKEN` with read access, since that repo is
private. Without a token it says it could not look rather than passing.

## What runs it

- `.github/workflows/scanner-contract.yml`, on every pull request and every
  push to main that touches `site_build.py`, this directory, or `docs/scan/`.
  It also rebuilds the page and requires the committed `docs/scan/index.html`
  to match byte for byte, because `docs/` is committed and Pages serves it
  straight, so a correct builder with a stale build still ships the old page.
- the daily routine, at step 2a of `prompts/routine_instructions.md`, since
  every run rebuilds `docs/` and ships whatever the page currently says.
- `scripts/gate_status.py`, as the `scanner_sync` row, so the run's own GATE
  STATUS block reports it rather than a human sentence about it.

It needs `node` on PATH, because the counter block it runs is JavaScript. With
no node it exits 2 and says so. Exit 2 is a failure, not a pass: a check that
cannot see is not a check.

## Refreshing these copies

When the backend repo changes any guarded value, re-vendor and update the
tables above in the same commit as the matching `site_build.py` change.

```
git clone --depth 1 https://github.com/talonsturgill/alaska-ai-scanner /tmp/scanner
cp /tmp/scanner/prompts/scan_routine.md vendor/scanner/scan_routine.md
cp /tmp/scanner/web/scan.html            vendor/scanner/scan.html
git -C /tmp/scanner rev-parse HEAD          # the commit for the tables
shasum -a 256 vendor/scanner/*             # the sha256 for the tables
python scripts/scanner_sync_check.py
```

To ask whether a refresh is due without doing one, run the check with
`--fetch`. Against a checkout rather than GitHub, point `SCANNER_RAW_BASE` at
it, which is also how the fetch path itself is tested:

```
SCANNER_RAW_BASE="file:///tmp/scanner/" python scripts/scanner_sync_check.py --fetch
```
