```python
def _matches_sums(a, b, c, d, r1, r2, c1, c2, d1, d2):
    return (
        len({a, b, c, d}) == 4
        and a + b == r1
        and c + d == r2
        and a + c == c1
        and b + d == c2
        and a + d == d1
        and b + c == d2
    )


def solve_magic_box(r1, r2, c1, c2, d1, d2):
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    if _matches_sums(a, b, c, d, r1, r2, c1, c2, d1, d2):
                        return f"{a} {b}\n{c} {d}"
    return "-1"


def _read_input():
    r1, r2 = map(int, input().split())
    c1, c2 = map(int, input().split())
    d1, d2 = map(int, input().split())
    return r1, r2, c1, c2, d1, d2


def _print_result(result):
    print(result)


def _run():
    values = _read_input()
    result = solve_magic_box(*values)
    _print_result(result)


_run()
```

- Extracted the candidate check so `solve_magic_box` focuses on searching, without changing search order or conditions.
- Moved input reading and output printing into separate functions, with a short function coordinating them. The file still runs on import, as before.