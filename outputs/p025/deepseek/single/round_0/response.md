Here's the refactored code:

```python
import sys


def parse_input(line):
    """Parse the input line and return the target number and operators."""
    tokens = line.split()
    n = int(tokens[-1])
    operators = [token for token in tokens if token in ('+', '-')]
    return n, operators


def count_terms(operators):
    """Count positive and negative terms based on operators."""
    num_plus = 1  # The first '?' is always positive
    num_minus = 0
    for op in operators:
        if op == '+':
            num_plus += 1
        else:
            num_minus += 1
    return num_plus, num_minus


def is_feasible(n, num_plus, num_minus):
    """Check if the target sum is achievable."""
    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1
    return min_sum <= n <= max_sum


def distribute_values(num_terms, diff, max_value):
    """Distribute a difference across terms, starting from 1."""
    values = [1] * num_terms
    remaining = abs(diff)
    for i in range(num_terms):
        add_amount = min(remaining, max_value - 1)
        values[i] += add_amount
        remaining -= add_amount
        if remaining == 0:
            break
    return values


def construct_values(n, num_plus, num_minus):
    """Construct the values for positive and negative terms."""
    current_sum = num_plus - num_minus
    diff = n - current_sum
    
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus
    
    if diff > 0:
        pos_values = distribute_values(num_plus, diff, n)
    elif diff < 0:
        neg_values = distribute_values(num_minus, diff, n)
    
    return pos_values, neg_values


def format_rebus(pos_values, neg_values, operators, n):
    """Format the solution as a string."""
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
    
    result_parts.extend(["=", str(n)])
    return " ".join(result_parts)


def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    line = sys.stdin.readline()
    n, operators = parse_input(line)
    num_plus, num_minus = count_terms(operators)
    
    if not is_feasible(n, num_plus, num_minus):
        print("Impossible")
        return
    
    print("Possible")
    pos_values, neg_values = construct_values(n, num_plus, num_minus)
    print(format_rebus(pos_values, neg_values, operators, n))


solve()
```

**Changes made:**

- **Extracted `parse_input` function**: Separates input parsing logic from the main flow, making it clearer what data is being extracted.
- **Extracted `count_terms` function**: Isolates the counting of positive/negative terms, removing the need to track operators separately during counting.
- **Extracted `is_feasible` function**: Encapsulates the feasibility check logic, making the main function more readable.
- **Extracted `distribute_values` function**: Consolidates the duplicated logic for distributing values across terms (previously repeated for positive and negative cases).
- **Extracted `construct_values` function**: Groups the value construction logic together, separating it from the formatting concern.
- **Extracted `format_rebus` function**: Isolates the output formatting logic, making the main function focus on orchestration.
- **Simplified operator counting**: Removed the redundant `operators.append()` calls in the counting loop by using a list comprehension in `parse_input`.
- **Reduced nesting**: The main `solve` function now has a linear flow with clear steps, each delegated to a well-named function.