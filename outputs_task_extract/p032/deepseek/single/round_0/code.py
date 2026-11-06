import sys

def read_input():
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))
    return n, ai

def create_dp(n):
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][i] = 0
    return dp

def update_dp_entry(dp, ai, i, j):
    if ai[i - 1] >= j:
        dp[i][j] = 1
        return

    limit = min(ai[i - 1] + 1, j)
    for k in range(i + 1, limit):
        candidate = dp[i][k] + dp[k][j]
        if candidate < dp[i][j]:
            dp[i][j] = candidate

def compute_dp(dp, ai, n):
    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            update_dp_entry(dp, ai, i, j)

def compute_total_cost(dp, n):
    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]
    return total_cost

def print_result(total_cost):
    print(total_cost)

def main():
    n, ai = read_input()
    dp = create_dp(n)
    compute_dp(dp, ai, n)
    total_cost = compute_total_cost(dp, n)
    print_result(total_cost)

if __name__ == "__main__":
    main()
