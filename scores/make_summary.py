"""Turn scores/scores.csv into the comparison table for the A2 write-up.

Means hide how often a model helps, so each metric is also reported as the
number of programs it improved, left unchanged, or made worse against that
program's own original.

    python3 scores/make_summary.py
"""
import csv
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["gpt", "deepseek", "qwen"]
# metric -> does a smaller value mean better code?
METRICS = {"max_cc": True, "max_nesting": True, "n_smells": True, "sloc": True}


def load():
    rows = list((ROOT / "scores" / "scores.csv").open(encoding="utf-8"))
    return list(csv.DictReader(rows))


def main() -> None:
    rows = load()
    originals = {r["program_id"]: r for r in rows if r["model"] == "original"}
    by_model = defaultdict(list)
    for row in rows:
        if row["model"] != "original":
            by_model[row["model"]].append(row)

    lines = ["## Code quality before and after refactoring", ""]

    # --- averages -----------------------------------------------------------
    lines += [
        "| Version | Programs | Mean max CC | Mean nesting | Mean SLOC | "
        "Total smells | Passes all hidden tests |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    groups = [("original", list(originals.values()))] + [(m, by_model[m]) for m in MODELS]
    for name, group in groups:
        lines.append(
            f"| {name} | {len(group)} "
            f"| {st.mean(float(r['max_cc']) for r in group):.2f} "
            f"| {st.mean(float(r['max_nesting']) for r in group):.2f} "
            f"| {st.mean(float(r['sloc']) for r in group):.1f} "
            f"| {sum(int(r['n_smells']) for r in group)} "
            f"| {sum(r['all_hidden_passed'] == 'True' for r in group)}/{len(group)} |"
        )

    # --- per-program wins and losses ---------------------------------------
    lines += ["", "## Programs improved / unchanged / worse, against their own original", ""]
    lines += ["| Model | " + " | ".join(METRICS) + " |",
              "|---" * (len(METRICS) + 1) + "|"]
    for model in MODELS:
        cells = []
        for metric, lower_is_better in METRICS.items():
            better = same = worse = 0
            for row in by_model[model]:
                before = float(originals[row["program_id"]][metric])
                after = float(row[metric])
                if after == before:
                    same += 1
                elif (after < before) == lower_is_better:
                    better += 1
                else:
                    worse += 1
            cells.append(f"{better} / {same} / {worse}")
        lines.append(f"| {model} | " + " | ".join(cells) + " |")

    # --- running time -------------------------------------------------------
    lines += ["", "## Running time, same machine and same runner for every version", ""]
    lines += ["| Model | Programs timed | Median vs original | Slowest case |",
              "|---|---:|---:|---:|"]
    for model in MODELS:
        ratios = [
            float(r["time_seconds"]) / float(originals[r["program_id"]]["time_seconds"])
            for r in by_model[model]
            if r["time_seconds"] and originals[r["program_id"]]["time_seconds"]
        ]
        lines.append(f"| {model} | {len(ratios)} | {st.median(ratios):.3f}x "
                     f"| {max(ratios):.2f}x |")

    out = ROOT / "scores" / "summary_table.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\n-> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
