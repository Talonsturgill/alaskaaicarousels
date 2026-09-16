#!/usr/bin/env python3
"""unbound_names_check.py -- module-scope names a file USES but nothing BINDS.

WHY THIS EXISTS
    On 2026-09-15, run No.60's slide 06 declared 1,347 marks with
    `dispersed: true`. render.py strides any census over 240 centres, so
    qa.py's marks_disperse() took its `stride > 1` branch for the first time
    in the gate's life and died on

        NameError: name 'MARK_PROBE_MAX' is not defined

    The constant is real. render.py defines it (`const MARK_PROBE_MAX = 240`),
    three of qa.py's own docstrings quote it by name and by value, and the one
    line that actually READS it was never given a Python binding. Nothing
    caught it because Python resolves module-scope names at RUN time, so the
    file imports, compiles and passes every other gate. The only way to find
    it was to take that branch, and the only way to take that branch was to
    ship a deck with more than 240 dispersed marks.

    That is the shape worth gating. A gate that crashes is worse than a gate
    that fails, because a crash takes the whole QA pass with it and tells the
    run nothing about the deck. This machine is mostly gates, most of their
    branches are rare by design (they fire on defects), and a rare branch is
    exactly where an unbound name hides.

WHAT IT DOES
    Walks each file's AST, collects every name bound at module scope or
    reachable from it (imports, assignments, function and class defs,
    comprehension and except targets, globals, builtins, and the file's own
    parameters and locals per function), then reports every `Name` load that
    no binding covers.

    It is deliberately CONSERVATIVE. A false alarm here would train people to
    ignore it, which is worse than silence, so anything it cannot resolve
    cleanly it stays quiet about: star imports disable the file, `globals()`
    and `locals()` tricks disable the file, and a name bound anywhere in the
    module counts as bound everywhere.

USAGE
    python scripts/unbound_names_check.py                 # engine + scripts
    python scripts/unbound_names_check.py --path a.py b.py
    python scripts/unbound_names_check.py --json

    Exit 0 clean, 1 when a file references a name nothing binds.

NOT A TYPE CHECKER. It answers one question, which is the question that cost
this run a crash: does every module-scope name this file reads actually exist.
"""
import argparse
import ast
import builtins
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PATHS = [ROOT / "scripts", ROOT / ".claude" / "skills" / "carousel-engine"]
BUILTINS = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__spec__",
                                 "__package__", "__loader__", "__builtins__"}


def _targets(node, out):
    """Every name a binding construct binds, including tuple and star targets."""
    if isinstance(node, ast.Name):
        out.add(node.id)
    elif isinstance(node, (ast.Tuple, ast.List)):
        for e in node.elts:
            _targets(e, out)
    elif isinstance(node, ast.Starred):
        _targets(node.value, out)
    # Attribute and Subscript targets bind nothing new.


class Collector(ast.NodeVisitor):
    """Every name bound anywhere in the module, plus every name loaded."""

    def __init__(self):
        self.bound = set()
        self.loaded = []          # (name, lineno)
        self.opaque = False       # star import or a globals()/locals() trick

    def visit_Import(self, n):
        for a in n.names:
            self.bound.add((a.asname or a.name).split(".")[0])

    def visit_ImportFrom(self, n):
        for a in n.names:
            if a.name == "*":
                self.opaque = True
            else:
                self.bound.add(a.asname or a.name)

    def visit_FunctionDef(self, n):
        self.bound.add(n.name)
        self._args(n)
        self.generic_visit(n)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _args(self, n):
        a = n.args
        for x in list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs):
            self.bound.add(x.arg)
        if a.vararg:
            self.bound.add(a.vararg.arg)
        if a.kwarg:
            self.bound.add(a.kwarg.arg)

    def visit_Lambda(self, n):
        self._args(n)
        self.generic_visit(n)

    def visit_ClassDef(self, n):
        self.bound.add(n.name)
        self.generic_visit(n)

    def visit_Assign(self, n):
        for t in n.targets:
            _targets(t, self.bound)
        self.generic_visit(n)

    def visit_AnnAssign(self, n):
        _targets(n.target, self.bound)
        self.generic_visit(n)

    def visit_AugAssign(self, n):
        _targets(n.target, self.bound)
        self.generic_visit(n)

    def visit_NamedExpr(self, n):
        _targets(n.target, self.bound)
        self.generic_visit(n)

    def visit_For(self, n):
        _targets(n.target, self.bound)
        self.generic_visit(n)

    visit_AsyncFor = visit_For

    def visit_comprehension(self, n):
        _targets(n.target, self.bound)
        self.generic_visit(n)

    def visit_withitem(self, n):
        if n.optional_vars is not None:
            _targets(n.optional_vars, self.bound)
        self.generic_visit(n)

    def visit_ExceptHandler(self, n):
        if n.name:
            self.bound.add(n.name)
        self.generic_visit(n)

    def visit_Global(self, n):
        self.bound.update(n.names)

    def visit_Nonlocal(self, n):
        self.bound.update(n.names)

    def visit_MatchAs(self, n):
        if n.name:
            self.bound.add(n.name)
        self.generic_visit(n)

    def visit_MatchStar(self, n):
        if n.name:
            self.bound.add(n.name)
        self.generic_visit(n)

    def visit_MatchMapping(self, n):
        if n.rest:
            self.bound.add(n.rest)
        self.generic_visit(n)

    def visit_Call(self, n):
        # A file that reaches into its own namespace can bind anything.
        if isinstance(n.func, ast.Name) and n.func.id in ("globals", "locals", "vars", "exec", "eval"):
            self.opaque = True
        self.generic_visit(n)

    def visit_Name(self, n):
        if isinstance(n.ctx, ast.Load):
            self.loaded.append((n.id, n.lineno))
        else:
            self.bound.add(n.id)


def check_file(path):
    """Return a list of (name, lineno) this file loads and never binds."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError) as e:
        return [("<unparseable: %s>" % e.__class__.__name__, 0)]
    c = Collector()
    c.visit(tree)
    if c.opaque:
        return []
    seen, out = set(), []
    for name, line in c.loaded:
        if name in c.bound or name in BUILTINS or name in seen:
            continue
        seen.add(name)
        out.append((name, line))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", nargs="*", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.path:
        files = [pathlib.Path(p) for p in args.path]
    else:
        files = []
        for d in DEFAULT_PATHS:
            files.extend(sorted(d.glob("*.py")))

    findings, n_ok = {}, 0
    for f in files:
        bad = check_file(f)
        if bad:
            try:
                rel = str(f.relative_to(ROOT))
            except ValueError:
                rel = str(f)          # a path outside the repo, e.g. a reconstruction copy
            findings[rel] = [{"name": n, "line": l} for n, l in bad]
        else:
            n_ok += 1

    if args.json:
        print(json.dumps({"checked": len(files), "clean": n_ok, "findings": findings}, indent=2))
    else:
        for rel, items in findings.items():
            for it in items:
                print("FAIL: %s:%d references '%s' and nothing in the module binds it. "
                      "Python resolves this at RUN time, so the file imports and every "
                      "other gate passes; the branch that reads it raises NameError the "
                      "first time it is taken. Define it, import it, or delete the line."
                      % (rel, it["line"], it["name"]))
        if findings:
            print("unbound_names_check: FAIL -- %d file(s) of %d reference a name nothing binds"
                  % (len(findings), len(files)))
        else:
            print("unbound_names_check: PASS -- %d file(s), every module-scope name resolves"
                  % len(files))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
