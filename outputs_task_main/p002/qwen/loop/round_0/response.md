```python
def read_pair():
    return map(int, input().split())


def read_inputs():
    r1, r2 = read_pair()
    c1, c2 = read_pair()
    d1, d2 = read_pair()
    return r1, r2, c1, c2, d1, d2


def find_solution(r1, r2, c1, c2, d1, d2):
    for a in range(1, 10):
        b = r1 - a
        c = c1 - a
        d = d1 - a

        if 1 <= b <= 9 and 1 <= c <= 9 and 1 <= d <= 9:
            s = {a, b, c, d}
            if len(s) == 4:
                if c + d == r2 and b + d == c2 and b + c == d2:
                    return [[a, b], [c, d]]

    return None


def print_result(result):
    if result is not None:
        print(result[0][0], result[0][1])
        print(result[1][0], result[1][1])
    else:
        print(-1)


def main():
    r1, r2, c1, c2, d1, d2 = read_inputs()
    result = find_solution(r1, r2, c1, c2, d1, d2)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved input reading into `read_inputs()` and a shared `read_pair()` helper, eliminating repeated input-parsing code while preserving the original three-input sequence and exception behavior.
- Moved the core search logic into `find_solution()`, passing all needed values as parameters and returning the first valid result or `None`, matching the original control flow.
- Moved output handling into `print_result()`, preserving the exact printed output for both success and failure cases.
- Removed top-level mutable state (`found`, `result`) and replaced it with local variables and function return values.
- Added a `main()` function and invoked it only under `if __name__ == "__main__":`, preventing program logic from running at import time.