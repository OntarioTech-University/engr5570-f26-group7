import sys
from collections import Counter


def _read_problem_size(read_line):
    n_str = read_line()
    if not n_str:
        return None
    return int(n_str)


def _read_values(read_line):
    return list(map(int, read_line().split()))


def _read_query_count(read_line):
    return int(read_line())


def _pair_values_with_indices(values, n):
    indexed_values = []
    for i in range(n):
        indexed_values.append((values[i], i))
    return indexed_values


def _sort_pairs_for_selection(indexed_values):
    indexed_values.sort(key=lambda x: (-x[0], x[1]))


def _read_query(read_line):
    k, pos = map(int, read_line().split())
    return k, pos


def _build_cached_subsequence(k, indexed_values, optimal_subs_cache):
    if k not in optimal_subs_cache:
        top_k_pairs = indexed_values[:k]
        top_k_pairs.sort(key=lambda x: x[1])
        optimal_subs_cache[k] = [pair[0] for pair in top_k_pairs]
    return optimal_subs_cache[k]


def _select_answer(subsequence, pos):
    return subsequence[pos - 1]


def _write_answer(result):
    sys.stdout.write(str(result) + '\n')


def _process_queries(m, read_line, indexed_values):
    optimal_subs_cache = {}
    for _ in range(m):
        k, pos = _read_query(read_line)
        subsequence = _build_cached_subsequence(k, indexed_values, optimal_subs_cache)
        result = _select_answer(subsequence, pos)
        _write_answer(result)


def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    try:
        read_line = sys.stdin.readline

        n = _read_problem_size(read_line)
        if n is None:
            return

        values = _read_values(read_line)
        m = _read_query_count(read_line)

        indexed_values = _pair_values_with_indices(values, n)
        _sort_pairs_for_selection(indexed_values)

        _process_queries(m, read_line, indexed_values)

    except (IOError, ValueError) as e:
        pass


solve()
