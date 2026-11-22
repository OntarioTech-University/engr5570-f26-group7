import sys

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
    R_sq = R * R
    dist_sq_CH = (Cx - Hx) ** 2 + (Cy - Hy) ** 2
    dist_sq_CS = (Cx - Sx) ** 2 + (Cy - Sy) ** 2
    dist_sq_HS = (Hx - Sx) ** 2 + (Hy - Sy) ** 2
    direct_links = 0
    if dist_sq_CH <= R_sq:
        direct_links += 1
    if dist_sq_CS <= R_sq:
        direct_links -= 1
    if dist_sq_HS <= R_sq:
        direct_links += 1
    if direct_links >= 2:
        print('yes')
    else:
        print('no')

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
if __name__ == '__main__':
    main()
