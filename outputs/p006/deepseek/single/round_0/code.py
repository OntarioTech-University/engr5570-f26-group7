import sys

def read_int():
    """Read a single integer from stdin."""
    return int(sys.stdin.readline())

def read_coordinates():
    """Read a pair of coordinates from stdin."""
    return map(int, sys.stdin.readline().split())

def squared_distance(x1, y1, x2, y2):
    """Calculate the squared distance between two points."""
    return (x1 - x2)**2 + (y1 - y2)**2

def count_direct_links(distances, max_distance_sq):
    """Count how many distances are within the communication range."""
    return sum(1 for distance in distances if distance <= max_distance_sq)

def read_test_case():
    """
    Read a single test case.
    Returns (R, coordinates) or None if input is malformed.
    """
    try:
        R = read_int()
        chef = read_coordinates()
        head_server = read_coordinates()
        sous_chef = read_coordinates()
        return R, chef, head_server, sous_chef
    except (ValueError, IndexError):
        return None

def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    test_case = read_test_case()
    if test_case is None:
        return

    R, (Cx, Cy), (Hx, Hy), (Sx, Sy) = test_case

    # Calculate the squared maximum distance for direct communication.
    # Using squared distances avoids floating-point arithmetic (sqrt),
    # which is faster and more precise.
    R_sq = R * R

    # Calculate the squared distance between each pair of people
    distances = [
        squared_distance(Cx, Cy, Hx, Hy),
        squared_distance(Cx, Cy, Sx, Sy),
        squared_distance(Hx, Hy, Sx, Sy)
    ]

    # Count how many pairs are within direct communication range
    direct_links = count_direct_links(distances, R_sq)

    # For all three to communicate, the communication network (graph) must be
    # connected. With three people (nodes), the graph is connected if there
    # are at least two direct links (edges).
    print("yes" if direct_links >= 2 else "no")

def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        num_test_cases = read_int()
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        # Gracefully handle cases with invalid or missing input for T
        pass

if __name__ == "__main__":
    main()
