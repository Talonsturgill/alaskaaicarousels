#!/usr/bin/env python3
"""docket_dates_check.py is the build gate that stops the docket rendering one
decision's date as another's.

On 2026-07-21 Phase 3.5 added the Houston City Council's August 13 vote to the
AIDEA item, whose own DNR comment window closes 5 p.m. August 19. Every date
slot on the site picked the soonest upcoming key_date of any kind, so from that
day the marquee entry carried a gold button reading COMMENT NOW, CLOSES AUG 13,
six days early, for a vote by a different body on a different question. The
entry's own prose, timeline rail and change notes said August 19 throughout.
The contradiction sat inside a single card and nothing looked.

The docket is machine-maintained, so a one-time correction is worth very
little. This is the part that has to exist: a check that FAILS THE BUILD.

What it asserts

  ROLES        every rendered date equals the resolved value for its role.
               A call to action renders its own action deadline or no date.
  PROSE        a date the chrome presents as an item's action deadline also
               appears in that item's own prose. Where prose and metadata
               disagree, that is a human's call, so it fails.
  STATUS       OPEN implies a future action path. CLOSED implies no call to
               action. An expired window does not keep soliciting comment.
  SURFACES     the built home page and docket page agree with the resolver
               and with each other, read out of the real emitted HTML.
  ALERTS       the subscriber email composes the same resolved dates.

It runs six fixtures through the REAL renderers, not a copy of their logic, and
then runs the real build over the real ledger. --self-test proves the gate
still fails on a deliberately broken item; a green check that cannot go red is
just a slower way of shipping the bug.

  python scripts/docket_dates_check.py [--date YYYY-MM-DD] [--self-test]

Exit 0 clean, 1 on any violation, 2 if it could not look (a blind check is a
FAIL, not a pass).
"""

import argparse
import copy
import html
import re
import subprocess
import sys
import tempfile
from datetime import date as ddate
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docket_build as db

REPO = Path(__file__).resolve().parents[1]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
# "August 19", "Aug. 19", "August 19, 2026". Day is captured without a year so
# a prose sentence that omits the year still matches.
PROSE_DATE = re.compile(
    r"\b(" + "|".join(m[:3] for m in MONTH_NAMES) + r")[a-z]*\.?\s+(\d{1,2})\b")
CTA_RE = re.compile(r"COMMENT NOW(?:\s*&middot;\s*CLOSES\s+([A-Z]{3}\s+\d{1,2}))?")
CHIP_RE = re.compile(r'<span class="chip days" data-date="(\d{4}-\d{2}-\d{2})">'
                     r'([a-z]+)\s+([A-Z]{3}\s+\d{1,2})</span>')


class Report:
    def __init__(self):
        self.bad = []
        self.checked = 0

    def ok(self, cond, where, msg):
        self.checked += 1
        if not cond:
            self.bad.append(f"{where}: {msg}")
        return cond


def mon_day_pair(iso):
    d = ddate.fromisoformat(iso)
    return MONTH_NAMES[d.month - 1], d.day


# ---------- fixtures ----------
#
# Built to OBSERVE the failure, not to certify the current output. A fixture
# copied from today's broken render will happily agree with the bug. Each of
# these fails loudly against the pre-fix selector.

def item(**kw):
    base = {
        "id": "fixture", "title": "A fixture decision", "kind": "state-land-lease",
        "status": "open-for-comment", "decider": "Some Body", "public_access": "open",
        "access_note": "Comment on the record.", "summary": "A fixture.",
        "key_dates": [], "location": {"name": "Anchorage", "lon": -149.9, "lat": 61.2},
        "sources": [{"url": "https://example.gov/notice", "outlet": "Notice",
                     "date": "2026-07-10"}],
        "first_seen": "2026-07-10", "last_updated": "2026-07-10",
        "history": [{"date": "2026-07-10", "note": "Tracked."}],
    }
    base.update(kw)
    return base


def kd(date, label, kind):
    return {"date": date, "label": label, "kind": kind}


TODAY = ddate(2026, 7, 29)

FIXTURES = [
    # 6a. Entry 01 as it exists today: an unrelated vote sooner than the
    # entry's own comment deadline. Every slot must read AUG 19.
    ("entry-01-today", item(
        id="fx-aidea", status="open-for-comment", public_access="open",
        summary="Public comment runs through August 19.",
        access_note="Anyone can comment through 5 p.m. August 19, 2026.",
        key_dates=[kd("2026-07-13", "Preliminary decision reported", "milestone"),
                   kd("2026-08-13", "Another city's council vote", "vote"),
                   kd("2026-08-19", "Public comment closes", "deadline")]),
     {"cta_date": "AUG 19", "chip": ("by", "AUG 19"), "access": "open",
      "headline": "2026-08-19"}),

    # 6b. Inverted: the unrelated milestone is LATER than the deadline. Catches
    # a "fix" that only swapped min for max.
    ("milestone-after-deadline", item(
        id="fx-inverted", summary="Public comment runs through August 5.",
        access_note="Comment through August 5, 2026.",
        key_dates=[kd("2026-08-05", "Public comment closes", "deadline"),
                   kd("2026-09-30", "Council vote", "vote")]),
     {"cta_date": "AUG 5", "chip": ("by", "AUG 5"), "access": "open",
      "headline": "2026-08-05"}),

    # 6c. Open-looking, no action deadline ever recorded. Rule 3: invent no
    # date. The call to action survives without one; it does not borrow the
    # vote sitting right next to it.
    ("open-no-deadline", item(
        id="fx-nodate", summary="A window is open. No close date is published.",
        access_note="Comment on the record while it is open.",
        key_dates=[kd("2026-08-13", "Council vote", "vote")]),
     {"cta_date": None, "chip": ("vote", "AUG 13"), "access": "open",
      "headline": "2026-08-13"}),

    # 6d. Deadline in the past. Rule 4: status and access flip with no human
    # in the loop, and the call to action goes away.
    ("deadline-passed", item(
        id="fx-expired", summary="Public comment ran through July 17.",
        access_note="The window closed July 17, 2026.",
        key_dates=[kd("2026-07-17", "Public comment closes", "deadline")]),
     {"cta_date": None, "no_cta": True, "chip": None, "access": "closed",
      "headline": None}),

    # 6e. Exactly one date. Nothing clever should happen to the simple case.
    ("single-date", item(
        id="fx-single", summary="Public comment runs through August 19.",
        access_note="Comment through August 19, 2026.",
        key_dates=[kd("2026-08-19", "Public comment closes", "deadline")]),
     {"cta_date": "AUG 19", "chip": ("by", "AUG 19"), "access": "open",
      "headline": "2026-08-19"}),

    # 6f. The DNR notice closes at 5 p.m. Alaska time. The hour lives in the
    # label, never in the date, so a build running in UTC cannot shift the day.
    # Asserted on the day itself, which is where an off-by-one would show.
    ("time-of-day-and-zone", item(
        id="fx-tz", summary="Public comment runs through August 19.",
        access_note="Comment through 5 p.m. AKDT August 19, 2026.",
        key_dates=[kd("2026-08-19", "Public comment closes, 5 p.m. AKDT", "deadline")]),
     {"cta_date": "AUG 19", "chip": ("by", "AUG 19"), "access": "open",
      "headline": "2026-08-19", "today": ddate(2026, 8, 19)}),
]


def check_fixtures(rep):
    for name, it, want in FIXTURES:
        today = want.get("today", TODAY)
        where = f"fixture {name}"
        db.validate([it])
        r = db.resolve(it, today)

        got_headline = r["headline"]["date"] if r["headline"] else None
        rep.ok(got_headline == want["headline"], where,
               f"headline {got_headline} want {want['headline']}")
        rep.ok(r["access"] == want["access"], where,
               f"access {r['access']} want {want['access']}")

        # The REAL renderers, not a restatement of them.
        item_out = db.item_html(it, today, 1)
        card_out = db.card_html(it, today)

        m = CTA_RE.search(item_out)
        if want.get("no_cta"):
            rep.ok(m is None, where, "renders a call to action after its deadline passed")
        else:
            rep.ok(m is not None, where, "renders no call to action")
            if m:
                rep.ok(m.group(1) == want["cta_date"], where,
                       f"call to action says {m.group(1)!r}, want {want['cta_date']!r}")

        chips = CHIP_RE.findall(item_out)
        if want["chip"] is None:
            rep.ok(not chips, where, f"renders a date chip when it should not: {chips}")
        else:
            rep.ok(len(chips) == 1, where, f"expected one date chip, got {chips}")
            if chips:
                iso, prefix, shown = chips[0]
                rep.ok((prefix, shown) == want["chip"], where,
                       f"chip {(prefix, shown)} want {want['chip']}")
                rep.ok(iso == want["headline"], where,
                       f"chip data-date {iso} want {want['headline']}")

        # The card is a second surface over the same item and must agree.
        for iso, prefix, shown in CHIP_RE.findall(card_out):
            rep.ok(iso == want["headline"], where,
                   f"card chip {iso} disagrees with the item chip {want['headline']}")
        rep.ok(f'b-{want["access"]}' in card_out, where,
               f"card badge does not read {want['access']}")


# ---------- the invariants, over any set of items ----------

def check_items(rep, items, today, label="ledger"):
    for it in items:
        where = f"{label} {it['id']}"
        r = db.resolve(it, today)

        # ROLES. An action deadline is a deadline-kind date and nothing else.
        if r["deadline"]:
            rep.ok(r["deadline"]["kind"] == "deadline", where,
                   f"action deadline came from a {r['deadline']['kind']} date, "
                   f"{r['deadline']['label']!r}")
            rep.ok(r["deadline"]["date"] >= today.isoformat(), where,
                   "action deadline is in the past")

        # STATUS. Open implies a path the reader can still walk.
        if r["access"] == "open":
            rep.ok(r["status"] == "open-for-comment", where,
                   f"access open with status {r['status']}")
            rep.ok(not (db.had_action_deadline(it) and r["deadline"] is None), where,
                   "reads OPEN with its published deadline already passed")
        if r["cta"]:
            rep.ok(r["access"] == "open", where, "offers a call to action while not open")

        # FRESHNESS. last_updated is what a data consumer pins on to know when
        # this record was last verified, so it may never fall behind the item's
        # own newest note. gvea-lm6000-turbine-purchase shipped last_updated
        # 2026-07-30 against a 2026-08-01 history note, and the public feed
        # under-reported its own freshness by two days with nothing to catch
        # it. Phase 3.5 hand-edits this ledger, which is precisely why the two
        # fields can diverge; db.append_history() pairs them for any code that
        # ever writes them, and this is the gate for everything else.
        hist = it.get("history") or []
        if hist and it.get("last_updated"):
            newest = max(h["date"] for h in hist)
            rep.ok(newest <= it["last_updated"], where,
                   f"last_updated {it['last_updated']} is older than this "
                   f"item's newest history note {newest}. Stamp the item in "
                   f"the same edit that adds the note.")
            rep.ok(it["last_updated"] >= it["first_seen"], where,
                   f"last_updated {it['last_updated']} precedes first_seen "
                   f"{it['first_seen']}")

        # PROSE vs METADATA. Any date the chrome presents as this item's action
        # deadline must appear in the item's own words. This is the assertion
        # that would have caught the shipped defect on the day it shipped:
        # the button said AUG 13, and no sentence in the entry contains it.
        if r["deadline"]:
            prose = f"{it['summary']} {it['access_note']}"
            found = {(m.group(1), int(m.group(2))) for m in PROSE_DATE.finditer(prose)}
            found = {(MONTH_NAMES[[m[:3] for m in MONTH_NAMES].index(mo)], d)
                     for mo, d in found}
            want = mon_day_pair(r["deadline"]["date"])
            rep.ok(want in found or not found, where,
                   f"chrome would show a {want[0]} {want[1]} deadline, but the entry's "
                   f"own prose says {sorted(found)}. Prose and metadata disagree; "
                   f"a human decides which is right.")


def check_alerts(rep, items, today):
    """The subscriber email is the surface a correction cannot reach. It reads
    the same resolver as the page, and this proves it."""
    try:
        import docket_alerts as da
    except Exception as e:
        rep.ok(False, "alerts", f"could not import docket_alerts ({type(e).__name__})")
        return
    for k, kind, it, d in da.due_alerts(items, set(), today):
        if kind != "window-open":
            continue
        want = db.resolve(it, today)["deadline"]
        got = d["date"] if d else None
        rep.ok(got == (want["date"] if want else None), "alerts " + it["id"],
               f"window-open email would carry {got}, resolver says "
               f"{want['date'] if want else None}")


# ---------- the real built pages ----------

def text_of(path):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "\n", s))


def check_built_site(rep, items, today, out):
    """Build the site for real and read the dates back out of the emitted HTML.
    Nothing here trusts the renderer's return value; it reads what a visitor
    would get."""
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "site_build.py"),
                        "--date", today.isoformat(), "--out", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-2000:], file=sys.stderr)
        print("BLIND: the site build failed, so this gate could not look.", file=sys.stderr)
        sys.exit(2)

    page = out / "docket" / "index.html"
    home = out / "index.html"
    for p in (page, home):
        if not p.exists():
            print(f"BLIND: {p} was not built.", file=sys.stderr)
            sys.exit(2)

    by_id = {it["id"]: it for it in items}
    doc = page.read_text(encoding="utf-8")

    # Every entry article, read back out of the page one at a time.
    for art in re.findall(r'<article class="item [^"]*" id="([^"]+)"(.*?)</article>',
                          doc, flags=re.S):
        iid, body = art
        it = by_id.get(iid)
        if not it:
            rep.ok(False, f"page {iid}", "rendered an item that is not in the ledger")
            continue
        res = db.resolve(it, today)
        where = f"page {iid}"

        m = CTA_RE.search(body)
        if res["cta"]:
            rep.ok(m is not None, where, "resolver offers a call to action, page has none")
        else:
            rep.ok(m is None, where, "page offers a call to action the resolver forbids")
        if m:
            want = db.mon_day(res["deadline"]["date"]).upper() if res["deadline"] else None
            rep.ok(m.group(1) == want, where,
                   f"call to action shows {m.group(1)!r}, action deadline is {want!r}")

        for iso, prefix, shown in CHIP_RE.findall(body):
            want = res["headline"]["date"] if res["headline"] else None
            rep.ok(iso == want, where, f"chip date {iso} != resolved headline {want}")
            rep.ok(prefix == db.ROLE_PREFIX[res["headline"]["kind"]], where,
                   f"chip prefix {prefix!r} does not match the date's role "
                   f"{res['headline']['kind']!r}")
            rep.ok(shown == db.mon_day(iso), where, f"chip text {shown} != {iso}")

        rep.ok(f'class="badge b-{res["access"]}"' in body, where,
               f"badge does not read the resolved access {res['access']}")

    # Closing-soon cards sit under "The nearest deadlines and votes", so their
    # order has to be the order of the dates they print. Sorting them by one
    # date and printing another put AUG 19 above AUG 15 under that heading, and
    # could push the actual nearest deadline out of the six that get rendered.
    for name, p in (("docket", page), ("home", home)):
        shown = re.findall(r'<div class="big" data-days="(\d{4}-\d{2}-\d{2})">',
                           p.read_text(encoding="utf-8"))
        rep.ok(shown == sorted(shown), f"{name} cards",
               f"closing-soon cards are out of date order: {shown}")

    # The homepage stat and the cards under it are one claim, not two. On
    # 2026-08-05 the header read 02 DOORS OPEN TO YOU and the strip below it
    # showed one gold card, because the cards were picked by soonest date and
    # two milestones outranked a door. The maintainer counted them and caught
    # it; nothing here could. A door is the only thing on that page a reader
    # can act on, so the strip shows every one it has room for.
    hbody = home.read_text(encoding="utf-8")
    strip = re.search(r'<div class="cards">(.*?)</div>\s*<div class="ctarow"',
                      hbody, flags=re.S)
    rep.ok(strip is not None, "home cards", "no closing-soon card strip on the home page")
    if strip:
        slots = len(re.findall(r'class="badge b-', strip.group(1)))
        gold = len(re.findall(r'class="badge b-open"', strip.group(1)))
        doors = db.open_count(items, today)
        rep.ok(gold == min(doors, slots), "home cards",
               f"header says {doors} open door(s), the {slots} cards below it show "
               f"{gold}. A door never loses a card slot to a milestone.")

    # Cross-surface: the header stat, the closing-soon cards on both pages, and
    # the homepage sentence all trace to one resolved value.
    # Per-decision pages are a SECOND surface rendering the same dates, and a
    # surface the guard cannot see is a surface that can drift. Every one of
    # them is read back out of its own emitted HTML, same rules as the entries
    # on the docket page.
    for iid, it in by_id.items():
        dp = out / "docket" / iid / "index.html"
        if not dp.exists():
            rep.ok(False, f"decision page {iid}", "no canonical page was built")
            continue
        dbody = dp.read_text(encoding="utf-8")
        res = db.resolve(it, today)
        where = f"decision page {iid}"
        m = CTA_RE.search(dbody)
        if res["cta"]:
            rep.ok(m is not None, where, "resolver offers a call to action, page has none")
        else:
            rep.ok(m is None, where, "page offers a call to action the resolver forbids")
        if m:
            want = db.mon_day(res["deadline"]["date"]).upper() if res["deadline"] else None
            rep.ok(m.group(1) == want, where,
                   f"call to action shows {m.group(1)!r}, action deadline is {want!r}")
        for iso, prefix, shown in CHIP_RE.findall(dbody):
            want = res["headline"]["date"] if res["headline"] else None
            rep.ok(iso == want, where, f"chip date {iso} != resolved headline {want}")
            rep.ok(prefix == db.ROLE_PREFIX[res["headline"]["kind"]], where,
                   f"chip prefix {prefix!r} does not match role "
                   f"{res['headline']['kind']!r}")
        rep.ok(f'class="badge b-{res["access"]}"' in dbody, where,
               f"badge does not read the resolved access {res['access']}")
        # An Event node is a promise that a comment window is open with that end
        # date, so it may exist only when the resolver says so, and must carry
        # the resolved deadline.
        ev = re.search(r'"@type":"Event".*?"endDate":"(\d{4}-\d{2}-\d{2})"', dbody, re.S)
        if res["cta"] and res["deadline"]:
            rep.ok(ev is not None, where, "open window but no Event structured data")
            if ev:
                rep.ok(ev.group(1) == res["deadline"]["date"], where,
                       f"Event endDate {ev.group(1)} != deadline {res['deadline']['date']}")
        else:
            rep.ok(ev is None, where,
                   "publishes an open comment Event the resolver does not support")

    # The questions page renders a resolved deadline chip for every open window,
    # so it is a date surface too and gets the same treatment. Any chip it shows
    # must belong to an item the resolver says is genuinely open, and carry that
    # item's resolved headline date.
    qp = out / "questions" / "index.html"
    if qp.exists():
        qbody = qp.read_text(encoding="utf-8")
        open_ids = {i: db.resolve(it, today) for i, it in by_id.items()
                    if db.resolve(it, today)["cta"]}
        want_dates = {r["headline"]["date"] for r in open_ids.values() if r["headline"]}
        for iso, prefix, shown in CHIP_RE.findall(qbody):
            rep.ok(iso in want_dates, "questions page",
                   f"chip shows {iso}, which is not the resolved headline of any "
                   f"item the resolver reports as open ({sorted(want_dates)})")
            rep.ok(shown == db.mon_day(iso), "questions page",
                   f"chip text {shown} does not match its own date {iso}")
        rep.ok(len(CHIP_RE.findall(qbody)) == len(want_dates), "questions page",
               f"renders {len(CHIP_RE.findall(qbody))} date chips for "
               f"{len(want_dates)} open window(s)")

    nearest = db.nearest_headline(
        [it for it in items
         if it["status"] in ("open-for-comment", "pending-decision", "watching")], today)
    for name, p in (("docket", page), ("home", home)):
        for iso, prefix, shown in CHIP_RE.findall(p.read_text(encoding="utf-8")):
            src = by_id.get(_card_owner(p.read_text(encoding="utf-8"), iso))
            if src is None:
                continue
            want = db.resolve(src, today)["headline"]
            rep.ok(want is not None and iso == want["date"], f"{name} card {src['id']}",
                   f"card shows {iso}, resolver says {want['date'] if want else None}")
    if nearest:
        stat = re.search(r'<div class="n">([A-Z]{3} \d{1,2})</div><div class="l">NEXT DATE</div>',
                         doc)
        rep.ok(stat is not None, "page header", "NEXT DATE stat is missing")
        if stat:
            rep.ok(stat.group(1) == db.mon_day(nearest["date"]), "page header",
                   f"NEXT DATE says {stat.group(1)}, resolver says "
                   f"{db.mon_day(nearest['date'])}")
        htxt = text_of(home)
        m = re.search(r"Next on the docket is (.+?), ([A-Z][a-z]+ \d{1,2}), (\d{4})\.", htxt)
        rep.ok(m is not None, "home", "the next-on-the-docket line is missing")
        if m:
            want_m, want_d = mon_day_pair(nearest["date"])
            rep.ok(m.group(2) == f"{want_m} {want_d}", "home",
                   f"homepage says {m.group(2)}, resolver says {want_m} {want_d}")
            # A title and a date in one sentence must belong to the SAME item.
            # The first fix corrected which date each surface shows and left
            # ordering keyed to the old value, so the home page could pair one
            # item's title with another item's date. Selection was fixed;
            # ordering was not. This is the assertion that covers ordering.
            named = [it for it in items if html.unescape(it["title"]) == m.group(1)]
            rep.ok(len(named) == 1, "home",
                   f"headline names {m.group(1)!r}, which matches "
                   f"{len(named)} ledger items")
            if len(named) == 1:
                own = db.resolve(named[0], today)["headline"]
                rep.ok(own is not None and own["date"] == nearest["date"], "home",
                       f"headline names {named[0]['id']} but prints "
                       f"{nearest['date']}, which is not that item's date "
                       f"({own['date'] if own else None})")


def _card_owner(doc, iso):
    """Which item a closing-soon card belongs to, read off its own anchor."""
    m = re.search(r'<a class="card [^"]*" href="[^"]*#([^"]+)"[^>]*>(?:(?!</a>).)*?'
                  r'data-date="' + re.escape(iso) + '"', doc, flags=re.S)
    return m.group(1) if m else None


# ---------- self-test: prove the gate can go red ----------

def self_test(items, today):
    """Prove the gate can go red. Two deliberate breakages, one on each side of
    the defect, and both must fire.

    A. THE ORIGINAL BUG, THROUGH THE REAL RENDERER. Widening ACTION_KINDS to
       every date kind restores exactly the pre-fix selector: the action
       deadline becomes the soonest upcoming date of any kind. Nothing here
       reimplements the old logic, it re-enables it, and db.item_html then
       emits the button that shipped. If the fixtures cannot see that, they
       were built to agree with the bug and are worthless.

    B. THE SAME DEFECT IN DATA. Relabel another body's event as this item's
       deadline, which is what a future automated entry could plausibly do,
       and require the prose gate to catch it.
    """
    failures = []

    original = db.ACTION_KINDS
    try:
        db.ACTION_KINDS = set(db.DATE_KINDS)     # the pre-fix selector, restored
        rep_a = Report()
        check_fixtures(rep_a)
        check_items(rep_a, items, today, label="pre-fix")
    finally:
        db.ACTION_KINDS = original
    if not rep_a.bad:
        failures.append("the pre-fix selector passed the fixtures")
    else:
        print(f"self-test A: the pre-fix selector fails {len(rep_a.bad)} assertion(s), "
              f"through the real renderer")
        for b in rep_a.bad[:8]:
            print(f"  would fail: {b}")

    # THE BREAKAGE HAS TO BE ONE THE GATE CAN SEE, and only an UPCOMING date is
    # one of those. The resolver ignores dates that have already passed, which
    # is correct behaviour and was silently fatal here: this used to mislabel
    # every vote or decision on a deadline-bearing item, count it as injected,
    # and then assert the gate caught it. The live ledger's only such date was
    # the Houston City Council vote of August 13th on the AIDEA item, so on
    # August 14th the injected breakage became invisible, rep_b came back empty,
    # and the self-test announced that the gate was not watching what it claims
    # to watch. Nothing was wrong with the gate or the ledger. The test had a
    # date in it. Count a mislabel only when it lands in the future.
    broken = copy.deepcopy(items)
    hit = 0
    for it in broken:
        if any(d["kind"] == "deadline" for d in it["key_dates"]):
            for d in it["key_dates"]:
                if d["kind"] in ("vote", "decision"):
                    d["kind"] = "deadline"
                    if ddate.fromisoformat(d["date"]) > today:
                        hit += 1
    b_today = today
    if not hit:
        # No upcoming vote or decision anywhere in the live ledger, which is the
        # normal state of a docket between sessions. Fall back to the fixture,
        # and judge it at the fixture anchor rather than at the live date, or
        # the fallback rots exactly the way the ledger path just did.
        broken = copy.deepcopy([FIXTURES[0][1]])
        b_today = TODAY
        for d in broken[0]["key_dates"]:
            if d["kind"] == "vote":
                d["kind"] = "deadline"
    rep_b = Report()
    check_items(rep_b, broken, b_today, label="mislabelled")
    if not rep_b.bad:
        failures.append("a mislabelled date passed the gate")
    else:
        print(f"self-test B: a mislabelled date fails {len(rep_b.bad)} assertion(s)")
        for b in rep_b.bad[:8]:
            print(f"  would fail: {b}")

    if failures:
        for f in failures:
            print(f"SELF-TEST FAILED: {f}. The gate is not watching what it "
                  f"claims to watch.", file=sys.stderr)
        return 1
    print("self-test: the gate goes red on both breakages, as designed")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None,
                    help="build date YYYY-MM-DD; defaults to the ledger's newest last_updated")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the gate fails on a deliberately broken fixture")
    ap.add_argument("--skip-build", action="store_true",
                    help="fixtures and ledger invariants only, no site build")
    args = ap.parse_args()

    import json
    ledger = json.loads((REPO / "ledger/docket.json").read_text())
    items = ledger["items"]
    today = (ddate.fromisoformat(args.date) if args.date
             else max(ddate.fromisoformat(it["last_updated"]) for it in items))

    if args.self_test:
        return self_test(items, today)

    rep = Report()
    check_fixtures(rep)
    check_items(rep, items, today)
    check_alerts(rep, items, today)
    if not args.skip_build:
        with tempfile.TemporaryDirectory() as tmp:
            check_built_site(rep, items, today, Path(tmp))

    if rep.bad:
        print(f"FAIL: {len(rep.bad)} docket date violation(s) at {today}", file=sys.stderr)
        for b in rep.bad:
            print(f"  {b}", file=sys.stderr)
        print("\nDates have roles. A call to action renders its own action's "
              "deadline or no date at all.", file=sys.stderr)
        return 1
    print(f"docket dates clean at {today}: {rep.checked} assertions over "
          f"{len(FIXTURES)} fixtures and {len(items)} ledger items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
