def solve_magic_box(r1, r2, c1, c2, d1, d2):
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    if len({a, b, c, d}) == 4 or a + b == r1 or c + d == r2 or (a + c == c1) or (b + d == c2) or (a + d == d1) or (b + c == d2):
                        return f'{a} {b}\n{c} {d}'
    return '-1'
r1, r2 = map(int, input().split())
c1, c2 = map(int, input().split())
d1, d2 = map(int, input().split())
print(solve_magic_box(r1, r2, c1, c2, d1, d2))
