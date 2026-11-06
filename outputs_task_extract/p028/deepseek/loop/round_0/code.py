import sys
input = sys.stdin.read

def read_input():
    return input().split()

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
    return n, m, k, blocked, a

def build_blocked_flags(n, blocked):
    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True
    return is_blocked

def find_lamp_position(l, i, n, is_blocked):
    start_pos = max(0, i - l + 1)
    pos = min(i, n - 1)
    while pos >= start_pos:
        if not is_blocked[pos]:
            return pos
        pos -= 1
    return -1

def count_lamps_for_power(l, n, is_blocked):
    count = 0
    i = 0
    while i < n:
        pos = find_lamp_position(l, i, n, is_blocked)
        if pos == -1:
            return -1
        count += 1
        i = pos + l
    return count

def compute_min_cost(n, k, a, is_blocked):
    min_cost = float('inf')
    for l in range(1, k + 1):
        count = count_lamps_for_power(l, n, is_blocked)
        if count != -1:
            total_cost = count * a[l - 1]
            if total_cost < min_cost:
                min_cost = total_cost
    return min_cost

def print_result(min_cost):
    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)

def main():
    data = read_input()
    n, m, k, blocked, a = parse_input(data)
    is_blocked = build_blocked_flags(n, blocked)
    min_cost = compute_min_cost(n, k, a, is_blocked)
    print_result(min_cost)

if __name__ == "__main__":
    main()
