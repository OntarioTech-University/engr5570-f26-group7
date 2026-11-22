# Buggy programs (A4, test-strength check)

`data/buggy/pNNN/pNNN_bKK.py` are copies of the 34 original programs with exactly ONE small
injected bug each. Yujie runs the hidden tests and the new inputs on them to see how many bugs
the tests catch (RQ1 reliability check).

## How to rebuild (deterministic)

    python scripts/inject_bugs.py --seed 5570 --per-program 15

Same seed and same Python version give byte-identical files (checked: two runs on Python 3.13, same SHA-256 over all mutants and an identical CSV). On Python 3.10 the CSV (which bugs, which changes) is identical, but `ast.unparse` formats some lines differently (for example `(a, b) = ...` instead of `a, b = ...`), so the files differ only in formatting. The committed files were made with Python 3.13.

## What is injected

| kind | change |
|---|---|
| relational | `<` <-> `<=`, `>` <-> `>=`, `==` <-> `!=` |
| arithmetic | `+` <-> `-`, `*` <-> `//` |
| logical | `and` <-> `or` |
| negation | `not x` -> `x` |
| constant | integer constant c -> c+1 or c-1 |
| augassign | `+=` <-> `-=` |

Each mutant is made on the AST and written with `ast.unparse`, so formatting and comments of the
original are not kept. The reference for every mutant is therefore `ast.unparse(original)`, which
passes the public tests for all 34 programs. Only one node changes per mutant.

## Selection and filtering

1. List every mutation site per program. 2. Shuffle with a per-program RNG (sha1 of seed + program id).
3. Round-robin over the kinds so each kind present in a program is used before any kind repeats.
4. Take candidates until 15 mutants per program are kept (cap). 5. Remove mutants that do not run
(syntax error, crash or 5 s timeout on any PUBLIC test input) and mutants identical to the reference.

A removed mutant is replaced by the next candidate in the shuffled round-robin order; the report keeps the removal counts.

## Files

- `data/buggy_programs.csv`: bug_id, program_id, problem_id, kind, change, lineno, code_path, tests_path
- `data/buggy_report.json`: counts (kept, removed by reason, by kind, by program, sites per program)
- `scripts/inject_bugs.py`: the generator
- `scripts/pilot_kill_rate.py`: stand-in pilot (hidden tests and new-input differential). Yujie's run replaces it.

## Known limits

- Some mutants are equivalent (the change does not alter behavior on any valid input), so a survived bug is not always a test weakness. Every surviving bug needs a manual look.
- Constants are the largest kind (they are the most common site), so overall rates lean toward constant bugs; per-kind rates are reported separately.
- p010 has only one mutation site (the original is tiny), p033 has 6.
- Mutants that crash or loop on public tests are removed, so bugs that the public tests would catch trivially are under-represented.
- The new-input check uses the original program as the reference (see A3 limits: p012 is already wrong; 143_A, 309_B, 663_A accept several answers).
