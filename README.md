# engr5570-f26-group7

ENGR 5570 Group 7: LLM refactoring of AI-generated Python code.

We ask three LLMs to refactor 34 AI-written Python programs from CodeContests.
Then we check if the refactored programs still give the same output, and if
the code is easier to maintain.

This README explains how to set up the environment and run every step.
Each folder also has its own README with more detail.

## 1. Setup

You need Python 3.12 and Git. Exact versions are in `VERSIONS.md`.

```bash
git clone https://github.com/OntarioTech-University/engr5570-f26-group7
cd engr5570-f26-group7
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The refactoring step calls the models through OpenRouter. Make a file called
`.env` in the repository root with this one line:

```
OPENROUTER_API_KEY=your_key_here
```

`.env` is in `.gitignore`. Never commit it.

The code smell scores need PyExamine, which is installed in its own
environment. See step 5.

## 2. Data

Everything needed is already in `data/`, so you do not need to download
anything to rerun the experiments.

| Path | What it is |
| --- | --- |
| `data/programs.csv` | The 34 programs, one row each |
| `data/programs/pNNN.py` | The original programs |
| `data/tests/pNNN.json` | Public and hidden tests from CodeContests |
| `data/new_inputs/pNNN.json` | 3,378 new inputs, made in A3 |

The programs come from the replication package of Zhu, Tsantalis and Rigby,
Zenodo DOI 10.5281/zenodo.19245562. The tests come from CodeContests,
Hugging Face `deepmind/code_contests`, revision
`802411c3010cb00d1b05bad57ca77365a3c699d6`.

To build the data again from these sources:

```bash
python scripts/build_subjects.py      # programs and tests
python scripts/verify_subjects.py     # check every original passes all tests
python scripts/build_new_inputs.py    # new inputs
python scripts/verify_new_inputs.py   # check the originals run on every new input
```

See `data/README.md` and `data/NEW_INPUTS.md` for details.

## 3. Refactoring

`refactor/run_loop.py` sends each program to each model and saves the result.
Settings: temperature 0, max_tokens 32,000, up to 3 retries on API errors.

| Short name | OpenRouter model |
| --- | --- |
| qwen | qwen/qwen3.8-max-0902 |
| deepseek | deepseek/deepseek-v4-pro-0813 |
| gpt | openai/gpt-6-sol |

```bash
# free test with no API calls
python refactor/run_loop.py --dry-run --limit 2

# A2: general refactoring task, results in outputs/
python refactor/run_loop.py --condition single

# A3: two specific refactoring tasks
python refactor/run_loop.py --condition single \
    --task-file refactor/task_main_function.txt --out outputs_task_main
python refactor/run_loop.py --condition single \
    --task-file refactor/task_extract.txt --out outputs_task_extract

# summary of the results in one folder
python refactor/results_report.py outputs_task_extract
```

The prompt template is `refactor/prompt_base.txt`. The task text for each
experiment is in `refactor/task_*.txt`.

## 4. Tests

```bash
# check the hidden test results of every refactored version
python -m tests.run_hidden_batch --out outputs

# compare the outputs of the original and refactored programs on the new inputs
python -m tests.compare_outputs --out outputs --results difftest
python -m tests.compare_outputs --out outputs_task_main --results difftest_task_main
python -m tests.compare_outputs --out outputs_task_extract --results difftest_task_extract
```

Hidden tests and new inputs are never shown to the models.

## 5. Code quality scores

PyExamine needs its own environment. A2 and A3 used different versions, and
the version changes the smell counts, so please install the exact commit.
See `scores/README.md` for the full reason.

```bash
# A2 scores, PyExamine 0.2.3
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python radon \
    "code-quality-analyzer @ git+https://github.com/KarthikShivasankar/python_smells_detector@fd6d9f971c8eb577a5686da0e0c283e81edc0695"
.venv/bin/python scores/run_scoring.py
python scores/make_summary.py

# A3 analysis, PyExamine 0.3.0
uv venv --python 3.12 .venv-a3
uv pip install --python .venv-a3/bin/python radon \
    "code-quality-analyzer @ git+https://github.com/KarthikShivasankar/python_smells_detector@838b212fafe9b1ff1e06c3364892e53177dab16f"
.venv-a3/bin/python scores/analyze_tradeoff.py
.venv-a3/bin/python scores/analyze_tradeoff.py --outputs outputs_task_main
.venv-a3/bin/python scores/analyze_tradeoff.py --outputs outputs_task_extract
```

## 6. Where the results are

| Folder | What it holds |
| --- | --- |
| `outputs/` | A2 results, general refactoring task |
| `outputs_task_main/` | A3 results, remove globals and top-level code |
| `outputs_task_extract/` | A3 results, extract short functions |
| `outputs_pilot_hard/` | Small pilot of the harder tasks on 5 programs |
| `difftest*/` | Output comparisons on the new inputs |
| `scores/` | Complexity and code smell scores |
| `docs/` | Notes and screenshots for each assignment |

Each run is saved as `<folder>/<program>/<model>/<condition>/`, with
`summary.json`, `hidden.json` and one folder per round with the code and the
model's reply.

## Team

Fangyu Lin, Cris Huynh, Yujie Lin, Camilo Bellnavis, Hiranmayee Brundavanam.