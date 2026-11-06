def read_rows(data, idx, count):
    rows = []
    for _ in range(count):
        rows.append(data[idx])
        idx += 1
    return rows, idx


def read_input():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    idx = 0
    n, m = map(int, data[idx].split())
    idx += 1
    table, idx = read_rows(data, idx, n)

    r, c = map(int, data[idx].split())
    idx += 1
    pattern, idx = read_rows(data, idx, r)
    return n, m, table, r, c, pattern


def matches_at(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(i + x) % n][(j + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def build_answer(n, m, table, r, c, pattern):
    ans = [['0'] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if matches_at(table, pattern, n, m, r, c, i, j):
                ans[i][j] = '1'
    return ans


def print_answer(ans):
    for row in ans:
        print(''.join(row))


def main():
    n, m, table, r, c, pattern = read_input()
    ans = build_answer(n, m, table, r, c, pattern)
    print_answer(ans)


if __name__ == "__main__":
    main()
