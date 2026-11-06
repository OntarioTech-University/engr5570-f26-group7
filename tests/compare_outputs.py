"""ENGR 5570 Group 7 A3: differential testing on Cris's new inputs.

Run from the repository root (no third-party dependencies):
    python -m tests.compare_outputs --program p003 --model gpt
    python -m tests.compare_outputs --out outputs --results difftest
    python -m tests.compare_outputs --out outputs_pilot_hard --results difftest_pilot_hard

Writes only into --results, never into an experiment's outputs folder.
Raw output differences are NOT necessarily incorrect answers for multi-answer problems.
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from tests.run_tests import _as_text, _last_error_lines, _normalize_output

MODELS = ("gpt", "qwen", "deepseek")
CONDITIONS = ("single", "loop")


def _run_program(script: Path, input_text: str, timeout: float, env: dict) -> tuple[str, str]:
    """Return (stdout, error). An empty error denotes successful execution."""
    try:
        completed = subprocess.run(
            [sys.executable, "-B", str(script)],
            input=input_text,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            check=False,
        )
        error = (
            _last_error_lines(completed.stderr, completed.returncode)
            if completed.returncode != 0 else ""
        )
        return completed.stdout, error
    except subprocess.TimeoutExpired as exc:
        return _as_text(exc.stdout), "timeout"


def compare_outputs(original_path: str, refactored_path: str,
                    inputs_path: str, timeout: float = 5.0) -> dict:
    """Compare the same NEW inputs on original and refactored Python programs.

    Schema mandated by A3 Part 4.2. Each input is run in a fresh subprocess.
    The original must succeed on every input (Cris's input-data precondition).
    When the original fails, raise instead of falsely attributing a bug to the
    refactored program; the batch runner logs the failure and continues.
    """
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")

    original = Path(original_path).resolve()
    refactored = Path(refactored_path).resolve()
    inputs_file = Path(inputs_path).resolve()
    if not original.is_file() or not refactored.is_file():
        raise FileNotFoundError(f"Missing original or refactored file: {original}, {refactored}")
    with inputs_file.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict) or not isinstance(data.get("inputs"), list):
        raise ValueError("Input JSON must be an object containing an 'inputs' array")
    if not all(isinstance(item, str) for item in data["inputs"]):
        raise ValueError("All inputs must be strings")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    total = len(data["inputs"])
    same = 0
    different = 0
    differences = []
    start = time.perf_counter()

    for index, input_text in enumerate(data["inputs"]):
        original_output, original_error = _run_program(original, input_text, timeout, env)
        if original_error:
            raise RuntimeError(
                f"Original failed on input {index} of {inputs_file.name}: {original_error}"
            )

        refactored_output, refactored_error = _run_program(refactored, input_text, timeout, env)
        matched = (
            not refactored_error
            and _normalize_output(original_output) == _normalize_output(refactored_output)
        )
        if matched:
            same += 1
        else:
            different += 1
            if len(differences) < 5:
                differences.append({
                    "input_index": index,
                    "input": input_text[:500],
                    "original_output": original_output[:500],
                    "refactored_output": refactored_output[:500],
                    "error": refactored_error[:500],
                })

    return {
        "total": total,
        "same": same,
        "different": different,
        "differences": differences,
        "time_seconds": round(time.perf_counter() - start, 3),
    }


def batch_compare(repo: Path, out_name: str = "outputs", results_name: str = "difftest",
                  program: str | None = None, model: str | None = None,
                  condition: str | None = None, timeout: float = 5.0,
                  skip_existing: bool = False) -> int:
    """Run A3 comparisons and save one JSON per program/model/condition."""
    repo = repo.resolve()
    out_root = (repo / out_name).resolve()
    results_root = (repo / results_name).resolve()
    if not out_root.is_dir():
        raise FileNotFoundError(f"Experiment folder does not exist: {out_root}")
    if out_root == results_root or out_root in results_root.parents or results_root in out_root.parents:
        raise ValueError("--results must be separate from --out to protect experiment files")

    with (repo / "data" / "programs.csv").open(newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    counts = {"checked": 0, "same": 0, "different": 0, "versions_with_differences": 0,
              "skipped": 0, "already_done": 0, "errors": 0}

    for row in rows:
        pid = row["program_id"]
        if program and program != pid:
            continue
        original = (repo / row["code_path"]).resolve()
        inputs = repo / "data" / "new_inputs" / f"{pid}.json"
        for model_name in MODELS:
            if model and model_name != model:
                continue
            for condition_name in CONDITIONS:
                if condition and condition_name != condition:
                    continue
                name = f"{pid}/{model_name}/{condition_name}"
                run_dir = out_root / pid / model_name / condition_name
                summary_file = run_dir / "summary.json"
                if not summary_file.is_file():
                    counts["skipped"] += 1
                    continue
                output_path = results_root / pid / model_name / f"{condition_name}.json"
                if skip_existing and output_path.is_file():
                    counts["already_done"] += 1
                    print(f"SKIP   {name}: result already exists", flush=True)
                    continue

                try:
                    summary = json.loads(summary_file.read_text(encoding="utf-8"))
                    relative_code = summary.get("final_code")
                    if not isinstance(relative_code, str) or not relative_code:
                        raise ValueError("summary.json has no valid final_code")
                    refactored = (run_dir / relative_code).resolve()
                    if not refactored.is_relative_to(run_dir.resolve()) or not refactored.is_file():
                        raise ValueError(f"final_code missing/outside run directory: {relative_code}")
                    input_data = json.loads(inputs.read_text(encoding="utf-8"))
                    if input_data.get("program_id") != pid:
                        raise ValueError(f"Input program ID mismatch for {pid}")
                    result = compare_outputs(str(original), str(refactored), str(inputs), timeout)
                    record = {
                        **result,
                        "program_id": pid,
                        "model": model_name,
                        "condition": condition_name,
                        "refactored_path": str(refactored.relative_to(repo)).replace(os.sep, "/"),
                    }
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    tmp_path = output_path.with_suffix(".json.tmp")
                    tmp_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
                    tmp_path.replace(output_path)
                    counts["checked"] += 1
                    counts["same"] += result["same"]
                    counts["different"] += result["different"]
                    counts["versions_with_differences"] += (result["different"] > 0)
                    print(f"DONE   {name}: {result['same']}/{result['total']} same; "
                          f"{result['different']} different; {result['time_seconds']}s", flush=True)
                except (OSError, ValueError, KeyError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
                    counts["errors"] += 1
                    print(f"ERROR  {name}: {exc}", file=sys.stderr, flush=True)

    print("\nSUMMARY: " + ", ".join(f"{key}={value}" for key, value in counts.items()))
    if counts["checked"] == 0 and counts["already_done"] == 0:
        print("No results were processed. Check --out, --program, --model, and --condition.")
        return 1
    return 1 if counts["errors"] else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="outputs", help="Experiment directory, e.g. outputs")
    parser.add_argument("--results", default="difftest", help="Separate directory for A3 JSON reports")
    parser.add_argument("--program", help="Only one program, e.g. p003")
    parser.add_argument("--model", choices=MODELS, help="Only one model")
    parser.add_argument("--condition", choices=CONDITIONS, help="Only one condition")
    parser.add_argument("--timeout", type=float, default=5.0, help="Seconds per execution")
    parser.add_argument("--skip-existing", action="store_true", help="Resume without rewriting existing JSON")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    try:
        status = batch_compare(repo, args.out, args.results, args.program,
                               args.model, args.condition, args.timeout, args.skip_existing)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    raise SystemExit(status)


if __name__ == "__main__":
    main()
