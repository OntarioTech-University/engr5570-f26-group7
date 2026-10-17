def read_input():
    """Read and parse the input constraints."""
    r1, r2 = map(int, input().split())
    c1, c2 = map(int, input().split())
    d1, d2 = map(int, input().split())
    return r1, r2, c1, c2, d1, d2

def is_valid_number(value):
    """Check if a number is within the valid range [1, 9]."""
    return 1 <= value <= 9

def are_all_distinct(numbers):
    """Check if all numbers in the list are distinct."""
    return len(set(numbers)) == len(numbers)

def satisfies_constraints(a, b, c, d, r2, c2, d2):
    """Check if the numbers satisfy all remaining constraints."""
    return c + d == r2 and b + d == c2 and b + c == d2

def find_solution(r1, r2, c1, c2, d1, d2):
    """Find a valid solution for the magic square."""
    for a in range(1, 10):
        b = r1 - a
        c = c1 - a
        d = d1 - a
        
        if not all(is_valid_number(x) for x in [b, c, d]):
            continue
            
        if not are_all_distinct([a, b, c, d]):
            continue
            
        if satisfies_constraints(a, b, c, d, r2, c2, d2):
            return [[a, b], [c, d]]
    
    return None

def print_solution(solution):
    """Print the solution or -1 if no solution exists."""
    if solution:
        print(solution[0][0], solution[0][1])
        print(solution[1][0], solution[1][1])
    else:
        print(-1)

def main():
    r1, r2, c1, c2, d1, d2 = read_input()
    solution = find_solution(r1, r2, c1, c2, d1, d2)
    print_solution(solution)

if __name__ == "__main__":
    main()
