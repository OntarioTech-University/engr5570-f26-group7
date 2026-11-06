def read_test_case():
    """
    Reads a single test case input and returns the parsed values.
    """
    n, k = map(int, input().split())
    numbers = list(map(int, input().split()))
    return n, k, numbers


def count_set_bits(numbers):
    """
    Calculates the number of set bits (cheesecakes) for each number.
    """
    return [bin(num).count('1') for num in numbers]


def calculate_max_cakes(cheesecake_counts, k):
    """
    Sorts the cheesecake counts in descending order and sums the top K counts.
    """
    cheesecake_counts.sort(reverse=True)
    return sum(cheesecake_counts[:k])


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k, numbers = read_test_case()
        cheesecake_counts = count_set_bits(numbers)
        max_cakes = calculate_max_cakes(cheesecake_counts, k)
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


if __name__ == "__main__":
    main()
