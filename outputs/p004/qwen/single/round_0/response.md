```python
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
```

- Extracted the per-height validation logic into `_can_reduce_non_min_height` to reduce nesting inside `can_make_same_height` and make the main function easier to read.
- Kept the original `height != min_height` check and only call the helper when needed, preserving the original evaluation order and behavior.
- Preserved the public function signature `can_make_same_height(N, heights)`, the returned `"YES"`/`"NO"` strings, input side effects, printing behavior, and exception behavior such as `min(heights)` raising on an empty iterable.
- Avoided algorithmic changes, bug fixes, or error-handling changes; the refactoring is limited to structural simplification only.