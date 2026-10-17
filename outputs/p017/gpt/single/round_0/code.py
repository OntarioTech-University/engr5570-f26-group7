import sys
from collections import Counter


def _build_optimal_subsequence(indexed_a, k):
    """Return the top k elements in their original order."""
    top_k_pairs = indexed_a[:k]
    top_k_pairs.sort(key=lambda pair: pair[1])
    return [pair[0] for pair in top_k_pairs]


def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    try:
        input = sys.stdin.readline

        n_str = input()
        if not n_str:
            return
        n = int(n_str)

        a = list(map(int, input().split()))
        m = int(input())

        indexed_a = []
        for i in range(n):
            indexed_a.append((a[i], i))

        # Choose larger values first, breaking ties by earlier index.
        indexed_a.sort(key=lambda pair: (-pair[0], pair[1]))

        optimal_subs_cache = {}
        for _ in range(m):
            k, pos = map(int, input().split())

            if k not in optimal_subs_cache:
                optimal_subs_cache[k] = _build_optimal_subsequence(indexed_a, k)

            result = optimal_subs_cache[k][pos - 1]
            sys.stdout.write(str(result) + '\n')

    except (IOError, ValueError) as e:
        pass


solve()
