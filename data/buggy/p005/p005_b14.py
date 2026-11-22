def solve():
    """
    This function handles a single test case.
    """
    try:
        n, m = map(int, input().split())
    except (EOFError, ValueError):
        return
    arr1 = list(map(int, input().split()))
    arr2 = list(map(int, input().split()))
    i = 1
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
if __name__ == '__main__':
    main()
