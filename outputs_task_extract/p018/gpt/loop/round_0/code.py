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


def _read_initial_values():
    n = int(input())
    a = list(map(int, input().split()))
    return a


def _read_query_count():
    return int(input())


def _read_query():
    k, pos = map(int, input().split())
    return k, pos


def _select_query_value(a, k, pos):
    optimal_subsequence = find_optimal_subsequence(a, k)
    return optimal_subsequence[pos-1]


def _print_query_value(value):
    print(value)


def main():
    a = _read_initial_values()
    m = _read_query_count()
    for _ in range(m):
        k, pos = _read_query()
        value = _select_query_value(a, k, pos)
        _print_query_value(value)


if __name__ == "__main__":
    main()
