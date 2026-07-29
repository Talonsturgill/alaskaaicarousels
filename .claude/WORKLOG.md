# WORKLOG: full-site review remediation (2026-07-29)

A multi-agent review of the whole site generator surfaced 21 verified
findings beyond the 13 already shipped in #143. This is the durable plan
for fixing all of them. Every fix is proven by executing the code, and
must not change what the 19 shipped runs currently publish except where
that output is the bug.

## PR plan (three themed PRs, each merges independently)

### PR-SEC: security
| id | file | fix | status |
|----|------|-----|--------|
| S1 | site_build.py:1500 | JSON-LD breakout escaped | DONE |
| S2 | gmail_draft.py:240,283 | esc() score fields | DONE |
| S3 | scanner_sync_check.py:474 | token gated to GitHub hosts | DONE |
| S4 | docs/videos/index.html | DOM XSS, CANNOT FIX HERE (HARD GUARD). Flag; fix belongs in alaska-ai-weekly publish_feed.py | DEFER+REPORT |

### PR-BUILD: page-builder correctness
| id | file | fix | status |
|----|------|-----|--------|
| B1 | site_build.py:1679 | _claim_rows: honor selected_story pointer; skip unverified* containers | TODO |
| B2 | site_build.py:1741 | date [:10] slice fabricates tokens; validate ISO or blank | TODO |
| B3 | site_build.py:1765 | title: tolerant fallback (title/deck_title) + house() | TODO |
| B4 | site_build.py:1600 | outlet: derive from URL domain when no outlet field (NOT source_title, which is a headline) | TODO |
| B5 | site_build.py:2219 | sources_page: cap of 8 disagrees with counted total; show all or count shown | TODO |
| B6 | site_build.py:1766 | hook through house() (folded into B3) | TODO |
| B7 | site_build.py:2218 | sources_page: URL truncated to 110 chars w/o ellipsis, link text 404s | TODO |

### PR-GATE: gate integrity
| id | file | fix | status |
|----|------|-----|--------|
| G1 | gate_status.py:43 | binary_ok only checks 8 magic bytes; add structural truncation check for PNG/WebP/PDF | TODO |
| G2 | gate_status.py:101 | qa_row trusts fails counter, ignores verdict + named-fail slides | TODO |
| G3 | gate_status.py:157 | copy_sync_row uses n/a on subprocess fail; should be absent()=FAIL under require | TODO |
| G4 | copy_sync_check.py:141 | empty slides list -> 0 comparisons -> PASS | TODO |
| G5 | dedupe_check.py:137 | jaccard branch unreachable; word-for-word repeat clears dedupe | TODO |
| G6 | caption_check.py:152 | missing ledger path silently disables variety check, writes PASS | TODO |
| G7 | dossier_check.py:139 | MODELED_HINTS unanchored substring ("ground" etc.) passes dead-zone defect | TODO |
| G8 | ship_images.py:111 | og.jpg repair path unreachable on already-converted run | TODO |
| G9 | prune_runs.py:47 | deletes shipped caption_report.json + machine_qa.json; off-by-one on --days | TODO |
| G10 | shrink_pdfs.py:179 | type-integrity guard vacuous for raster PDF (hypothesis; latent) | TODO |

### Frontend reviewer
Died 4x on API 500/529. Relaunched. Findings TBD -> own PR if any.

## House rules that bind these fixes
- No em/en dashes, straight quotes, honest degradation over fabrication.
- Deleting/overwriting shipped runs/ artifacts is stop-and-ask. G9 fixes
  prune so it STOPS doing that; it does not itself delete anything.
- docs/videos/* is a HARD GUARD (S4). Do not touch from this repo.
- Every fix verified by running the real code; no regression on 19 runs.

## Status: PR-SEC shipping; PR-BUILD next.
