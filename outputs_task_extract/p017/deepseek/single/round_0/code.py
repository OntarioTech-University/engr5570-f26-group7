import sys
from collections import Counter

def _read_array(input_func, n):
    return list(map(int, input_func().split()))

def _build_indexed_values(values):
    return [(value, index) for index, value in enumerate(values)]

def _sort_for_optimal_selection(indexed_values):
    indexed_values.sort(key=lambda x: (-x[0], x[1]))

def _get_or_build_subsequence(k, indexed_a, cache):
    if k not in cache:
        top_k_pairs = indexed_a[:k]
        top_k_pairs.sort(key=lambda x: x[1])
        cache[k] = [pair[0] for pair in top_k_pairs]
    return cache[k]

def _process_queries(input_func, output_func, indexed_a, m):
    cache = {}
    for _ in range(m):
        k, pos = map(int, input_func().split())
        subsequence = _get_or_build_subsequence(k, indexed_a, cache)
        output_func(str(subsequence[pos - 1]) + '\n')

def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    try:
        input_func = sys.stdin.readline

        n_str = input_func()
        if not n_str:
            return
        n = int(n_str)

        a = _read_array(input_func, n)
        m = int(input_func())

        indexed_a = _build_indexed_values(a)
        _sort_for_optimal_selection(indexed_a)

        _process_queries(input_func, sys.stdout.write, indexed_a, m)

    except (IOError, ValueError):
        pass

solve()
