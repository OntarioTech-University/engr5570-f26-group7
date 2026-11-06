```python
def read_input_lines():
    import sys
    return sys.stdin.read().splitlines()


def read_dimensions(data, idx):
    rows, cols = map(int, data[idx].split())
    return rows, cols, idx + 1


def read_rows(data, idx, count):
    rows = []
    for _ in range(count):
        rows.append(data[idx])
        idx += 1
    return rows, idx


def initialize_answer(n, m):
    return [['0'] * m for _ in range(n)]


def pattern_matches_at(table, pattern, n, m, r, c, i, j):
    for x in range(r):
        for y in range(c):
            pat_char = pattern[x][y]
            tbl_char = table[(i + x) % n][(j + y) % m]
            if pat_char != '?' and pat_char != tbl_char:
                return False
    return True


def build_answer(table, pattern, n, m, r, c):
    ans = initialize_answer(n, m)
    for i in range(n):
        for j in range(m):
            if pattern_matches_at(table, pattern, n, m, r, c, i, j):
                ans[i][j] = '1'
    return ans


def print_answer(ans):
    for row in ans:
        print(''.join(row))


def main():
    data = read_input_lines()
    idx = 0
    n, m, idx = read_dimensions(data, idx)
    table, idx = read_rows(data, idx, n)
    r, c, idx = read_dimensions(data, idx)
    pattern, idx = read_rows(data, idx, r)
    ans = build_answer(table, pattern, n, m, r, c)
    print_answer(ans)


if __name__ == "__main__":
    main()
```

- Extracted stdin reading into `read_input_lines` to isolate input acquisition.
- Added `read_dimensions` and `read_rows` to parse input sequentially while preserving the original index advancement and exception behavior.
- Moved answer-grid creation into `initialize_answer` to separate initialization from matching logic.
- Extracted the nested match check into `pattern_matches_at`, preserving the original comparison order and early-exit behavior.
- Added `build_answer` to construct the result grid and `print_answer` to handle output.
- Kept `main()` as the public entry point, now only orchestrating the same steps in the same order.