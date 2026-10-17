from itertools import combinations


def _should_replace_current_best(candidate, candidate_sum, current_best, current_best_sum):
    if candidate_sum > current_best_sum:
        return True
    if candidate_sum == current_best_sum:
        return current_best is None or candidate < current_best
    return False


def find_optimal_subsequence(a, k):
    max_sum = 0
    optimal_subsequence = None

    for subsequence in combinations(a, k):
        subsequence_sum = sum(subsequence)
        if _should_replace_current_best(
            subsequence,
            subsequence_sum,
            optimal_subsequence,
            max_sum
        ):
            max_sum = subsequence_sum
            optimal_subsequence = subsequence

    return optimal_subsequence


def main():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    for _ in range(m):
        k, pos = map(int, input().split())
        optimal_subsequence = find_optimal_subsequence(a, k)
        print(optimal_subsequence[pos-1])


if __name__ == "__main__":
    main()
