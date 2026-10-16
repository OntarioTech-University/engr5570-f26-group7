import sys

def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    try:
        # Read the communication range R
        R = int(sys.stdin.readline())
        
        # Read the coordinates of the Chef, Head Server, and Sous-Chef
        Cx, Cy = map(int, sys.stdin.readline().split())
        Hx, Hy = map(int, sys.stdin.readline().split())
        Sx, Sy = map(int, sys.stdin.readline().split())
    except (ValueError, IndexError):
        # Handle potential malformed input for a test case
        return

    # Calculate the squared maximum distance for direct communication.
    # Using squared distances avoids floating-point arithmetic (sqrt),
    # which is faster and more precise.
    R_sq = R * R

    # Calculate the squared distance between each pair of people
    dist_sq_CH = (Cx - Hx)**2 + (Cy - Hy)**2
    dist_sq_CS = (Cx - Sx)**2 + (Cy - Sy)**2
    dist_sq_HS = (Hx - Sx)**2 + (Hy - Sy)**2

    # Count how many pairs are within direct communication range
    direct_links = 0
    if dist_sq_CH <= R_sq:
        direct_links += 1
    if dist_sq_CS <= R_sq:
        direct_links += 1
    if dist_sq_HS <= R_sq:
        direct_links += 1

    # For all three to communicate, the communication network (graph) must be
    # connected. With three people (nodes), the graph is connected if there
    # are at least two direct links (edges).
    if direct_links >= 2:
        print("yes")
    else:
        print("no")

def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        # Read the total number of test cases from the first line
        num_test_cases = int(sys.stdin.readline())
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        # Gracefully handle cases with invalid or missing input for T
        pass

if __name__ == "__main__":
    main()
