```python
def read_input():
    import sys

    input = sys.stdin.read
    data = input().splitlines()

    idx = 0
    n, m = map(int, data[idx].split())
    idx += 1

    table = []
    for _ in range(n):
        table.append(data[idx])
        idx += 1

    r, c = map(int, data[idx].split())
    idx += 1

    pattern = []
    for _ in range(r):
        pattern.append(data[idx])
        idx += 1

    return n, m, table, r, c, pattern


def compute_answer(n, m, table, r, c, pattern):
    ans = [['0'] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            match = True
            for x in range(r):
                for y in range(c):
                    pat_char = pattern[x][y]
                    tbl_char = table[(i + x) % n][(j + y) % m]
                    if pat_char != '?' and pat_char != tbl_char:
                        match = False
                        break
                if not match:
                    break
            if match:
                ans[i][j] = '1'

    return ans


def print_answer(ans):
    for row in ans:
        print(''.join(row))


def main():
    n, m, table, r, c, pattern = read_input()
    ans = compute_answer(n, m, table, r, c, pattern)
    print_answer(ans)


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and printing into functions that pass data through parameters and return values.
- Kept the matching and parsing logic unchanged to preserve behavior. There was no duplicated code to extract into a helper.
- Left only the `main()` call under the execution guard; no variables are global.