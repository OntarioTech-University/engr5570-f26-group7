# New test inputs (A3, Part 4.1) · Cris

`data/new_inputs/pNNN.json` holds new, valid inputs for every program, in the
Part 4.1 format: `{"program_id": "p001", "inputs": [...]}`. Inputs only, no
expected outputs. **Never show them to a model.**

## Numbers

* 3,378 inputs for 34 programs: 100 for each program, except p018 (82) and p031 (96),
  where the original is too slow on the bigger inputs.
* Mix of sizes: 497 tiny, 1,209 small, 1,095 medium, 577 large.
* The original program runs on every input without an error or a timeout. This was
  checked one run at a time with the 5-second timeout (`scripts/verify_new_inputs.py`);
  the slowest single run is 1.4 s.

## How they were made

1. `scripts/input_generators.py` has one generator per problem (25), written from
   the problem's input format and limits. Problems with a guarantee are built so it
   holds: connected or strongly connected graphs (1253_F, 1361_E), edges that are
   new each day (1037_E), a real hidden permutation (1208_D), a unique answer date
   (260_B, checked, 19 candidates rejected), at least one question query (634_C).
   Each problem gets 140 seeded candidates in four sizes.
2. `scripts/build_new_inputs.py` runs every candidate on the original program and
   drops it if the original crashes (7), times out (149) or takes over 2 s (20).
   The 2 s margin keeps refactored versions from failing just because of the clock.
   The first 100 that remain, mixing all sizes, are kept.

## Extra check: are the originals really correct?

The build also runs an oracle on each input: accepted CodeContests Python 3
solutions (majority of up to 3), our own simple solutions for 6 easy problems
(`scripts/own_references.py`), or an answer checker for the three "print any
valid answer" problems (143_A, 663_A). 2,782 inputs were checked this way.

| Result | Programs |
| --- | --- |
| Original agrees with the oracle on every checked input | 27 |
| **Original is wrong on 52 of 100 inputs** | **p012** (roys_life_cycle, Qwen3-Coder 480B) |
| No oracle (cross-checked between the two programs where possible: p033 = p034 on all 100) | p008, p022, p030, p031, p033, p034 |

p012 passed all 101 CodeContests tests but is wrong when a coding streak runs
through a whole day into the next ones (for example, three days that are all `C`).
The CodeContests tests never had a full day of `C` (their days are at most 24 characters long, not 1,440), so they missed it.

## Notes for the comparison (Yujie)

* **p012:** the original itself has a bug, so a refactored version that differs from
  it may have *fixed* the bug, not broken it. Use `scripts/own_references.py` (ROYS)
  to tell the two apart.
* **143_A, 309_B, 663_A accept any valid answer.** A refactored version can print a
  different but correct answer. Treat differences there as "check by hand", or use
  the checkers in `build_new_inputs.py` (`check_143_A`, `check_663_A`).
* The inputs are about 41 MB, mostly p011/p012 (365 days x 1,440 characters) and
  p005. Each file is under 11 MB.

## Rebuild

```bash
python scripts/build_new_inputs.py --refs data/ref_solutions.json   # about 8 minutes
python scripts/verify_new_inputs.py
```
`data/ref_solutions.json` comes from the CodeContests `solutions` field (Python 3
only). The candidates are seeded, but which slow inputs are dropped can change a
little with machine load, so the committed files are the reference set.
