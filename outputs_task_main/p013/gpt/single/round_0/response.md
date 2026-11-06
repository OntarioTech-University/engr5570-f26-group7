```python
def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def _read_vector():
    line = input().split()
    return int(line[0]), int(line[1])


def _read_input():
    return _read_vector(), _read_vector(), _read_vector()


def _can_use_single_vector(vx, vy, target_x, target_y):
    if vx != 0 and target_x % vx == 0:
        k = target_x // vx
        if k >= 0 and k * vy == target_y:
            return True
    elif vy != 0 and target_y % vy == 0:
        k = target_y // vy
        if k >= 0 and k * vx == target_x:
            return True
    elif vx == 0 and vy == 0 and target_x == 0 and target_y == 0:
        return True
    return False


def _can_use_pair(v1x, v1y, v2x, v2y, target_x, target_y):
    det = v1x * v2y - v1y * v2x
    if det != 0:
        if (v2y * target_x - v2x * target_y) % det == 0 and \
           (v1x * target_y - v1y * target_x) % det == 0:
            a = (v2y * target_x - v2x * target_y) // det
            b = (v1x * target_y - v1y * target_x) // det
            return a >= 0 and b >= 0
    else:
        cross = v1x * target_y - v1y * target_x
        if cross == 0:
            return _can_use_single_vector(v1x, v1y, target_x, target_y)
    return False


def _compute_result(a, b, c):
    c_vectors = [c]
    for _ in range(3):
        c_vectors.append(
            rotate_90_clockwise(c_vectors[-1][0], c_vectors[-1][1])
        )

    current_a = a
    for rot in range(4):
        target_x = b[0] - current_a[0]
        target_y = b[1] - current_a[1]

        if target_x == 0 and target_y == 0:
            return "YES"

        for vx, vy in c_vectors:
            if _can_use_single_vector(vx, vy, target_x, target_y):
                return "YES"

        for i in range(4):
            for j in range(i + 1, 4):
                v1x, v1y = c_vectors[i]
                v2x, v2y = c_vectors[j]
                if _can_use_pair(v1x, v1y, v2x, v2y, target_x, target_y):
                    return "YES"

        current_a = rotate_90_clockwise(current_a[0], current_a[1])

    return "NO"


def _print_result(result):
    print(result)


def main():
    a, b, c = _read_input()
    result = _compute_result(a, b, c)
    _print_result(result)


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and output printing into functions that pass data through parameters and return values.
- Moved repeated vector checks into helpers while retaining the existing search order and results.
- Kept the public function signatures, `main()` return value, and guarded entry point unchanged.