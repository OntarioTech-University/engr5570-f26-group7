def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def read_point():
    x, y = map(int, input().split())
    return x, y


def generate_rotations(point):
    rotations = [point]
    for _ in range(3):
        rotations.append(rotate_90_clockwise(*rotations[-1]))
    return rotations


def is_zero_vector(vx, vy):
    return vx == 0 and vy == 0


def try_single_vector(c_vectors, target_x, target_y):
    for vx, vy in c_vectors:
        if is_zero_vector(vx, vy):
            if target_x == 0 and target_y == 0:
                return True
            continue

        if vx != 0 and target_x % vx == 0:
            k = target_x // vx
            if k >= 0 and k * vy == target_y:
                return True
        elif vy != 0 and target_y % vy == 0:
            k = target_y // vy
            if k >= 0 and k * vx == target_x:
                return True

    return False


def try_vector_pair(v1, v2, target_x, target_y):
    v1x, v1y = v1
    v2x, v2y = v2

    det = v1x * v2y - v1y * v2x

    if det != 0:
        numerator_a = v2y * target_x - v2x * target_y
        numerator_b = v1x * target_y - v1y * target_x

        if numerator_a % det == 0 and numerator_b % det == 0:
            a = numerator_a // det
            b = numerator_b // det
            return a >= 0 and b >= 0

        return False

    # Dependent vectors: check if target is parallel to v1
    cross = v1x * target_y - v1y * target_x
    if cross != 0:
        return False

    if v1x != 0:
        if target_x % v1x == 0:
            a = target_x // v1x
            return a >= 0 and a * v1y == target_y
    elif v1y != 0:
        if target_y % v1y == 0:
            a = target_y // v1y
            return a >= 0 and a * v1x == target_x
    else:
        return target_x == 0 and target_y == 0

    return False


def try_all_vector_pairs(c_vectors, target_x, target_y):
    for i in range(4):
        for j in range(i + 1, 4):
            if try_vector_pair(c_vectors[i], c_vectors[j], target_x, target_y):
                return True
    return False


def can_reach_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True

    if try_single_vector(c_vectors, target_x, target_y):
        return True

    if try_all_vector_pairs(c_vectors, target_x, target_y):
        return True

    return False


def main():
    x1, y1 = read_point()
    x2, y2 = read_point()
    x3, y3 = read_point()

    c_vectors = generate_rotations((x3, y3))

    current_a = (x1, y1)
    for _ in range(4):
        target_x = x2 - current_a[0]
        target_y = y2 - current_a[1]

        if can_reach_target(c_vectors, target_x, target_y):
            print("YES")
            return

        current_a = rotate_90_clockwise(*current_a)

    print("NO")


if __name__ == "__main__":
    main()
