from itertools import combinations


def find_optimal_subsequence(a, k):
    max_sum = 0
    optimal_subsequence = None

    for subsequence in combinations(a, k):
        optimal_subsequence, max_sum = _update_optimal_subsequence(
            optimal_subsequence, max_sum, subsequence
        )

    return optimal_subsequence


def _update_optimal_subsequence(optimal_subsequence, max_sum, subsequence):
    subsequence_sum = sum(subsequence)

    if subsequence_sum > max_sum:
        return subsequence, subsequence_sum

    if subsequence_sum == max_sum:
        if optimal_subsequence is None or subsequence < optimal_subsequence:
            return subsequence, max_sum

    return optimal_subsequence, max_sum


def _read_sequence():
    _ = int(input())
    return list(map(int, input().split()))


def _read_query_count():
    return int(input())


def _read_next_query():
    k, pos = map(int, input().split())
    return k, pos


def _print_subsequence_element(optimal_subsequence, pos):
    print(optimal_subsequence[pos - 1])


def _process_queries(a, m):
    for _ in range(m):
        k, pos = _read_next_query()
        optimal_subsequence = find_optimal_subsequence(a, k)
        _print_subsequence_element(optimal_subsequence, pos)


def main():
    a = _read_sequence()
    m = _read_query_count()
    _process_queries(a, m)


if __name__ == "__main__":
    main()
