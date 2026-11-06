def read_test_count():
    return int(input())


def read_array():
    return list(map(int, input().split()))


def read_case():
    try:
        n, m = map(int, input().split())
    except (EOFError, ValueError):
        return None

    arr1 = read_array()
    arr2 = read_array()
    return n, m, arr1, arr2


def append_remaining(merged_array, array, index, length):
    while index < length:
        merged_array.append(array[index])
        index += 1


def merge_arrays(n, m, arr1, arr2):
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

    append_remaining(merged_array, arr1, i, n)
    append_remaining(merged_array, arr2, j, m)
    return merged_array


def print_merged_array(merged_array):
    print(*merged_array)


def solve():
    """
    This function handles a single test case.
    """
    case = read_case()
    if case is None:
        return

    merged_array = merge_arrays(*case)
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
        pass


if __name__ == "__main__":
    main()
