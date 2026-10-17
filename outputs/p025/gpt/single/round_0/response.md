```python
import sys


def _count_terms(line):
    num_plus = 1  # The first '?' is always positive.
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


def _increase_values(values, amount, n):
    for i in range(len(values)):
        add_amount = min(amount, n - 1)
        values[i] += add_amount
        amount -= add_amount
        if amount == 0:
            break


def _format_result(pos_values, neg_values, operators, n):
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
        else:  # op == '-'
            result_parts.append(str(neg_values[neg_idx]))
            neg_idx += 1

    result_parts.append("=")
    result_parts.append(str(n))
    return " ".join(result_parts)


def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    line = sys.stdin.readline().split()
    n = int(line[-1])

    num_plus, num_minus, operators = _count_terms(line)

    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1

    if not (min_sum <= n <= max_sum):
        print("Impossible")
        return

    print("Possible")

    pos_values = [1] * num_plus
    neg_values = [1] * num_minus

    current_sum = num_plus - num_minus
    diff = n - current_sum

    if diff > 0:
        _increase_values(pos_values, diff, n)
    elif diff < 0:
        _increase_values(neg_values, -diff, n)

    print(_format_result(pos_values, neg_values, operators, n))


solve()
```

- Extracted term counting and output formatting into named helpers so `solve()` reads as the main sequence of steps.
- Combined the duplicated value-adjustment loops into one helper, retaining the same positive and negative branches.