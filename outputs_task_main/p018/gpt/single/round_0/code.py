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


def read_input():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    return a, m


def read_query():
    k, pos = map(int, input().split())
    return k, pos


def compute_result(a, k, pos):
    optimal_subsequence = find_optimal_subsequence(a, k)
    return optimal_subsequence[pos - 1]


def print_result(result):
    print(result)


def main():
    a, m = read_input()
    for _ in range(m):
        k, pos = read_query()
        result = compute_result(a, k, pos)
        print_result(result)


if __name__ == "__main__":
    main()
