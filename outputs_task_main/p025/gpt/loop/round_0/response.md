```python
import sys


def read_input():
    return sys.stdin.readline().split()


def _increase_values(values, amount, n):
    for i in range(len(values)):
        add_amount = min(amount, n - 1)
        values[i] += add_amount
        amount -= add_amount
        if amount == 0:
            break


def _format_solution(operators, pos_values, neg_values, n):
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


def compute_solution(line):
    n = int(line[-1])

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

    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1

    if not (min_sum <= n <= max_sum):
        return "Impossible", None

    pos_values = [1] * num_plus
    neg_values = [1] * num_minus

    current_sum = num_plus - num_minus
    diff = n - current_sum

    if diff > 0:
        _increase_values(pos_values, diff, n)
    elif diff < 0:
        _increase_values(neg_values, -diff, n)

    return "Possible", _format_solution(operators, pos_values, neg_values, n)


def print_output(status, solution):
    print(status)
    if solution is not None:
        print(solution)


def solve():
    """Solve the rebus problem by checking feasibility and constructing a solution."""
    line = read_input()
    status, solution = compute_solution(line)
    print_output(status, solution)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and output printing while keeping `solve()` unchanged.
- Moved the duplicated value-increase loops into one helper.
- Replaced the top-level `solve()` call with a guarded `main()` call.