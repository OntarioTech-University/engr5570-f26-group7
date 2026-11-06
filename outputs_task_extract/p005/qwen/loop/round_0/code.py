def read_test_count():
    """Read the number of test cases."""
    return int(input())


def read_case_sizes():
    """Read the sizes of the two arrays for one test case."""
    n, m = map(int, input().split())
    return n, m


def read_int_array():
    """Read one space-separated integer array."""
    return list(map(int, input().split()))


def merge_until_one_exhausted(arr1, arr2, n, m, merged_array):
    """Merge elements while both arrays still have unmerged elements."""
    i = 0
    j = 0
    while i < n and j < m:
        if arr1[i] >= arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1
    return i, j


def append_remaining_elements(source, index, limit, merged_array):
    """Append any leftover elements from one array."""
    while index < limit:
        merged_array.append(source[index])
        index += 1


def merge_arrays(arr1, arr2, n, m):
    """Merge two sorted arrays into a single sorted array."""
    merged_array = []
    i, j = merge_until_one_exhausted(arr1, arr2, n, m, merged_array)
    append_remaining_elements(arr1, i, n, merged_array)
    append_remaining_elements(arr2, j, m, merged_array)
    return merged_array


def print_merged_array(merged_array):
    """Print the merged array as space-separated values."""
    print(*merged_array)


def solve():
    """
    This function handles a single test case.
    """
    try:
        n, m = read_case_sizes()
    except (EOFError, ValueError):
        return  # Stop if there's no more input

    arr1 = read_int_array()
    arr2 = read_int_array()

    merged_array = merge_arrays(arr1, arr2, n, m)

    print_merged_array(merged_array)


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        t = read_test_count()
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        # Handles cases with no input or invalid input
        pass


if __name__ == "__main__":
    main()
