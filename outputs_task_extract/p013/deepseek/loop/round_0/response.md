```python
def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def read_point():
    line = input().split()
    return int(line[0]), int(line[1])


def read_points():
    return read_point(), read_point(), read_point()


def generate_rotations(point):
    rotations = [point]
    for _ in range(3):
        rotations.append(rotate_90_clockwise(*rotations[-1]))
    return rotations


def compute_target(a, b):
    return (b[0] - a[0], b[1] - a[1])


def is_zero(point):
    return point[0] == 0 and point[1] == 0


def print_yes():
    print("YES")


def print_no():
    print("NO")


def can_express_with_single_vector(target, vector):
    tx, ty = target
    vx, vy = vector

    if vx != 0 and tx % vx == 0:
        k = tx // vx
        return k >= 0 and k * vy == ty
    elif vy != 0 and ty % vy == 0:
        k = ty // vy
        return k >= 0 and k * vx == tx
    elif vx == 0 and vy == 0 and tx == 0 and ty == 0:
        return True

    return False


def check_single_vectors(target, vectors):
    for vector in vectors:
        if can_express_with_single_vector(target, vector):
            return True
    return False


def can_express_with_independent_pair(target, v1, v2, det):
    tx, ty = target
    v1x, v1y = v1
    v2x, v2y = v2

    num_a = v2y * tx - v2x * ty
    num_b = v1x * ty - v1y * tx

    if num_a % det == 0 and num_b % det == 0:
        a = num_a // det
        b = num_b // det
        return a >= 0 and b >= 0

    return False


def can_express_with_dependent_pair(target, v1, v2):
    tx, ty = target
    v1x, v1y = v1

    if v1x * ty - v1y * tx != 0:
        return False

    if v1x != 0:
        if tx % v1x == 0:
            a = tx // v1x
            return a >= 0 and a * v1y == ty
    elif v1y != 0:
        if ty % v1y == 0:
            a = ty // v1y
            return a >= 0 and a * v1x == tx
    elif tx == 0 and ty == 0:
        return True

    return False


def can_express_with_pair(target, v1, v2):
    det = v1[0] * v2[1] - v1[1] * v2[0]
    if det != 0:
        return can_express_with_independent_pair(target, v1, v2, det)
    return can_express_with_dependent_pair(target, v1, v2)


def check_pairs(target, vectors):
    for i in range(4):
        for j in range(i + 1, 4):
            if can_express_with_pair(target, vectors[i], vectors[j]):
                return True
    return False


def can_express(target, vectors):
    return check_single_vectors(target, vectors) or check_pairs(target, vectors)


def main():
    a, b, c = read_points()
    c_vectors = generate_rotations(c)
    current_a = a

    for _ in range(4):
        target = compute_target(current_a, b)
        if is_zero(target) or can_express(target, c_vectors):
            print_yes()
            return
        current_a = rotate_90_clockwise(*current_a)

    print_no()


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_point` and `read_points` to isolate I/O.
- Extracted rotation generation into `generate_rotations` for clarity.
- Extracted target computation and zero checking into `compute_target` and `is_zero`.
- Split the main combination logic into small, focused helpers: `can_express`, `check_single_vectors`, `check_pairs`, and their single/pair case helpers.
- Extracted output printing into `print_yes` and `print_no`.
- Preserved all public signatures (`rotate_90_clockwise`, `gcd`, `main`) and the exact control flow, arithmetic, and short-circuit behavior of the original code.