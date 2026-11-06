import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R


def read_number_of_cases():
    return int(input())


def read_point():
    return tuple(map(int, input().split()))


def read_case_input():
    R = int(input())
    chef = read_point()
    head_server = read_point()
    sous_chef = read_point()
    positions = [chef, head_server, sous_chef]
    return R, positions


def can_communicate_pair(i, j, positions, R):
    if i == j:
        return True
    return can_communicate_directly(positions[i], positions[j], R)


def create_empty_communication_matrix(size):
    return [[False for _ in range(size)] for _ in range(size)]


def fill_communication_matrix(matrix, positions, R):
    for i in range(len(positions)):
        for j in range(len(positions)):
            matrix[i][j] = can_communicate_pair(i, j, positions, R)


def build_communication_matrix(positions, R):
    matrix = create_empty_communication_matrix(len(positions))
    fill_communication_matrix(matrix, positions, R)
    return matrix


def pair_has_direct_or_indirect_link(matrix, i, j, helper):
    if matrix[i][j]:
        return True
    return matrix[i][helper] and matrix[j][helper]


def all_pairs_can_communicate(matrix):
    all_can_communicate = True

    if not pair_has_direct_or_indirect_link(matrix, 0, 1, 2):
        all_can_communicate = False

    if not pair_has_direct_or_indirect_link(matrix, 0, 2, 1):
        all_can_communicate = False

    if not pair_has_direct_or_indirect_link(matrix, 1, 2, 0):
        all_can_communicate = False

    return all_can_communicate


def solve_case():
    R, positions = read_case_input()
    matrix = build_communication_matrix(positions, R)
    all_can_communicate = all_pairs_can_communicate(matrix)
    return "yes" if all_can_communicate else "no"


def print_result(result):
    print(result)


def process_cases(case_count):
    for _ in range(case_count):
        print_result(solve_case())


def main():
    case_count = read_number_of_cases()
    process_cases(case_count)


main()
