# vendor/scanner

`scan.html` here is a verbatim copy of the Bottleneck Scanner reference page
from the backend repo. It is vendored, never edited, and never served. It
exists so `scripts/scanner_sync_check.py` has something local to compare the
live page against.

## Source

| field | value |
| --- | --- |
| repo | `Talonsturgill/alaska-ai-scanner` |
| path | `web/scan.html` |
| commit | `fbd527a3b901a5fb9700361bade9e207025ef4ce` (branch `main`) |
| landed by | PR #9, "Deepen the scan, rebuild the wait, and close the captcha" |
| merged | 2026-07-25 |
| sha256 | `4ba75a18fa6e91a39b42094b8959066f6e9e7d186c557e13dbb808490d13b388` |
| bytes | 34391 |

## Why a second copy of the same page exists

The page a visitor loads at https://alaskaaihq.com/scan/ is NOT this file. It
is emitted by `scan_page()` in `scripts/site_build.py`, a separate hand
maintained implementation of the same flow wearing this site's shell (Fraunces
and JBMono, the `--panel` and `--line` tokens, the gold `.cta`, the shared nav
and footer). The backend repo's copy is a plain dark standalone page with its
own type and its own tokens.

Two hand maintained copies of one flow is exactly how the two drifted the
first time. PR #9 rebuilt the waiting view in the backend repo and the live
page kept its old spinner for a day, because nothing machine checked the gap.

## What is shared and what is not

Shared, and guarded by `scripts/scanner_sync_check.py`:

- the Supabase function base URL
- the publishable key
- the Cloudflare Turnstile sitekey
- the phase list the progress feed writes on every note
- the endpoint names the page calls

Deliberately NOT shared, and never compared:

- markup, class names, fonts, colors, spacing, copy, animation
- the artwork, the quips, the section order

The check is a contract check, not a diff. Two pages that look nothing alike
pass it. Two pages that agree on every pixel but disagree on a sitekey fail
it.

## Refreshing this copy

When the backend repo changes any of the guarded values, re-vendor and update
the table above in the same commit as the matching `site_build.py` change.

```
git clone --depth 1 https://github.com/talonsturgill/alaska-ai-scanner /tmp/scanner
cp /tmp/scanner/web/scan.html vendor/scanner/scan.html
git -C /tmp/scanner rev-parse HEAD          # the commit for the table
shasum -a 256 vendor/scanner/scan.html      # the sha256 for the table
python scripts/scanner_sync_check.py
```
