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

def _generate_c_vectors(x, y):
    c_vectors = [(x, y)]
    for _ in range(3):
        c_vectors.append(rotate_90_clockwise(c_vectors[-1][0], c_vectors[-1][1]))
    return c_vectors

def _is_single_vector_solution(c_vectors, target_x, target_y):
    for i in range(4):
        vx, vy = c_vectors[i]
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

def _is_dependent_pair_solution(v1x, v1y, target_x, target_y):
    if v1x != 0:
        if target_x % v1x == 0:
            a = target_x // v1x
            if a >= 0 and a * v1y == target_y:
                return True
    elif v1y != 0:
        if target_y % v1y == 0:
            a = target_y // v1y
            if a >= 0 and a * v1x == target_x:
                return True
    elif target_x == 0 and target_y == 0:
        return True
    return False

def _is_pair_solution(c_vectors, target_x, target_y):
    for i in range(4):
        for j in range(i + 1, 4):
            v1x, v1y = c_vectors[i]
            v2x, v2y = c_vectors[j]

            det = v1x * v2y - v1y * v2x
            if det != 0:
                if ((v2y * target_x - v2x * target_y) % det == 0 and
                        (v1x * target_y - v1y * target_x) % det == 0):
                    a = (v2y * target_x - v2x * target_y) // det
                    b = (v1x * target_y - v1y * target_x) // det
                    if a >= 0 and b >= 0:
                        return True
            else:
                cross = v1x * target_y - v1y * target_x
                if cross == 0:
                    if _is_dependent_pair_solution(v1x, v1y, target_x, target_y):
                        return True
    return False

def _can_express_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True
    if _is_single_vector_solution(c_vectors, target_x, target_y):
        return True
    if _is_pair_solution(c_vectors, target_x, target_y):
        return True
    return False

def _solve(point_a, point_b, point_c):
    x1, y1 = point_a
    x2, y2 = point_b
    x3, y3 = point_c

    c_vectors = _generate_c_vectors(x3, y3)

    current_a = (x1, y1)
    for _ in range(4):
        target_x = x2 - current_a[0]
        target_y = y2 - current_a[1]

        if _can_express_target(c_vectors, target_x, target_y):
            return "YES"

        current_a = rotate_90_clockwise(current_a[0], current_a[1])

    return "NO"

def _print_answer(answer):
    print(answer)

def main():
    point_a, point_b, point_c = _read_input()
    answer = _solve(point_a, point_b, point_c)
    _print_answer(answer)

if __name__ == "__main__":
    main()
