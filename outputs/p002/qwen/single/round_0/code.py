def _derived_values_in_range(b, c, d):
    return all(1 <= value <= 9 for value in (b, c, d))


def _values_are_distinct(a, b, c, d):
    return len({a, b, c, d}) == 4


def _satisfies_remaining_constraints(b, c, d, r2, c2, d2):
    return c + d == r2 and b + d == c2 and b + c == d2


def _is_valid_solution(a, b, c, d, r2, c2, d2):
    return (
        _derived_values_in_range(b, c, d)
        and _values_are_distinct(a, b, c, d)
        and _satisfies_remaining_constraints(b, c, d, r2, c2, d2)
    )


# Read input
r1, r2 = map(int, input().split())
c1, c2 = map(int, input().split())
d1, d2 = map(int, input().split())

found = False
result = []

# Try all possibilities for a (from 1 to 9)
for a in range(1, 10):
    # Compute others using constraint equations
    b = r1 - a
    c = c1 - a
    d = d1 - a

    if _is_valid_solution(a, b, c, d, r2, c2, d2):
        found = True
        result = [[a, b], [c, d]]
        break

if found:
    print(result[0][0], result[0][1])
    print(result[1][0], result[1][1])
else:
    print(-1)
