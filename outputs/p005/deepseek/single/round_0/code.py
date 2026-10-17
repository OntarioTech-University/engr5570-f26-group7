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
