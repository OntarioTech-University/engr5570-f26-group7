```python
import sys

class FenwickTree:
    """
    A class for a Fenwick Tree (Binary Indexed Tree).
    It supports point updates and prefix sum queries in O(log n) time.
    The tree is 1-indexed internally.
    """
    def __init__(self, size):
        """
        Initializes a Fenwick Tree of a given size.
        The internal array has size+1 to accommodate 1-based indexing.
        """
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index, delta):
        """
        Adds a delta to the value at a given index.
        This operation takes O(log n) time.
        """
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def query(self, index):
        """
        Queries the cumulative sum of values from index 1 to the given index.
        This operation takes O(log n) time.
        """
        if index <= 0:
            return 0
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & -index
        return s


def _read_initial_values():
    return map(int, sys.stdin.readline().strip().split())


def _create_orders(n):
    return [0] * (n + 1)


def _create_fenwick_trees(n):
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)
    return bit_b, bit_a


def _read_query_line():
    return sys.stdin.readline().strip()


def _parse_query_line(line):
    return line.split()


def _parse_query_type(query):
    return int(query[0])


def _parse_update_query(query):
    return int(query[1]), int(query[2])


def _filled_for_day(orders, day, limit):
    return min(orders[day], limit)


def _add_orders_for_day(orders, day, value):
    orders[day] += value


def _apply_delta(bit, index, delta):
    if delta != 0:
        bit.update(index, delta)


def _handle_update_query(query, orders, bit_b, bit_a, a, b):
    d, val = _parse_update_query(query)
    old_filled_b = _filled_for_day(orders, d, b)
    old_filled_a = _filled_for_day(orders, d, a)
    _add_orders_for_day(orders, d, val)
    new_filled_b = _filled_for_day(orders, d, b)
    new_filled_a = _filled_for_day(orders, d, a)
    delta_b = new_filled_b - old_filled_b
    _apply_delta(bit_b, d, delta_b)
    delta_a = new_filled_a - old_filled_a
    _apply_delta(bit_a, d, delta_a)


def _parse_question_query(query):
    return int(query[1])


def _query_before_maintenance(bit_b, p):
    return bit_b.query(p - 1)


def _query_after_maintenance(bit_a, n, p, k):
    return bit_a.query(n) - bit_a.query(p + k - 1)


def _write_answer(total_filled):
    sys.stdout.write(str(total_filled) + '\n')


def _handle_question_query(query, bit_b, bit_a, n, k):
    p = _parse_question_query(query)
    sum_b = _query_before_maintenance(bit_b, p)
    sum_a = _query_after_maintenance(bit_a, n, p, k)
    total_filled = sum_b + sum_a
    _write_answer(total_filled)


def _dispatch_query(query, orders, bit_b, bit_a, n, k, a, b):
    query_type = _parse_query_type(query)
    if query_type == 1:
        _handle_update_query(query, orders, bit_b, bit_a, a, b)
    elif query_type == 2:
        _handle_question_query(query, bit_b, bit_a, n, k)


def _process_queries(q, orders, bit_b, bit_a, n, k, a, b):
    for _ in range(q):
        line = _read_query_line()
        if not line:
            continue
        query = _parse_query_line(line)
        _dispatch_query(query, orders, bit_b, bit_a, n, k, a, b)


def solve():
    """
    Main function to read input, process queries, and print output.
    """
    try:
        n, k, a, b, q = _read_initial_values()
    except (IOError, ValueError):
        return

    orders = _create_orders(n)
    bit_b, bit_a = _create_fenwick_trees(n)
    _process_queries(q, orders, bit_b, bit_a, n, k, a, b)


if __name__ == "__main__":
    solve()
```

- Kept `FenwickTree` and `solve` signatures unchanged to preserve the public interface.
- Extracted initial input reading into `_read_initial_values`, while leaving the original `try/except` in `solve` to preserve error handling behavior.
- Split initialization into `_create_orders` and `_create_fenwick_trees` so `solve` only coordinates high-level steps.
- Broke the query loop into `_process_queries`, `_read_query_line`, `_parse_query_line`, and `_dispatch_query` to separate reading, parsing, and routing.
- Decomposed update handling into small helpers for parsing, computing filled orders, updating stored orders, and applying Fenwick deltas.
- Decomposed question handling into helpers for parsing, prefix/range sum computation, and output writing.
- Preserved the original evaluation order, blank-line skipping, side effects, and exception propagation.