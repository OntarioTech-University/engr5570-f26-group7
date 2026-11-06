```python
import sys


def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    tokens, n = read_input()
    num_plus, num_minus, operators = count_terms(tokens)

    if not is_feasible(num_plus, num_minus, n):
        print_impossible()
        return

    print_possible()
    pos_values, neg_values = construct_values(num_plus, num_minus, n)
    solution = format_solution(operators, pos_values, neg_values, n)
    print_solution(solution)


def read_input():
    line = sys.stdin.readline().split()
    n = int(line[-1])
    return line, n


def count_terms(line):
    num_plus = 1
    num_minus = 0
    operators = []

    for item in line:
        if item == '+':
            num_plus += 1
            operators.append('+')
        elif item == '-':
            num_minus += 1
            operators.append('-')

    return num_plus, num_minus, operators


def is_feasible(num_plus, num_minus, n):
    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1
    return min_sum <= n <= max_sum


def construct_values(num_plus, num_minus, n):
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus
    diff = n - (num_plus - num_minus)

    if diff > 0:
        _add_amount_to_values(pos_values, diff, n)
    elif diff < 0:
        _add_amount_to_values(neg_values, -diff, n)

    return pos_values, neg_values


def _add_amount_to_values(values, amount, n):
    for i in range(len(values)):
        add_amount = min(amount, n - 1)
        values[i] += add_amount
        amount -= add_amount
        if amount == 0:
            break


def format_solution(operators, pos_values, neg_values, n):
    result_parts = [str(pos_values[0])]
    _append_operator_operands(result_parts, operators, pos_values, neg_values)
    result_parts.append("=")
    result_parts.append(str(n))
    return " ".join(result_parts)


def _append_operator_operands(result_parts, operators, pos_values, neg_values):
    pos_idx = 1
    neg_idx = 0

    for op in operators:
        result_parts.append(op)
        if op == '+':
            result_parts.append(str(pos_values[pos_idx]))
            pos_idx += 1
        else:
            result_parts.append(str(neg_values[neg_idx]))
            neg_idx += 1


def print_impossible():
    print("Impossible")


def print_possible():
    print("Possible")


def print_solution(solution):
    print(solution)


solve()
```

- Extracted input parsing into `read_input()` so stdin access and target conversion are isolated from the main algorithm.
- Moved operator/term counting into `count_terms()` to give that computation a single, clearly named responsibility.
- Extracted the feasibility calculation into `is_feasible()` so the condition check is separate from control flow.
- Split solution construction into `construct_values()` and `_add_amount_to_values()` to keep value assignment logic small and reusable.
- Extracted output formatting into `format_solution()` and `_append_operator_operands()` so string building is separate from printing.
- Moved all printing into dedicated functions: `print_impossible()`, `print_possible()`, and `print_solution()`.
- Kept `solve()` as the public orchestrator and retained the unconditional top-level `solve()` call to preserve the original runtime behavior.