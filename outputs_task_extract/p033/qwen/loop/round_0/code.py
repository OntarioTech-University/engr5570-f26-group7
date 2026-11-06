def create_result_grid(n, m):
    return [['0' for _ in range(m)] for _ in range(n)]


def matches_at(n, m, table, r, c, pattern, i, j):
    for x in range(r):
        for y in range(c):
            if (pattern[x][y] != '?' and
                    pattern[x][y] != table[(i + x) % n][(j + y) % m]):
                return False
    return True


def fill_matches(result, n, m, table, r, c, pattern):
    for i in range(n):
        for j in range(m):
            if matches_at(n, m, table, r, c, pattern, i, j):
                result[i][j] = '1'


def solve(n, m, table, r, c, pattern):
    result = create_result_grid(n, m)
    fill_matches(result, n, m, table, r, c, pattern)
    return result


def read_dimensions():
    n, m = map(int, input().split())
    return n, m


def read_table(n):
    return [list(input()) for _ in range(n)]


def read_pattern_dimensions():
    r, c = map(int, input().split())
    return r, c


def read_pattern(r):
    return [list(input()) for _ in range(r)]


def print_result(result):
    for row in result:
        print(''.join(row))


def main():
    n, m = read_dimensions()
    table = read_table(n)
    r, c = read_pattern_dimensions()
    pattern = read_pattern(r)
    result = solve(n, m, table, r, c, pattern)
    print_result(result)


main()
