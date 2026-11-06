```python
def read_input():
    """Read the six input integers from three lines."""
    r1, r2 = map(int, input().split())
    c1, c2 = map(int, input().split())
    d1, d2 = map(int, input().split())
    return r1, r2, c1, c2, d1, d2


def is_valid_solution(a, b, c, d, r2, c2, d2):
    """Check whether the computed values satisfy all remaining constraints."""
    return (1 <= b <= 9 and 1 <= c <= 9 and 1 <= d <= 9 and
            len({a, b, c, d}) == 4 and
            c + d == r2 and b + d == c2 and b + c == d2)


def find_solution(r1, r2, c1, c2, d1, d2):
    """Find a valid 2x2 grid or return None if no solution exists."""
    for a in range(1, 10):
        b = r1 - a
        c = c1 - a
        d = d1 - a
        if is_valid_solution(a, b, c, d, r2, c2, d2):
            return [[a, b], [c, d]]
    return None


def print_solution(solution):
    """Print the solution grid or -1 if no solution was found."""
    if solution is None:
        print(-1)
    else:
        print(solution[0][0], solution[0][1])
        print(solution[1][0], solution[1][1])


def main():
    r1, r2, c1, c2, d1, d2 = read_input()
    solution = find_solution(r1, r2, c1, c2, d1, d2)
    print_solution(solution)


if __name__ == "__main__":
    main()
```

- Moved input reading into `read_input()` returning the six integers.
- Moved the main computation into `find_solution()` returning the solution grid or `None`.
- Moved output printing into `print_solution()`.
- Extracted validation logic into `is_valid_solution()` to reduce nesting and improve readability.
- Added `main()` and the `if __name__ == "__main__":` guard; no top-level logic or global variables remain.
- No duplicated code was present; the validation helper centralizes the condition checks.