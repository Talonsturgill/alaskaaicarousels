#!/usr/bin/env python3
"""cast_promise_verify.py -- the reconstruction behind dossier_check's
"the dossier promises a cast" WARN (2026-10-16, weekly machine pass).

WHAT IT RECONSTRUCTS. Run No.88's dossiers for slides 02 and 03 promised a plate
that "casts onto the base". Neither slide declared data-contacts, so qa.py's
contact gate (which already says "light the ground first" for a declared cast on
a near-black ground) never looked, and on a desk at L* 5 to 7 neither cast read.
dossier_check's contact promise only knew the words "contact shadow" and
"two-part shadow".

  python3 tests/cast_promise_verify.py     # exit 0 = the check holds

Calls dossier_check.check_slide directly with a minimal dossier body.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dossier_check as D  # noqa: E402

BASE = ("**4a. Lower third:** the walnut desk under a lit bevel, graded, with the "
        "plate's cast and a burnished ledger rule.\n")
MARK = "the dossier promises a cast"


def run(body, contacts=None, built=True, runtime=()):
    fails, warns = D.check_slide(2, "SLIDE 02", BASE + body, None, contacts=contacts,
                                 built=built, runtime=runtime)
    return fails, [w for w in warns if MARK in w]


def main():
    bad = 0

    def ok(label, cond, extra=""):
        nonlocal bad
        print("  %s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond else "  " + str(extra)))
        bad += 0 if cond else 1

    f, w = run("- [ ] the carbon sheet's lifted corner casts onto the base\n- [ ] DUE OCTOBER 26\n")
    ok("No.88 slide 02: a promised cast with no data-contacts WARNS", len(w) == 1, w)
    ok("... and quotes the phrase only, not the next checklist line",
       w and "'casts onto the base'" in w[0], w)
    f, w = run("the plate-mark bevel and its cast onto the base below it. **5. Depth**\n")
    ok("No.88 slide 03: 'cast onto the base below it' WARNS", len(w) == 1, w)
    f, w = run("- [ ] the lifted corner casts onto the base\n", contacts=1)
    ok("a slide that declares data-contacts is silent", not w, w)
    f, w = run("- [ ] the lifted corner casts onto the base\n", runtime=("data-contacts",))
    ok("a runtime declaration is not called missing here", not w, w)
    f, w = run("its embossed LED array casting a pool onto the road below\n")
    ok("light thrown onto a ground is not a cast", not w, w)
    f, w = run("- [ ] the lifted corner casts onto the base\n", built=False)
    ok("before the build there is nothing to point at", not w, w)
    f, w = run("a two-part contact shadow under the plate, which casts onto the desk\n")
    ok("the strong promise keeps its own FAIL and adds no second finding",
       not w and any("promises a contact shadow" in x for x in f), (f, w))
    for body in ("the plate casts a sharp shadow with no penumbra onto the desk\n",
                 "the plate casts a hard shape without blur onto the desk\n"):
        f, w = run(body)
        ok("'no'/'without' qualifying the shadow keeps the promise: " + body.strip(), len(w) == 1, w)
    for body in ("the plate casts no shadow onto the desk\n", "the plate does not cast onto the desk\n",
                 "the plate cannot cast onto the desk\n"):
        f, w = run(body)
        ok("a negated cast promises nothing: " + body.strip(), not w, w)
    for body in ("the lamp glows and softly casts onto the desk\n", "the lamp glows and will cast onto the desk\n"):
        f, w = run(body)
        ok("a shared light subject survives an adverb or auxiliary: " + body.strip(), not w, w)
    f, w = run("the plates catch the light and cast onto the base\n")
    ok("a shared subject is the clause's subject, not its object", len(w) == 1, w)
    print("\ncast promise check: " + ("HOLDS" if not bad else "%d BROKEN" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
