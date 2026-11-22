"""
A4 (Cris): add ONE small bug at a time to each of the 34 original programs.

Purpose: measure how strong our tests are. If hidden tests + new inputs catch
fewer than half of these bugs, "all refactored versions kept their behavior" is
not reliable (RQ1).

Mutation kinds (one change per mutant, applied to the AST, then ast.unparse):
  relational   < <-> <=, > <-> >=, == <-> !=
  arithmetic   + <-> -, * <-> //
  logical      and <-> or
  negation     "not x" -> "x"
  constant     integer constant c -> c+1 or c-1
  augassign    += <-> -=

Reproducible: fixed seed (default 5570); per-program RNG = sha1(f"{seed}-{pid}").
Selection is stratified: shuffled round-robin over kinds, so every kind that
exists in a program is represented before any kind repeats.

Mutants that do not run are removed: syntax error, crash, or timeout on any
PUBLIC test input. (Mutants that only produce wrong output are kept; they are
the bugs we want the tests to catch.) Mutants whose source text equals the
reference rendering (ast.unparse of the original) are dropped.

Reference rendering: every mutant is compared with ast.unparse(original), so the
ONLY difference between a mutant and its reference is the one injected change.
The reference rendering is also checked against the public tests (sanity).

Outputs
  data/buggy/<pid>/<pid>_bNN.py      the buggy programs
  data/buggy_programs.csv            one row per kept mutant
  data/buggy_report.json             counts: generated / removed (by reason) / kept, by kind and by program

Usage:  python scripts/inject_bugs.py [--seed 5570] [--per-program 15] [--workers 8]
"""
import argparse
import ast
import copy
import csv
import hashlib
import json
import os
import random
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS = ["relational", "arithmetic", "logical", "negation", "constant", "augassign"]

REL = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
       ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}
ARITH = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.FloorDiv, ast.FloorDiv: ast.Mult}
AUG = {ast.Add: ast.Sub, ast.Sub: ast.Add}
LOGIC = {ast.And: ast.Or, ast.Or: ast.And}
SYM = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=", ast.Eq: "==", ast.NotEq: "!=",
       ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.FloorDiv: "//", ast.And: "and", ast.Or: "or"}


def _is_str(n):
    return isinstance(n, ast.Constant) and isinstance(n.value, (str, bytes))


def _docstring_ids(tree):
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and _is_str(b[0].value):
                ids.add(id(b[0].value))
    return ids


def find_sites(tree):
    """Return a list of dicts: {idx, kind, sub, desc, lineno}. idx = position in ast.walk order."""
    nodes = list(ast.walk(tree))
    doc = _docstring_ids(tree)
    sites = []
    for idx, n in enumerate(nodes):
        ln = getattr(n, "lineno", 0)
        if isinstance(n, ast.Compare):
            for i, op in enumerate(n.ops):
                if type(op) in REL:
                    sites.append(dict(idx=idx, kind="relational", sub=i, lineno=ln,
                                      desc=f"{SYM[type(op)]} -> {SYM[REL[type(op)]]}"))
        elif isinstance(n, ast.BinOp) and type(n.op) in ARITH and not (_is_str(n.left) or _is_str(n.right)):
            sites.append(dict(idx=idx, kind="arithmetic", sub=0, lineno=ln,
                              desc=f"{SYM[type(n.op)]} -> {SYM[ARITH[type(n.op)]]}"))
        elif isinstance(n, ast.BoolOp) and type(n.op) in LOGIC:
            sites.append(dict(idx=idx, kind="logical", sub=0, lineno=ln,
                              desc=f"{SYM[type(n.op)]} -> {SYM[LOGIC[type(n.op)]]}"))
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            sites.append(dict(idx=idx, kind="negation", sub=0, lineno=ln, desc="not x -> x"))
        elif (isinstance(n, ast.Constant) and type(n.value) is int and id(n) not in doc):
            for d in (+1, -1):
                sites.append(dict(idx=idx, kind="constant", sub=d, lineno=ln,
                                  desc=f"{n.value} -> {n.value + d}"))
        elif isinstance(n, ast.AugAssign) and type(n.op) in AUG:
            sites.append(dict(idx=idx, kind="augassign", sub=0, lineno=ln,
                              desc=f"{SYM[type(n.op)]}= -> {SYM[AUG[type(n.op)]]}="))
    return sites


def apply_site(tree, site):
    t = copy.deepcopy(tree)
    nodes = list(ast.walk(t))
    n, k = nodes[site["idx"]], site["kind"]
    if k == "relational":
        n.ops[site["sub"]] = REL[type(n.ops[site["sub"]])]()
        return t
    if k == "arithmetic":
        n.op = ARITH[type(n.op)]()
        return t
    if k == "logical":
        n.op = LOGIC[type(n.op)]()
        return t
    if k == "augassign":
        n.op = AUG[type(n.op)]()
        return t
    if k == "constant":
        n.value = n.value + site["sub"]
        return t
    if k == "negation":
        # replace the UnaryOp node with its operand: find its parent and swap
        for p in nodes:
            for f, v in ast.iter_fields(p):
                if v is n:
                    setattr(p, f, n.operand)
                    return t
                if isinstance(v, list):
                    for j, c in enumerate(v):
                        if c is n:
                            v[j] = n.operand
                            return t
    raise RuntimeError("site not applicable")


def run_public(code_path, tests_path, timeout=5.0):
    """Return (ok, reason). ok = compiled and ran on every PUBLIC input without error/timeout."""
    with open(tests_path, encoding="utf-8") as f:
        cases = json.load(f)["public"]
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    for c in cases:
        try:
            p = subprocess.run([sys.executable, code_path], input=c["input"].encode(),
                               capture_output=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            return False, "timeout"
        if p.returncode != 0:
            return False, "crash"
    return True, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=5570)
    ap.add_argument("--per-program", type=int, default=15)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--programs-csv", default=os.path.join(ROOT, "data", "programs.csv"))
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "buggy"))
    args = ap.parse_args()

    with open(args.programs_csv, encoding="utf-8") as f:
        progs = list(csv.DictReader(f))

    os.makedirs(args.out, exist_ok=True)
    rows, removed, generated = [], Counter(), Counter()
    per_prog_sites = {}
    ref_problems = []

    for pr in progs:
        pid = pr["program_id"]
        src = open(os.path.join(ROOT, pr["code_path"]), encoding="utf-8").read()
        tree = ast.parse(src)
        ref_src = ast.unparse(tree) + "\n"
        sites = find_sites(tree)
        per_prog_sites[pid] = len(sites)

        pdir = os.path.join(args.out, pid)
        os.makedirs(pdir, exist_ok=True)
        # sanity: the reference rendering must pass the public tests
        ref_path = os.path.join(pdir, "_reference_unparse.py")
        open(ref_path, "w", encoding="utf-8").write(ref_src)
        ok, why = run_public(ref_path, os.path.join(ROOT, pr["tests_path"]))
        if not ok:
            ref_problems.append((pid, why))
        os.remove(ref_path)

        rng = random.Random(int(hashlib.sha1(f"{args.seed}-{pid}".encode()).hexdigest(), 16))
        by_kind = defaultdict(list)
        for s in sites:
            by_kind[s["kind"]].append(s)
        for k in by_kind:
            rng.shuffle(by_kind[k])
        kinds = [k for k in KINDS if by_kind[k]]
        rng.shuffle(kinds)

        # candidate order: round-robin over kinds (stratified), more candidates than needed
        order = []
        while any(by_kind[k] for k in kinds):
            for k in kinds:
                if by_kind[k]:
                    order.append(by_kind[k].pop())

        kept, seen = [], {ref_src}
        for s in order:
            if len(kept) >= args.per_program:
                break
            m_src = ast.unparse(apply_site(tree, s)) + "\n"
            generated[s["kind"]] += 1
            if m_src in seen:
                removed["duplicate_or_identical"] += 1
                continue
            seen.add(m_src)
            n = len(kept) + 1
            path = os.path.join(pdir, f"{pid}_b{n:02d}.py")
            open(path, "w", encoding="utf-8").write(m_src)
            ok, why = run_public(path, os.path.join(ROOT, pr["tests_path"]))
            if not ok:
                removed[why] += 1
                generated[s["kind"] + "__removed"] += 1
                os.remove(path)
                continue
            kept.append((s, path))
            rows.append(dict(bug_id=f"{pid}_b{n:02d}", program_id=pid, problem_id=pr["problem_id"],
                             kind=s["kind"], change=s["desc"], lineno=s["lineno"],
                             code_path=os.path.relpath(path, ROOT).replace(os.sep, "/"),
                             tests_path=pr["tests_path"]))
        print(f"{pid}: sites={len(sites)} kept={len(kept)}", flush=True)

    csv_path = os.path.join(ROOT, "data", "buggy_programs.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    report = dict(
        seed=args.seed, per_program_cap=args.per_program, programs=len(progs),
        kept=len(rows),
        kept_by_kind=dict(Counter(r["kind"] for r in rows)),
        removed_total=sum(removed.values()), removed_by_reason=dict(removed),
        kept_by_program=dict(Counter(r["program_id"] for r in rows)),
        mutation_sites_by_program=per_prog_sites,
        reference_rendering_failures=ref_problems,
    )
    with open(os.path.join(ROOT, "data", "buggy_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: report[k] for k in ("kept", "kept_by_kind", "removed_by_reason",
                                             "reference_rendering_failures")}, indent=2))


if __name__ == "__main__":
    main()
