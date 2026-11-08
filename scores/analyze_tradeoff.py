"""A3 Part 5 - Quality trade-off (Camilo).

Why does the highest complexity go down while the code smells go up? This
script measures, for every original program and every refactored version:

  max_cc, total_cc   highest and summed cyclomatic complexity (radon, through
                     Cris's scripts/cleanup_metrics.py)
  n_functions        number of functions and methods
  smells by type     PyExamine, code-level detector

and writes scores/a3_tradeoff.csv (one row per version) and
scores/a3_tradeoff_summary.md (the tables for the report). The A2 files
(scores.csv, summary_table.md) are not touched.

The smell counts depend on the PyExamine version: A2 used 0.2.3, which flags
Python builtins such as `range` as Potential Shotgun Surgery. This script is
meant to run with 0.3.0, which fixes that. See scores/README.md for the two
environments. Run from the repository root:

    .venv-a3/bin/python scores/analyze_tradeoff.py
    .venv-a3/bin/python scores/analyze_tradeoff.py --outputs outputs_pilot_hard
"""
import argparse
import csv
import json
import logging
import statistics as st
import sys
from collections import Counter
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from cleanup_metrics import metrics                                        # noqa: E402
from code_quality_analyzer.code_smell_detector import CodeSmellDetector    # noqa: E402
from code_quality_analyzer.config_handler import ConfigHandler             # noqa: E402
from radon.complexity import cc_visit                                      # noqa: E402

logging.disable(logging.CRITICAL)

MODELS = ["gpt", "deepseek", "qwen"]
SMELL_TYPES = ["Long Method", "Long Parameter List", "Data Clumps"]


def total_cc(code: str, module_cc: int) -> int:
    blocks = [b for b in cc_visit(code) if b.letter in "FM"]
    return sum(b.complexity for b in blocks) + module_cc


def score(path: Path, thresholds: dict) -> dict:
    code = path.read_text(encoding="utf-8")
    m = metrics(code)
    detector = CodeSmellDetector(thresholds)
    detector.detect_smells(str(path))
    kinds = Counter(s.name for s in detector.code_smells)
    row = {"max_cc": m["max_cc"], "total_cc": total_cc(code, m["module_cc"]),
           "n_functions": m["n_functions"], "n_smells": sum(kinds.values())}
    for kind in SMELL_TYPES:
        row[kind] = kinds[kind]
    row["other_smells"] = row["n_smells"] - sum(kinds[k] for k in SMELL_TYPES)
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs", default="outputs",
                        help="folder with <program>/<model>/<condition>/summary.json")
    parser.add_argument("--condition", default="single",
                        help="which condition to score (the loop never ran a second round)")
    args = parser.parse_args()

    thresholds = ConfigHandler(str(ROOT / "scores" / "code_quality_config.yaml")
                               ).get_thresholds("code_smells")
    programs = list(csv.DictReader((ROOT / "data" / "programs.csv").open(encoding="utf-8")))

    rows = []
    for prog in programs:
        pid = prog["program_id"]
        runs = sorted((ROOT / args.outputs / pid).glob(f"*/{args.condition}/summary.json"))
        if not runs:
            continue
        rows.append({"program_id": pid, "model": "original", "condition": "original",
                     **score(ROOT / prog["code_path"], thresholds)})
        for summary_path in runs:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if not summary.get("final_code"):
                continue
            rows.append({"program_id": pid, "model": summary["model"],
                         "condition": summary["condition"],
                         **score(summary_path.parent / summary["final_code"], thresholds)})

    fields = ["program_id", "model", "condition", "max_cc", "total_cc", "n_functions",
              "n_smells", *SMELL_TYPES, "other_smells"]
    out_csv = ROOT / "scores" / ("a3_tradeoff.csv" if args.outputs == "outputs"
                                 else f"a3_tradeoff_{Path(args.outputs).name}.csv")
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    # Compare only the programs where every model gave usable code, so each row
    # of the tables is computed over the same programs.
    have = {m: {r["program_id"] for r in rows if r["model"] == m} for m in MODELS}
    common = set.intersection(*have.values()) if all(have.values()) else set()
    all_originals = {r["program_id"] for r in rows if r["model"] == "original"}
    rows = [r for r in rows if r["program_id"] in common]
    originals = {r["program_id"]: r for r in rows if r["model"] == "original"}
    pids = sorted(originals)
    dropped = sorted(all_originals - common)
    lines = [f"PyExamine {version('code-quality-analyzer')}, {len(pids)} programs, "
             f"outputs folder `{args.outputs}`, condition `{args.condition}`"
             + (f"; left out because a model gave no usable code: {', '.join(dropped)}"
                if dropped else ""), "",
             "| Version | Mean max CC | Mean total CC | Mean functions | "
             + " | ".join(SMELL_TYPES) + " | All smells |",
             "|---|---:|---:|---:|" + "---:|" * (len(SMELL_TYPES) + 1)]
    groups = [("original", [originals[p] for p in pids])]
    groups += [(m, [r for r in rows if r["model"] == m]) for m in MODELS]
    for name, group in groups:
        if not group:
            continue
        lines.append(
            f"| {name} | {st.mean(r['max_cc'] for r in group):.2f} "
            f"| {st.mean(r['total_cc'] for r in group):.2f} "
            f"| {st.mean(r['n_functions'] for r in group):.2f} | "
            + " | ".join(str(sum(r[k] for r in group)) for k in SMELL_TYPES)
            + f" | {sum(r['n_smells'] for r in group)} |")

    lines += ["", "Runs where the highest complexity went down and the smells went up, "
              "and runs where the total complexity went up:", "",
              "| Model | Runs | Max CC down and smells up | Total CC up |", "|---|---:|---:|---:|"]
    for m in MODELS:
        group = [r for r in rows if r["model"] == m]
        if not group:
            continue
        trade = sum(1 for r in group
                    if r["max_cc"] < originals[r["program_id"]]["max_cc"]
                    and r["n_smells"] > originals[r["program_id"]]["n_smells"])
        up = sum(1 for r in group if r["total_cc"] > originals[r["program_id"]]["total_cc"])
        lines.append(f"| {m} | {len(group)} | {trade} | {up} |")

    out_md = out_csv.with_suffix(".md").with_name(out_csv.stem + "_summary.md")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out_csv.relative_to(ROOT)}, {out_md.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
