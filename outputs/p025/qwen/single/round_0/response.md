```python
import sys


def _count_terms(line):
    """Count positive/negative terms and record operator order."""
    num_plus = 1  # The first '?' is always positive
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


def _is_feasible(num_plus, num_minus, n):
    """Return True if the target can be reached with values in [1, n]."""
    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1
    return min_sum <= n <= max_sum


def _add_difference(values, remaining, n):
    """Increase values until the remaining difference is zero."""
    for i in range(len(values)):
        add_amount = min(remaining, n - 1)
        values[i] += add_amount
        remaining -= add_amount
        if remaining == 0:
            break


def _build_values(num_plus, num_minus, n):
    """Construct concrete positive and negative term values."""
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus

    current_sum = num_plus - num_minus
    diff = n - current_sum

    if diff > 0:
        _add_difference(pos_values, diff, n)
    elif diff < 0:
        _add_difference(neg_values, -diff, n)

    return pos_values, neg_values


def _format_solution(pos_values, neg_values, operators, n):
    """Build the printable rebus string from the chosen values."""
    result_parts = [str(pos_values[0])]
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

    result_parts.append("=")
    result_parts.append(str(n))
    return " ".join(result_parts)


def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    line = sys.stdin.readline().split()

    # The target number 'n' is the last element
    n = int(line[-1])

    num_plus, num_minus, operators = _count_terms(line)

    if not _is_feasible(num_plus, num_minus, n):
        print("Impossible")
        return

    print("Possible")
    pos_values, neg_values = _build_values(num_plus, num_minus, n)
    print(_format_solution(pos_values, neg_values, operators, n))


solve()
```

- Extracted term counting into `_count_terms` to separate input classification from the main control flow.
- Extracted feasibility checking into `_is_feasible` to make the range condition easier to read and keep `solve` focused on orchestration.
- Extracted value adjustment into `_add_difference` and `_build_values` to reduce duplicated loop logic and clarify construction steps.
- Extracted output assembly into `_format_solution` to separate formatting from algorithm logic.
- Preserved the public `solve` signature, the unconditional `solve()` call, all arithmetic, printing order, and return behavior.