```python
def read_input():
    r1, r2 = map(int, input().split())
    c1, c2 = map(int, input().split())
    d1, d2 = map(int, input().split())
    return r1, r2, c1, c2, d1, d2


def find_solution(r1, r2, c1, c2, d1, d2):
    for a in range(1, 10):
        b = r1 - a
        c = c1 - a
        d = d1 - a

        if not all(1 <= x <= 9 for x in (b, c, d)):
            continue

        if len({a, b, c, d}) != 4:
            continue

        if c + d == r2 and b + d == c2 and b + c == d2:
            return [[a, b], [c, d]]

    return None


def print_solution(solution):
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

- Split input reading into `read_input()` so all parsing is isolated and easy to locate.
- Moved the core search logic into `find_solution()` with a single clear responsibility: find and return the valid grid or `None`.
- Extracted output formatting and printing into `print_solution()` to separate presentation from computation.
- Added a `main()` function to orchestrate the three steps, leaving no logic at the top level.
- Preserved the original behavior, including input parsing, validation order, distinctness checks, and output format.