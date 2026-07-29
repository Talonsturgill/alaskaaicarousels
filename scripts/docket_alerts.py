#!/usr/bin/env python3
"""docket_alerts.py sends subscriber email alerts for live docket events.

Zero-touch by design. The daily routine runs this in Phase 11 after the
docket ledger is current. It reads ledger/docket.json, works out which
alerts are due, bundles everything due into at most ONE email, sends it
through the Buttondown API, and appends the send to ledger/alerts.json
(the no-repeat ledger, committed with the run so an alert can never fire
twice). The key is read from BUTTONDOWN_API_KEY, then Buttondown, then
BUTTONDOWN; if none is set it prints SKIP and exits 0, so the routine
never breaks on a missing key.

Alert triggers, deliberately narrow so subscribers only hear from us when
something real happens
  window-open   an item is open-for-comment with open public access and
                subscribers have never been told
  near          a deadline or vote lands within the next 2 days

House style is enforced on the composed email, no em or en dashes, no
curly quotes, no emoji, and no prose colons (clock times and URLs pass).

  python scripts/docket_alerts.py --date 2026-07-10 [--dry-run]

Exit 0 always unless the ledger is unreadable or the send fails hard.
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.request
from datetime import date as ddate
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import docket_build as db

REPO = Path(__file__).resolve().parents[1]
API = "https://api.buttondown.com/v1/emails"
SITE = f"{db.DEFAULT_SITE}/docket/"
MONTH_FULL = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
MAX_PER_RUN = 1  # at most one subscriber email per day, ever

# Words that end in a period without ending a sentence. Alaska legislative
# copy is full of them, and "HB 259, introduced by Rep." went out looking like
# a complete thought.
ABBREVIATIONS = {"Rep", "Sen", "Gov", "Sec", "Dept", "Mr", "Ms", "Mrs", "Dr",
                 "St", "No", "Inc", "Co", "Corp", "Jr", "Sr", "Ave", "Blvd",
                 "Ft", "Mt", "vs", "etc", "approx", "Assn", "Comm"}


def pretty(iso):
    d = ddate.fromisoformat(iso)
    return f"{MONTH_FULL[d.month - 1]} {d.day}"


def lint(text):
    if db.BANNED.findall(text):
        db.fail(f"banned punctuation in alert email {db.BANNED.findall(text)[:4]}")
    t = re.sub(r"https?://\S+", " ", text)
    t = re.sub(r"\d{1,2}:\d{2}", " ", t)
    if ":" in t:
        db.fail(f"prose colon in alert email near {t[t.index(':') - 30:t.index(':') + 10]!r}")


def load_sent():
    p = REPO / "ledger/alerts.json"
    if not p.exists():
        return {"_spec": {"purpose": "No-repeat ledger for subscriber alerts. "
                          "Each send appends one entry; docket_alerts.py refuses "
                          "to send a key that already appears here."},
                "sent": []}
    return json.loads(p.read_text())


def migrate_window_keys(sent, items, today):
    """Pin legacy dateless window-open keys to the deadline they were sent for.

    The key gained a date so a reopened comment period can alert again. That
    change alone would make every already-sent window-open key stop matching,
    and the next run would mail every open item to subscribers a second time.

    A legacy key means "we already told them about the window that was open
    then", and the window open then is the one open now unless it has moved.
    So pin it to the item's current deadline, once, in the ledger. After that
    the key is dated like any other and a genuinely new window gets a new key.
    Idempotent; returns True when it changed something."""
    by_id = {it["id"]: it for it in items}
    changed = False
    for e in sent["sent"]:
        key = e["key"]
        if not key.endswith("/window-open"):
            continue
        iid = key[: -len("/window-open")]
        it = by_id.get(iid)
        dl = db.resolve(it, today)["deadline"] if it else None
        # No item or no deadline: pin to what it was, so it still cannot resend.
        e["key"] = f"{iid}/window-open/{dl['date'] if dl else 'undated'}"
        e["migrated_from"] = key
        changed = True
    return changed


def due_alerts(items, sent_keys, today):
    due = []
    for it in items:
        if it["status"] not in ("open-for-comment", "pending-decision", "watching"):
            continue
        r = db.resolve(it, today)
        # A window-open alert says one thing, that a comment window is open and
        # here is when it shuts. So it carries the item's OWN action deadline
        # and nothing else (rule 2). It used to carry the soonest upcoming date
        # of any kind, which for the AIDEA item after 2026-07-21 would have been
        # another city's council vote, mailed to subscribers as the close of a
        # state comment window. r["cta"] also means an expired window can never
        # newly alert as open.
        if r["cta"]:
            # The key carries the deadline it is about. Without it, one
            # window-open send silences an item forever, so a REOPENED comment
            # period or a second hearing on the same docket item is never told
            # to subscribers. Reopened DNR windows are routine. The near key
            # below already carried its date; this one did not.
            dl = r["deadline"]["date"] if r["deadline"] else "undated"
            k = f"{it['id']}/window-open/{dl}"
            if k not in sent_keys:
                due.append((k, "window-open", it, r["deadline"]))
        for d in it["key_dates"]:
            dd = ddate.fromisoformat(d["date"])
            if d["kind"] in ("deadline", "vote") and 0 <= (dd - today).days <= 2:
                k = f"{it['id']}/near/{d['date']}"
                if k not in sent_keys:
                    due.append((k, "near", it, d))
    return due


def teaser(summary):
    """The first sentence of a summary, without cutting it at an abbreviation.

    summary.split(". ")[0] rendered hb-259 as "HB 259, introduced by Rep." in
    a subscriber email. Require the next character to start a new sentence, and
    fall back to the whole summary rather than emit a fragment. The schema says
    a summary is one or two sentences, so the whole thing is always a safe
    answer; a truncated one never is."""
    s = " ".join((summary or "").split())
    for m in re.finditer(r"\.\s+(?=[A-Z0-9])", s):
        word = re.search(r"([A-Za-z.]+)$", s[:m.start()])
        head = word.group(1) if word else ""
        # A single capital (initials) or a known title is not a sentence end.
        if head in ABBREVIATIONS or (len(head) == 1 and head.isupper()):
            continue
        first = s[:m.start() + 1]
        if len(first) >= 40 and first.count(" ") >= 6:
            return first
        break                          # suspiciously short, do not truncate
    return s


def intro(due):
    """One opening sentence, describing what is ACTUALLY due.

    This used to be hardcoded to "a public window closing soon" in render_html,
    which is the body that sends. A `near` alert about another body's vote then
    opened by telling the reader their comment window was closing, while the
    card underneath correctly named the vote and the access note underneath
    that said the window ran another week. The subject line was honest; the
    body was not. Same defect family as the AUG 13 button.

    Living in compose() means the colon and punctuation lint covers it too,
    which it never did while it was a literal inside the HTML builder."""
    kinds = {kind for _, kind, _, _ in due}
    if kinds == {"window-open"}:
        return ("A public comment window just opened on an Alaska "
                "AI-infrastructure decision.")
    if kinds == {"near"}:
        return ("A quick heads-up on Alaska AI-infrastructure decisions "
                "with a date in the next few days.")
    return ("A quick heads-up on Alaska AI-infrastructure decisions, an open "
            "comment window and a date landing soon.")


def compose(due, today):
    """One email covering everything due. Returns (subject, markdown body)."""
    due = dedupe_by_item(due)
    if len(due) == 1:
        k, kind, it, d = due[0]
        when = pretty(d["date"]) if d else "now"
        if kind == "window-open":
            subject = f"A public comment window is open, {it['title']}"
        else:
            days = (ddate.fromisoformat(d["date"]) - today).days
            inwords = "today" if days == 0 else ("tomorrow" if days == 1 else f"in {days} days")
            subject = f"{it['title']}, {d['kind']} {inwords}"
    else:
        subject = f"{len(due)} Alaska AI decisions land in the next few days"

    lines = [intro(due)]
    for k, kind, it, d in due:
        lines.append(f"**{it['title']}**")
        lines.append(teaser(it["summary"]))
        if d:
            lines.append(f"{d['label']}, {pretty(d['date'])}.")
        lines.append(it["access_note"])
        src = it["sources"][0]["url"]
        lines.append(f"Act or read the record here\n{src}")
        lines.append("")
    lines.append(f"Every decision we track, with live countdowns\n{SITE}")
    body = "\n\n".join(l for l in lines if l is not None)
    return subject, body


def dedupe_by_item(due):
    """One card per docket item for display, keeping the first (window-open beats
    near for framing). The caller still records every key in alerts.json so the
    no-repeat ledger is unchanged; this only collapses the visible duplicates."""
    seen, out = set(), []
    for e in due:
        iid = e[2]["id"]
        if iid not in seen:
            seen.add(iid)
            out.append(e)
    return out


def esc(s):
    return html.escape(str(s), quote=True)


def render_html(due, today):
    """Inline-styled HTML email body. Renders on any plan (no custom-CSS add-on
    needed) and sits inside the newsletter's branded header/footer. The plain
    prose from compose() is what the colon lint gates; this is the sent body."""
    due = dedupe_by_item(due)
    P = ["<div style='font-family:Arial,Helvetica,sans-serif;'>",
         f"<p style='font-size:15px;color:#33424f;line-height:1.6;margin:0 0 20px;'>"
         f"{esc(intro(due))}</p>"]
    for k, kind, it, d in due:
        title = esc(it["title"])
        summary = esc(teaser(it["summary"]))
        access = esc(it["access_note"])
        src = esc(it["sources"][0]["url"])
        when = ""
        if d:
            when = ("<div style='font-family:Menlo,Consolas,monospace;font-size:13px;"
                    "color:#7a5c00;background:#fbf3d6;display:inline-block;padding:5px 11px;"
                    f"border-radius:3px;margin:10px 0 4px;'>{esc(d['label'])}, "
                    f"{esc(pretty(d['date']))}</div>")
        P.append(
            "<table width='100%' cellpadding='0' cellspacing='0' role='presentation' "
            "style='margin:0 0 18px;'><tr><td style='border-left:4px solid #FFC72C;"
            "background:#f7f9fb;padding:16px 20px;border-radius:0 6px 6px 0;'>"
            f"<div style='font-family:Georgia,serif;font-size:19px;font-weight:bold;"
            f"color:#0b1a2e;line-height:1.3;'>{title}</div>"
            f"<div style='font-size:15px;color:#33424f;line-height:1.55;padding-top:6px;'>"
            f"{summary}</div>{when}"
            f"<div style='font-size:13px;color:#6a7783;line-height:1.5;padding-top:2px;'>"
            f"{access}</div>"
            f"<div style='padding-top:13px;'><a href='{src}' style='font-size:14px;"
            f"font-weight:bold;color:#0b1a2e !important;background-color:#FFC72C;"
            f"text-decoration:none !important;padding:10px 18px;border-radius:4px;"
            f"display:inline-block;'>"
            "<span style='color:#0b1a2e !important;text-decoration:none;'>"
            "Act or read the record &rarr;</span></a></div></td></tr></table>")
    P.append(
        "<table width='100%' cellpadding='0' cellspacing='0' role='presentation' "
        "style='margin-top:4px;'><tr><td style='padding:14px 0 0;border-top:1px solid "
        f"#e3e9ee;'><a href='{esc(SITE)}' style='font-family:Menlo,Consolas,monospace;"
        "font-size:14px;color:#0b64b8 !important;text-decoration:none;'>Every decision we track, "
        "with live countdowns &rarr;</a></td></tr></table>")
    P.append("</div>")
    return "\n".join(P)


def send(subject, body, dry):
    key = (os.environ.get("BUTTONDOWN_API_KEY")
           or os.environ.get("Buttondown")
           or os.environ.get("BUTTONDOWN")
           or "").strip()
    if dry or not key:
        print(("DRY RUN" if dry else "SKIP, no Buttondown API key (set BUTTONDOWN_API_KEY or Buttondown)") +
              f"\nsubject {subject}\n---\n{body}")
        return bool(dry)
    req = urllib.request.Request(
        API, method="POST",
        data=json.dumps({"subject": subject, "body": body,
                         "status": "about_to_send"}).encode(),
        headers={"Authorization": f"Token {key}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status not in (200, 201):
            db.fail(f"buttondown returned {r.status}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    today = ddate.fromisoformat(args.date)

    ledger = json.loads((REPO / "ledger/docket.json").read_text())
    # Every other docket consumer validates before it reads. This one did not,
    # so an item Phase 3.5 added with an empty sources list raised a bare
    # IndexError from compose() mid-run instead of the intended
    # "FAIL: <id>: needs at least one source".
    db.validate(ledger["items"])
    sent = load_sent()
    if migrate_window_keys(sent, ledger["items"], today):
        (REPO / "ledger/alerts.json").write_text(json.dumps(sent, indent=2) + "\n")
        print("alerts ledger migrated to dated window-open keys")
    sent_keys = {e["key"] for e in sent["sent"]}
    due = due_alerts(ledger["items"], sent_keys, today)
    if not due:
        print("no alerts due")
        return

    subject, body = compose(due, today)
    lint(subject + "\n" + body)          # colon/house-style gate runs on the prose words
    html_body = render_html(due, today)  # branded HTML is what actually sends
    delivered = send(subject, html_body, args.dry_run)
    if delivered and not args.dry_run:
        for k, kind, it, d in due:
            sent["sent"].append({"key": k, "kind": kind, "sent_on": args.date,
                                 "subject": subject})
        (REPO / "ledger/alerts.json").write_text(json.dumps(sent, indent=2) + "\n")
        print(f"sent 1 email covering {len(due)} alert(s), ledger updated")


if __name__ == "__main__":
    main()
