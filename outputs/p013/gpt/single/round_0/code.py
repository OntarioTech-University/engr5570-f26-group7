def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def read_vector():
    line = input().split()
    return int(line[0]), int(line[1])


def rotations(vector):
    vectors = [vector]
    for _ in range(3):
        vectors.append(rotate_90_clockwise(vectors[-1][0], vectors[-1][1]))
    return vectors


def matches_single_vector(vector, target_x, target_y):
    vx, vy = vector
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


def matches_dependent_pair(v1x, v1y, target_x, target_y):
    if v1x * target_y - v1y * target_x != 0:
        return False

    if v1x != 0:
        if target_x % v1x == 0:
            a = target_x // v1x
            return a >= 0 and a * v1y == target_y
    elif v1y != 0:
        if target_y % v1y == 0:
            a = target_y // v1y
            return a >= 0 and a * v1x == target_x
    elif target_x == 0 and target_y == 0:
        return True

    return False


def matches_pair(v1, v2, target_x, target_y):
    v1x, v1y = v1
    v2x, v2y = v2
    det = v1x * v2y - v1y * v2x

    if det == 0:
        return matches_dependent_pair(v1x, v1y, target_x, target_y)

    a_numerator = v2y * target_x - v2x * target_y
    b_numerator = v1x * target_y - v1y * target_x
    if a_numerator % det == 0 and b_numerator % det == 0:
        a = a_numerator // det
        b = b_numerator // det
        return a >= 0 and b >= 0

    return False


def can_express_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True

    for vector in c_vectors:
        if matches_single_vector(vector, target_x, target_y):
            return True

    for i in range(4):
        for j in range(i + 1, 4):
            if matches_pair(c_vectors[i], c_vectors[j], target_x, target_y):
                return True

    return False


def main():
    x1, y1 = read_vector()
    x2, y2 = read_vector()
    x3, y3 = read_vector()

    c_vectors = rotations((x3, y3))
    current_a = (x1, y1)

    for _ in range(4):
        target_x = x2 - current_a[0]
        target_y = y2 - current_a[1]

        if can_express_target(c_vectors, target_x, target_y):
            print("YES")
            return

        current_a = rotate_90_clockwise(current_a[0], current_a[1])

    print("NO")


if __name__ == "__main__":
    main()
