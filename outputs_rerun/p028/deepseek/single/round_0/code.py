import sys

input = sys.stdin.read

def parse_input(data):
    idx = 0
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1

    if m > 0:
        blocked = set(map(int, data[idx:idx + m]))
        idx += m
    else:
        blocked = set()

    a = list(map(int, data[idx:idx + k]))
    return n, k, blocked, a

def build_blocked_flags(n, blocked):
    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True
    return is_blocked

def find_lamp_position(is_blocked, start_pos, end_pos):
    pos = end_pos
    while pos >= start_pos:
        if not is_blocked[pos]:
            return pos
        pos -= 1
    return -1

def min_lamps_for_power(n, is_blocked, l):
    count = 0
    i = 0
    while i < n:
        start_pos = max(0, i - l + 1)
        end_pos = min(i, n - 1)
        lamp_pos = find_lamp_position(is_blocked, start_pos, end_pos)
        if lamp_pos == -1:
            return -1
        count += 1
        i = lamp_pos + l
    return count

def main():
    data = input().split()
    n, k, blocked, a = parse_input(data)
    is_blocked = build_blocked_flags(n, blocked)

    min_cost = float('inf')
    for l in range(1, k + 1):
        cost_per_lamp = a[l - 1]
        lamp_count = min_lamps_for_power(n, is_blocked, l)
        if lamp_count != -1:
            total_cost = lamp_count * cost_per_lamp
            if total_cost < min_cost:
                min_cost = total_cost

    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)

if __name__ == "__main__":
    main()
