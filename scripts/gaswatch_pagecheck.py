#!/usr/bin/env python3
"""gaswatch_pagecheck.py, the daily once over of the published Gas Watch page.

The carousel routine rebuilds docs/ every run and its Phase 12 engineer can
edit any script, so the page can break on a day nobody was looking at it. The
maintainer is not going to open it each morning, which is the whole reason this
exists. It gives the routine an objective read of whether the page is sound
before it uses its own eyes on the parts a checker cannot judge.

READ ONLY. It asserts, it never writes, and it never touches the ledgers, the
model, or anything that produces a number. Its job is to notice, not to repair.

It also never fails a carousel run. CLAUDE.md keeps the collector independent of
the routine precisely so neither can hold the other hostage, so a gas problem
here is reported and exits 2, which the routine records without aborting. Only a
genuinely broken CHECK exits 1.

Run:
  python3 scripts/gaswatch_pagecheck.py --self-test   # hermetic, red cases
  python3 scripts/gaswatch_pagecheck.py               # check docs/
  python3 scripts/gaswatch_pagecheck.py --out out/site --json
"""

import argparse
import html as _html
import json
import os
import re
import sys
from datetime import date, datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gaswatch_build as gw  # noqa: E402

# Freshness. The collector runs twice a day, so a published reading older than
# this means collection or the rebuild has been failing quietly.
STALE_DAYS = 3

# Things that must never appear in visible copy. Template leakage first,
# because an f-string that lost its braces ships a literal placeholder and
# nothing else would notice.
FORBIDDEN = [
    (r"\{f\[", "an unrendered f-string placeholder"),
    (r"\bNone\b", "a Python None"),
    (r"\bnan\b", "a NaN"),
    (r"\bundefined\b", "an undefined"),
    (r"\bNaN\b", "a NaN"),
    (r"\{count\(|\{stat\(|\{gauge\(", "an unrendered template call"),
]

# The page's promises. If any of these stops being true the page has drifted
# from what CLAUDE.md says it is allowed to be.
REQUIRED = [
    ("nothing here learns on its own", "the no-training statement"),
    ("sendout is not published", "the limit more data cannot fix"),
    ("verdict", "the no-verdict statement"),
]

VERDICT_WORDS = [
    "will run out", "all clear", "we will make it", "is safe", "is not safe",
    "blackout", "shortfall is coming", "supply is adequate",
]


def main_region(page_html):
    """Just this page's own copy.

    The shared nav, footer and head belong to site_build and carry their own
    numerals, including the footer's coordinates. Linting the whole document
    flagged 61, 13, 149 and 54 from "61 degrees 13 minutes N" as invented
    figures. site_build lints the page BODY, so this checker must scope the
    same way or it reports the site chrome as a gas watch defect.
    """
    m = re.search(r"(?s)<main[^>]*>(.*?)</main>", page_html)
    return m.group(1) if m else page_html


def visible_text(page_html):
    txt = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", page_html)
    txt = re.sub(r"(?s)<svg.*?</svg>", " ", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return _html.unescape(txt)


def check_page(out_dir, today=None):
    """Return (rows, verdict). Each row is (status, label, detail)."""
    today = today or date.today()
    rows = []

    def ok(label, detail=""):
        rows.append(("PASS", label, detail))

    def bad(label, detail=""):
        rows.append(("FAIL", label, detail))

    def warn(label, detail=""):
        rows.append(("WARN", label, detail))

    page_path = os.path.join(out_dir, "gas-watch", "index.html")
    feed_path = os.path.join(out_dir, "gas-watch.json")
    if not os.path.exists(page_path):
        bad("the page exists", f"{page_path} missing")
        return rows, "FAIL"
    page = open(page_path, encoding="utf-8").read()
    ok("the page exists", f"{len(page) // 1024} KB")

    body = main_region(page)
    text = visible_text(body)

    # Template leakage and machine spill.
    spill = [why for pat, why in FORBIDDEN if re.search(pat, text)]
    (ok if not spill else bad)("no machine spill in visible copy",
                               ", ".join(spill) or "clean")

    # The page's standing promises.
    missing = [why for phrase, why in REQUIRED if phrase not in text.lower()]
    (ok if not missing else bad)("the page keeps its promises",
                                 ", ".join(missing) or "all present")

    said = [w for w in VERDICT_WORDS if w in text.lower()]
    (ok if not said else bad)("no safety verdict", ", ".join(said) or "none")

    # The series behind it, and whether the page agrees with it.
    series = gw.load_series()
    model = gw.gc.load_model(gw.MODEL_CONFIG)
    verified = [r for r in series if r.get("verified")]
    figs = gw.figures(series, model)

    if not verified:
        warn("a verified reading exists",
             f"{len(series)} record(s), none verified")
    else:
        ok("a verified reading exists", f"{len(verified)} of {len(series)}")
        age = (today - date.fromisoformat(figs["as_of"])).days
        (ok if age <= STALE_DAYS else warn)(
            "the published reading is current",
            f"read {figs['as_of']}, {age} day(s) old")
        # The headline figure has to be ON the page, not merely computed.
        (ok if str(figs["inventory_pct_of_design"]) in text else bad)(
            "the headline figure reaches the page",
            f"{figs['inventory_pct_of_design']} percent of design")

    gaps = gw.continuity(series)
    (ok if not gaps else warn)(
        "no gap in the series",
        f"{len(gaps)} missing, first {gaps[0]}" if gaps else "continuous")

    # The chart is a claim about having a trend. It must appear when there is
    # one and stay away when there is not.
    has_chart = '<div class="gw-chart"' in body
    should = len([r for r in verified if (r.get("cingsa") or {}).get("inventory_mcf")]) >= 2
    (ok if has_chart == should else bad)(
        "the chart matches the record",
        f"chart {'present' if has_chart else 'absent'}, "
        f"{len(verified)} verified day(s)")

    # Nothing invented, checked against the same lint the build runs.
    planted = gw.numeral_lint(body, gw.allowed_numerals(
        figs, model, ["CC BY 4.0", gw.SCHEMA_VERSION]))
    (ok if not planted else bad)("every numeral traces to a computation",
                                 ", ".join(sorted(set(planted))[:6]) or "clean")

    # The feed and the page must not disagree.
    if not os.path.exists(feed_path):
        bad("the feed exists", f"{feed_path} missing")
    else:
        try:
            feed = json.loads(open(feed_path, encoding="utf-8").read())
        except json.JSONDecodeError as exc:
            bad("the feed parses", str(exc)[:80])
        else:
            ok("the feed parses", f"{feed.get('count')} record(s)")
            (ok if feed.get("count") == len(series) else bad)(
                "the feed and the ledger agree",
                f"feed {feed.get('count')}, ledger {len(series)}")
            (ok if feed.get("warning") else bad)(
                "the feed carries its warning",
                "present" if feed.get("warning") else "missing")

    fails = [r for r in rows if r[0] == "FAIL"]
    warns = [r for r in rows if r[0] == "WARN"]
    return rows, "FAIL" if fails else ("WARN" if warns else "PASS")


def render(rows, verdict):
    for status, label, detail in rows:
        print(f"  [{status}] {label}" + (f"  {detail}" if detail else ""))
    print(f"\ngas watch page check: {verdict}")


# ------------------------------------------------------------------ self test

def self_test():
    """The checker has to be able to go red, or it certifies nothing."""
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    import tempfile
    good = os.path.join(REPO, "docs")
    rows, verdict = check_page(good)
    check("the shipped page passes", verdict in ("PASS", "WARN"),
          f"verdict {verdict}, " +
          ", ".join(f"{s} {l}" for s, l, _ in rows if s == "FAIL") or "no fails")

    page = open(os.path.join(good, "gas-watch", "index.html"), encoding="utf-8").read()
    feed = open(os.path.join(good, "gas-watch.json"), encoding="utf-8").read()

    def with_page(mutated):
        td = tempfile.mkdtemp()
        os.makedirs(os.path.join(td, "gas-watch"))
        open(os.path.join(td, "gas-watch", "index.html"), "w").write(mutated)
        open(os.path.join(td, "gas-watch.json"), "w").write(feed)
        return check_page(td)[1]

    breakages = [
        ("an unrendered f-string placeholder",
         page.replace("</main>", '<p>{f["inventory_bcf"]} Bcf</p></main>')),
        ("a Python None in visible copy",
         page.replace("</main>", "<p>Storage None Bcf</p></main>")),
        ("a safety verdict",
         page.replace("</main>", "<p>Southcentral is safe, supply is adequate.</p></main>")),
        ("the no-training statement removed",
         page.replace("Nothing here learns on its own", "This model improves itself")),
        ("the sendout limit removed",
         page.replace("sendout is not published", "sendout is available")),
        ("a numeral nothing computed",
         page.replace("</main>", "<p>Storage sits at 87.3 percent.</p></main>")),
    ]
    for label, mutated in breakages:
        check(f"goes red on {label}", with_page(mutated) == "FAIL")

    td = tempfile.mkdtemp()
    check("goes red when the page is missing", check_page(td)[1] == "FAIL")

    os.makedirs(os.path.join(td, "gas-watch"))
    open(os.path.join(td, "gas-watch", "index.html"), "w").write(page)
    open(os.path.join(td, "gas-watch.json"), "w").write("{not json")
    check("goes red on an unparseable feed", check_page(td)[1] == "FAIL")

    print()
    if not ok[0]:
        print("self-test FAILED")
        return 1
    print("self-test clean")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Daily once over of the Gas Watch page")
    ap.add_argument("--out", default=os.path.join(REPO, "docs"),
                    help="built site directory, default docs/")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    rows, verdict = check_page(args.out)
    if args.json:
        print(json.dumps({"verdict": verdict,
                          "rows": [{"status": s, "check": l, "detail": d}
                                   for s, l, d in rows]}, indent=2))
    else:
        render(rows, verdict)
    # 0 clean, 2 needs attention. Never 1 for a page problem, because a gas
    # watch fault must not abort a carousel run.
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
