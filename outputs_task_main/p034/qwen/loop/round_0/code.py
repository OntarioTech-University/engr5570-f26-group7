def read_input_lines():
    import sys
    input = sys.stdin.read
    return input().splitlines()


def read_block(data, idx, count):
    block = []
    for _ in range(count):
        block.append(data[idx])
        idx += 1
    return block, idx


def parse_input(data):
    idx = 0

    n, m = map(int, data[idx].split())
    idx += 1

    table, idx = read_block(data, idx, n)

    r, c = map(int, data[idx].split())
    idx += 1

    pattern, idx = read_block(data, idx, r)

    return n, m, table, r, c, pattern


def create_answer_grid(n, m):
    return [['0'] * m for _ in range(n)]


def matches_at(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(i + x) % n][(j + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def compute_answer(table, pattern, n, m, r, c):
    ans = create_answer_grid(n, m)

    for i in range(n):
        for j in range(m):
            if matches_at(table, pattern, n, m, r, c, i, j):
                ans[i][j] = '1'

    return ans


def print_answer(ans):
    for row in ans:
        print(''.join(row))


def main():
    data = read_input_lines()
    n, m, table, r, c, pattern = parse_input(data)
    ans = compute_answer(table, pattern, n, m, r, c)
    print_answer(ans)


if __name__ == "__main__":
    main()
