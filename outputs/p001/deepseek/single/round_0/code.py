def _is_valid_solution(a, b, c, d, r1, r2, c1, c2, d1, d2):
    """Check if the given numbers satisfy all magic box constraints."""
    return (
        len({a, b, c, d}) == 4
        and a + b == r1
        and c + d == r2
        and a + c == c1
        and b + d == c2
        and a + d == d1
        and b + c == d2
    )


def _format_solution(a, b, c, d):
    """Format the solution as a 2x2 grid string."""
    return f"{a} {b}\n{c} {d}"


def solve_magic_box(r1, r2, c1, c2, d1, d2):
    # Iterate through all possible combinations of a, b, c, and d
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    if _is_valid_solution(a, b, c, d, r1, r2, c1, c2, d1, d2):
                        return _format_solution(a, b, c, d)
    return "-1"


# Read input from stdin
r1, r2 = map(int, input().split())
c1, c2 = map(int, input().split())
d1, d2 = map(int, input().split())

# Solve the problem and print the result
print(solve_magic_box(r1, r2, c1, c2, d1, d2))
