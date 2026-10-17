def _read_rows(data, idx, count):
    rows = []
    for _ in range(count):
        rows.append(data[idx])
        idx += 1
    return rows, idx


def _cell_matches(table, pattern, row, col, n, m, r, c):
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(row + x) % n][(col + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def _build_match_grid(table, pattern, n, m, r, c):
    ans = [['0'] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if _cell_matches(table, pattern, i, j, n, m, r, c):
                ans[i][j] = '1'

    return ans


def _print_grid(grid):
    for row in grid:
        print(''.join(row))


def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    idx = 0
    n, m = map(int, data[idx].split())
    idx += 1

    table, idx = _read_rows(data, idx, n)

    r, c = map(int, data[idx].split())
    idx += 1

    pattern, idx = _read_rows(data, idx, r)

    ans = _build_match_grid(table, pattern, n, m, r, c)
    _print_grid(ans)


if __name__ == "__main__":
    main()
