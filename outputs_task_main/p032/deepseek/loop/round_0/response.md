```python
import sys

def read_input():
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))
    return n, ai

def compute_total_cost(n, ai):
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][i] = 0

    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            if ai[i - 1] >= j:
                dp[i][j] = 1
            else:
                for k in range(i + 1, min(ai[i - 1] + 1, j)):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])

    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]

    return total_cost

def print_output(total_cost):
    print(total_cost)

def main():
    n, ai = read_input()
    total_cost = compute_total_cost(n, ai)
    print_output(total_cost)

if __name__ == "__main__":
    main()
```

- Moved input reading into `read_input()`, returning the parsed values.
- Moved the dynamic programming computation and summation into `compute_total_cost()`, returning the final result.
- Moved output printing into `print_output()`.
- `main()` now only orchestrates the three steps, with no logic at the top level of the file.
- Removed the local `INF` from `main()` and placed it inside `compute_total_cost()` to avoid any global or shared state.
- No duplicated code was present; all original behavior, outputs, and exceptions are preserved exactly.