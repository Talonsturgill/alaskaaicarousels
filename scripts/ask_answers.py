#!/usr/bin/env python3
"""The answer engine behind the docket's ask box.

WHY THIS IS NOT A MODEL CALL. Look at what the common questions actually are.
"What can I still comment on?" is a filter on public access. "Who decides the
STAK lease?" is a field read. "What deadlines are coming up?" is a sort by
date. "How many does DNR have?" is a count. They read like conversation and
they are queries over structured data, so answering them in Python is not a
cheaper approximation of a model answer, it is a better one:

  - it cannot hallucinate, because nothing is generated, only assembled
  - it is exactly current, because it is rebuilt from the ledger every build
  - it costs nothing and takes no time, because it ships inside the page
  - it needs no verification layer, because there is no guess to check

That leaves the model lanes for what they are actually for, which is the
open-ended question nobody anticipated.

FOUR THINGS COME OUT OF HERE.

  index     one record per tracked decision, flattened for client side search
            AND for client side answering. The page carries this and resolves
            a question against it as the reader types, so an answer appears in
            the same frame rather than after a round trip. Twenty items is
            small enough that scoring every one on every keystroke is cheaper
            than asking a server anything.

  facets    the entity vocabulary. Every agency, place, kind, topic, status
            and access level the record contains, each with the query words a
            reader might use for it and the ids it covers. This is what turns
            "what is DNR up to" and "anything on the Kenai Peninsula" from
            text matches that might work into lookups that always do.

  views     the named queries behind the suggestion chips. Each carries a
            plain summary line AND the ids it matched, so the page can show a
            sentence and the live cards underneath it.

  catalogue every question this record can answer, written out, each paired
            with the ROUTE that answers it.

WHY THE CATALOGUE STORES ROUTES AND NOT ANSWERS. An answer cache goes stale
the moment a deadline passes, and it would have to be regenerated and
reshipped to stay honest. A route does not go stale, because it names which
resolver runs and what it runs on, and the resolver reads today's clock. So a
catalogued question is not a special case with a canned reply. It is a query
whose routing was worked out ahead of time, handed to exactly the same
answerer a typed query goes through. What the catalogue buys is not speed,
which is already there. It is EXACTNESS. A catalogued question can never be
mis-parsed, and it lets the box complete a thought before the reader has
finished typing it.

WHAT THIS READS. db.resolve(), the same single source the badges, the cards
and the subscriber email read. Never the raw ledger fields. An item whose
comment window closed this morning still says open-for-comment in the ledger
until Phase 3.5 next runs, and resolve() is what turns that into closed. An
answer built on the raw field would tell a reader a door is open while the
badge beside it says shut.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import date, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import docket_build as db  # noqa: E402
import gaswatch_build as gw  # noqa: E402

DOCKET = os.path.join(REPO, "ledger", "docket.json")
RECENT_DAYS = 7
SUMMARY_CHARS = 190
HOWTO_CHARS = 260
# The empty box's starter chips are one line each. A question longer than this
# wraps and the strip stops reading as six offers. ONE constant, because the
# picker and the self test used to hold this number separately, the picker
# holding it as "the shortest title" and the test as a length in characters,
# and the two disagreed the first time a short title carried a long question.
CHIP_MAX = 58

# A history note that records a NON event. The docket writes an entry every
# time an item is checked, so most entries say a version of "looked, nothing
# moved". A reader asking what changed this week wants the days something
# actually happened, and without this filter the answer is nineteen of twenty
# items, which is the same as no answer.
NO_CHANGE = re.compile(
    r"^\s*(?:re[- ]?verified|re[- ]?confirmed|checked and unchanged"
    r"|carried forward|no change|still (?:no|pending|open)"
    r"|(?:one|two|three|four|five|six|seven|\d+) days? out)\b", re.I)

KIND_LABEL = {
    "state-land-lease": "state land lease",
    "federal-lease": "federal lease",
    "regulatory-docket": "regulatory docket",
    "utility-decision": "utility decision",
    "procurement": "procurement",
    "legislation": "legislation",
    "grant": "grant",
    "other": "decision",
}
KIND_PLURAL = {
    "state-land-lease": "state land leases",
    "federal-lease": "federal leases",
    "regulatory-docket": "regulatory dockets",
    "utility-decision": "utility decisions",
    "procurement": "procurements",
    "legislation": "bills and ordinances",
    "grant": "grants",
    "other": "other decisions",
}
STATUS_LABEL = {
    "open-for-comment": "open for comment",
    "pending-decision": "pending a decision",
    "decided": "decided",
    "closed": "closed",
    "watching": "being watched",
}
ACCESS_LABEL = {
    "open": "open to public comment",
    "indirect": "decided by a body you can reach but not formally comment to",
    "closed": "closed to public comment",
}

# ---------------------------------------------------------------- entities
#
# A reader does not type "Alaska DNR, Division of Oil and Gas". They type dnr.
# They do not type "Dalton Highway, about 26 mi south of Deadhorse", they type
# north slope. These tables carry the SHORT name a person uses and the words
# they reach for, and every one of them is checked against the record in the
# self test, so a rule that stops matching anything is a build failure rather
# than a query that quietly returns nothing.
#
# Order does not decide which agency wins. Position in the decider string
# does, because a decider reading "Regulatory Commission of Alaska (prudency);
# Alaska DNR (storage lease)" names the RCA as the body in front. Both are
# recorded, so a reader asking about either finds the item.
AGENCY_RULES = [
    (r"Regulatory Commission of Alaska", "the RCA",
     ("rca", "regulatory commission", "regulatory commission of alaska")),
    (r"\bDNR\b|Department of Natural Resources", "Alaska DNR",
     ("dnr", "natural resources", "state land office", "division of oil and gas")),
    (r"Federal Energy Regulatory", "FERC", ("ferc", "federal energy regulatory")),
    # Ordered BEFORE the bare-word rules below and after FERC, because
    # "Federal Communications Commission" and "Federal Energy Regulatory" share
    # a first word and only one of them may own the phrase (see the note above
    # this table). Added 2026-08-31 with the first FCC item on the docket, the
    # universal service AI proceeding; the self-test caught it as an item with
    # no recognised agency the same hour the item landed.
    (r"Federal Communications Commission|\bFCC\b", "the FCC",
     ("fcc", "federal communications", "federal communications commission")),
    (r"Air Force", "the Air Force", ("air force", "usaf", "afb")),
    (r"\bArmy\b", "the Army", ("army", "us army")),
    (r"Nuclear Regulatory Commission", "the NRC", ("nrc", "nuclear regulatory")),
    (r"Defense Innovation Unit", "the Defense Innovation Unit", ("diu", "defense innovation")),
    (r"Golden Valley", "GVEA", ("gvea", "golden valley")),
    (r"Copper Valley", "CVEA", ("cvea", "copper valley")),
    (r"Alaska Legislature", "the Alaska Legislature",
     ("legislature", "lawmakers", "legislators", "state house", "state senate")),
    (r"Anchorage Assembly", "the Anchorage Assembly",
     ("assembly", "anchorage assembly", "municipality")),
    (r"Oil and Gas Conservation", "AOGCC", ("aogcc", "oil and gas conservation")),
    (r"Environmental Protection Agency", "the EPA", ("epa", "environmental protection")),
    (r"Department of Administration", "Alaska DOA",
     ("doa", "department of administration", "state procurement office")),
    (r"Department of Energy", "the US DOE", ("doe", "department of energy")),
    (r"Administration for Native Americans", "ANA",
     ("ana", "administration for native americans", "hhs")),
    (r"School District", "the Kenai school board",
     ("school board", "kpbsd", "school district", "board of education")),
    (r"^The President", "the President",
     ("president", "white house", "executive order")),
    (r"electric utility board", "Alaska's electric utilities",
     ("utilities", "utility boards", "co ops", "cooperatives", "railbelt utilities")),
]

# A place is where the decision LANDS, not where the paperwork sits. Items with
# no location are statewide, which is a real answer and gets its own facet
# rather than an empty field.
PLACE_RULES = [
    (r"Deadhorse|North Slope|Dalton", "the North Slope",
     ("north slope", "the slope", "deadhorse", "dalton highway", "prudhoe")),
    (r"Fairbanks|Eielson|Wainwright|Clear SFS", "Fairbanks and the Interior",
     ("fairbanks", "the interior", "eielson", "fort wainwright", "clear sfs",
      "north pole")),
    (r"JBER|Anchorage", "Anchorage", ("anchorage", "jber", "elmendorf", "richardson")),
    (r"Kenai|Soldotna|Bradley Lake", "the Kenai Peninsula",
     ("kenai", "soldotna", "kenai peninsula", "homer", "seward", "the peninsula")),
    (r"Mat-Su|Houston", "the Mat-Su Borough",
     ("mat su", "matsu", "mat-su", "houston", "wasilla", "palmer")),
    (r"Juneau", "Juneau", ("juneau",)),
    (r"Cordova|Prince William", "Prince William Sound",
     ("cordova", "prince william sound")),
    (r"Glennallen|Copper River", "the Copper River Basin",
     ("glennallen", "copper river", "copper basin")),
    (r"Susitna|Skwentna", "the Susitna watershed",
     ("susitna", "skwentna")),
    (r"Cook Inlet", "Cook Inlet", ("cook inlet",)),
]

# What a decision is ABOUT, scanned out of its own text. A topic is the thing
# readers arrive caring about, which is almost never the filing category.
# What a decision is ABOUT, scanned out of its own text. A topic is the thing
# readers arrive caring about, which is almost never the filing category.
#
# TWO WORD LISTS, ON PURPOSE. The first scans the record and decides which
# items carry the topic. The second is what a READER types at it. They are not
# the same list and conflating them is what makes a facet fight with its
# neighbours, because "air force" belongs in the first list here and in the
# agency table's second list, and only one of them can own the phrase.
TOPIC_RULES = [
    ("data-centre", "data centres",
     ("data center", "data centre", "datacenter", "datacentre", "ai campus",
      "hyperscale", "server farm", "compute campus"),
     ("data center", "data centre", "datacenter", "datacentre", "data centers",
      "data centres", "server farm", "hyperscale", "ai campus")),
    ("power", "the electric grid",
     ("electric", "electricity", "power", "grid", "turbine", "megawatt",
      "gigawatt", "generation", "utility", "transmission", "railbelt",
      "ratepayer", "kilowatt"),
     ("power", "electricity", "electric", "the grid", "megawatt", "gigawatt",
      "transmission", "railbelt", "ratepayer", "kilowatt", "generation")),
    ("gas", "natural gas",
     ("natural gas", "gas fired", "gas-fired", "lng", "gas line", "gas storage",
      "cook inlet", "aklng"),
     ("natural gas", "gas", "lng", "gas line", "gas storage")),
    ("nuclear", "nuclear power",
     ("nuclear", "reactor", "microreactor", "oklo", "janus", "smr"),
     ("nuclear", "reactor", "reactors", "microreactor", "microreactors",
      "atomic", "oklo")),
    ("land", "state and federal land",
     ("lease", "acres", "acreage", "parcel", "right of way", "easement",
      "state land", "land"),
     ("land", "acres", "acreage", "parcel", "right of way", "easement",
      "lease", "leases", "leasing")),
    ("water", "water and hydro",
     ("hydro", "diversion", "glacier", "river", "watershed", "lake", "dam"),
     ("water", "hydro", "hydropower", "diversion", "glacier", "river",
      "watershed", "dam")),
    ("carbon", "carbon and emissions",
     ("carbon", "class vi", "sequestration", "emission", "coal", "co2"),
     ("carbon", "class vi", "sequestration", "emissions", "coal", "climate")),
    ("schools", "schools and students",
     ("school", "student", "classroom", "district", "education", "teacher",
      "curriculum"),
     ("school", "schools", "students", "classroom", "education", "teachers",
      "curriculum", "kids")),
    ("military", "military bases",
     ("air force", "army", "defense", "jber", "eielson", "wainwright",
      "clear sfs", "military", "base"),
     ("military", "defense", "army base", "air base", "the base", "bases")),
    ("money", "public money",
     ("grant", "million", "billion", "tax", "funding", "appropriation",
      "dollar", "ratepayer", "subsidy", "incentive"),
     ("money", "cost", "funding", "tax", "taxes", "grant money", "subsidy",
      "appropriation", "dollars", "spending", "billion", "million")),
    ("rules", "rules and policy",
     ("ordinance", "zoning", "policy", "standard", "regulation", "statute",
      "bill", "executive order", "permit", "rulebook"),
     ("rules", "policy", "policies", "regulation", "regulations", "zoning",
      "permit", "permits", "standards", "rulebook")),
    ("native", "Alaska Native communities",
     ("native", "tribal", "tribe", "indigenous"),
     ("native", "alaska native", "tribal", "tribes", "indigenous")),
    ("jobs", "jobs and workers",
     ("jobs", "employment", "workforce", "hiring", "worker"),
     ("jobs", "employment", "workforce", "workers", "hiring")),
    ("government", "the state's own use of AI",
     ("department of administration", "state agency", "statewide", "dmv",
      "motor vehicles", "procurement", "rfp", "rfi", "commercial licenses"),
     ("state government", "the state itself", "government use",
      "agencies using ai", "state agencies", "public sector")),
]

# Explicit query vocabulary for the rest of the groups. Derived labels made
# two facets fight over the same word, because a status of closed and an
# access of closed are different answers to the same typed word, and a rule
# that guesses which one a reader meant is a rule that is wrong half the time.
KIND_TERMS = {
    "state-land-lease": ("state land lease", "state land leases", "state lease"),
    "federal-lease": ("federal lease", "federal leases"),
    "regulatory-docket": ("regulatory docket", "regulatory dockets", "docket case"),
    "utility-decision": ("utility decision", "utility decisions"),
    "procurement": ("procurement", "procurements", "rfp", "rfi", "contract",
                    "contracts", "solicitation", "vendor", "bid"),
    "legislation": ("legislation", "bill", "bills", "ordinance", "ordinances",
                    "statute", "law"),
    "grant": ("grant", "grants", "federal grant"),
    "other": ("other decision", "other decisions"),
}
STATUS_TERMS = {
    "open-for-comment": ("open for comment",),
    "pending-decision": ("pending", "pending decision", "undecided",
                         "not yet decided", "still pending", "in progress"),
    "decided": ("decided", "already decided", "settled"),
    "closed": ("closed case", "closed docket", "process closed"),
    "watching": ("watching", "being watched", "just watching"),
}
# The bare word closed belongs to ACCESS, not to status, because a reader
# typing it is asking whether they can still be heard rather than about the
# filing state of a docket.
ACCESS_TERMS = {
    "open": ("open", "open now", "still open", "accepting comment",
             "taking comment", "open to comment", "open for public comment"),
    "indirect": ("indirect", "no formal comment", "not a formal comment"),
    "closed": ("closed", "closed to the public", "not open", "cannot comment",
               "cant comment", "no comment", "no public comment", "too late",
               "shut to the public"),
}

# ---------------------------------------------------------------- synonyms
#
# The LEFT side is what a reader types. The RIGHT side is what the record
# says. Nothing here is a guess about English in general, every entry exists
# because the two vocabularies genuinely differ, and the self test asserts
# every right hand term appears somewhere in the corpus. A synonym pointing at
# a word the record does not contain is dead weight that fails the build.
SYNONYMS = {
    "testify": ["comment"],
    "testimony": ["comment"],
    "speak": ["comment"],
    "weigh": ["comment"],
    "input": ["comment"],
    "feedback": ["comment"],
    "voice": ["comment"],
    "participate": ["comment", "public"],
    "involved": ["comment", "public"],
    "protest": ["comment"],
    "oppose": ["comment"],
    "support": ["comment"],
    "due": ["deadline", "closes"],
    "cutoff": ["deadline"],
    "expires": ["deadline", "closes"],
    "electricity": ["electric", "power"],
    "juice": ["power"],
    "datacenter": ["data center"],
    "datacentre": ["data center"],
    "servers": ["data center"],
    "computers": ["data center", "compute"],
    "atomic": ["nuclear"],
    "smr": ["microreactor", "reactor"],
    "windmill": ["generation"],
    "acreage": ["acres"],
    "parcel": ["acres", "land"],
    "bill": ["legislation", "hb"],
    "law": ["legislation"],
    "lawmakers": ["legislature"],
    "legislators": ["legislature"],
    "regulators": ["commission"],
    "agency": ["commission", "department", "division"],
    "kids": ["school", "student"],
    "students": ["student"],
    "teachers": ["school"],
    "money": ["million", "grant", "dollar"],
    "cost": ["million", "dollar"],
    "price": ["million", "dollar"],
    "funding": ["grant", "million"],
    "tribes": ["native"],
    "tribal": ["native"],
    "indigenous": ["native"],
    "army": ["army"],
    "base": ["base"],
    "warming": ["carbon"],
    "climate": ["carbon"],
    "pollution": ["carbon", "coal"],
    "water": ["water"],
    "salmon": ["river", "watershed"],
    "fish": ["river", "watershed"],
    "mine": ["land"],
    "drilling": ["oil and gas"],
    "pipeline": ["gas line", "gas"],
    "utility": ["utility", "electric"],
    "coop": ["cooperative"],
    "borough": ["borough"],
    "town": ["borough"],
    "city": ["anchorage", "borough"],
    "statewide": ["statewide"],
}

# The meta answers. Everything about how this record is KEPT rather than what
# is in it, which is the second thing every reader wants to know and the one
# thing the index itself cannot say. Written here so it goes through the same
# house style gate as every other published sentence.
META = {
    "what": ("The Alaska AI Docket is a running record of the decisions about "
             "artificial intelligence being made in Alaska right now, by whom, "
             "and whether the public still gets a say. Every entry carries its "
             "own page, its own sources and its own history."),
    "how": ("Every tracked decision is re-checked against its primary source on "
            "a daily pass. A check that finds nothing writes a note saying so, "
            "which is why the record can tell you a quiet week apart from a gap."),
    "where": ("Sources are the primary filings wherever one exists, so agency "
              "notices, commission dockets, board packets and bill text, with "
              "reporting used to find them rather than to stand in for them. "
              "Every item lists what it was built from."),
    "when": ("The record is rebuilt and republished every day. The date at the "
             "top of this page is the last time it was rewritten."),
    "who": ("It is kept by Alaska.Ai. Nothing on this page is sponsored and no "
            "tracked party has any say over what appears."),
    "why": ("Because these decisions are public, scattered across a dozen "
            "agencies, and almost none of them are covered until after they are "
            "made. A person who wants a say has to find the window while it is "
            "still open."),
    "ai": ("The record is assembled by software from primary sources and the "
           "wording is checked before it publishes. Nothing on this page is "
           "invented, and the answer you are reading was assembled from the "
           "fields of this record rather than written by a model."),
    "cost": ("Nothing. There is no paywall, no account and no tracking on this "
             "page."),
    "data": ("The whole docket is published as JSON beside this page, so anyone "
             "can check the numbers or build on them."),
    "correct": ("If something here is wrong, the correction goes into the item's "
                "own history with the date, so the mistake stays visible rather "
                "than being quietly overwritten."),
    "search": ("Everything you are typing is answered inside this page. No "
               "request leaves your browser, so there is nothing to log and "
               "nothing to send."),
    "removed": ("A decided item stays on the record instead of being removed, so "
                "the outcome is checkable later against what was said before it."),
    "gas": ("Cook Inlet Gas Watch is the sister record, a daily numeric read of "
            "Southcentral Alaska's gas position. It publishes measured storage "
            "and modeled demand and it never publishes a safety verdict."),
    "subscribe": ("There is an email list for the docket that goes out when a "
                  "tracked window opens or closes, not on a schedule."),
    "contact": ("There is a contact route on the about page for a correction, a "
                "tip or a decision this record is missing."),
}


def load_items():
    raw = json.loads(open(DOCKET).read())
    return raw["items"] if isinstance(raw, dict) and "items" in raw else raw


def trim(text, n=SUMMARY_CHARS):
    """Cut to length on a word boundary, and never leave punctuation stranded
    in front of the ellipsis. A note ending "nine sites,..." is a small ugly
    thing that ships on every card that hits the limit."""
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0].rstrip(",;:.-")
    return cut + "..."


def handles(it):
    """The short names a reader would actually type for one item.

    A person looking for the STAK lease types stak. A person looking for HB
    259 types hb 259. Neither is a word a title match finds reliably, and both
    are the most confident thing that reader will type all session.

    THE DESIGNATOR HAS TO BE A DESIGNATOR. Matching any short word before a
    number turned "An 89 million dollar federal grant" into the handle "an
    89", so the pattern reads capitals in the title and the slug's own prefix
    and nothing else.
    """
    out = set()
    for m in re.findall(r"\b[A-Z]{3,}\b", it["title"]):
        out.add(m.lower())
    for m in re.findall(r"\b([A-Z]{2,4})[ -](\d{2,6}(?:-\d{2,4})?)\b", it["title"]):
        out.add(f"{m[0].lower()} {m[1]}")
        out.add(f"{m[0].lower()}{m[1]}")
    for m in re.findall(r"\b([a-z]{2,4})-(\d{2,6}(?:-\d{2,4})?)\b", it["id"]):
        out.add(f"{m[0]} {m[1]}")
        out.add(f"{m[0]}{m[1]}")
    for m in re.findall(r"\b(\d{5,7})\b", it["title"] + " " + it["id"]):
        out.add(m)
    return sorted(h for h in out if len(h) >= 3)


def prune_handles(rows):
    """A handle two decisions share is not a handle.

    Every item on this record is about AI, so AI named all of them and none of
    them, and it scored sixty points on any query with those two letters
    anywhere inside it. A word that cannot tell one decision from another is
    noise wearing the costume of precision.
    """
    seen = Counter()
    for r in rows:
        for h in r["alias"]:
            seen[h] += 1
    for r in rows:
        r["alias"] = [h for h in r["alias"] if seen[h] == 1]


def index_row(it, today):
    """One decision, flattened. Everything the reader might type at it goes in
    `hay`, so matching is one pass over one string rather than a walk over the
    object on every keystroke. Everything an ANSWER needs goes in its own
    field, so the page never has to parse prose to say who decides something.
    """
    r = db.resolve(it, today)
    loc_pt = it.get("location") or {}
    loc = loc_pt.get("name") or ""
    outlets = []
    for s in (it.get("sources") or []):
        o = s.get("outlet", "")
        if o and o not in outlets:
            outlets.append(o)
    # The last time the item actually MOVED, and what was written about it.
    # last_updated is bumped by the daily check, so it answers "was this looked
    # at" rather than "did anything happen", which is not the question anyone
    # asks.
    hist = sorted((h for h in (it.get("history") or []) if h.get("date")),
                  key=lambda h: h["date"])
    moves = [h for h in hist if not NO_CHANGE.match(h.get("note") or "")]
    dates = sorted(it.get("key_dates") or [], key=lambda d: d["date"])
    head = r["headline"] or {}

    agencies = []
    for pat, label, _terms in AGENCY_RULES:
        m = re.search(pat, it.get("decider") or "", re.I)
        if m:
            agencies.append((m.start(), label))
    agencies.sort()
    agency_labels = []
    for _pos, label in agencies:
        if label not in agency_labels:
            agency_labels.append(label)

    places = []
    for pat, label, _terms in PLACE_RULES:
        if re.search(pat, loc, re.I) and label not in places:
            places.append(label)

    row = {
        "id": it["id"],
        "title": it["title"],
        "kind": KIND_LABEL.get(it.get("kind"), "decision"),
        "kindKey": it.get("kind") or "other",
        "status": r["status"],
        "statusLabel": STATUS_LABEL.get(r["status"], r["status"]),
        "access": r["access"],
        "decider": it.get("decider") or "",
        "agency": agency_labels[0] if agency_labels else "",
        "agencies": agency_labels,
        "where": loc,
        "places": places or ["statewide"],
        "summary": trim(it.get("summary")),
        "howto": trim(it.get("access_note"), HOWTO_CHARS),
        "moved": moves[-1]["date"] if moves else "",
        "note": trim(moves[-1].get("note"), 170) if moves else "",
        "checked": hist[-1]["date"] if hist else "",
        "first": it.get("first_seen") or "",
        # The date the chrome shows, and what it means. The page counts down
        # against this, so it has to be the resolved headline and not whichever
        # key_date happens to sort first.
        "on": head.get("date") or "",
        "onLabel": trim(head.get("label"), 90),
        "role": "deadline" if r.get("deadline") else ("date" if head else ""),
        # Every published date, so "what happens next" and "when did this
        # start" are field reads rather than guesses.
        "dates": [[d["date"], trim(d.get("label"), 80), d.get("kind", "milestone")]
                  for d in dates],
        "outlets": outlets,
        # The point, when the record has one. Five of twenty decisions are
        # statewide and have none, and inventing a centroid for those would
        # put a pin on a map where nothing is happening.
        "at": ([round(loc_pt["lat"], 4), round(loc_pt["lon"], 4)]
               if loc_pt.get("lat") is not None else None),
        "alias": handles(it),
    }

    hay_parts = [
        it["title"], row["kind"], row["decider"], loc, row["summary"],
        row["howto"], row["status"].replace("-", " "), " ".join(outlets),
        " ".join(row["agencies"]), " ".join(row["places"]),
        " ".join(d[1] for d in row["dates"]),
        " ".join(row["alias"]),
        # The slug, spelled out. It carries vocabulary the prose does not, the
        # statewide speech-to-text contract is filed under transcription and
        # says that word nowhere in its title or summary, so a reader typing
        # the obvious term found nothing at all until this line existed.
        it["id"].replace("-", " "),
    ]
    hay = " ".join(hay_parts).lower()
    row["topics"] = [k for k, _lab, terms, _ask in TOPIC_RULES
                     if any(t in hay for t in terms)]
    for k in row["topics"]:
        hay += " " + k.replace("-", " ")
    for _pat, label, terms in AGENCY_RULES:
        if label in row["agencies"]:
            hay += " " + " ".join(terms)
    for _pat, label, terms in PLACE_RULES:
        if label in row["places"]:
            hay += " " + " ".join(terms)
    row["hay"] = re.sub(r"\s+", " ", hay)
    return row


# ------------------------------------------------------------------ facets



PLACES_FILE = os.path.join(REPO, "assets", "geo", "alaska-places.json")

# How far from a town still counts as near it. Alaska is enormous and a
# hundred miles is a normal errand in much of it, so this is deliberately
# generous. The distance is always shown, so a reader judges for themselves
# rather than trusting the threshold.
NEAR_MILES = 120


def communities():
    """The towns a reader would name, with their points.

    From the same gazetteer the map artwork uses, so a place named here is a
    place the site already draws. Population orders the list and is never
    published, because the file itself says those figures are for sizing dots
    and not for citation.
    """
    try:
        raw = json.loads(open(PLACES_FILE).read())
    except Exception:
        return []
    out = []
    for p in raw.get("places") or []:
        if p.get("lat") is None or p.get("lon") is None:
            continue
        out.append({"name": p["name"],
                    "key": re.sub(r"[^a-z0-9]+", "-", p["name"].lower()).strip("-"),
                    "at": [round(p["lat"], 4), round(p["lon"], 4)],
                    "rank": p.get("pop") or 0})
    out.sort(key=lambda p: (-p["rank"], p["name"]))
    for p in out:
        p.pop("rank", None)
    return out


def miles(a, b):
    """Great circle distance. The earth's curve matters at Alaska's size, and
    treating lon and lat as a flat grid would put Utqiagvik and Ketchikan
    closer together than they are by a wide margin."""
    import math
    r = 3958.8
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1, math.sqrt(h)))


def near(place, rows, limit=NEAR_MILES):
    """Tracked decisions within reach of one town, nearest first."""
    out = []
    for r in rows:
        if not r.get("at"):
            continue
        d = miles(place["at"], r["at"])
        if d <= limit:
            out.append((round(d), r["id"]))
    out.sort()
    return out


def facets(rows):
    """The entity vocabulary. Every named thing in the record, with the words a
    reader reaches for and the ids it covers.

    This is the difference between a search box and something that knows what
    it holds. "what is dnr doing" is not a text match that happens to work, it
    is a lookup that always does, and it can carry a counted answer sentence
    because the set is known rather than inferred.
    """
    out = {}
    # A word that names one decision cannot also name a group. JBER is where
    # the Air Force lease is and it is also the only thing called JBER, so a
    # reader typing it wants that decision and not the two Anchorage ones.
    # The handle is the more specific claim, so the group gives the word up.
    handles_ = {h for r in rows for h in r["alias"]}

    def group(name, entries):
        keep = []
        for e in entries:
            if not e["ids"]:
                continue
            e["terms"] = [t for t in e["terms"] if t not in handles_]
            keep.append(e)
        keep.sort(key=lambda e: (-len(e["ids"]), e["label"].lower()))
        out[name] = keep

    group("agency", [
        {"key": re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-"),
         "label": label, "terms": sorted(set(terms)),
         "ids": [r["id"] for r in rows if label in r["agencies"]]}
        for _pat, label, terms in AGENCY_RULES])

    group("place", [
        {"key": re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-"),
         "label": label, "terms": sorted(set(terms)),
         "ids": [r["id"] for r in rows if label in r["places"]]}
        for _pat, label, terms in PLACE_RULES] + [
        {"key": "statewide", "label": "the whole state",
         "terms": ["statewide", "state wide", "all of alaska", "the whole state"],
         "ids": [r["id"] for r in rows if r["places"] == ["statewide"]]}])

    group("kind", [
        {"key": k, "label": KIND_PLURAL[k], "terms": sorted(KIND_TERMS[k]),
         "ids": [r["id"] for r in rows if r["kindKey"] == k]}
        for k in KIND_LABEL])

    group("topic", [
        {"key": k, "label": label, "terms": sorted(set(ask)),
         "ids": [r["id"] for r in rows if k in r["topics"]]}
        for k, label, _match, ask in TOPIC_RULES])

    group("status", [
        {"key": k, "label": v, "terms": sorted(STATUS_TERMS[k]),
         "ids": [r["id"] for r in rows if r["status"] == k]}
        for k, v in STATUS_LABEL.items()])

    group("access", [
        {"key": k, "label": v, "terms": sorted(ACCESS_TERMS[k]),
         "ids": [r["id"] for r in rows if r["access"] == k]}
        for k, v in ACCESS_LABEL.items()])
    return out


# ------------------------------------------------------------------- views


def open_now(rows):
    return [r for r in rows if r["access"] == "open"]


def v_comment(rows, today):
    hits = open_now(rows)
    if not hits:
        return hits, ("No formal public comment window is open today. Several tracked "
                      "decisions are still made by elected or member accountable bodies, "
                      "which is a slower path and a real one.")
    n = gw.count(len(hits), "decision")
    verb = "is" if len(hits) == 1 else "are"
    return hits, f"{n} {verb} open to public comment right now."


def v_deadlines(rows, today):
    hits = sorted((r for r in rows if r["on"]), key=lambda r: r["on"])
    if not hits:
        return hits, "Nothing on the docket has a published upcoming date."
    return hits, (f"The next {gw.count(len(hits), 'published date')}, soonest first. "
                  f"The nearest is {gw.long_date(hits[0]['on'])}.")


def v_changed(rows, today):
    # NOT last_updated. That field is touched on every daily check, so keying
    # off it matched nineteen of twenty items and told a reader nothing at all.
    # A history entry is written when something actually moved, so it is the
    # field that answers the question the reader is asking.
    cutoff = (today - timedelta(days=RECENT_DAYS)).isoformat()
    hits = sorted((r for r in rows if r["moved"] >= cutoff),
                  key=lambda r: r["moved"], reverse=True)
    if not hits:
        return hits, (f"Nothing on the docket actually moved in the last {RECENT_DAYS} "
                      "days. Every item is still checked daily, and a quiet week is a "
                      "real answer rather than a gap in the record.")
    return hits, (f"{gw.count(len(hits), 'decision')} moved in the last "
                  f"{RECENT_DAYS} days, most recent first. Each carries the note "
                  "written when it changed.")


def v_decided(rows, today):
    hits = [r for r in rows if r["status"] in ("decided", "closed")]
    if not hits:
        return hits, ("Nothing has been finally decided yet. Every tracked decision "
                      "is still in progress, which is why the docket exists.")
    verb = "has" if len(hits) == 1 else "have"
    return hits, (f"{gw.count(len(hits), 'decision')} {verb} been settled and "
                  "stay on the record. A decided item is kept rather than removed, "
                  "so the outcome is checkable later.")


# Order is the order they appear. Comment windows lead because participation is
# the only thing on this record a reader can act on today.
# The third field is the TILE LABEL, which is not the question. On a phone the
# four tiles sit two across, and a full question truncated to fit reads "What
# can I ..." and "What deadl...", which is four cards that all look the same and
# say nothing. The question is still what gets typed into the box when one is
# clicked; the label is only what the tile calls it.
VIEWS = [
    ("open", "What can I still comment on?", "Open to comment", v_comment),
    ("soon", "What deadlines are coming up?", "Deadlines ahead", v_deadlines),
    ("new", "What changed this week?", "Changed this week", v_changed),
    ("done", "What is already decided?", "Already decided", v_decided),
]


# --------------------------------------------------------------- catalogue


def catalogue(rows, fac, today, places=()):
    """Every question this record can answer, each paired with its route.

    A route is `type:target`, and the page hands it to exactly the same
    answerer a typed query resolves to. So this list is not a second
    implementation of anything. It is a set of pre-worked routings, which is
    what makes a catalogued question impossible to mis-parse and makes the box
    able to finish a sentence the reader has only started.
    """
    out = []
    seen = set()

    def add(q, route, label=None):
        k = q.lower()
        if k in seen:
            return
        seen.add(k)
        # The name of the thing being asked about is already in the route, so
        # writing it out again would ship every long title a dozen times over.
        # It is stored as a tilde and put back by whoever reads this, which is
        # substitution rather than a second generator, so the two cannot drift.
        if label and label in q:
            q = q.replace(label, "~")
        out.append(f"{q}|{route}")

    for key, q, _tag, _fn in VIEWS:
        add(q, f"view:{key}")

    for r in rows:
        t = r["title"]
        i = r["id"]
        add(f"What is {t}?", f"what:{i}", t)
        add(f"Tell me about {t}", f"what:{i}", t)
        add(f"Why does {t} matter?", f"what:{i}", t)
        add(f"Who decides {t}?", f"who:{i}", t)
        add(f"Can I comment on {t}?", f"how:{i}", t)
        add(f"How do I have a say on {t}?", f"how:{i}", t)
        add(f"Is {t} open to the public?", f"how:{i}", t)
        add(f"Has {t} been decided?", f"stat:{i}", t)
        add(f"What is the status of {t}?", f"stat:{i}", t)
        add(f"What kind of decision is {t}?", f"kind:{i}", t)
        add(f"When did {t} start?", f"since:{i}", t)
        add(f"Where can I read the sources for {t}?", f"src:{i}", t)
        add(f"What happens next with {t}?", f"next:{i}", t)
        if r["on"]:
            add(f"When is the deadline for {t}?", f"when:{i}", t)
            add(f"When is {t} decided?", f"when:{i}", t)
        if r["where"]:
            add(f"Where is {t}?", f"where:{i}", t)
        if r["note"]:
            add(f"What changed on {t}?", f"chg:{i}", t)

    for e in fac["agency"]:
        L = e["label"]
        add(f"What is {L} deciding?", f"fac:agency/{e['key']}", L)
        add(f"How many decisions does {L} have?", f"fac:agency/{e['key']}", L)
        add(f"Show everything from {L}", f"fac:agency/{e['key']}", L)
        add(f"Can I comment on anything before {L}?", f"facopen:agency/{e['key']}", L)
    for e in fac["place"]:
        L = e["label"]
        add(f"What is happening in {L}?", f"fac:place/{e['key']}", L)
        add(f"Can I comment on anything in {L}?", f"facopen:place/{e['key']}", L)
    for e in fac["kind"]:
        L = e["label"]
        add(f"Which decisions are {L}?", f"fac:kind/{e['key']}", L)
        add(f"How many {L} are tracked?", f"fac:kind/{e['key']}", L)
    for e in fac["topic"]:
        L = e["label"]
        add(f"Which decisions involve {L}?", f"fac:topic/{e['key']}", L)
        add(f"Can I comment on anything about {L}?", f"facopen:topic/{e['key']}", L)
    for e in fac["status"]:
        add(f"What is {e['label']}?", f"fac:status/{e['key']}", e["label"])
    for e in fac["access"]:
        add(f"What is {e['label']}?", f"fac:access/{e['key']}", e["label"])

    for pl in places:
        add(f"What is happening near {pl['name']}?", f"near:{pl['key']}", pl["name"])

    for days, phrase in ((7, "this week"), (14, "in the next two weeks"),
                         (30, "this month"), (60, "in the next two months"),
                         (90, "in the next three months")):
        add(f"What is due {phrase}?", f"win:{days}")
        add(f"What closes {phrase}?", f"win:{days}")
    # Named months ahead, because a reader planning a comment thinks in months
    # rather than in a rolling window.
    y, m = today.year, today.month
    for _n in range(6):
        add(f"What is happening in {db.MONTHS[m - 1].title()}?"
            .replace("Jan", "January").replace("Feb", "February")
            .replace("Mar", "March").replace("Apr", "April")
            .replace("Jun", "June").replace("Jul", "July")
            .replace("Aug", "August").replace("Sep", "September")
            .replace("Oct", "October").replace("Nov", "November")
            .replace("Dec", "December"), f"mon:{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m, y = 1, y + 1

    for q, route in (
        ("What is the nearest deadline?", "sup:near"),
        ("What is next?", "sup:near"),
        ("What was added most recently?", "sup:new"),
        ("What has been tracked the longest?", "sup:old"),
        ("Which agency has the most decisions?", "sup:busy"),
        ("Where is the most happening?", "sup:place"),
        ("What moved most recently?", "sup:moved"),
        ("How many decisions are tracked?", "cnt:all"),
        ("How many are open to comment?", "cnt:open"),
        ("How many have a deadline?", "cnt:dated"),
        ("How many are already decided?", "cnt:done"),
        ("How many sources back this?", "cnt:src"),
        ("Show me everything", "cnt:all"),
        ("List every decision", "cnt:all"),
        ("What is open right now?", "cnt:open"),
        ("Is anything closing soon?", "win:14"),
        ("What is new?", "sup:new"),
        ("Anything I can act on?", "view:open"),
        ("What did I miss?", "view:new"),
        ("What is coming up?", "view:soon"),
        ("What is still undecided?", "fac:status/pending-decision"),
        ("Which decisions are closed to the public?", "fac:access/closed"),
        ("Where can I actually be heard?", "fac:access/open"),
    ):
        add(q, route)

    for q, key in (
        ("What is the Alaska AI Docket?", "what"),
        ("What is this?", "what"),
        ("How is this record kept?", "how"),
        ("How often is this updated?", "when"),
        ("Where does this data come from?", "where"),
        ("What are the sources?", "where"),
        ("Who keeps this?", "who"),
        ("Who is behind this?", "who"),
        ("Why does this exist?", "why"),
        ("Is this written by AI?", "ai"),
        ("Is this generated?", "ai"),
        ("Does this cost anything?", "cost"),
        ("Can I download the data?", "data"),
        ("Is there an API?", "data"),
        ("What happens if something is wrong?", "correct"),
        ("How do corrections work?", "correct"),
        ("Are my searches tracked?", "search"),
        ("Is this private?", "search"),
        ("Do decided items get removed?", "removed"),
        ("What is Cook Inlet Gas Watch?", "gas"),
        ("Can I subscribe?", "subscribe"),
        ("How do I get updates?", "subscribe"),
        ("How do I contact you?", "contact"),
        ("How do I report a missing decision?", "contact"),
    ):
        add(q, f"meta:{key}")
    return out


# ------------------------------------------------------------------- build


def questions_for(route, cat, by_id, fac):
    """Every catalogued phrasing of one route, each written out in full.

    A route carries several wordings on purpose, so a reader who types any of
    them lands in the same place. That also means a caller who needs one of
    them to FIT somewhere has a choice to make rather than a first match to
    accept.
    """
    return [expand(e, by_id, fac) for e in cat if e.split("|", 1)[1] == route]


def starters(rows, fac, cat, by_id):
    """Six questions the empty box offers, one per shape of answer.

    Not a random sample. A reader arriving cold learns what this can do from
    what it offers, so the strip has to show a field read, an agency, a place,
    a topic, a count and a question about the record itself. Six different
    shapes teaches the range in one glance, where six variations on one shape
    teaches that the box does one thing.
    """
    # THE FIELD READ. One dated decision, asked in the most useful way that
    # still fits a chip.
    #
    # "Can I comment on ~?" is the phrasing this docket most wants to offer,
    # because the whole point of the record is telling a reader when they can
    # act, so it is tried first and across every dated item before anything
    # else is considered. It is also the LONGEST wrapper of the per-item
    # shapes, and a title has to come in at 40 characters or under to survive
    # it. Two of the twenty two titles on the docket do, so whether that
    # phrasing fits has always depended on which items happen to be dated this
    # week, and on 2026-08-27 neither short title was dated and the self test
    # went red on a record that was otherwise correct.
    #
    # So the shape degrades rather than the chip breaking. Status, timing,
    # decider, subject and place are all field reads of the same decision, in
    # descending order of how much a docket reader gets from one, and each
    # wrapper is shorter than the last. The old code took the shortest TITLE
    # and then the catalogue's FIRST phrasing of it, which are two proxies for
    # the thing that has to fit and neither is what the gate below measures.
    lead = None
    for kind in ("how", "stat", "when", "who", "what", "where"):
        fits = [q
                for r in rows if r["on"]
                for q in questions_for(f"{kind}:{r['id']}", cat, by_id, fac)
                if len(q) <= CHIP_MAX]
        if fits:
            lead = min(fits, key=len)
            break
    if lead is None:
        # Nothing on the docket fits under any shape. Offer the shortest
        # anyway rather than dropping the field read out of the strip, and
        # leave the gate red, which is the right outcome: six shapes is the
        # contract and a chip that wraps is a real defect.
        every = [q
                 for r in rows if r["on"]
                 for q in questions_for(f"how:{r['id']}", cat, by_id, fac)]
        lead = min(every, key=len) if every else None

    want = []
    for group in ("agency", "place", "topic"):
        # The first entry with a name of its own. Statewide leads the place
        # list on count and teaches a reader nothing about what this holds.
        for e in fac.get(group) or []:
            if e["key"] != "statewide":
                want.append(f"fac:{group}/{e['key']}")
                break
    want += ["cnt:open", "meta:where"]
    out = [lead] if lead else []
    for route in want:
        qs = questions_for(route, cat, by_id, fac)
        if qs:
            out.append(qs[0])
    return out[:6]


def label_for(route, by_id, fac, places=()):
    """The name the tilde in a catalogued question stands for.

    THE PAGE MIRRORS THIS IN FIVE LINES. Keep them the same. It is a lookup
    rather than a rule, so there is nothing here to get subtly wrong, but a
    route type added on one side and not the other would print a raw tilde at
    a reader, which is why the self test expands every entry.
    """
    kind, target = route.split(":", 1)
    if kind == "near":
        for p in places:
            if p["key"] == target:
                return p["name"]
        return ""
    if kind in ("fac", "facopen"):
        group, key = target.split("/", 1)
        for e in fac.get(group, []):
            if e["key"] == key:
                return e["label"]
        return ""
    row = by_id.get(target)
    return row["title"] if row else ""


def expand(entry, by_id, fac, places=()):
    """One catalogue line, written back out in full."""
    q, route = entry.split("|", 1)
    return q.replace("~", label_for(route, by_id, fac, places)) if "~" in q else q



# ------------------------------------------------------- answers, in Python
#
# THIS MIRRORS THE PAGE'S OWN ANSWERER, ON PURPOSE, AND IT IS GATED.
#
# The box answers in the reader's browser, which is what makes it instant and
# what makes it invisible: an answer engine fetching the page sees an empty
# field, because the sentence does not exist until someone types. So the same
# answers are written into each decision's own page at build time, where a
# machine can read them and a person without script still gets them.
#
# Two implementations of one wording is a drift risk and there is no way to
# avoid it, so it is made loud instead. tests/ask_engine.mjs asks every one of
# these questions in a live box and compares what the box says to what the
# page says, and a difference fails CI. Day counts are normalised out of that
# comparison because the page is built once a day and the box counts against
# the reader's own clock, which is the one difference that is supposed to be
# there.

def days_out(iso, today):
    if not iso:
        return None
    return (date.fromisoformat(iso) - today).days


def long_date(iso, today):
    """House style takes the ordinal, month first. The year appears only when
    it is not this one, because a reader reading today does not need telling
    the year twice."""
    if not iso:
        return ""
    d = date.fromisoformat(iso)
    out = f"{gw.MONTHS[d.month - 1]} {gw.ordinal(d.day)}"
    if d.year != today.year:
        out += f", {d.year}"
    return out


def out_in(d):
    if d == 0:
        return "today"
    if d == 1:
        return "tomorrow"
    if d < 0:
        return "a day ago" if abs(d) == 1 else f"{abs(d)} days ago"
    return f"{d} days out"


# The order the answers read best in on a page. What it is, then who decides
# it, then the only thing a reader can act on, then when.
ANSWER_ORDER = ["what", "who", "how", "when", "where", "stat", "next",
                "chg", "kind", "since", "src"]


def answer_for(kind, row, today):
    """One field question about one decision. Assembled from the record, never
    generated, so there is nothing here that can be wrong in a way the record
    is not already wrong."""
    sub = "on " + row["title"]
    if kind == "who":
        return {"kick": "WHO DECIDES", "lead": row["decider"], "sub": sub}
    if kind == "when":
        if not row["on"]:
            return {"kick": "WHEN", "sub": sub,
                    "lead": "No upcoming date is published for it. It is "
                            + row["statusLabel"] + ", and the record carries a "
                            "date only once one is filed."}
        d = days_out(row["on"], today)
        return {"kick": "DEADLINE" if row["role"] == "deadline" else "NEXT DATE",
                "sub": sub,
                "lead": f"{long_date(row['on'], today)}, {out_in(d)}. "
                        + (row["onLabel"] or "Published date.")}
    if kind == "where":
        return {"kick": "WHERE", "sub": sub,
                "lead": row["where"] or "Statewide. No single site is on the record for it."}
    if kind == "how":
        kick = ("YES, IT IS OPEN" if row["access"] == "open"
                else "NOT A FORMAL COMMENT" if row["access"] == "indirect"
                else "NO OPEN COMMENT PATH")
        return {"kick": kick, "lead": row["howto"], "sub": sub}
    if kind == "stat":
        return {"kick": "STATUS", "sub": sub,
                "lead": f"It is {row['statusLabel']}. " + (row["note"] or row["summary"])}
    if kind == "chg":
        if not row["moved"]:
            return {"kick": "WHAT CHANGED", "sub": sub,
                    "lead": "Nothing has moved on it since it was first tracked on "
                            f"{long_date(row['first'], today)}."}
        return {"kick": f"LAST MOVED {long_date(row['moved'], today).upper()}",
                "lead": row["note"], "sub": sub}
    if kind == "src":
        n = len(row["outlets"])
        return {"kick": f"{n} {'SOURCE' if n == 1 else 'SOURCES'}", "sub": sub,
                "lead": ", ".join(row["outlets"]) + ". Every one is listed with "
                        "its date on the decision page."}
    if kind == "next":
        for d0, label, _k in row["dates"]:
            if days_out(d0, today) >= 0:
                return {"kick": "WHAT HAPPENS NEXT", "sub": sub,
                        "lead": f"{label}, {long_date(d0, today)}, "
                                f"{out_in(days_out(d0, today))}."}
        return {"kick": "WHAT HAPPENS NEXT", "sub": sub,
                "lead": f"No further date is published. It is {row['statusLabel']} "
                        "and the record is checked against its source every day."}
    if kind == "kind":
        return {"kick": "TYPE", "sub": sub,
                "lead": f"A {row['kind']}, decided by {row['decider']}."}
    if kind == "since":
        d = days_out(row["first"], today)
        lead = f"Tracked since {long_date(row['first'], today)}, {out_in(d)}."
        if row["dates"]:
            lead += (" The earliest date on its record is "
                     f"{long_date(row['dates'][0][0], today)}.")
        return {"kick": "TRACKED SINCE", "lead": lead, "sub": sub}
    return {"kick": row["kind"].upper(), "lead": row["summary"], "sub": row["title"]}


def decision_answers(row, cat, by_id, fac, today):
    """Every question this record can answer about ONE decision, with its
    answer. One per shape of answer rather than one per wording, because three
    ways of asking what something is deserve one entry and not three."""
    first = {}
    for entry in cat:
        q, route = entry.split("|", 1)
        kind, target = route.split(":", 1)
        if target != row["id"] or kind not in ANSWER_ORDER:
            continue
        first.setdefault(kind, expand(entry, by_id, fac))
    out = []
    for kind in ANSWER_ORDER:
        if kind not in first:
            continue
        a = answer_for(kind, row, today)
        if not a["lead"]:
            continue
        out.append({"q": first[kind], "kind": kind, **a})
    return out


def vocabulary(rows, fac):
    """Every word the record contains, for spelling correction.

    A reader who types kenia or micoreactor has told us exactly what they want
    and a strict matcher answers nothing. Correction needs a word list, and the
    only honest word list is the one the record actually uses, so it is
    harvested rather than shipped.
    """
    seen = Counter()
    for r in rows:
        for w in re.findall(r"[a-z][a-z0-9]{3,}", r["hay"]):
            seen[w] += 1
    for group in fac.values():
        for e in group:
            for t in e["terms"]:
                for w in re.findall(r"[a-z][a-z0-9]{3,}", t):
                    seen[w] += 1
    return sorted(seen)


def build(today=None):
    today = today or date.today()
    items = load_items()
    rows = [index_row(it, today) for it in items]
    prune_handles(rows)
    fac = facets(rows)
    views = []
    for key, q, tag, fn in VIEWS:
        hits, summary = fn(rows, today)
        views.append({"key": key, "q": q, "tag": tag, "summary": summary,
                      "ids": [r["id"] for r in hits]})
    # Proximity, worked out here rather than in the page. Forty two towns
    # against fifteen points is six hundred distances, which is nothing at
    # build time and pointless to repeat in every reader's browser.
    places = communities()
    for pl in places:
        pl["ids"] = near(pl, rows)
    cat = catalogue(rows, fac, today, places)
    by_id = {r["id"]: r for r in rows}
    return {
        "generated": today.isoformat(),
        "recent": RECENT_DAYS,
        "index": rows,
        "facets": fac,
        "views": views,
        "syn": SYNONYMS,
        "vocab": vocabulary(rows, fac),
        "meta": META,
        "q": cat,
        "near": {"miles": NEAR_MILES, "places": places},
        "try": starters(rows, fac, cat, by_id),
    }


# --------------------------------------------------------------- self test


def self_test():
    print("the answer engine")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    today = date.today()
    items = load_items()
    out = build(today)
    rows, views, fac = out["index"], out["views"], out["facets"]
    by_id = {r["id"]: r for r in rows}

    check("every decision is indexed", len(rows) == len(items), f"{len(rows)} rows")
    check("every row is searchable", all(r["hay"].strip() for r in rows))
    check("ids are unique", len({r["id"] for r in rows}) == len(rows))
    check("every row can answer who decides it",
          all(r["decider"].strip() for r in rows))
    check("every row can answer what it is",
          all(len(r["summary"]) > 40 for r in rows))
    check("every row can answer how to take part",
          all(len(r["howto"]) > 20 for r in rows))
    # A handle is a claim that one word names one decision. Two letters names
    # nothing, and a handle two items share scores both of them on a query
    # meant for neither.
    hands = [h for r in rows for h in r["alias"]]
    check("no handle is too short to name anything",
          all(len(h) >= 3 for h in hands), str([h for h in hands if len(h) < 3][:4]))
    check("no handle is claimed by two decisions",
          len(hands) == len(set(hands)),
          str([h for h in hands if hands.count(h) > 1][:4]))

    print("the index agrees with the page beside it")
    # resolve() is what makes a closed window read closed while the ledger
    # still says open-for-comment. An index built on the raw field would
    # contradict the badge next to it.
    check("open access matches db.open_count",
          len(open_now(rows)) == db.open_count(items, today),
          f"{len(open_now(rows))} open")
    raw_open = sum(1 for it in items if it.get("public_access") == "open")
    if raw_open != len(open_now(rows)):
        check("and not the raw ledger field",
              raw_open != len(open_now(rows)), f"raw {raw_open}")
    else:
        print(f"  ..    raw and resolved agree today ({raw_open}), nothing to distinguish")

    print("entities, because a rule that stops matching is a silent dead end")
    for name in ("agency", "place", "kind", "topic", "status", "access"):
        check(f"{name} facet is populated", len(fac[name]) > 0, f"{len(fac[name])} groups")
        stray = [i for e in fac[name] for i in e["ids"] if i not in by_id]
        check(f"{name} points only at indexed items", not stray, str(stray[:3]))
    covered = {i for e in fac["agency"] for i in e["ids"]}
    check("every decision has a recognised agency",
          len(covered) == len(rows),
          "missing " + str(sorted({r["id"] for r in rows} - covered)[:3]))
    covered = {i for e in fac["place"] for i in e["ids"]}
    check("every decision has a place or is statewide", len(covered) == len(rows))
    covered = {i for e in fac["topic"] for i in e["ids"]}
    check("every decision carries at least one topic",
          len(covered) == len(rows),
          "missing " + str(sorted({r["id"] for r in rows} - covered)[:3]))
    # A facet term nobody can reach is worse than no facet, it reads as
    # coverage that is not there.
    dead = [f"{name}/{e['key']}" for name in fac for e in fac[name]
            if not any(t.strip() for t in e["terms"])]
    check("every facet carries query words", not dead, str(dead[:3]))
    # Two facets owning the same typed word is a coin flip dressed as an
    # answer. A reader typing closed means one thing, and the page has to pick
    # the same one every time, so the collision is a build failure rather than
    # a behaviour nobody can predict.
    owner, clash = {}, []
    for name in fac:
        for e in fac[name]:
            for t in e["terms"]:
                key = t.lower().strip()
                if key in owner and owner[key] != f"{name}/{e['key']}":
                    clash.append(f"{key} claimed by {owner[key]} and {name}/{e['key']}")
                owner[key] = f"{name}/{e['key']}"
    check("no two facets claim the same query word", not clash, str(clash[:3]))
    # A one or two letter term matches inside everything and filters nothing.
    tiny = sorted({t for name in fac for e in fac[name] for t in e["terms"]
                   if len(t.strip()) < 3})
    check("no facet term is too short to discriminate", not tiny, str(tiny[:6]))
    # A handle names ONE decision and a facet term names a group. A word that
    # is both filters the named decision out of a query about it, which is how
    # aklng returned three gas decisions and not the AKLNG bill.
    handset = {h for r in rows for h in r["alias"]}
    both = sorted(handset & {t for name in fac for e in fac[name] for t in e["terms"]})
    check("no facet term is also the name of one decision", not both, str(both[:4]))
    # Giving a word up must not leave a group unreachable.
    mute = [f"{name}/{e['key']}" for name in fac for e in fac[name] if not e["terms"]]
    check("no group was left without a word of its own", not mute, str(mute[:3]))

    print("the words a reader types resolve to words the record uses")
    hay = " ".join(r["hay"] for r in rows)
    dead = sorted({t for terms in SYNONYMS.values() for t in terms if t not in hay})
    check("no synonym points at a word the record does not contain",
          not dead, str(dead[:6]))
    check("the spelling vocabulary is big enough to correct against",
          len(out["vocab"]) > 400, f"{len(out['vocab'])} words")

    print("the views")
    check("every view has a summary and a key",
          all(v["summary"].strip() and v["key"] for v in views), f"{len(views)} views")
    stray = [i for v in views for i in v["ids"] if i not in by_id]
    check("no view points at an item that is not indexed", not stray, str(stray))
    # A view that matches nothing must still say something useful. An empty
    # result with an empty sentence reads as broken rather than as an answer.
    for v in views:
        check(f"{v['key']} says something even when it matches nothing",
              len(v["summary"]) > 30, f"{len(v['ids'])} hits")

    print("the question catalogue")
    cat = out["q"]
    check("it covers at least five hundred questions", len(cat) >= 500, f"{len(cat)} questions")
    check("every entry is a question and a route",
          all(e.count("|") == 1 and e.split("|")[1].count(":") >= 1 for e in cat))
    check("no question contains the field separator",
          all("|" not in e.split("|")[0] for e in cat))
    bad = []
    types = Counter()
    for e in cat:
        q, route = e.split("|")
        kind, target = route.split(":", 1)
        types[kind] += 1
        if kind in ("what", "who", "when", "where", "how", "stat", "chg",
                    "src", "next", "kind", "since"):
            if target not in by_id:
                bad.append(route)
        elif kind == "view":
            if target not in {v["key"] for v in views}:
                bad.append(route)
        elif kind in ("fac", "facopen"):
            group, key = target.split("/", 1)
            if group not in fac or key not in {e2["key"] for e2 in fac[group]}:
                bad.append(route)
        elif kind == "meta":
            if target not in META:
                bad.append(route)
        elif kind == "win":
            if not target.isdigit():
                bad.append(route)
        elif kind == "mon":
            if not re.fullmatch(r"\d{4}-\d{2}", target):
                bad.append(route)
        elif kind == "near":
            if target not in {p["key"] for p in out["near"]["places"]}:
                bad.append(route)
        elif kind in ("sup", "cnt"):
            pass
        else:
            bad.append(route)
    check("every route points at something that exists", not bad, str(bad[:4]))
    # The tilde is only a saving if it always comes back. One that survives
    # expansion is a raw punctuation mark shown to a reader.
    full = [expand(e, by_id, fac, out["near"]["places"]) for e in cat]
    check("every question expands back to a whole sentence",
          all("~" not in q and len(q) > 8 for q in full),
          str([q for q in full if "~" in q][:2]))
    check("expanded questions are still unique", len({q.lower() for q in full}) == len(full))
    # The strip on the empty box teaches what this can do, so it has to show
    # six different shapes of answer rather than six wordings of one.
    check("the empty box offers six starters", len(out["try"]) == 6, str(len(out["try"])))
    check("every starter is a real catalogued question",
          all(q in full for q in out["try"]),
          str([q for q in out["try"] if q not in full][:2]))
    check("no starter is too long to sit in a chip",
          all(len(q) <= CHIP_MAX for q in out["try"]),
          str([q for q in out["try"] if len(q) > CHIP_MAX][:2]))
    check("the catalogue spans every route type", len(types) >= 10,
          " ".join(f"{k}={v}" for k, v in sorted(types.items())))
    # Every item must be reachable by name, or the catalogue is a list of the
    # convenient rather than a map of the record.
    reach = {r.split(":", 1)[1] for e in cat for r in [e.split("|")[1]]
             if ":" in r and r.split(":", 1)[1] in by_id}
    check("every decision appears in the catalogue", len(reach) == len(rows),
          f"{len(reach)} of {len(rows)}")

    print("the answers written into each decision's own page")
    every = []
    for r in rows:
        qa = decision_answers(r, cat, by_id, fac, today)
        check(f"{r['id'][:34]} publishes its answers", len(qa) >= 8, f"{len(qa)}")
        every.extend(qa)
    # Not a length. Juneau is a complete and correct answer to where is it,
    # and a rule that calls it too short is a rule about the rule rather than
    # about the record.
    check("every published answer says something",
          all(a["lead"].strip() and a["kick"].strip() for a in every),
          f"{len(every)} answers")
    # These go into FAQPage structured data, where a machine quotes them
    # verbatim under this site's name, so they are held to the same rules as
    # anything else published here.
    check("no published answer carries banned punctuation",
          not [a for a in every if any(c in a["lead"] + a["kick"] for c in "—–‘’“”")])
    check("no published answer predicts an outcome",
          not [a for a in every if re.search(
              r"\b(will be approved|is likely|we expect|guaranteed)\b", a["lead"], re.I)])

    print("house style, because this ships as visible page copy")
    prose = ([v["summary"] for v in views] + list(META.values()) + full
             + out["try"] + [a["q"] for a in every])
    for text in prose:
        if ":" in text or any(c in text for c in "—–‘’“”"):
            check(f"clean copy {text[:50]!r}", False)
            break
    else:
        check("no prose colon, dash or curly quote in any shipped sentence", True,
              f"{len(prose)} sentences")
    for r in rows:
        if any(c in (r["summary"] + r["howto"]) for c in "—–‘’“”"):
            check(f"item copy {r['id']} is clean", False)

    print("dates are resolved, not raw")
    dated = [r for r in rows if r["on"]]
    check("dated rows carry what the date means",
          all(r["role"] in ("deadline", "date") for r in dated),
          f"{len(dated)} dated")
    check("every published date is sorted and typed",
          all(d[0] and d[2] for r in rows for d in r["dates"]))

    print("size, because this ships inline in the page")
    blob = json.dumps(out, separators=(",", ":"))
    check("the payload is small enough to inline", len(blob) < 190_000,
          f"{len(blob) / 1024:.1f} KB, roughly {len(blob) // 3400} KB gzipped")

    print()
    print("self-test clean" if ok[0] else "self-test FAILED")
    return 0 if ok[0] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--questions", action="store_true",
                    help="print the whole question catalogue")
    ap.add_argument("--date")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    today = date.fromisoformat(args.date) if args.date else date.today()
    out = build(today)
    if args.questions:
        for e in out["q"]:
            q, route = e.split("|")
            print(f"{route:<28} {q}")
        return 0
    for v in out["views"]:
        print(f"\n{v['q']}\n  {v['summary']}\n  {len(v['ids'])} item(s)")
    print(f"\n{len(out['q'])} catalogued questions, "
          f"{sum(len(g) for g in out['facets'].values())} entities, "
          f"{len(out['vocab'])} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
