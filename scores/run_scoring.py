"""A2 Part 4 - Score the code (Camilo).

Scores the 34 original programs and every refactored version on three dimensions:

  complexity / size  radon, through Cris's scripts/cleanup_metrics.py, so the
                     numbers are produced exactly like the baseline in
                     data/subjects_meta.csv
  code smells        PyExamine (Shivashankar and Martini, MSR 2025), the same
                     tool the ASE paper used for the `smells` column
  running time       Yujie's tests/run_tests.py on the hidden suite

Running time is re-measured here instead of read from each hidden.json, because
those files were produced on different machines: the same 123 hidden tests of
p001 take 1.2 s on one machine and 5.1 s on another. Comparing across them would
measure the hardware, not the refactoring. Pass --no-timing to skip this and
leave the time columns empty.

Interface rules followed (Shared Interfaces, Part 3):
  - score the original (code_path in programs.csv) and every final_code
  - skip runs whose final_code is null
  - a time is only comparable when the version passes every hidden test

Needs Python >=3.10 for PyExamine. Setup:
    uv venv --python 3.12 .venv
    uv pip install --python .venv/bin/python radon \\
        "code-quality-analyzer @ git+https://github.com/KarthikShivasankar/python_smells_detector@fd6d9f971c8eb577a5686da0e0c283e81edc0695"
    .venv/bin/python scores/run_scoring.py
"""
import argparse
import csv
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from cleanup_metrics import metrics                                  # noqa: E402
from code_quality_analyzer.code_smell_detector import CodeSmellDetector  # noqa: E402
from code_quality_analyzer.config_handler import ConfigHandler       # noqa: E402
from tests.run_tests import run_tests                                # noqa: E402

logging.getLogger("code_quality_analyzer").setLevel(logging.WARNING)

FIELDS = [
    "program_id", "source_model", "model", "condition", "rounds", "stop_reason",
    "sloc", "n_functions", "max_cc", "module_cc", "max_nesting", "longest_block",
    "n_smells", "smells",
    "hidden_passed", "hidden_failed", "hidden_total", "all_hidden_passed",
    "time_seconds", "time_source",
]


def smell_detector(config_path: Path):
    thresholds = ConfigHandler(str(config_path)).get_thresholds("code_smells")

    def detect(file_path: Path) -> list[str]:
        detector = CodeSmellDetector(thresholds)
        detector.detect_smells(str(file_path))
        return sorted(s.name for s in detector.code_smells)

    return detect


def score(code_path: Path, tests_path: Path, detect, timing: bool) -> dict:
    row = metrics(code_path.read_text(encoding="utf-8"))
    names = detect(code_path)
    row["n_smells"] = len(names)
    row["smells"] = ";".join(names)

    if timing:
        result = run_tests(str(code_path), str(tests_path), suite="hidden")
        passed_all = result["failed"] == 0
        row.update(
            hidden_passed=result["passed"],
            hidden_failed=result["failed"],
            hidden_total=result["total"],
            all_hidden_passed=passed_all,
            # a crash or a timeout makes the time meaningless
            time_seconds=round(result["time_seconds"], 3) if passed_all else "",
            time_source="local",
        )
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path,
                        default=ROOT / "scores" / "code_quality_config.yaml",
                        help="PyExamine threshold file")
    parser.add_argument("--no-timing", action="store_true",
                        help="skip re-running the hidden tests")
    parser.add_argument("--limit", type=int, help="only the first N programs (smoke test)")
    args = parser.parse_args()

    detect = smell_detector(args.config)
    timing = not args.no_timing

    programs = list(csv.DictReader((ROOT / "data" / "programs.csv").open(encoding="utf-8")))
    if args.limit:
        programs = programs[:args.limit]

    rows, skipped = [], []
    for prog in programs:
        pid = prog["program_id"]
        tests_path = ROOT / prog["tests_path"]

        base = {"program_id": pid, "source_model": prog["source_model"],
                "model": "original", "condition": "original",
                "rounds": "", "stop_reason": ""}
        rows.append({**base, **score(ROOT / prog["code_path"], tests_path, detect, timing)})
        print(f"{pid} original", flush=True)

        for summary_path in sorted((ROOT / "outputs" / pid).glob("*/*/summary.json")):
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            final_code = summary.get("final_code")
            if not final_code:
                skipped.append({"program_id": pid, "model": summary.get("model"),
                                "condition": summary.get("condition"),
                                "stop_reason": summary.get("stop_reason")})
                continue
            base = {"program_id": pid, "source_model": prog["source_model"],
                    "model": summary.get("model"), "condition": summary.get("condition"),
                    "rounds": summary.get("rounds", ""),
                    "stop_reason": summary.get("stop_reason", "")}
            rows.append({**base, **score(summary_path.parent / final_code,
                                         tests_path, detect, timing)})
            print(f"{pid} {summary.get('model')} {summary.get('condition')}", flush=True)

    out_dir = ROOT / "scores"
    with (out_dir / "scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})

    (out_dir / "skipped.json").write_text(json.dumps(skipped, indent=2), encoding="utf-8")
    print(f"\n{len(rows)} rows -> scores/scores.csv ({len(skipped)} runs skipped, no final_code)")


if __name__ == "__main__":
    main()
