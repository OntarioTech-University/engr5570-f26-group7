```python
import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R


def read_positions():
    chef = tuple(map(int, input().split()))
    head_server = tuple(map(int, input().split()))
    sous_chef = tuple(map(int, input().split()))
    return [chef, head_server, sous_chef]


def build_communication_matrix(positions, R):
    can_communicate = [[False for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(positions[i], positions[j], R)
    return can_communicate


def can_communicate_via_intermediary(matrix, a, b, intermediary):
    return matrix[a][intermediary] and matrix[b][intermediary]


def all_can_communicate(matrix):
    if not matrix[0][1]:
        if not can_communicate_via_intermediary(matrix, 0, 1, 2):
            return False

    if not matrix[0][2]:
        if not can_communicate_via_intermediary(matrix, 0, 2, 1):
            return False

    if not matrix[1][2]:
        if not can_communicate_via_intermediary(matrix, 1, 2, 0):
            return False

    return True


def solve_case():
    R = int(input())
    positions = read_positions()
    matrix = build_communication_matrix(positions, R)
    return "yes" if all_can_communicate(matrix) else "no"


def read_test_case_count():
    return int(input())


def run_all_cases():
    T = read_test_case_count()
    for _ in range(T):
        print(solve_case())


if __name__ == "__main__":
    run_all_cases()
```