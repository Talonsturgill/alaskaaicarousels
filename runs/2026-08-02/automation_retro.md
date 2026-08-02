# AUTOMATION RETRO, run 2026-08-02 (carousel No.23, score 8.37 vs 7.7, 0 hard fails)

Phase 12, written after the merge and before the Gmail draft. Every deviation
below carries its evidence. Upgrades are listed at the end with verification.

## 0. TREND CHECK, and what this phase did about it

`python scripts/trend_check.py --window 10` names the top repeat offender:

    weakest 8/10  mean 6.25  last 6.0   Artwork craft & genuine detail
                                        worked 2026-07-31 (2 runs ago)

**DECISION: DEFERRED THIS RUN, DELIBERATELY, AND HERE IS WHY.** Two reactive
fact-integrity defects outrank it, and one of them is a gate-shaped hole rather
than a craft preference: a FALSE NUMBER REACHED A RENDER AND EVERY MACHINE GATE
PASSED IT. The phase's own rule is reactive-first, and a deck that is beautiful
and wrong is worse than a deck that is plain and right.

The deferral is also an honest read of the last two attempts. Artwork craft has
been the target of two upgrades (2026-07-30 and 2026-07-31) and it has not
moved. This run's own evidence says why: the declared TOOTH density falloff RAN
IN CODE and was invisible in pixels, reported independently by multiple pixel
critics and the scorer. The failure is not that the machine lacks a helper. It
is that a mechanism parameterised by POSITION (a gradient laid over a texture
that is otherwise identical everywhere) is not visible as non-uniformity to a
reader, at any size. A third helper aimed at the same idea would be the third
upgrade to miss.

WHAT WOULD HAVE TO BE TRUE TO TACKLE IT NEXT TIME (concrete, so this cannot
become a standing excuse):
1. A technique whose detail is parameterised by the DATA UNDER IT rather than by
   position, so the non-uniformity is structural. The candidate is now parked
   with parameters and a source: slope-and-aspect hachure shading, in this run's
   `knowledge/FIELD_NOTES.md` Phase 12 park block.
2. That candidate written up as a TECHNIQUE_LIBRARY entry with OUR parameters
   and rendered on ONE trial slide, judged at 432px BEFORE nine siblings are
   built. This is exactly the scorer's own one_sentence_fix this run, and it is
   a Phase 7 process change, not a script, which is why Phase 12 is not the
   phase that should ship it.
3. A run whose reactive slot is empty. This run's was not.

Recommendation carried to the email: the scorer's one-sentence fix (build ONE
proof slide, judge its 432px thumb, and kill any declared craft mechanism that
does not read there) belongs in Phase 7 of the spec. Phase 12 did not write it
this run because it is a doctrine change to the art-build loop, not a bounded
machine change, and the maintainer should see it named rather than slipped in.

## 1. DEVIATIONS, phase by phase, with evidence

### 1.1 A FACTUAL ERROR REACHED A RENDER AND EVERY MACHINE GATE PASSED IT (Phase 7 to 8)

EVIDENCE: `storyboard.md` PIXEL REVIEW ROUND 1, first hard fail. Slide 04
printed `FIVE STATE POSTINGS, 22 TO 31 JUL`, counting the 22 July Eielson
virtual industry day (C22, eielson.af.mil) as a state posting. It contradicted
slide 09 of the same deck, which shows four dated state postings. `qa.py`
returned PASS 0 fails 0 warns; `copy_sync_check` PASS on 99 strings;
`claims_check` PASS on 27 claims. A pixel critic caught it by READING.

The class, stated generally: any on-slide string that AGGREGATES verified claims
into a NEW number (a count, a span, a total, a ratio) is itself a fresh factual
assertion that no gate re-derives. claims_check proves each claim has a source.
copy_sync_check proves copy.json matches the render. Nothing checked the
arithmetic sitting on top of them. The run KNEW this failure mode: the
fact-checker killed an "eight days" span the same run for the same class of
error, and the FIELD_NOTES entry for this run names it in so many words.

**AND IT HAPPENED TWICE. THE SECOND ONE SHIPPED.** Phase 12 built the gate,
declared this deck's 18 aggregate assertions against claims.json, and the gate
failed a string nobody had flagged:

    S7 'TWO DAYS EARLIER' [duration]: prints 2 days but 2026-07-30 to
       2026-07-31 re-derives to 1 days

Slide 07's kicker and its dossier takeaway ("A second Alaska notice, two days
earlier") compare the DMV RFI (published 30 July, C11) with the transcription
RFP (published 31 July, C02). That is ONE day. Both dates are printed on slide
07 itself. No reading rescues it: the deadlines are 20 and 24 August (four days
apart, which the caption states correctly), and today is 2 August (three days
after 30 July). This is a live error in the SHIPPED and MERGED deck, found by
the new gate, and it is disclosed here rather than quietly patched, because
runs/ is not to be rewritten. It belongs in the Gmail draft as a correction
note.

### 1.2 A GATE HAS BEEN HALF-BLIND SINCE IT WAS WRITTEN (Phase 6)

EVIDENCE: the caption critic found it, the scorer confirmed it independently,
and `ledger/captions.json`'s 2026-08-02 entry records it as a demerit:
`scripts/caption_check.py` carried a hardcoded `AI_TELLS` list and NEVER read
`config/brand.yaml`. brand.yaml's `banned_phrases` array holds 27 phrases; 4 of
them ("leverage", "disrupt", "unlock", "here's where the frame breaks") were
absent from the script's list, written down as banned and enforced by nothing.
Two config surfaces disagreed and the gate was silent about it.

This run's caption opens on "Leverage", legitimately, inside a verbatim
quotation of the governor's order (C13), and the scorer ruled it clean on the
merits. So the fix had to tighten the gate WITHOUT failing a correct caption.

### 1.3 A DECLARED CRAFT MECHANISM RAN IN CODE AND WAS INVISIBLE IN PIXELS (Phase 7)

EVIDENCE: `score_report.json` artwork craft 6/10, "THE DECLARED TARGET AND IT
DID NOT MOVE ... the TOOTH falloff is not legible anywhere"; PIXEL REVIEW
ACCEPTED-AND-NOT-FIXED, "two critics independently said the mechanism may be
running but the composition gives it nowhere to show". Related, from the same
section: the planned akthree GPU beat was NEVER BUILT, every slide is Canvas 2D,
and no dossier argued flat as a choice, so the deck claimed a rung on the
rendered ladder and skipped it silently until the build reconciliation disclosed
it. Both were disclosed to the scorer rather than hidden, which is the system
working; neither was caught by a machine, which is the system's limit.

Handled under section 0 as the deferred trend item, with the conditions for
picking it up.

### 1.4 ENVIRONMENT BREAKAGE, recorded (Phase 2)

EVIDENCE: `scout_log.txt`, plus this phase's own retries.
- ALL SIX SCOUTS hit the account's 200-call WebSearch ceiling mid-hunt. The
  2026-08-01 scan_log records the same ceiling stopping the frontier scan dead.
  The ceiling had RESET by the time Phase 12 ran today (5 searches completed),
  so it is a per-window budget being exhausted by the research phase, not an
  account-level block. The research phase is the largest consumer and it is
  first, so everything downstream inherits an empty budget.
- Reddit is unreachable to WebSearch entirely.
- alaskabeacon.com, rca.alaska.gov, SAM.gov, openai.com and murkowski.senate.gov
  all refuse automated fetches. SAM.GOV MATTERS MOST: it held the Eielson lease
  text, and its unavailability narrowed a load-bearing claim to what the Air
  Force press release says, which is why slide 05 has to print "THE LEASE
  DOCUMENT ON SAM.GOV WAS NOT READ".
Recommendation, not built this run: a fetch-failure ledger that records which
hosts refuse automation and how recently, so a scout stops spending calls on a
host that has refused five runs running.

### 1.5 THE SITE-FRESHNESS GATE GOES STALE ON ITS OWN, WITHIN HOURS (Phase 11)

EVIDENCE: `gate_status.py --run-dir out/2026-08-02` now reports
`[FAIL] site_fresh` post-merge. The single differing page is `docs/index.html`
and the single differing line is the home stat counter:

    < <div class="stat"><div class="n" data-count="32">32</div>...VIDEOS PUBLISHED
    > <div class="stat"><div class="n" data-count="31">31</div>...VIDEOS PUBLISHED

`docs/videos/videos.json` is external data owned by `publish_feed.py` in the
alaska-ai-weekly repo and appended to DAILY, and this repo's CLAUDE.md hard
guard forbids touching it. So the home page's derived count is correct at build
time and wrong a few hours later, through no fault of this repo, and a ship gate
that reads FAIL for a legitimate reason teaches the next run to ignore it.
NOT FIXED THIS RUN, on purpose: every available fix either changes what a gate
compares (a loosening, which is the maintainer's call, not Phase 12's) or
requires touching docs/ by hand (forbidden). Recommended to the maintainer:
either build the counter from a snapshot committed with the run, or have
site_fresh_check exclude counters derived from externally-owned data and say so
in its output.

## 2. WHAT THE MACHINE DID RIGHT, so it is not lost

- The pixel review caught the factual error that all three text gates missed,
  and the flow critic's one structural cut fixed three findings at once. The
  human-shaped layers of the pipeline are earning their cost.
- The build reconciliation disclosed the unbuilt akthree beat rather than
  letting it pass as delivered. Honest reporting held under pressure.
- The palette claim was made falsifiable BEFORE the build and then passed,
  breaking a two-deck losing streak. That is the shape every craft claim should
  take, and it is the model for the deferred artwork work.

## 3. UPGRADES SHIPPED THIS RUN (2 of a possible 3, both reactive)

### UPGRADE 1 (fix): `scripts/aggregate_check.py`, a new ship gate that RE-DERIVES every aggregate number printed on a slide

Detects four aggregate shapes in the rendered text (count, duration, span,
ratio), requires each one to be DECLARED in `out/<date>/aggregates.json` with
the claim ids it comes from, and re-derives the arithmetic. Also enforces two
coherence rules that need no semantics:
- SUBJECT/SOURCE: a count whose printed subject says STATE may not include a
  federally-sourced claim (decidable from `source_url`), and vice versa.
- COUPLING: when a count and a span are printed in the same string, the span's
  endpoints must be members of the count.
Wired into `gate_status.py` as the `aggregate` row and into Phase 8 of the spec
as step 6. Declarations tighten; there is one disclosed escape hatch
(`kind: "design"`, for artwork constants like `22 PX = 1 DAY`) and it is
reported under NOT RE-DERIVED so it can be audited.

VERIFICATION (all commands run from the repo root):
1. Detection on this run's real render: 18 aggregate assertions found across 10
   slides, no false positives on slide counters, on the printed scale legend, or
   on line-break concatenations.
2. `out/2026-08-02/aggregates.json` written as the reference declaration set (18
   entries). Gate result on the SHIPPED render: exactly one FAIL, the live
   `TWO DAYS EARLIER` error of section 1.1. Everything else re-derives.
3. DEFECT RECONSTRUCTION, path A (the string as first rendered, `FIVE STATE
   POSTINGS, 22 TO 31 JUL`, declared with the honest four state postings):
   FAILS twice, on the count (prints 5, declares 4 members) and on the coupling
   (the span's 22 JUL endpoint C22 is not one of the counted members).
4. DEFECT RECONSTRUCTION, path B (same string, declared with five members
   including C22, which is how an incurious run would have written it): FAILS on
   subject/source coherence, naming C22's eielson.af.mil source against a
   printed subject that says STATE. Both ways of declaring the defect fail.
5. CLASS TEST (the "eight days" span the fact-checker killed this run,
   reconstructed onto slide 02): FAILS, "prints 8 days but 2026-07-31 to
   2026-08-24 re-derives to 24 days".
6. CORRECTED ARTIFACT: the same render with slide 07 reading `ONE DAY EARLIER`
   and its declaration corrected: PASS, 0 fails, 18 of 18 declared.
7. MISSING-DECLARATION behaviour: with 18 detections and no aggregates.json, the
   gate FAILS rather than passing blind (the caption_check --ledger precedent).
8. Engine untouched, and proven so: `render.py` on `out/2026-08-02/slides`
   10/10 OK, 0 errors, 0 overflow warnings; `qa.py` PASS 0 fails 0 warns;
   `render.py` on `examples/demo-deck` 4/4 OK; `qa.py` on the demo deck WARN
   with 0 fails, its known baseline.

### UPGRADE 2 (fix): `scripts/caption_check.py` now reads `config/brand.yaml`

brand.yaml's 27 `banned_phrases` are loaded (with a 4-line reader, no new
dependency) and merged with the hardcoded AI_TELLS. A brand.yaml phrase inside a
straight-quoted verbatim passage is a WARN naming it; anywhere else it FAILS.
The exemption is deliberately narrow: it does NOT apply to any phrase already in
AI_TELLS, so nothing that failed before this change passes after it, and
unbalanced quotes mean no exemption at all. An unreadable brand.yaml is a FAIL,
not a silent pass.

VERIFICATION:
1. THIS RUN'S ACTUAL CAPTION, against the captions ledger as it stood BEFORE
   this run's entry: PASS, 849 chars, hook 102, with the warn
   "banned phrase 'leverage' appears only inside a straight-quoted verbatim
   passage". The correct caption still passes.
2. Same caption with the quotation marks stripped: FAILS on 'leverage'.
3. Same caption with "disrupt" inserted in ordinary prose: FAILS on 'disrupt'
   while still warning on the quoted 'leverage'.
4. An existing AI_TELL ("delve", "tapestry") placed INSIDE the quotation: still
   FAILS both. No weakening.
5. Unbalanced quotes: no exemption, 'leverage' FAILS.
6. `--brand /nonexistent/brand.yaml`: reports the read failure and FAILS.
7. brand_phrases_loaded: 27 is recorded in caption_report.json, so a future run
   can see that the check actually looked.

### NOT DONE, and why

- Artwork craft, the trend offender: deferred, section 0, with conditions.
- The site_fresh staleness of section 1.5: recommendation only. Every fix is
  either a gate loosening or a hand edit to docs/.
- The scout WebSearch ceiling: recommendation only (a fetch-failure ledger).
  Genuinely useful, not bounded enough to build in the same run as a new gate.
- Nothing from the frontier scan. Both slots went to reactive fixes, which is
  the phase's own rule, and two candidates are parked instead (FIELD_NOTES,
  2026-08-02 Phase 12 park block): slope-and-aspect hachure shading, and the
  human-recognisable-object thumbnail finding.

## Phase 13 deviation, recorded

`gmail_draft.py` emits `"to": "me"`, the account-relative form the routine
requires, and the Gmail connector REJECTED it twice, first with "Invalid email
address. Please provide a raw email address" and then, with the recipient
omitted entirely, with "At least one recipient (To, Cc, or Bcc) must be
specified." The draft was created addressed to `docket@alaskaaihq.com`, which
CLAUDE.md and the routine both document as the mailbox this connector
authenticates as, so it resolves to the same inbox rather than substituting a
different one. Nothing was sent; this routine drafts only.

The body is the script's output verbatim, generated with `--preview-mode remote`
rather than the default grid. At the default the html_body is 531 KB, of which
515 KB is ten inline base64 previews, which is more than one create_draft call
can carry. The remote mode exists for exactly this and produces a 16 KB body
with the contact sheet sourced from its raw URL on main, all ten per-slide links
and the PDF link intact.

WORTH A FUTURE UPGRADE, not taken this run because the reactive slots were
spent: `gmail_draft.py` could detect the payload size and pick the preview mode
itself, and the `to` field could be made configurable so the connector's
requirement and the routine's account-relative default stop disagreeing.
