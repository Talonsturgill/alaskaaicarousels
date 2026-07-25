#!/usr/bin/env python3
"""scanner_sync_check.py -- guard the contract the live scanner page depends on.

WHY THIS EXISTS
    The live Bottleneck Scanner page is emitted by scan_page() in
    scripts/site_build.py. The routine that feeds it lives in another repo,
    Talonsturgill/alaska-ai-scanner. They are two hand maintained sides of one
    flow, and they are SUPPOSED to look nothing alike. What they are not
    allowed to disagree about is the contract between them.

    Version one compared the live page against vendor/scanner/scan.html, a
    reference implementation of the same page. Wrong document. Scanner PR #10
    made the routine write 60 to 120 progress notes a run instead of a dozen
    and added a `kind` field to every note so the counters would survive the
    density. The check stayed green through all of it, because `kind` is not a
    value it compared and does not appear in scan.html at all. Meanwhile the
    HONESTY GATE ROUNDS tile silently started reading 50 for a five round gate.

    Version two guarded the right document, prompts/scan_routine.md, but proved
    the live half by pattern matching its source. That is a proxy for behaviour,
    and a bad one: transposing two counters kept the pattern intact and passed,
    while renaming one local variable broke the pattern and failed a page that
    was correct.

    So the live half is now proved by EXECUTION. The counter block is cut out of
    site_build.py between two markers and run in Node against probe feeds whose
    right answers are known. Rename anything you like. Restructure the loop.
    What the check asserts is that the numbers come out true.

WHAT IT CHECKS, AND AGAINST WHAT

    from vendor/scanner/scan_routine.md  (THE SPECIFICATION)
      PHASES   the ordered phase list, which drives the ring and the roster
      KINDS    the note kinds, which drive the three live counters

    from vendor/scanner/scan.html  (wiring constants only, NOT a spec)
      FN          the Supabase function base URL
      PUBKEY      the publishable key sent as apikey and bearer
      TS_SITEKEY  the Cloudflare Turnstile sitekey
      endpoints   the /scan-* function names either side actually calls

    internal to the live page, because a contract it agrees with but wires up
    wrong still reaches a visitor broken
      every phase has a ring percentage, in a non decreasing order
      no agent watches for a phase the routine never writes

    the vendored copies themselves
      each file still hashes to the sha256 recorded in vendor/scanner/README.md

    It does NOT diff markup, classes, CSS, fonts, copy, artwork or layout.
    Those are meant to differ and comparing them would make the check noise.

THE KIND RULES, WHICH ARE THE POINT
    Each kind in the spec is fed to the real counter block on its own. Exactly
    one tile must move, or none if the kind is in IGNORED_KINDS. A kind the
    routine writes that no tile answers to is the exact shape of the bug above,
    so it fails until someone either counts it or ignores it on purpose.

EXIT CODES
    0  the two sides agree
    1  drift, or a value could not be found on one side
    2  usage, missing file, or no node to run the counter block with

This script reads only. Fix reported drift by reconciling scan_page() in
scripts/site_build.py, or, when the scanner side genuinely changed, re-vendor
per vendor/scanner/README.md and update both sides in one commit.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REF_HTML = REPO / "vendor" / "scanner" / "scan.html"
REF_SPEC = REPO / "vendor" / "scanner" / "scan_routine.md"
REF_README = REPO / "vendor" / "scanner" / "README.md"
LIVE = REPO / "scripts" / "site_build.py"

HTML_LABEL = "vendor/scanner/scan.html"
SPEC_LABEL = "vendor/scanner/scan_routine.md"
LIVE_LABEL = "scripts/site_build.py scan_page()"

# Kinds the routine writes that the live page deliberately does not count.
# Adding to this list is a decision, which is the whole point of it existing.
IGNORED_KINDS = {"step"}

# The three tiles, in the order the page shows them, keyed by the variable the
# counter block leaves each one in.
TILES = [("nPages", "PAGES READ"), ("nInd", "INDUSTRY CHECKS"), ("nGate", "GATE ROUNDS")]

# An endpoint is a name reached through the function base URL. Scoped this
# tightly on purpose: a prose mention of scan-result in a comment, or an input
# with id="scan-url", is not a call site and must not read as one.
CALLSITE_RE = re.compile(r"FN\s*\+\s*\"/(scan-[a-z][a-z0-9-]*)")


# ---------- readers ----------

def scalar(text, name):
    """The string literal assigned to `name`, or None. Matches both const and
    var styles, double quoted, which is what both sides use."""
    m = re.search(r"\b" + re.escape(name) + r"\s*=\s*\"([^\"]*)\"", text)
    return m.group(1) if m else None


def endpoints(text):
    return sorted(set(CALLSITE_RE.findall(text)))


def spec_phases(text):
    """The ordered phase list from THE PROGRESS FEED. The spec writes it as a
    prose line directly under the `phase` bullet."""
    m = re.search(r"drives the stepper[^\n]*\n\s*([a-z][a-z, ]*[a-z])\s*\n", text)
    return [p.strip() for p in m.group(1).split(",")] if m else None


def spec_kinds(text):
    """The note kinds from THE PROGRESS FEED, as sub bullets under `kind`.
    Hyphens are legal in a kind, so `page-error` reads as one kind and not as
    `page`, which would have quietly counted a new kind as already handled."""
    i = text.find("drives the three live counters")
    if i < 0:
        return None
    out = []
    for line in text[i:].split("\n")[1:]:
        if re.match(r"^[A-Z]", line):        # next section heading, stop
            break
        m = re.match(r"^\s+-\s+`([a-z][a-z0-9-]*)`", line)
        if m:
            out.append(m.group(1))
    return out or None


def live_phases(text):
    m = re.search(r"\bPHASES\s*=\s*\[(.*?)\]", text, re.S)
    return re.findall(r"\"([^\"]+)\"", m.group(1)) if m else None


def live_phase_pct(text):
    """The ring percentages, in source order, as [(phase, pct)]."""
    m = re.search(r"\bPHASE_PCT\s*=\s*\{(.*?)\}", text, re.S)
    if not m:
        return None
    return [(k, int(v)) for k, v in re.findall(r"([a-z][a-z0-9_]*)\s*:\s*(\d+)", m.group(1))]


def live_agent_phases(text):
    """Every phase named in an agent's `on` list, deduped."""
    m = re.search(r"\bAGENTS\s*=\s*\[(.*?)\n\s*\];", text, re.S)
    if not m:
        return None
    out = []
    for lst in re.findall(r"\bon\s*:\s*\[([^\]]*)\]", m.group(1)):
        out.extend(re.findall(r"\"([^\"]+)\"", lst))
    return out or None


def counter_block(text):
    """The counter block, cut out between its markers. This is the code the
    check runs, so it is taken verbatim and never parsed for meaning."""
    m = re.search(r"//\s*sync:counters begin\n(.*?)//\s*sync:counters end", text, re.S)
    return m.group(1) if m else None


def scan_page_src(text):
    """Slice site_build.py down to scan_page(), so a stray match elsewhere in
    the builder can never satisfy or break the check."""
    start = text.find("def scan_page(")
    if start < 0:
        return None
    nxt = re.search(r"\ndef [a-z_]+\(", text[start + 1:])
    return text[start:start + 1 + nxt.start()] if nxt else text[start:]


# ---------- running the real counter block ----------

def note(phase, kind=None, text="a note"):
    n = {"at": "00:00", "phase": phase, "note": text}
    if kind:
        n["kind"] = kind
    return n


def build_probes(kinds):
    """Feeds whose right answers are known, and are known to be DIFFERENT from
    the answers a broken counter would give.

    Every probe uses three distinct totals, so a transposition cannot hide
    behind two tiles that happen to match. The kind probe deliberately pairs
    each kind with the wrong phase, so a page that fell back to counting phases
    reports numbers nothing like the truth rather than numbers close to it.
    """
    probes = [
        ("counts by kind, not by phase",
         [note("critic", "page")] * 3 + [note("render", "search")] * 5
         + [note("footprint", "round", "reading a.com/x")] * 7,
         {"nPages": 3, "nInd": 5, "nGate": 7}),
        ("still reads feeds written before kind existed",
         [note("footprint", None, "reading a.com/p%d" % i) for i in range(4)]
         + [note("footprint", None, "the yard books by phone")] * 2
         + [note("industry", None, "searching")] * 6
         + [note("critic", None, "round verdict")] * 9,
         {"nPages": 4, "nInd": 6, "nGate": 9}),
        ("decides each note on its own, mixed feed",
         [note("footprint", None, "reading a.com/p%d" % i) for i in range(4)]
         + [note("critic", "page")] * 3
         + [note("industry", "search")] * 2
         + [note("critic", "round")] * 8,
         {"nPages": 7, "nInd": 2, "nGate": 8}),
        ("an empty feed is three zeros, never a crash",
         [], {"nPages": 0, "nInd": 0, "nGate": 0}),
    ]
    # One probe per kind the routine writes: feed forty of it and nothing else.
    # Forty, so a tile that answers to it cannot be confused with a tile that
    # happens to hold a small number for another reason.
    for k in kinds or []:
        probes.append(("the `%s` kind, on its own" % k,
                       [note("assemble", k, "a %s note" % k)] * 40, None))
    return probes


# typeof on an undeclared name is safe in JS, which is what lets the harness
# tell "the block renamed its totals" apart from "the block threw". Without
# that split, a rename reports as a runtime crash and sends the reader to look
# for a bug that is not there, which is exactly how the last version of this
# check wasted a morning.
HARNESS = """
'use strict';
const probes = JSON.parse(process.argv[2]);
function count(notes){
%s
  const missing = [];
  if (typeof nPages === 'undefined') { missing.push('nPages'); }
  if (typeof nInd   === 'undefined') { missing.push('nInd'); }
  if (typeof nGate  === 'undefined') { missing.push('nGate'); }
  if (missing.length) { return { missing: missing }; }
  return { nPages: nPages, nInd: nInd, nGate: nGate };
}
const out = [];
for (const p of probes) {
  try { out.push({ ok: true, got: count(p.notes) }); }
  catch (e) { out.push({ ok: false, err: String(e && e.message || e) }); }
}
process.stdout.write(JSON.stringify(out));
"""


def run_counters(block, probes):
    """Run the page's own counter block over each probe. Returns (results, err)."""
    node = shutil.which("node") or shutil.which("nodejs")
    if not node:
        return None, ("no node on PATH, and the counter block is JavaScript.\n"
                      "    This check proves the live counters by running them, not by "
                      "reading them.\n    Install node, or run this where node exists.")
    with tempfile.TemporaryDirectory() as td:
        js = Path(td) / "counters.js"
        js.write_text(HARNESS % block)
        payload = json.dumps([{"notes": n} for _, n, _ in probes])
        try:
            p = subprocess.run([node, str(js), payload],
                               capture_output=True, text=True, timeout=60)
        except Exception as e:
            return None, "could not run node: %s" % e
    if p.returncode != 0:
        return None, ("the counter block does not run on its own.\n    node said: %s\n"
                      "    It has to be self contained: read only `notes`, declare "
                      "everything else." % (p.stderr.strip().splitlines() or ["?"])[0])
    try:
        results = json.loads(p.stdout)
    except Exception:
        return None, "the counter harness returned nothing readable: %r" % p.stdout[:200]
    missing = next((r["got"]["missing"] for r in results
                    if r.get("ok") and "missing" in r["got"]), None)
    if missing:
        return None, ("the counter block no longer leaves its totals where the page "
                      "reads them.\n    not left behind   %s\n"
                      "    Rename freely inside the block, but it has to finish with the "
                      "three tile totals in nPages, nInd and nGate.\n"
                      "    This is a naming contract, not a bug in the counting."
                      % ", ".join(missing))
    return results, None


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


def check_wiring(phases, pct, agent_on, problems):
    """A page can agree with the contract and still wire it up wrong. Adding a
    phase to PHASES and to the routine, and to nothing else, passed every other
    check here while the ring ran backwards on the new phase."""
    if phases is None:
        return
    if pct is None:
        problems.append("PHASE_PCT could not be found in %s.\n"
                        "    It is what turns a phase into a ring percentage." % LIVE_LABEL)
    else:
        table = dict(pct)
        missing = [p for p in phases if p not in table]
        if missing:
            problems.append(
                "A phase has no ring percentage.\n    without a PHASE_PCT entry   %s\n"
                "    pctFor() reads undefined for it, so the ring drops to nothing the "
                "moment the run reaches that phase." % ", ".join(missing))
        extra = [k for k, _ in pct if k not in phases]
        if extra:
            problems.append(
                "PHASE_PCT carries a phase the routine never writes.\n"
                "    dead entries   %s\n"
                "    Harmless today and confusing forever. Drop it, or add the phase to "
                "the contract on both sides." % ", ".join(extra))
        ordered = [table[p] for p in phases if p in table]
        backwards = [(phases[i], ordered[i - 1], ordered[i])
                     for i in range(1, len(ordered)) if ordered[i] < ordered[i - 1]]
        if backwards:
            problems.append(
                "The ring runs backwards.\n    %s\n"
                "    PHASE_PCT has to climb in PHASES order, because the ring only ever "
                "moves forward for a visitor watching it."
                % "; ".join("at %s it drops from %d to %d" % b for b in backwards))
    if agent_on is None:
        problems.append("The AGENTS roster could not be found in %s." % LIVE_LABEL)
    else:
        orphan = [p for p in agent_on if p not in phases]
        if orphan:
            problems.append(
                "An agent watches for a phase the routine never writes.\n"
                "    never lights up   %s\n"
                "    That row sits grey for every scan, which reads as an agent that did "
                "not run." % ", ".join(sorted(set(orphan))))


def check_counters(probes, results, problems):
    """The heart of it. Each probe carries either an exact expectation or, for
    a bare kind probe, the rule that exactly one tile must answer to it."""
    for (label, notes, want), got in zip(probes, results):
        if not got.get("ok"):
            problems.append(
                "The live counters threw on a feed the routine can write.\n"
                "    probe   %s\n    threw   %s\n"
                "    paint() runs this on every poll, so a throw here stops the whole "
                "waiting room." % (label, got.get("err")))
            continue
        vals = got["got"]
        if want is not None:
            if vals != want:
                lines = "\n".join(
                    "    %-18s expected %-4d got %d" % (name, want[var], vals[var])
                    for var, name in TILES if want[var] != vals[var])
                problems.append(
                    "The live counters do not report the truth.\n    probe   %s\n%s\n"
                    "    These are the numbers a visitor reads off the tiles, so a wrong "
                    "one is the page overstating or understating the work."
                    % (label, lines))
            continue
        # A bare kind probe. label reads "the `x` kind, on its own".
        kind = label.split("`")[1]
        moved = [name for var, name in TILES if vals[var]]
        if kind in IGNORED_KINDS:
            if moved:
                problems.append(
                    "A kind listed as ignored is being counted anyway.\n"
                    "    kind    %s\n    moves   %s\n"
                    "    IGNORED_KINDS in this script says it should move nothing. Either "
                    "the page changed on purpose, in which case take it off that list, or "
                    "a tile is counting the wrong thing." % (kind, ", ".join(moved)))
            continue
        if not moved:
            problems.append(
                "The routine writes a kind no tile answers to.\n"
                "    kind    %s\n"
                "    Count it in scan_page() or add it to IGNORED_KINDS in this script, "
                "on purpose.\n"
                "    This is the exact shape of the bug that shipped when the feed went "
                "dense, so it fails loudly." % kind)
        elif len(moved) > 1:
            problems.append(
                "One kind moves more than one tile.\n    kind    %s\n    moves   %s\n"
                "    Each tile counts one kind, or the same work is reported twice."
                % (kind, ", ".join(moved)))


def check_vendored(problems):
    """The vendored copies are a snapshot, and a snapshot nobody can trust is
    worse than none. This does not prove they match upstream today, only that
    nobody has edited them here since they were recorded. Use --fetch for the
    upstream question."""
    try:
        readme = REF_README.read_text()
    except OSError:
        problems.append("vendor/scanner/README.md is missing, so the recorded hashes "
                        "cannot be checked.")
        return
    for path, label in ((REF_SPEC, SPEC_LABEL), (REF_HTML, HTML_LABEL)):
        want = None
        # Each file gets its own section, so read the sha256 row after its heading.
        i = readme.find("## " + path.name)
        if i >= 0:
            m = re.search(r"\|\s*sha256\s*\|\s*`([0-9a-f]{64})`\s*\|", readme[i:])
            want = m.group(1) if m else None
        if not want:
            problems.append(
                "%s has no sha256 recorded in vendor/scanner/README.md.\n"
                "    Without it nobody can tell a faithful copy from an edited one."
                % label)
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != want:
            problems.append(
                "%s does not match the hash recorded for it.\n"
                "    README says   %s\n    the file is   %s\n"
                "    A vendored copy is a snapshot of another repo, not a file to edit. "
                "Re-vendor per vendor/scanner/README.md and update the table in the same "
                "commit." % (label, want, got))


def check_upstream(problems, notes):
    """Optional. Answers the one question the hashes cannot: is the snapshot
    still what that repo has today. Needs read access to a private repo, so it
    is off by default and says so plainly when it cannot look."""
    import urllib.error
    import urllib.request
    import os
    # SCANNER_RAW_BASE exists so this path can be pointed at a local checkout
    # and actually tested, rather than being the one branch nobody ever proves.
    base = os.environ.get(
        "SCANNER_RAW_BASE",
        "https://raw.githubusercontent.com/Talonsturgill/alaska-ai-scanner/main/")
    token = os.environ.get("SCANNER_REPO_TOKEN") or os.environ.get("GH_TOKEN")
    for path, label, remote in ((REF_SPEC, SPEC_LABEL, "prompts/scan_routine.md"),
                                (REF_HTML, HTML_LABEL, "web/scan.html")):
        req = urllib.request.Request(base + remote)
        if token:
            req.add_header("Authorization", "Bearer " + token)
        try:
            body = urllib.request.urlopen(req, timeout=30).read()
        except (urllib.error.URLError, OSError) as e:
            notes.append("could not read %s upstream (%s). The repo is private, so this "
                         "needs SCANNER_REPO_TOKEN or GH_TOKEN with read access."
                         % (remote, getattr(e, "code", None) or type(e).__name__))
            continue
        if hashlib.sha256(body).hexdigest() != hashlib.sha256(path.read_bytes()).hexdigest():
            problems.append(
                "%s is stale.\n    Our copy differs from %s on main today.\n"
                "    Re-vendor per vendor/scanner/README.md and reconcile whatever "
                "changed, in one commit." % (label, remote))
        else:
            notes.append("%s matches upstream main" % label)


def main():
    ap = argparse.ArgumentParser(
        description="Verify the live scanner page still agrees with the "
                    "routine contract it depends on.")
    ap.add_argument("--spec", default=str(REF_SPEC), help="vendored scan_routine.md")
    ap.add_argument("--ref", default=str(REF_HTML), help="vendored reference page")
    ap.add_argument("--live", default=str(LIVE), help="the site builder")
    ap.add_argument("--fetch", action="store_true",
                    help="also ask GitHub whether the vendored copies are still "
                         "current. Needs SCANNER_REPO_TOKEN or GH_TOKEN.")
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

    block = counter_block(live_txt)
    if block is None:
        print("scanner_sync_check: no sync:counters block in %s" % LIVE_LABEL, file=sys.stderr)
        print("The counters are proved by running them, so they have to be findable.",
              file=sys.stderr)
        print("Restore the // sync:counters begin and // sync:counters end markers "
              "around the counting loop in paint().", file=sys.stderr)
        return 2

    problems, notes = [], []

    # Read each value once. The PASS block prints the same four things the
    # comparisons just checked, and re-extracting them there meant the report
    # could, in principle, print something other than what was compared.
    wiring = [
        ("The function base URL (FN)", "FN", "function base URL",
         "Every request from the page goes to this host, so a stale one "
         "means the page talks to nothing."),
        ("The publishable key (PUBKEY)", "PUBKEY", "publishable key",
         "It is sent as both apikey and the bearer token, so a stale one "
         "means every call comes back 401."),
        ("The Turnstile sitekey (TS_SITEKEY)", "TS_SITEKEY", "turnstile sitekey",
         "The gatekeeper requires a token whenever the matching secret is "
         "set server-side, so a stale sitekey means nobody can start a scan."),
    ]
    ref_wiring = {}
    for title, name, label, hint in wiring:
        ref_wiring[label] = scalar(ref_txt, name)
        compare(title, ref_wiring[label], HTML_LABEL, scalar(live_txt, name),
                problems, hint)

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

    phases, spec_ph = live_phases(live_txt), spec_phases(spec_txt)
    check_phases(spec_ph, phases, problems)
    check_wiring(phases, live_phase_pct(live_txt), live_agent_phases(live_txt), problems)

    kinds_ref = spec_kinds(spec_txt)
    if kinds_ref is None:
        problems.append(
            "The note kinds could not be found in %s.\n"
            "    They drive the three live counters, so this check is blind "
            "without them." % SPEC_LABEL)
    probes = build_probes(kinds_ref)
    results, err = run_counters(block, probes)
    if err:
        print("scanner_sync_check: %s" % err, file=sys.stderr)
        return 2
    check_counters(probes, results, problems)

    check_vendored(problems)
    if args.fetch:
        check_upstream(problems, notes)

    if not problems:
        print("scanner_sync_check: PASS")
        print("  spec        %s" % SPEC_LABEL)
        print("  wiring      %s" % HTML_LABEL)
        for _, _, label, _ in wiring:
            print("  %-19s %s" % (label, ref_wiring[label]))
        print("  endpoints (%d)       %s" % (len(ref_ep), ", ".join(ref_ep)))
        ph = spec_ph or []
        print("  phases (%d)          %s" % (len(ph), ", ".join(ph)))
        print("  kinds (%d)           %s" % (len(kinds_ref or []), ", ".join(kinds_ref or [])))
        print("  ignored (%d)         %s" % (len(IGNORED_KINDS), ", ".join(sorted(IGNORED_KINDS))))
        print("  counter probes (%d)  run against the page's own block, all true"
              % len(probes))
        for n in notes:
            print("  note        %s" % n)
        print("  markup, CSS and copy are NOT compared, the two pages are "
              "meant to look different")
        return 0

    print("scanner_sync_check: FAIL -- %d contract mismatch(es) between the "
          "live scanner page and the routine it serves:\n" % len(problems))
    for i, p in enumerate(problems, 1):
        print("  %d. %s\n" % (i, p))
    for n in notes:
        print("  note: %s" % n)
    print("Fix by reconciling scan_page() in scripts/site_build.py,")
    print("then rebuild with  python scripts/site_build.py --date <YYYY-MM-DD> --out docs")
    print("If the SCANNER side changed, re-vendor per vendor/scanner/README.md")
    print("and update both sides in one commit.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
