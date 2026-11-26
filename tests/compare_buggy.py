"""Group 7 A4: test strength on injected bugs (raw output comparison)."""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tests.run_tests import _normalize_output
from tests.compare_outputs import _run_program

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "bug_validation"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
MULTI_ANSWER = {"143_A", "309_B", "663_A"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def first_failure(code, cases, timeout):
    # Stop within a suite once a bug is detected.
    for index, (inp, expected) in enumerate(cases):
        actual, error = _run_program(code, inp, timeout, ENV)
        if error or _normalize_output(actual) != _normalize_output(expected):
            return {"index": index,
                    "reason": "timeout" if error == "timeout" else (
                        "runtime_error" if error else "output_difference"),
                    "error": error[:500], "expected": expected[:500],
                    "actual": actual[:500]}
    return None


def check_program(pid, original, bugs, timeout, resume):
    checkpoint = RESULTS / "programs" / f"{pid}.json"
    settings = {"timeout": timeout, "python": sys.version.split()[0],
                "method": "raw_output_v1"}
    if resume and checkpoint.exists():
        saved = read_json(checkpoint)
        if (saved["settings"] == settings and
                [r["bug_id"] for r in saved["rows"]] == [b["bug_id"] for b in bugs]):
            print(f"{pid}: reused completed results", flush=True)
            return saved["rows"]

    tests = read_json(ROOT / original["tests_path"])
    hidden = [(c["input"], c["output"]) for c in tests["private"] + tests["generated"]]
    inputs = read_json(ROOT / "data" / "new_inputs" / f"{pid}.json")["inputs"]
    if not hidden or not inputs:
        raise ValueError(f"Missing test cases for {pid}")

    # Run the original only once per input, not once per mutant.
    original_code = ROOT / original["code_path"]
    new_cases = []
    for index, inp in enumerate(inputs):
        output, error = _run_program(original_code, inp, timeout, ENV)
        if error:
            raise RuntimeError(f"Original {pid} failed on input {index}: {error}")
        new_cases.append((inp, output))

    rows = []
    for bug in bugs:
        code = ROOT / bug["code_path"]
        if not code.is_file():
            raise FileNotFoundError(code)
        h = first_failure(code, hidden, timeout)
        n = first_failure(code, new_cases, timeout)
        hidden_caught = int(h is not None)
        new_caught = int(n is not None)
        review = ("known_bug_in_original" if pid == "p012" else
                  "multiple_valid_outputs" if bug["problem_id"] in MULTI_ANSWER else "")
        rows.append({**bug, "hidden": hidden_caught, "new_inputs": new_caught,
                     "both": int(hidden_caught and new_caught),
                     "either": int(hidden_caught or new_caught),
                     "review_note": review, "hidden_witness": h, "new_witness": n})
    write_json(checkpoint, {"settings": settings, "rows": rows})
    print(f"{pid}: {sum(r['either'] for r in rows)}/{len(rows)} caught", flush=True)
    return rows


def save_results(rows, dataset_size):
    rows = sorted(rows, key=lambda r: r["bug_id"])
    flat = []
    for r in rows:
        item = {k: v for k, v in r.items() if k not in ("hidden_witness", "new_witness")}
        for key in ("hidden", "new"):
            witness = r[f"{key}_witness"]
            item[f"{key}_index"] = witness["index"] if witness else ""
            item[f"{key}_reason"] = witness["reason"] if witness else ""
        flat.append(item)
    fields = list(flat[0])
    write_csv(RESULTS / "results.csv", flat, fields)
    write_csv(RESULTS / "undetected.csv", [r for r in flat if not r["either"]], fields)
    write_csv(RESULTS / "oracle_review.csv", [r for r in flat if r["review_note"]], fields)
    total = len(rows)
    counts = {k: sum(r[k] for r in rows) for k in ("hidden", "new_inputs", "both", "either")}
    summary = {"n_bugs": total, "dataset_size": dataset_size,
               "complete": total == dataset_size, **counts,
               "missed_by_all": total - counts["either"],
               "rates_percent": {k: round(100 * v / total, 2) for k, v in counts.items()}}
    # Only use pilot results for a cross-check after the independent run.
    pilot_path = ROOT / "data" / "buggy_pilot_results.csv"
    if pilot_path.exists():
        pilot = {r["bug_id"]: r for r in read_csv(pilot_path)}
        differences = []
        for r in flat:
            old = pilot.get(r["bug_id"])
            if old and any(r[k] != int(old[k]) for k in ("hidden", "new_inputs")):
                differences.append({"bug_id": r["bug_id"], "hidden": r["hidden"],
                                    "pilot_hidden": old["hidden"], "new_inputs": r["new_inputs"],
                                    "pilot_new_inputs": old["new_inputs"]})
        write_csv(RESULTS / "pilot_differences.csv", differences,
                  ["bug_id", "hidden", "pilot_hidden", "new_inputs", "pilot_new_inputs"])
        summary["pilot_disagreements"] = len(differences)
    write_json(RESULTS / "summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", help="Run one program, e.g. p001")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--resume", action="store_true", help="Reuse completed program results")
    args = parser.parse_args()
    if args.workers < 1 or args.timeout <= 0:
        parser.error("workers and timeout must be positive")
    originals = {r["program_id"]: r for r in read_csv(ROOT / "data/programs.csv")}
    all_bugs = read_csv(ROOT / "data/buggy_programs.csv")
    if len({b["bug_id"] for b in all_bugs}) != len(all_bugs):
        raise ValueError("Duplicate bug IDs")
    groups = defaultdict(list)
    for bug in all_bugs:
        if not args.program or bug["program_id"] == args.program:
            groups[bug["program_id"]].append(bug)
    if not groups:
        parser.error("No matching buggy programs")
    (RESULTS / "programs").mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(check_program, pid, originals[pid], bugs,
                               args.timeout, args.resume) for pid, bugs in groups.items()]
        for future in as_completed(futures):
            rows.extend(future.result())
    save_results(rows, len(all_bugs))


if __name__ == "__main__":
    main()
