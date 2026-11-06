def _read_test_count():
    """Read the number of test cases."""
    return int(input())


def _read_test_case():
    """Read a single test case and return the values needed for computation."""
    _n, k = map(int, input().split())
    numbers = list(map(int, input().split()))
    return k, numbers


def _compute_max_cakes(numbers, k):
    """Compute the maximum number of cheesecakes for one test case."""
    cheesecake_counts = [bin(num).count('1') for num in numbers]
    cheesecake_counts.sort(reverse=True)
    return sum(cheesecake_counts[:k])


def _print_result(max_cakes):
    """Print the final answer for one test case."""
    print(max_cakes)


def _solve_case():
    """Run the input, computation, and output steps for one test case."""
    k, numbers = _read_test_case()
    max_cakes = _compute_max_cakes(numbers, k)
    _print_result(max_cakes)


def _suppress_input_errors(operation):
    """Run operation and suppress the same input-related errors as before."""
    try:
        operation()
    except (ValueError, EOFError):
        pass


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    _suppress_input_errors(_solve_case)


def main():
    """
    Main function to handle multiple test cases.
    """
    def _run_all_cases():
        t = _read_test_count()
        for _ in range(t):
            solve()

    _suppress_input_errors(_run_all_cases)


if __name__ == "__main__":
    main()
