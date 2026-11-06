```python
def read_pair():
    return tuple(map(int, input().split()))


def read_input():
    r1, r2 = read_pair()
    c1, c2 = read_pair()
    d1, d2 = read_pair()
    return r1, r2, c1, c2, d1, d2


def compute_result(r1, r2, c1, c2, d1, d2):
    found = False
    result = []

    for a in range(1, 10):
        b = r1 - a
        c = c1 - a
        d = d1 - a

        if 1 <= b <= 9 and 1 <= c <= 9 and 1 <= d <= 9:
            s = {a, b, c, d}
            if len(s) == 4:
                if c + d == r2 and b + d == c2 and b + c == d2:
                    found = True
                    result = [[a, b], [c, d]]
                    break

    return found, result


def print_result(found, result):
    if found:
        for row in result:
            print(row[0], row[1])
    else:
        print(-1)


def main():
    values = read_input()
    found, result = compute_result(*values)
    print_result(found, result)


if __name__ == "__main__":
    main()
```

- Moved input, computation, and output into separate functions, with data passed through parameters and return values.
- Consolidated repeated input parsing and row printing while retaining the original search and output behavior.
- Placed the program entry point under the `__main__` guard, so importing the file does not run it.