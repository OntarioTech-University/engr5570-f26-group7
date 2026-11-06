```python
def _read_pair():
    first, second = map(int, input().split())
    return first, second


def _read_magic_box_input():
    r1, r2 = _read_pair()
    c1, c2 = _read_pair()
    d1, d2 = _read_pair()
    return r1, r2, c1, c2, d1, d2


def _candidate_assignments():
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    yield a, b, c, d


def _is_magic_arrangement(a, b, c, d, r1, r2, c1, c2, d1, d2):
    return (
        len({a, b, c, d}) == 4 and
        a + b == r1 and
        c + d == r2 and
        a + c == c1 and
        b + d == c2 and
        a + d == d1 and
        b + c == d2
    )


def _format_magic_box(a, b, c, d):
    return f"{a} {b}\n{c} {d}"


def solve_magic_box(r1, r2, c1, c2, d1, d2):
    for a, b, c, d in _candidate_assignments():
        if _is_magic_arrangement(a, b, c, d, r1, r2, c1, c2, d1, d2):
            return _format_magic_box(a, b, c, d)
    return "-1"


def _print_result(result):
    print(result)


def _main():
    r1, r2, c1, c2, d1, d2 = _read_magic_box_input()
    result = solve_magic_box(r1, r2, c1, c2, d1, d2)
    _print_result(result)


_main()
```

- Extracted input parsing into `_read_pair` and `_read_magic_box_input`, keeping the original stdin behavior and unpacking semantics.
- Split the brute-force logic into `_candidate_assignments` and `_is_magic_arrangement`, preserving the original search order and condition evaluation.
- Moved result formatting into `_format_magic_box` and output printing into `_print_result`, separating computation from side effects.
- Kept `solve_magic_box`’s public signature and return behavior unchanged, with `_main()` orchestrating the script without changing runtime output.