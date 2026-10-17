import sys

input = sys.stdin.read


def _count_lamps(n, power, is_blocked):
    count = 0
    i = 0

    while i < n:
        start_pos = max(0, i - power + 1)
        pos = min(i, n - 1)

        while pos >= start_pos and is_blocked[pos]:
            pos -= 1

        if pos < start_pos:
            return -1

        count += 1
        i = pos + power

    return count


def main():
    data = input().split()
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
    else:
        blocked_list = []

    a = list(map(int, data[idx:idx + k]))

    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True

    min_cost = float('inf')

    for l in range(1, k + 1):
        count = _count_lamps(n, l, is_blocked)
        if count != -1:
            total_cost = count * a[l - 1]
            if total_cost < min_cost:
                min_cost = total_cost

    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)


if __name__ == "__main__":
    main()
