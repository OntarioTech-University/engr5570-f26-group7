def read_case_parameters():
    """Read N and K from the current input line."""
    return map(int, input().split())


def read_numbers():
    """Read the list of numbers from the current input line."""
    return list(map(int, input().split()))


def calculate_cheesecake_counts(numbers):
    """Return the number of set bits for each number."""
    return [bin(num).count('1') for num in numbers]


def sort_counts_descending(counts):
    """Sort counts in descending order in place."""
    counts.sort(reverse=True)


def sum_top_counts(counts, k):
    """Return the sum of the first k counts."""
    return sum(counts[:k])


def print_result(answer):
    """Print the answer for one test case."""
    print(answer)


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k = read_case_parameters()
        numbers = read_numbers()
        cheesecake_counts = calculate_cheesecake_counts(numbers)
        sort_counts_descending(cheesecake_counts)
        max_cakes = sum_top_counts(cheesecake_counts, k)
        print_result(max_cakes)
    except (ValueError, EOFError):
        pass


def read_test_count():
    """Read the number of test cases."""
    return int(input())


def run_test_cases(test_count):
    """Run solve once for each test case."""
    for _ in range(test_count):
        solve()


def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        test_count = read_test_count()
        run_test_cases(test_count)
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    main()
