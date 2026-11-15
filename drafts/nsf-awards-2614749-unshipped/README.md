# UNSHIPPED — NSF awards 2614749 and 2614751 — parked 2026-08-15

**This is not a shipped run. Nothing here has a carousel number and nothing here
is in any ledger.** It is parked so a verified story and a part-built deck
survive the container, pending a decision by the maintainer.

## Why it is parked rather than shipped

Two sessions worked the 2026-08-14 slot in parallel without knowing about each
other. The other session finished first and merged **Carousel No. 33, "The
Equal-Award Projection, 552 to 1"** to `main` at 08:51 on 2026-08-15 (PR #269,
commit 3efd24e). That deck is about NSF solicitation 26-513, the one-award-per-
state cap, and the 552 to 1 Alaska to Rhode Island land area ratio. It scored
8.45 with every gate green and its artifacts are in `runs/2026-08-14/`.

This session had independently researched and verified a DIFFERENT story for the
same slot. Continuing would have meant overwriting `runs/2026-08-14/`, adding a
second No. 33 to `ledger/topics.json`, `artwork.json` and `captions.json`, and
drafting a second Gmail for one date. CLAUDE.md names overwriting shipped run
artifacts as one of three things that stop and ask, so the run stopped.

Nothing shipped was touched. This directory sits outside `runs/` deliberately,
because `scripts/site_build.py` iterates `runs/` at line 5062 and an extra
directory there would have produced a bogus archive entry.

## The story, and it is still unshipped and still good

On August 5th, 2026 NSF obligated three linked standard grants under EPSCoR RII
Focused EPSCoR Collaborations for one project. The **University of Alaska
ANCHORAGE leads** at $3,824,575, UAF holds $913,037, Montana Technological
University in Butte holds $1,260,800, and all three are obligated in full in
fiscal 2026. Alaska's share is $4,737,612 and Anchorage holds about 4.2 times
what Fairbanks holds, which inverts the assumption that Alaska research money
runs through Fairbanks.

The abstract describes applying "reinforcement-learning controllers within a
bioprocess digital twin integrated with microgrid simulators" to steer
*Shewanella oneidensis* recovering rare earth elements from domestic coal refuse
and ash, as an energy-constrained system. NSF's own program tag on the award
includes Artificial Intelligence. No large language model appears anywhere in
the abstract. Nothing is built; the grant starts September 1st, 2026.

Two scouts on unrelated beats (research and Indigenous AI, and robotics and
national with Alaska teeth) found this independently and both named it the best
unreported thing they had. As of August 14th no item about award 2614749
appeared on the UAF news listing spanning July 24th to August 13th, or on the
UAA news index.

## Dedupe status against the ledger AS IT NOW STANDS

Re-run after No. 33 shipped:

    exit 0, soft overlaps only. Strongest match No.33 2026-08-14,
    1 shared entity (NSF), token jaccard 0.017.

The two NSF stories are genuinely distinct. No. 33 is a SOLICITATION and its
per-state award cap. This is a set of ISSUED AWARDS, a different program, a
different mechanism and a different argument. It would clear the 30 day rule as
a future run.

## What is here and what state it is in

| Artifact | State |
|---|---|
| `claims.json` | 36 claims, `claims_check` PASS, 36/36 usable, all primary, all from the NSF Award API |
| `caption.txt` | `caption_check` PASS, 896 chars, hook 125. Winner of a two director room, one critic fix applied |
| `storyboard.md` | 10 full dossiers, `dossier_check` PASS 10/10 |
| `selection.md` | Story choice, the dedupe reasoning, three director treatments and the synthesis |
| `scout_merge.md` | Six beat scouts merged, with the killed and quarantined leads |
| `slides/` | 3 of 10 built (01 cover GPU, 02 record sheet, 03 mechanism) |
| `render/` | 3 PNGs, `qa.py` PASS, 0 fails 0 warns |

Slides 04 to 10 are specified in full in `storyboard.md` but not built.

## If the maintainer wants this shipped

It would be a NEW run with a NEW number and a NEW date, never a second No. 33.
The work needed before it could ship:

1. Re-run the ten day NSF window query for the new run date. The caption's
   "ten days ending August 14th" and claims C26 to C29 are scoped to a window
   that moves.
2. Re-read the two campus news indexes and re-date C34 and C35, which are
   scoped to reads made on August 14th.
3. Build slides 04 to 10 from the dossiers.
4. Run the normal remaining phases, pixel review, flow review, assembly,
   `bespoke_check`, `aggregate_check`, scoring, ship, upgrade, Gmail.

## One fix from this session that DID land

The CI "Docket dates" check was red on `main`. The cause was not the gate. It
was `docket_dates_check.py`'s own self-test B, which counted any relabelled date
as injected breakage while the resolver correctly ignores dates that have
passed. The ledger's only qualifying date was a Houston City Council vote of
August 13th, so once that date passed the injected breakage became invisible and
the test declared the gate blind. The fallback fixture rotted the same way by
judging itself at the live date. Fixed to count a mislabel only when it lands in
the future, and to run the fixture at its own anchor. Verified at four dates, no
threshold moved and no assertion removed. That fix is on `main`.
