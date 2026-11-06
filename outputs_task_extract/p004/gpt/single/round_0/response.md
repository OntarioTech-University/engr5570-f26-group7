```python
def can_reduce_to_minimum(height, min_height):
    if height % 2 != 0:
        return False

    temp = height
    while temp > min_height:
        if temp % 2 == 0:
            temp = temp // 2
        else:
            return False

    return temp == min_height


def can_make_same_height(N, heights):
    min_height = min(heights)

    for height in heights:
        if height != min_height and not can_reduce_to_minimum(height, min_height):
            return "NO"

    return "YES"


def read_number_of_sugarcanes():
    return int(input())


def read_heights():
    return list(map(int, input().split()))


def print_result(N, heights):
    print(can_make_same_height(N, heights))


N = read_number_of_sugarcanes()
heights = read_heights()
print_result(N, heights)
```

- Moved the height-reduction check into a small helper, leaving `can_make_same_height` focused on checking all heights.
- Separated the two input reads and output printing into dedicated functions. The public function signature and top-level execution remain unchanged.