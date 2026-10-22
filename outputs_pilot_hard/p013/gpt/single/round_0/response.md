```python
def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def read_vectors():
    line = input().split()
    x1, y1 = int(line[0]), int(line[1])

    line = input().split()
    x2, y2 = int(line[0]), int(line[1])

    line = input().split()
    x3, y3 = int(line[0]), int(line[1])

    return (x1, y1), (x2, y2), (x3, y3)


def can_use_single_vector(vx, vy, target_x, target_y):
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


def can_use_pair(v1x, v1y, v2x, v2y, target_x, target_y):
    det = v1x * v2y - v1y * v2x
    if det != 0:
        if (v2y * target_x - v2x * target_y) % det == 0 and \
           (v1x * target_y - v1y * target_x) % det == 0:
            a = (v2y * target_x - v2x * target_y) // det
            b = (v1x * target_y - v1y * target_x) // det
            if a >= 0 and b >= 0:
                return True
    else:
        cross = v1x * target_y - v1y * target_x
        if cross == 0:
            return can_use_single_vector(v1x, v1y, target_x, target_y)

    return False


def can_reach_target(a, b, c):
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
            return True

        for vx, vy in c_vectors:
            if can_use_single_vector(vx, vy, target_x, target_y):
                return True

        for i in range(4):
            for j in range(i + 1, 4):
                v1x, v1y = c_vectors[i]
                v2x, v2y = c_vectors[j]
                if can_use_pair(v1x, v1y, v2x, v2y, target_x, target_y):
                    return True

        current_a = rotate_90_clockwise(current_a[0], current_a[1])

    return False


def print_result(found):
    print("YES" if found else "NO")


def main():
    a, b, c = read_vectors()
    found = can_reach_target(a, b, c)
    print_result(found)


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and output printing; `main()` passes data between them without global state.
- Moved the repeated single-vector check into a shared helper, while retaining the existing search order and public function signatures.