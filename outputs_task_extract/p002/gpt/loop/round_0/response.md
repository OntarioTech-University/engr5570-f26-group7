```python
def read_input():
    r1, r2 = map(int, input().split())
    c1, c2 = map(int, input().split())
    d1, d2 = map(int, input().split())
    return r1, r2, c1, c2, d1, d2


def compute_others(a, r1, c1, d1):
    b = r1 - a
    c = c1 - a
    d = d1 - a
    return b, c, d


def has_valid_distinct_values(a, b, c, d):
    if 1 <= b <= 9 and 1 <= c <= 9 and 1 <= d <= 9:
        s = {a, b, c, d}
        return len(s) == 4
    return False


def meets_remaining_constraints(b, c, d, r2, c2, d2):
    return c + d == r2 and b + d == c2 and b + c == d2


def find_result(r1, r2, c1, c2, d1, d2):
    for a in range(1, 10):
        b, c, d = compute_others(a, r1, c1, d1)
        if has_valid_distinct_values(a, b, c, d):
            if meets_remaining_constraints(b, c, d, r2, c2, d2):
                return True, [[a, b], [c, d]]
    return False, []


def print_output(found, result):
    if found:
        print(result[0][0], result[0][1])
        print(result[1][0], result[1][1])
    else:
        print(-1)


def main():
    values = read_input()
    found, result = find_result(*values)
    print_output(found, result)


main()
```

- Moved input reading and output printing into dedicated functions.
- Separated candidate calculation, validation, and constraint checks into small functions while retaining their order and logic.
- Kept the search in a short function and left only the call to `main()` at the top level.