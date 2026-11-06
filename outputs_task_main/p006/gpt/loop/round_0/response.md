```python
import sys


def read_test_case():
    """Read one test case, returning None if its input is malformed."""
    try:
        R = int(sys.stdin.readline())
        Cx, Cy = map(int, sys.stdin.readline().split())
        Hx, Hy = map(int, sys.stdin.readline().split())
        Sx, Sy = map(int, sys.stdin.readline().split())
    except (ValueError, IndexError):
        return None

    return R, (Cx, Cy), (Hx, Hy), (Sx, Sy)


def squared_distance(first, second):
    return (first[0] - second[0])**2 + (first[1] - second[1])**2


def compute_result(R, chef, head_server, sous_chef):
    """Determine whether the three-person communication network is connected."""
    R_sq = R * R
    direct_links = 0

    for first, second in (
        (chef, head_server),
        (chef, sous_chef),
        (head_server, sous_chef),
    ):
        if squared_distance(first, second) <= R_sq:
            direct_links += 1

    return "yes" if direct_links >= 2 else "no"


def print_result(result):
    print(result)


def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    test_case = read_test_case()
    if test_case is None:
        return

    print_result(compute_result(*test_case))


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        num_test_cases = int(sys.stdin.readline())
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        pass


if __name__ == "__main__":
    main()
```

- Separated test-case input, computation, and output into functions, passing data through parameters and return values.
- Replaced repeated distance calculations with a shared helper.
- Kept `solve()` and `main()` signatures, input order, exception handling, and printed output unchanged.