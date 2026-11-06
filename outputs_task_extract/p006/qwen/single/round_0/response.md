```python
import sys


def read_test_case_count():
    """Read the total number of test cases."""
    return int(sys.stdin.readline())


def read_range():
    """Read the communication range for a test case."""
    return int(sys.stdin.readline())


def read_point():
    """Read a single coordinate pair."""
    x, y = map(int, sys.stdin.readline().split())
    return x, y


def read_test_case():
    """Read all values needed for one test case."""
    R = read_range()
    chef = read_point()
    head_server = read_point()
    sous_chef = read_point()
    return R, chef, head_server, sous_chef


def square(value):
    """Return the square of a number."""
    return value * value


def squared_distance(point_a, point_b):
    """Return the squared distance between two 2D points."""
    return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2


def count_direct_links(range_squared, chef, head_server, sous_chef):
    """Count pairs of people that are within direct communication range."""
    direct_links = 0

    if squared_distance(chef, head_server) <= range_squared:
        direct_links += 1
    if squared_distance(chef, sous_chef) <= range_squared:
        direct_links += 1
    if squared_distance(head_server, sous_chef) <= range_squared:
        direct_links += 1

    return direct_links


def is_connected(direct_links):
    """Return True if the three-person communication network is connected."""
    return direct_links >= 2


def print_result(is_network_connected):
    """Print the answer for one test case."""
    if is_network_connected:
        print("yes")
    else:
        print("no")


def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    try:
        R, chef, head_server, sous_chef = read_test_case()
    except (ValueError, IndexError):
        # Handle potential malformed input for a test case
        return

    range_squared = square(R)
    direct_links = count_direct_links(range_squared, chef, head_server, sous_chef)
    print_result(is_connected(direct_links))


def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        num_test_cases = read_test_case_count()
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        # Gracefully handle cases with invalid or missing input for T
        pass


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_test_case_count`, `read_range`, `read_point`, and `read_test_case` so input handling is isolated and the original exception flow is preserved.
- Extracted arithmetic helpers `square` and `squared_distance` to keep distance calculations small and reusable.
- Moved pair-range counting into `count_direct_links` so the counting logic is separate from input and output.
- Moved the connectivity decision into `is_connected` to make the graph-connectivity rule explicit.
- Moved output printing into `print_result` so `solve` only orchestrates the test case.
- Kept `solve` and `main` signatures unchanged, preserving the public interface and runtime behavior.