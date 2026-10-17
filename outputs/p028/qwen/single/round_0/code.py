import sys
input = sys.stdin.read


def _parse_header(data):
    idx = 0

    n = int(data[idx])
    idx += 1

    m = int(data[idx])
    idx += 1

    k = int(data[idx])
    idx += 1

    return n, m, k, idx


def _parse_blocked_positions(data, idx, m):
    if m > 0:
        blocked_list = list(map(int, data[idx:idx + m]))
        idx += m
        return set(blocked_list), idx

    return set(), idx


def _parse_lamp_costs(data, idx, k):
    return list(map(int, data[idx:idx + k]))


def _parse_input(data):
    n, m, k, idx = _parse_header(data)
    blocked, idx = _parse_blocked_positions(data, idx, m)
    lamp_costs = _parse_lamp_costs(data, idx, k)

    return n, k, blocked, lamp_costs


def _build_blocked_mask(n, blocked):
    is_blocked = [False] * n

    for pos in blocked:
        is_blocked[pos] = True

    return is_blocked


def _find_rightmost_unblocked_position(is_blocked, start_pos, end_pos):
    for pos in range(end_pos, start_pos - 1, -1):
        if not is_blocked[pos]:
            return pos

    return -1


def _count_lamps_needed(n, is_blocked, power):
    count = 0
    uncovered = 0

    while uncovered < n:
        start_pos = max(0, uncovered - power + 1)
        end_pos = min(uncovered, n - 1)

        lamp_pos = _find_rightmost_unblocked_position(
            is_blocked,
            start_pos,
            end_pos,
        )

        if lamp_pos == -1:
            return -1

        count += 1
        uncovered = lamp_pos + power

    return count


def _compute_min_cost(n, blocked, lamp_costs, k):
    is_blocked = _build_blocked_mask(n, blocked)
    min_cost = float('inf')

    for power in range(1, k + 1):
        cost_per_lamp = lamp_costs[power - 1]
        lamps_needed = _count_lamps_needed(n, is_blocked, power)

        if lamps_needed != -1:
            total_cost = lamps_needed * cost_per_lamp
            if total_cost < min_cost:
                min_cost = total_cost

    return min_cost


def main():
    data = input().split()

    n, k, blocked, lamp_costs = _parse_input(data)
    min_cost = _compute_min_cost(n, blocked, lamp_costs, k)

    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)


if __name__ == "__main__":
    main()
