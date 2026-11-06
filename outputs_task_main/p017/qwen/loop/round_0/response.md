```python
import sys
from collections import Counter


def read_initial_input(read_line):
    n_str = read_line()
    if not n_str:
        return None

    n = int(n_str)
    a = list(map(int, read_line().split()))
    m = int(read_line())
    return n, a, m


def build_indexed_candidates(a, n):
    indexed_a = []
    for i in range(n):
        indexed_a.append((a[i], i))

    indexed_a.sort(key=lambda x: (-x[0], x[1]))
    return indexed_a


def read_query(read_line):
    k, pos = map(int, read_line().split())
    return k, pos


def get_optimal_subsequence(k, indexed_a, optimal_subs_cache):
    if k not in optimal_subs_cache:
        top_k_pairs = indexed_a[:k]
        top_k_pairs.sort(key=lambda x: x[1])
        optimal_subs_cache[k] = [pair[0] for pair in top_k_pairs]

    return optimal_subs_cache[k]


def compute_answer(indexed_a, optimal_subs_cache, k, pos):
    subsequence = get_optimal_subsequence(k, indexed_a, optimal_subs_cache)
    return subsequence[pos - 1]


def write_result(write_line, result):
    write_line(str(result) + '\n')


def process_queries(m, indexed_a, read_line, write_line):
    optimal_subs_cache = {}

    for _ in range(m):
        k, pos = read_query(read_line)
        result = compute_answer(indexed_a, optimal_subs_cache, k, pos)
        write_result(write_line, result)


def main():
    try:
        read_line = sys.stdin.readline
        write_line = sys.stdout.write

        initial_input = read_initial_input(read_line)
        if initial_input is None:
            return

        n, a, m = initial_input
        indexed_a = build_indexed_candidates(a, n)
        process_queries(m, indexed_a, read_line, write_line)

    except (IOError, ValueError) as e:
        pass


def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    main()


if __name__ == "__main__":
    main()
```

- Removed the unconditional top-level `solve()` call and replaced it with `main()` under `if __name__ == "__main__":`, so importing the module no longer executes program logic.
- Kept `solve()` with its original name, signature, and docstring, delegating to `main()` to preserve the existing public interface.
- Extracted initial input parsing into `read_initial_input()`, preserving the original early return when the first line is empty.
- Moved the core sorting/index preparation into `build_indexed_candidates()` to separate the main computation from input handling.
- Split query processing into focused helpers: `read_query()` for input, `get_optimal_subsequence()` for cached computation, `compute_answer()` for selecting the requested element, and `write_result()` for output.
- Kept the same exception-handling behavior: only `IOError` and `ValueError` are caught and ignored; other exceptions, such as `IndexError`, still propagate.
- Left the unused `Counter` import unchanged to avoid altering the module namespace or import-time behavior.