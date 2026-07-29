# WORKLOG: be the cited source (machine-readable authority) 2026-07-29

Goal: when anyone asks an AI about AI infrastructure in Alaska, this site is
the source it quotes, at the level of a SPECIFIC DECISION, not just "a site
about Alaska AI".

## Audit: what already exists (do NOT rebuild)

llms.txt, llms-full.txt (whole corpus, one fetch), feed.xml/atom.xml/feed.json/
docket/feed.xml (full content), docs/docket.json (open JSON), robots.txt that
welcomes AI crawlers, sitemap.xml WITH lastmod, per-article Markdown twins,
NewsArticle + Organization + basic Dataset + CollectionPage + BreadcrumbList
JSON-LD, /sources/ archive of 109 verified documents. This is a strong base;
roughly 60 percent of the job was already done.

## The gaps this task closes

| # | Gap | Why it decides citability |
|---|-----|---------------------------|
| A | Docket is ONE page with #anchors; no URL per decision | An LLM citing a specific decision has nothing to link. 9 decisions, 0 citable URLs. Anchors are not separately indexed, have no own title, lastmod or structured data. |
| B | docket.json has no version, schema docs or license | Nothing states the contract or that reuse is allowed, so nobody builds on it and no catalog indexes it. |
| C | Dataset JSON-LD lacks license/temporalCoverage/spatialCoverage/variableMeasured/keywords | Exactly the fields Google Dataset Search indexes. Currently invisible there. |
| D | No FAQ/answer layer with FAQPage markup | Answer engines quote direct sourced answers to real questions. |
| E | No decider hub pages | Alaska DNR decides 4 of 9 items and has no page. Hubs are how the topic graph gets owned. |
| F | No citation block or license statement on data surfaces | Citation friction, and no explicit reuse grant. |

## Build order (each slice ships verified)

1. **A. Per-decision pages** `/docket/<id>/` built from the SAME resolve()
   components as the docket page (no second date logic, rule 5 from the
   date-roles work). Full timeline, sources, history, access path, citation
   block. Canonical, in sitemap with real lastmod (item.last_updated), in
   llms.txt. Docket page entries link to them.
2. **B. Dataset contract**: docket.json gains version, license, schema
   documentation, generated-by, canonical URL. Add `/data/` page that
   documents every field in prose a human and a machine can both read.
3. **C. Rich Dataset + DataCatalog JSON-LD** on /docket/ and /data/, plus
   per-decision entity JSON-LD on the new pages.
4. **D. FAQ layer** at /questions/ (FAQPage), answers derived ONLY from
   verified docket/claims data, every answer carrying its source link.
5. **E. Decider hubs** `/deciders/<slug>/`.
6. **F. Citation blocks** + explicit CC license statement on data surfaces.

## Hard constraints (house rules that bind this)

- No em/en dashes, no emoji, straight quotes, NO PROSE COLONS (the build's
  colon gate will fail the ship otherwise).
- Every new page goes through site_build's punctuation + colon gates.
- Dates on new pages MUST come from docket_build.resolve(), never recomputed.
  Extend scripts/docket_dates_check.py to cover the new per-decision pages, or
  the guard has a hole the moment this ships.
- docs/videos/* is a HARD GUARD. Do not touch.
- No fabrication: an answer or field with no verified source does not ship.
  Degrade honestly, per the house standard.

## Status (A/B/C/G shipped in tranche 1; D/E/F next)

| # | Slice | Status |
|---|-------|--------|
| A | per-decision pages | DONE |
| B | dataset contract + /data/ | DONE |
| C | rich Dataset/entity JSON-LD | DONE |
| D | /questions/ FAQ layer | TODO |
| E | decider hubs | TODO |
| F | citation + license | TODO |
| G | extend docket_dates_check to new pages | DONE |
