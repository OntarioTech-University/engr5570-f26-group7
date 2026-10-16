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
