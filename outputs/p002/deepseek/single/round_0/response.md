Here's the refactored version of the code:

```python
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
```

**Changes made:**

- **Extracted input reading** into `read_input()` function to separate I/O concerns from logic
- **Created `is_valid_number()`** helper to make the range validation more readable and reusable
- **Created `are_all_distinct()`** helper to clarify the distinctness check intent
- **Created `satisfies_constraints()`** to encapsulate the remaining constraint verification
- **Created `find_solution()`** to isolate the core algorithm, replacing the `found` flag and `result` variable with a cleaner return-based approach
- **Created `print_solution()`** to separate output formatting from the solution logic
- **Added `main()` function** with proper entry point guard for better structure
- **Replaced nested conditionals** with early `continue` statements to reduce indentation depth and improve readability
- **Used list comprehension** with `all()` for cleaner validation of multiple values