```python
import sys

class FenwickTree:
    """
    A class for a Fenwick Tree (Binary Indexed Tree).
    It supports point updates and prefix sum queries in O(log n) time.
    The tree is 1-indexed internally.
    """
    def __init__(self, size):
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index, delta):
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def query(self, index):
        if index <= 0:
            return 0
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & -index
        return s


def read_parameters():
    try:
        n, k, a, b, q = map(int, sys.stdin.readline().strip().split())
        return n, k, a, b, q
    except (IOError, ValueError):
        return None


def read_query_parts():
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def apply_order_update(orders, day, amount, capacity_a, capacity_b):
    old_filled_b = min(orders[day], capacity_b)
    old_filled_a = min(orders[day], capacity_a)

    orders[day] += amount

    new_filled_b = min(orders[day], capacity_b)
    new_filled_a = min(orders[day], capacity_a)

    return new_filled_b - old_filled_b, new_filled_a - old_filled_a


def update_filled_capacities(bit_b, bit_a, day, delta_b, delta_a):
    if delta_b != 0:
        bit_b.update(day, delta_b)
    if delta_a != 0:
        bit_a.update(day, delta_a)


def handle_update_query(query_parts, orders, bit_b, bit_a, capacity_a, capacity_b):
    day = int(query_parts[1])
    amount = int(query_parts[2])

    delta_b, delta_a = apply_order_update(orders, day, amount, capacity_a, capacity_b)
    update_filled_capacities(bit_b, bit_a, day, delta_b, delta_a)


def handle_sum_query(query_parts, bit_b, bit_a, n, k):
    p = int(query_parts[1])

    sum_b = bit_b.query(p - 1)
    sum_a = bit_a.query(n) - bit_a.query(p + k - 1)

    return sum_b + sum_a


def write_result(total_filled):
    sys.stdout.write(str(total_filled) + '\n')


def process_next_query(orders, bit_b, bit_a, n, k, capacity_a, capacity_b):
    query_parts = read_query_parts()
    if query_parts is None:
        return

    query_type = int(query_parts[0])

    if query_type == 1:
        handle_update_query(query_parts, orders, bit_b, bit_a, capacity_a, capacity_b)
    elif query_type == 2:
        total_filled = handle_sum_query(query_parts, bit_b, bit_a, n, k)
        write_result(total_filled)


def solve():
    params = read_parameters()
    if params is None:
        return

    n, k, a, b, q = params

    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)

    for _ in range(q):
        process_next_query(orders, bit_b, bit_a, n, k, a, b)


if __name__ == "__main__":
    solve()
```

- Extracted problem parameter reading into `read_parameters` while preserving the original exception handling.
- Extracted query line reading and blank-line handling into `read_query_parts`.
- Split order update logic into `apply_order_update` and Fenwick-tree writes into `update_filled_capacities`.
- Extracted type-1 query handling into `handle_update_query`.
- Extracted type-2 query computation into `handle_sum_query`.
- Extracted output writing into `write_result`.
- Added `process_next_query` for per-query dispatch, keeping `solve` small and high-level.
- Left the public `FenwickTree` class and `solve` signature unchanged.