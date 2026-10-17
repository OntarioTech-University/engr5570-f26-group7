```python
def rotate_90_clockwise(x, y):
    return (y, -x)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def _generate_rotations(vector):
    rotations = [vector]
    for _ in range(3):
        rotations.append(rotate_90_clockwise(rotations[-1][0], rotations[-1][1]))
    return rotations

def _can_express_target(c_vectors, target_x, target_y):
    if target_x == 0 and target_y == 0:
        return True

    if _can_use_single_vector(c_vectors, target_x, target_y):
        return True

    return _can_use_pair_of_vectors(c_vectors, target_x, target_y)

def _can_use_single_vector(c_vectors, target_x, target_y):
    for i in range(4):
        vx, vy = c_vectors[i]
        if _single_vector_matches(vx, vy, target_x, target_y):
            return True
    return False

def _single_vector_matches(vx, vy, target_x, target_y):
    if vx != 0 and target_x % vx == 0:
        k = target_x // vx
        return k >= 0 and k * vy == target_y

    if vy != 0 and target_y % vy == 0:
        k = target_y // vy
        return k >= 0 and k * vx == target_x

    return vx == 0 and vy == 0 and target_x == 0 and target_y == 0

def _can_use_pair_of_vectors(c_vectors, target_x, target_y):
    for i in range(4):
        for j in range(i + 1, 4):
            v1 = c_vectors[i]
            v2 = c_vectors[j]
            if _pair_of_vectors_matches(v1, v2, target_x, target_y):
                return True
    return False

def _pair_of_vectors_matches(v1, v2, target_x, target_y):
    v1x, v1y = v1
    v2x, v2y = v2

    det = v1x * v2y - v1y * v2x
    if det != 0:
        return _independent_pair_matches(v1x, v1y, v2x, v2y, det, target_x, target_y)

    return _dependent_pair_matches(v1x, v1y, target_x, target_y)

def _independent_pair_matches(v1x, v1y, v2x, v2y, det, target_x, target_y):
    a_numerator = v2y * target_x - v2x * target_y
    b_numerator = v1x * target_y - v1y * target_x

    if a_numerator % det != 0 or b_numerator % det != 0:
        return False

    a = a_numerator // det
    b = b_numerator // det
    return a >= 0 and b >= 0

def _dependent_pair_matches(v1x, v1y, target_x, target_y):
    cross = v1x * target_y - v1y * target_x
    if cross != 0:
        return False

    if v1x != 0:
        if target_x % v1x == 0:
            a = target_x // v1x
            return a >= 0 and a * v1y == target_y
        return False

    if v1y != 0:
        if target_y % v1y == 0:
            a = target_y // v1y
            return a >= 0 and a * v1x == target_x
        return False

    return target_x == 0 and target_y == 0

def main():
    line = input().split()
    x1, y1 = int(line[0]), int(line[1])
    
    line = input().split()
    x2, y2 = int(line[0]), int(line[1])
    
    line = input().split()
    x3, y3 = int(line[0]), int(line[1])
    
    c_vectors = _generate_rotations((x3, y3))
    current_a = (x1, y1)

    for _ in range(4):
        target_x = x2 - current_a[0]
        target_y = y2 - current_a[1]

        if _can_express_target(c_vectors, target_x, target_y):
            print("YES")
            return

        current_a = rotate_90_clockwise(current_a[0], current_a[1])
    
    print("NO")

if __name__ == "__main__":
    main()
```

- Extracted rotation generation into `_generate_rotations` to keep `main` focused on overall control flow.
- Centralized the per-target feasibility decision in `_can_express_target`, preserving the original early exit for a zero target.
- Split the single-vector search into `_can_use_single_vector` and `_single_vector_matches`, keeping the original branch precedence and loop order.
- Split the pair-vector search into `_can_use_pair_of_vectors`, `_pair_of_vectors_matches`, `_independent_pair_matches`, and `_dependent_pair_matches` to reduce nesting while preserving the same arithmetic checks.
- Left public functions, input parsing, printing behavior, and exception behavior unchanged.