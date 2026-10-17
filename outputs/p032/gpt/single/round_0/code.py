import sys


def _build_costs(n, ai):
    inf = float('inf')
    dp = [[inf] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][i] = 0

    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            if ai[i - 1] >= j:
                dp[i][j] = 1
                continue

            for k in range(i + 1, min(ai[i - 1] + 1, j)):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])

    return dp


def _sum_costs(dp, n):
    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]
    return total_cost


def main():
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))

    dp = _build_costs(n, ai)
    print(_sum_costs(dp, n))


if __name__ == "__main__":
    main()
