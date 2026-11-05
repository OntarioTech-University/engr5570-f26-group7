"""
Check data/new_inputs/ against Part 4.1 of the interface:
  - one file per program in data/programs.csv, keys exactly program_id and inputs
  - inputs are non-empty strings, no duplicates
  - the ORIGINAL program runs on every input without an error or a timeout
Runs one program at a time (no parallel load), with the 5-second timeout of Part 2.
  python scripts/verify_new_inputs.py
"""
import csv
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "programs.csv"), encoding="utf-8")))
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    errors, total, worst = [], 0, (0.0, "")
    for r in rows:
        pid = r["program_id"]
        path = os.path.join(ROOT, "data", "new_inputs", f"{pid}.json")
        if not os.path.exists(path):
            errors.append(f"{pid}: missing file")
            continue
        d = json.load(open(path, encoding="utf-8"))
        if set(d) != {"program_id", "inputs"} or d["program_id"] != pid:
            errors.append(f"{pid}: bad keys or program_id")
        xs = d["inputs"]
        if not xs or not all(isinstance(x, str) and x.strip() for x in xs) or len(set(xs)) != len(xs):
            errors.append(f"{pid}: empty, non-string or duplicate inputs")
        bad = 0
        for x in xs:
            t0 = time.perf_counter()
            try:
                p = subprocess.run([sys.executable, os.path.join(ROOT, r["code_path"])],
                                   input=x.encode("utf-8"), capture_output=True, timeout=5.0, env=env)
                if p.returncode != 0:
                    bad += 1
            except subprocess.TimeoutExpired:
                bad += 1
            dt = time.perf_counter() - t0
            if dt > worst[0]:
                worst = (dt, pid)
        total += len(xs)
        if bad:
            errors.append(f"{pid}: original fails on {bad} inputs")
        print(f"{pid}  {len(xs):3d} inputs  {'ok' if not bad else 'FAIL ' + str(bad)}", flush=True)
    print(f"\n{len(rows)} programs, {total} inputs, slowest single run {worst[0]:.2f}s ({worst[1]})")
    print("ALL CHECKS PASSED" if not errors else "\n".join(errors))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
