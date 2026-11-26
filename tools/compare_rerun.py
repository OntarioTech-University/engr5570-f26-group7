"""ENGR 5570 Group 7 A4: compare the rerun with the A2 run.

For each program and model in the rerun folder, compare with the same
version in outputs/: hidden test results, output differences on the new
inputs, and how many lines of code changed between the two runs.

Run from the repository root after the rerun and its output comparison:
    python tools/compare_rerun.py
    python tools/compare_rerun.py --rerun outputs_rerun --rerun-diff difftest_rerun

Writes a CSV and a Markdown table into the rerun folder. No API calls.
"""

import argparse
import csv
import difflib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def code_of(run_dir):
    summary = load(run_dir / "summary.json")
    if not summary.get("final_code"):
        return None
    return (run_dir / summary["final_code"]).read_text(encoding="utf-8")


def hidden_of(run_dir):
    path = run_dir / "hidden.json"
    if not path.exists():
        return None
    h = load(path)
    return h["passed"], h["total"]


def diff_of(diff_dir, program, model):
    path = diff_dir / program / model / "single.json"
    if not path.exists():
        return None
    d = load(path)
    return d["different"], d["total"]


def changed_lines(a, b):
    """Lines added plus lines removed between two versions."""
    n = 0
    for line in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0):
        if line.startswith(("+++", "---", "@@")):
            continue
        if line.startswith(("+", "-")):
            n += 1
    return n


def fmt(pair):
    return "missing" if pair is None else f"{pair[0]}/{pair[1]}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a2", default="outputs")
    p.add_argument("--a2-diff", default="difftest")
    p.add_argument("--rerun", default="outputs_rerun")
    p.add_argument("--rerun-diff", default="difftest_rerun")
    args = p.parse_args()

    a2, rerun = ROOT / args.a2, ROOT / args.rerun
    rows = []
    for run_dir in sorted(rerun.glob("p*/*/single")):
        program, model = run_dir.parent.parent.name, run_dir.parent.name
        old_dir = a2 / program / model / "single"
        old_code, new_code = code_of(old_dir), code_of(run_dir)
        if old_code is None or new_code is None:
            same, lines = "no code", ""
        else:
            same = "yes" if old_code == new_code else "no"
            lines = changed_lines(old_code, new_code)
        rows.append({
            "program": program,
            "model": model,
            "a2_hidden": fmt(hidden_of(old_dir)),
            "rerun_hidden": fmt(hidden_of(run_dir)),
            "a2_new_input_diffs": fmt(diff_of(ROOT / args.a2_diff, program, model)),
            "rerun_new_input_diffs": fmt(diff_of(ROOT / args.rerun_diff, program, model)),
            "identical_code": same,
            "lines_changed": lines,
            "a2_lines": "" if old_code is None else len(old_code.splitlines()),
            "rerun_lines": "" if new_code is None else len(new_code.splitlines()),
        })

    if not rows:
        print(f"No runs found in {rerun}")
        return

    csv_path = rerun / "rerun_comparison.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    head = ["Program", "Model", "A2 hidden", "Rerun hidden", "A2 diffs",
            "Rerun diffs", "Same code", "Lines changed"]
    md = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        md.append(f"| {r['program']} | {r['model']} | {r['a2_hidden']} | {r['rerun_hidden']} | "
                  f"{r['a2_new_input_diffs']} | {r['rerun_new_input_diffs']} | "
                  f"{r['identical_code']} | {r['lines_changed']} |")
    both_pass = sum(r["a2_hidden"] == r["rerun_hidden"] and r["rerun_hidden"].split("/")[0] == r["rerun_hidden"].split("/")[-1]
                    for r in rows)
    identical = sum(r["identical_code"] == "yes" for r in rows)
    md += ["", f"Versions: {len(rows)}. Pass all hidden tests in both runs: {both_pass}. "
           f"Identical code: {identical}."]
    (rerun / "rerun_comparison.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"\nSaved {csv_path} and {rerun / 'rerun_comparison.md'}")


if __name__ == "__main__":
    main()