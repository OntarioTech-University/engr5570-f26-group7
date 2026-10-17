def _matches_at(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(i + x) % n][(j + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    idx = 0
    n, m = map(int, data[idx].split())
    idx += 1

    # Read the cyclic table
    table = []
    for _ in range(n):
        table.append(data[idx])
        idx += 1

    r, c = map(int, data[idx].split())
    idx += 1

    # Read the pattern
    pattern = []
    for _ in range(r):
        pattern.append(data[idx])
        idx += 1

    # Initialize answer grid
    ans = [['0'] * m for _ in range(n)]

    # Check for each cell (i,j) in the table
    for i in range(n):
        for j in range(m):
            if _matches_at(table, pattern, n, m, r, c, i, j):
                ans[i][j] = '1'

    # Print the result
    for row in ans:
        print(''.join(row))


if __name__ == "__main__":
    main()
