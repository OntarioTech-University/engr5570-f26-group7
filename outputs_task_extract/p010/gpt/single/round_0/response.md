```python
def read_case_header():
    """Read the total number of numbers and the number to choose."""
    n, k = map(int, input().split())
    return n, k


def read_numbers():
    """Read the numbers for one test case."""
    return list(map(int, input().split()))


def count_cheesecakes(numbers):
    """Count the set bits in each number."""
    return [bin(num).count('1') for num in numbers]


def sort_counts(cheesecake_counts):
    """Sort cheesecake counts in descending order."""
    cheesecake_counts.sort(reverse=True)


def sum_top_counts(cheesecake_counts, k):
    """Sum the first k counts."""
    return sum(cheesecake_counts[:k])


def print_answer(max_cakes):
    """Print the answer for one test case."""
    print(max_cakes)


def read_test_case_count():
    """Read the number of test cases."""
    return int(input())


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k = read_case_header()
        numbers = read_numbers()
        cheesecake_counts = count_cheesecakes(numbers)
        sort_counts(cheesecake_counts)
        max_cakes = sum_top_counts(cheesecake_counts, k)
        print_answer(max_cakes)
    except (ValueError, EOFError):
        pass


def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        t = read_test_case_count()
        for _ in range(t):
            solve()
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    main()
```

- Moved input reading, each computation step, and output printing into small, single-purpose functions.
- Kept `solve()` and `main()` signatures, execution order, and exception handling unchanged.