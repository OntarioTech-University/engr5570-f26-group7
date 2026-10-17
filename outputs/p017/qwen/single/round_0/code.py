import sys
from collections import Counter


def _read_problem_input(read_line):
    n_str = read_line()
    if not n_str:
        return None

    n = int(n_str)
    a = list(map(int, read_line().split()))
    m = int(read_line())
    return n, a, m


def _build_indexed_pairs(a, n):
    return [(a[i], i) for i in range(n)]


def _sort_for_max_sum_subsequence(indexed_a):
    indexed_a.sort(key=lambda pair: (-pair[0], pair[1]))


def _read_query(read_line):
    k, pos = map(int, read_line().split())
    return k, pos


def _build_subsequence(top_k_pairs):
    top_k_pairs.sort(key=lambda pair: pair[1])
    return [pair[0] for pair in top_k_pairs]


def _get_cached_subsequence(optimal_subs_cache, indexed_a, k):
    if k not in optimal_subs_cache:
        optimal_subs_cache[k] = _build_subsequence(indexed_a[:k])
    return optimal_subs_cache[k]


def _write_answer(value):
    sys.stdout.write(str(value) + '\n')


def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    try:
        # Fast I/O
        read_line = sys.stdin.readline

        problem_input = _read_problem_input(read_line)
        if problem_input is None:
            return
        n, a, m = problem_input

        # 1. Pair values with their original indices.
        indexed_a = _build_indexed_pairs(a, n)

        # 2. Sort to find the elements for the max-sum subsequence.
        _sort_for_max_sum_subsequence(indexed_a)

        # Cache to store computed optimal subsequences for each k.
        optimal_subs_cache = {}

        for _ in range(m):
            k, pos = _read_query(read_line)
            subsequence = _get_cached_subsequence(optimal_subs_cache, indexed_a, k)

            # pos is 1-based, so we use pos-1 for list indexing.
            _write_answer(subsequence[pos - 1])

    except (IOError, ValueError) as e:
        # Handle potential empty lines or format errors at the end of input
        pass


solve()
