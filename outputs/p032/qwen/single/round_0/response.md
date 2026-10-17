```python
import sys


def _read_input():
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))
    return n, ai


def _create_dp_table(n):
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][i] = 0

    return dp


def _update_dp_cell(dp, ai, i, j):
    if ai[i - 1] >= j:
        dp[i][j] = 1
        return

    for k in range(i + 1, min(ai[i - 1] + 1, j)):
        dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])


def _fill_dp_table(dp, ai, n):
    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            _update_dp_cell(dp, ai, i, j)


def _compute_total_cost(dp, n):
    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]
    return total_cost


def main():
    n, ai = _read_input()
    dp = _create_dp_table(n)
    _fill_dp_table(dp, ai, n)
    total_cost = _compute_total_cost(dp, n)
    print(total_cost)


if __name__ == "__main__":
    main()
```

- Extracted input parsing into `_read_input()` so `main()` starts with a clear, high-level workflow while preserving the original read order and exception behavior.
- Moved DP table creation and diagonal base-case initialization into `_create_dp_table()` to separate setup from the DP transition logic.
- Extracted the per-cell DP transition into `_update_dp_cell()` to reduce nesting in the fill loop and make the direct-reachability case explicit via early return.
- Kept the original in-place updates to `dp[i][j]` inside the transition loop to preserve the exact mutation behavior of the original implementation.
- Extracted the final summation into `_compute_total_cost()` while preserving the original nested-loop order and accumulation behavior.
- Left the public interface unchanged: `main()` retains the same signature and the script entry point remains identical.