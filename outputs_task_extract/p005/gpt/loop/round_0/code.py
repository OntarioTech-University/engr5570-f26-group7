def _read_sizes():
    try:
        n, m = map(int, input().split())
    except (EOFError, ValueError):
        return None
    return n, m


def _read_arrays():
    arr1 = list(map(int, input().split()))
    arr2 = list(map(int, input().split()))
    return arr1, arr2


def _merge_prefix(arr1, arr2, n, m, merged_array):
    i = j = 0
    while i < n and j < m:
        if arr1[i] >= arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1
    return i, j


def _append_remaining(array, index, size, merged_array):
    while index < size:
        merged_array.append(array[index])
        index += 1


def _merge_arrays(arr1, arr2, n, m):
    merged_array = []
    i, j = _merge_prefix(arr1, arr2, n, m, merged_array)
    _append_remaining(arr1, i, n, merged_array)
    _append_remaining(arr2, j, m, merged_array)
    return merged_array


def _print_array(merged_array):
    print(*merged_array)


def solve():
    """
    This function handles a single test case.
    """
    sizes = _read_sizes()
    if sizes is None:
        return

    n, m = sizes
    arr1, arr2 = _read_arrays()
    merged_array = _merge_arrays(arr1, arr2, n, m)
    _print_array(merged_array)


def _read_test_count():
    return int(input())


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        t = _read_test_count()
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        pass


if __name__ == "__main__":
    main()
