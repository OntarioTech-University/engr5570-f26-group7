# A2 · Study Subjects and Test Split (Cris)

## Study subjects

**Source.** Our subjects are AI-written Python programs from the replication package of
Zhu, Tsantalis and Rigby [1]. In their Experiment 1, five LLMs (Gemini 2.5 Pro,
Llama 3.3 70B, DeepSeek-Coder-V2 16B, Qwen3-Coder 30B and Qwen3-Coder 480B) solved 90
CodeContests problems [2] under a zero-shot and a few-shot prompt, and the authors
detected smells in the answers with PyExamine [3]. We reuse these programs for two
reasons. First, their smells are already documented by an independent study, so we
start from code that is known to need cleaning. Second, every CodeContests problem
comes with many input and output tests, so behaviour can be checked automatically
and, unlike the sqlite-utils pilot in A1, we can hold back tests from the model.

**Matching programs to tests.** The package stores the full problem text next to each
program. We found every problem in CodeContests (revision 802411c, the one the
ASE scripts use) by exact text match, and linked each program to its PyExamine
report through its snippet file. All matches were exact.

**Public and hidden tests.** For each program, the CodeContests public tests (the
examples in the problem statement) are the *public* tests, which the refactoring loop
may show to the model. The private and generated tests are the *hidden* tests, which
are only run on the final code. We removed one hidden test that repeated a public
test, so the hidden suite never contains a test the model has seen.

**Selection.** Starting from the 810 programs of the five paper models, we kept a
program only if (1) it is Python 3 that reads standard input, (2) its problem has
both public and hidden tests, (3) the original passes **every** public, private and
generated test, so any later failure is caused by the refactoring, (4) its slowest test
runs in under 1 second, five times below our 5-second timeout, and (5) it has
something to clean up: a PyExamine smell from [1], a block with cyclomatic
complexity above 10 [4], nesting of 4 or more levels, or a block of 20 or more lines
of code. We then kept one program per problem and model, and at most two per
problem. This left **34 programs** for 25 problems (Table X). All 34 pass all their
tests under Python 3.11, 3.12 and 3.13.

| Step | Programs left |
| --- | ---: |
| Programs of the 5 paper models, 2 prompt conditions | 810 |
| Python 3 reading stdin, with public and hidden tests, no duplicates | 606 |
| Original passes all tests | 184 |
| Slowest test under 1 s | 183 |
| Has something to clean up | 48 |
| One per problem and model, at most two per problem | **34** |

| | 34 programs |
| --- | --- |
| Source model | Qwen3-Coder 480B 13, Gemini 2.5 Pro 12, Llama 3.3 70B 6, DeepSeek-Coder-V2 16B 3 |
| Difficulty | easy 12, middle 16, hard 6 |
| Tests | 70 public, 3,034 hidden (701 private, 2,333 generated) |
| Size | 16 to 82 lines of code, median 34 |

**What we learned about the dataset.** Checking the package gave three facts that
matter for anyone reusing it. (a) The five models did not solve one shared set of
problems: the two models run locally (DeepSeek-Coder-V2 16B and Qwen3-Coder 30B)
used a different sample, and only 41 problems overlap, so the package covers 139
distinct problems. (b) Only 183 of the 810 programs pass all their tests; the paper
studies smells whether or not a solution is correct, so correctness has to be
checked again before refactoring. (c) Some answers are empty (58) or not Python
(101), and the zero-shot answers of Qwen3-Coder 30B have no result file that links
them to problems.

**Limits.** The programs are short contest solutions, not project code, so the kinds of
refactoring they allow are limited. Exact output comparison removes problems with
several correct answers. The source models are uneven (Qwen3-Coder 30B has no program
left), and 16 of the 34 come from Qwen or DeepSeek models, the same families as two of
our refactoring models; we keep the source model in every analysis. Our "something
to clean up" rule is a filter with common thresholds, not a quality measurement.

**Artifacts.** `data/programs.csv`, `data/programs/`, `data/tests/`,
`data/subjects_meta.csv`, `data/dataset_stats.json`, and the scripts
`scripts/build_subjects.py` (rebuilds the set from the two public sources with a fixed
seed) and `scripts/verify_subjects.py` (checks the format and reruns all tests).

**Contribution:** Downloaded and checked the ASE replication package and CodeContests,
matched every program to its problem, tests and smells, defined and applied the
selection rules, split the tests, wrote the build and verification scripts, verified
all 34 originals on three Python versions, and wrote this section.

**AI Use:** I used Claude to help write the build and verification scripts and to
draft this section. I checked the counts against the script output and the paper,
ran the verification myself, and edited the text.

**References**

[1] Y. Zhu, N. Tsantalis, and P. C. Rigby, "Understanding the code and architectural
smells generated by LLMs and autonomous agents," in *Proc. IEEE/ACM Int. Conf. Automated
Software Engineering (ASE)*, 2026, doi: 10.1145/3832783.3834413. Replication package:
doi: 10.5281/zenodo.19245562.

[2] Y. Li *et al.*, "Competition-level code generation with AlphaCode," *Science*,
vol. 378, no. 6624, pp. 1092-1097, 2022, doi: 10.1126/science.abq1158.

[3] K. Shivashankar and A. Martini, "PyExamine: A comprehensive, un-opinionated smell
detection tool for Python," in *Proc. IEEE/ACM Int. Conf. Mining Software Repositories
(MSR)*, 2025.

[4] T. J. McCabe, "A complexity measure," *IEEE Trans. Softw. Eng.*, vol. SE-2, no. 4,
pp. 308-320, 1976, doi: 10.1109/TSE.1976.233837.
