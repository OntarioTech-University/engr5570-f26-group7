```python
def _read_test_case_count():
    """Read the number of test cases."""
    return int(input())


def _read_case_dimensions():
    """Read the sizes of the two arrays for one test case."""
    n, m = map(int, input().split())
    return n, m


def _read_integer_array():
    """Read one space-separated array of integers."""
    return list(map(int, input().split()))


def _append_remaining_elements(source, index, limit, destination):
    """Append remaining elements from source[index:limit] to destination."""
    while index < limit:
        destination.append(source[index])
        index += 1


def _merge_arrays(arr1, arr2, n, m):
    """Merge two sorted arrays using the original two-pointer logic."""
    i = 0  # Pointer for arr1
    j = 0  # Pointer for arr2
    merged_array = []

    # Merge the two arrays using the two-pointer technique
    while i < n and j < m:
        # Since arrays are sorted in non-increasing order,
        # we pick the larger element to maintain the order.
        if arr1[i] >= arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1

    # Append any remaining elements from either array
    _append_remaining_elements(arr1, i, n, merged_array)
    _append_remaining_elements(arr2, j, m, merged_array)

    return merged_array


def _print_array(values):
    """Print the final merged array with space-separated values."""
    print(*values)


def solve():
    """
    This function handles a single test case.
    """
    # Read the sizes of the two arrays
    try:
        n, m = _read_case_dimensions()
    except (EOFError, ValueError):
        return  # Stop if there's no more input

    # Read the two sorted arrays
    arr1 = _read_integer_array()
    arr2 = _read_integer_array()

    # Perform the main computation
    merged_array = _merge_arrays(arr1, arr2, n, m)

    # Print the final merged array with space-separated values
    _print_array(merged_array)


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        # Read the number of test cases
        t = _read_test_case_count()
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        # Handles cases with no input or invalid input
        pass


if __name__ == "__main__":
    main()
```

- Introduced private input helpers (`_read_test_case_count`, `_read_case_dimensions`, `_read_integer_array`) to isolate input reading while keeping `solve()` and `main()` signatures unchanged.
- Moved the core merge logic into `_merge_arrays()` so computation is separated from input/output and data is passed via parameters and return values.
- Added `_print_array()` to centralize output formatting and separate printing from computation.
- Replaced the duplicated “append remaining elements” loops with the shared helper `_append_remaining_elements()`.
- Preserved the original exception-handling structure and scopes so runtime behavior, outputs, return values, side effects, and exception types remain unchanged.
- Kept all executable logic inside functions and retained only the `if __name__ == "__main__":` guard at the top level.