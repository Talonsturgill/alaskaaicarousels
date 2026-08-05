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
# Substance, not a fixed sentence. The copy is allowed to be rewritten; what
# it may never do is claim the model retrains itself or drop the limit.
REQUIRED = [
    ("estimate", "the demand figure called an estimate"),
    ("not reported daily", "the disclosure of what nothing reports daily"),
    ("enstar realtime sendout", "sendout named in that disclosure"),
    ("verdict", "the no-verdict statement"),
]

OVERCLAIMS = [
    "our ai", "learns on its own", "self-improving", "machine learning",
    "trains itself", "fine-tunes itself", "gets smarter", "continuously trained",
    "learns automatically", "retrains",
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


PEAK_ON_PAGE = (r'gw-num">\s*(-?[\d.]+)\s*</div>\s*<div class="gw-lab">'
                r'\s*MMcf/d modeled peak ahead')


def stale_model_output(page_html, figs, model):
    """Whether the peak PRINTED ON THE PAGE disagrees with the published formula.

    Each record stamps the model that produced its numbers, so for a day after
    every refit the ledger holds a modeled peak built on the old coefficients.
    The page recomputes model output from the record's measured inputs for
    exactly that reason, and this is what proves it did.

    It reads the rendered HTML, which the first version of this did not. That
    one took the peak out of figures() and compared it against the same formula
    applied to the same inputs by the same model, so it was the identity
    check gc.demand(h, m) == gc.demand(h, m) wearing a costume. Moving the
    model +7 MMcf/d left figures at 111 and the shipped page at 104 and it
    still returned None. A gate that reads its answer from the thing it is
    checking against is not a gate.
    """
    hdd = figs.get("peak_forecast_hdd")
    if hdd is None:
        return None
    m = re.search(PEAK_ON_PAGE, page_html)
    if not m:
        return "no modeled peak found on the page to check"
    shown, want = float(m.group(1)), gw.gc.demand(hdd, model)
    if shown == want:
        return None
    return (f"page prints {m.group(1)}, the published formula on "
            f"{hdd} degree days gives {want}")


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

    claimed = [w for w in OVERCLAIMS if w in text.lower()]
    (ok if not claimed else bad)("no training the model does not do",
                                 ", ".join(claimed) or "none")

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

    drift = stale_model_output(page, figs, model)
    (ok if not drift else bad)(
        "a reader can reproduce the modeled peak from the published formula",
        drift or f"{figs.get('peak_modeled_demand_mmcfd')} MMcf/d "
                 f"from model {model['version']}")

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
        figs, model, ["CC BY 4.0", gw.SCHEMA_VERSION], series))
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

REFERENCE_META = {
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "license_label": "CC BY 4.0",
    "attribution": "Alaska AI",
    "publisher": "Alaska AI",
    "spatial_coverage": "Alaska",
    "docket_item_id": "enstar-cook-inlet-gas-storage",
}


def render_reference(out_dir, today=None):
    """A correct page and feed, built here, for the self-test to work against.

    Built from gaswatch_build rather than from site_build, so it needs no
    Pillow, no fonts and no run artifacts, and it cannot be stale by
    construction. It is a <main> wrapper around the same page_body the site
    ships, which is all check_page scopes to anyway.
    """
    today = today or date.today()
    series = gw.load_series()
    model = gw.gc.load_model(gw.MODEL_CONFIG)
    body = gw.page_body(today, "https://alaskaaihq.com", series, model,
                        REFERENCE_META, prefix="../")
    os.makedirs(os.path.join(out_dir, "gas-watch"), exist_ok=True)
    with open(os.path.join(out_dir, "gas-watch", "index.html"), "w",
              encoding="utf-8") as fh:
        fh.write(f"<main>{body}</main>")
    with open(os.path.join(out_dir, "gas-watch.json"), "w", encoding="utf-8") as fh:
        json.dump(gw.feed(series, model, "https://alaskaaihq.com", today,
                          REFERENCE_META), fh)
    return out_dir


def self_test():
    """The checker has to be able to go red, or it certifies nothing."""
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    import tempfile

    # HERMETIC. This used to open docs/ and assert the COMMITTED page passed,
    # which made a gate about the checker into an assertion about the checkout.
    # It ran third in gaswatch.yml, before the collector, and it exits 1, so a
    # docs/ that lagged the model took the whole job down and the day's CINGSA
    # reading with it. gaswatch-eia.yml arms exactly that every time it refits,
    # since it commits a new model and does not rebuild the page. Measured:
    # move base_mmcfd +7 without rebuilding and this self-test exits 1.
    #
    # So it renders its own page from the same library the site uses and tests
    # the checker against that. Whether the page in docs/ is current is a real
    # question, and it is the job of `--out docs`, which exits 2 and cannot
    # abort anything.
    good = render_reference(tempfile.mkdtemp())
    rows, verdict = check_page(good)
    check("a freshly built page passes", verdict in ("PASS", "WARN"),
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
        ("a claim that the model trains itself",
         page.replace("</main>", "<p>The model fine-tunes itself daily.</p></main>")),
        ("the not-reported-daily disclosure removed",
         page.replace("not reported daily", "all fully reported")),
        ("a numeral nothing computed",
         page.replace("</main>", "<p>Storage sits at 87.3 percent.</p></main>")),
    ]
    for label, mutated in breakages:
        check(f"goes red on {label}", with_page(mutated) == "FAIL")

    live = gw.gc.load_model(gw.MODEL_CONFIG)
    figs = gw.figures(gw.load_series(), live)
    check("a freshly built page's peak reproduces from its formula",
          stale_model_output(page, figs, live) is None,
          stale_model_output(page, figs, live) or "reproduces")
    # The case the identity-check version could not see. The page is left
    # alone and the MODEL moves under it, which is what a refit does.
    moved = dict(live, base_mmcfd=live["base_mmcfd"] + 7.0)
    check("a page left behind by a refit is caught",
          stale_model_output(page, figs, moved) is not None,
          stale_model_output(page, moved and figs, moved) or "MISSED IT")
    check("a page with no peak on it is reported, not passed",
          stale_model_output("<main>nothing here</main>", figs, live) is not None)
    check("it says nothing when the record carries no forecast",
          stale_model_output(page, {}, live) is None)

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
