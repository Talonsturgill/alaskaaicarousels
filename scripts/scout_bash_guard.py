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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import url_safety  # noqa: E402  (same directory, after sys.path is set)

REPO = Path(__file__).resolve().parent.parent
READER_REL = "scripts/fetch_pdf_text.py"
READER_ABS = str((REPO / READER_REL).resolve())
GUARD_REL = "scripts/scout_bash_guard.py"
GUARD_ABS = str(Path(__file__).resolve())

INTERPRETERS = ("python3", "python")

# Every flag fetch_pdf_text.py accepts EXCEPT --out, which is the only one that
# writes a file. A scout returns text in its report; it has no business writing.
FLAGS_WITH_VALUE = ("--pages", "--max-chars", "--max-mb", "--timeout")
FLAGS_BARE = ("--json", "--self-test")
FLAGS_DENIED = ("--out",)

# CEILINGS ON THE NUMERIC FLAGS. Without these the one allowed command is a
# memory and time lever: --max-mb 100000 on a hostile URL is an out-of-memory
# kill of the whole run, and a long --timeout parks a scout forever. The values
# are the reader's own documented defaults, roughly doubled, so no honest fetch
# meets them.
FLAG_CEILINGS = {"--max-mb": 64, "--max-chars": 400000, "--timeout": 120}

# THE TARGET MUST BE A PUBLIC http(s) URL, and the policy that decides that
# lives in scripts/url_safety.py, beside the socket that opens it, NOT here.
# Two review rounds on run No.66 are the reason. The first found that the
# command shape was pinned and the target never was, so the reader turned a
# bare path into file:// by itself. The second found two ways past a
# string-only check that lived only in this hook: a legacy numeric host such
# as http://2852039166/, which ipaddress rejects and the resolver reads as
# 169.254.169.254, and a public URL that simply answers 302 to a loopback
# address, which this hook never sees at all.
#
# So the hook is a PRE-CHECK and the reader is the guarantee. Both call
# url_safety.check_url; fetch_pdf_text.py calls it again on every redirect hop.
# resolve=False here, because a hook runs on every Bash call and a DNS lookup
# in it would be latency for a decision the reader makes properly anyway.

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


def is_guard_path(tok):
    """True when this argument names THIS guard file and nothing else.

    A basename test is not enough, and review measured why: `python3
    /tmp/scout_bash_guard.py` would have certified the wiring while running a
    stale copy or a no-op with the same name. The hook's whole value is that a
    Bash grant cannot exist without THIS file screening it, so the wiring check
    has to resolve the path rather than read its last component.

    `$CLAUDE_PROJECT_DIR` is expanded because that is the spelling the agent
    file documents and the harness substitutes; the guard is asked whether the
    wiring is right, and the wiring is written in the harness's vocabulary.
    """
    tok = tok.strip()
    for spelling in ("${CLAUDE_PROJECT_DIR}", "$CLAUDE_PROJECT_DIR"):
        if tok.startswith(spelling):
            tok = str(REPO) + tok[len(spelling):]
            break
    if "$" in tok:                      # any other variable is unresolvable here
        return False
    norm = os.path.normpath(tok).replace(os.sep, "/")
    if os.path.isabs(norm):
        try:
            return os.path.realpath(norm) == GUARD_ABS
        except OSError:
            return False
    if norm.startswith("../") or "/../" in norm:
        return False
    return norm == GUARD_REL


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


def bad_target(tok):
    """Why this positional is not a public PDF URL, or None if it is fine."""
    return url_safety.check_url(tok, resolve=False)


def bad_flag_value(flag, value):
    """Why this numeric flag value is out of bounds, or None if it is fine."""
    ceiling = FLAG_CEILINGS.get(flag)
    if ceiling is None:
        return None
    try:
        n = float(value)
    except (TypeError, ValueError):
        return "%s takes a number, not %r. %s" % (flag, value, USAGE)
    if n <= 0:
        return "%s must be positive, not %r." % (flag, value)
    if n > ceiling:
        return ("%s is capped at %s for a scout, and %r is above it. The cap "
                "is there so one fetch can't exhaust the run's memory or "
                "park the scout." % (flag, ceiling, value))
    return None


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
            why = bad_flag_value(t, toks[i + 1])
            if why:
                return False, why
            i += 2
            continue
        matched = [f for f in FLAGS_WITH_VALUE if t.startswith(f + "=")]
        if matched:
            why = bad_flag_value(matched[0], t.split("=", 1)[1])
            if why:
                return False, why
            i += 1
            continue
        if t.startswith("-"):
            return False, "%s is not a flag the PDF reader accepts. %s" % (t, USAGE)
        why = bad_target(t)
        if why:
            return False, why + " " + USAGE
        positional += 1
        if positional > 1:
            return False, ("the PDF reader takes ONE url; %r is a second "
                           "one. Run it once per document." % t)
        i += 1
    if positional != 1 and "--self-test" not in toks:
        return False, ("the PDF reader needs exactly one public http or https "
                       "URL. %s" % USAGE)
    return True, ""


# ------------------------------------------------------------------ self-test

FRONTMATTER_MUST_CONTAIN = (
    "PreToolUse",
    "matcher: Bash",
    "scripts/scout_bash_guard.py",
)


def hook_is_wired(fm_text):
    """Why this frontmatter's Bash hook is not actually wired, or None.

    PARSED, NOT GREPPED. The first version of this check looked for three
    substrings in the raw frontmatter, and review showed a frontmatter that
    granted Bash with all three hook lines COMMENTED OUT still passed: the
    needles were all present in the text, and Claude would have ignored the
    YAML comments and handed a leaf worker an unguarded shell. A check that a
    comment satisfies is not a check.

    So the structure is walked: hooks -> PreToolUse -> an entry whose matcher
    mentions Bash -> a command hook naming this file. If PyYAML is missing the
    caller is told that, rather than being told everything is fine.
    """
    try:
        import yaml
    except ImportError:                                  # pragma: no cover
        return ("PyYAML is not installed, so the hook wiring cannot be parsed "
                "and this check cannot vouch for it")
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        return "the frontmatter is not valid YAML (%s)" % exc
    if not isinstance(fm, dict):
        return "the frontmatter is not a mapping"

    hooks = fm.get("hooks")
    if not isinstance(hooks, dict):
        return "there is no `hooks:` mapping"
    pre = hooks.get("PreToolUse")
    if not isinstance(pre, list) or not pre:
        return "`hooks.PreToolUse` is missing or is not a list"

    for entry in pre:
        if not isinstance(entry, dict):
            continue
        matcher = entry.get("matcher")
        if not isinstance(matcher, str) or "Bash" not in matcher:
            continue
        inner = entry.get("hooks")
        if not isinstance(inner, list):
            continue
        for h in inner:
            if not isinstance(h, dict):
                continue
            if h.get("type") != "command":
                continue
            cmd = h.get("command")
            if not isinstance(cmd, str) or not cmd.strip():
                continue
            # THE COMMAND IS PARSED, not searched. `echo scout_bash_guard.py`
            # mentions this file and runs nothing, and a hook that runs nothing
            # allows every Bash call, so a substring test could certify an
            # unguarded shell. Require an interpreter with this script as its
            # argument, which is the only shape that actually executes it.
            try:
                parts = shlex.split(cmd)
            except ValueError:
                continue
            if len(parts) < 2:
                continue
            interp = os.path.basename(parts[0]).lower()
            if interp not in ("python3", "python", "python3.11", "python3.12"):
                continue
            # -c and -m never run THIS FILE. `-c` runs the string that follows
            # and `-m` runs whatever the import system finds, so the name
            # appearing after either proves nothing about what executes.
            if any(a in ("-c", "-m") for a in parts[1:]):
                continue
            # AND THE PATH IS RESOLVED, not read for its last component.
            # `python3 /tmp/scout_bash_guard.py` has the right shape and the
            # right basename and can be anything at all.
            if any(is_guard_path(a) for a in parts[1:] if not a.startswith("-")):
                return None
        return ("the PreToolUse entry matching Bash has no command hook "
                "running this repository's scripts/scout_bash_guard.py")
    return "no PreToolUse entry matches Bash"


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
        "python3 scripts/fetch_pdf_text.py HTTPS://X.GOV/D.PDF",
        "python3 scripts/fetch_pdf_text.py https://x.gov:8443/d.pdf",
        "python3 scripts/fetch_pdf_text.py https://8.8.8.8/d.pdf",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-mb=64",
    ]
    deny = [
        # THE TARGET, which the first version of this guard never checked. The
        # reader turns a bare path into file:// by itself, so a command shape
        # that is exactly right can still read the container's own disk.
        "python3 scripts/fetch_pdf_text.py /etc/passwd",
        "python3 scripts/fetch_pdf_text.py file:///etc/passwd",
        "python3 scripts/fetch_pdf_text.py FILE:///etc/shadow",
        "python3 scripts/fetch_pdf_text.py ledger/gaswatch.jsonl",
        "python3 scripts/fetch_pdf_text.py ../../etc/passwd",
        "python3 scripts/fetch_pdf_text.py ftp://x.gov/d.pdf",
        "python3 scripts/fetch_pdf_text.py data:application/pdf;base64,AAAA",
        "python3 scripts/fetch_pdf_text.py http://localhost/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://LOCALHOST:8080/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://127.0.0.1/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://0.0.0.0/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://10.0.0.5/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://192.168.1.1/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://169.254.169.254/latest/meta-data/",
        "python3 scripts/fetch_pdf_text.py http://metadata.google.internal/x",
        "python3 scripts/fetch_pdf_text.py http://[::1]/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://user:pw@127.0.0.1/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://build.internal/d.pdf",
        # the legacy numeric spellings the second review round found. every one
        # of these resolves to loopback or to the metadata endpoint.
        "python3 scripts/fetch_pdf_text.py http://2852039166/latest/meta-data/",
        "python3 scripts/fetch_pdf_text.py http://127.1/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://0x7f000001/d.pdf",
        "python3 scripts/fetch_pdf_text.py http://017700000001/d.pdf",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-mb 100000",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-mb=99999",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --timeout 86400",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-chars 99999999",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --max-mb -1",
        "python3 scripts/fetch_pdf_text.py https://x.gov/d.pdf --timeout abc",
        "python3 scripts/fetch_pdf_text.py --json",
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
    # FIRST, THE WIRING CHECK ITSELF, against synthetic frontmatter. Three
    # rounds of review landed on this function and each one certified a hook
    # that ran something other than this file: a commented-out line, then
    # `echo scout_bash_guard.py`, then `/tmp/scout_bash_guard.py`. A check
    # that says yes to those is worse than no check, because it reports the
    # shell is guarded while it is not. So the cases are pinned here.
    def _fm(cmd):
        return ("name: probe\ntools: Bash\nhooks:\n  PreToolUse:\n"
                "    - matcher: Bash\n      hooks:\n        - type: command\n"
                "          command: %s\n" % json.dumps(cmd))

    for cmd, want_wired in [
            ("python3 scripts/scout_bash_guard.py", True),
            ('python3 "$CLAUDE_PROJECT_DIR/scripts/scout_bash_guard.py"', True),
            ("python3 ${CLAUDE_PROJECT_DIR}/scripts/scout_bash_guard.py", True),
            ("python3 %s" % GUARD_ABS, True),
            ("echo scout_bash_guard.py", False),
            ("cat scripts/scout_bash_guard.py", False),
            ("bash -c 'scout_bash_guard.py'", False),
            ('python3 -c \'print("scout_bash_guard.py")\'', False),
            ("python3 -m scout_bash_guard", False),
            ("python3 /tmp/scout_bash_guard.py", False),
            ("python3 ./fake/scout_bash_guard.py", False),
            ("python3 ../scout_bash_guard.py", False),
            ("python3 $SOMETHING/scout_bash_guard.py", False),
            ("python3 scripts/fetch_pdf_text.py", False)]:
        wired = hook_is_wired(_fm(cmd)) is None
        if wired != want_wired:
            print("  FAIL  wiring check called %r %s" %
                  (cmd, "wired" if wired else "not wired"))
            ok = False

    agent = REPO / ".claude" / "agents" / "scout.md"
    fm = _agent_frontmatter(agent) if agent.exists() else None
    if fm is None:
        print("  FAIL  .claude/agents/scout.md has no readable frontmatter")
        ok = False
    else:
        # THE INVARIANT IS CONDITIONAL, and that is the point of it: IF the
        # scout is granted Bash, THEN this guard must be attached. It is not
        # "the scout must have Bash". Run No.66 withheld the grant after five
        # rounds of review found a bypass every round and a reproduced DNS
        # rebinding it could not close in the time it had, and an assertion
        # that demanded the grant would have failed the build for doing the
        # careful thing. Written this way it stays useful for the case that
        # actually matters: a future run pastes the grant back and forgets the
        # hook, and this goes red instead of shipping an unguarded shell to six
        # leaf workers at once.
        tools_line = next((l for l in fm.splitlines()
                           if l.strip().startswith("tools:")), "")
        grants_bash = "Bash" in tools_line
        if not grants_bash:
            print("  ok    scout.md withholds Bash, so the guard is inert and "
                  "its wiring is not required")
        else:
            why = hook_is_wired(fm)
            if why:
                print("  FAIL  scout.md grants Bash but %s; that Bash would be "
                      "unguarded" % why)
                ok = False
            else:
                print("  ok    scout.md grants Bash and the guard is wired to "
                      "it, verified against the parsed frontmatter")
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
