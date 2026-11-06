def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def _next_a(current_a):
    return rotate_90_clockwise(current_a[0], current_a[1])


def _read_point():
    line = input().split()
    return int(line[0]), int(line[1])


def _generate_c_vectors(x3, y3):
    c_vectors = [(x3, y3)]
    for _ in range(3):
        c_vectors.append(_next_a(c_vectors[-1]))
    return c_vectors


def _compute_target(x2, y2, current_a):
    return x2 - current_a[0], y2 - current_a[1]


def _is_nonnegative_multiple(component, other_component, target_component, target_other):
    if target_component % component != 0:
        return False
    factor = target_component // component
    return factor >= 0 and factor * other_component == target_other


def _can_use_single_vector(vector, target_x, target_y):
    vx, vy = vector
    if vx != 0 and target_x % vx == 0:
        k = target_x // vx
        return k >= 0 and k * vy == target_y
    if vy != 0 and target_y % vy == 0:
        k = target_y // vy
        return k >= 0 and k * vx == target_x
    return vx == 0 and vy == 0 and target_x == 0 and target_y == 0


def _found_in_single_vectors(c_vectors, target_x, target_y):
    for vector in c_vectors:
        if _can_use_single_vector(vector, target_x, target_y):
            return True
    return False


def _can_use_independent_pair(v1x, v1y, v2x, v2y, det, target_x, target_y):
    a_num = v2y * target_x - v2x * target_y
    b_num = v1x * target_y - v1y * target_x
    if a_num % det != 0 or b_num % det != 0:
        return False
    a = a_num // det
    b = b_num // det
    return a >= 0 and b >= 0


def _can_use_dependent_pair(v1x, v1y, target_x, target_y):
    if v1x * target_y - v1y * target_x != 0:
        return False
    if v1x != 0:
        return _is_nonnegative_multiple(v1x, v1y, target_x, target_y)
    if v1y != 0:
        return _is_nonnegative_multiple(v1y, v1x, target_y, target_x)
    return target_x == 0 and target_y == 0


def _can_use_pair(v1, v2, target_x, target_y):
    v1x, v1y = v1
    v2x, v2y = v2
    det = v1x * v2y - v1y * v2x
    if det != 0:
        return _can_use_independent_pair(v1x, v1y, v2x, v2y, det, target_x, target_y)
    return _can_use_dependent_pair(v1x, v1y, target_x, target_y)


def _found_in_pairs(c_vectors, target_x, target_y):
    for i in range(4):
        for j in range(i + 1, 4):
            if _can_use_pair(c_vectors[i], c_vectors[j], target_x, target_y):
                return True
    return False


def _can_express_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True
    if _found_in_single_vectors(c_vectors, target_x, target_y):
        return True
    return _found_in_pairs(c_vectors, target_x, target_y)


def _has_valid_rotation(x1, y1, x2, y2, c_vectors):
    current_a = (x1, y1)
    for _ in range(4):
        target_x, target_y = _compute_target(x2, y2, current_a)
        if _can_express_target(c_vectors, target_x, target_y):
            return True
        current_a = _next_a(current_a)
    return False


def _print_yes():
    print("YES")


def _print_no():
    print("NO")


def main():
    x1, y1 = _read_point()
    x2, y2 = _read_point()
    x3, y3 = _read_point()
    c_vectors = _generate_c_vectors(x3, y3)
    if _has_valid_rotation(x1, y1, x2, y2, c_vectors):
        _print_yes()
        return
    _print_no()


if __name__ == "__main__":
    main()
