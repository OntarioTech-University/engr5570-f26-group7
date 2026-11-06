```python
def read_pair():
    return map(int, input().split())


def read_input():
    r1, r2 = read_pair()
    c1, c2 = read_pair()
    d1, d2 = read_pair()
    return r1, r2, c1, c2, d1, d2


def print_result(result):
    print(result)


def solve_magic_box(r1, r2, c1, c2, d1, d2):
    # Iterate through all possible combinations of a, b, c, and d
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    if len({a, b, c, d}) == 4 and \
                       a + b == r1 and \
                       c + d == r2 and \
                       a + c == c1 and \
                       b + d == c2 and \
                       a + d == d1 and \
                       b + c == d2:
                        return f"{a} {b}\n{c} {d}"
    return "-1"


def main():
    r1, r2, c1, c2, d1, d2 = read_input()
    result = solve_magic_box(r1, r2, c1, c2, d1, d2)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved input reading into `read_input()` and extracted a shared `read_pair()` helper to remove duplicated `map(int, input().split())` calls.
- Moved output printing into `print_result()` to separate concerns.
- Added `main()` to orchestrate input, computation, and output, passing data through parameters and return values.
- Wrapped script execution in `if __name__ == "__main__":` so no logic runs at the top level when the module is imported.
- Kept `solve_magic_box` signature and internal logic unchanged to preserve public interface and runtime behavior.