```python
import sys


def _squared_distance(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    try:
        R = int(sys.stdin.readline())
        Cx, Cy = map(int, sys.stdin.readline().split())
        Hx, Hy = map(int, sys.stdin.readline().split())
        Sx, Sy = map(int, sys.stdin.readline().split())
    except (ValueError, IndexError):
        return

    # Compare squared distances to avoid floating-point arithmetic.
    R_sq = R * R
    dist_sq_CH = _squared_distance(Cx, Cy, Hx, Hy)
    dist_sq_CS = _squared_distance(Cx, Cy, Sx, Sy)
    dist_sq_HS = _squared_distance(Hx, Hy, Sx, Sy)

    # Three people can all communicate when at least two pairs are linked.
    direct_links = (
        (dist_sq_CH <= R_sq)
        + (dist_sq_CS <= R_sq)
        + (dist_sq_HS <= R_sq)
    )
    print("yes" if direct_links >= 2 else "no")


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

- Extracted the repeated squared-distance calculation into a small, named helper.
- Replaced three link-counting branches with a single expression and simplified the final output branch. Input handling and public interfaces remain unchanged.