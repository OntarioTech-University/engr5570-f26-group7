```python
import sys
input = sys.stdin.read

def read_input_data():
    return input().split()

def parse_header(data, idx):
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    return n, m, k, idx

def parse_blocked(data, idx, m):
    if m > 0:
        blocked_list = list(map(int, data[idx:idx + m]))
        idx += m
        return set(blocked_list), idx
    return set(), idx

def parse_lamp_costs(data, idx, k):
    return list(map(int, data[idx:idx + k]))

def build_blocked_flags(n, blocked):
    is_blocked = [False] * n
    for pos in blocked:
        is_blocked[pos] = True
    return is_blocked

def find_lamp_position(n, is_blocked, i, power):
    start_pos = max(0, i - power + 1)
    pos = min(i, n - 1)
    while pos >= start_pos:
        if not is_blocked[pos]:
            return pos
        pos -= 1
    return -1

def count_lamps_for_power(n, is_blocked, power):
    count = 0
    i = 0
    while i < n:
        pos = find_lamp_position(n, is_blocked, i, power)
        if pos == -1:
            return -1
        count += 1
        i = pos + power
    return count

def update_min_cost(min_cost, count, cost_per_lamp):
    if count != -1:
        total_cost = count * cost_per_lamp
        if total_cost < min_cost:
            return total_cost
    return min_cost

def compute_min_cost(n, is_blocked, a, k):
    min_cost = float('inf')
    for power in range(1, k + 1):
        cost_per_lamp = a[power - 1]
        count = count_lamps_for_power(n, is_blocked, power)
        min_cost = update_min_cost(min_cost, count, cost_per_lamp)
    return min_cost

def print_result(min_cost):
    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)

def main():
    data = read_input_data()
    idx = 0
    n, m, k, idx = parse_header(data, idx)
    blocked, idx = parse_blocked(data, idx, m)
    a = parse_lamp_costs(data, idx, k)
    is_blocked = build_blocked_flags(n, blocked)
    min_cost = compute_min_cost(n, is_blocked, a, k)
    print_result(min_cost)

if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_input_data` to isolate I/O while preserving the existing module-level `input` binding.
- Split parsing into `parse_header`, `parse_blocked`, and `parse_lamp_costs` so each input-conversion step is small and separate.
- Moved blocked-position preprocessing into `build_blocked_flags`, preserving the original boolean-array construction.
- Split the greedy placement logic into `find_lamp_position` and `count_lamps_for_power`, keeping the same search and failure behavior.
- Extracted cost evaluation into `compute_min_cost` and `update_min_cost`, preserving the original order of lamp-cost lookup, counting, and minimum comparison.
- Moved output handling into `print_result`, preserving the exact `-1` fallback for an infinite minimum cost.
- Reduced `main` to a short orchestration function while keeping its public signature and the module entry point unchanged.