"""
Group 7 refactoring script for A2 and A3.

For every program in data/programs.csv and every model, it runs:
  single : the model refactors once, no feedback
  loop   : the model refactors, we run the PUBLIC tests, and send any
           failures back so it can fix its code, up to --max-rounds calls

Round 0 of the loop is the same request as the single condition, so the
loop reuses the single result as its round 0. This keeps the two
conditions paired and saves API calls.

At the end of each run it also runs the HIDDEN tests on the final code and
saves hidden.json. Hidden results are never sent to the model.

Output folders follow Part 3 of the Shared Interfaces.

Examples (run from the repository root):
  python refactor/run_loop.py --dry-run --limit 2          # free test, no API calls
  python refactor/run_loop.py --programs p001 --models qwen  # one real run
  python refactor/run_loop.py --condition single           # A2 baseline
  python refactor/run_loop.py                              # everything
  python refactor/run_loop.py --task-file refactor/task_main_function.txt \\
      --condition single --programs p023 p013 --out outputs_pilot_hard
                                                           # try a different task
"""

import argparse
import csv
import datetime
import difflib
import importlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MODELS = {
    "qwen": "qwen/qwen3.8-max-0902",
    "deepseek": "deepseek/deepseek-v4-pro-0813",
    "gpt": "openai/gpt-6-sol",
}

TASK = ("Reduce complexity and improve readability. Simplify complex or deeply "
        "nested conditional logic, and split long code into smaller, well named "
        "functions where this makes the code easier to understand.")

FEEDBACK_TEMPLATE = """Your refactored code failed {failed} of {total} tests. \
The refactored code must behave exactly like the original code, so the output \
for every input must be the same.

Failed tests:
{failures}

Please fix your refactored code so that it behaves exactly like the original. \
Keep your structural improvements where you can. Do not change the original \
behavior in any other way.

Response format:
1. The complete fixed file in a single Python code block.
2. A short bulleted list of what you changed."""

CODE_BLOCK = re.compile(r"```(?:python|py)[ \t]*\n(.*?)```", re.S)
MAX_FIELD = 500


# ----------------------------------------------------------------- runner

def load_runner():
    """Yujie's runner if it is in the repo, otherwise Cris's stand-in."""
    for module_name, label in [("tools.run_tests", "tools/run_tests.py (Yujie)"),
                               ("scripts.check_runner", "scripts/check_runner.py (Cris stand-in)")]:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "run_tests"):
                return module.run_tests, label
        except ImportError:
            continue
    sys.exit("No test runner found. Expected tools/run_tests.py or scripts/check_runner.py "
             "with a run_tests() function.")


def cut(text):
    text = "" if text is None else str(text)
    return text if len(text) <= MAX_FIELD else text[:MAX_FIELD] + "\n...[cut]"


def format_failures(result):
    parts = []
    for i, f in enumerate(result.get("failures", [])[:5], 1):
        lines = [f"Test {i}:",
                 "Input:", cut(f.get("input")),
                 "Expected output:", cut(f.get("expected")),
                 "Your output:", cut(f.get("actual"))]
        if f.get("error"):
            lines += ["Error:", cut(f.get("error"))]
        parts.append("\n".join(lines))
    return "\n\n".join(parts)


# ----------------------------------------------------------------- model

class Caller:
    def __init__(self, dry_run):
        self.dry_run = dry_run
        if not dry_run:
            from dotenv import load_dotenv
            from openai import OpenAI
            load_dotenv(ROOT / ".env")
            self.client = OpenAI(base_url="https://openrouter.ai/api/v1",
                                 api_key=os.environ["OPENROUTER_API_KEY"])

    def call(self, model_id, messages):
        """Returns (text, meta). meta has model_returned, finish_reason, usage, attempts.
        Retries up to 3 times on an error or an empty reply. Raises if every try errors."""
        if self.dry_run:
            # Echo the code from the first message back, unchanged. Costs nothing.
            original = messages[0]["content"].split("Code:", 1)[-1].strip()
            return (f"```python\n{original}\n```\n- dry run, no change",
                    {"model_returned": "dry-run", "finish_reason": "stop", "usage": {}, "cost": 0.0})
        last_error, meta, cost = None, None, 0.0
        for attempt in range(1, 4):
            try:
                resp = self.client.chat.completions.create(
                    model=model_id, messages=messages, temperature=0, max_tokens=32000,
                    extra_body={"usage": {"include": True}})
            except Exception as e:  # network or provider error
                last_error = e
                time.sleep(5 * attempt)
                continue
            usage = resp.usage.model_dump() if resp.usage else {}
            cost += usage.get("cost") or 0.0  # empty replies are billed too
            text = resp.choices[0].message.content or ""
            meta = {"model_returned": resp.model,
                    "finish_reason": resp.choices[0].finish_reason,
                    "usage": usage, "attempts": attempt, "cost": cost}
            if text.strip():
                return text, meta
            time.sleep(5 * attempt)  # empty reply, try again
        if meta is not None:
            return "", meta  # every try came back empty
        raise RuntimeError(str(last_error))


# ----------------------------------------------------------------- helpers

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path, data):
    write(path, json.dumps(data, indent=2, ensure_ascii=False))


def make_diff(old, new, old_name, new_name):
    return "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                        fromfile=old_name, tofile=new_name))


def do_round(caller, model_id, messages, round_dir, previous_code, previous_name,
             tests_path, run_tests):
    """One model call plus public tests. Returns (code or None, reply text, tests, usage, error)."""
    write(round_dir / "prompt.txt", messages[-1]["content"])
    try:
        text, meta = caller.call(model_id, messages)
    except RuntimeError as e:
        write_json(round_dir / "meta.json", {"error": str(e)})
        return None, "", None, {}, "api_error"
    write_json(round_dir / "meta.json", meta)
    usage = {"cost": meta.get("cost", 0.0)}
    write(round_dir / "response.md", text)
    match = CODE_BLOCK.search(text)
    if not match:
        return None, text, None, usage, "no_code"
    code = match.group(1)
    code_path = round_dir / "code.py"
    write(code_path, code)
    write(round_dir / "diff.txt", make_diff(previous_code, code, previous_name, "code.py"))
    tests = run_tests(str(code_path), str(tests_path), suite="public")
    write_json(round_dir / "tests.json", tests)
    return code, text, tests, usage, None


def cost_of(usage):
    return usage.get("cost") or 0.0


# ----------------------------------------------------------------- conditions

def run_single(caller, program, short, model_id, base, run_tests):
    out = base / "single"
    original = Path(ROOT / program["code_path"]).read_text(encoding="utf-8")
    prompt = TEMPLATE.replace("{REFACTORING_TASK}", TASK).replace("{CODE}", original)
    messages = [{"role": "user", "content": prompt}]
    code, _, tests, usage, error = do_round(caller, model_id, messages, out / "round_0",
                                            original, "original.py",
                                            ROOT / program["tests_path"], run_tests)
    return finish(out, program, short, model_id, "single", 1, 1,
                  "round_0/code.py" if code else None,
                  error or "single_pass", cost_of(usage), run_tests)


def run_loop(caller, program, short, model_id, base, max_rounds, run_tests):
    out = base / "loop"
    single_round0 = base / "single" / "round_0"
    original = Path(ROOT / program["code_path"]).read_text(encoding="utf-8")
    tests_path = ROOT / program["tests_path"]
    prompt = TEMPLATE.replace("{REFACTORING_TASK}", TASK).replace("{CODE}", original)
    messages = [{"role": "user", "content": prompt}]
    total_cost = 0.0
    reused_cost = 0.0

    # Round 0: reuse the single result (same request), or call the model.
    if (single_round0 / "response.md").exists():
        shutil.copytree(single_round0, out / "round_0", dirs_exist_ok=True)
        reply = (out / "round_0" / "response.md").read_text(encoding="utf-8")
        code_file = out / "round_0" / "code.py"
        code = code_file.read_text(encoding="utf-8") if code_file.exists() else None
        tests_file = out / "round_0" / "tests.json"
        tests = json.loads(tests_file.read_text(encoding="utf-8")) if tests_file.exists() else None
        error = None if code else "no_code"
        single_summary = base / "single" / "summary.json"
        if single_summary.exists():  # count the cost of the reused round 0 in the loop too
            reused_cost = json.loads(single_summary.read_text(encoding="utf-8")).get("cost_usd", 0.0)
            total_cost += reused_cost
    else:
        code, reply, tests, usage, error = do_round(caller, model_id, messages, out / "round_0",
                                                    original, "original.py", tests_path, run_tests)
        total_cost += cost_of(usage)

    rounds, final, last_code = 1, ("round_0/code.py" if code else None), code
    while error is None:
        if tests["failed"] == 0:
            error = "all_public_passed"
            break
        if rounds >= max_rounds:
            error = "max_rounds"
            break
        # Only public test failures are sent back. Never hidden tests.
        feedback = FEEDBACK_TEMPLATE.format(failed=tests["failed"], total=tests["total"],
                                            failures=format_failures(tests))
        messages += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": feedback}]
        name = f"round_{rounds}"
        code, reply, tests, usage, error = do_round(caller, model_id, messages, out / name,
                                                    last_code, f"round_{rounds - 1}/code.py",
                                                    tests_path, run_tests)
        total_cost += cost_of(usage)
        rounds += 1
        if code:
            final, last_code = f"{name}/code.py", code

    summary = finish(out, program, short, model_id, "loop", rounds, max_rounds, final,
                     error, total_cost, run_tests)
    return summary, reused_cost


def finish(out, program, short, model_id, condition, rounds, max_rounds, final_code,
           stop_reason, cost, run_tests):
    if final_code:
        hidden = run_tests(str(out / final_code), str(ROOT / program["tests_path"]), suite="hidden")
        write_json(out / "hidden.json", hidden)
    summary = {
        "program_id": program["program_id"],
        "model": short,
        "model_id": model_id,
        "condition": condition,
        "rounds": rounds,
        "max_rounds": max_rounds,
        "stop_reason": stop_reason,
        "final_code": final_code,
        "cost_usd": round(cost, 6),
        "date": datetime.date.today().isoformat(),
    }
    write_json(out / "summary.json", summary)
    hidden_text = ""
    if final_code:
        h = json.loads((out / "hidden.json").read_text(encoding="utf-8"))
        hidden_text = f"hidden {h['passed']}/{h['total']}"
    print(f"  {condition:6} rounds {rounds}  {stop_reason:18} {hidden_text}")
    return summary


# ----------------------------------------------------------------- main

def main():
    global TEMPLATE
    p = argparse.ArgumentParser()
    p.add_argument("--models", nargs="+", default=list(MODELS), choices=list(MODELS))
    p.add_argument("--programs", nargs="+", help="program ids, e.g. p001 p002")
    p.add_argument("--limit", type=int, help="only the first N programs")
    p.add_argument("--condition", choices=["single", "loop", "both"], default="both")
    p.add_argument("--max-rounds", type=int, default=4)
    p.add_argument("--force", action="store_true", help="redo runs that already have summary.json")
    p.add_argument("--redo-failed", action="store_true",
                   help="redo runs that ended with no_code or api_error")
    p.add_argument("--dry-run", action="store_true", help="no API calls, the model echoes the code")
    p.add_argument("--out", default="outputs", help="output folder, default outputs")
    p.add_argument("--task-file", help="text file with a different refactoring task, "
                                       "e.g. refactor/task_main_function.txt")
    args = p.parse_args()

    global TASK
    if args.task_file:
        TASK = (ROOT / args.task_file).read_text(encoding="utf-8-sig").strip()
        if args.out == "outputs" and not args.dry_run:
            sys.exit("Please use --out with --task-file, so the baseline in outputs/ is not mixed up.")

    TEMPLATE = (ROOT / "refactor" / "prompt_base.txt").read_text(encoding="utf-8-sig")
    with open(ROOT / "data" / "programs.csv", encoding="utf-8") as f:
        programs = list(csv.DictReader(f))
    if args.programs:
        programs = [x for x in programs if x["program_id"] in args.programs]
    if args.limit:
        programs = programs[:args.limit]

    run_tests, runner_label = load_runner()
    caller = Caller(args.dry_run)
    out_root = ROOT / ("outputs_dryrun" if args.dry_run and args.out == "outputs" else args.out)
    print(f"runner: {runner_label} | programs: {len(programs)} | models: {args.models} | "
          f"condition: {args.condition} | max rounds: {args.max_rounds}"
          f"{' | DRY RUN' if args.dry_run else ''}")

    total = 0.0
    for program in programs:
        for short in args.models:
            model_id = MODELS[short]
            base = out_root / program["program_id"] / short
            print(f"{program['program_id']} {short}")
            for condition in (["single", "loop"] if args.condition == "both" else [args.condition]):
                summary_file = base / condition / "summary.json"
                redo = args.force
                if summary_file.exists() and not redo and args.redo_failed:
                    old = json.loads(summary_file.read_text(encoding="utf-8"))
                    redo = old.get("stop_reason") in ("no_code", "api_error")
                if summary_file.exists() and not redo:
                    print(f"  {condition:6} already done, skipped")
                    continue
                if (base / condition).exists():
                    shutil.rmtree(base / condition)
                if condition == "single":
                    s = run_single(caller, program, short, model_id, base, run_tests)
                    total += s["cost_usd"]
                else:
                    s, reused = run_loop(caller, program, short, model_id, base,
                                         args.max_rounds, run_tests)
                    total += s["cost_usd"] - reused  # round 0 was already paid in single
    print(f"Done. New API cost of this run: about {total:.4f} US dollars. Results in {out_root}")


if __name__ == "__main__":
    main()