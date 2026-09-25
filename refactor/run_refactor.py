import datetime
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODELS = {
    "claude": "anthropic/claude-opus-4.6",
    "gpt": "openai/gpt-6-sol",
    "gemini": "google/gemini-3.8-flash",
    "deepseek": "deepseek/deepseek-v4-pro-0813",
}

TASK = "Find complex or deeply nested if/else logic, and make it simpler and easier to read."

template = (ROOT / "refactor" / "prompt_base.txt").read_text(encoding="utf-8")
code = (ROOT / "pilot" / "utils_original.py").read_text(encoding="utf-8")
prompt = template.replace("{REFACTORING_TASK}", TASK).replace("{CODE}", code)

today = datetime.date.today().isoformat()
out_dir = ROOT / "outputs" / today
out_dir.mkdir(parents=True, exist_ok=True)

runs = []
for short_name, model_id in MODELS.items():
    print(f"Calling {model_id} ...")
    try:
        resp = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=32000,
        )
    except Exception as e:
        print(f"  FAILED: {e}")
        runs.append({"model_requested": model_id, "error": str(e)})
        continue

    text = resp.choices[0].message.content or ""
    (out_dir / f"{short_name}_raw.md").write_text(text, encoding="utf-8")

    match = re.search(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    if match:
        (out_dir / f"{short_name}_utils.py").write_text(match.group(1), encoding="utf-8")
        status = "ok"
    else:
        status = "no code block found"

    usage = resp.usage.model_dump() if resp.usage else {}
    runs.append({
        "model_requested": model_id,
        "model_returned": resp.model,
        "status": status,
        "usage": usage,
    })
    print(f"  {status}, tokens used: {usage.get('total_tokens')}")

log = {"date": today, "task": TASK, "prompt_file": "refactor/prompt_base.txt", "runs": runs}
(out_dir / "run_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
print(f"Done. Outputs saved in {out_dir}")