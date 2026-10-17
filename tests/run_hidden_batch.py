"""Independently verify final refactored programs with the locked hidden suite.

Run from the repository root:
    python -m tests.run_hidden_batch --out outputs --program p001 --model qwen --condition single
    python -m tests.run_hidden_batch --out outputs
    python -m tests.run_hidden_batch --out outputs --write

DEFAULT: read-only. Existing hidden.json is compared (ignoring time_seconds),
never overwritten. --write creates MISSING hidden.json files; it does not
modify existing files. Hidden cases/results must never be sent back to a model.
"""

import argparse
import csv
import json
from pathlib import Path

from tests.run_tests import run_tests

MODELS = ("qwen", "deepseek", "gpt")
CONDITIONS = ("single", "loop")
COMPARE_FIELDS = ("suite", "passed", "failed", "total", "failures")


def verify_results(repo: Path, out_name: str, program_filter, model_filter,
                   condition_filter, write_missing: bool):
    csv_path = repo / "data" / "programs.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(f"Missing Cris dataset: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    out_root = (repo / out_name).resolve()
    if not out_root.is_dir():
        raise FileNotFoundError(f"Missing Fangyu output folder: {out_root}")

    counts = {"checked": 0, "matching": 0, "mismatching": 0,
              "missing_hidden": 0, "written": 0, "skipped": 0, "errors": 0}
    for row in rows:
        pid = row["program_id"]
        if program_filter and pid != program_filter:
            continue
        tests_path = (repo / row["tests_path"]).resolve()
        for model in MODELS:
            if model_filter and model != model_filter:
                continue
            for condition in CONDITIONS:
                if condition_filter and condition != condition_filter:
                    continue
                run_dir = out_root / pid / model / condition
                summary_file = run_dir / "summary.json"
                if not summary_file.is_file():
                    counts["skipped"] += 1
                    continue
                name = f"{pid}/{model}/{condition}"
                try:
                    summary = json.loads(summary_file.read_text(encoding="utf-8"))
                    final_code = summary.get("final_code")
                    if final_code is None:
                        print(f"SKIP {name}: final_code is null")
                        counts["skipped"] += 1
                        continue
                    if not isinstance(final_code, str) or not final_code:
                        raise ValueError("final_code is not a valid path")
                    # Accept only final code paths inside this experiment folder.
                    code_file = (run_dir / final_code).resolve()
                    if not code_file.is_relative_to(run_dir.resolve()) or not code_file.is_file():
                        raise ValueError(f"Invalid/missing final code: {final_code}")
                    if not tests_path.is_file():
                        raise FileNotFoundError(tests_path)
                    result = run_tests(str(code_file), str(tests_path), suite="hidden")
                    counts["checked"] += 1
                    hidden_path = run_dir / "hidden.json"
                    status = f"{result['passed']}/{result['total']} passed"
                    if hidden_path.exists():
                        old = json.loads(hidden_path.read_text(encoding="utf-8"))
                        differs = [k for k in COMPARE_FIELDS if old.get(k) != result[k]]
                        if differs:
                            counts["mismatching"] += 1
                            print(f"MISMATCH {name}: {status}; differs in {', '.join(differs)}")
                        else:
                            counts["matching"] += 1
                            print(f"MATCH    {name}: {status} (time may differ)")
                    elif write_missing:
                        hidden_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")
                        counts["written"] += 1
                        print(f"WROTE    {name}: {status} -> hidden.json")
                    else:
                        counts["missing_hidden"] += 1
                        print(f"NO FILE  {name}: {status}; use --write after group approval")
                except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                    counts["errors"] += 1
                    print(f"ERROR    {name}: {exc}")

    print("\nSUMMARY:", ", ".join(f"{k}={v}" for k, v in counts.items()))
    if not counts["checked"]:
        print("No eligible final_code was checked. Check --out / --program / model / condition.")
    return 0 if counts["checked"] > 0 and counts["mismatching"] == 0 and counts["errors"] == 0 else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="outputs", help="Folder containing Fangyu's experiment results")
    parser.add_argument("--program", help="Only check one program ID, e.g. p001")
    parser.add_argument("--model", choices=MODELS, help="Only check one model")
    parser.add_argument("--condition", choices=CONDITIONS, help="Only check single or loop")
    parser.add_argument("--write", action="store_true", help="Write hidden.json only when missing, never overwrite")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    raise SystemExit(verify_results(repo, args.out, args.program, args.model,
                                    args.condition, args.write))


if __name__ == "__main__":
    main()
