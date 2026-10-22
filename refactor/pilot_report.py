"""
Show public and hidden test results for every run in one output folder.

Usage (from the repository root):
  python refactor/pilot_report.py outputs_pilot_hard
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def score(path):
    if not path.exists():
        return "none"
    r = json.loads(path.read_text(encoding="utf-8"))
    return f"{r['passed']}/{r['total']}"


def main():
    folder = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "outputs_pilot_hard")
    rows = sorted(folder.glob("p*/*/single/summary.json"))
    if not rows:
        print(f"No results found in {folder}")
        return
    failed = 0
    print(f"{'program':8} {'model':9} {'public':>8} {'hidden':>10}  stop_reason")
    for f in rows:
        s = json.loads(f.read_text(encoding="utf-8"))
        public = score(f.parent / "round_0" / "tests.json")
        hidden = score(f.parent / "hidden.json")
        bad = public == "none" or public.split("/")[0] != public.split("/")[1]
        failed += bad
        mark = "  <-- public test failed" if bad else ""
        print(f"{s['program_id']:8} {s['model']:9} {public:>8} {hidden:>10}  {s['stop_reason']}{mark}")
    print(f"\n{failed} of {len(rows)} runs failed a public test. "
          f"These are the runs where the loop would start.")


if __name__ == "__main__":
    main()