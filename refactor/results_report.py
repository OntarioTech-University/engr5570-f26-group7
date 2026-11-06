"""
Show the test results of every run in one output folder.

Usage (from the repository root):
  python refactor/results_report.py outputs_task_extract
  python refactor/results_report.py outputs_task_extract --condition loop
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def score(result):
    return "none" if result is None else f"{result['passed']}/{result['total']}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("folder")
    p.add_argument("--condition", choices=["single", "loop"], default="single")
    args = p.parse_args()

    folder = ROOT / args.folder
    files = sorted(folder.glob(f"p*/*/{args.condition}/summary.json"))
    if not files:
        print(f"No {args.condition} results found in {folder}")
        return

    totals = defaultdict(lambda: defaultdict(float))
    print(f"{'program':8} {'model':9} {'public r0':>9} {'hidden':>9} {'rounds':>6}  stop_reason")
    for f in files:
        s = json.loads(f.read_text(encoding="utf-8"))
        first_public = load(f.parent / "round_0" / "tests.json")
        hidden = load(f.parent / "hidden.json")
        public_ok = first_public is not None and first_public["failed"] == 0
        hidden_ok = hidden is not None and hidden["failed"] == 0
        mark = "" if public_ok else "  <-- failed a public test in round 0"
        print(f"{s['program_id']:8} {s['model']:9} {score(first_public):>9} {score(hidden):>9} "
              f"{s['rounds']:>6}  {s['stop_reason']}{mark}")
        t = totals[s["model"]]
        t["runs"] += 1
        t["public_ok_r0"] += public_ok
        t["hidden_ok"] += hidden_ok
        t["loop_used"] += s["rounds"] > 1
        t["cost"] += s.get("cost_usd") or 0.0

    print(f"\nCondition: {args.condition}")
    print(f"{'model':9} {'runs':>5} {'pass public r0':>15} {'pass hidden':>12} {'loop used':>10} {'cost USD':>9}")
    for model in sorted(totals):
        t = totals[model]
        print(f"{model:9} {int(t['runs']):>5} {int(t['public_ok_r0']):>15} {int(t['hidden_ok']):>12} "
              f"{int(t['loop_used']):>10} {t['cost']:>9.2f}")


if __name__ == "__main__":
    main()