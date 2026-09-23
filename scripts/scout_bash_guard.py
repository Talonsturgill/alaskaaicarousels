#!/usr/bin/env python3
"""scout_bash_guard.py -- the only Bash a research scout is allowed to run.

WHY THIS EXISTS (2026-09-23, run No.66).

Run No.62 built scripts/fetch_pdf_text.py so a scout could read a primary
source that happens to be a PDF, and every scout brief since has NAMED it.
Nobody checked that a scout could actually run it. It could not: the scout
agent's tool list is WebSearch, WebFetch and Read, and none of those execute a
script. On No.66 four of six scouts said so in `dead_ends` and several primary
documents went unread, among them the DNR preliminary decision for ADL 234762,
AIDEA's development plan and fact sheet, the AI3 NOFO, and the draft
2027-2030 STIP. The showrunner ran the same command by hand and it worked first
time on both Mat-Su documents, which is the only reason that deck had its
primary sources at all. NAMING A SCRIPT IN A BRIEF IS NOT THE SAME AS HANDING
OVER THE TOOL THAT RUNS IT.

WHY NOT SIMPLY GIVE THE SCOUT BASH. A scout is a leaf worker and six of them
run at once. `Bash` is allowed outright in .claude/settings.json, so an
unrestricted shell would let a leaf worker write anywhere in the repo, drive
git, or start another agent process, which is precisely the uncapped fan-out
the routine's non-negotiable 7 was written after. The capability the scout is
owed is a PDF READER, not a shell.

SO THE SHELL IS KEPT AND NARROWED. .claude/agents/scout.md grants `Bash` and
attaches this file as a PreToolUse hook on the `Bash` matcher. Claude Code
feeds the hook the tool call as JSON on stdin and treats exit status 2 as a
block, with this script's stderr handed back to the agent as the reason. The
allowed set is exactly one command:

    python3 scripts/fetch_pdf_text.py <url> [--pages ...] [--max-chars ...]
                                            [--max-mb ...] [--timeout ...]
                                            [--json] [--self-test]

Everything else is denied, including `--out`, which is the one flag that makes
that script write a file. So the scout can turn a PDF URL into text and can do
nothing else: it can't write to the repo, can't reach git, and can't spawn a
process of any kind, quite apart from having no Task tool.

DEFAULT DENY, AND FAIL CLOSED. Unparseable stdin, an unparseable command line,
an unbalanced quote, or any shell metacharacter outside quotes is a denial. A
guard that guesses is not a guard.

  python3 scripts/scout_bash_guard.py --self-test    battery + wiring check

Exit codes as a hook: 0 allow, 2 deny. As --self-test: 0 pass, 1 fail.
Stdlib only. Reads nothing but stdin and, under --self-test, the agent file.
"""
from __future__ import annotations

import json
import os
import shlex
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READER_REL = "scripts/fetch_pdf_text.py"
READER_ABS = str((REPO / READER_REL).resolve())

INTERPRETERS = ("python3", "python")

# Every flag fetch_pdf_text.py accepts EXCEPT --out, which is the only one that
# writes a file. A scout returns text in its report; it has no business writing.
FLAGS_WITH_VALUE = ("--pages", "--max-chars", "--max-mb", "--timeout")
FLAGS_BARE = ("--json", "--self-test")
FLAGS_DENIED = ("--out",)

USAGE = ("the only shell command a scout may run is the PDF reader, e.g. "
         "python3 scripts/fetch_pdf_text.py 'https://host/doc.pdf' --pages 1-6 "
         "--max-chars 40000 . Put the URL in single quotes (an unquoted & or ? "
         "is a shell metacharacter and is refused). Everything else, including "
         "--out, is blocked; report the text in your findings instead of "
         "writing a file. Use WebFetch for anything that is not a PDF.")

# Outside quotes these start a new command, a pipe, a redirect or a
# substitution. Inside single quotes they are ordinary characters, which is
# what lets a URL carry & and ?.
METACHARS = set(";&|<>`()$\n\r{}!*?[]~#")


def unquoted_metachar(cmd):
    """Return the first shell metacharacter that sits OUTSIDE quotes, or None.

    Also returns a complaint for an unterminated quote and for a substitution
    inside double quotes, where $ and ` are still live.
    """
    i, state = 0, None
    while i < len(cmd):
        ch = cmd[i]
        if state is None:
            if ch == "\\":
                i += 2
                continue
            if ch in ("'", '"'):
                state = ch
                i += 1
                continue
            if ch in METACHARS:
                return repr(ch)
        elif state == "'":
            if ch == "'":
                state = None
        else:  # inside double quotes
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                state = None
            elif ch in ("$", "`"):
                return repr(ch) + " inside double quotes (still a substitution)"
        i += 1
    if state is not None:
        return "an unterminated %s quote" % ("single" if state == "'" else "double")
    return None


def is_reader_path(tok):
    """True when this argument names scripts/fetch_pdf_text.py and nothing else."""
    norm = os.path.normpath(tok).replace(os.sep, "/")
    if os.path.isabs(norm):
        try:
            return os.path.realpath(norm) == READER_ABS
        except OSError:
            return False
    if norm.startswith("../") or "/../" in norm:
        return False
    return norm == READER_REL


def decide(tool_name, tool_input):
    """Return (allow, reason). Reason is the text the agent is shown on a deny."""
    if tool_name != "Bash":
        return True, ""
    if not isinstance(tool_input, dict):
        return False, "the Bash call carried no readable input, so it is refused"
    cmd = tool_input.get("command")
    if not isinstance(cmd, str) or not cmd.strip():
        return False, "the Bash call carried no command, so it is refused"

    bad = unquoted_metachar(cmd)
    if bad:
        return False, ("this command contains %s outside quotes, so it could "
                       "chain or redirect. %s" % (bad, USAGE))
    try:
        toks = shlex.split(cmd)
    except ValueError as e:
        return False, "this command could not be parsed as a single command (%s). %s" % (e, USAGE)
    if len(toks) < 2:
        return False, "this is not the PDF reader. " + USAGE
    if toks[0] not in INTERPRETERS:
        return False, ("a scout may only run the PDF reader through %s. %s"
                       % (" or ".join(INTERPRETERS), USAGE))
    if not is_reader_path(toks[1]):
        return False, ("a scout may only run %s, not %r. %s"
                       % (READER_REL, toks[1], USAGE))

    i = 2
    positional = 0
    while i < len(toks):
        t = toks[i]
        if t in FLAGS_DENIED or any(t.startswith(f + "=") for f in FLAGS_DENIED):
            return False, ("%s writes a file and a scout does not write files. "
                           "Drop it and read the text from stdout." % t)
        if t in FLAGS_BARE:
            i += 1
            continue
        if t in FLAGS_WITH_VALUE:
            if i + 1 >= len(toks):
                return False, "%s was given no value. %s" % (t, USAGE)
            i += 2
            continue
        if any(t.startswith(f + "=") for f in FLAGS_WITH_VALUE):
            i += 1
            continue
        if t.startswith("-"):
            return False, "%s is not a flag the PDF reader accepts. %s" % (t, USAGE)
        positional += 1
        if positional > 1:
            return False, ("the PDF reader takes ONE url or path; %r is a second "
                           "one. Run it once per document." % t)
        i += 1
    return True, ""


# ------------------------------------------------------------------ self-test

FRONTMATTER_MUST_CONTAIN = (
    "PreToolUse",
    "matcher: Bash",
    "scripts/scout_bash_guard.py",
)


def _agent_frontmatter(path):
    text = path.read_text(encoding="utf8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end > 0 else None


def self_test():
    ok = True

    allow = [
        "python3 scripts/fetch_pdf_text.py https://dnr.alaska.gov/doc.pdf",
        "python3 scripts/fetch_pdf_text.py 'https://x.gov/d.pdf?id=1&v=2'",
        "python3 scripts/fetch_pdf_text.py \"https://x.gov/d.pdf\" --pages 1-6",
        "python scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-chars 40000 --json",
        "python3 ./scripts/fetch_pdf_text.py https://x.gov/d.pdf --timeout 60",
        "python3 %s https://x.gov/d.pdf" % READER_ABS,
        "python3 scripts/fetch_pdf_text.py --self-test",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-mb 60",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --pages=1-6",
    ]
    deny = [
        # the blast radius this guard exists to remove
        "python3 -c \"open('ledger/topics.json','w').write('[]')\"",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --out /tmp/a.txt",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --out=/tmp/a.txt",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf; rm -rf runs",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf && git push",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf | tee /tmp/a",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf > /tmp/a.txt",
        "cd /tmp && python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf",
        "python3 $(echo scripts/fetch_pdf_text.py) https://x.gov/d.pdf",
        "python3 \"$HOME/evil.py\"",
        "python3 `which evil` https://x.gov/d.pdf",
        "claude -p 'spawn more scouts'",
        "curl https://x.gov/d.pdf -o /tmp/d.pdf",
        "bash scripts/fetch_pdf_text.py https://x.gov/d.pdf",
        "python3 scripts/../scripts/fetch_pdf_text.py https://x.gov/d.pdf; ls",
        "python3 scripts/docket_watch.py",
        "python3 scripts/fetch_pdf_text.py a.pdf b.pdf",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --pages",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --quiet",
        "python3 scripts/fetch_pdf_text.py 'https://x.gov/d.pdf",
        "echo hi",
        "",
    ]

    for cmd in allow:
        allowed, why = decide("Bash", {"command": cmd})
        if not allowed:
            print("  FAIL  should ALLOW: %s\n        denied: %s" % (cmd, why))
            ok = False
    for cmd in deny:
        allowed, _ = decide("Bash", {"command": cmd})
        if allowed:
            print("  FAIL  should DENY: %s" % cmd)
            ok = False

    # a non-Bash tool is none of this guard's business
    if not decide("WebFetch", {"url": "https://x"})[0]:
        print("  FAIL  a non-Bash tool must pass straight through")
        ok = False
    # malformed input fails CLOSED
    for bad_input in (None, "", [], {"description": "no command"}):
        if decide("Bash", bad_input)[0]:
            print("  FAIL  malformed tool_input must be denied: %r" % (bad_input,))
            ok = False

    # THE WIRING. A guard that is not attached protects nothing, and the
    # failure mode of a mis-spelled hooks block is that Claude Code logs it and
    # carries on with an UNGUARDED Bash, so this half matters as much as the
    # battery above.
    agent = REPO / ".claude" / "agents" / "scout.md"
    fm = _agent_frontmatter(agent) if agent.exists() else None
    if fm is None:
        print("  FAIL  .claude/agents/scout.md has no readable frontmatter")
        ok = False
    else:
        for needle in FRONTMATTER_MUST_CONTAIN:
            if needle not in fm:
                print("  FAIL  scout.md frontmatter is missing %r; the guard is "
                      "not attached and the scout's Bash would be unguarded" % needle)
                ok = False
        for banned in ("Task", "Write", "Edit", "NotebookEdit"):
            line = [l for l in fm.splitlines() if l.strip().startswith("tools:")]
            if line and banned in line[0]:
                print("  FAIL  scout.md grants %s; a leaf worker must not write "
                      "or spawn" % banned)
                ok = False
        if not (REPO / READER_REL).exists():
            print("  FAIL  %s does not exist, so the one allowed command is a "
                  "dead reference" % READER_REL)
            ok = False

    print("scout_bash_guard self-test: %s (%d allow, %d deny, plus wiring)"
          % ("PASS" if ok else "FAIL", len(allow), len(deny)))
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        sys.stderr.write("scout guard: the tool call could not be read (%s), so "
                         "it is refused. %s\n" % (e, USAGE))
        return 2
    allowed, reason = decide(payload.get("tool_name"), payload.get("tool_input"))
    if allowed:
        return 0
    sys.stderr.write("scout guard: BLOCKED. " + reason + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
