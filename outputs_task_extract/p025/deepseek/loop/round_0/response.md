```python
import sys


def read_tokens():
    return sys.stdin.readline().split()


def parse_target(tokens):
    return int(tokens[-1])


def count_terms(tokens):
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

    return num_plus, num_minus, operators


def is_feasible(n, num_plus, num_minus):
    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1
    return min_sum <= n <= max_sum


def distribute_positive_increase(pos_values, diff, n):
    for i in range(len(pos_values)):
        add_amount = min(diff, n - 1)
        pos_values[i] += add_amount
        diff -= add_amount
        if diff == 0:
            break


def distribute_negative_increase(neg_values, to_decrease, n):
    for i in range(len(neg_values)):
        add_amount = min(to_decrease, n - 1)
        neg_values[i] += add_amount
        to_decrease -= add_amount
        if to_decrease == 0:
            break


def construct_values(n, num_plus, num_minus):
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus

    current_sum = num_plus - num_minus
    diff = n - current_sum

    if diff > 0:
        distribute_positive_increase(pos_values, diff, n)
    elif diff < 0:
        distribute_negative_increase(neg_values, -diff, n)

    return pos_values, neg_values


def format_rebus(n, operators, pos_values, neg_values):
    parts = [str(pos_values[0])]
    pos_idx = 1
    neg_idx = 0

    for op in operators:
        if op == '+':
            parts.extend([op, str(pos_values[pos_idx])])
            pos_idx += 1
        else:
            parts.extend([op, str(neg_values[neg_idx])])
            neg_idx += 1

    parts.extend(["=", str(n)])
    return " ".join(parts)


def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    tokens = read_tokens()
    n = parse_target(tokens)
    num_plus, num_minus, operators = count_terms(tokens)

    if not is_feasible(n, num_plus, num_minus):
        print("Impossible")
        return

    print("Possible")
    pos_values, neg_values = construct_values(n, num_plus, num_minus)
    print(format_rebus(n, operators, pos_values, neg_values))


solve()
```

- Split input reading into `read_tokens` and `parse_target` so each step is isolated and reusable.
- Extracted operator counting into `count_terms`, keeping the original counting logic unchanged.
- Moved feasibility checking into `is_feasible`, making the condition clear and testable.
- Separated value construction into `construct_values` with two small helper functions for distributing increases/decreases.
- Extracted output formatting into `format_rebus`, reducing the size of `solve` and isolating string building.
- Kept `solve` as the only public entry point and preserved the top-level `solve()` call to maintain original import-time behavior.