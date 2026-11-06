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


def read_input():
    n, m = map(int, input().split())
    table = [list(input()) for _ in range(n)]

    r, c = map(int, input().split())
    pattern = [list(input()) for _ in range(r)]

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

- Moved input reading and output printing into separate functions, with data passed through parameters and return values.
- Added a guarded `main()` so execution logic does not run on import.
- Kept `solve` unchanged; there was no duplicated logic to extract.