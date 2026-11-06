import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R

def _read_case():
    R = int(input())
    chef = tuple(map(int, input().split()))
    head_server = tuple(map(int, input().split()))
    sous_chef = tuple(map(int, input().split()))
    return R, [chef, head_server, sous_chef]

def _can_all_communicate(positions, R):
    n = len(positions)
    can_communicate = [[False] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(positions[i], positions[j], R)

    all_can_communicate = True
    pairs = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]

    for a, b, c in pairs:
        if not can_communicate[a][b]:
            if not (can_communicate[a][c] and can_communicate[b][c]):
                all_can_communicate = False

    return all_can_communicate

def solve_case():
    R, positions = _read_case()
    return "yes" if _can_all_communicate(positions, R) else "no"

def _print_result(result):
    print(result)

def main():
    T = int(input())
    for _ in range(T):
        _print_result(solve_case())

if __name__ == "__main__":
    main()
