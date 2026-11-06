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


def _read_parameters():
    return map(int, sys.stdin.readline().strip().split())


def _read_query():
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def _create_order_state(n):
    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)
    return orders, bit_b, bit_a


def _update_orders(query, orders, a, b, bit_a, bit_b):
    d, val = int(query[1]), int(query[2])
    old_filled_b = min(orders[d], b)
    old_filled_a = min(orders[d], a)
    orders[d] += val
    new_filled_b = min(orders[d], b)
    new_filled_a = min(orders[d], a)
    delta_b = new_filled_b - old_filled_b
    if delta_b != 0:
        bit_b.update(d, delta_b)
    delta_a = new_filled_a - old_filled_a
    if delta_a != 0:
        bit_a.update(d, delta_a)


def _calculate_filled_orders(p, n, k, bit_a, bit_b):
    sum_b = bit_b.query(p - 1)
    sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
    return sum_b + sum_a


def _write_result(total_filled):
    sys.stdout.write(str(total_filled) + '\n')


def _process_query(query, orders, n, k, a, b, bit_a, bit_b):
    query_type = int(query[0])
    if query_type == 1:
        _update_orders(query, orders, a, b, bit_a, bit_b)
    elif query_type == 2:
        p = int(query[1])
        total_filled = _calculate_filled_orders(p, n, k, bit_a, bit_b)
        _write_result(total_filled)


def _process_queries(q, orders, n, k, a, b, bit_a, bit_b):
    for _ in range(q):
        query = _read_query()
        if query is None:
            continue
        _process_query(query, orders, n, k, a, b, bit_a, bit_b)


def solve():
    """
    Read input, process queries, and print output.
    """
    try:
        n, k, a, b, q = _read_parameters()
    except (IOError, ValueError):
        return

    orders, bit_b, bit_a = _create_order_state(n)
    _process_queries(q, orders, n, k, a, b, bit_a, bit_b)


if __name__ == "__main__":
    solve()
