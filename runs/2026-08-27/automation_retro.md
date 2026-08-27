# AUTOMATION RETRO, 2026-08-27, Carousel No. 42

Shipped 8.67 against an unrelaxed 8.3, after FIVE editing rounds and FOUR
scoring passes. Every machine gate was green at ship. The budget was spent on
one deck, so this retro is about the cost of the rounds, not about the score.

## 1. WHAT DEVIATED, PHASE BY PHASE, WITH EVIDENCE

`run_state.json` records seven phases done and the rest pending, because the
showrunner stopped updating it at Phase 7 and shipped from the score report.
That is itself a small deviation and it is noted; the evidence below comes from
`score_report.json`, `ledger/instincts.json`, `out/2026-08-27/upgrade_candidates.md`
and the artifacts.

### A gate that was silently off (art build, Phase 8)

Three slides declared a measured axis as `window.__akScale`. render.py reads
`data-scale` off the BODY (render.py, the axis census block). `__akAssert`,
`__akMotifs` and `__akLeaders` ARE window globals, so the generalisation was
natural and nothing rejected it.

Cost: qa.py's axis pixel census never ran on slides 02, 06 and 07 and the rows
read PASS. Converting the three declarations surfaced two undeclared marks on
the hero within a minute, one of them a terrain crest drawn fifty metres above
the 0 m datum it was measured from. A gate that reports nothing is worse than
one never written.

### A rule enforced on one surface out of two (copy, Phase 7)

`config/brand.yaml` visual.on_slide_text_rules bans first person on a slide
outright and cites run No.26. The only code behind the rule read the CAPTION.
Slide 07 set "OUR ARITHMETIC" in type and walked it through every machine gate.

Cost, measured: scoring pass 1 returned an uncapped 8.32 capped to 6.90 by that
one hard fail (`score_report.json.score_history_this_run[0]`). One rule, one
surface, a whole scoring pass and a whole editing round.

### A sync gate that cannot see a damaged string (copy, Phases 8 and 9)

copy.json was rebuilt from `render_report.json` twice and damaged twice, and
`copy_sync_check` passed both times because it asks only whether an authored
string is PRESENT:

- Round A: four bodies pasted out of `text`, which is cut at 80 characters. A
  truncated string is present, so presence can never see it.
- Round B: four labels rebuilt from `texts`, which holds only DIRECT text
  children, so a `<span>` wrapping a unit is dropped. "1 DOT = 0.1 g OF SILVER
  IODIDE" became "1 DOT = 0.1OF SILVER IODIDE" and the gate found it, because
  the old matcher joined every `texts` entry into one blob and the shredded
  string matched the join of the entries it came from.

Cost: two rounds, and one of them shipped four labels that had lost their units
on a deck whose thesis is that each retelling stripped a qualifier.

### A convention nobody wrote down (scoring, Phase 10)

`config/scoring_rubric.yaml`'s ten weights sum to 1.10. The rubric instructs a
literal weighted sum, every score in the ledger was computed that way, and the
thresholds were calibrated against it, so the comparison is internally
consistent. Nothing in the repo says so, and two separate scoring passes spent
time rediscovering it and writing the same note.

### Environment and budget

No install failures, no fetch failures, no API limits hit. One real budget
deviation: three of six scouts exceeded the 25 WebSearch cap, at 27, 27 and 29,
and each disclosed it in its own return. Total spend was about 158 of 200.
Nothing measured it; the showrunner learned it by reading six returns.

Repeated retries: five editing rounds, three of them spent on ONE object, the
aksdf hero. The diagnosis is already in FIELD_NOTES and instincts.json and is a
CRAFT lesson rather than a machine one, so no code was written for it here.

## 2. FRONTIER SCAN

Focus (g), accessibility and PDF/document-format changes. Stalest legal slot,
last scanned 2026-08-12, and distinct from the last three logged foci
(2026-08-26 procedural art, 2026-08-25 headless Chromium, 2026-08-21 LinkedIn
platform). Three searches, two substantive reads, one local experiment on this
studio's own artifact. Outcome: PARKED, and the parking is the finding.

The deck ships as a PDF and every archive page offers it for download, so a
tagged PDF is a real accessibility surface here. Measured, not assumed:

- Playwright 1.62's `page.pdf(tagged=True)` DOES produce `/MarkInfo` and
  `/StructTreeRoot`, verified on this run's own slide 07, for +5.9 KB on a
  4.47 MB page.
- `assemble.py` never passes it, and the shipped `runs/2026-08-27/carousel.pdf`
  carries neither key.
- The merge is where it would die anyway. pypdf 6.16.2 drops both the
  `/MarkInfo` and the `/StructTreeRoot` through `PdfWriter.add_page` (what
  assemble.py uses) AND through `PdfWriter.append`. Tested both.
- On LinkedIn itself the payoff is small: Intopia's NVDA testing of the
  document viewer found announcement order that does not follow the PDF's
  reading order, heading levels partly picked up, list tags ignored, and alt
  text acknowledged but never spoken. The gain would be on OUR archive's
  downloadable PDF, not in the feed.

Parked rather than applied because the assembly path would have to change to
carry a structure tree across nine pages, which is a redesign of the merge and
not a corner of it, and because the three upgrade slots below went to reactive
fixes. Unblocking condition and sources are in knowledge/FIELD_NOTES.md.

## 3. UPGRADES MADE (3 of 3, all reactive)

1. **A declaration on the wrong surface is now a FAIL** (render.py + qa.py).
2. **The first-person rule now runs on slide text** (caption_check.py).
3. **copy_sync_check can see a truncated or shredded string** (copy_sync_check.py
   + render.py's new `text_nodes[].full`).

Each is logged in `ledger/upgrades.json` with its verification. All three ship
as one `upgrade(2026-08-27):` commit and revert as one.

## 4. WHAT WAS DELIBERATELY NOT DONE

- **The rubric's 1.10 weight sum.** Left alone. Historical scores are NOT
  rescaled and no threshold moved; that is the maintainer's call by this
  phase's own rules. The recommendation is to add one sentence to
  `config/scoring_rubric.yaml` stating that the sum is literal and deliberate,
  and to have the scorer print the weight total beside the score. Recommended
  in the email rather than done here, because it is a convention decision and
  because the 0 to 3 upgrade budget was full of things that cost this run
  rounds.
- **The scouts' search cap.** A prompt sentence cannot be enforced from the
  showrunner's side. The reporting fix (each scout returns `searches_used`, the
  merge totals it against the ceiling) is a prompt change to six agent briefs
  and the merge step, which is more surface than a Phase 12 slot should take
  without a run behind it. Recommended, not done.
- **akstipple.js and akrail.js missing from TECHNIQUE_LIBRARY.md.** Real, and
  it is the second time an uncatalogued bench went unused. It wants both the
  two entries AND a check that walks `assets/js/*.js`, which is a fourth
  upgrade past the cap. Carried forward as the first candidate for the next
  run, and left in `upgrade_candidates.md` where the next Phase 12 will read it.
- **The hero's three rounds.** A craft lesson, already in FIELD_NOTES and
  instincts.json. No gate can tell a rock from a cloud, and building one that
  guesses would be worse than the defect.
