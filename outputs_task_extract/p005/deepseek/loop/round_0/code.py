def read_test_case_count():
    return int(input())


def read_test_case_sizes():
    try:
        n, m = map(int, input().split())
    except (EOFError, ValueError):
        return None
    return n, m


def read_arrays():
    arr1 = list(map(int, input().split()))
    arr2 = list(map(int, input().split()))
    return arr1, arr2


def merge_sorted_arrays(arr1, arr2, n, m):
    i = j = 0
    merged = []
    while i < n and j < m:
        if arr1[i] >= arr2[j]:
            merged.append(arr1[i]); i += 1
        else:
            merged.append(arr2[j]); j += 1
    while i < n:
        merged.append(arr1[i]); i += 1
    while j < m:
        merged.append(arr2[j]); j += 1
    return merged


def print_merged_array(merged_array):
    print(*merged_array)


def solve():
    sizes = read_test_case_sizes()
    if sizes is None:
        return
    n, m = sizes
    arr1, arr2 = read_arrays()
    merged_array = merge_sorted_arrays(arr1, arr2, n, m)
    print_merged_array(merged_array)


def main():
    try:
        t = read_test_case_count()
        for _ in range(t):
            solve()
    except (EOFError, ValueError):
        pass


if __name__ == "__main__":
    main()
