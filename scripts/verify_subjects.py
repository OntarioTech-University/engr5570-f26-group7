"""
Check data/ against Part 1 of the Shared Interfaces, then run every ORIGINAL
program on every test.

  python scripts/verify_subjects.py            # uses Yujie's run_tests.py if present
  python scripts/verify_subjects.py --quick    # format checks only, no test runs

Exit code 0 means every check passed. Results go to data/verification_<python>.json
"""
import argparse
import csv
import json
import os
import platform
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
try:
    from run_tests import run_tests
    RUNNER = "run_tests.py (Yujie)"
except Exception:
    from check_runner import run_tests
    RUNNER = "scripts/check_runner.py (Part 2 stand-in)"

HEADER = ["program_id", "problem_id", "source_model", "code_path", "tests_path", "smells"]


def fail(msg, errors):
    errors.append(msg)
    print("  FAIL:", msg)


def check_format(errors):
    path = os.path.join(ROOT, "data", "programs.csv")
    raw = open(path, "rb").read()
    raw.decode("utf-8")
    if raw.startswith(b"\xef\xbb\xbf"):
        fail("programs.csv has a BOM", errors)
    rows = list(csv.DictReader(open(path, encoding="utf-8", newline="")))
    with open(path, encoding="utf-8") as f:
        if next(csv.reader(f)) != HEADER:
            fail("programs.csv header differs from Part 1", errors)
    ids = [r["program_id"] for r in rows]
    if ids != [f"p{i:03d}" for i in range(1, len(rows) + 1)]:
        fail("program_id must be p001, p002, ... with no gaps", errors)
    if not 30 <= len(rows) <= 50:
        fail(f"{len(rows)} programs, plan says 30 to 50", errors)
    for r in rows:
        for col in ("code_path", "tests_path"):
            p = r[col]
            if "\\" in p or p.startswith("/"):
                fail(f"{r['program_id']} {col} must be relative with '/'", errors)
            if not os.path.isfile(os.path.join(ROOT, p)):
                fail(f"{r['program_id']} missing {p}", errors)
        if r["code_path"] != f"data/programs/{r['program_id']}.py":
            fail(f"{r['program_id']} code_path not in the agreed place", errors)
        if r["tests_path"] != f"data/tests/{r['program_id']}.json":
            fail(f"{r['program_id']} tests_path not in the agreed place", errors)
        if r["smells"] and (r["smells"] != r["smells"].strip() or ";;" in r["smells"]):
            fail(f"{r['program_id']} smells badly formatted", errors)
        t = json.load(open(os.path.join(ROOT, r["tests_path"]), encoding="utf-8"))
        if set(t) != {"public", "private", "generated"}:
            fail(f"{r['program_id']} tests keys {sorted(t)}", errors)
        for k, v in t.items():
            for c in v:
                if set(c) != {"input", "output"} or not all(isinstance(x, str) for x in c.values()):
                    fail(f"{r['program_id']} bad test entry in {k}", errors)
                    break
        if not t["public"]:
            fail(f"{r['program_id']} has no public tests", errors)
        if not (t["private"] or t["generated"]):
            fail(f"{r['program_id']} has no hidden tests", errors)
        code = open(os.path.join(ROOT, r["code_path"]), encoding="utf-8").read()
        compile(code, r["code_path"], "exec")
        if not re.search(r"\binput\s*\(|sys\.stdin|open\s*\(\s*0", code):
            fail(f"{r['program_id']} does not read standard input", errors)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--timeout", type=float, default=5.0)
    a = ap.parse_args()
    errors = []
    print(f"runner: {RUNNER} | python {platform.python_version()} | {platform.system()}")
    rows = check_format(errors)
    print(f"format: {len(rows)} programs checked, {len(errors)} problems")
    if a.quick:
        sys.exit(1 if errors else 0)
    report = []
    for r in rows:
        code, tests = os.path.join(ROOT, r["code_path"]), os.path.join(ROOT, r["tests_path"])
        res = {s: run_tests(code, tests, suite=s, timeout=a.timeout) for s in ("all", "public", "hidden")}
        ok = all(res[s]["failed"] == 0 for s in res)
        consistent = res["all"]["total"] == res["public"]["total"] + res["hidden"]["total"]
        if not consistent:
            fail(f"{r['program_id']} public + hidden != all", errors)
        if not ok:
            f = (res["all"]["failures"] or [{}])[0]
            fail(f"{r['program_id']} fails {res['all']['failed']}/{res['all']['total']} "
                 f"(first: test {f.get('test_index')}, error={f.get('error','')[:60]!r})", errors)
        report.append({"program_id": r["program_id"], "passed_all": ok,
                       "n_public": res["public"]["total"], "n_hidden": res["hidden"]["total"],
                       "time_all_s": res["all"]["time_seconds"]})
        print(f"  {r['program_id']}  {'ok ' if ok else 'BAD'}  public {res['public']['total']:>3}"
              f"  hidden {res['hidden']['total']:>3}  {res['all']['time_seconds']:6.2f}s", flush=True)
    out = os.path.join(ROOT, "data", f"verification_py{sys.version_info[0]}{sys.version_info[1]}.json")
    json.dump({"runner": RUNNER, "python": platform.python_version(), "os": platform.system(),
               "hash_seed": os.environ.get("PYTHONHASHSEED", "random"),
               "errors": errors, "programs": report}, open(out, "w", encoding="utf-8"), indent=1)
    print(f"\n{'ALL CHECKS PASSED' if not errors else str(len(errors)) + ' PROBLEMS'} -> {out}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
