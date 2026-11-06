```python
def rotate_90_clockwise(x, y):
    return (y, -x)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def read_vector():
    line = input().split()
    return int(line[0]), int(line[1])


def generate_rotations(vector):
    rotations = [vector]
    for _ in range(3):
        rotations.append(rotate_90_clockwise(rotations[-1][0], rotations[-1][1]))
    return rotations


def matches_single_vector(vx, vy, target_x, target_y):
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


def matches_any_single_vector(vectors, target_x, target_y):
    for i in range(4):
        vx, vy = vectors[i]
        if matches_single_vector(vx, vy, target_x, target_y):
            return True
    return False


def matches_independent_pair(v1x, v1y, v2x, v2y, target_x, target_y, det):
    if (v2y * target_x - v2x * target_y) % det == 0 and \
       (v1x * target_y - v1y * target_x) % det == 0:
        a = (v2y * target_x - v2x * target_y) // det
        b = (v1x * target_y - v1y * target_x) // det
        return a >= 0 and b >= 0
    return False


def matches_dependent_pair(v1x, v1y, target_x, target_y):
    if v1x * target_y - v1y * target_x != 0:
        return False
    if v1x != 0:
        if target_x % v1x != 0:
            return False
        a = target_x // v1x
        return a >= 0 and a * v1y == target_y
    if v1y != 0:
        if target_y % v1y != 0:
            return False
        a = target_y // v1y
        return a >= 0 and a * v1x == target_x
    return target_x == 0 and target_y == 0


def matches_pair(v1, v2, target_x, target_y):
    v1x, v1y = v1
    v2x, v2y = v2
    det = v1x * v2y - v1y * v2x
    if det != 0:
        return matches_independent_pair(
            v1x, v1y, v2x, v2y, target_x, target_y, det
        )
    return matches_dependent_pair(v1x, v1y, target_x, target_y)


def matches_any_pair(vectors, target_x, target_y):
    for i in range(4):
        for j in range(i + 1, 4):
            if matches_pair(vectors[i], vectors[j], target_x, target_y):
                return True
    return False


def matches_rotation(current_a, target, c_vectors):
    target_x = target[0] - current_a[0]
    target_y = target[1] - current_a[1]
    if target_x == 0 and target_y == 0:
        return True
    if matches_any_single_vector(c_vectors, target_x, target_y):
        return True
    return matches_any_pair(c_vectors, target_x, target_y)


def has_solution(a, target, c_vectors):
    current_a = a
    for rot in range(4):
        if matches_rotation(current_a, target, c_vectors):
            return True
        current_a = rotate_90_clockwise(current_a[0], current_a[1])
    return False


def print_result(found):
    if found:
        print("YES")
    else:
        print("NO")


def main():
    a = read_vector()
    target = read_vector()
    c = read_vector()
    c_vectors = generate_rotations(c)
    print_result(has_solution(a, target, c_vectors))


if __name__ == "__main__":
    main()
```

- Moved input reading, rotation generation, solution checking, and output printing into short, single-purpose functions.
- Split single-vector and pair checks into focused helpers while preserving their original check order and conditions.
- Kept the public function signatures and the program’s output behavior unchanged.