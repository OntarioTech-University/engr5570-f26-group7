import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R

def read_positions():
    R = int(input())
    chef = tuple(map(int, input().split()))
    head_server = tuple(map(int, input().split()))
    sous_chef = tuple(map(int, input().split()))
    return R, [chef, head_server, sous_chef]

def build_communication_matrix(positions, R):
    can_communicate = [[False for _ in range(3)] for _ in range(3)]
    
    for i in range(3):
        for j in range(3):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(positions[i], positions[j], R)
    
    return can_communicate

def can_communicate_indirectly(matrix, node1, node2, intermediate):
    return matrix[node1][intermediate] and matrix[node2][intermediate]

def all_nodes_connected(matrix):
    # Check each pair can communicate directly or through the third node
    pairs_to_check = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]
    
    for node1, node2, intermediate in pairs_to_check:
        if not matrix[node1][node2]:
            if not can_communicate_indirectly(matrix, node1, node2, intermediate):
                return False
    
    return True

def solve_case():
    R, positions = read_positions()
    communication_matrix = build_communication_matrix(positions, R)
    return "yes" if all_nodes_connected(communication_matrix) else "no"

T = int(input())
for _ in range(T):
    print(solve_case())
