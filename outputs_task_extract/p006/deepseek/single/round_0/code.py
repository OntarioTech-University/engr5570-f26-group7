import sys

def read_int():
    """Read a single integer from stdin."""
    return int(sys.stdin.readline())

def read_coordinates():
    """Read a pair of coordinates from stdin."""
    return map(int, sys.stdin.readline().split())

def read_test_case_data():
    """Read all data for a single test case."""
    R = read_int()
    Cx, Cy = read_coordinates()
    Hx, Hy = read_coordinates()
    Sx, Sy = read_coordinates()
    return R, (Cx, Cy), (Hx, Hy), (Sx, Sy)

def calculate_squared_distance(point1, point2):
    """Calculate squared distance between two points."""
    x1, y1 = point1
    x2, y2 = point2
    return (x1 - x2)**2 + (y1 - y2)**2

def count_direct_links(R_sq, chef, head_server, sous_chef):
    """Count how many pairs are within direct communication range."""
    direct_links = 0
    
    if calculate_squared_distance(chef, head_server) <= R_sq:
        direct_links += 1
    if calculate_squared_distance(chef, sous_chef) <= R_sq:
        direct_links += 1
    if calculate_squared_distance(head_server, sous_chef) <= R_sq:
        direct_links += 1
    
    return direct_links

def is_network_connected(direct_links):
    """Check if the communication network is connected."""
    return direct_links >= 2

def print_result(is_connected):
    """Print the result for a test case."""
    if is_connected:
        print("yes")
    else:
        print("no")

def solve():
    """
    Solves a single test case for the Chef and Transceivers problem.
    """
    try:
        R, chef, head_server, sous_chef = read_test_case_data()
    except (ValueError, IndexError):
        # Handle potential malformed input for a test case
        return

    R_sq = R * R
    direct_links = count_direct_links(R_sq, chef, head_server, sous_chef)
    is_connected = is_network_connected(direct_links)
    print_result(is_connected)

def read_num_test_cases():
    """Read the number of test cases."""
    return read_int()

def main():
    """
    Main function to handle the number of test cases.
    """
    try:
        num_test_cases = read_num_test_cases()
        for _ in range(num_test_cases):
            solve()
    except (ValueError, IndexError):
        # Gracefully handle cases with invalid or missing input for T
        pass

if __name__ == "__main__":
    main()
