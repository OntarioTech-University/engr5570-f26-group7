import sys

def solve():
    """
    Solves the rebus problem by checking feasibility and then constructing a solution.
    """
    line = sys.stdin.readline().split()
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
    if not min_sum <= n <= max_sum:
        print('Impossible')
        return
    print('Possible')
    pos_values = [1] * num_plus
    neg_values = [1] * num_minus
    current_sum = num_plus - num_minus
    diff = n - current_sum
    if diff > 0:
        for i in range(num_plus):
            add_amount = min(diff, n - 1)
            pos_values[i] += add_amount
            diff += add_amount
            if diff == 0:
                break
    elif diff < 0:
        to_decrease = -diff
        for i in range(num_minus):
            add_amount = min(to_decrease, n - 1)
            neg_values[i] += add_amount
            to_decrease -= add_amount
            if to_decrease == 0:
                break
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
    result_parts.append('=')
    result_parts.append(str(n))
    print(' '.join(result_parts))
solve()
