def _can_reduce_non_min_height(height, min_height):
    if height % 2 != 0:
        return False

    temp = height
    while temp > min_height:
        if temp % 2 != 0:
            return False
        temp //= 2

    return temp == min_height


def can_make_same_height(N, heights):
    min_height = min(heights)

    for height in heights:
        if height != min_height and not _can_reduce_non_min_height(height, min_height):
            return "NO"

    return "YES"


# Read the number of sugarcanes
N = int(input())

# Read the heights of sugarcanes
heights = list(map(int, input().split()))

# Check if it's possible to make all sugarcanes of the same height
print(can_make_same_height(N, heights))
