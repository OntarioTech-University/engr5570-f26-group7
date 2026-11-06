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


def read_ints():
    return list(map(int, input().split()))


def read_initial_data():
    n = int(input())
    a = read_ints()
    m = int(input())
    return n, a, m


def read_query():
    return read_ints()


def compute_answer(a, k, pos):
    optimal_subsequence = find_optimal_subsequence(a, k)
    return optimal_subsequence[pos - 1]


def print_answer(answer):
    print(answer)


def main():
    n, a, m = read_initial_data()
    for _ in range(m):
        k, pos = read_query()
        answer = compute_answer(a, k, pos)
        print_answer(answer)


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_initial_data`, `read_query`, and a shared `read_ints` helper to remove duplicated line parsing.
- Extracted the per-query computation into `compute_answer`, which delegates to the unchanged public `find_optimal_subsequence`.
- Extracted output printing into `print_answer`.
- `main` now only orchestrates the flow by calling these functions, passing data through parameters and return values.
- No logic runs at the top level except the `if __name__ == "__main__":` guard, and no global variables are used.
- Runtime behavior, public interfaces, and error handling remain unchanged.