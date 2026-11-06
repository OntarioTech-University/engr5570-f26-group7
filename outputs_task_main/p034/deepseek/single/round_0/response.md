```
def _read_pair(data, idx):
    a, b = map(int, data[idx].split())
    return a, b, idx + 1


def _read_lines(data, idx, count):
    lines = []
    for _ in range(count):
        lines.append(data[idx])
        idx += 1
    return lines, idx


def read_input():
    import sys
    data = sys.stdin.read().splitlines()
    idx = 0

    n, m, idx = _read_pair(data, idx)
    table, idx = _read_lines(data, idx, n)

    r, c, idx = _read_pair(data, idx)
    pattern, idx = _read_lines(data, idx, r)

    return n, m, table, r, c, pattern


def _matches_at(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(i + x) % n][(j + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def compute_matches(n, m, table, r, c, pattern):
    ans = [['0'] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if _matches_at(table, pattern, n, m, r, c, i, j):
                ans[i][j] = '1'

    return ans


def print_result(ans):
    for row in ans:
        print(''.join(row))


def main():
    n, m, table, r, c, pattern = read_input()
    ans = compute_matches(n, m, table, r, c, pattern)
    print_result(ans)


if __name__ == "__main__":
    main()
```