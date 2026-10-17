def _merge_non_increasing(arr1, arr2, n, m):
    """
    Merge two sorted arrays into a single array sorted in non-increasing order.
    """
    i = 0  # Pointer for arr1
    j = 0  # Pointer for arr2
    merged_array = []

    # Merge the two arrays using the two-pointer technique
    while i < n and j < m:
        # Since arrays are sorted in non-increasing order,
        # pick the larger element to maintain the order.
        if arr1[i] >= arr2[j]:
            merged_array.append(arr1[i])
            i += 1
        else:
            merged_array.append(arr2[j])
            j += 1

    # If there are remaining elements in arr1, append them
    while i < n:
        merged_array.append(arr1[i])
        i += 1

    # If there are remaining elements in arr2, append them
    while j < m:
        merged_array.append(arr2[j])
        j += 1

    return merged_array


def solve():
    """
    This function handles a single test case.
    """
    # Read the sizes of the two arrays
    try:
        n, m = map(int, input().split())
    except (EOFError, ValueError):
        return  # Stop if there's no more input

    # Read the two sorted arrays
    arr1 = list(map(int, input().split()))
    arr2 = list(map(int, input().split()))

    # Merge the two arrays
    merged_array = _merge_non_increasing(arr1, arr2, n, m)

    # Print the final merged array with space-separated values
    print(*merged_array)


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        # Read the number of test cases
        t = int(input())
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        # Handles cases with no input or invalid input
        pass


if __name__ == "__main__":
    main()
