import sys

def read_test_case():
    """Reads a single test case from stdin. Returns None on malformed input."""
    try:
        R = int(sys.stdin.readline())
        Cx, Cy = map(int, sys.stdin.readline().split())
        Hx, Hy = map(int, sys.stdin.readline().split())
        Sx, Sy = map(int, sys.stdin.readline().split())
    except (ValueError, IndexError):
        return None
    return R, Cx, Cy, Hx, Hy, Sx, Sy

def squared_distance(x1, y1, x2, y2):
    """Returns the squared Euclidean distance between two points."""
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def can_communicate(R, Cx, Cy, Hx, Hy, Sx, Sy):
    """Determines if all three people can communicate."""
    R_sq = R * R
    direct_links = sum([
        squared_distance(Cx, Cy, Hx, Hy) <= R_sq,
        squared_distance(Cx, Cy, Sx, Sy) <= R_sq,
        squared_distance(Hx, Hy, Sx, Sy) <= R_sq,
    ])
    return direct_links >= 2

def print_result(can_communicate_result):
    """Prints the result for a test case."""
    if can_communicate_result:
        print("yes")
    else:
        print("no")

def solve():
    """Solves a single test case for the Chef and Transceivers problem."""
    test_case = read_test_case()
    if test_case is None:
        return
    R, Cx, Cy, Hx, Hy, Sx, Sy = test_case
    result = can_communicate(R, Cx, Cy, Hx, Hy, Sx, Sy)
    print_result(result)

def main():
    """Main function to handle the number of test cases."""
    try:
        num_test_cases = int(sys.stdin.readline())
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()
