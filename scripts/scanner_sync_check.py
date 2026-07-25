#!/usr/bin/env python3
"""scanner_sync_check.py -- guard the contract shared by the two Bottleneck
Scanner front ends.

WHY THIS EXISTS
    There are two hand maintained implementations of one flow.

      vendor/scanner/scan.html   the reference page from the backend repo
                                 (Talonsturgill/alaska-ai-scanner web/scan.html),
                                 vendored verbatim, never served
      scripts/site_build.py      scan_page(), which emits the page real
                                 visitors load at alaskaaihq.com/scan/

    They are SUPPOSED to look nothing alike. The live page wears this site's
    shell (Fraunces, JBMono, the --panel and --line tokens, the gold .cta, the
    shared nav and footer); the reference page is a standalone dark page with
    its own type and its own tokens. Copy is written twice, on purpose.

    What they are NOT allowed to disagree about is the contract with the
    backend. When PR #9 rebuilt the waiting view over there, the live page
    kept its old spinner, because nothing machine checked the gap. If the
    backend moves its function URL, rotates the publishable key, changes the
    Turnstile sitekey, renames a progress phase, or adds an endpoint, the two
    sides silently fall out of agreement and the live page breaks in a way
    that only a visitor notices.

WHAT IT CHECKS
    Five values, and nothing else.

      FN            the Supabase function base URL
      PUBKEY        the publishable key sent as apikey and bearer
      TS_SITEKEY    the Cloudflare Turnstile sitekey (public)
      PHASES        the ordered phase list the progress feed writes on every
                    note, which drives the ring, the roster and the quips
      endpoints     every /scan-* function name either page calls

    It does NOT diff markup, classes, CSS, copy, artwork, or layout. Those are
    meant to differ and comparing them would make the check noise.

EXIT CODES
    0  the two sides agree on the contract
    1  drift, or a value could not be found on one side
    2  usage / missing-file error

This script reads only. Fix reported drift by reconciling scan_page() in
scripts/site_build.py to the vendored reference (or, when the backend really
did change, re-vendor per vendor/scanner/README.md and update BOTH sides in
one commit).
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REF = REPO / "vendor" / "scanner" / "scan.html"
LIVE = REPO / "scripts" / "site_build.py"

REF_LABEL = "vendor/scanner/scan.html"
LIVE_LABEL = "scripts/site_build.py scan_page()"

# Every /scan-<name> function either page is allowed to call. A name that
# appears on one side and not the other is drift in both directions: a live
# page calling an endpoint the reference does not know about is just as much
# a gap as the reverse.
ENDPOINT_RE = re.compile(r"/(scan-[a-z][a-z0-9-]*)")


def scalar(text, name):
    """Return the string literal assigned to `name`, or None.

    Matches both files' styles, `const FN = "..."` and `var FN = "..."`, and
    a bare reassignment. Only double-quoted literals, which is what both
    sides use."""
    m = re.search(r"\b" + re.escape(name) + r"\s*=\s*\"([^\"]*)\"", text)
    return m.group(1) if m else None


def phases(text):
    """Return the ordered PHASES list, or None if the array is not found."""
    m = re.search(r"\bPHASES\s*=\s*\[(.*?)\]", text, re.S)
    if not m:
        return None
    return re.findall(r"\"([^\"]+)\"", m.group(1))


def endpoints(text):
    return sorted(set(ENDPOINT_RE.findall(text)))


def scan_page_src(text):
    """Slice site_build.py down to scan_page() so a stray match elsewhere in
    the builder can never satisfy or break the check."""
    start = text.find("def scan_page(")
    if start < 0:
        return None
    nxt = re.search(r"\ndef [a-z_]+\(", text[start + 1:])
    return text[start:start + 1 + nxt.start()] if nxt else text[start:]


def compare(name, ref, live, problems, hint):
    if ref is None or live is None:
        missing = REF_LABEL if ref is None else LIVE_LABEL
        problems.append(
            "%s could not be found in %s.\n"
            "    Either it was renamed or the assignment style changed. %s"
            % (name, missing, hint))
        return
    if ref != live:
        problems.append(
            "%s has drifted.\n"
            "    %-34s %r\n"
            "    %-34s %r\n"
            "    %s" % (name, REF_LABEL, ref, LIVE_LABEL, live, hint))


def main():
    ap = argparse.ArgumentParser(
        description="Verify the live scanner page and the vendored reference "
                    "still agree on the backend contract.")
    ap.add_argument("--ref", default=str(REF), help="vendored reference page")
    ap.add_argument("--live", default=str(LIVE), help="the site builder")
    args = ap.parse_args()

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
    compare("The function base URL (FN)", scalar(ref_txt, "FN"), scalar(live_txt, "FN"),
            problems,
            "Every request from the page goes to this host, so a stale one "
            "means the page talks to nothing.")
    compare("The publishable key (PUBKEY)", scalar(ref_txt, "PUBKEY"), scalar(live_txt, "PUBKEY"),
            problems,
            "It is sent as both apikey and the bearer token, so a stale one "
            "means every call comes back 401.")
    compare("The Turnstile sitekey (TS_SITEKEY)",
            scalar(ref_txt, "TS_SITEKEY"), scalar(live_txt, "TS_SITEKEY"), problems,
            "The gatekeeper requires a token whenever the matching secret is "
            "set server-side, so a stale sitekey means nobody can start a scan.")

    ref_ph, live_ph = phases(ref_txt), phases(live_txt)
    if ref_ph is None or live_ph is None:
        problems.append(
            "The phase list (PHASES) could not be found in %s.\n"
            "    The ring, the agent roster and the quips all read it."
            % (REF_LABEL if ref_ph is None else LIVE_LABEL))
    elif ref_ph != live_ph:
        only_ref = [p for p in ref_ph if p not in live_ph]
        only_live = [p for p in live_ph if p not in ref_ph]
        detail = ""
        if only_ref:
            detail += "\n    missing from the live page   %s" % ", ".join(only_ref)
        if only_live:
            detail += "\n    unknown to the reference     %s" % ", ".join(only_live)
        if not detail:
            detail = "\n    same phases, different order, and the order is what " \
                     "drives the ring and the roster"
        problems.append(
            "The phase list (PHASES) has drifted.\n"
            "    %-34s %s\n"
            "    %-34s %s%s\n"
            "    A phase the live page does not know sits at 0 percent on the "
            "ring and lights no agent."
            % (REF_LABEL, ref_ph, LIVE_LABEL, live_ph, detail))

    ref_ep, live_ep = endpoints(ref_txt), endpoints(live_txt)
    if ref_ep != live_ep:
        only_ref = [e for e in ref_ep if e not in live_ep]
        only_live = [e for e in live_ep if e not in ref_ep]
        detail = ""
        if only_ref:
            detail += "\n    called by the reference, not by the live page   %s" % ", ".join(only_ref)
        if only_live:
            detail += "\n    called by the live page, not by the reference   %s" % ", ".join(only_live)
        problems.append(
            "The endpoint names have drifted.%s\n"
            "    An endpoint only one side calls is a feature only one side ships."
            % detail)

    if not problems:
        print("scanner_sync_check: PASS")
        print("  function base URL   %s" % scalar(ref_txt, "FN"))
        print("  publishable key     %s" % scalar(ref_txt, "PUBKEY"))
        print("  turnstile sitekey   %s" % scalar(ref_txt, "TS_SITEKEY"))
        print("  phases (%d)          %s" % (len(ref_ph), ", ".join(ref_ph)))
        print("  endpoints (%d)       %s" % (len(ref_ep), ", ".join(ref_ep)))
        print("  markup, CSS and copy are NOT compared, the two pages are "
              "meant to look different")
        return 0

    print("scanner_sync_check: FAIL -- %d contract mismatch(es) between the "
          "live scanner page and the vendored reference:\n" % len(problems))
    for i, p in enumerate(problems, 1):
        print("  %d. %s\n" % (i, p))
    print("Fix by reconciling scan_page() in scripts/site_build.py to "
          "vendor/scanner/scan.html,")
    print("then rebuild with  python scripts/site_build.py --date <YYYY-MM-DD> --out docs")
    print("If the BACKEND is what changed, re-vendor the reference per "
          "vendor/scanner/README.md")
    print("and update both sides in one commit.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
