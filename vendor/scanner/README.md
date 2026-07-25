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
| commit | `c60a5e3b851ec92bc312c6cc28fa969975918f8d` (branch `main`) |
| landed by | PR #10, "make the live feed dense, and fix the two bugs that would have hidden it" |
| sha256 | `7c7b548693b1c14d0fa28f99823476b2132b7b03aaa9417c44b08cf73fb192bf` |
| bytes | 29323 |

## scan.html, four wiring constants and nothing else

**This file is NOT a specification and must never be copied over the live
page.** It is a reference implementation of the same flow that has drifted in
both directions from the page we actually serve. Our live page is ahead of it
in at least two ways it would regress: it has no give-up state on a long run,
and it repaints its feed by content signature rather than freezing after a
handful of notes.

It is vendored for exactly four values that have no better machine readable
home in that repo, and the check reads nothing else from it.

- the Supabase function base URL
- the publishable key
- the Cloudflare Turnstile sitekey
- the `/scan-*` endpoint names

| field | value |
| --- | --- |
| repo | `Talonsturgill/alaska-ai-scanner` |
| path | `web/scan.html` |
| commit | `c60a5e3b851ec92bc312c6cc28fa969975918f8d` (branch `main`) |
| sha256 | `2e4aa9d3c85003113184218700db3b0fc3cf98ae1f6582b717fe7552888cb579` |
| bytes | 35279 |

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
- that the live page still counts by `kind` rather than by `phase`
- the function base URL, the publishable key, the Turnstile sitekey and the
  endpoint names, from `scan.html`

Deliberately NOT compared, ever:

- markup, class names, fonts, colors, spacing, copy, animation
- the artwork, the quips, the section order

The check is a contract check, not a diff. Two pages that look nothing alike
pass it. Two pages that agree on every pixel but disagree on a note kind fail
it.

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
