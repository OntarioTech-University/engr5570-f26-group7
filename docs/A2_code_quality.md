# A2 · Code Quality Scores (Camilo)

## Metrics

**Complexity and size.** We score every program with radon [1] through Cris's
`scripts/cleanup_metrics.py` rather than a separate copy, so the before and after
numbers are produced the same way as the baseline in `data/subjects_meta.csv`.
This matters here: radon only scores `def` and `class` blocks, and most of these
contest programs keep their logic at module level, so radon on its own would
score them 0. Cris's module wrapping avoids that. As a check, our rows for the
34 originals reproduce `subjects_meta.csv` exactly on `sloc`, `n_functions`,
`max_cc`, `max_nesting` and `longest_block`.

**Code smells.** We use PyExamine [2], the tool the ASE authors used to produce
the `smells` column of `data/programs.csv`. We run its code-level detector on
each file. We do not run its structural or architectural detectors: the
structural metrics overlap with what radon already gives us, and the
architectural ones describe a whole project folder rather than a single program,
which is also why the team excluded Orphan Module and High Fan-in from the
selection rule.

Our counts are therefore code-level only, and they are not the same quantity as
the `smells` column: on the 34 originals we count 14 code smells across 13
programs, while the column lists 25 entries across 18 programs, 11 of them
Orphan Module. The column is also empty for 16 of the 34 originals. We do not
compare our numbers to that column. What the comparison below rests on is that
originals and refactored versions are measured the same way as each other, by
the same detector, on the same kind of input.

Our count reports occurrences, not distinct kinds: two long functions in one
file count twice.

**Running time.** The wall time of the whole hidden suite, measured with Yujie's
`tests/run_tests.py`.

We report the highest complexity, the nesting depth, the size and the smell
count together rather than picking one number, because a model can lower one of
them by moving work somewhere else. The results below show that happening.

## How the running time was measured

The plan was to read the time from each `hidden.json`. Those files, and the
original timings in `data/verification_py31*.json`, were produced on different
machines, and the gap between machines is larger than any difference we are
trying to measure. For `p001`:

| Source | Tests | Time |
| --- | ---: | ---: |
| original, our machine, Yujie's runner | 123 hidden | 1.267 s |
| refactored gpt, `outputs/p001/gpt/single/hidden.json` | 123 hidden | 5.112 s |
| original, `verification_py312.json`, Linux, Part 2 stand-in runner | 127 all | 1.853 s |

Reading the first and third rows as a before and after would report the
refactoring as about 2.8 times slower when nothing in the code changed, and the
third row does not even cover the same tests. We therefore rerun the hidden
suite for every version in one session on one machine, which takes about two
minutes for all 136 versions. A time is only recorded when the version passes
every hidden test, because a crash or a timeout makes the number meaningless.

## Results

| Version | Programs | Mean max CC | Mean nesting | Mean SLOC | Total smells | Passes all hidden tests |
|---|---:|---:|---:|---:|---:|---:|
| original | 34 | 11.29 | 3.85 | 39.0 | 14 | 34/34 |
| gpt | 34 | 6.62 | 2.74 | 41.2 | 17 | 34/34 |
| deepseek | 34 | 5.41 | 2.76 | 45.5 | 25 | 34/34 |
| qwen | 34 | 5.53 | 2.68 | 47.4 | 26 | 34/34 |

Averages hide how often a model helps, so we also count, for each metric, how
many of the 34 programs each model improved, left unchanged, or made worse
against that program's own original.

| Model | max CC | nesting | smells | SLOC |
|---|---|---|---|---|
| gpt | 29 / 4 / 1 | 21 / 13 / 0 | 8 / 17 / 9 | 7 / 3 / 24 |
| deepseek | 30 / 3 / 1 | 20 / 14 / 0 | 7 / 16 / 11 | 1 / 1 / 32 |
| qwen | 29 / 4 / 1 | 21 / 13 / 0 | 5 / 19 / 10 | 0 / 4 / 30 |

| Model | Programs timed | Median vs original | Slowest case |
|---|---:|---:|---:|
| gpt | 34 | 1.003x | 1.04x |
| deepseek | 34 | 1.004x | 1.20x |
| qwen | 34 | 1.005x | 1.18x |

**All three models reduce complexity, and all three pay for it.** Peak
cyclomatic complexity falls by roughly half, from 11.29 to between 5.41 and
6.62, and nesting improves in 20 to 21 of the 34 programs with no program made
worse. At the same time the code grows and collects smells. DeepSeek and Qwen
raise the total smell count from 14 to 25 and 26, and make 32 and 30 of the 34
programs longer. GPT is the most conservative of the three: it gains the least
complexity and does the least damage.

**No version broke behaviour.** Across the 102 refactored versions we ran 9,102
hidden tests and recorded zero failures, and running time is unchanged at a
median of 1.00 times the original.

This repeats the A1 result at a larger scale. One metric moving in the right
direction is not evidence that the code improved; here the metric that improved
and the metric that got worse move in opposite directions for the same edit,
which is the concern Shepperd raises about reading cyclomatic complexity on its
own [3].

## Limits

**The time measurement is not sensitive.** Every test runs the program as a new
process and these programs are small, so most of the wall time is Python
interpreter startup. Starting the interpreter on nothing takes about 9.2 ms on
our machine over 60 samples, so the 123 runs behind the `p001` figure account
for roughly 1.13 s of the 1.267 s measured, near 90%. The exact share moves
between runs. This measurement can detect a large slowdown but not a small one,
and the ratios near 1.00 should be read as "no large regression", not as
"identical performance".

**The smell counts depend on thresholds.** We use PyExamine's defaults and keep
a copy of the configuration in the repository, so a rerun gives the same numbers
even if the tool's defaults change later.

**The zero failure rate says something about the task, not only about the
models.** The refactoring prompt asks for simpler conditionals and smaller
functions while explicitly forbidding behaviour changes, and under it no model
broke a single one of 9,102 hidden tests. A loop condition that feeds test
failures back to the model would have nothing to feed back here. This is worth
weighing when the group chooses the task for A3.

**The subjects are small contest programs**, 16 to 82 lines with a median of 34,
not project code, which limits both the kinds of refactoring that are possible
and the size of any effect we can observe.

**Only the single-pass condition is scored.** The loop condition is planned for
A3.

## Artifacts

`scores/run_scoring.py` produces the scores, `scores/make_summary.py` builds the
tables above, `scores/scores.csv` holds one row per version, `scores/summary_table.md`
holds the tables, `scores/skipped.json` records runs with no usable code
(currently empty), and `scores/code_quality_config.yaml` pins the PyExamine
thresholds. `scores/README.md` documents how to reproduce the run.

**Contribution:** Chose the metrics after trying radon and PyExamine on sample
programs, wrote the scoring and summary scripts, reused Cris's complexity module
so the baseline is reproduced exactly, found that the recorded times came from
different machines and re-measured all 136 versions on one machine, measured the
interpreter startup share to establish what the time metric can detect, and
wrote this section.

**AI Use:** I used Claude Code to help write the scoring and summary scripts and
to draft this section. I ran everything myself, checked the original rows
against `data/subjects_meta.csv`, and verified the startup measurement and the
cross-machine timing difference before writing the text.

**References**

[1] Radon documentation. [Online]. Available: https://radon.readthedocs.io/en/latest/

[2] K. Shivashankar and A. Martini, "PyExamine: A comprehensive, un-opinionated
smell detection tool for Python," in *Proc. IEEE/ACM Int. Conf. Mining Software
Repositories (MSR)*, 2025.

[3] M. Shepperd, "A critique of cyclomatic complexity as a software metric,"
*Software Engineering Journal*, vol. 3, no. 2, pp. 30-36, 1988,
doi: 10.1049/sej.1988.0003.

[4] T. J. McCabe, "A complexity measure," *IEEE Trans. Softw. Eng.*, vol. SE-2,
no. 4, pp. 308-320, 1976, doi: 10.1109/TSE.1976.233837.
