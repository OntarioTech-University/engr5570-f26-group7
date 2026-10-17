import sys

input = sys.stdin.read


def parse_input(data):
    """Parse the input data and return n, m, k, blocked set, and lamp costs."""
    idx = 0

    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1

    blocked = set()
    if m > 0:
        blocked_list = list(map(int, data[idx:idx + m]))
        idx += m
        blocked = set(blocked_list)

    a = list(map(int, data[idx:idx + k]))

    return n, blocked, a


def build_blocked_array(n, blocked):
    """Create a boolean array indicating blocked positions."""
    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True
    return is_blocked


def find_lamp_position(is_blocked, start_pos, end_pos):
    """Find the last valid lamp position in the given range, or None if none exists."""
    for pos in range(end_pos, start_pos - 1, -1):
        if not is_blocked[pos]:
            return pos
    return None


def count_lamps_for_power(is_blocked, n, power):
    """Count the minimum number of lamps of given power needed to cover all positions."""
    count = 0
    i = 0
    while i < n:
        start_pos = max(0, i - power + 1)
        end_pos = min(i, n - 1)
        lamp_pos = find_lamp_position(is_blocked, start_pos, end_pos)

        if lamp_pos is None:
            return -1

        count += 1
        i = lamp_pos + power

    return count


def main():
    data = input().split()
    n, blocked, lamp_costs = parse_input(data)
    is_blocked = build_blocked_array(n, blocked)

    min_cost = float('inf')

    for power in range(1, len(lamp_costs) + 1):
        lamp_count = count_lamps_for_power(is_blocked, n, power)
        if lamp_count != -1:
            total_cost = lamp_count * lamp_costs[power - 1]
            min_cost = min(min_cost, total_cost)

    print(-1 if min_cost == float('inf') else min_cost)


if __name__ == "__main__":
    main()
