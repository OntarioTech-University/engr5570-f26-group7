```python
def can_make_same_height(N, heights):
    # Find the minimum height
    min_height = min(heights)

    # Check if all heights can be made equal to the minimum height
    for height in heights:
        if height != min_height and not _can_reduce_to_min(height, min_height):
            return "NO"

    return "YES"


def _can_reduce_to_min(height, target):
    """Return True if height can be reduced to target by repeated halving."""
    temp = height
    while temp > target and temp % 2 == 0:
        temp //= 2
    return temp == target


# Read the number of sugarcanes
N = int(input())

# Read the heights of sugarcanes
heights = list(map(int, input().split()))

# Check if it's possible to make all sugarcanes of the same height
print(can_make_same_height(N, heights))
```

- Extracted the reduction logic into a small helper function `_can_reduce_to_min`, which removes nested conditionals and makes the main loop easier to read.
- Simplified the loop condition to `while temp > target and temp % 2 == 0`, eliminating the redundant initial odd check and inner `if/else`.
- Preserved the public function signature and all input/output behavior exactly.