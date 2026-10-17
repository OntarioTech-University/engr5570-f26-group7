import sys


def read_input():
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))
    return n, ai


def initialize_dp(n):
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][i] = 0
    return dp


def fill_dp(dp, ai, n):
    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            if ai[i - 1] >= j:
                dp[i][j] = 1
            else:
                max_k = min(ai[i - 1] + 1, j)
                for k in range(i + 1, max_k):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])


def compute_total_cost(dp, n):
    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]
    return total_cost


def main():
    n, ai = read_input()
    dp = initialize_dp(n)
    fill_dp(dp, ai, n)
    total_cost = compute_total_cost(dp, n)
    print(total_cost)


if __name__ == "__main__":
    main()
