def _matches_pattern_at(table, pattern, n, m, start_i, start_j, r, c):
    """Check if pattern matches table at the given starting position."""
    for x in range(r):
        for y in range(c):
            pattern_char = pattern[x][y]
            table_char = table[(start_i + x) % n][(start_j + y) % m]
            if pattern_char != '?' and pattern_char != table_char:
                return False
    return True


def solve(n, m, table, r, c, pattern):
    result = [['0' for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if _matches_pattern_at(table, pattern, n, m, i, j, r, c):
                result[i][j] = '1'

    return result


def main():
    n, m = map(int, input().split())
    table = [list(input()) for _ in range(n)]

    r, c = map(int, input().split())
    pattern = [list(input()) for _ in range(r)]

    result = solve(n, m, table, r, c, pattern)

    for row in result:
        print(''.join(row))


if __name__ == '__main__':
    main()
