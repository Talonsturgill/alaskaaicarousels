# Automation retro, 2026-10-22 (No.93)

## Weekly pass

Not due. `machine_due.py`: last pass 2026-10-21, one day ago, due at seven; 21 items queued, no repeat offender. Steps 2 to 4 don't run today.

## Trend check (window 10)

Top repeat offender: Artwork craft and genuine detail, weakest on 6 of 10, mean 7.1, last worked 2026-10-04. Deferred to the weekly pass, which is where the owner put it. What this run did about it in the moment: a deck helper (assets/js/akstone.js) for stone, relief and paper so the per slide code spends its lines on the object and not on plumbing, and one hero object per frame modelled in light rather than drawn as boxes. Whether that moved the criterion is for the scorer to say.

## Deviations, phase by phase

- Phase 2 to 3. The DeepGreen story is a FERC docket, and the FERC eLibrary has no keyless reader in this repo. The run reverse engineered the eLibrary search and the DownloadP8File endpoint (POST with a JSON accession body; a GET returns 405) and parsed the docx inside the zips by hand. Queued already as the FERC eLibrary reader item (committed 74c9dd87).
- Phase 3. The City of Kenai's motion is a scanned PDF and there is no OCR in the container. Pages were rasterised with pdftoppm and read visually into kenai.txt. A tesseract install would turn this into a script.
- Phase 3.5. The docket's DeepGreen item had been refreshed for six weeks against the Federal Register only, which never lists interventions, so two motions went unrecorded. Queued (2026-10-22 docket item).
- Phase 3.6. docket-watch output check FAIL on an upstream Cloudflare challenge at akleg.gov; recorded in cron_incidents.json as an upstream blocker with attempts and evidence. Gas Watch live audit PASS.
- Phase 7. qa.py failed four frames on false evidence: strings drawn on detached TEXTURE canvases (the numbering machine's wheel bands, the slug glyph masks, the forme's height map) were placed on the page with the backing-ratio fallback and read as overprinting the wordmark, the counter and body copy. FIXED IN RUN, because it failed this deck: a detached canvas that isn't frame shaped can't be placed and is not judged; a full-frame offscreen layer, which is composited 1:1, still is. Two regression cases in tests/overprint_verify.py, which fails without the fix.
- Phase 7. The ink law census reads brushes. A brass relief computed pixel by pixel through putImageData, and a PBR brass material, never pass through a brush, so four frames failed "no brush ever carried #FFC72C" while plainly gold. Fixed in the deck with a helper, STONE.inkTint, which fills the declared ink into the object's own silhouette (a second render with every other mesh depth only, or the relief's mask) and composites it with `color`. Queued: the engine could offer the same idiom for any per-pixel or WebGL mark.
- Phase 7. Every first contact declaration was a guess and failed; contact_probe measured each one off the render. Three grounds were near black and had to be lit before any cast could read (03, 04, 08), which is the failure the doctrine already names. Not a new machine defect.

## Queued

- ink law: a per-pixel or WebGL mark has no brush to census (one line in MACHINE_QUEUE.md).
