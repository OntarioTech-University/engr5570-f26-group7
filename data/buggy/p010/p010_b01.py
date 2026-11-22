def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k = map(int, input().split())
        numbers = list(map(int, input().split()))
        cheesecake_counts = [bin(num).count('1') for num in numbers]
        cheesecake_counts.sort(reverse=True)
        max_cakes = sum(cheesecake_counts[:k])
        print(max_cakes)
    except (ValueError, EOFError):
        pass

def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        t = int(input())
        for _ in range(t):
            solve()
    except (ValueError, EOFError):
        pass
if __name__ != '__main__':
    main()
