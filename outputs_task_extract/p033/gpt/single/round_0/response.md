```python
def _read_dimensions():
    return map(int, input().split())


def _read_rows(count):
    return [list(input()) for _ in range(count)]


def _matches(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            if pattern[x][y] != '?' and pattern[x][y] != table[(i + x) % n][(j + y) % m]:
                return False
    return True


def solve(n, m, table, r, c, pattern):
    result = [['0' for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if _matches(table, pattern, n, m, r, c, i, j):
                result[i][j] = '1'

    return result


def _print_result(result):
    for row in result:
        print(''.join(row))


n, m = _read_dimensions()
table = _read_rows(n)

r, c = _read_dimensions()
pattern = _read_rows(r)

result = solve(n, m, table, r, c, pattern)
_print_result(result)
```

- Moved dimension and row reading into small functions while retaining the original input order and module-level assignments.
- Extracted the matching check so `solve` focuses on constructing the result; its public signature is unchanged.
- Moved output printing into its own function without changing the printed rows.