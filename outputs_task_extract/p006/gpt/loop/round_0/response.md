```python
import sys


def _read_test_case():
    R = int(sys.stdin.readline())
    Cx, Cy = map(int, sys.stdin.readline().split())
    Hx, Hy = map(int, sys.stdin.readline().split())
    Sx, Sy = map(int, sys.stdin.readline().split())
    return R, (Cx, Cy), (Hx, Hy), (Sx, Sy)


def _calculate_distances(chef, head_server, sous_chef):
    Cx, Cy = chef
    Hx, Hy = head_server
    Sx, Sy = sous_chef
    dist_sq_CH = (Cx - Hx)**2 + (Cy - Hy)**2
    dist_sq_CS = (Cx - Sx)**2 + (Cy - Sy)**2
    dist_sq_HS = (Hx - Sx)**2 + (Hy - Sy)**2
    return dist_sq_CH, dist_sq_CS, dist_sq_HS


def _count_direct_links(R, distances):
    R_sq = R * R
    dist_sq_CH, dist_sq_CS, dist_sq_HS = distances
    direct_links = 0
    if dist_sq_CH <= R_sq:
        direct_links += 1
    if dist_sq_CS <= R_sq:
        direct_links += 1
    if dist_sq_HS <= R_sq:
        direct_links += 1
    return direct_links


def _print_result(direct_links):
    if direct_links >= 2:
        print("yes")
    else:
        print("no")


def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    try:
        R, chef, head_server, sous_chef = _read_test_case()
    except (ValueError, IndexError):
        return

    distances = _calculate_distances(chef, head_server, sous_chef)
    direct_links = _count_direct_links(R, distances)
    _print_result(direct_links)


def _read_test_case_count():
    return int(sys.stdin.readline())


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        num_test_cases = _read_test_case_count()
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        pass


if __name__ == "__main__":
    main()
```

- Separated input reading, distance calculation, link counting, and output printing into small, single-purpose functions.
- Kept `solve()` and `main()` signatures, computation order, and exception-handling boundaries unchanged.