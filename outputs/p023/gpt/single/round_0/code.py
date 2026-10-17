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


def _add_orders(orders, d, val, b, a, bit_b, bit_a):
    """Update one day's orders and the corresponding capped sums."""
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


def _filled_orders(p, k, n, bit_b, bit_a):
    """Sum orders filled before and after the maintenance period."""
    sum_b = bit_b.query(p - 1)
    sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
    return sum_b + sum_a


def solve():
    """
    Main function to read input, process queries, and print output.
    """
    try:
        n, k, a, b, q = map(int, sys.stdin.readline().strip().split())
    except (IOError, ValueError):
        return

    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)

    for _ in range(q):
        line = sys.stdin.readline().strip()
        if not line:
            continue

        query = line.split()
        query_type = int(query[0])

        if query_type == 1:
            d, val = int(query[1]), int(query[2])
            _add_orders(orders, d, val, b, a, bit_b, bit_a)
        elif query_type == 2:
            p = int(query[1])
            total_filled = _filled_orders(p, k, n, bit_b, bit_a)
            sys.stdout.write(str(total_filled) + '\n')


if __name__ == "__main__":
    solve()
