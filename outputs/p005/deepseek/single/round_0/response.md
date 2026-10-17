```python
def read_two_integers():
    """Read two space-separated integers from input."""
    return map(int, input().split())


def read_integer_list():
    """Read a line of space-separated integers into a list."""
    return list(map(int, input().split()))


def merge_sorted_arrays(arr1, arr2):
    """
    Merge two arrays sorted in non-increasing order using the two-pointer technique.
    """
    i = 0
    j = 0
    merged = []

    while i < len(arr1) and j < len(arr2):
        if arr1[i] >= arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1

    merged.extend(arr1[i:])
    merged.extend(arr2[j:])

    return merged


def solve():
    """
    This function handles a single test case.
    """
    try:
        n, m = read_two_integers()
    except (EOFError, ValueError):
        return

    arr1 = read_integer_list()
    arr2 = read_integer_list()

    merged_array = merge_sorted_arrays(arr1, arr2)

    print(*merged_array)


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        t = int(input())
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        pass


if __name__ == "__main__":
    main()
```

### Summary of changes

- **Extracted `read_two_integers()`** – Encapsulates reading and parsing two integers, reducing duplication and making the input step clearer.
- **Extracted `read_integer_list()`** – Encapsulates reading a line of integers into a list, improving readability and reuse.
- **Extracted `merge_sorted_arrays()`** – Moves the core merging logic into a dedicated, well-named function. This reduces the complexity of `solve()` and makes the algorithm easier to test and understand in isolation.
- **Replaced manual remaining-element loops with `extend()` and slicing** – Simplifies the code by using Python's built-in list operations, which are more concise and less error-prone while preserving identical behavior.
- **Removed redundant comments** – Kept only comments that add meaningful context, reducing visual noise and improving readability.