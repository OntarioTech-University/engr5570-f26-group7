```python
def _merge_sorted_arrays(arr1, arr2, n, m):
    """Merge up to n and m elements from two non-increasing arrays."""
    i = 0
    j = 0
    merged_array = []

    while i < n and j < m:
        if arr1[i] >= arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1

    while i < n:
        merged_array.append(arr1[i])
        i += 1

    while j < m:
        merged_array.append(arr2[j])
        j += 1

    return merged_array


def solve():
    """Handle a single test case."""
    try:
        n, m = map(int, input().split())
    except (EOFError, ValueError):
        return

    arr1 = list(map(int, input().split()))
    arr2 = list(map(int, input().split()))

    merged_array = _merge_sorted_arrays(arr1, arr2, n, m)
    print(*merged_array)


def main():
    """Handle the number of test cases."""
    try:
        t = int(input())
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        pass


if __name__ == "__main__":
    main()
```

- Extracted the merge logic into a private helper so `solve()` focuses on input and output.
- Kept the merge loops and exception handling unchanged to preserve behavior.