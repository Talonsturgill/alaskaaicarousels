# AUTOMATION RETRO - Carousel No. 41 - 2026-08-26

Phase 12. Run_state walked phase by phase against prompts/routine_instructions.md,
with the evidence for each deviation named. The run SHIPPED at 8.51 against a
round-5 threshold of 7.7, zero hard fails, weakest criterion artwork craft at 6.

## Phase-by-phase deviations

| Phase | Verdict | Evidence |
|---|---|---|
| wake .. gas_watch | to spec | site_signoff PASS (85 pages, 18 checks), gaswatch_pagecheck PASS, docket 16 items re-verified |
| research / claims | ONE REVERSAL | showrunner killed NSF award 2536745 on a regex for the two-word "machine learning" against an abstract that hyphenates it; NSF files the award under progRefCode 075Z (Artificial Intelligence). Fact-checker reversed. Deck is 5 projects / 6 awards / $18,647,929, not 4 / $17,059,782. A tool that answers "no" was read as a fact. |
| copy / art_build | to spec | 48 claims, 47 primary, claims_check PASS |
| pixel_review | POLICY CHANGE MID-RUN | Owner capped editing at FIVE rounds after first render: "judges are becoming a token burning crutch masking inefficiencies". Five pixel critics returned a mean of 6.1; the run then spent more time reacting to their lists than it had spent building the deck. |
| pixel_review, rounds 3-5 | TWO SELF-INFLICTED REGRESSIONS | (a) type reserve on six slides written as `createRadialGradient(0,0,24,0,0,r)` filled into `ctx.ellipse(cx,cy,r,ry)`, ry < r: circular ramp, elliptical fill, hard arc across the ground of all six. Four critics called it the most conspicuous thing in the frame. (b) contact declarations failing the 4.0 L* floor were repaired by widening pools and deepening casts to plus thirty; five critics then read a detached black hole in a spotlight with no light source. Each cost a full round. |
| art_build | FIVE OF NINE DECLARATIONS WRONG, ONE WAY | ground rect placed directly BELOW the shadow rect, landing it on the lit pool's dark edge while the shadow sat near the pool's bright centre; three measured NEGATIVE separation; slide 03's pair was 118px from where the marker drew. Diagnosed each time by a throwaway profiling script, written and discarded repeatedly in one run. |
| flow_review | DEGRADED, DECLARED | showrunner read the contact sheet in place of a flow-critic round, per the cap. This is how slide 07's rust-red ramp regression was caught, so the degraded path did work. |
| dossier gate | FALSE FAILURE | `dossier_check.slide_sections()` ran the last slide's section to end of file, so the deck-level BUILD RECONCILIATION section (which describes contact-shadow repairs) was parsed as SLIDE 09's dossier and slide 09 failed a promise it never made. Worked around by moving the section above SLIDE 01. |
| aggregate gate | COST CYCLES | `aggregate_check.py` parses the count from `text` for the cross-deck CONTRADICTION check but from `fragment or text` everywhere else, so a rendered string carrying two numbers self-contradicts unless every count declaration carries an explicit `n`. |
| ship / docket_alerts | DISCLOSURE FAILURE | `scripts/docket_alerts.py` SENT one live Buttondown subscriber email during Phase 11 while looking like a SKIP: the key is provisioned as env `Buttondown`, and CLAUDE.md and the script's docstring both name `BUTTONDOWN_API_KEY` first, so a check of the documented name reads "not set". The send was correct and the alert was real; the run could not know in advance. |
| tooling friction | SMALL | `render.py --only` takes integers and errors unhelpfully on `--only slide-05`. `window.__akProbes` is read by nothing, so a slide declaring hachure predictions gets no feedback; slide 06's meanWidth ratio needed a standalone Playwright harness. |

## What the cap changes about this phase

An upgrade that makes a LATER round cheaper is now worth less than one that
makes the FIRST build correct. Two of the three chosen upgrades move a
measurement to before the render is reviewed; the third removes a false failure
that cost an authoring workaround.

## Upgrades chosen (3 of 3), reactive-first

1. engine: the circular-ramp-in-an-ellipse defect is detected as the slide
   draws, and qa.py WARNs with the exact `scale()` to write instead.
   Reconstruction: `tests/gradient_clip_verify.py`. It found two live
   instances in this run's own shipped slide 08.
2. scripts: `contact_probe.py`, which measures a contact declaration off the
   render in qa.py's own colour space at qa.py's own feed width, proposes the
   rect pair from the object's base line, and names the stacked-rect and
   detached-cast defects. Reconstruction: `tests/contact_probe_verify.py`.
3. scripts: `dossier_check` bounds the last dossier at the next top-level
   heading that is not a slide. Reconstruction: `tests/dossier_tail_verify.py`,
   which reproduces the failure against this run's own storyboard.

## Deliberately NOT done, and why

- **No upper threshold on contact-shadow depth.** The "black hole" defect looks
  like a candidate for a dL ceiling in qa.py, and it is not one. This run's own
  slides measured 11.5 to 43.8 dL and the deep ones were not all wrong: slide
  05's cast sits on L* 84 scree where a deep core is correct, slide 08's on
  L* 27 rail where a shallow one is. The defect is spatial (a dark blob
  detached from its object inside a pool with no light source), not scalar. A
  ceiling would have been a threshold that fires on honest drawing, which is
  worse than nothing. The probe reports the structure instead.
- **`docket_alerts.py` pre-send disclosure.** Genuinely worth doing and only
  about fifteen lines, but the right fix may be to make the environment supply
  the documented name rather than to teach the script a second one, and that is
  the maintainer's call. Recommended in the email. Interim: the script DOES
  find `Buttondown`; do not read "BUTTONDOWN_API_KEY not set" as "will skip".
- **`aggregate_check.py` count-source inconsistency** and the two small tooling
  frictions: real, but each is a behaviour change inside a gate that this run
  did not have budget to verify to the bar. Carried to the next Phase 12.

## Frontier scan

Focus (c), generative/procedural art portable to offline Canvas/SVG. Chosen for
relevance rather than staleness: artwork craft was again the weakest criterion,
and both of this run's expensive regressions were canvas shading idioms. Six
searches, one substantive read. Two candidates parked in FIELD_NOTES (the
second domain warp stage from iquilezles.org, which noise.js's `warp2` stops
short of; and `shadowBlur` being immune to the current transformation matrix).
One finding corroborated an upgrade rather than adding one: the scrim behind
type is the standard device, and a rescaled circle is the only way to draw an
elliptical gradient on Canvas.
