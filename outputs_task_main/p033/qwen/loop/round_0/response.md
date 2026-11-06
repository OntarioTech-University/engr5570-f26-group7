```python
def solve(n, m, table, r, c, pattern):
    result = [['0' for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            match = True
            for x in range(r):
                for y in range(c):
                    if pattern[x][y] != '?' and pattern[x][y] != table[(i + x) % n][(j + y) % m]:
                        match = False
                        break
                if not match:
                    break
            if match:
                result[i][j] = '1'

    return result


def _read_dimensions():
    return map(int, input().split())


def _read_grid(row_count):
    return [list(input()) for _ in range(row_count)]


def read_input():
    n, m = _read_dimensions()
    table = _read_grid(n)

    r, c = _read_dimensions()
    pattern = _read_grid(r)

    return n, m, table, r, c, pattern


def print_result(result):
    for row in result:
        print(''.join(row))


def main():
    n, m, table, r, c, pattern = read_input()
    result = solve(n, m, table, r, c, pattern)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved all script execution into `main()` guarded by `if __name__ == "__main__":` so nothing runs at import time.
- Added `read_input()` to centralize stdin parsing and return all input data explicitly.
- Added `print_result()` to isolate output formatting and printing.
- Extracted repeated grid reading into `_read_grid()` and repeated dimension parsing into `_read_dimensions()`.
- Kept `solve()`’s signature and internal algorithm unchanged to preserve existing behavior, return values, and exception conditions.