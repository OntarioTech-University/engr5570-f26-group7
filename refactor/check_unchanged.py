"""
Check how many refactored results are the same as the original program.

For every outputs/<program>/<model>/<condition>/summary.json it compares the
final code with the original code and puts each result in one group:

  unchanged     the code is exactly the same (ignoring spaces at line ends)
  format_only   only comments, blank lines or spacing changed; Python sees
                the same program (same syntax tree)
  changed       the program itself was changed
  no_code       the run has no final code

Usage (from the repository root):
  python refactor/check_unchanged.py                  # single condition
  python refactor/check_unchanged.py --condition loop
"""

import argparse
import ast
import csv
import difflib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def normalize(code):
    lines = [line.rstrip() for line in code.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def same_tree(a, b):
    try:
        return ast.dump(ast.parse(a)) == ast.dump(ast.parse(b))
    except SyntaxError:
        return False


def changed_lines(a, b):
    diff = difflib.unified_diff(normalize(a).split("\n"), normalize(b).split("\n"), lineterm="", n=0)
    return sum(1 for line in diff
               if line[:1] in "+-" and not line.startswith(("+++", "---")))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--condition", choices=["single", "loop"], default="single")
    p.add_argument("--out", default="outputs")
    args = p.parse_args()

    with open(ROOT / "data" / "programs.csv", encoding="utf-8") as f:
        originals = {row["program_id"]: (ROOT / row["code_path"]).read_text(encoding="utf-8")
                     for row in csv.DictReader(f)}

    rows = []
    for summary_file in sorted((ROOT / args.out).glob(f"p*/*/{args.condition}/summary.json")):
        s = json.loads(summary_file.read_text(encoding="utf-8"))
        pid, model = s["program_id"], s["model"]
        if pid not in originals:
            continue
        if not s.get("final_code"):
            rows.append({"program_id": pid, "model": model, "group": "no_code", "changed_lines": ""})
            continue
        new = (summary_file.parent / s["final_code"]).read_text(encoding="utf-8")
        old = originals[pid]
        if normalize(new) == normalize(old):
            group = "unchanged"
        elif same_tree(new, old):
            group = "format_only"
        else:
            group = "changed"
        rows.append({"program_id": pid, "model": model, "group": group,
                     "changed_lines": changed_lines(old, new)})

    if not rows:
        print("No results found.")
        return

    by_model = defaultdict(Counter)
    for r in rows:
        by_model[r["model"]][r["group"]] += 1
    groups = ["changed", "format_only", "unchanged", "no_code"]
    print(f"Condition: {args.condition}\n")
    print(f"{'model':10}" + "".join(f"{g:>13}" for g in groups) + f"{'total':>8}")
    for model in sorted(by_model):
        c = by_model[model]
        print(f"{model:10}" + "".join(f"{c[g]:>13}" for g in groups) + f"{sum(c.values()):>8}")

    not_changed = [r for r in rows if r["group"] != "changed"]
    if not_changed:
        print("\nResults that are not real code changes:")
        for r in not_changed:
            print(f"  {r['program_id']} {r['model']:9} {r['group']}")

    out_file = ROOT / args.out / f"change_check_{args.condition}.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["program_id", "model", "group", "changed_lines"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()