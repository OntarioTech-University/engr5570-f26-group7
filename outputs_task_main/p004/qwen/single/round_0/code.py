def read_input():
    N = int(input())
    heights = list(map(int, input().split()))
    return N, heights


def _can_reduce_to_min(height, min_height):
    temp = height
    while temp > min_height:
        if temp % 2 != 0:
            return False
        temp = temp // 2

    return temp == min_height


def can_make_same_height(N, heights):
    min_height = min(heights)

    for height in heights:
        if not _can_reduce_to_min(height, min_height):
            return "NO"

    return "YES"


def print_result(result):
    print(result)


def main():
    N, heights = read_input()
    result = can_make_same_height(N, heights)
    print_result(result)


if __name__ == "__main__":
    main()
