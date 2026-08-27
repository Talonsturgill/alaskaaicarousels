# PHASE 12 CANDIDATES, found during the run

## 1. akstipple.js and akrail.js are NOT in TECHNIQUE_LIBRARY.md (found Phase 5)

`grep -c "akstipple\|akrail" knowledge/TECHNIQUE_LIBRARY.md` returns **0**. Both
files are committed under `assets/js/` and both are substantial, documented
benches. The index runs to 93 and stops, and neither ever got a number.

This is the exact failure the library's own entry 93 was written about:

> Committed 2026-07-31 for No.21 and then LOST, because it was never given a
> number here and the directors room reads this file. Five consecutive decks did
> not use it and artwork craft was the weakest criterion in four of them. That is
> the lesson: a capability that exists in code and not in the index does not
> exist.

It has happened again, and this time to the bench built specifically to fix the
standing weakness. `akstipple.js`'s own header carries the diagnosis:

> "Artwork craft and genuine detail" has been the weakest scored criterion in 8
> of the 10 runs to 2026-08-15, mean 6.1 ... What the criterion actually measures
> is DESIGN_DOCTRINE section 5, the zoom test, craft in every region, and a
> smooth physically-rendered material is beautiful and has no marks in it.

The proof that the index is what the room reads: **three treatment directors ran
in parallel this run with TECHNIQUE_LIBRARY.md in their brief, and not one of
them proposed akstipple.** One of them proposed writing a new marked-volume
renderer from scratch, and named its own biggest risk as the fact that it would
be new code. The capability it wanted was already committed, tested and shipped
once, and it was invisible.

**The upgrade.** Give both benches numbers, 94 for akstipple and 95 for akrail,
written in the house style with the load bearing parameters and the traps
(`height` is required and throws with no default, `box` must be passed whenever
the region is small relative to the frame, the three-function rule that density,
radius and alpha are separate functions of the same quantity, `reserve()` before
`field()` and after `document.fonts.ready`).

**Verification bar.** A grep for each module name in the index returns non-zero,
and the entries name the same traps the module headers do.

**The stronger version of the same fix, if it is boundable.** A check that walks
`assets/js/*.js` and fails when a committed module is not mentioned in
TECHNIQUE_LIBRARY.md. Prose has now failed at this twice and a gate would not.
That is the preferred shape per Phase 12's own rule to prefer objective
machinery over prose instructions.

## 2. Search budget overrun is invisible until the retro (found Phase 2)

Three of six scouts exceeded the 25 WebSearch cap this run, at 27, 27 and 29,
and every one of them disclosed it honestly in its own return. Nothing measured
it, nothing enforced it, and the showrunner learned it only by reading six
returns. The cap exists because a previous run's scouts ate the whole session
budget and Phase 12's frontier scan recorded zero searches available on four
separate days.

Total spend this run was roughly 158 of about 200.

**The upgrade, if boundable.** The cap is currently a sentence in a prompt. It
cannot be enforced from the showrunner's side. What CAN be done is to make the
overrun visible without reading six full returns, by requiring each scout to
return a `searches_used` integer and having the merge step total them and print
the figure against the ceiling. That is a reporting fix rather than a gate, and
it should be described as one.
