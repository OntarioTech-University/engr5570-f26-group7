```python
def parse_int_list(data, idx, count):
    return list(map(int, data[idx:idx + count])), idx + count


def read_input():
    import sys
    data = sys.stdin.read().split()
    idx = 0

    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1

    if m > 0:
        blocked_values, idx = parse_int_list(data, idx, m)
        blocked = set(blocked_values)
    else:
        blocked = set()

    a, _ = parse_int_list(data, idx, k)
    return n, m, k, blocked, a


def compute_min_cost(n, m, k, blocked, a):
    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True

    min_cost = float('inf')

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

    return -1 if min_cost == float('inf') else min_cost


def print_result(result):
    print(result)


def main():
    n, m, k, blocked, a = read_input()
    result = compute_min_cost(n, m, k, blocked, a)
    print_result(result)


if __name__ == "__main__":
    main()
```

- **Moved all logic out of top level** — only function definitions and the `if __name__ == "__main__"` guard remain at module level.
- **Eliminated global variables** — `sys.stdin.read` is now imported and used inside `read_input`, and all data is passed via parameters and return values.
- **Separated input, computation, and output** into `read_input`, `compute_min_cost`, and `print_result`.
- **Extracted duplicated parsing** into `parse_int_list`, which is used for both blocked positions and lamp costs.
- **Preserved runtime behavior** — parsing, error conditions, loop logic, and output formatting remain identical to the original.