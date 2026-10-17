Here’s the refactored version of the code:

```python
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
```

### Summary of changes:
- **Extracted helper function `can_reduce_to_min`** – This removes the deeply nested conditional logic from the main loop and gives a clear name to the repeated reduction check.
- **Simplified conditionals** – Replaced nested `if` blocks with early returns, making the logic linear and easier to follow.
- **Used `//=` operator** – Minor readability improvement for integer division assignment.
- **Preserved all behavior** – The function still returns the same strings (`"YES"`/`"NO"`) and handles the same edge cases without changing error handling or input/output behavior.