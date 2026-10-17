import sys
from collections import Counter

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

        indexed_a = create_indexed_pairs(a)
        indexed_a.sort(key=lambda x: (-x[0], x[1]))

        optimal_subs_cache = {}

        for _ in range(m):
            k, pos = map(int, input().split())
            
            if k not in optimal_subs_cache:
                optimal_subs_cache[k] = compute_optimal_subsequence(indexed_a, k)
            
            result = optimal_subs_cache[k][pos - 1]
            sys.stdout.write(str(result) + '\n')

    except (IOError, ValueError) as e:
        pass


def create_indexed_pairs(values):
    """
    Pair each value with its original index.
    
    Args:
        values: List of integers
        
    Returns:
        List of tuples (value, index)
    """
    return [(value, index) for index, value in enumerate(values)]


def compute_optimal_subsequence(sorted_pairs, k):
    """
    Compute the optimal subsequence of length k from sorted pairs.
    
    Args:
        sorted_pairs: List of (value, index) tuples sorted by value descending, then index ascending
        k: Length of subsequence to compute
        
    Returns:
        List of values forming the optimal subsequence
    """
    top_k_pairs = sorted_pairs[:k]
    top_k_pairs.sort(key=lambda x: x[1])
    return [pair[0] for pair in top_k_pairs]


solve()
