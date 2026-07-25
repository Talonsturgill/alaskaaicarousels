#!/usr/bin/env python3
"""scanner_sync_check.py -- guard the contract the live scanner page depends on.

WHY THIS EXISTS, AND WHY IT WAS REBUILT
    The live Bottleneck Scanner page is emitted by scan_page() in
    scripts/site_build.py. The routine that feeds it lives in another repo,
    Talonsturgill/alaska-ai-scanner. They are two hand maintained sides of one
    flow, and they are SUPPOSED to look nothing alike. What they are not
    allowed to disagree about is the contract between them.

    The first version of this check compared the live page against
    vendor/scanner/scan.html, a reference implementation of the same page. That
    was the wrong document to guard, and it cost us. Scanner PR #10 made the
    routine write 60 to 120 progress notes a run instead of a dozen and added a
    `kind` field to every note so the wait page counters would survive the
    density. This check stayed green through all of it, because `kind` is not a
    value it compared and does not appear in scan.html at all. Meanwhile the
    HONESTY GATE ROUNDS tile silently started reading 50 for a five round gate.

    A reference implementation is not a specification. The specification is
    prompts/scan_routine.md, because the routine literally executes it at fire
    time. So the feed contract is now guarded against THAT, and scan.html is
    demoted to what it actually is, a carrier for four wiring constants.

WHAT IT CHECKS, AND AGAINST WHAT

    from vendor/scanner/scan_routine.md  (THE SPECIFICATION)
      PHASES   the ordered phase list, which drives the ring and the roster
      KINDS    the note kinds, which drive the three live counters

    from vendor/scanner/scan.html  (wiring constants only, NOT a spec)
      FN          the Supabase function base URL
      PUBKEY      the publishable key sent as apikey and bearer
      TS_SITEKEY  the Cloudflare Turnstile sitekey
      endpoints   the /scan-* function names either side calls

    It also asserts the live page still counts by `kind` at all, so a revert to
    phase counting fails here rather than on a visitor's screen.

    It does NOT diff markup, classes, CSS, fonts, copy, artwork or layout.
    Those are meant to differ and comparing them would make the check noise.

THE KIND RULES, WHICH ARE THE POINT
    A kind the page counts but the routine never writes leaves a tile stuck at
    zero. A kind the routine writes that the page has no decision about is the
    exact shape of the bug above, so a new kind fails until someone either
    counts it or adds it to IGNORED_KINDS on purpose.

EXIT CODES
    0  the two sides agree
    1  drift, or a value could not be found on one side
    2  usage / missing-file error

This script reads only. Fix reported drift by reconciling scan_page() in
scripts/site_build.py, or, when the scanner side genuinely changed, re-vendor
per vendor/scanner/README.md and update both sides in one commit.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REF_HTML = REPO / "vendor" / "scanner" / "scan.html"
REF_SPEC = REPO / "vendor" / "scanner" / "scan_routine.md"
LIVE = REPO / "scripts" / "site_build.py"

HTML_LABEL = "vendor/scanner/scan.html"
SPEC_LABEL = "vendor/scanner/scan_routine.md"
LIVE_LABEL = "scripts/site_build.py scan_page()"

# Kinds the routine writes that the live page deliberately does not count.
# Adding to this list is a decision, which is the whole point of it existing.
IGNORED_KINDS = {"step"}

ENDPOINT_RE = re.compile(r"/(scan-[a-z][a-z0-9-]*)")


# ---------- readers ----------

def scalar(text, name):
    """The string literal assigned to `name`, or None. Matches both const and
    var styles, double quoted, which is what both sides use."""
    m = re.search(r"\b" + re.escape(name) + r"\s*=\s*\"([^\"]*)\"", text)
    return m.group(1) if m else None


def endpoints(text):
    return sorted(set(ENDPOINT_RE.findall(text)))


def spec_phases(text):
    """The ordered phase list from THE PROGRESS FEED. The spec writes it as a
    prose line directly under the `phase` bullet."""
    m = re.search(r"drives the stepper[^\n]*\n\s*([a-z][a-z, ]*[a-z])\s*\n", text)
    return [p.strip() for p in m.group(1).split(",")] if m else None


def spec_kinds(text):
    """The note kinds from THE PROGRESS FEED, as sub bullets under `kind`."""
    i = text.find("drives the three live counters")
    if i < 0:
        return None
    out = []
    for line in text[i:].split("\n")[1:]:
        if re.match(r"^[A-Z]", line):        # next section heading, stop
            break
        m = re.match(r"^\s+-\s+`([a-z]+)`", line)
        if m:
            out.append(m.group(1))
    return out or None


def live_phases(text):
    m = re.search(r"\bPHASES\s*=\s*\[(.*?)\]", text, re.S)
    return re.findall(r"\"([^\"]+)\"", m.group(1)) if m else None


def live_kinds(text):
    """The kinds the counter block actually keys on."""
    return sorted(set(re.findall(r'\bkd\s*===\s*"([a-z]+)"', text)))


def counts_by_kind(text):
    """True when the counter block reads the note's kind at all."""
    return bool(re.search(r"\bkd\s*=\s*notes\[i\]\s*&&\s*notes\[i\]\.kind", text))


def scan_page_src(text):
    """Slice site_build.py down to scan_page(), so a stray match elsewhere in
    the builder can never satisfy or break the check."""
    start = text.find("def scan_page(")
    if start < 0:
        return None
    nxt = re.search(r"\ndef [a-z_]+\(", text[start + 1:])
    return text[start:start + 1 + nxt.start()] if nxt else text[start:]


# ---------- comparisons ----------

def compare(name, ref, ref_label, live, problems, hint):
    if ref is None or live is None:
        problems.append(
            "%s could not be found in %s.\n"
            "    Either it was renamed or its shape changed. %s"
            % (name, ref_label if ref is None else LIVE_LABEL, hint))
        return
    if ref != live:
        problems.append(
            "%s has drifted.\n    %-34s %r\n    %-34s %r\n    %s"
            % (name, ref_label, ref, LIVE_LABEL, live, hint))


def check_phases(ref, live, problems):
    if ref is None or live is None:
        problems.append(
            "The phase list (PHASES) could not be found in %s.\n"
            "    The ring, the agent roster and the quips all read it."
            % (SPEC_LABEL if ref is None else LIVE_LABEL))
        return
    if ref == live:
        return
    detail = ""
    only_ref = [p for p in ref if p not in live]
    only_live = [p for p in live if p not in ref]
    if only_ref:
        detail += "\n    missing from the live page   %s" % ", ".join(only_ref)
    if only_live:
        detail += "\n    unknown to the routine       %s" % ", ".join(only_live)
    if not detail:
        detail = ("\n    same phases, different order, and the order is what "
                  "drives the ring and the roster")
    problems.append(
        "The phase list (PHASES) has drifted.\n    %-34s %s\n    %-34s %s%s\n"
        "    A phase the live page does not know sits at 0 percent on the "
        "ring and lights no agent." % (SPEC_LABEL, ref, LIVE_LABEL, live, detail))


def check_kinds(ref, live, problems):
    """The guard that would have caught scanner PR #10."""
    if ref is None:
        problems.append(
            "The note kinds could not be found in %s.\n"
            "    They drive the three live counters, so this check is blind "
            "without them." % SPEC_LABEL)
        return
    unknown = [k for k in live if k not in ref]
    if unknown:
        problems.append(
            "The live page counts a kind the routine never writes.\n"
            "    %-34s %s\n    %-34s %s\n"
            "    counted but never written    %s\n"
            "    That tile will sit at zero for every scan."
            % (SPEC_LABEL, ref, LIVE_LABEL, live, ", ".join(unknown)))
    undecided = [k for k in ref if k not in live and k not in IGNORED_KINDS]
    if undecided:
        problems.append(
            "The routine writes a kind the live page has no decision about.\n"
            "    %-34s %s\n    %-34s %s\n"
            "    new, and neither counted nor ignored   %s\n"
            "    Either count it in scan_page() or add it to IGNORED_KINDS in "
            "this script, on purpose.\n"
            "    This is the exact shape of the bug that shipped when the feed "
            "went dense, so it fails loudly."
            % (SPEC_LABEL, ref, LIVE_LABEL, live, ", ".join(undecided)))


def main():
    ap = argparse.ArgumentParser(
        description="Verify the live scanner page still agrees with the "
                    "routine contract it depends on.")
    ap.add_argument("--spec", default=str(REF_SPEC), help="vendored scan_routine.md")
    ap.add_argument("--ref", default=str(REF_HTML), help="vendored reference page")
    ap.add_argument("--live", default=str(LIVE), help="the site builder")
    args = ap.parse_args()

    try:
        spec_txt = Path(args.spec).read_text()
    except OSError as e:
        print("scanner_sync_check: cannot read the routine contract: %s" % e, file=sys.stderr)
        print("Re-vendor it per vendor/scanner/README.md.", file=sys.stderr)
        return 2
    try:
        ref_txt = Path(args.ref).read_text()
    except OSError as e:
        print("scanner_sync_check: cannot read the reference page: %s" % e, file=sys.stderr)
        print("Re-vendor it per vendor/scanner/README.md.", file=sys.stderr)
        return 2
    try:
        live_all = Path(args.live).read_text()
    except OSError as e:
        print("scanner_sync_check: cannot read the site builder: %s" % e, file=sys.stderr)
        return 2

    live_txt = scan_page_src(live_all)
    if live_txt is None:
        print("scanner_sync_check: no scan_page() in %s" % args.live, file=sys.stderr)
        print("If the page moved, point --live at its new home.", file=sys.stderr)
        return 2

    problems = []

    compare("The function base URL (FN)", scalar(ref_txt, "FN"), HTML_LABEL,
            scalar(live_txt, "FN"), problems,
            "Every request from the page goes to this host, so a stale one "
            "means the page talks to nothing.")
    compare("The publishable key (PUBKEY)", scalar(ref_txt, "PUBKEY"), HTML_LABEL,
            scalar(live_txt, "PUBKEY"), problems,
            "It is sent as both apikey and the bearer token, so a stale one "
            "means every call comes back 401.")
    compare("The Turnstile sitekey (TS_SITEKEY)", scalar(ref_txt, "TS_SITEKEY"),
            HTML_LABEL, scalar(live_txt, "TS_SITEKEY"), problems,
            "The gatekeeper requires a token whenever the matching secret is "
            "set server-side, so a stale sitekey means nobody can start a scan.")

    ref_ep, live_ep = endpoints(ref_txt), endpoints(live_txt)
    if ref_ep != live_ep:
        detail = ""
        only_ref = [e for e in ref_ep if e not in live_ep]
        only_live = [e for e in live_ep if e not in ref_ep]
        if only_ref:
            detail += "\n    called by the reference, not by the live page   %s" % ", ".join(only_ref)
        if only_live:
            detail += "\n    called by the live page, not by the reference   %s" % ", ".join(only_live)
        problems.append(
            "The endpoint names have drifted.%s\n"
            "    An endpoint only one side calls is a feature only one side ships." % detail)

    check_phases(spec_phases(spec_txt), live_phases(live_txt), problems)

    kinds_ref, kinds_live = spec_kinds(spec_txt), live_kinds(live_txt)
    if not counts_by_kind(live_txt):
        problems.append(
            "The live page no longer counts by kind.\n"
            "    %s says \"The counters count `kind`, never `phase`.\"\n"
            "    Counting by phase inflates every tile the moment the feed "
            "runs dense, which is what it does now." % SPEC_LABEL)
    else:
        check_kinds(kinds_ref, kinds_live, problems)

    if not problems:
        print("scanner_sync_check: PASS")
        print("  spec        %s" % SPEC_LABEL)
        print("  wiring      %s" % HTML_LABEL)
        print("  function base URL   %s" % scalar(ref_txt, "FN"))
        print("  publishable key     %s" % scalar(ref_txt, "PUBKEY"))
        print("  turnstile sitekey   %s" % scalar(ref_txt, "TS_SITEKEY"))
        print("  endpoints (%d)       %s" % (len(ref_ep), ", ".join(ref_ep)))
        ph = spec_phases(spec_txt) or []
        print("  phases (%d)          %s" % (len(ph), ", ".join(ph)))
        print("  kinds (%d)           %s" % (len(kinds_ref or []), ", ".join(kinds_ref or [])))
        print("  counted (%d)         %s" % (len(kinds_live), ", ".join(kinds_live)))
        print("  ignored (%d)         %s" % (len(IGNORED_KINDS), ", ".join(sorted(IGNORED_KINDS))))
        print("  markup, CSS and copy are NOT compared, the two pages are "
              "meant to look different")
        return 0

    print("scanner_sync_check: FAIL -- %d contract mismatch(es) between the "
          "live scanner page and the routine it serves:\n" % len(problems))
    for i, p in enumerate(problems, 1):
        print("  %d. %s\n" % (i, p))
    print("Fix by reconciling scan_page() in scripts/site_build.py,")
    print("then rebuild with  python scripts/site_build.py --date <YYYY-MM-DD> --out docs")
    print("If the SCANNER side changed, re-vendor per vendor/scanner/README.md")
    print("and update both sides in one commit.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
