```python
def read_int_pair():
    """Read two space-separated integers from standard input."""
    return tuple(map(int, input().split()))


def read_numbers():
    """Read a line of space-separated integers into a list."""
    return list(map(int, input().split()))


def read_test_case_count():
    """Read a single integer from standard input."""
    return int(input())


def count_set_bits(number):
    """Return the number of 1 bits in the binary representation of number."""
    return bin(number).count('1')


def compute_cheesecake_counts(numbers):
    """Map each number to its set-bit count."""
    return [count_set_bits(number) for number in numbers]


def sort_descending(values):
    """Return a new list with values sorted in descending order."""
    return sorted(values, reverse=True)


def sum_top_k(values, k):
    """Return the sum of the first k elements in values."""
    return sum(values[:k])


def print_result(result):
    """Print the result for a test case."""
    print(result)


def solve():
    """Solve a single test case for the Monk and Cakes problem."""
    try:
        n, k = read_int_pair()
        numbers = read_numbers()
        cheesecake_counts = compute_cheesecake_counts(numbers)
        cheesecake_counts = sort_descending(cheesecake_counts)
        max_cakes = sum_top_k(cheesecake_counts, k)
        print_result(max_cakes)
    except (ValueError, EOFError):
        pass


def main():
    """Main function to handle multiple test cases."""
    try:
        t = read_test_case_count()
        for _ in range(t):
            solve()
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_int_pair`, `read_numbers`, and `read_test_case_count` to isolate I/O concerns.
- Extracted bit-count computation into `count_set_bits` and `compute_cheesecake_counts` for clarity and reuse.
- Extracted sorting and top-K summation into `sort_descending` and `sum_top_k` to separate transformation steps.
- Extracted output printing into `print_result` to keep side effects explicit.
- Preserved `solve` and `main` signatures and exception handling behavior exactly.