"""Independent local checks for run_tests.py (no Cris data needed)."""
import json
import tempfile
from pathlib import Path

from run_tests import run_tests


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("PASS:", message)


def main():
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        code = root / "program.py"
        tests = root / "tests.json"
        tests.write_text(json.dumps({
            "public": [
                {"input": "2 3\n", "output": "5\n"},
                {"input": "10 20\n", "output": "30\n"},
            ],
            "private": [{"input": "-1 2\n", "output": "1\n"}],
            "generated": [{"input": "0 0\n", "output": "0\n"}],
        }), encoding="utf-8")
        code.write_text(
            'a, b = map(int, input().split())\nprint(a + b)\n',
            encoding="utf-8",
        )
        for mode, total in [("public", 2), ("hidden", 2), ("all", 4)]:
            result = run_tests(str(code), str(tests), suite=mode)
            check(result["passed"] == total and result["failed"] == 0,
                  f"{mode}: all {total} cases passed")
            check(result["total"] == result["passed"] + result["failed"],
                  f"{mode}: total equals passed + failed")
            check(result["time_seconds"] >= 0, f"{mode}: nonnegative timing")

        code.write_text('a, b = map(int, input().split())\nprint(a - b)\n', encoding="utf-8")
        wrong = run_tests(str(code), str(tests), suite="public")
        check(wrong["failed"] == 2 and wrong["failures"][0]["error"] == "",
              "wrong output: failed and error is empty")

        code.write_text('print(\n', encoding="utf-8")
        bad_syntax = run_tests(str(code), str(tests), suite="public")
        check(bad_syntax["failed"] == 2 and "SyntaxError" in bad_syntax["failures"][0]["error"],
              "syntax error: every selected test failed")

        code.write_text('while True:\n    pass\n', encoding="utf-8")
        timed = run_tests(str(code), str(tests), suite="public", timeout=0.15)
        check(timed["failed"] == 2 and all(x["error"] == "timeout" for x in timed["failures"]),
              "infinite loop: each process timed out and was terminated")

        tests.write_text(json.dumps({
            "public": [{"input": "", "output": "5\n"}],
            "private": [], "generated": []
        }), encoding="utf-8")
        code.write_text('import sys\nsys.stdout.write("5   \\r\\n\\r\\n")\n', encoding="utf-8")
        normalized = run_tests(str(code), str(tests))
        check(normalized["passed"] == 1,
              "CRLF, trailing spaces and trailing blank lines normalize")

        code.write_text('print(" 5")\n', encoding="utf-8")
        leading = run_tests(str(code), str(tests))
        check(leading["failed"] == 1, "leading spaces are NOT ignored")

        tests.write_text(json.dumps({
            "public": [{"input": "", "output": "correct\n"} for _ in range(7)],
            "private": [], "generated": []
        }), encoding="utf-8")
        code.write_text('print("incorrect")\n', encoding="utf-8")
        capped = run_tests(str(code), str(tests))
        check(capped["failed"] == 7 and capped["total"] == 7 and len(capped["failures"]) == 5,
              "7 failures counted, only first 5 detailed")

        try:
            run_tests(str(code), str(tests), suite="other")
            raise AssertionError("Invalid suite unexpectedly accepted")
        except ValueError:
            print("PASS: invalid suite rejected")

    print("\nALL LOCAL CHECKS PASSED")


if __name__ == "__main__":
    main()
