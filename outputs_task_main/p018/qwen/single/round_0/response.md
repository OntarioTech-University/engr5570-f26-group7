```python
from itertools import combinations


def find_optimal_subsequence(a, k):
    max_sum = 0
    optimal_subsequence = None
    for subsequence in combinations(a, k):
        subsequence_sum = sum(subsequence)
        if subsequence_sum > max_sum:
            max_sum = subsequence_sum
            optimal_subsequence = subsequence
        elif subsequence_sum == max_sum:
            if optimal_subsequence is None or subsequence < optimal_subsequence:
                optimal_subsequence = subsequence
    return optimal_subsequence


def read_int():
    return int(input())


def read_integers():
    return map(int, input().split())


def compute_selected_element(a, k, pos):
    optimal_subsequence = find_optimal_subsequence(a, k)
    return optimal_subsequence[pos - 1]


def print_answer(answer):
    print(answer)


def main():
    n = read_int()
    a = list(read_integers())
    m = read_int()

    for _ in range(m):
        k, pos = read_integers()
        answer = compute_selected_element(a, k, pos)
        print_answer(answer)


if __name__ == "__main__":
    main()
```

- Kept `find_optimal_subsequence` unchanged to preserve its public signature and exact behavior.
- Added `read_int` and `read_integers` helper functions to centralize repeated input parsing and avoid duplicated logic.
- Added `compute_selected_element` to isolate the per-query computation and return the value to print.
- Added `print_answer` to separate output side effects from orchestration logic.
- `main` now only coordinates input, computation, and output, while all data is passed via parameters and return values.
- The program entry point remains guarded by `if __name__ == "__main__":`, with no top-level execution logic or global mutable state.