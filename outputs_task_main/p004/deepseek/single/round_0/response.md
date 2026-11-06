```python
def _can_reduce_to_min(height, min_height):
    """Return True if height can be reduced to min_height by halving even values."""
    temp = height
    while temp > min_height:
        if temp % 2 == 0:
            temp //= 2
        else:
            return False
    return temp == min_height


def can_make_same_height(N, heights):
    min_height = min(heights)

    for height in heights:
        if height != min_height and not _can_reduce_to_min(height, min_height):
            return "NO"

    return "YES"


def read_input():
    N = int(input())
    heights = list(map(int, input().split()))
    return N, heights


def print_result(result):
    print(result)


def main():
    N, heights = read_input()
    result = can_make_same_height(N, heights)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved top-level input reading, computation, and output printing into `read_input()`, `main()`, and `print_result()` respectively, eliminating top-level logic and global variables.
- Added a private helper `_can_reduce_to_min()` to encapsulate the repeated halving/odd-check logic, removing the duplicated odd check inside `can_make_same_height()`.
- Preserved the public `can_make_same_height(N, heights)` signature and its exact return values (`"YES"`/`"NO"`).
- Wrapped program startup in `if __name__ == "__main__":` so the code only runs when executed directly, not on import.