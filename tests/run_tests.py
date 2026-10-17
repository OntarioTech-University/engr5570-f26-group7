"""Group 7 / ENGR 5570G A2: shared CodeContests test runner.

Contract: run_tests(code_path, tests_path, suite='public', timeout=5.0) -> dict
Standard library only; accepts Python 3 stdin/stdout programs and UTF-8 JSON tests.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path


def _normalize_output(text: str) -> str:
    """Apply ONLY the team's three permitted output-normalization rules."""
    text = text.replace("\r\n", "\n")
    lines = [line.rstrip(" ") for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _as_text(value) -> str:
    """TimeoutExpired may contain byte strings even with text=True."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _last_error_lines(stderr: str, return_code: int) -> str:
    lines = stderr.strip().splitlines()
    return ("\n".join(lines[-5:]) or f"Process exited with code {return_code}")[:500]


def run_tests(
    code_path: str,
    tests_path: str,
    suite: str = "public",
    timeout: float = 5.0,
) -> dict:
    """Execute selected cases, count outcomes, and return the exact shared schema.

    Test indices are currently zero-based in the combined selected test list.
    Confirm with the group if a different convention is desired.
    """
    suite_keys = {
        "public": ("public",),
        "hidden": ("private", "generated"),
        "all": ("public", "private", "generated"),
    }
    if suite not in suite_keys:
        raise ValueError("suite must be 'public', 'hidden', or 'all'")
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")

    with Path(tests_path).open("r", encoding="utf-8") as file:
        test_data = json.load(file)

    cases = []
    for key in suite_keys[suite]:
        group = test_data[key]
        if not isinstance(group, list):
            raise ValueError(f"'{key}' must contain a list of tests")
        cases.extend(group)

    passed = 0
    failed = 0
    failures = []
    script = str(Path(code_path).resolve())
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    start = time.perf_counter()
    for index, case in enumerate(cases):
        test_input = case["input"]
        expected = case["output"]
        actual = ""
        error = ""
        success = False

        try:
            result = subprocess.run(
                [sys.executable, "-B", script],
                input=test_input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                env=env,
                check=False,
            )
            actual = result.stdout
            if result.returncode != 0:
                error = _last_error_lines(result.stderr, result.returncode)
            else:
                success = (_normalize_output(actual) == _normalize_output(expected))
        except subprocess.TimeoutExpired as exc:
            # subprocess.run kills and waits for the direct child on timeout.
            actual = _as_text(exc.stdout)
            error = "timeout"

        if success:
            passed += 1
        else:
            failed += 1
            if len(failures) < 5:
                failures.append({
                    "test_index": index,
                    "input": test_input[:500],
                    "expected": expected[:500],
                    "actual": actual[:500],
                    "error": error[:500],
                })

    return {
        "suite": suite,
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "failures": failures,
        "time_seconds": time.perf_counter() - start,
    }
