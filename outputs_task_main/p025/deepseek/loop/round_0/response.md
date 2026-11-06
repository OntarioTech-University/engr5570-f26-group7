```python
import sys

def read_input():
    """Read and split the rebus input line."""
    return sys.stdin.readline().split()

def parse_input(tokens):
    """Parse tokens into target n, counts, and operator list."""
    n = int(tokens[-1])
    num_plus = 1
    num_minus = 0
    operators = []

    for item in tokens:
        if item == '+':
            num_plus += 1
            operators.append('+')
        elif item == '-':
            num_minus += 1
            operators.append('-')

    return n, num_plus, num_minus, operators

def adjust_values(values, amount, max_increment):
    """Distribute amount across values, increasing each by at most max_increment."""
    remaining = amount
    for i in range(len(values)):
        add_amount = min(remaining, max_increment)
        values[i] += add_amount
        remaining -= add_amount
        if remaining == 0:
            break

def compute_solution(n, num_plus, num_minus):
    """Return positive and negative value lists if feasible, otherwise None."""
    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1

    if not (min_sum <= n <= max_sum):
        return None

    pos_values = [1] * num_plus
    neg_values = [1] * num_minus

    current_sum = num_plus - num_minus
    diff = n - current_sum

    if diff > 0:
        adjust_values(pos_values, diff, n - 1)
    elif diff < 0:
        adjust_values(neg_values, -diff, n - 1)

    return pos_values, neg_values

def format_solution(n, operators, pos_values, neg_values):
    """Format the rebus solution as a single string."""
    result_parts = []
    pos_idx = 0
    neg_idx = 0

    result_parts.append(str(pos_values[pos_idx]))
    pos_idx += 1

    for op in operators:
        result_parts.append(op)
        if op == '+':
            result_parts.append(str(pos_values[pos_idx]))
            pos_idx += 1
        else:
            result_parts.append(str(neg_values[neg_idx]))
            neg_idx += 1

    result_parts.append("=")
    result_parts.append(str(n))

    return " ".join(result_parts)

def print_solution(n, operators, pos_values, neg_values):
    """Print the possible solution."""
    print("Possible")
    print(format_solution(n, operators, pos_values, neg_values))

def solve():
    """Solve the rebus problem from stdin."""
    tokens = read_input()
    n, num_plus, num_minus, operators = parse_input(tokens)

    solution = compute_solution(n, num_plus, num_minus)
    if solution is None:
        print("Impossible")
        return

    pos_values, neg_values = solution
    print_solution(n, operators, pos_values, neg_values)

def main():
    solve()

if __name__ == "__main__":
    main()
```

- Moved the top-level `solve()` call into a `main()` function guarded by `if __name__ == "__main__":`.
- Split input handling into `read_input()` and `parse_input()`.
- Extracted the core feasibility and value construction logic into `compute_solution()`.
- Removed duplicated adjustment loops by adding the shared helper `adjust_values()`.
- Separated output formatting and printing into `format_solution()` and `print_solution()`.
- All data is passed through parameters and return values; no global variables are used.