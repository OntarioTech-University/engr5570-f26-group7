def read_test_count():
    return int(input())


def read_case():
    n, k = map(int, input().split())
    numbers = list(map(int, input().split()))
    return n, k, numbers


def calculate_max_cakes(numbers, k):
    cheesecake_counts = [bin(num).count('1') for num in numbers]
    cheesecake_counts.sort(reverse=True)
    return sum(cheesecake_counts[:k])


def print_answer(max_cakes):
    print(max_cakes)


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k, numbers = read_case()
        max_cakes = calculate_max_cakes(numbers, k)
        print_answer(max_cakes)
    except (ValueError, EOFError):
        pass


def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        t = read_test_count()
        for _ in range(t):
            solve()
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    main()
