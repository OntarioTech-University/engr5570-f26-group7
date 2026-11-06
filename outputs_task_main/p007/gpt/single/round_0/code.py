import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R


def read_case():
    R = int(input())
    chef = tuple(map(int, input().split()))
    head_server = tuple(map(int, input().split()))
    sous_chef = tuple(map(int, input().split()))
    return R, [chef, head_server, sous_chef]


def _pair_can_communicate(direct, via_first, via_second):
    if not direct:
        if not (via_first and via_second):
            return False
    return True


def compute_case(R, positions):
    can_communicate = [[False for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(
                    positions[i], positions[j], R
                )

    all_can_communicate = True

    if not _pair_can_communicate(
        can_communicate[0][1], can_communicate[0][2], can_communicate[1][2]
    ):
        all_can_communicate = False

    if not _pair_can_communicate(
        can_communicate[0][2], can_communicate[0][1], can_communicate[1][2]
    ):
        all_can_communicate = False

    if not _pair_can_communicate(
        can_communicate[1][2], can_communicate[0][1], can_communicate[0][2]
    ):
        all_can_communicate = False

    return "yes" if all_can_communicate else "no"


def solve_case():
    R, positions = read_case()
    return compute_case(R, positions)


def print_result(result):
    print(result)


def main():
    T = int(input())
    for _ in range(T):
        print_result(solve_case())


if __name__ == "__main__":
    main()
