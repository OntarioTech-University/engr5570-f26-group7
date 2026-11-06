def get_min_height(heights):
    return min(heights)


def can_reduce_to_min(height, min_height):
    if height == min_height:
        return True
    if height % 2 != 0:
        return False

    temp = height
    while temp > min_height:
        if temp % 2 == 0:
            temp //= 2
        else:
            return False

    return temp == min_height


def can_make_same_height(N, heights):
    min_height = get_min_height(heights)

    for height in heights:
        if not can_reduce_to_min(height, min_height):
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


main()
