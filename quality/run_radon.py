"""Part D - Code Quality Metrics.

Runs radon's cyclomatic complexity (cc) check on the original pilot file and
each of the 4 LLM-refactored versions, then builds a comparison table.

Usage: python3 quality/run_radon.py
"""
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = {
    "original": ROOT / "pilot" / "utils_original.py",
    "claude": ROOT / "outputs" / "2026-09-24" / "claude_utils.py",
    "gpt": ROOT / "outputs" / "2026-09-24" / "gpt_utils.py",
    "gemini": ROOT / "outputs" / "2026-09-24" / "gemini_utils.py",
    "deepseek": ROOT / "outputs" / "2026-09-24" / "deepseek_utils.py",
}

RAW_DIR = ROOT / "quality" / "radon_raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def run_radon_cc(path: Path, extra_args: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "radon", "cc", *extra_args, str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def grade(score: int) -> str:
    # radon's standard A-F cyclomatic complexity ranks
    if score <= 5:
        return "A"
    if score <= 10:
        return "B"
    if score <= 20:
        return "C"
    if score <= 30:
        return "D"
    if score <= 40:
        return "E"
    return "F"


rows = []
for name, path in FILES.items():
    if not path.exists():
        print(f"WARNING: missing {path}", file=sys.stderr)
        continue

    # Human-readable output, saved as evidence (stand-in for a screenshot).
    readable = run_radon_cc(path, ["-s", "-a"])
    (RAW_DIR / f"{name}_cc.txt").write_text(readable, encoding="utf-8")

    # JSON output, parsed to compute total/average/highest reliably.
    raw_json = run_radon_cc(path, ["-j"])
    data = json.loads(raw_json)
    blocks = data.get(str(path), [])
    scores = [b["complexity"] for b in blocks]

    if scores:
        total = sum(scores)
        average = round(statistics.mean(scores), 2)
        highest = max(scores)
        worst_block = max(blocks, key=lambda b: b["complexity"])
        worst_name = worst_block["name"]
    else:
        total = average = highest = 0
        worst_name = "-"

    rows.append({
        "version": name,
        "blocks": len(scores),
        "total_cc": total,
        "average_cc": average,
        "highest_cc": highest,
        "highest_grade": grade(highest),
        "worst_block": worst_name,
    })
    print(f"{name}: blocks={len(scores)} total={total} avg={average} highest={highest} ({grade(highest)}) in {worst_name}")

(ROOT / "quality" / "summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

# Markdown comparison table
lines = [
    "| Version | Blocks analyzed | Total CC | Average CC | Highest CC | Grade of worst block | Worst block |",
    "|---|---|---|---|---|---|---|",
]
for r in rows:
    lines.append(
        f"| {r['version']} | {r['blocks']} | {r['total_cc']} | {r['average_cc']} | "
        f"{r['highest_cc']} | {r['highest_grade']} | {r['worst_block']} |"
    )
(ROOT / "quality" / "summary_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"\nDone. Summary written to quality/summary_table.md and quality/summary.json")
