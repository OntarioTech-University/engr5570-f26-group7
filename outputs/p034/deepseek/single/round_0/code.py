def read_grid(data, idx, rows):
    """Read a grid of given row count from data starting at idx."""
    grid = []
    for _ in range(rows):
        grid.append(data[idx])
        idx += 1
    return grid, idx


def parse_input(data):
    """Parse the input data and return table, pattern, and their dimensions."""
    idx = 0
    n, m = map(int, data[idx].split())
    idx += 1

    table, idx = read_grid(data, idx, n)

    r, c = map(int, data[idx].split())
    idx += 1

    pattern, idx = read_grid(data, idx, r)

    return table, pattern, n, m, r, c


def matches_pattern(table, pattern, n, m, r, c, i, j):
    """Check if pattern matches table at position (i, j) with cyclic wrapping."""
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(i + x) % n][(j + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def build_answer_grid(table, pattern, n, m, r, c):
    """Build the answer grid by checking pattern matches at each position."""
    ans = [['0'] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if matches_pattern(table, pattern, n, m, r, c, i, j):
                ans[i][j] = '1'

    return ans


def print_grid(grid):
    """Print the grid row by row."""
    for row in grid:
        print(''.join(row))


def main():
    import sys
    data = sys.stdin.read().splitlines()

    table, pattern, n, m, r, c = parse_input(data)
    ans = build_answer_grid(table, pattern, n, m, r, c)
    print_grid(ans)


if __name__ == "__main__":
    main()
