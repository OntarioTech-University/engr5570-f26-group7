import sys


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


def increase_positive_values(pos_values, diff, n):
    for i in range(len(pos_values)):
        add_amount = min(diff, n - 1)
        pos_values[i] += add_amount
        diff -= add_amount
        if diff == 0:
            break


def increase_negative_values(neg_values, to_decrease, n):
    for i in range(len(neg_values)):
        add_amount = min(to_decrease, n - 1)
        neg_values[i] += add_amount
        to_decrease -= add_amount
        if to_decrease == 0:
            break


def construct_values(num_plus, num_minus, n):
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus
    current_sum = num_plus - num_minus
    diff = n - current_sum
    if diff > 0:
        increase_positive_values(pos_values, diff, n)
    elif diff < 0:
        increase_negative_values(neg_values, -diff, n)
    return pos_values, neg_values


def format_result(operators, pos_values, neg_values, n):
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


def print_status(status):
    print(status)


def print_solution(result):
    print(result)


def solve():
    """Solves the rebus problem by checking feasibility and constructing a solution."""
    line, n = read_input()
    num_plus, num_minus, operators = count_terms(line)
    if not is_feasible(num_plus, num_minus, n):
        print_status("Impossible")
        return
    print_status("Possible")
    pos_values, neg_values = construct_values(num_plus, num_minus, n)
    result = format_result(operators, pos_values, neg_values, n)
    print_solution(result)


solve()
