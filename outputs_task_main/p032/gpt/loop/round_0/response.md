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

- Separated input, computation, and output into functions that exchange data through parameters and return values.
- Kept `main()` as the entry point and left the computation and its behavior unchanged.