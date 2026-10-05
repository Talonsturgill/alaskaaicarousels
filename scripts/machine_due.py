#!/usr/bin/env python3
"""machine_due.py, is the weekly machine pass due today? Exit 0 = yes, run it. Exit 1 = no.

WHY THIS EXISTS (owner, 2026-10-02)

Until this day every run ended in Phase 12, which spawned the upgrade engineer and made zero to
three changes to the machine from what THAT ONE RUN saw. The owner's words: the daily automation
should "only fix like the things that were broken during the run", and once a week a run should
spend time "addressing the things that really need to be fixed based on the recurring themes that
it saw during the week. So that it can be constantly making upgrades each week based on actual
output." One run is one sample. A defect the judges name on four decks in a week is a defect in
the machine, and one they name once may be that deck's.

So a run now fixes what broke in it and QUEUES the rest in `knowledge/MACHINE_QUEUE.md`, and the
weekly pass reads the whole week (`scripts/week_digest.py`) and works the themes that recurred.

THE PASS IS DUE WHEN
  no pass has ever run, or
  the last one was DAYS or more days ago, or
  an open queue item has bitten two or more runs beyond the one that found it, and the last pass
  was not today, because a repeat offender waiting a week is a week of decks paying for it.

  AN ESCALATED ITEM DOES NOT MAKE IT DUE EARLY (2026-10-06, the second weekly pass). An item the
  pass can't fix carries ` | escalated <date>: <why>` (prompts/machine_weekly.md) and goes to the
  owner in the email. The Gas Watch evening-slot item is one, an owner decision on schedules and
  credentials, and at `repeat: 5` it made the pass due EVERY day, which is the daily upgrading the
  owner moved away from on 2026-10-02: the pass of 2026-10-06 ran two days after the last for it
  alone. An escalated item still counts as open, still shows in the digest, and the seven-day pass
  still reads it.

It is due on schedule even with an empty queue, because the themes come from the week's own score
reports and flow reviews and not only from what a run remembered to queue.

  python3 scripts/machine_due.py --date 2026-10-09
  python3 scripts/machine_due.py --self-test
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STATE = REPO_ROOT / "config" / "machine_pass.json"
QUEUE = REPO_ROOT / "knowledge" / "MACHINE_QUEUE.md"
DAYS = 7
ITEM = re.compile(r"^- \[ \] (.*)$")
REPEAT = re.compile(r"repeat:\s*(\d+)", re.I)
ESCALATED = re.compile(r"\|\s*escalated\s+\d{4}-\d{2}-\d{2}", re.I)


def open_items(text: str) -> list[dict]:
    """Open items, column 0 only, so the indented format example never counts."""
    items = []
    for line in text.splitlines():
        m = ITEM.match(line)
        if m:
            r = REPEAT.search(m.group(1))
            items.append({"text": m.group(1), "repeat": int(r.group(1)) if r else 0,
                          "escalated": bool(ESCALATED.search(m.group(1)))})
    return items


def verdict(state: dict, queue_text: str, today: dt.date) -> tuple[bool, str]:
    items = open_items(queue_text)
    last = state.get("last_pass")
    if not last:
        return True, f"no weekly pass has run yet ({len(items)} item(s) queued)"
    try:
        last_d = dt.date.fromisoformat(str(last))
    except ValueError:
        return True, f"the last pass date {last!r} does not parse, so treat the pass as never run"
    age = (today - last_d).days
    if age >= DAYS:
        return True, f"last pass {last}, {age} days ago, {len(items)} item(s) queued"
    repeats = [i for i in items if i["repeat"] >= 2 and not i["escalated"]]
    if repeats and age >= 1:
        return True, f"{len(repeats)} repeat offender(s) queued, last pass {last}"
    return False, (f"last pass {last}, {age} day(s) ago, due at {DAYS}; {len(items)} item(s) "
                   f"queued, {len(repeats)} repeat offender(s)")


def self_test() -> int:
    bad = 0

    def ok(label, cond, extra=""):
        nonlocal bad
        print(f"  {'ok  ' if cond else 'FAIL'}  {label}{'' if cond else '  ' + extra}")
        bad += 0 if cond else 1

    d = dt.date(2026, 10, 10)
    q0 = ("    - [ ] <date found> | repeat: <n> | the format example\n"
          "## Open\n(none)\n## Done\n- [x] 2026-10-01 | repeat: 3 | old\n")
    q1 = "## Open\n- [ ] 2026-10-03 | repeat: 0 | a | evidence: x | fix: y\n"
    q2 = "## Open\n- [ ] 2026-10-03 | repeat: 2 | a | evidence: x | fix: y\n"
    ok("the format example and done items are not open items", open_items(q0) == [])
    ok("no pass ever run is due, even with nothing queued", verdict({}, q0, d)[0])
    ok("a pass seven days ago is due with nothing queued", verdict({"last_pass": "2026-10-03"}, q0, d)[0])
    ok("a pass three days ago with one ordinary item is not due",
       not verdict({"last_pass": "2026-10-07"}, q1, d)[0])
    ok("a repeat offender makes it due early", verdict({"last_pass": "2026-10-07"}, q2, d)[0])
    ok("...but never twice on one day", not verdict({"last_pass": "2026-10-10"}, q2, d)[0])
    ok("a date that does not parse is treated as never run", verdict({"last_pass": "soon"}, q1, d)[0])
    q3 = ("## Open\n- [ ] 2026-09-30 | repeat: 5 | gaswatch: owner only | evidence: x | fix: owner"
          " | escalated 2026-10-06: schedules and credentials are the owner's\n")
    ok("an escalated repeat offender does not make it due early",
       not verdict({"last_pass": "2026-10-06"}, q3, dt.date(2026, 10, 7))[0])
    ok("...it is still an open item", len(open_items(q3)) == 1 and open_items(q3)[0]["escalated"])
    ok("...and the seven-day pass still runs", verdict({"last_pass": "2026-10-06"}, q3, dt.date(2026, 10, 13))[0])
    ok("...while an unescalated repeat offender beside it still does",
       verdict({"last_pass": "2026-10-06"}, q3 + q2.split("\n", 1)[1], dt.date(2026, 10, 7))[0])
    ok("the word 'escalated' in evidence is not an escalation",
       not open_items("- [ ] 2026-10-03 | repeat: 2 | a | evidence: it escalated fast | fix: y\n")[0]["escalated"])
    ok("the live queue and state parse", isinstance(open_items(QUEUE.read_text(encoding="utf-8")
                                                               if QUEUE.exists() else ""), list))
    print("\nmachine_due self-test: " + ("all passed" if not bad else f"{bad} FAILED"))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    due, why = verdict(state, QUEUE.read_text(encoding="utf-8") if QUEUE.exists() else "",
                       dt.date.fromisoformat(a.date))
    print(f"weekly machine pass {'DUE' if due else 'not due'}: {why}")
    return 0 if due else 1


if __name__ == "__main__":
    sys.exit(main())
