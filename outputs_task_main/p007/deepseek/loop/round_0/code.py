import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R

def read_input():
    T = int(input())
    test_cases = []
    for _ in range(T):
        R = int(input())
        chef = tuple(map(int, input().split()))
        head_server = tuple(map(int, input().split()))
        sous_chef = tuple(map(int, input().split()))
        test_cases.append((R, chef, head_server, sous_chef))
    return test_cases

def build_communication_matrix(positions, R):
    can_communicate = [[False for _ in range(3)] for _ in range(3)]
    
    for i in range(3):
        for j in range(3):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(positions[i], positions[j], R)
    
    return can_communicate

def check_all_can_communicate(can_communicate):
    all_can_communicate = True
    
    # Check Chef <-> Head Server
    if not can_communicate[0][1]:
        # Need to go through Sous Chef
        if not (can_communicate[0][2] and can_communicate[1][2]):
            all_can_communicate = False
    
    # Check Chef <-> Sous Chef  
    if not can_communicate[0][2]:
        # Need to go through Head Server
        if not (can_communicate[0][1] and can_communicate[1][2]):
            all_can_communicate = False
    
    # Check Head Server <-> Sous Chef
    if not can_communicate[1][2]:
        # Need to go through Chef
        if not (can_communicate[0][1] and can_communicate[0][2]):
            all_can_communicate = False
    
    return all_can_communicate

def solve_case(R, chef, head_server, sous_chef):
    positions = [chef, head_server, sous_chef]
    can_communicate = build_communication_matrix(positions, R)
    all_can_communicate = check_all_can_communicate(can_communicate)
    return "yes" if all_can_communicate else "no"

def process_test_cases(test_cases):
    results = []
    for R, chef, head_server, sous_chef in test_cases:
        results.append(solve_case(R, chef, head_server, sous_chef))
    return results

def print_results(results):
    for result in results:
        print(result)

def main():
    test_cases = read_input()
    results = process_test_cases(test_cases)
    print_results(results)

if __name__ == "__main__":
    main()
