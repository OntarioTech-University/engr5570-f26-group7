# A3 · New Test Inputs (Cris)

**What we did:** In A2, all 102 refactored versions passed every CodeContests test, but those tests may miss behaviour changes. Following the professor's first suggestion, we built a new set of valid inputs for the 34 programs, so Yujie can run each original and refactored version on the same inputs and compare their outputs.

**How we did it:** We wrote one input generator per problem (25 generators) that follows the input format and limits in each problem statement, `scripts/input_generators.py`. Inputs for problems with a guarantee, such as a connected graph or a unique answer, are built so that the guarantee holds. For each problem we generated 140 seeded candidates in four sizes. `scripts/build_new_inputs.py` ran every candidate on the original program and removed those where it crashed, timed out, or took more than 2 seconds, then kept up to 100 per program. As an extra check, it compared the original's output with an oracle: accepted CodeContests solutions, our own simple solutions for six easy problems, or an answer checker for problems that accept several answers. `scripts/verify_new_inputs.py` confirmed the interface format and re-ran every original with the 5-second timeout. The files are in `data/new_inputs/`.

**Results:**

| | Value |
| --- | --- |
| New inputs | 3,378 (100 per program; p018: 82, p031: 96) |
| Sizes (tiny / small / medium / large) | 497 / 1,209 / 1,095 / 577 |
| Candidates removed (crash / timeout / over 2 s) | 7 / 149 / 20 |
| Inputs checked against an oracle | 2,782, covering 28 programs |
| Originals that disagree with the oracle | 1 (p012: wrong on 52 of 100) |

p012 (Qwen3-Coder 480B) passed all 101 CodeContests tests, but it gives a wrong answer when a coding streak covers a whole day and continues into the next days.

**What the results mean:** The CodeContests tests are weaker than they looked. They missed a real bug in a program we had treated as correct, so the A2 result "all tests passed" is not enough to say behaviour was preserved. This supports RQ2, and Yujie's output comparison will show whether the refactorings changed behaviour on these new inputs.

**Problems, limits and next steps:** Six programs have no oracle, so we only know that their originals run, not that they are correct; p033 and p034 do agree with each other on all 100 inputs. Problems 143_A, 309_B and 663_A accept several correct answers, so a different output there is not always a bug. For p012, a difference from the original may be a bug fix. The generators are random rather than targeted, so rare edge cases may still be missing; for A4 we could add inputs aimed at the paths each refactoring changed.

**Contribution:** I wrote the input generators, the build and verification scripts and the oracle checks, built the 3,378 inputs, found the p012 bug, and wrote this section.

**AI Use:** I used Claude to help write the generators and scripts and to draft this section. I checked the generators against the problem statements, ran the verification myself, and confirmed the p012 bug by hand.

**References**

[1] Y. Li *et al.*, "Competition-level code generation with AlphaCode," *Science*, vol. 378, no. 6624, pp. 1092–1097, 2022, doi: 10.1126/science.abq1158. (CodeContests dataset and its accepted solutions.)
