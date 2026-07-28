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
| A1 | Add WebP q92 encoder to carousel-engine; future runs ship `.webp` | TODO |
| A2 | Backfill: convert all 18 runs' slides + contact sheets to WebP, drop PNGs | TODO |
| A3 | Point `site_build.py` image refs at `.webp`; keep a raster og:image for social scrapers | TODO |
| A4 | `scripts/prune_runs.py` — 30-day review-scratch retention | TODO |
| A5 | Investigate `carousel.pdf` size (7 MB x 18 = 126 MB) | TODO |
| A6 | Write history-rewrite recommendation, do NOT execute | TODO |

### Workstream B — Crawlability (the AI SEO win)
| ID | Task | Status |
|---|---|---|
| B1 | Extract `SITE_CSS` to one external cached stylesheet | TODO |
| B2 | Render a real article body on every deck page from `copy.json` | TODO |
| B3 | Inline primary-source hyperlinks in that body from `claims.json` (item 2) | TODO |
| B4 | Upgrade JSON-LD: `articleBody`, `citation[]`, `isBasedOn`, `author`, `publisher` | TODO |
| B5 | Per-deck plaintext mirror for LLM fetchers; expand `llms.txt` | TODO |
| B6 | Verify: re-measure text ratio as GPTBot, before vs after | TODO |

### Workstream C — Feeds (item 5)
| ID | Task | Status |
|---|---|---|
| C1 | RSS 2.0 + Atom for the daily deck, full content | TODO |
| C2 | Docket-changes feed (nobody else in Alaska has this) | TODO |
| C3 | JSON Feed + `<link rel=alternate>` autodiscovery on every page | TODO |
| C4 | Feed validation gate in `site_build.py` | TODO |

### Workstream D — Source archive (items 2, 3)
| ID | Task | Status |
|---|---|---|
| D1 | Mirror cited primary documents to `docs/sources/` at stable URLs | TODO |
| D2 | Per-deck source list linking original + mirror | TODO |
| D3 | Wire mirroring into the routine so it runs every day | TODO |

### Workstream E — Permanent URLs (item 6)
| ID | Task | Status |
|---|---|---|
| E1 | Topic hub pages at `/topics/<slug>/`, live year-round | TODO |
| E2 | Assign topics from ledger; add hubs to sitemap + `llms.txt` | TODO |

### Workstream F — Routine integration
| ID | Task | Status |
|---|---|---|
| F1 | Update `prompts/routine_instructions.md` so B/C/D/E happen every run | TODO |
| F2 | Update carousel-engine `SKILL.md` slide contract for WebP | TODO |
| F3 | Add run gates: fail if article body, feeds, or source mirrors are missing | TODO |

### Wrap
| ID | Task | Status |
|---|---|---|
| Z1 | Full site rebuild, lint gates green, verify no `docs/videos/` writes | TODO |
| Z2 | Push branch, open ready PR, merge per CLAUDE.md ship policy | TODO |

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
