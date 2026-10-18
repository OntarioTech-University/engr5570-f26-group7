# Code quality scores (A2, Part 4) · Camilo

Complexity, code smells and running time for the 34 original programs and all
102 refactored versions (34 programs x 3 models, `single` condition).

## Files

| File | What it is |
| --- | --- |
| `run_scoring.py` | Produces the scores. One row per version. |
| `make_summary.py` | Turns `scores.csv` into the comparison table for the write-up. |
| `scores.csv` | 136 rows: every program as original, gpt, deepseek and qwen. |
| `summary_table.md` | The table for the A2 report. |
| `skipped.json` | Runs with no usable code (`final_code: null`). Currently empty. |
| `code_quality_config.yaml` | PyExamine thresholds, copied from the tool so a rerun gives the same numbers if upstream defaults change. |

## Metrics and why

**Complexity and size** come from radon through Cris's `scripts/cleanup_metrics.py`,
not a separate copy. That file already scores module-level code as one block,
which matters because most of these contest programs keep their logic outside any
function and radon alone would score them 0. Reusing it means the original rows
here reproduce `data/subjects_meta.csv` exactly: all 34 match on `sloc`,
`n_functions`, `max_cc`, `max_nesting` and `longest_block`.

**Code smells** come from PyExamine, the tool the ASE paper used for the `smells`
column of `data/programs.csv`, so before and after are counted the same way.
It also fills a gap: the ASE package has no PyExamine report for the
`deepseek_coder/np` programs, so those originals have an empty `smells` value
upstream. Running the tool ourselves scores every original.

`n_smells` counts occurrences, not distinct kinds, the same way the `smells`
column does: two long functions in one file count twice.

**Running time** is the wall time of the whole hidden suite, measured with
Yujie's `tests/run_tests.py`.

## Why the time is measured again here

The plan was to read the time from each `hidden.json`. Those files and the
original timings in `data/verification_py31*.json` were produced on different
machines, so they cannot be compared with each other. The same 123 hidden tests
of `p001`:

| Source | Time |
| --- | ---: |
| original, this machine, Yujie's runner | 1.21 s |
| refactored gpt, `outputs/p001/gpt/single/hidden.json` | 5.11 s |
| original, `verification_py312.json` (Linux, Part 2 stand-in runner) | 1.85 s |

Reading the first and third rows as a before/after would report the refactoring
as roughly 2.8x slower when nothing about the code changed. `run_scoring.py`
therefore reruns the hidden suite for every version in one session on one
machine. It costs about two minutes for all 136 versions.

A time is only written when the version passes every hidden test, because a
crash or a timeout makes the number meaningless.

**Limit of this measurement.** Every test runs the program as a new process, and
these programs are small, so about 97% of the wall time is Python interpreter
startup (9.9 ms per run, 123 runs, 1.22 s of the 1.26 s measured for `p001`).
This metric can only detect a large slowdown, not a small one. Read the near-1.00
ratios as "no large regression", not as "identical performance".

## Rules followed

From the Shared Interfaces document, Part 3:

* score the original (`code_path` in `programs.csv`) and every `final_code`
* skip runs whose `final_code` is null (none so far, see `skipped.json`)
* compare running time only for versions that pass all hidden tests

## Reproduce

PyExamine needs Python 3.10 or newer, so it runs in its own environment.
`scripts/cleanup_metrics.py` works on 3.9 as well, but the script runs entirely
inside this environment.

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python radon \
    "code-quality-analyzer @ git+https://github.com/KarthikShivasankar/python_smells_detector"
.venv/bin/python scores/run_scoring.py      # about 2 minutes
python3 scores/make_summary.py
```

`--no-timing` skips rerunning the tests, `--limit N` scores only the first N
programs.

## Open point

Only the `single` condition exists in `outputs/` so far. The scripts read
`outputs/<program_id>/<model>/<condition>/`, so `loop` results are picked up
with no change once they land.

## References

* Shivashankar, K. and Martini, A. "PyExamine: A comprehensive, un-opinionated
  smell detection tool for Python." MSR 2025.
  <https://github.com/KarthikShivasankar/python_smells_detector>
* McCabe, T. J. "A complexity measure." *IEEE Trans. Softw. Eng.*, SE-2(4),
  308-320, 1976. doi: 10.1109/TSE.1976.233837
* Radon documentation. <https://radon.readthedocs.io/en/latest/>
