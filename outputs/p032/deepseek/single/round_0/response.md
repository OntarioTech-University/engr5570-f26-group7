```python
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
```

- Extracted `read_input` to separate input parsing from the main logic, improving readability and testability.
- Extracted `initialize_dp` to isolate the base-case setup of the DP table, making the initialization logic clearer.
- Extracted `fill_dp` to encapsulate the dynamic programming fill step, reducing the nesting depth in `main` and giving the core algorithm a descriptive name.
- Extracted `compute_total_cost` to separate the final summation from the DP computation, making the overall flow easier to follow.
- Renamed the inner loop bound variable to `max_k` to clarify its purpose without changing behavior.