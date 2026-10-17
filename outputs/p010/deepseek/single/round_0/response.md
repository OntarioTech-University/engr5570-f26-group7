Here's the refactored version of the code:

```python
def count_set_bits(number):
    """
    Count the number of set bits (1s) in the binary representation of a number.
    """
    return bin(number).count('1')


def read_numbers():
    """
    Read a line of space-separated integers from input.
    """
    return list(map(int, input().split()))


def get_max_cheesecakes(numbers, k):
    """
    Calculate the maximum number of cheesecakes by selecting K numbers
    with the highest set bit counts.
    """
    cheesecake_counts = [count_set_bits(num) for num in numbers]
    cheesecake_counts.sort(reverse=True)
    return sum(cheesecake_counts[:k])


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k = read_numbers()
        numbers = read_numbers()
        max_cakes = get_max_cheesecakes(numbers, k)
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
```

**Changes made:**

- **Extracted `count_set_bits` function**: Moved the bit-counting logic into a named function to make the operation's purpose clearer and reusable.
- **Extracted `read_numbers` function**: Consolidated the input parsing logic into a single function, reducing duplication and making the code more maintainable.
- **Extracted `get_max_cheesecakes` function**: Separated the core business logic (counting bits, sorting, and summing) from the I/O operations in `solve()`, making the algorithm easier to understand and test in isolation.
- **Removed excessive comments**: Eliminated verbose inline comments that explained obvious operations, keeping only essential documentation in docstrings.
- **Simplified `solve()` function**: Reduced the function to a clear sequence of steps: read input, process data, output result.