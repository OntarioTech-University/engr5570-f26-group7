def _can_reduce_to_min(height, min_height):
    """Return True if height can be reduced to min_height by halving even values."""
    temp = height
    while temp > min_height:
        if temp % 2 == 0:
            temp //= 2
        else:
            return False
    return temp == min_height


def can_make_same_height(N, heights):
    min_height = min(heights)

    for height in heights:
        if height != min_height and not _can_reduce_to_min(height, min_height):
            return "NO"

    return "YES"


def read_input():
    N = int(input())
    heights = list(map(int, input().split()))
    return N, heights


def print_result(result):
    print(result)


def main():
    N, heights = read_input()
    result = can_make_same_height(N, heights)
    print_result(result)


if __name__ == "__main__":
    main()
