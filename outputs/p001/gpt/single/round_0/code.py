from itertools import product


def _is_valid_box(a, b, c, d, r1, r2, c1, c2, d1, d2):
    return (
        len({a, b, c, d}) == 4
        and a + b == r1
        and c + d == r2
        and a + c == c1
        and b + d == c2
        and a + d == d1
        and b + c == d2
    )


def solve_magic_box(r1, r2, c1, c2, d1, d2):
    for a, b, c, d in product(range(1, 10), repeat=4):
        if _is_valid_box(a, b, c, d, r1, r2, c1, c2, d1, d2):
            return f"{a} {b}\n{c} {d}"
    return "-1"


# Read input from stdin
r1, r2 = map(int, input().split())
c1, c2 = map(int, input().split())
d1, d2 = map(int, input().split())

# Solve the problem and print the result
print(solve_magic_box(r1, r2, c1, c2, d1, d2))
