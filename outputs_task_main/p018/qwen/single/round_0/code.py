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


def read_int():
    return int(input())


def read_integers():
    return map(int, input().split())


def compute_selected_element(a, k, pos):
    optimal_subsequence = find_optimal_subsequence(a, k)
    return optimal_subsequence[pos - 1]


def print_answer(answer):
    print(answer)


def main():
    n = read_int()
    a = list(read_integers())
    m = read_int()

    for _ in range(m):
        k, pos = read_integers()
        answer = compute_selected_element(a, k, pos)
        print_answer(answer)


if __name__ == "__main__":
    main()
