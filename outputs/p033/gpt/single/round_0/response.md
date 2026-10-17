```python
def _matches_at(n, m, table, r, c, pattern, i, j):
    for x in range(r):
        for y in range(c):
            if pattern[x][y] != '?' and pattern[x][y] != table[(i + x) % n][(j + y) % m]:
                return False
    return True


def solve(n, m, table, r, c, pattern):
    result = [['0' for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if _matches_at(n, m, table, r, c, pattern, i, j):
                result[i][j] = '1'

    return result


n, m = map(int, input().split())
table = [list(input()) for _ in range(n)]

r, c = map(int, input().split())
pattern = [list(input()) for _ in range(r)]

result = solve(n, m, table, r, c, pattern)

for row in result:
    print(''.join(row))
```

- Extracted the pattern check into `_matches_at`, making `solve` easier to read.
- Replaced the match flag and nested breaks with an early return, preserving the comparison logic.