import sys


def _read_input():
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))
    return n, ai


def _create_dp_table(n):
    INF = float('inf')
    return [[INF] * (n + 1) for _ in range(n + 1)]


def _set_base_costs(dp, n):
    for i in range(1, n + 1):
        dp[i][i] = 0


def _fill_dp_table(dp, ai, n):
    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            if ai[i - 1] >= j:
                dp[i][j] = 1
            else:
                for k in range(i + 1, min(ai[i - 1] + 1, j)):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])


def _compute_total_cost(dp, n):
    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]
    return total_cost


def _print_total_cost(total_cost):
    print(total_cost)


def main():
    n, ai = _read_input()
    dp = _create_dp_table(n)
    _set_base_costs(dp, n)
    _fill_dp_table(dp, ai, n)
    total_cost = _compute_total_cost(dp, n)
    _print_total_cost(total_cost)


if __name__ == "__main__":
    main()
