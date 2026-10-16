"""
Stand-in test runner used by Cris to screen the ORIGINAL programs.

It follows Part 2 of the Group 7 Shared Interfaces exactly (same inputs, same
output shape, same comparison rules), so the screening result should match
Yujie's run_tests(). When Yujie's run_tests.py is in the repo, prefer it:
build_subjects.py and verify_subjects.py import it first and fall back to this file.

Extra (not in Part 2): stop_at_first_failure, used only to speed up screening.
"""
import json
import os
import subprocess
import sys
import time

MAX_FAILURES = 5
CUT = 500


def _normalize(text: str) -> list:
    lines = text.replace("\r\n", "\n").split("\n")
    lines = [ln.rstrip() for ln in lines]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _select(tests: dict, suite: str) -> list:
    if suite == "public":
        return tests["public"]
    if suite == "hidden":
        return tests["private"] + tests["generated"]
    if suite == "all":
        return tests["public"] + tests["private"] + tests["generated"]
    raise ValueError(f"unknown suite: {suite}")


def run_tests(code_path: str, tests_path: str, suite: str = "public",
              timeout: float = 5.0, stop_at_first_failure: bool = False) -> dict:
    with open(tests_path, encoding="utf-8") as f:
        cases = _select(json.load(f), suite)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    passed, failures, total_time = 0, [], 0.0
    for idx, case in enumerate(cases):
        start = time.perf_counter()
        error, actual = "", ""
        try:
            proc = subprocess.run(
                [sys.executable, code_path], input=case["input"].encode("utf-8"),
                capture_output=True, timeout=timeout, env=env)   # run() kills on timeout
            actual = proc.stdout.decode("utf-8", errors="replace")
            if proc.returncode != 0:
                err = proc.stderr.decode("utf-8", errors="replace").strip().splitlines()
                error = "\n".join(err[-5:]) or f"exit code {proc.returncode}"
        except subprocess.TimeoutExpired:
            error = "timeout"
        total_time += time.perf_counter() - start
        ok = not error and _normalize(actual) == _normalize(case["output"])
        if ok:
            passed += 1
        else:
            if len(failures) < MAX_FAILURES:
                failures.append({"test_index": idx, "input": case["input"][:CUT],
                                 "expected": case["output"][:CUT],
                                 "actual": actual[:CUT], "error": error[:CUT]})
            if stop_at_first_failure:
                total = passed + 1
                return {"suite": suite, "passed": passed, "failed": 1, "total": total,
                        "failures": failures, "time_seconds": round(total_time, 3),
                        "stopped_early": True}
    total = len(cases)
    return {"suite": suite, "passed": passed, "failed": total - passed, "total": total,
            "failures": failures, "time_seconds": round(total_time, 3)}
