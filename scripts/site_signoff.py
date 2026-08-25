#!/usr/bin/env python3
"""site_signoff.py, the daily once over of EVERY published page.

WHY THIS EXISTS. gaswatch_pagecheck.py reads one page deeply and there are
seventy three. The rest were signed off by the build that wrote them, and a
build gate only ever proves the BUILDER was right at the moment it ran. What is
actually on alaskaaihq.com is whatever the last successful build left there,
and the two stop agreeing the moment a collector commits a number and nothing
rebuilds the page that prints it. That is not a hypothetical: it is what the
cron jobs do by design, every month, on their own clock.

So this asks a different question from every other gate here. Not "is the code
correct" but "is the thing a reader will load today still true". It reads the
built directory, never the builder.

WHAT IT CHECKS THAT NOTHING ELSE DOES.

  Ledger to page agreement. Every number a cron job writes has exactly one page
  that publishes it, and this asserts the CURRENT value is on that page. A
  monthly EIA release that lands without a rebuild leaves last month's price
  published under this month's ledger, which no build gate can see because the
  build was fine and simply never happened.

  Freshness against a cadence. Each ledger declares how often it should move.
  A daily series three days cold means collection has been failing quietly.

  Dead links and dead sitemap entries. A build validates the page it writes,
  not the pages it points at. A renamed URL leaves a link that was correct when
  it was written.

  The published bytes, not the builder's output. The house voice gates run at
  build time; this runs the same rules against what shipped, so docs/ lagging
  its own builder is visible rather than invisible.

IT REPORTS SO THE RUN CAN REPAIR. Every check carries its own remedy, printed
under any failure and returned in --json as `fix`, because a checker that hands
back a list of complaints has moved the work rather than done it. The routine's
job in Phase 3.6 is to FIX what this finds and then report what is left, not to
copy the complaints into an email.

Two categories are marked REPORT and must not be fixed by a run: a collector
that has stopped running, whose ledger is cron written and would be corrupted
by a run writing into it, and a surface another repo owns. Everything else is
presentation or a stale build, and both are a run's to repair.

CONTRACT, the same one gaswatch_pagecheck signs. This SCRIPT is read only, it
asserts and never repairs; the repairing is the routine's. Exit 0 clean, exit 2
needs attention, exit 1 ONLY if the checker itself broke. A site problem must
never abort a carousel run, because the routine that runs this is also the
thing that ships the day's deck and one must not hold the other hostage.

docs/videos/ IS NOT CHECKED. CLAUDE.md makes it a hard guard: the page is a
static passthrough and the JSON beside it is owned by another repo. This
confirms both are present and reads neither.

Run:
  python3 scripts/site_signoff.py --self-test   # hermetic, red cases
  python3 scripts/site_signoff.py               # sign off docs/
  python3 scripts/site_signoff.py --out /tmp/site --json
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

# A page whose body is this small never rendered. Measured against the smallest
# real page on the site, which is the 404 at about 9 KB.
MIN_PAGE_BYTES = 3000

# Template leakage and machine spill. An f-string that lost its braces ships a
# literal placeholder, and nothing downstream would ever notice.
SPILL = [
    (r"\{[a-z_]+\[", "an unrendered f-string placeholder"),
    (r"\{esc\(|\{len\(|\{count\(", "an unrendered template call"),
    (r"\bNaN\b|\bnan\b", "a NaN"),
    (r"\bundefined\b", "an undefined"),
    (r"\[object Object\]", "a stringified JS object"),
]

# "None" IS ALSO AN ENGLISH WORD, and a flat \bNone\b called two correct pages
# broken on the first run. The privacy page says "No cookies. None are set" and
# the power beat says "None are open for public comment right now", which are
# both exactly the sentence a careful writer wants.
#
# A leaked Python None never starts a sentence. It lands mid clause, beside the
# words that were supposed to surround the value, which is a difference this can
# actually test: what sits before it. After a full stop it is English; after a
# letter, a digit or an opening bracket it is a value that failed to render.
LEAK_BEFORE = re.compile(r"[A-Za-z0-9,(/\-]$")


def leaked_none(text):
    """Occurrences of None that are values rather than the English word."""
    out = []
    for m in re.finditer(r"\bNone\b", text):
        before = text[:m.start()].rstrip()
        if before and LEAK_BEFORE.search(before):
            out.append(re.sub(r"\s+", " ", text[max(0, m.start() - 40):
                                               m.end() + 20]).strip())
    return out

# House voice, checked against what SHIPPED rather than what was built. The
# build gates these too, and that is the point: if these two ever disagree, the
# published directory is behind its own builder.
VOICE = [
    ("—", "an em dash"),
    ("–", "an en dash"),
    (r"\bcannot\b", "'cannot' where the house writes can't"),
]

# NOT THIS SITE'S TO SIGN OFF. Two directories live under docs/ and are written
# by something else, and site_fresh_check.py already draws the same line: they
# are reported and ignored, because gating a surface you neither generate nor
# may edit produces a red light nobody is allowed to fix.
#
#   videos/           a static passthrough plus JSON owned by alaska-ai-weekly.
#                     CLAUDE.md makes it a HARD GUARD. Confirmed present, read
#                     never.
#   awesomeproposal/  client field studies, published by their own process.
#
# The count of what was skipped is printed, so the exclusion is a stated fact
# rather than a silent hole.
FOREIGN = ("videos", "awesomeproposal")

# Shipped run copy is exempt from the voice rules, on the deck page and in the
# cards that excerpt it, for the reason CLAUDE.md gives: published artifacts are
# not rewritten and a quoted source wrote however it wrote.
# A file rather than a page. Extensions only, so a docket item at /docket/id/
# is never mistaken for one.
ASSET = re.compile(r"\.(woff2?|ttf|otf|png|jpe?g|webp|gif|svg|ico|css|js|mjs|"
                   r"json|xml|txt|pdf|zip|mp4|webm)$", re.I)

DECK_CARD = re.compile(r'(?s)<a class="deck".*?</a>')
DECK_PAGE = re.compile(r"archive/\d{4}-\d{2}-\d{2}/index\.html$")


def visible(page_html, drop_svg=True):
    """The visible PROSE of a page.

    A URL IS AN ADDRESS, NOT PROSE (2026-08-25). The sources page prints each
    citation's URL as visible text, and one of them is the ADN's own slug for
    an op-ed titled "public safety cannot come at the expense of civil
    liberties". Read as house copy it fails the voice rule on a string this
    repo cannot change: rewriting a third party's URL breaks the citation, and
    printing it is the whole point, because a reader can go and check. Only
    http(s) runs are dropped, so every sentence anyone here wrote is still
    read, including the prose either side of the link. site_build.py's
    contraction_gate carries the same exclusion for the same reason; these two
    are meant to agree, and that is why the rule is spelled out in both.
    """
    txt = DECK_CARD.sub(" ", page_html)
    txt = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", txt)
    if drop_svg:
        txt = re.sub(r"(?s)<svg.*?</svg>", " ", txt)
    txt = re.sub(r"(?s)<!--.*?-->", " ", txt)
    txt = _html.unescape(re.sub(r"<[^>]+>", " ", txt))
    return re.sub(r"https?://\S+", " ", txt)


# ------------------------------------------------------- the published numbers

def _gaswatch(out_dir):
    """Newest verified reading, as the page writes it."""
    import gaswatch_build as gw
    series = gw.load_series()
    verified = [r for r in series if r.get("verified")]
    if not verified:
        return None, []
    newest = verified[-1]["date"]
    return newest, [("the newest reading", gw.long_date(newest))]


def _power(out_dir):
    import power_panel as pw
    d = pw.load()
    if not d:
        return None, []
    res = (d.get("sectors") or {}).get("residential") or {}
    return d.get("generated", "")[:10], [
        ("the latest month", res.get("latest_label", "")),
        ("the household price", f"{res['latest']:.2f}" if res.get("latest") else ""),
    ]


def _power_utility(out_dir):
    import power_panel as pw
    d = pw.load_utilities()
    rows = [u for u in ((d or {}).get("utilities") or [])
            if u.get("sectors", {}).get("residential", {}).get("cents_per_kwh")]
    if not rows:
        return None, []
    top = rows[0]["sectors"]["residential"]
    return d.get("generated", "")[:10], [
        ("the data year", str(d.get("data_year", ""))),
        (f"the price for {rows[0]['name']}", f"{top['cents_per_kwh']:.2f}"),
    ]


def _docket(out_dir):
    try:
        items = json.loads(open(os.path.join(REPO, "ledger", "docket.json"),
                                encoding="utf-8").read())
    except Exception:
        return None, []
    rows = items.get("items") if isinstance(items, dict) else items
    rows = [r for r in (rows or []) if isinstance(r, dict) and r.get("id")]
    if not rows:
        return None, []
    dates = sorted(r.get("last_updated", "") for r in rows if r.get("last_updated"))
    return (dates[-1] if dates else None), [
        ("the tracked decision count", f"{len(rows):02d}")]


# Every number cron writes, the page that publishes it, and how long it may go
# without moving before something is wrong. A ledger with no entry here is a
# number nobody is watching, which is the state this file exists to end.
PUBLISHED = [
    ("ledger/gaswatch.jsonl", "gas-watch/index.html", 3, _gaswatch),
    ("ledger/power.json", "gas-watch/index.html", 45, _power),
    ("ledger/power_utility.json", "gas-watch/index.html", 40, _power_utility),
    ("ledger/docket.json", "docket/index.html", 21, _docket),
]

# Written by cron, read by a run, never published as a page. Freshness only.
QUEUES = [("ledger/watch.json", 3, "generated")]


# --------------------------------------------------------------------- checks

def sitemap_urls(out_dir):
    path = os.path.join(out_dir, "sitemap.xml")
    if not os.path.exists(path):
        return []
    return re.findall(r"<loc>([^<]+)</loc>",
                      open(path, encoding="utf-8").read())


def page_files(out_dir):
    """Every html page the site wrote, relative to out_dir."""
    out, skipped = [], 0
    for root, dirs, files in os.walk(out_dir):
        if root == out_dir:
            skipped = sum(1 for d in dirs if d in FOREIGN)
            dirs[:] = [d for d in dirs if d not in FOREIGN]
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(root, f), out_dir))
    return sorted(out), skipped


def internal_links(page_html):
    """Relative hrefs worth resolving. Anchors, mail and absolute URLs are
    somebody else's problem and a fragment is not a file.

    Script and style go first. A page that builds its own links in JS carries
    href="' + esc(row.id) + '" in a string, and reading that as markup reported
    five dead links that no reader could ever click."""
    markup = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", page_html)
    for href in re.findall(r'href="([^"]+)"', markup):
        if href.startswith(("http://", "https://", "//", "mailto:", "tel:", "#",
                            "data:", "javascript:")):
            continue
        yield href.split("#")[0].split("?")[0]


def resolve(out_dir, rel_page, href):
    base = os.path.dirname(os.path.join(out_dir, rel_page))
    target = os.path.normpath(os.path.join(base, href)) if not href.startswith("/") \
        else os.path.normpath(os.path.join(out_dir, href.lstrip("/")))
    if os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return target


def age_days(stamp, today):
    if not stamp:
        return None
    try:
        return (today - date.fromisoformat(str(stamp)[:10])).days
    except ValueError:
        return None


def check_site(out_dir, today=None):
    """Return (rows, verdict). Each row is (status, label, detail)."""
    today = today or date.today()
    rows = []

    def ok(label, detail=""):
        rows.append(("PASS", label, detail))

    def bad(label, detail=""):
        rows.append(("FAIL", label, detail))

    def warn(label, detail=""):
        rows.append(("WARN", label, detail))

    if not os.path.isdir(out_dir):
        bad("the built site exists", f"{out_dir} missing")
        return rows, "FAIL"

    pages, foreign = page_files(out_dir)
    if not pages:
        bad("the built site has pages", f"no html under {out_dir}")
        return rows, "FAIL"
    ok("every page is on disk",
       f"{len(pages)} pages" + (f", {foreign} foreign director"
                                f"{'y' if foreign == 1 else 'ies'} not ours to "
                                "sign off" if foreign else ""))

    loaded = {}
    thin = []
    for rel in pages:
        html = open(os.path.join(out_dir, rel), encoding="utf-8").read()
        loaded[rel] = html
        if len(html) < MIN_PAGE_BYTES:
            thin.append(f"{rel} ({len(html)} B)")
    (ok if not thin else bad)("no page rendered empty",
                              ", ".join(thin[:4]) or "all substantial")

    # Machine spill, on every page rather than on the one somebody remembered.
    spilled = []
    for rel, html in loaded.items():
        text = visible(html)
        for pat, why in SPILL:
            if re.search(pat, text):
                spilled.append(f"{rel}: {why}")
        for hit in leaked_none(text)[:1]:
            spilled.append(f"{rel}: a Python None ({hit})")
    (ok if not spilled else bad)("no machine spill in visible copy",
                                 "; ".join(spilled[:4]) or "clean")

    # House voice, against the bytes that shipped.
    offences = []
    for rel, html in loaded.items():
        if DECK_PAGE.search(rel):
            continue
        text = visible(html)
        for pat, why in VOICE:
            if re.search(pat, text):
                offences.append(f"{rel}: {why}")
    (ok if not offences else bad)("the published copy keeps the house voice",
                                  "; ".join(offences[:4]) or "clean")

    # Head essentials. A page with no title is a page no search result can name.
    headless = []
    for rel, html in loaded.items():
        head = html[:8000]
        if not re.search(r"<title>\s*\S", head):
            headless.append(f"{rel}: no title")
        elif not re.search(r'name="description"\s+content="\s*\S', head):
            headless.append(f"{rel}: no description")
    (ok if not headless else warn)("every page names itself",
                                   "; ".join(headless[:4]) or "all titled")

    # Dead internal links. The build validates what it writes, never what it
    # points at, so a renamed URL leaves a link that was right when written.
    #
    # PAGES AND ASSETS ARE DIFFERENT FAILURES and were one check until this
    # went red on a correct build. A dead page link is a 404 a reader clicks
    # and it fails. A dead asset reference usually means the directory is
    # partial rather than the site broken: the fonts and the og images live in
    # docs/ and site_build does not emit them, which site_fresh_check.py has
    # said in its own docstring for months, so a fresh build into a scratch
    # directory has every one of them missing and none of it is wrong. That is
    # a WARN, which still reports and still exits 2.
    dead_pages, dead_assets, checked = [], [], 0
    for rel, html in loaded.items():
        for href in internal_links(html):
            if not href:
                continue
            checked += 1
            if os.path.exists(resolve(out_dir, rel, href)):
                continue
            (dead_assets if ASSET.search(href) else dead_pages).append(
                f"{rel} -> {href}")
    (ok if not dead_pages else bad)(
        "every link a reader can click resolves",
        "; ".join(sorted(set(dead_pages))[:5]) or f"{checked} checked")
    (ok if not dead_assets else warn)(
        "every asset a page asks for is present",
        "; ".join(sorted(set(dead_assets))[:4]) or "all present")

    # A sitemap entry with no page behind it is a 404 offered to a crawler.
    urls = sitemap_urls(out_dir)
    if not urls:
        warn("the sitemap exists", "no sitemap.xml")
    else:
        missing = []
        for u in urls:
            rel = re.sub(r"^https?://[^/]+/", "", u)
            path = os.path.join(out_dir, rel)
            if os.path.isdir(path) or rel.endswith("/") or rel == "":
                path = os.path.join(out_dir, rel, "index.html")
            if not os.path.exists(path):
                missing.append(rel or "/")
        (ok if not missing else bad)("every sitemap entry has a page",
                                     ", ".join(missing[:5]) or f"{len(urls)} urls")

    # THE ONE NO BUILD GATE CAN DO. Is the number a reader sees today the
    # number the ledger holds today.
    for ledger, page_rel, cadence, extract in PUBLISHED:
        name = os.path.basename(ledger)
        if not os.path.exists(os.path.join(REPO, ledger)):
            warn(f"{name} is present", "not in this checkout")
            continue
        try:
            stamp, figures = extract(out_dir)
        except Exception as exc:
            warn(f"{name} could be read", f"{exc.__class__.__name__} {exc}"[:70])
            continue
        if not figures:
            warn(f"{name} holds a published figure", "nothing to publish yet")
            continue
        age = age_days(stamp, today)
        if age is None:
            warn(f"{name} carries a date", "no timestamp to age")
        else:
            (ok if age <= cadence else warn)(
                f"{name} is current", f"{age} day(s) old, cadence {cadence}")
        html = loaded.get(page_rel)
        if html is None:
            bad(f"{name} has a page to reach", f"{page_rel} missing")
            continue
        text = visible(html, drop_svg=False)
        absent = [f"{label} ({value})" for label, value in figures
                  if value and value not in text]
        (ok if not absent else bad)(
            f"{name} reaches {page_rel}",
            "; ".join(absent) or ", ".join(v for _, v in figures if v))

    for ledger, cadence, field in QUEUES:
        name = os.path.basename(ledger)
        path = os.path.join(REPO, ledger)
        if not os.path.exists(path):
            warn(f"{name} is present", "not in this checkout")
            continue
        try:
            stamp = json.loads(open(path, encoding="utf-8").read()).get(field)
        except Exception as exc:
            warn(f"{name} parses", exc.__class__.__name__)
            continue
        age = age_days(stamp, today)
        (ok if age is not None and age <= cadence else warn)(
            f"{name} is current",
            f"{age} day(s) old, cadence {cadence}" if age is not None
            else "no timestamp to age")

    # The hard guard. Present, never read, never linted.
    vids = os.path.join(out_dir, "videos")
    have = (os.path.exists(os.path.join(vids, "index.html"))
            and os.path.exists(os.path.join(vids, "videos.json")))
    (ok if have else warn)("the videos passthrough is intact",
                           "present, not read" if have else "missing from the build")

    fails = [r for r in rows if r[0] == "FAIL"]
    warns = [r for r in rows if r[0] == "WARN"]
    return rows, "FAIL" if fails else ("WARN" if warns else "PASS")


# WHAT TO DO ABOUT IT, not just what is wrong.
#
# A checker that hands back a list of complaints puts the diagnosis on whoever
# reads it, and the reader here is a routine at six in the morning with a deck
# to ship. It went out reporting only, and reporting is not the job: if
# something on the site is broken the run should FIX it, and the report should
# be what is left over after it tried.
#
# So every check carries its own remedy. Almost all of them are fixable inside
# a run, because almost all of them are presentation or a stale build. The two
# that are not are marked REPORT, and they are the same two CLAUDE.md already
# protects: a collector that has stopped running, and a surface another repo
# owns. A run that "fixed" either would be writing a number it does not produce.
FIXES = [
    (r"^every page is on disk|^the built site",
     "Rebuild. python3 scripts/site_build.py --date <date> --out docs"),
    (r"rendered empty",
     "FIX. The page's builder returned nothing. Find the function that emits "
     "it in site_build.py and make it render, then rebuild."),
    (r"machine spill",
     "FIX. A value failed to render into copy. Repair the f-string or the "
     "template call in site_build.py, then rebuild."),
    (r"house voice",
     "FIX. Rewrite the offending copy at its source in site_build.py, "
     "docket_build.py or power_panel.py. The build gates the same rules, so if "
     "the source is already clean the published directory is stale. Rebuild."),
    (r"names itself",
     "FIX. Give the page a title and a description in site_build.page()."),
    (r"a reader can click",
     "FIX. Correct the href, or restore the page it points at. A renamed URL "
     "leaves links that were right when they were written."),
    (r"asset a page asks for",
     "CHECK. Assets are hand managed in docs/ and no fresh build emits them, "
     "so this is expected against a scratch directory and real against docs/. "
     "If it is real, restore the file."),
    (r"sitemap entry",
     "FIX. Either build the page or stop listing it in site_build.sitemap(). "
     "A sitemap entry with no page is a 404 offered to a crawler."),
    (r"reaches ",
     "FIX BY REBUILDING. The ledger moved and the page did not. This is the "
     "failure this checker exists for. python3 scripts/site_build.py --date "
     "<date> --out docs, then run this again. If it still disagrees after a "
     "rebuild, the page's builder is not reading that ledger."),
    (r"is current",
     "REPORT, DO NOT FIX. A collector has not run. Its ledger is cron written "
     "and off limits to a run (CLAUDE.md, routine rule 19). Say so in the "
     "draft and ship the deck."),
    (r"videos passthrough",
     "REPORT, DO NOT FIX. docs/videos/ is a hard guard owned by another repo. "
     "Never write, reformat or regenerate it."),
]


def fix_for(label):
    """The remedy for a check, or None. Kept beside the checks so a new check
    cannot ship without someone deciding what a run should do about it."""
    for pattern, how in FIXES:
        if re.search(pattern, label):
            return how
    return None


def render(rows, verdict, show_fixes=True):
    for status, label, detail in rows:
        print(f"  [{status}] {label}" + (f"  {detail}" if detail else ""))
    n = sum(1 for r in rows if r[0] == "PASS")
    print(f"\nsite sign-off: {verdict}  ({n} of {len(rows)} clean)")
    trouble = [r for r in rows if r[0] != "PASS"]
    if trouble and show_fixes:
        print("\nwhat to do about it")
        for status, label, detail in trouble:
            print(f"  {label}\n    {fix_for(label) or 'FIX at the source.'}")


def summary_line(rows, verdict, pages):
    """The one line the routine puts in the run record and the Gmail draft.

    It names what is UNFIXED, because by the time this line is written the run
    was supposed to have fixed everything it could. A clean line means clean,
    and a line with something in it means a person needs to look."""
    trouble = [f"{l}" for s, l, _ in rows if s in ("FAIL", "WARN")]
    tail = f", UNFIXED {'; '.join(trouble[:3])}" if trouble else ""
    return f"SITE SIGN-OFF: {verdict}, {pages} pages, {len(rows)} checks{tail}"


# ------------------------------------------------------------------ self test

def _fake_site(root, **broken):
    """A minimal site with exactly the faults asked for, so each red case is
    tested one at a time rather than against a page carrying six problems."""
    os.makedirs(os.path.join(root, "videos"), exist_ok=True)
    open(os.path.join(root, "videos", "index.html"), "w").write("<html>videos")
    open(os.path.join(root, "videos", "videos.json"), "w").write("[]")
    # Comfortably over MIN_PAGE_BYTES, so the fixture is testing the checks
    # rather than tripping the floor meant for a page that never rendered.
    filler = "<p>Alaska AI keeps a public record of what is decided here.</p>" * 90

    def write(rel, body):
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(
            f'<title>{rel}</title><meta name="description" content="a page">'
            f"<main>{body}{filler}</main>")

    write("index.html", broken.get("home", '<a href="about/">About</a>'))
    write("about/index.html", broken.get("about", "<p>We build things.</p>"))
    if broken.get("thin"):
        os.makedirs(os.path.join(root, "thin"), exist_ok=True)
        open(os.path.join(root, "thin", "index.html"), "w").write("<title>t</title>")
    open(os.path.join(root, "sitemap.xml"), "w").write(
        '<?xml version="1.0"?><urlset>'
        "<loc>https://alaskaaihq.com/</loc><loc>https://alaskaaihq.com/about/</loc>"
        + (broken.get("sitemap_extra") or "") + "</urlset>")
    return root


def self_test():
    """The checker has to be able to go red, or it certifies nothing."""
    import tempfile
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    # A synthetic site has none of the pages the real ledgers publish to, so
    # those rows are noise here and the page checks are what is under test.
    def LEDGER_ROW(label):
        return ".json" in label or ".jsonl" in label

    def verdict_of(**broken):
        root = _fake_site(tempfile.mkdtemp(), **broken)
        rows, v = check_site(root)
        # The ledger checks are about the real repo and a fake site has none of
        # those pages, so only the page-level rows are under test here.
        page_rows = [r for r in rows if not LEDGER_ROW(r[1])]
        return ("FAIL" if any(r[0] == "FAIL" for r in page_rows)
                else "WARN" if any(r[0] == "WARN" for r in page_rows) else "PASS"), rows

    print("a sound site signs off")
    v, rows = verdict_of()
    check("a clean site passes its page checks", v == "PASS",
          f"{v}, " + "; ".join(f"{s} {l}" for s, l, d in rows
                               if s == "FAIL") or "no fails")

    print("and every fault it exists to catch turns it red")
    cases = [
        ("an unrendered f-string placeholder",
         {"about": '<p>Storage {f["inventory_bcf"]} Bcf</p>'}),
        ("a Python None in visible copy", {"about": "<p>Storage None Bcf</p>"}),
        ("a None where a number belonged", {"about": "<p>Price is None cents.</p>"}),
        ("a stringified JS object", {"about": "<p>[object Object]</p>"}),
        ("an em dash in published copy", {"about": "<p>Alaska — the state</p>"}),
        ("'cannot' in published copy", {"about": "<p>This cannot be done.</p>"}),
        ("a dead link a reader can click", {"home": '<a href="nowhere/">Gone</a>'}),
        ("a page that rendered empty", {"thin": True}),
        ("a sitemap entry with no page behind it",
         {"sitemap_extra": "<loc>https://alaskaaihq.com/ghost/</loc>"}),
    ]
    for label, broken in cases:
        v, _ = verdict_of(**broken)
        check(f"goes red on {label}", v == "FAIL", v)

    # A missing asset is a real report and not a failure, because the fonts and
    # the og images live in docs/ and no fresh build emits them.
    v, rows = verdict_of(home='<link rel="preload" href="fonts/x.woff2">')
    row = [r for r in rows if "asset a page asks for" in r[1]]
    check("a missing asset warns rather than fails",
          v == "WARN" and row and row[0][0] == "WARN",
          f"{v}, {row[0][2] if row else 'no row'}")

    print("and stays quiet on what is allowed")
    # The two real sentences a flat \bNone\b called broken on its first run.
    for sentence in ("<p>No cookies. None are set and none are read.</p>",
                     "<p>Every one carries its documents. None are open for "
                     "public comment right now.</p>"):
        v, _ = verdict_of(about=sentence)
        check("the English word None is left alone", v == "PASS",
              f"{v}: {sentence[3:44]}")

    root = _fake_site(tempfile.mkdtemp())
    # Shipped run copy keeps its own words, on the deck page and in the card.
    open(os.path.join(root, "about", "index.html"), "a").write(
        '<a class="deck" href="#"><p>operators cannot read the airspace</p></a>')
    os.makedirs(os.path.join(root, "archive", "2026-07-17"), exist_ok=True)
    open(os.path.join(root, "archive", "2026-07-17", "index.html"), "w").write(
        '<title>deck</title><meta name="description" content="d"><main>'
        "<p>Bill Walker said manufactured ideas cannot substitute thought.</p>"
        + "<p>filler filler filler filler filler filler filler. " * 60 + "</main>")
    rows, _ = check_site(root)
    voice = [r for r in rows if "house voice" in r[1]]
    check("a quoted 'cannot' in shipped run copy is left alone",
          voice and voice[0][0] == "PASS", voice[0][2] if voice else "no row")

    print("the surfaces this repo does not own are skipped, and said to be")
    root = _fake_site(tempfile.mkdtemp())
    # A page under a foreign directory carrying every fault at once. None of it
    # is ours to fix, so none of it may turn the sign-off red.
    for foreign in FOREIGN:
        os.makedirs(os.path.join(root, foreign), exist_ok=True)
        open(os.path.join(root, foreign, "index.html"), "w").write(
            "<p>None cannot \u2014 [object Object]</p>"
            '<a href="nowhere/">dead</a>')
    open(os.path.join(root, "videos", "videos.json"), "w").write("[]")
    rows, _ = check_site(root)
    dirty = [l for s_, l, d in rows if s_ == "FAIL" and not LEDGER_ROW(l)]
    check("a foreign page's faults are not this site's failures", not dirty,
          "; ".join(dirty[:3]) or "clean")
    walked = [r for r in rows if r[1] == "every page is on disk"]
    check("and the skip is stated rather than silent",
          walked and "not ours to sign off" in walked[0][2],
          walked[0][2] if walked else "no row")
    root = _fake_site(tempfile.mkdtemp())
    os.remove(os.path.join(root, "videos", "videos.json"))
    rows, _ = check_site(root)
    row = [r for r in rows if "videos passthrough" in r[1]]
    check("a missing passthrough warns rather than fails",
          row and row[0][0] == "WARN", row[0][0] if row else "no row")

    print("the check no build gate can do")
    # THE FAILURE THIS FILE EXISTS FOR. A collector commits a new figure, the
    # page that prints it is not rebuilt, and every build gate stays green
    # because the build was fine and simply never ran. Simulated by putting the
    # PREVIOUS month back on an otherwise correct page, which is exactly what a
    # missed rebuild leaves behind.
    docs = os.path.join(REPO, "docs")
    gaspage = os.path.join(docs, "gas-watch", "index.html")
    if os.path.exists(gaspage):
        import shutil
        stale = tempfile.mkdtemp()
        shutil.copytree(docs, os.path.join(stale, "s"), symlinks=True)
        stale = os.path.join(stale, "s")
        page = open(gaspage, encoding="utf-8").read()
        import power_panel as pw
        res = (pw.load() or {}).get("sectors", {}).get("residential", {})
        behind = page.replace(res["latest_label"], "April 2001").replace(
            f"{res['latest']:.2f}", "19.11")
        open(os.path.join(stale, "gas-watch", "index.html"), "w",
             encoding="utf-8").write(behind)
        rows, _ = check_site(stale)
        row = [r for r in rows if r[1].startswith("power.json reaches")]
        check("a page left behind by a collector is caught",
              row and row[0][0] == "FAIL", row[0][2] if row else "no row")
        # And the reverse, so the check is not just always red.
        rows, _ = check_site(docs)
        row = [r for r in rows if r[1].startswith("power.json reaches")]
        check("and a current page is not", row and row[0][0] == "PASS",
              row[0][2] if row else "no row")
    else:
        print("    (no built docs/ in this checkout, skipped)")

    print("every check says what to do about itself")
    rows, _ = check_site(os.path.join(REPO, "docs")) if os.path.isdir(
        os.path.join(REPO, "docs")) else ([], "")
    orphan = [l for _, l, _ in rows if not fix_for(l)]
    check("no check ships without a remedy", not orphan, "; ".join(orphan[:4]))
    fixable = [l for _, l, _ in rows if (fix_for(l) or "").startswith(
        ("FIX", "Rebuild", "CHECK"))]
    guarded = [l for _, l, _ in rows if (fix_for(l) or "").startswith("REPORT")]
    check("most of them a run can repair itself", len(fixable) > len(guarded),
          f"{len(fixable)} fixable, {len(guarded)} report only")
    check("a stale collector is never one a run repairs",
          all("REPORT" in (fix_for(l) or "") for _, l, _ in rows
              if l.endswith("is current")))
    check("a stale page is one a run repairs, by rebuilding",
          all("REBUILDING" in (fix_for(l) or "") for _, l, _ in rows
              if " reaches " in l))

    print("it reports and never aborts")
    check("a page fault is a 2, never a 1",
          exit_code("FAIL") == 2 and exit_code("WARN") == 2
          and exit_code("PASS") == 0)
    check("the summary line names what went wrong",
          "SITE SIGN-OFF: WARN" in summary_line(
              [("WARN", "power.json is current", "60 days old")], "WARN", 73)
          and "power.json is current" in summary_line(
              [("WARN", "power.json is current", "60 days old")], "WARN", 73))

    print("and it signs off the real built site when there is one")
    docs = os.path.join(REPO, "docs")
    if os.path.isdir(docs):
        rows, v = check_site(docs)
        fails = [f"{l} ({d})" for s, l, d in rows if s == "FAIL"]
        check("docs/ has no outright failures", not fails, "; ".join(fails[:3]))
    else:
        print("    (no docs/ in this checkout, skipped)")

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def exit_code(verdict):
    """0 clean, 2 needs attention. Never 1 for a site problem, because a page
    fault must not abort the carousel run that noticed it."""
    return 0 if verdict == "PASS" else 2


def main():
    ap = argparse.ArgumentParser(
        description="Daily once over of every published page")
    ap.add_argument("--out", default=os.path.join(REPO, "docs"),
                    help="built site directory, default docs/")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    rows, verdict = check_site(args.out)
    pages = len(page_files(args.out)[0]) if os.path.isdir(args.out) else 0
    if args.json:
        print(json.dumps({"verdict": verdict, "pages": pages,
                          "line": summary_line(rows, verdict, pages),
                          "rows": [{"status": s, "check": l, "detail": d,
                                    "fix": fix_for(l)}
                                   for s, l, d in rows]}, indent=2))
    else:
        render(rows, verdict)
        print(summary_line(rows, verdict, pages))
    return exit_code(verdict)


if __name__ == "__main__":
    sys.exit(main())
