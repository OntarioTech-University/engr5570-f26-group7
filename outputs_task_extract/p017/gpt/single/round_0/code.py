import sys
from collections import Counter


def read_input(input):
    n_str = input()
    if not n_str:
        return None

    n = int(n_str)
    a = list(map(int, input().split()))
    m = int(input())
    return n, a, m


def sort_indexed_values(n, a):
    indexed_a = []
    for i in range(n):
        indexed_a.append((a[i], i))

    indexed_a.sort(key=lambda x: (-x[0], x[1]))
    return indexed_a


def read_query(input):
    return map(int, input().split())


def optimal_subsequence(indexed_a, k):
    top_k_pairs = indexed_a[:k]
    top_k_pairs.sort(key=lambda x: x[1])
    return [pair[0] for pair in top_k_pairs]


def answer_query(indexed_a, cache, k, pos):
    if k not in cache:
        cache[k] = optimal_subsequence(indexed_a, k)
    return cache[k][pos - 1]


def print_result(result):
    sys.stdout.write(str(result) + '\n')


def process_queries(input, m, indexed_a):
    optimal_subs_cache = {}
    for _ in range(m):
        k, pos = read_query(input)
        result = answer_query(indexed_a, optimal_subs_cache, k, pos)
        print_result(result)


def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    try:
        input = sys.stdin.readline
        data = read_input(input)
        if data is None:
            return

        n, a, m = data
        indexed_a = sort_indexed_values(n, a)
        process_queries(input, m, indexed_a)
    except (IOError, ValueError) as e:
        # Handle potential empty lines or format errors at the end of input
        pass


solve()
