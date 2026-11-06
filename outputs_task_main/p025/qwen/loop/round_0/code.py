import sys


def _read_input():
    line = sys.stdin.readline().split()
    n = int(line[-1])
    return line, n


def _parse_terms(line):
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


def _is_feasible(num_plus, num_minus, n):
    min_sum = num_plus * 1 - num_minus * n
    max_sum = num_plus * n - num_minus * 1
    return min_sum <= n <= max_sum


def _increase_values(values, amount, max_add):
    for i in range(len(values)):
        add_amount = min(amount, max_add)
        values[i] += add_amount
        amount -= add_amount
        if amount == 0:
            break
    return values


def _build_values(num_plus, num_minus, n):
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus

    current_sum = num_plus - num_minus
    diff = n - current_sum

    if diff > 0:
        pos_values = _increase_values(pos_values, diff, n - 1)
    elif diff < 0:
        neg_values = _increase_values(neg_values, -diff, n - 1)

    return pos_values, neg_values


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
        else:  # op == '-'
            result_parts.append(str(neg_values[neg_idx]))
            neg_idx += 1

    result_parts.append("=")
    result_parts.append(str(n))
    return " ".join(result_parts)


def _construct_solution_line(num_plus, num_minus, operators, n):
    pos_values, neg_values = _build_values(num_plus, num_minus, n)
    return _format_solution(operators, pos_values, neg_values, n)


def _print_impossible():
    print("Impossible")


def _print_possible_header():
    print("Possible")


def _print_solution_line(solution_line):
    print(solution_line)


def main():
    line, n = _read_input()
    num_plus, num_minus, operators = _parse_terms(line)

    if not _is_feasible(num_plus, num_minus, n):
        _print_impossible()
        return

    _print_possible_header()
    solution_line = _construct_solution_line(num_plus, num_minus, operators, n)
    _print_solution_line(solution_line)


def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    main()


if __name__ == "__main__":
    main()
