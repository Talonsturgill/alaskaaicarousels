# WORKLOG — Machine-Readable Overhaul (2026-07-28)

**READ THIS FILE FIRST after any context compaction.** It is the shared brain
for a long multi-context task. Update the STATUS table after every commit.

Branch: `claude/scanner-waiting-view-port-kga7cx`
Working dir: `/home/user/alaskaaicarousels`

---

## THE ASK (what the user approved, verbatim intent)

After a competitive study of ADN, Alaska's News Source, and The Alaska Story,
the user approved this scope:

| # | Item | Decision |
|---|---|---|
| 0 | Repo data bloat | FIX. User asked "dump stuff 30+ days old?" See ANSWER below. |
| 1 | Named recurring franchises | **SKIP.** User already has FB/LinkedIn automations doing this. |
| 2 | Hyperlink primary sources inline + make the carousel routine do it every run | **DO** |
| 3 | Primary-source archive (mirror cited docs at stable URLs) | **DO** ("add that if you can") |
| 4 | Win AI SEO. ChatGPT could not find or scrape the site. | **DO — top priority** |
| 5 | RSS feed | **DO** |
| 6 | Dormant-but-permanent URLs | **DO** |
| — | Tier 1 of the build plan | **DO** |
| — | Tiers 2, 3, 4 | **HOLD OFF.** No masthead, corrections archive, standards page, search, podcast, or separate daily-brief product. |

User instructions on process: plan first, execute task by task, keep a durable
shared brain across context windows, re-read it after each compaction.

---

## ANSWER TO "dump stuff 30+ days old?"

**No. Deletion is the wrong fix and would break the public site.**

Measured facts:
- `runs/` = 610 MB across 18 runs, ~34 MB/run. `.git` pack = 668 MB. Total 1.3 GB.
- Oldest run is 2026-07-08, only 20 days old. Nothing is 30+ days old yet.
- **The live site serves images straight out of `runs/`** via
  `raw.githubusercontent.com/.../main/runs/<date>/slide-NN.png`. Deleting old
  runs would blank every archive page.
- The bulk per run: 9 slide PNGs at 2160x2700, ~3.7 to 5.3 MB each (~38 MB),
  plus `carousel.pdf` at ~7 MB, plus `contact_sheet.png` at ~1 MB.
- Only ~1.2 MB/run is genuinely disposable review scratch.

**The real fix is compression, not deletion.** Benchmarked on a real slide
(`runs/2026-07-26/slide-01.png`, 5.03 MB):

| Encoding | Size | Shrink |
|---|---|---|
| PNG 2160x2700 optimize=9 | 4.74 MB | 1.1x |
| PNG 1080x1350 optimize=9 | 1.38 MB | 3.6x |
| WebP 1080x1350 lossless | 0.97 MB | 5.2x |
| **WebP 2160x2700 q92** | **0.47 MB** | **10.6x** |
| WebP 1080x1350 q90 | 0.10 MB | 51.8x |
| JPEG 1080x1350 q90 4:4:4 | 0.24 MB | 21.1x |

**Chosen: WebP q92 at full 2160x2700.** Keeps every pixel of the retina master,
10.6x smaller, ~1.2s/slide to encode. No resolution loss at all.

Retention policy (secondary, small): prune review scratch
(`contact_sheet.png`, `storyboard.md`, `scout_merge.md`, `selection.md`,
`automation_retro.md`, `gmail_payload.json`) older than 30 days. Keep forever:
slides, PDF, `claims.json`, `copy.json`, `caption.txt`, `score_report.json`,
`run_state.json`, `plan.md`.

`.git` history (668 MB) can only shrink via `git filter-repo`, which needs a
force-push to main on a live public repo. **Do NOT run it. Recommend only.**
Ship the script + writeup and let the user decide.

---

## THE AI-SEO DIAGNOSIS (why ChatGPT sees nothing)

Measured on `docs/archive/2026-07-26/index.html`:

```
total HTML         81,957 bytes
  inline <style>    39,893 bytes  (49%)
  inline <script>    6,204 bytes  ( 8%)
  VISIBLE TEXT       4,209 bytes  ( 5.1%)   <-- the whole problem
```

Root causes, in order of severity:

1. **The story is pixels, not text.** A deck page's editorial payload lives
   inside nine PNGs on a different domain. The page itself carries a headline,
   a caption, and a source list. There is no article body. An LLM crawler that
   does not OCR images sees ~1,500 bytes of actual story.
2. **49% of every page is inline CSS**, duplicated on all 26+ pages, uncached.
3. Images are 5 MB each and cross-origin on `raw.githubusercontent.com`.

What is already RIGHT and must not be broken: `robots.txt` is `Allow: /`,
alt text is rich and per-slide, `NewsArticle` + `BreadcrumbList` JSON-LD are
present, `llms.txt` exists, `docket.json` is open data.

**The fix is available today at zero research cost.** Every run already
produces the article:
- `runs/<date>/copy.json` -> `slides[]` with `headline`, `body`, `labels`,
  `claim_ids`
- `runs/<date>/claims.json` -> `claims[]` with `id`, `claim`, `source_url`,
  `source_outlet`, `source_is_primary`, `date_of_source`, `verbatim`

Join them on `claim_ids` and you get a real, indexable, hyperlinked article
body. That single change serves items 2, 3, and 4 simultaneously.

---

## KEY FILES

| Path | Role |
|---|---|
| `scripts/site_build.py` | 3,286 lines. Builds all of `docs/`. `deck_page()` L1777, `SITE_CSS` L310, `page()` L1312, `sitemap()` L3151, `llms_txt()` L3170, `build()` L3209 |
| `scripts/docket_build.py` | 828 lines, shared library imported by site_build |
| `prompts/routine_instructions.md` | 630 lines, Phases 0-14. Phase 3 = claims, Phase 11 = ship, Phase 13 = Gmail |
| `.claude/skills/carousel-engine/` | render.py, qa.py, assemble.py, SKILL.md |
| `runs/<date>/` | shipped artifacts, served publicly |
| `docs/` | the built site, GitHub Pages -> alaskaaihq.com |

Guards that must not be violated: `docs/videos/` is a HARD GUARD (static
passthrough owned by another repo). No em/en dashes, no emojis, straight
quotes anywhere in output.

---

## STATUS

Legend: TODO / WIP / DONE / BLOCKED

### Workstream A — Payload (answers the disk question)
| ID | Task | Status |
|---|---|---|
| A1 | `scripts/ship_images.py`, adaptive q92->q96->q98->lossless against a 40 dB PSNR floor | DONE `9fc93f0` |
| A2 | Backfill: 513 MB PNG -> 57.7 MB WebP across 18 runs, 8.9x, 90/342 files escalated | DONE `9fc93f0` |
| A3 | `site_build.py` -> `.webp` for slides, per-run `og.jpg` for og:image + schema image | DONE `9fc93f0` |
| A4 | `scripts/prune_runs.py` — 30-day review-scratch retention | TODO |
| A5 | `carousel.pdf`: 90 MB total. NOT shrinkable. Chromium vector-text output whose source HTML lives in gitignored `out/`, so historical PDFs cannot be regenerated. Vector text is a house rule. LEAVE. | DONE (declined, reasoned) |
| A6 | Write history-rewrite recommendation, do NOT execute | TODO |

Result: `runs/` 610 MB -> 157 MB. Verified 198 site asset refs, 0 missing;
18/18 decks complete. User confirmed the concern was Gmail payloads, which are
17 KB/run and were never the issue.

### Workstream B — Crawlability (the AI SEO win)
| ID | Task | Status |
|---|---|---|
| B1 | `site.css` + `site.js` externalized and cached sitewide (was ~46 KB inlined per page) | DONE `f1407cc` |
| B2 | `article_html()` rebuilds the deck as prose from `copy.json` slides | DONE `f1407cc` |
| B3 | `link_claims()` inline figure links + `claims_html()` full verification record | DONE `f1407cc` |
| B4 | JSON-LD gained `articleBody`, `wordCount`, `citation[]`, `isBasedOn` | DONE `f1407cc` |
| B5 | Markdown twin per deck + `llms-full.txt` + rewritten `llms.txt` | DONE `cec787a` |
| B6 | Verify text ratio as GPTBot against the live site after deploy | TODO |

Measured on deck page 2026-07-26:
HTML 81,957 -> 59,864. Visible text 4,209 -> 11,482 (2.7x). Ratio 5.1% -> 19.2%.
Linked sources 0 -> 30, of which 16 primary. Plus a 3 KB Markdown twin.

Gotchas found and fixed, do not regress these:
- Prose colon gate kills the build on slide copy like "two newer ideas: AI".
  `house()` normalizes colons, em/en dashes, curly quotes and emoji on
  everything pulled out of a run. claims.json quotes sources verbatim, so a
  source's em dash WILL reach the page otherwise.
- A claim `value` of `2026-04-21` made the matcher link the bare year in
  "introduced on April 21, 2026", reading as if the year were the fact.
  `_anchor_candidates` now rejects ISO dates and any bare 4-digit year.

### Workstream C — Feeds (item 5)
| ID | Task | Status |
|---|---|---|
| C1 | `/feed.xml` RSS 2.0 + `/atom.xml`, full content not teasers | DONE `cec787a` |
| C2 | `/docket/feed.xml`, sorted by `last_updated`, guid carries the date so movement resurfaces | DONE `cec787a` |
| C3 | `/feed.json` JSON Feed 1.1 with per-item source list; autodiscovery on all 26 pages | DONE `cec787a` |
| C4 | `fb.validate()` parses every feed before writing; `db.fail` on bad XML/JSON or banned punctuation | DONE `cec787a` |

All in `scripts/feeds_build.py` (new module, imported by site_build like
docket_build). Verified 18/18/18/9 items, all parse clean.

### Workstream D — Source archive (items 2, 3)
| ID | Task | Status |
|---|---|---|
| D1 | `/sources/` publishes all 95 documents behind 428 claims, grouped by outlet | DONE `83144dd` |
| D2 | Per-deck verification record links every claim to its document | DONE `f1407cc` |
| D3 | Rebuilt from `claims.json` on every build, so it is automatic | DONE `f13d366` |

DELIBERATE SCOPE CALL: built an INDEX, not a content mirror. Re-hosting news
articles is a copyright exposure for a publication, and we had just removed
455 MB, so re-bloating the repo with mirrored PDFs would undo workstream A.
The index delivers the actual value (permanence, discoverability, proof of
sourcing) at zero storage cost. Flagged to the user.

### Workstream E — Permanent URLs (item 6)
| ID | Task | Status |
|---|---|---|
| E1 | 7 standing beats at `/topics/<slug>/`, render even with zero decks | DONE `83144dd` |
| E2 | Beats matched from `ledger/topics.json`; in sitemap, `llms.txt`, footer, nav | DONE `83144dd` |

### Workstream F — Routine integration
| ID | Task | Status |
|---|---|---|
| F1 | Phase 3 runs `claims_check.py` (gate); Phase 11 runs `ship_images.py` + documents the whole surface | DONE `f13d366` |
| F2 | `SKILL.md`: PNG in the review loop, WebP on the way out | DONE `f13d366` |
| F3 | `claims_check.py` gate + `fb.validate()` feed gate + pinned fact-checker schema | DONE `f13d366` |

### Wrap
| ID | Task | Status |
|---|---|---|
| Z1 | Clean rebuild, two builds byte-identical, 987 internal refs 0 broken, 0 banned punctuation, `docs/videos/` untouched | DONE |
| Z2 | Push branch, open ready PR, merge per CLAUDE.md ship policy | WIP |

## FINAL NUMBERS

| | before | after |
|---|---|---|
| `runs/` on disk | 610 MB | 155 MB |
| deck page HTML (18) | 1,475,226 B | 919,052 B |
| readable text (18) | 51,534 B | 131,883 B |
| text ratio | 3.5% | 14.3% |
| verified claims on the site | 0 | 428 |
| linked source documents | 0 | 95 |
| feeds | 0 | 4 |
| permanent beat pages | 0 | 7 |

## A6 — THE HISTORY REWRITE (recommended, NOT run)

`.git` is still ~668 MB because the PNG blobs live in history. Only
`git filter-repo --path-glob 'runs/*/slide-*.png' --invert-paths` (plus
`contact_sheet.png`, `thumbs/`) removes them, and that needs a force-push to
`main` on a live public repo with an active Pages deploy and open PRs.

NOT RUN. That is the user's call, not an agent's. If they approve:
1. Fresh mirror clone, run filter-repo there, verify `docs/` and `runs/`
   still resolve, then force-push.
2. Deck raw URLs point at `/main/`, so they follow the new head and survive.
3. Expected result: ~668 MB -> ~120 MB.
Nothing in the working tree depends on it; this is purely clone weight.

---

## DECISION LOG

- **2026-07-28** Chose WebP q92 @ 2160x2700 over downscaling. Preserves the
  retina master; 10.6x smaller is enough to solve both disk and page weight.
- **2026-07-28** Rejected deleting old runs: the public archive serves images
  directly out of `runs/`, so deletion blanks live pages.
- **2026-07-28** Will not run `git filter-repo`. Force-pushing rewritten
  history to a live public publication is the user's call, not mine.
- **2026-07-28** Skipping franchises (item 1) per user: covered by existing
  FB/LinkedIn automations.

## OPEN QUESTIONS (do not block on these)

- Item 3 "add that if you can" read as the primary-source archive (D). Stated
  as an assumption to the user; proceeding.
- "Tier 1 yes, tiers 2/3/4 hold" read as: do the machine-readable moat +
  source work, skip publication furniture and the multi-artifact fan-out.
