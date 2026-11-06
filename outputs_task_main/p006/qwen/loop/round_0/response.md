```python
import sys


def _read_int():
    return int(sys.stdin.readline())


def _read_point():
    x, y = map(int, sys.stdin.readline().split())
    return x, y


def _read_test_case():
    R = _read_int()
    chef = _read_point()
    head_server = _read_point()
    sous_chef = _read_point()
    return R, chef, head_server, sous_chef


def _squared_distance(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b
    return (ax - bx) ** 2 + (ay - by) ** 2


def _count_direct_links(R, chef, head_server, sous_chef):
    R_sq = R * R

    dist_sq_CH = _squared_distance(chef, head_server)
    dist_sq_CS = _squared_distance(chef, sous_chef)
    dist_sq_HS = _squared_distance(head_server, sous_chef)

    direct_links = 0
    if dist_sq_CH <= R_sq:
        direct_links += 1
    if dist_sq_CS <= R_sq:
        direct_links += 1
    if dist_sq_HS <= R_sq:
        direct_links += 1

    return direct_links


def _format_result(direct_links):
    if direct_links >= 2:
        return "yes"
    return "no"


def _print_result(result):
    print(result)


def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    try:
        R, chef, head_server, sous_chef = _read_test_case()
    except (ValueError, IndexError):
        # Handle potential malformed input for a test case
        return

    direct_links = _count_direct_links(R, chef, head_server, sous_chef)
    result = _format_result(direct_links)
    _print_result(result)


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        num_test_cases = _read_int()
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        # Gracefully handle cases with invalid or missing input for T
        pass


if __name__ == "__main__":
    main()
```

- Added `_read_int` and `_read_point` to centralize repeated input parsing, removing duplicated reading logic.
- Added `_read_test_case` so `solve` only coordinates the test-case workflow instead of containing all raw input handling.
- Moved the repeated squared-distance calculation into `_squared_distance`, eliminating duplicated arithmetic.
- Moved the core computation into `_count_direct_links` and answer formatting into `_format_result`, separating computation from input/output.
- Added `_print_result` to isolate output side effects.
- Kept `solve()` and `main()` signatures, exception handling, and observable behavior unchanged.