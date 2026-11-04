"""
A3, Part 4.1: build data/new_inputs/pNNN.json for every program in data/programs.csv.

Steps for each problem:
  1. Generate candidate inputs with scripts/input_generators.py (seeded, so the
     same command gives the same files): tiny, small, medium and large sizes.
  2. Check problem guarantees that the generator cannot make true by construction
     (260_B: the most frequent correct date must be unique).
  3. Run accepted CodeContests Python 3 solutions (when the dataset has them) as an
     oracle. An input that every reference solution rejects is dropped as invalid.
Steps for each program:
  4. Run the ORIGINAL program on every candidate. Drop inputs where it crashes,
     times out, or is slower than --max-seconds (margin under the 5 s timeout).
  5. Keep the first --per-program inputs, in a fixed order that mixes all sizes.
  6. Extra check, not required by the interface: compare the original's output with
     the oracle (or with a checker for problems that accept several answers).
     A disagreement means the original has a bug that the CodeContests tests missed.

Usage:
  python scripts/build_new_inputs.py --refs data/ref_solutions.json [--per-program 100]
Writes data/new_inputs/pNNN.json, data/new_inputs_meta.csv, data/new_inputs_report.json
"""
import argparse
import csv
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from input_generators import GENERATORS  # noqa: E402
from own_references import OWN  # noqa: E402

PLAN = [("tiny", 15), ("small", 55), ("medium", 50), ("large", 20)]   # 140 candidates
MULTI_ANSWER = {"143_A", "309_B", "663_A"}   # "print any" problems


def norm(text):
    lines = text.replace("\r\n", "\n").split("\n")
    lines = [ln.rstrip() for ln in lines]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def run(path, stdin, timeout):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    t0 = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, path], input=stdin.encode("utf-8"),
                           capture_output=True, timeout=timeout, env=env)
        dt = time.perf_counter() - t0
        if p.returncode != 0:
            return None, "error", dt
        return p.stdout.decode("utf-8", "replace"), "", dt
    except subprocess.TimeoutExpired:
        return None, "timeout", timeout


# ------------------------------------------------------------ guarantees
DATE = re.compile(r"(?=(\d\d-\d\d-\d\d\d\d))")
MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def ok_260_B(inp):
    counts = Counter()
    for m in DATE.finditer(inp.strip()):
        d, mo, y = m.group(1).split("-")
        d, mo, y = int(d), int(mo), int(y)
        if 2013 <= y <= 2015 and 1 <= mo <= 12 and 1 <= d <= MDAYS[mo - 1]:
            counts[m.group(1)] += 1
    if not counts:
        return False
    top = counts.most_common(2)
    return len(top) == 1 or top[0][1] > top[1][1]


GUARANTEE = {"260_B": ok_260_B}


# ------------------------------------------------------------ checkers for "print any"
def check_143_A(inp, out, oracle):
    r1, r2, c1, c2, d1, d2 = map(int, inp.split())
    o = " ".join(norm(out)).split()
    if o == ["-1"]:
        return " ".join(norm(oracle)).split() == ["-1"]
    if len(o) != 4:
        return False
    a, b, c, d = map(int, o)
    return (len({a, b, c, d}) == 4 and all(1 <= x <= 9 for x in (a, b, c, d)) and
            a + b == r1 and c + d == r2 and a + c == c1 and b + d == c2 and a + d == d1 and b + c == d2)


def check_663_A(inp, out, oracle):
    lines = norm(out)
    if not lines:
        return False
    if lines[0] != norm(oracle)[0]:
        return False
    if lines[0] == "Impossible":
        return len(lines) == 1
    toks, n = inp.split("=")[0].split(), int(inp.split("=")[1])
    got = lines[1].split()
    if len(got) != len(toks) + 2 or got[-2] != "=" or int(got[-1]) != n:
        return False
    total, sign = 0, 1
    for t, g in zip(toks, got):
        if t == "?":
            v = int(g)
            if not 1 <= v <= n:
                return False
            total += sign * v
        elif t != g:
            return False
        else:
            sign = 1 if t == "+" else -1
    return total == n


CHECKERS = {"143_A": check_143_A, "663_A": check_663_A}


def agree(pid, inp, out, oracle):
    if pid in CHECKERS:
        return CHECKERS[pid](inp, out, oracle)
    return norm(out) == norm(oracle)


# ------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", default=os.path.join(ROOT, "data", "ref_solutions.json"))
    ap.add_argument("--per-program", type=int, default=100)
    ap.add_argument("--max-seconds", type=float, default=2.0)
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    a = ap.parse_args()

    programs = list(csv.DictReader(open(os.path.join(ROOT, "data", "programs.csv"), encoding="utf-8")))
    refs = json.load(open(a.refs, encoding="utf-8")) if os.path.exists(a.refs) else {}
    for pid, srcs in OWN.items():           # our own references where CodeContests has none
        if not refs.get(pid):
            refs[pid] = srcs
    tmp = tempfile.mkdtemp(prefix="refs_")
    pool = ThreadPoolExecutor(max_workers=a.jobs)

    cands, oracle, prob_stats = {}, {}, {}
    for pid in sorted({p["problem_id"] for p in programs}):
        seed = int(hashlib.sha1(f"5570-{pid}".encode()).hexdigest()[:8], 16)
        rng, gen = random.Random(seed), GENERATORS[pid]
        seen, items, rejected = set(), [], 0
        for size, count in PLAN:
            made, tries = 0, 0
            while made < count and tries < count * 20:
                tries += 1
                x = gen(rng, size)
                if x in seen:
                    continue
                if pid in GUARANTEE and not GUARANTEE[pid](x):
                    rejected += 1
                    continue
                seen.add(x)
                items.append((size, x))
                made += 1
        # interleave sizes so the first N kept inputs mix all sizes
        by = defaultdict(list)
        for s, x in items:
            by[s].append(x)
        order = []
        while any(by.values()):
            for s, _ in PLAN:
                if by[s]:
                    order.append((s, by[s].pop(0)))
        # oracle from up to 3 accepted solutions (majority vote)
        ref_paths = []
        for i, src in enumerate(refs.get(pid, [])[:3]):
            path = os.path.join(tmp, f"{pid}_{i}.py")
            open(path, "w", encoding="utf-8").write(src)
            ref_paths.append(path)
        orc, dropped_invalid = [], 0
        if ref_paths:
            for s, x in order:
                outs = list(pool.map(lambda rp: run(rp, x, 10), ref_paths))
                good = [o for o, e, _ in outs if not e]
                if not good:
                    if all(e == "error" for _, e, _ in outs):   # every reference rejects it
                        dropped_invalid += 1
                        orc.append("__INVALID__")
                    else:                                       # references too slow: unchecked
                        orc.append(None)
                    continue
                vote = Counter("\n".join(norm(o)) for o in good).most_common(1)[0][0]
                orc.append(vote)
            keep = [(o, sx) for o, sx in zip(orc, order) if o != "__INVALID__"]
            order = [sx for _, sx in keep]
            orc = [o for o, _ in keep]
        cands[pid], oracle[pid] = order, (orc if ref_paths else None)
        prob_stats[pid] = {"candidates": len(order), "guarantee_rejected": rejected,
                           "dropped_invalid_by_refs": dropped_invalid, "n_refs": len(ref_paths)}
        print(f"{pid:36s} candidates={len(order):3d} refs={len(ref_paths)} invalid={dropped_invalid}", flush=True)

    out_dir = os.path.join(ROOT, "data", "new_inputs")
    os.makedirs(out_dir, exist_ok=True)
    meta, report = [], {"settings": vars(a), "plan": PLAN, "problems": prob_stats, "programs": {}}
    for p in programs:
        pid, prog = p["problem_id"], p["program_id"]
        code = os.path.join(ROOT, p["code_path"])
        order = cands[pid]
        res = list(pool.map(lambda sx: run(code, sx[1], 5.0), order))
        kept, sizes, drop = [], Counter(), Counter()
        mism, n_checked = [], 0
        for i, ((s, x), (out, err, dt)) in enumerate(zip(order, res)):
            if err:
                drop[err] += 1
                continue
            if dt > a.max_seconds:
                drop["slow"] += 1
                continue
            if len(kept) >= a.per_program:
                continue
            kept.append(x)
            sizes[s] += 1
            if oracle[pid] is not None and oracle[pid][i] is not None:
                n_checked += 1
                if not agree(pid, x, out, oracle[pid][i]):
                    mism.append(len(kept) - 1)
        json.dump({"program_id": prog, "inputs": kept},
                  open(os.path.join(out_dir, f"{prog}.json"), "w", encoding="utf-8", newline="\n"),
                  ensure_ascii=False)
        checked = oracle[pid] is not None
        meta.append({"program_id": prog, "problem_id": pid, "n_inputs": len(kept),
                     "tiny": sizes["tiny"], "small": sizes["small"], "medium": sizes["medium"],
                     "large": sizes["large"], "dropped_error": drop["error"],
                     "dropped_timeout": drop["timeout"], "dropped_slow": drop["slow"],
                     "oracle": ("checker" if pid in CHECKERS else "reference") if checked else "none",
                     "oracle_checked_inputs": n_checked if checked else 0,
                     "original_disagrees_with_oracle": len(mism) if checked else ""})
        report["programs"][prog] = {"disagree_input_indexes": mism[:20]}
        print(f"{prog} {pid:36s} kept={len(kept):3d} drop={dict(drop)} oracle_disagree={len(mism) if checked else '-'}", flush=True)
    with open(os.path.join(ROOT, "data", "new_inputs_meta.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(meta[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(meta)
    json.dump(report, open(os.path.join(ROOT, "data", "new_inputs_report.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
