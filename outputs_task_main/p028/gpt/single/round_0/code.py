import sys


def read_input():
    data = sys.stdin.read().split()
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
    return n, k, blocked, a


def compute_min_cost(n, k, blocked, a):
    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True

    min_cost = float("inf")

    for l in range(1, k + 1):
        cost_per_lamp = a[l - 1]
        count = 0
        i = 0

        while i < n:
            start_pos = max(0, i - l + 1)
            found = False
            pos = min(i, n - 1)

            while pos >= start_pos:
                if not is_blocked[pos]:
                    count += 1
                    i = pos + l
                    found = True
                    break
                pos -= 1

            if not found:
                count = -1
                break

        if count != -1:
            total_cost = count * cost_per_lamp
            if total_cost < min_cost:
                min_cost = total_cost

    return min_cost


def print_result(min_cost):
    if min_cost == float("inf"):
        print(-1)
    else:
        print(min_cost)


def main():
    n, k, blocked, a = read_input()
    min_cost = compute_min_cost(n, k, blocked, a)
    print_result(min_cost)


if __name__ == "__main__":
    main()
