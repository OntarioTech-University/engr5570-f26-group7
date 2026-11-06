```python
from itertools import combinations


def find_optimal_subsequence(a, k):
    max_sum = 0
    optimal_subsequence = None
    for subsequence in _generate_subsequences(a, k):
        max_sum, optimal_subsequence = _consider_subsequence(
            subsequence, max_sum, optimal_subsequence
        )
    return optimal_subsequence


def main():
    _read_length()
    a = _read_sequence()
    m = _read_query_count()
    _process_queries(a, m)


def _read_length():
    return int(input())


def _read_sequence():
    return list(map(int, input().split()))


def _read_query_count():
    return int(input())


def _read_query():
    return map(int, input().split())


def _process_queries(a, m):
    for _ in range(m):
        _process_query(a)


def _process_query(a):
    k, pos = _read_query()
    optimal_subsequence = find_optimal_subsequence(a, k)
    answer = _element_at_position(optimal_subsequence, pos)
    _print_value(answer)


def _generate_subsequences(a, k):
    return combinations(a, k)


def _consider_subsequence(subsequence, max_sum, optimal_subsequence):
    subsequence_sum = sum(subsequence)
    if _is_better_subsequence(
        subsequence_sum, subsequence, max_sum, optimal_subsequence
    ):
        return subsequence_sum, subsequence
    return max_sum, optimal_subsequence


def _is_better_subsequence(candidate_sum, candidate, best_sum, best_subsequence):
    if candidate_sum > best_sum:
        return True
    if candidate_sum == best_sum:
        return best_subsequence is None or candidate < best_subsequence
    return False


def _element_at_position(sequence, pos):
    return sequence[pos - 1]


def _print_value(value):
    print(value)


if __name__ == "__main__":
    main()
```

- Extracted input operations into `_read_length`, `_read_sequence`, `_read_query_count`, and `_read_query` so parsing is isolated and input order/exceptions remain unchanged.
- Split query handling into `_process_queries` and `_process_query` to keep `main` short and make the per-query flow explicit.
- Kept `find_optimal_subsequence`’s public signature unchanged while delegating subsequence generation, summing/updating, and comparison to small helpers.
- Moved selection comparison into `_is_better_subsequence` to preserve the original tie-breaking logic in a dedicated function.
- Separated output into `_element_at_position` and `_print_value`, preserving the original evaluation order where indexing happens before printing.
- `_read_query` returns a lazy `map` object to preserve the original unpacking behavior for malformed query lines.