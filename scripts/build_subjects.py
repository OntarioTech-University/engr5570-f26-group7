"""
Build the Group 7 study subjects (A2, Part 1 of the Shared Interfaces).

Inputs (downloaded by hand, see data/README.md):
  --ase   folder "replication_package/experiment1" from Zenodo 10.5281/zenodo.19245562
  --cc    CodeContests parquet shard train-00000-of-00039 (HF deepmind/code_contests,
          revision 802411c3010cb00d1b05bad57ca77365a3c699d6)

Stages (each one is cached in build/ so it can be re-run cheaply):
  1. problems   rebuild the ASE sample: first 30 problems per difficulty bin, same as
                get_sample.py + experiment_*.py, and check every description matches
  2. pool       every program of the 5 paper models x 2 prompt conditions, with its
                problem, source model and PyExamine smells from the ASE data
  3. screen     drop non-Python / empty / duplicates, then run ALL tests on each original
  4. metrics    radon cyclomatic complexity for the "something to clean up" rule
  5. select     seeded, stratified choice of N programs, then write data/

Usage:
  python scripts/build_subjects.py --ase <dir> --cc <parquet> [--n 40] [--seed 5570] [--jobs 8]
"""
import argparse
import ast
import csv
import glob
import hashlib
import json
import os
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
try:                                   # Yujie's official runner, when it exists
    from run_tests import run_tests    # noqa: F401
    RUNNER = "run_tests.py (Yujie)"
except Exception:
    from check_runner import run_tests
    RUNNER = "scripts/check_runner.py (Part 2 stand-in)"

BINS = ["easy", "middle", "hard"]
# The five models analysed in the ASE paper (folder name -> label used in programs.csv)
PAPER_MODELS = {
    "gemini25p": "gemini-2.5-pro",
    "llama33_70b": "llama-3.3-70b",
    "deepseek_coder": "deepseek-coder-v2-16b",
    "qwen_coder_30b": "qwen3-coder-30b",
    "qwen_480b": "qwen3-coder-480b",
}
# ASE folder names for the two prompt conditions in the paper
CONDITIONS = {"raw": "zero-shot", "np": "few-shot"}
# PyExamine smells we do NOT count as "something to clean up":
#   Orphan Module / High Fan-in: whole-folder import facts, not about one program
#   Feature Envy / Potential Shotgun Surgery: the ASE paper calls them false positives here
IGNORED_SMELLS = {"Orphan Module", "High Fan-in", "Feature Envy", "Potential Shotgun Surgery"}
# "Something to clean up" = at least one of these (fixed before any refactoring run):
CC_THRESHOLD = 11          # a block with cyclomatic complexity > 10 (McCabe's limit, radon rank C+)
NEST_THRESHOLD = 4         # control statements nested 4 deep or more
LONG_BLOCK_THRESHOLD = 20  # a function, or the module-level script, with 20+ lines of code
MAX_TEST_SECONDS = 1.0     # slowest single test must stay 5x under the 5 s timeout
LANG_TAG = re.compile(r"^\s*(python3?|py)\s*\n", re.I)


def difficulty(r):
    return "easy" if 0 <= r <= 1199 else ("middle" if r <= 2199 else "hard")


# ---------------------------------------------------------------- stage 1
def _model_outputs(ase):
    """Yield (folder, cond, path to *_output.json) for the paper models."""
    for folder in PAPER_MODELS:
        for cond in CONDITIONS:
            js = glob.glob(f"{ase}/result/{folder}/{cond}/*_output.json")
            yield folder, cond, (js[0] if js else None)


def stage_problems(cc_paths, ase, build):
    """Find every problem the ASE models solved in CodeContests, by exact description.
    The ASE JSON files store the full problem text next to each program, so this
    mapping does not depend on the order of the sample."""
    import pyarrow.parquet as pq
    wanted = set()
    for _, _, js in _model_outputs(ase):
        if js:
            sol = json.load(open(js, encoding="utf-8"))["solutions"]
            wanted |= {s["description"] for b in BINS for s in sol[b]}
    cols = ["name", "description", "public_tests", "private_tests", "generated_tests",
            "source", "cf_contest_id", "cf_index", "cf_rating", "time_limit"]
    src = {1: "CodeChef", 2: "Codeforces", 3: "HackerEarth"}
    probs = {}
    for path in cc_paths:
        for r in pq.read_table(path, columns=cols).to_pylist():
            d = r["description"]
            if d not in wanted or d in probs:
                continue
            pid = (f"{r['cf_contest_id']}_{r['cf_index']}" if r["cf_contest_id"]
                   else re.sub(r"\W+", "_", r["name"].split(".")[0].strip()))
            tl = r["time_limit"]
            probs[d] = {
                "problem_id": pid, "name": r["name"], "difficulty": difficulty(r["cf_rating"]),
                "cf_rating": r["cf_rating"], "platform": src.get(r["source"], str(r["source"])),
                "time_limit_s": round(tl["seconds"] + tl["nanos"] / 1e9, 3) if tl else None,
                "tests": {k: [{"input": a, "output": o} for a, o in
                              zip(r[k + "_tests"]["input"], r[k + "_tests"]["output"])]
                          for k in ["public", "private", "generated"]},
            }
    missing = wanted - set(probs)
    if missing:
        sys.exit(f"{len(missing)} problems not found; add more CodeContests shards with --cc")
    ids = [p["problem_id"] for p in probs.values()]
    assert len(ids) == len(set(ids)), "problem_id collision"
    json.dump(list(probs.values()), open(f"{build}/problems.json", "w", encoding="utf-8"))
    return probs


# ---------------------------------------------------------------- stage 2
def _norm(s):
    return re.sub(r"\s+", "", s)


def stage_pool(ase, probs, build):
    pool, notes = [], Counter()
    for folder, cond, js in _model_outputs(ase):
        label, cond_name = PAPER_MODELS[folder], CONDITIONS[cond]
        base = f"{ase}/result/{folder}/{cond}"
        if not js:
            n = len(glob.glob(f"{base}/solution/snippets/*.py"))
            notes[f"{folder}/{cond}: no JSON in the package, {n} snippet files cannot be "
                  f"matched to problems, skipped"] += 1
            continue
        sol = json.load(open(js, encoding="utf-8"))["solutions"]
        snippets = {}
        for p in glob.glob(f"{base}/solution/snippets/solution_*.py"):
            k = int(re.findall(r"solution_(\d+)\.py", p)[0])
            snippets[k] = _norm(open(p, encoding="utf-8").read())
        smells_by_snip = defaultdict(list)
        rep = f"{base}/code_quality_report.csv"
        if os.path.exists(rep):
            for row in csv.DictReader(open(rep, encoding="utf-8")):
                m = re.search(r"solution_(\d+)\.py", row.get("File") or "")
                if m:
                    smells_by_snip[int(m.group(1))].append(row["Name"])
        else:
            notes[f"{folder}/{cond}: no PyExamine report in the package"] += 1
        for b in BINS:
            for i, s in enumerate(sol[b]):
                prob = probs[s["description"]]
                code = LANG_TAG.sub("", s["solution"].strip("\n"), count=1).strip("\n") + "\n"
                c = _norm(code)
                snip = [k for k, v in snippets.items() if c.strip() and v == c]
                smells = sorted(set(sm for k in snip for sm in smells_by_snip[k]))
                pool.append({
                    "key": f"{folder}/{cond}/{b}{i:02d}", "problem_id": prob["problem_id"],
                    "difficulty": prob["difficulty"], "source_model": label, "ase_folder": folder,
                    "ase_cond": cond, "condition": cond_name, "code": code, "ase_smells": smells,
                    "ase_snippet": snip[0] if snip else None,
                    "ase_reported_fail": s.get("fail"),
                })
    json.dump(pool, open(f"{build}/pool.json", "w", encoding="utf-8"))
    return pool, notes


# ---------------------------------------------------------------- stage 3
def _screen_one(args):
    key, code_path, tests_path = args
    r = run_tests(code_path, tests_path, suite="all", stop_at_first_failure=True)
    return key, r


def stage_screen(pool, probs, build, jobs):
    tdir, cdir = f"{build}/tests", f"{build}/code"
    os.makedirs(tdir, exist_ok=True)
    os.makedirs(cdir, exist_ok=True)
    for p in probs.values():
        json.dump(p["tests"], open(f"{tdir}/{p['problem_id']}.json", "w", encoding="utf-8"))
    tests_of = {p["problem_id"]: p["tests"] for p in probs.values()}
    seen, todo = {}, []
    for e in pool:
        code = e["code"]
        if not code.strip():
            e["status"] = "empty"
            continue
        try:
            ast.parse(code)
        except SyntaxError:
            e["status"] = "not_python"
            continue
        t = tests_of[e["problem_id"]]
        if not t["public"] or not (t["private"] or t["generated"]):
            e["status"] = "no_public_or_hidden_tests"
            continue
        if not re.search(r"\binput\s*\(|sys\.stdin|open\s*\(\s*0", code):
            e["status"] = "no_stdin"
            continue
        h = (e["problem_id"], e["source_model"], hashlib.sha1(_norm(code).encode()).hexdigest())
        if h in seen:
            e["status"] = "duplicate"
            e["duplicate_of"] = seen[h]
            continue
        seen[h] = e["key"]
        path = f"{cdir}/{e['key'].replace('/', '__')}.py"
        open(path, "w", encoding="utf-8", newline="\n").write(code)
        e["code_file"] = path
        todo.append((e["key"], path, f"{tdir}/{e['problem_id']}.json"))
    by_key = {e["key"]: e for e in pool}
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        for n, (key, r) in enumerate(ex.map(_screen_one, todo, chunksize=1), 1):
            e = by_key[key]
            e["status"] = "pass_all" if r["failed"] == 0 else "fails_tests"
            if r["failures"]:
                f = r["failures"][0]
                e["first_failure"] = {"test_index": f["test_index"],
                                      "kind": "timeout" if f["error"] == "timeout"
                                      else ("crash" if f["error"] else "wrong_answer")}
            if n % 50 == 0:
                print(f"  screened {n}/{len(todo)}", flush=True)
    json.dump(pool, open(f"{build}/screened.json", "w", encoding="utf-8"))
    return pool


# ---------------------------------------------------------------- stage 4
def stage_metrics(pool):
    from cleanup_metrics import metrics
    for e in pool:
        if e.get("status") != "pass_all":
            continue
        e.update(metrics(e["code"]))
        real = [s for s in e["ase_smells"] if s not in IGNORED_SMELLS]
        reasons = []
        if real:
            reasons.append("smell:" + "+".join(real))
        if e["max_cc"] >= CC_THRESHOLD:
            reasons.append(f"cc={e['max_cc']}")
        if e["max_nesting"] >= NEST_THRESHOLD:
            reasons.append(f"nesting={e['max_nesting']}")
        if e["longest_block"] >= LONG_BLOCK_THRESHOLD:
            reasons.append(f"block_lines={e['longest_block']}")
        e["cleanup_reasons"] = reasons
    return pool


def _slowest_test(args):
    import subprocess
    import time
    code_path, tests_path = args
    t = json.load(open(tests_path, encoding="utf-8"))
    worst = 0.0
    for c in t["public"] + t["private"] + t["generated"]:
        s = time.perf_counter()
        subprocess.run([sys.executable, code_path], input=c["input"].encode("utf-8"),
                       capture_output=True, timeout=30)
        worst = max(worst, time.perf_counter() - s)
    return round(worst, 3)


def stage_timing(pool, build, jobs):
    """Slowest single test of each eligible program. We keep a 5x margin below the
    5-second timeout of Part 2, so a refactored version on a slower laptop is not
    failed by the clock."""
    todo = [e for e in pool if e.get("status") == "pass_all" and e.get("cleanup_reasons")]
    args = [(e["code_file"], f"{build}/tests/{e['problem_id']}.json") for e in todo]
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        for e, w in zip(todo, ex.map(_slowest_test, args)):
            e["slowest_test_s"] = w
            if w > MAX_TEST_SECONDS:
                e["cleanup_reasons"] = []
                e["status"] = "too_slow"
    return pool


# ---------------------------------------------------------------- stage 5
def stage_select(pool, n, seed):
    rng = random.Random(seed)
    ok = [e for e in pool if e.get("status") == "pass_all" and e.get("cleanup_reasons")]
    # one program per (problem, source model): if both prompt conditions qualify, pick one
    by_pm = defaultdict(list)
    for e in ok:
        by_pm[(e["problem_id"], e["source_model"])].append(e)
    cands = [rng.choice(sorted(v, key=lambda x: x["key"])) for _, v in sorted(by_pm.items())]
    # round-robin over source models so no model dominates; at most 2 programs per problem
    per_model = defaultdict(list)
    for e in cands:
        per_model[e["source_model"]].append(e)
    for m in per_model:
        rng.shuffle(per_model[m])
        # prefer smell-backed programs first, then spread over difficulties
        per_model[m].sort(key=lambda e: (not any(r.startswith("smell") for r in e["cleanup_reasons"])))
    chosen, per_problem = [], Counter()
    models = sorted(per_model, key=lambda m: len(per_model[m]))
    while len(chosen) < n and any(per_model.values()):
        for m in models:
            while per_model[m]:
                e = per_model[m].pop(0)
                if per_problem[e["problem_id"]] < 2:
                    chosen.append(e)
                    per_problem[e["problem_id"]] += 1
                    break
            if len(chosen) >= n:
                break
    order = {b: i for i, b in enumerate(BINS)}
    chosen.sort(key=lambda e: (order[e["difficulty"]], e["problem_id"], e["source_model"]))
    return chosen, cands


def write_data(chosen, probs, out_root):
    data = f"{out_root}/data"
    for d in ["programs", "tests"]:
        shutil.rmtree(f"{data}/{d}", ignore_errors=True)
        os.makedirs(f"{data}/{d}")
    pmap = {p["problem_id"]: p for p in probs.values()}
    rows, meta = [], []
    for i, e in enumerate(chosen, 1):
        pid = f"p{i:03d}"
        code_path, tests_path = f"data/programs/{pid}.py", f"data/tests/{pid}.json"
        open(f"{out_root}/{code_path}", "w", encoding="utf-8", newline="\n").write(e["code"])
        t = pmap[e["problem_id"]]["tests"]
        # a hidden test must never repeat a public one, or the model has already seen it
        pub = {c["input"].strip() for c in t["public"]}
        hidden = {k: [c for c in t[k] if c["input"].strip() not in pub] for k in ("private", "generated")}
        e["removed_hidden_dupes"] = sum(len(t[k]) - len(hidden[k]) for k in hidden)
        t = {"public": t["public"], **hidden}
        json.dump({"public": t["public"], "private": t["private"], "generated": t["generated"]},
                  open(f"{out_root}/{tests_path}", "w", encoding="utf-8", newline="\n"),
                  ensure_ascii=False, indent=1)
        rows.append({"program_id": pid, "problem_id": e["problem_id"],
                     "source_model": e["source_model"], "code_path": code_path,
                     "tests_path": tests_path, "smells": ";".join(e["ase_smells"])})
        p = pmap[e["problem_id"]]
        meta.append({"program_id": pid, "problem_name": p["name"], "platform": p["platform"],
                     "difficulty": e["difficulty"], "cf_rating": p["cf_rating"],
                     "time_limit_s": p["time_limit_s"], "prompt_condition": e["condition"],
                     "ase_file": f"result/{e['ase_folder']}/{e['ase_cond']}/solution/snippets/solution_{e['ase_snippet']}.py" if e["ase_snippet"] is not None else "",
                     "n_public": len(t["public"]), "n_private": len(t["private"]),
                     "n_generated": len(t["generated"]), "sloc": e["sloc"],
                     "n_functions": e["n_functions"], "max_cc": e["max_cc"],
                     "max_nesting": e["max_nesting"], "longest_block": e["longest_block"],
                     "slowest_test_s": e["slowest_test_s"],
                     "cleanup_reasons": ";".join(e["cleanup_reasons"])})
    with open(f"{data}/programs.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(f"{data}/subjects_meta.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(meta[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(meta)


def write_stats(pool, cands, chosen, notes, out_root):
    S = {"runner": RUNNER, "notes": dict(notes)}
    S["pool_total"] = len(pool)
    S["pool_by_status"] = dict(Counter(e.get("status", "?") for e in pool))
    S["status_by_model"] = {m: dict(Counter(e.get("status") for e in pool if e["source_model"] == m))
                            for m in PAPER_MODELS.values()}
    S["status_by_condition"] = {c: dict(Counter(e.get("status") for e in pool if e["condition"] == c))
                                for c in CONDITIONS.values()}
    S["pass_all_by_difficulty"] = dict(Counter(e["difficulty"] for e in pool if e.get("status") == "pass_all"))
    S["fail_kind"] = dict(Counter(e["first_failure"]["kind"] for e in pool if e.get("first_failure")))
    ase_ok = [e for e in pool if e["ase_reported_fail"] == 0 and e.get("status") in ("fails_tests", "not_python", "empty", "no_stdin")]
    S["ase_marked_pass_but_not_usable"] = len(ase_ok)
    passing = [e for e in pool if e.get("status") == "pass_all"]
    S["passing_with_cleanup_reason"] = sum(1 for e in passing if e.get("cleanup_reasons"))
    S["passing_problem_model_pairs"] = len({(e["problem_id"], e["source_model"]) for e in passing})
    S["eligible_problem_model_pairs"] = len(cands)
    S["eligible_by_model"] = dict(Counter(e["source_model"] for e in cands))
    S["distinct_problems"] = len({e["problem_id"] for e in pool})
    folders = defaultdict(set)
    for e in pool:
        folders[e["source_model"]].add(e["problem_id"])
    S["problems_per_model"] = {m: len(v) for m, v in folders.items()}
    S["selected"] = len(chosen)
    S["selected_by_model"] = dict(Counter(e["source_model"] for e in chosen))
    S["selected_by_difficulty"] = dict(Counter(e["difficulty"] for e in chosen))
    S["selected_by_condition"] = dict(Counter(e["condition"] for e in chosen))
    S["selected_distinct_problems"] = len({e["problem_id"] for e in chosen})
    S["selected_reason_counts"] = dict(Counter(r.split(":")[0].split("=")[0] for e in chosen for r in e["cleanup_reasons"]))
    S["hidden_tests_removed_as_copies_of_public"] = sum(e.get("removed_hidden_dupes", 0) for e in chosen)
    S["selected_smells"] = dict(Counter(s for e in chosen for s in e["ase_smells"]))
    json.dump(S, open(f"{out_root}/data/dataset_stats.json", "w", encoding="utf-8"), indent=2)
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ase", required=True)
    ap.add_argument("--cc", required=True, nargs="+")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=5570)
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    ap.add_argument("--build", default=os.path.join(ROOT, "build"))
    ap.add_argument("--rescreen", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.build, exist_ok=True)
    print("runner:", RUNNER)
    probs = stage_problems(a.cc, a.ase, a.build)
    print(f"stage 1: {len(probs)} distinct problems found in CodeContests by exact description")
    pool, notes = stage_pool(a.ase, probs, a.build)
    print(f"stage 2: {len(pool)} programs in the pool", dict(notes))
    cache = f"{a.build}/screened.json"
    if os.path.exists(cache) and not a.rescreen:
        pool = json.load(open(cache, encoding="utf-8"))
        print("stage 3: loaded cached screening")
    else:
        pool = stage_screen(pool, probs, a.build, a.jobs)
    print("stage 3:", dict(Counter(e.get("status") for e in pool)))
    pool = stage_metrics(pool)
    pool = stage_timing(pool, a.build, a.jobs)
    chosen, cands = stage_select(pool, a.n, a.seed)
    write_data(chosen, probs, ROOT)
    picked = {e["key"] for e in chosen}
    with open(f"{ROOT}/data/reserves.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ase_key", "problem_id", "source_model", "prompt_condition", "cleanup_reasons"])
        for e in sorted(cands, key=lambda x: x["key"]):
            if e["key"] not in picked:
                w.writerow([e["key"], e["problem_id"], e["source_model"], e["condition"],
                            ";".join(e["cleanup_reasons"])])
    S = write_stats(pool, cands, chosen, notes, ROOT)
    print(json.dumps(S, indent=2))


if __name__ == "__main__":
    main()
