def rotate_90_clockwise(x, y):
    return (y, -x)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def _read_point():
    line = input().split()
    return int(line[0]), int(line[1])

def _read_input():
    point_a = _read_point()
    point_b = _read_point()
    point_c = _read_point()
    return point_a, point_b, point_c

def _generate_rotations(x, y):
    vectors = [(x, y)]
    for _ in range(3):
        vectors.append(rotate_90_clockwise(vectors[-1][0], vectors[-1][1]))
    return vectors

def _is_scalar_solution_via_x(vx, vy, target_x, target_y):
    k = target_x // vx
    return k >= 0 and k * vy == target_y

def _is_scalar_solution_via_y(vx, vy, target_x, target_y):
    k = target_y // vy
    return k >= 0 and k * vx == target_x

def _is_single_vector_solution(vx, vy, target_x, target_y):
    if vx != 0 and target_x % vx == 0:
        return _is_scalar_solution_via_x(vx, vy, target_x, target_y)
    elif vy != 0 and target_y % vy == 0:
        return _is_scalar_solution_via_y(vx, vy, target_x, target_y)
    elif vx == 0 and vy == 0 and target_x == 0 and target_y == 0:
        return True
    return False

def _is_pair_solution(v1, v2, target_x, target_y):
    v1x, v1y = v1
    v2x, v2y = v2

    det = v1x * v2y - v1y * v2x
    if det != 0:
        if ((v2y * target_x - v2x * target_y) % det == 0 and
                (v1x * target_y - v1y * target_x) % det == 0):
            a = (v2y * target_x - v2x * target_y) // det
            b = (v1x * target_y - v1y * target_x) // det
            if a >= 0 and b >= 0:
                return True
        return False

    cross = v1x * target_y - v1y * target_x
    if cross == 0:
        if v1x != 0:
            if target_x % v1x == 0:
                return _is_scalar_solution_via_x(v1x, v1y, target_x, target_y)
        elif v1y != 0:
            if target_y % v1y == 0:
                return _is_scalar_solution_via_y(v1x, v1y, target_x, target_y)
        elif target_x == 0 and target_y == 0:
            return True

    return False

def _can_express_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True

    for i in range(4):
        vx, vy = c_vectors[i]
        if _is_single_vector_solution(vx, vy, target_x, target_y):
            return True

    for i in range(4):
        for j in range(i + 1, 4):
            if _is_pair_solution(c_vectors[i], c_vectors[j], target_x, target_y):
                return True

    return False

def _is_possible(x1, y1, x2, y2, x3, y3):
    c_vectors = _generate_rotations(x3, y3)
    current_a = (x1, y1)

    for _ in range(4):
        target_x = x2 - current_a[0]
        target_y = y2 - current_a[1]

        if _can_express_target(c_vectors, target_x, target_y):
            return True

        current_a = rotate_90_clockwise(current_a[0], current_a[1])

    return False

def _print_answer(possible):
    print("YES" if possible else "NO")

def main():
    (x1, y1), (x2, y2), (x3, y3) = _read_input()
    answer = _is_possible(x1, y1, x2, y2, x3, y3)
    _print_answer(answer)

if __name__ == "__main__":
    main()
