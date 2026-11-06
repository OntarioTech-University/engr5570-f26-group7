```python
def read_two_ints():
    return tuple(map(int, input().split()))


def read_grid(rows):
    return [list(input()) for _ in range(rows)]


def print_result(result):
    for row in result:
        print(''.join(row))


def _create_empty_result(n, m):
    return [['0' for _ in range(m)] for _ in range(n)]


def _matches_at(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            if pattern[x][y] != '?' and pattern[x][y] != table[(i + x) % n][(j + y) % m]:
                return False
    return True


def solve(n, m, table, r, c, pattern):
    result = _create_empty_result(n, m)

    for i in range(n):
        for j in range(m):
            if _matches_at(table, pattern, n, m, r, c, i, j):
                result[i][j] = '1'

    return result


def main():
    n, m = read_two_ints()
    table = read_grid(n)

    r, c = read_two_ints()
    pattern = read_grid(r)

    result = solve(n, m, table, r, c, pattern)

    print_result(result)


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_two_ints` and `read_grid` to separate parsing from computation.
- Extracted output printing into `print_result` to isolate side effects.
- Extracted pattern matching into `_matches_at` so the matching logic is a single, focused function.
- Extracted result initialization into `_create_empty_result` to clarify the setup step.
- Kept `solve` as the public interface, now delegating to small helpers while preserving its exact signature and behavior.
- Moved top-level script logic into `main` guarded by `if __name__ == "__main__"` to avoid execution on import.