import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R


def _all_can_communicate(can_communicate):
    chef_head = can_communicate[0][1]
    chef_sous = can_communicate[0][2]
    head_sous = can_communicate[1][2]

    return (chef_head and (chef_sous or head_sous)) or (
        chef_sous and head_sous
    )


def solve_case():
    R = int(input())
    chef = tuple(map(int, input().split()))
    head_server = tuple(map(int, input().split()))
    sous_chef = tuple(map(int, input().split()))

    positions = [chef, head_server, sous_chef]

    can_communicate = [[False for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(
                    positions[i], positions[j], R
                )

    return "yes" if _all_can_communicate(can_communicate) else "no"


T = int(input())
for _ in range(T):
    print(solve_case())
