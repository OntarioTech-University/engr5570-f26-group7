def can_make_same_height(N, heights):
    min_height = min(heights)

    for height in heights:
        if not can_reduce_to_min(height, min_height):
            return "NO"

    return "YES"


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


# Read the number of sugarcanes
N = int(input())

# Read the heights of sugarcanes
heights = list(map(int, input().split()))

# Check if it's possible to make all sugarcanes of the same height
print(can_make_same_height(N, heights))
