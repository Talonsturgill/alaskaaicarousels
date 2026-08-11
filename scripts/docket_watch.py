#!/usr/bin/env python3
"""The docket's eyes. Two keyless public sources, swept daily, into a queue.

WHAT PROBLEM THIS SOLVES. Every item on the Alaska AI Docket got there because
a person or an agent read a news story and noticed. That is a real way to run a
record and it has one failure mode that matters: a decision nobody wrote about
is a decision the docket does not know exists, and the comment window closes
whether or not anyone noticed it opened. The two bodies that publish the most
Alaska AI infrastructure decisions both publish machine readable notice of
them, for free, and nothing here was reading either one.

  BASIS             the Alaska Legislature's own system. Every bill, with the
                    status the Legislature itself considers current, and every
                    scheduled committee meeting. No key.

  Federal Register  every federal notice, rule and proposed rule, with the
                    comment close date attached. No key.

THIS FILE NEVER WRITES THE DOCKET. It writes ledger/watch.json, a queue of
CANDIDATES and OBSERVATIONS for the routine's verification phase to triage. The
docket's value is that a human or a checked agent stood behind every entry, and
a collector that could add entries on its own would spend that in a week. What
this removes is the part that was luck, not the part that was judgement.

WHY THE FEDERAL REGISTER IS FILTERED BY AGENCY AND NOT BY TOPIC. Searching its
full text for Alaska returns marine mammal take authorisations, Boeing
airworthiness directives and Head Start paperwork notices, because the word
appears somewhere in the document rather than being its subject. Measured on
2026-08-10: 77 documents with open comment windows matched the term, and
almost none were on this beat. The same query scoped to FERC returned Kodiak
Electric, the Alaska Energy Authority, Southeast Alaska Power Agency and
Copper Valley Electric, which is already a tracked item. The agency list below
is the precision.

A FAILED FETCH IS RECORDED AS A FAILED FETCH. Nothing is carried forward from
the last run, because a queue that silently repeats yesterday's candidates
reads to a reviewer as a quiet day rather than a broken collector.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCKET = os.path.join(REPO, "ledger", "docket.json")
WATCH = os.path.join(REPO, "ledger", "watch.json")

UA = "AlaskaAI-DocketWatch/1.0 (+https://alaskaaihq.com; docket@alaskaaihq.com)"
TIMEOUT = 45

BASIS = "https://www.akleg.gov/publicservice/basis"
BASIS_NS = "{http://www.legis.state.ak.us/Basis}"
FEDREG = "https://www.federalregister.gov/api/v1/documents.json"

# The bodies that decide Alaska AI infrastructure in the Federal Register. Each
# was checked against a live query before being listed, and the ones that
# returned nothing on beat are not here. FERC arrives under the Energy
# Department in the agencies field but has its own slug, and both are kept
# because a notice can be filed under either.
FED_AGENCIES = [
    ("federal-energy-regulatory-commission", "FERC"),
    ("land-management-bureau", "BLM"),
    ("air-force-department", "the Air Force"),
    ("energy-department", "the US DOE"),
    ("army-department", "the Army"),
]

# What makes a bill worth a reviewer's attention. Deliberately wide, because
# this is a queue somebody reads and not a publisher. A false positive costs a
# glance; a false negative costs a comment window.
BILL_TERMS = re.compile(
    r"DATA CENTER|ARTIFICIAL INTELLIGENCE|\bAI\b|COMPUTE|COMPUTER"
    r"|LARGE ENERGY|ENERGY USE|UTILIT|ELECTRIC|POWER|GRID|INTERTIE"
    r"|TRANSMISSION|GENERATION|NUCLEAR|MICROREACTOR|GEOTHERMAL"
    r"|NATURAL GAS|\bLNG\b|CARBON|BROADBAND|FIBER|DATA PRIVACY", re.I)

FED_TERMS = re.compile(
    r"data cent|artificial intelligence|\bAI\b|computing|hyperscale"
    r"|lease|right-of-way|interconnect|transmission|generat|reactor"
    r"|carbon|geotherm|hydro|power|energy", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def tracked(items):
    """What the docket already knows, indexed the ways a source names it.

    A bill is matched on its number because BASIS spells it "HB 259" with
    padding and the docket slug spells it hb-259. A federal document is matched
    on its own document number, which nothing else collides with.
    """
    bills, docs, titles = {}, set(), []
    for it in items:
        blob = f"{it['id']} {it['title']}"
        for m in re.finditer(r"\b([HS][BCJR]?)\s*-?\s*(\d{1,4})\b", blob, re.I):
            bills[f"{m.group(1).upper()}{m.group(2)}"] = it["id"]
        for s in it.get("sources") or []:
            m = re.search(r"federalregister\.gov/(?:d|documents)/([0-9-]+)",
                          s.get("url", ""))
            if m:
                docs.add(m.group(1))
        titles.append((it["id"], it["title"].lower()))
    return bills, docs, titles


def bill_key(number, chamber):
    """HB 259 out of BASIS's padded "HB   259" plus its chamber."""
    n = re.sub(r"\s+", "", number or "").upper()
    return n if n else f"{chamber}{number}".upper()


def sweep_basis(session, known_bills, today, out):
    """Bill status straight from the body that sets it, plus every scheduled
    hearing. A hearing is a FORWARD date, which is the thing this record exists
    to publish and the thing it could not previously see."""
    try:
        raw = fetch(f"{BASIS}/bills?session={session}")
        root = ET.fromstring(raw)
    except Exception as e:
        out["failed"].append({"source": "basis-bills", "error": str(e)[:180]})
        return set()

    watched_committees = set()
    seen = 0
    for b in root.iter(f"{BASIS_NS}Bill") or []:
        seen += 1
    if not seen:  # BASIS answers without the namespace on the inner elements
        bills = list(root.iter("Bill"))
    else:
        bills = list(root.iter(f"{BASIS_NS}Bill"))

    def text(el, tag):
        n = el.find(tag) if el.find(tag) is not None else el.find(BASIS_NS + tag)
        return (n.text or "").strip() if n is not None else ""

    for b in bills:
        num = bill_key(b.get("billnumber", ""), b.get("chamber", ""))
        title = text(b, "ShortTitle")
        status = text(b, "StatusText")
        when = text(b, "StatusDate")
        comm_el = b.find("CurrentCommittee")
        if comm_el is None:
            comm_el = b.find(BASIS_NS + "CurrentCommittee")
        comm = (comm_el.get("committeecode") if comm_el is not None else "") or ""
        rec = {"bill": num, "title": title, "status": status,
               "status_date": when, "committee": comm,
               "url": f"https://www.akleg.gov/basis/Bill/Detail/{session}?Root={num}"}
        if num in known_bills:
            # Already tracked. This is an OBSERVATION, not a candidate: the
            # reviewer compares it to what the docket currently says.
            rec["docket_id"] = known_bills[num]
            out["bills"].append(rec)
            if comm:
                watched_committees.add(comm)
        elif BILL_TERMS.search(f"{num} {title}"):
            out["candidates"].append({**rec, "source": "basis", "why": "bill on beat"})
    out["counted"]["basis_bills"] = len(bills)
    return watched_committees


def sweep_hearings(session, committees, today, out):
    if not committees:
        return
    try:
        raw = fetch(f"{BASIS}/meetings?session={session}")
        root = ET.fromstring(raw)
    except Exception as e:
        out["failed"].append({"source": "basis-meetings", "error": str(e)[:180]})
        return
    meetings = list(root.iter("Meeting")) or list(root.iter(f"{BASIS_NS}Meeting"))
    out["counted"]["basis_meetings"] = len(meetings)

    def text(el, tag):
        n = el.find(tag) if el.find(tag) is not None else el.find(BASIS_NS + tag)
        return (n.text or "").strip() if n is not None else ""

    horizon = (today + timedelta(days=120)).isoformat()
    for m in meetings:
        sched = text(m, "Schedule")[:10]
        if not sched or sched < today.isoformat() or sched > horizon:
            continue
        sp = m.find("Sponsor")
        if sp is None:
            sp = m.find(BASIS_NS + "Sponsor")
        code = (sp.text or "").strip() if sp is not None else ""
        if code not in committees:
            continue
        out["hearings"].append({
            "on": sched, "committee": code, "chamber": text(m, "chamber"),
            "where": text(m, "Location"), "title": text(m, "Title"),
        })
    out["hearings"].sort(key=lambda h: h["on"])
    # Zero hearings is the normal answer for most of the year, and a reviewer
    # who reads zero as a broken collector stops trusting the whole queue.
    # Measured 2026-08-11: the feed carried 2,842 meetings and exactly one of
    # them was in the future, because the Legislature sits January to May.
    if not out["hearings"]:
        ahead = sum(1 for m in meetings if text(m, "Schedule")[:10] >= today.isoformat())
        out["note_hearings"] = (
            f"No upcoming hearing for a committee holding a tracked bill. "
            f"The feed carried {len(meetings)} meetings and {ahead} of them are "
            f"still ahead, so this is the Legislature being out of session "
            f"rather than the sweep failing.")


def sweep_fedreg(known_docs, titles, since, out):
    """One query per agency. Precision comes from the agency filter, so the
    term is only there to keep a national agency's whole output from arriving."""
    for slug, label in FED_AGENCIES:
        q = urllib.parse.urlencode({
            "per_page": 60,
            "order": "newest",
            "conditions[agencies][]": slug,
            "conditions[term]": "Alaska",
            "conditions[publication_date][gte]": since,
            "fields[]": "x",
        }, doseq=True).replace("fields%5B%5D=x", "&".join(
            f"fields%5B%5D={f}" for f in
            ("document_number", "title", "type", "publication_date",
             "comments_close_on", "html_url", "agencies", "abstract")))
        try:
            data = json.loads(fetch(f"{FEDREG}?{q}"))
        except Exception as e:
            out["failed"].append({"source": f"fedreg-{slug}", "error": str(e)[:180]})
            continue
        out["counted"][f"fedreg_{slug}"] = data.get("count", 0)
        for r in data.get("results") or []:
            num = r.get("document_number") or ""
            if num in known_docs:
                continue
            blob = f"{r.get('title','')} {r.get('abstract') or ''}"
            if not FED_TERMS.search(blob):
                continue
            # Already covered by a tracked item under a different name.
            low = r.get("title", "").lower()
            dupe = next((i for i, t in titles
                         if len(set(t.split()) & set(low.split())) >= 4), "")
            out["candidates"].append({
                "source": "federal-register",
                "why": f"{label} notice on beat",
                "doc": num,
                "title": r.get("title", ""),
                "type": r.get("type", ""),
                "published": r.get("publication_date", ""),
                "comments_close_on": r.get("comments_close_on"),
                "url": r.get("html_url", ""),
                "agencies": [a.get("name", "") for a in (r.get("agencies") or [])],
                **({"maybe_tracked": dupe} if dupe else {}),
            })


def build(today=None, session="34", days=45):
    today = today or date.today()
    raw = json.loads(open(DOCKET).read())
    items = raw["items"] if isinstance(raw, dict) else raw
    known_bills, known_docs, titles = tracked(items)

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "for_date": today.isoformat(),
        "session": session,
        "counted": {},
        "bills": [],
        "hearings": [],
        "candidates": [],
        "failed": [],
    }
    committees = sweep_basis(session, known_bills, today, out)
    sweep_hearings(session, committees, today, out)
    sweep_fedreg(known_docs, titles, (today - timedelta(days=days)).isoformat(), out)

    # One notice, one candidate. A FERC document is filed under the Energy
    # Department too, so the agency sweep sees the same thing twice by design,
    # and a reviewer reading it twice would reasonably conclude the queue is
    # broken. The agencies that surfaced it are merged rather than dropped,
    # because which body filed it is part of what a reviewer is judging.
    merged, order = {}, []
    for c in out["candidates"]:
        key = c.get("doc") or c.get("bill") or c.get("title", "")
        if key in merged:
            prev = merged[key]
            if c["why"] not in prev["why"]:
                prev["why"] += ", " + c["why"]
            continue
        merged[key] = c
        order.append(key)
    out["candidates"] = [merged[k] for k in order]

    # A candidate list nobody can get to the bottom of is a list nobody reads.
    out["candidates"] = out["candidates"][:60]
    return out


# --------------------------------------------------------------- self test
#
# Hermetic. Every network call is replaced with a recorded response, because a
# gate that needs the Legislature to be up is a gate that goes red on their
# maintenance window and teaches everyone to ignore it.

FIXTURE_BILLS = """<?xml version="1.0"?>
<Basis xmlns="http://www.legis.state.ak.us/Basis"><Bills xmlns="">
<Bill billnumber="HB   259" chamber="H">
  <ShortTitle>LARGE ENERGY USE FACILITIES</ShortTitle>
  <StatusText statuscode="002">(H) ENE</StatusText>
  <StatusDate>2026-01-20</StatusDate>
  <CurrentCommittee committeecode="ENE">ENERGY</CurrentCommittee>
</Bill>
<Bill billnumber="HB   404" chamber="H">
  <ShortTitle>DATA CENTER WATER USE</ShortTitle>
  <StatusText statuscode="002">(H) RES</StatusText>
  <StatusDate>2026-08-01</StatusDate>
  <CurrentCommittee committeecode="RES">RESOURCES</CurrentCommittee>
</Bill>
<Bill billnumber="HB   777" chamber="H">
  <ShortTitle>MOOSE HUNTING SEASONS</ShortTitle>
  <StatusText statuscode="002">(H) RES</StatusText>
  <StatusDate>2026-08-01</StatusDate>
</Bill>
</Bills></Basis>"""

FIXTURE_MEETINGS = """<?xml version="1.0"?>
<Basis xmlns="http://www.legis.state.ak.us/Basis"><Meetings xmlns="">
<Meeting><chamber>H</chamber><Schedule>2026-08-20T09:00:00-09:00</Schedule>
  <Location>CAPITOL 106</Location><Sponsor type="Standing Committee">ENE</Sponsor>
  <Title>LARGE ENERGY USE FACILITIES</Title></Meeting>
<Meeting><chamber>H</chamber><Schedule>2026-08-21T09:00:00-09:00</Schedule>
  <Location>CAPITOL 124</Location><Sponsor type="Standing Committee">FSH</Sponsor>
  <Title>SALMON</Title></Meeting>
<Meeting><chamber>H</chamber><Schedule>1999-01-06T09:00:00-09:00</Schedule>
  <Location>OLD</Location><Sponsor type="Standing Committee">ENE</Sponsor>
  <Title>ANCIENT HEARING</Title></Meeting>
<Meeting><chamber>H</chamber><Schedule>2099-01-06T09:00:00-09:00</Schedule>
  <Location>FAR</Location><Sponsor type="Standing Committee">ENE</Sponsor>
  <Title>HEARING BEYOND THE HORIZON</Title></Meeting>
</Meetings></Basis>"""

FIXTURE_FEDREG = json.dumps({"count": 2, "results": [
    {"document_number": "2026-99999", "title": "Notice of Intent, Alaska data center lease",
     "type": "Notice", "publication_date": "2026-08-01",
     "comments_close_on": "2026-09-01", "html_url": "https://x/1",
     "agencies": [{"name": "Interior Department"}], "abstract": "A lease."},
    {"document_number": "2026-00001", "title": "Moose survey methodology",
     "type": "Notice", "publication_date": "2026-08-02", "comments_close_on": None,
     "html_url": "https://x/2", "agencies": [{"name": "Interior"}], "abstract": ""},
]})


def self_test():
    print("the docket's eyes")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    global fetch
    real = fetch
    calls = []

    def fake(url):
        calls.append(url)
        if "/bills" in url:
            return FIXTURE_BILLS.encode()
        if "/meetings" in url:
            return FIXTURE_MEETINGS.encode()
        return FIXTURE_FEDREG.encode()

    fetch = fake
    try:
        out = build(date(2026, 8, 10))
    finally:
        fetch = real

    print("it reads the record it is meant to be watching")
    check("a tracked bill comes back as an observation",
          any(b["bill"] == "HB259" for b in out["bills"]),
          str([b["bill"] for b in out["bills"]]))
    obs = next((b for b in out["bills"] if b["bill"] == "HB259"), {})
    check("carrying the Legislature's own status", obs.get("status") == "(H) ENE",
          obs.get("status", ""))
    check("and pointing back at the docket item it belongs to",
          obs.get("docket_id") == "hb-259-data-center-utility-standards",
          obs.get("docket_id", ""))
    check("a tracked bill is never also a candidate",
          not any(c.get("bill") == "HB259" for c in out["candidates"]))

    print("it finds what the record has not got")
    check("an untracked bill on beat becomes a candidate",
          any(c.get("bill") == "HB404" for c in out["candidates"]),
          str([c.get("bill") or c.get("doc") for c in out["candidates"]]))
    check("a bill off beat is left alone",
          not any(c.get("bill") == "HB777" for c in out["candidates"]))
    check("a federal notice on beat becomes a candidate",
          any(c.get("doc") == "2026-99999" for c in out["candidates"]))
    check("a federal notice off beat is left alone",
          not any(c.get("doc") == "2026-00001" for c in out["candidates"]))
    cand = next((c for c in out["candidates"] if c.get("doc") == "2026-99999"), {})
    check("a comment window is carried with it",
          cand.get("comments_close_on") == "2026-09-01",
          str(cand.get("comments_close_on")))

    print("hearings, which is the half that looks forward")
    check("a future hearing of a watched committee is kept",
          any(h["title"] == "LARGE ENERGY USE FACILITIES" for h in out["hearings"]),
          str([h["title"] for h in out["hearings"]]))
    check("a hearing of a committee holding nothing tracked is not",
          not any(h["title"] == "SALMON" for h in out["hearings"]))
    check("a hearing in the past is not",
          not any(h["title"] == "ANCIENT HEARING" for h in out["hearings"]))
    check("nor one scheduled beyond the horizon this record can see",
          not any(h["title"] == "HEARING BEYOND THE HORIZON" for h in out["hearings"]))
    check("a federal notice filed under two agencies appears once",
          sum(1 for c in out["candidates"] if c.get("doc") == "2026-99999") == 1,
          str([c.get("doc") or c.get("bill") for c in out["candidates"]]))

    print("it cannot touch the docket")
    src = open(os.path.abspath(__file__)).read()
    body = src.split("def self_test", 1)[0]
    check("this file never opens the docket for writing",
          'open(DOCKET, "w")' not in body and "open(DOCKET,'w')" not in body
          and "'w'" not in body.split("DOCKET")[1][:200])
    writes = re.findall(r'open\(\s*([A-Za-z_]+)\s*,\s*["\']w', body)
    check("and the only thing it opens for writing is the queue",
          set(writes) <= {"WATCH"}, str(writes))

    print("a bad day is recorded as a bad day")
    fetch = lambda url: (_ for _ in ()).throw(urllib.error.URLError("down"))
    try:
        bad = build(date(2026, 8, 10))
    finally:
        fetch = real
    check("every failed source is named", len(bad["failed"]) >= 2,
          str([f["source"] for f in bad["failed"]]))
    check("and nothing is invented to fill the gap",
          not bad["bills"] and not bad["candidates"] and not bad["hearings"])

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--session", default="34")
    ap.add_argument("--days", type=int, default=45)
    ap.add_argument("--write", action="store_true", help="write ledger/watch.json")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    out = build(session=args.session, days=args.days)
    if args.write:
        with open(WATCH, "w") as f:
            json.dump(out, f, indent=1, sort_keys=False)
            f.write("\n")
        print(f"wrote {WATCH}")
    print(f"{len(out['bills'])} tracked bills observed, "
          f"{len(out['hearings'])} upcoming hearings, "
          f"{len(out['candidates'])} candidates, "
          f"{len(out['failed'])} sources failed")
    for f in out["failed"]:
        print(f"  FAILED {f['source']}  {f['error'][:90]}")
    for b in out["bills"]:
        print(f"  BILL   {b['bill']:<7} {b['status']:<16} {b['status_date']}  -> {b.get('docket_id','')}")
    if out.get("note_hearings"):
        print(f"  NOTE   {out['note_hearings']}")
    for h in out["hearings"][:8]:
        print(f"  HEARING {h['on']}  {h['committee']:<4} {h['title'][:56]}")
    for c in out["candidates"][:14]:
        tag = c.get("bill") or c.get("doc") or ""
        close = c.get("comments_close_on") or ""
        print(f"  CAND   {tag:<12} {close:<11}{c['title'][:62]}")
    # Nothing to say is a real answer, and an exit code nobody can act on is
    # not. 0 always, because this informs a review rather than gating a build.
    return 0


if __name__ == "__main__":
    sys.exit(main())
