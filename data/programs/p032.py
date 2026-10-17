import sys

def main():
    # Read input
    n = int(sys.stdin.readline().strip())
    ai = list(map(int, sys.stdin.readline().strip().split()))
    
    # Initialize dp array with infinity
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(n + 1)]
    
    # Base case: cost to travel from i to i is 0
    for i in range(1, n + 1):
        dp[i][i] = 0
    
    # Fill the dp array using dynamic programming
    for i in range(n - 1, 0, -1):
        for j in range(i + 1, n + 1):
            if ai[i - 1] >= j:
                dp[i][j] = 1
            else:
                for k in range(i + 1, min(ai[i - 1] + 1, j)):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
    
    # Compute the sum of all values ρi, j
    total_cost = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total_cost += dp[i][j]
    
    print(total_cost)

if __name__ == "__main__":
    main()
