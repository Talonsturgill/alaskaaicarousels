# PLAN — 2026-11-17 — Carousel No.117

Woke 2026-11-18 06:07Z (2026-11-17 21:07 AKST). run_guard: 2026-11-17 CLEAR (UTC date 2026-11-18 also CLEAR; Anchorage date taken per Phase 0.5). No prompts/NEXT_RUN.md.

EFFORT: `$CLAUDE_EFFORT` = medium. The repo settings carry `effortLevel: high`, so that setting did NOT take in this session. Noted here and in the Gmail editor notes.

SOCIAL PREFLIGHT: READY. Upload-Post profile alaska_ai present; Facebook Page 2003130316607965 and LinkedIn urn:li:organization:117084989 listed; both pins select the bound brand Page; TikTok PUBLIC_TO_EVERYONE available; social state branch initialized and read back.

## Top 5 instincts (confidence >= 0.7), injected into every subagent
1. Grain as a small repeating tile (AK.grainTile), never a full-frame feTurbulence rect.
2. A machine_qa PASS is not composition approval; critics judge composition at full and thumb size.
3. Before rendering, check long copy line counts against fixed-position labels, bars and plates.
4. A generated gate block pasted into a run record goes stale the moment another round runs; re-sync at the last render.
5. A constraint you cannot point at is one you invented: there is no context or token budget.

## Variety constraints (from ledger/artwork.json)
- Forbidden hero structures (last 4): instrument niche bodegon (No.113); lidar occlusion ledger (No.114); field kit one object per frame + measuring board (No.115); raking-light DEM relief survey with route (No.116).
- Forbidden atmospheres (last 3): sodium lot in ice fog; North Pacific overcast daylight; low November raking light on blue relief at dusk.
- Forbidden continuity devices (last 2): palette arc of one working day, edge-tease cable/board; gold route head, open benchmark ring, edge-tease route.
- Forbidden hook archetypes (last 3): the absence counted; the object's question; the order reversed.
- Forbidden palette families (last 3): sodium fog and returns; overcast wet steel + rain-gear orange; navy relief and ice blue.
- Forbidden type pairings (last 2): Fraunces + Manrope + Mono; Unbounded + Manrope + Mono.
- Also from FIELD_NOTES: sodium-lot ice fog used twice in a week; no winter-lot sodium again.

## Variance dials
design_variance 4, visual_density 3, type_temperature 2 (cooler grotesk/serif mix away from the last two warm-serif and wide-display decks). Chosen to move off No.116's dense relief survey (density was high) toward fewer, bigger modelled objects.

## Seasonal Alaska context (mid November)
- Post-election: November 3rd general; ranked-choice tabulation about 15 days after (around November 18th); certification late November.
- Legislature out of session; prefiling of bills begins in January; interim committee hearings only.
- Freeze-up, short days (Anchorage about 7 hours of light), Railbelt winter gas and power peak, CINGSA storage drawdown under an injection restriction.
- NPFMC December meeting ahead (early December); Board of Fisheries cycle; observer/EM plans.
- RCA dockets on large-load tariffs; AIDEA board; university regents met November.
- Dark-season aviation, Iditarod planning, Arctic military exercises (winter), PFD paid in October.

## Trend check (python scripts/trend_check.py --window 10)
```
REPEAT OFFENDERS
  weakest  8/10  mean 7.1    last 7.0    Artwork craft and genuine detail        worked 2026-11-11 (4 run(s) ago)  <-- STALE
  weakest  1/10  mean 7.45   last 7.5    Variety vs ledger                       worked 2026-11-01  <-- STALE
  weakest  1/10  mean 7.8    last 8.0    Insight density and factual weight      worked 2026-09-06  <-- STALE
HARD FAILS: none in window
DEFECT CLASSES THAT KEEP SHIPPING
   4 run(s)  warns:contact shadow      3 run(s) warns:busy art under text   3 run(s) warns:axis census
   2 run(s)  warns:ragged display line 2 run(s) warns:wrap drift            2 run(s) warns:tiny-text
SCORE: 11-08 8.45  11-09 8.51  11-10 8.73  11-11 8.57  11-12 8.36  11-13 8.35  11-14 8.23  11-15 8.59
```

## The ONE standing weakness this run attacks
ARTWORK CRAFT (weakest 8 of 10). How: (1) fewer, larger, better-modelled objects, the largest object on every frame named and modelled in the CRAFT PLAN before code; (2) build the masterful depth frame FIRST and copy its lighting discipline (lit ground under every contact, cast declared from contact_probe) to the rest; (3) no flat bar boards, every quantity instrument gets material identity; (4) render in batches of three; (5) re-run pixel critics on any craft-cycle frame before re-scoring.
