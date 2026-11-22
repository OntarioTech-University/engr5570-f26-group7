"""
Early pilot (Cris): how many injected bugs do the hidden tests / new inputs catch?

This is a STAND-IN for Yujie's A4 job (her run_tests / compare_outputs are the
official ones). It uses the same rules as Part 2 and Part 4 of the Shared
Interfaces (normalize CRLF, rstrip lines, drop trailing empty lines, 5 s timeout).

A bug is "caught by hidden tests" if the mutant fails at least one hidden test
(private + generated; a crash or timeout counts as a failure).
A bug is "caught by new inputs" if the mutant's output differs from the ORIGINAL
program's output on at least one data/new_inputs input (original = reference).

Usage: python scripts/pilot_kill_rate.py [--programs p001,p002] [--limit N]
Writes data/buggy_pilot_results.csv and data/buggy_pilot_summary.json
"""
import argparse
import csv
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from check_runner import _normalize  # same normalization as Part 2

ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")


def run(code_path, inp, timeout=5.0):
    try:
        p = subprocess.run([sys.executable, code_path], input=inp.encode("utf-8"),
                           capture_output=True, timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode != 0:
        return None
    return _normalize(p.stdout.decode("utf-8", errors="replace"))


def caught_by_hidden(code, tests):
    cases = tests["private"] + tests["generated"]
    for c in cases:
        out = run(code, c["input"])
        if out is None or out != _normalize(c["output"]):
            return True
    return False


def caught_by_new(code, inputs, ref_outputs):
    for inp, ref in zip(inputs, ref_outputs):
        if ref is None:
            continue
        out = run(code, inp)
        if out is None or out != ref:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--programs", default="")
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    want = set(filter(None, args.programs.split(",")))

    with open(os.path.join(ROOT, "data", "buggy_programs.csv"), encoding="utf-8") as f:
        bugs = [b for b in csv.DictReader(f) if not want or b["program_id"] in want]
    with open(os.path.join(ROOT, "data", "programs.csv"), encoding="utf-8") as f:
        orig = {r["program_id"]: r for r in csv.DictReader(f)}

    by_prog = defaultdict(list)
    for b in bugs:
        by_prog[b["program_id"]].append(b)

    results = []

    def do_program(pid):
        tests = json.load(open(os.path.join(ROOT, orig[pid]["tests_path"]), encoding="utf-8"))
        inputs = json.load(open(os.path.join(ROOT, "data", "new_inputs", f"{pid}.json")))["inputs"]
        ocode = os.path.join(ROOT, orig[pid]["code_path"])
        ref = [run(ocode, i) for i in inputs]
        out = []
        for b in by_prog[pid]:
            code = os.path.join(ROOT, b["code_path"])
            h = caught_by_hidden(code, tests)
            n = caught_by_new(code, inputs, ref)
            out.append(dict(b, hidden=int(h), new_inputs=int(n), both=int(h and n), either=int(h or n)))
        print(f"{pid}: {sum(r['either'] for r in out)}/{len(out)} caught", flush=True)
        return out

    with ThreadPoolExecutor(args.workers) as ex:
        for r in ex.map(do_program, sorted(by_prog)):
            results.extend(r)

    fields = list(results[0].keys())
    with open(os.path.join(ROOT, "data", "buggy_pilot_results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    N = len(results)
    s = dict(n_bugs=N,
             hidden=sum(r["hidden"] for r in results),
             new_inputs=sum(r["new_inputs"] for r in results),
             both_caught=sum(r["both"] for r in results),
             either=sum(r["either"] for r in results),
             missed_by_all=N - sum(r["either"] for r in results))
    kinds = {}
    for k in sorted({r["kind"] for r in results}):
        rs = [r for r in results if r["kind"] == k]
        kinds[k] = dict(n=len(rs), hidden=sum(r["hidden"] for r in rs),
                        new_inputs=sum(r["new_inputs"] for r in rs),
                        either=sum(r["either"] for r in rs))
    s["by_kind"] = kinds
    s["missed_ids"] = [r["bug_id"] for r in results if not r["either"]]
    with open(os.path.join(ROOT, "data", "buggy_pilot_summary.json"), "w") as f:
        json.dump(s, f, indent=2)
    print(json.dumps({k: v for k, v in s.items() if k != "missed_ids"}, indent=2))


if __name__ == "__main__":
    main()
