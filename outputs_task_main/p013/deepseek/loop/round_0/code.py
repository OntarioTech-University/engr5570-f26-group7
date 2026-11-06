def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def read_input():
    line = input().split()
    x1, y1 = int(line[0]), int(line[1])

    line = input().split()
    x2, y2 = int(line[0]), int(line[1])

    line = input().split()
    x3, y3 = int(line[0]), int(line[1])

    return (x1, y1), (x2, y2), (x3, y3)


def generate_rotations(x, y):
    rotations = [(x, y)]
    for _ in range(3):
        rotations.append(rotate_90_clockwise(rotations[-1][0], rotations[-1][1]))
    return rotations


def check_single_vector(c_vectors, target_x, target_y):
    for vx, vy in c_vectors:
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


def check_pair_vectors(c_vectors, target_x, target_y):
    for i in range(4):
        for j in range(i + 1, 4):
            v1x, v1y = c_vectors[i]
            v2x, v2y = c_vectors[j]

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


def can_reach_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True

    if check_single_vector(c_vectors, target_x, target_y):
        return True

    if check_pair_vectors(c_vectors, target_x, target_y):
        return True

    return False


def compute_result(a, b, c):
    c_vectors = generate_rotations(c[0], c[1])

    current_a = a
    for _ in range(4):
        target_x = b[0] - current_a[0]
        target_y = b[1] - current_a[1]

        if can_reach_target(c_vectors, target_x, target_y):
            return "YES"

        current_a = rotate_90_clockwise(current_a[0], current_a[1])

    return "NO"


def print_result(result):
    print(result)


def main():
    a, b, c = read_input()
    result = compute_result(a, b, c)
    print_result(result)


if __name__ == "__main__":
    main()
