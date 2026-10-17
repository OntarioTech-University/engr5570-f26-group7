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


def _apply_update_query(query, orders, bit_b, bit_a, capacity_a, capacity_b):
    """
    Applies a type-1 query by updating the day order count and the two
    Fenwick trees according to the capped fillable-order changes.
    """
    d, val = int(query[1]), int(query[2])

    old_filled_b = min(orders[d], capacity_b)
    old_filled_a = min(orders[d], capacity_a)

    orders[d] += val

    new_filled_b = min(orders[d], capacity_b)
    new_filled_a = min(orders[d], capacity_a)

    delta_b = new_filled_b - old_filled_b
    if delta_b != 0:
        bit_b.update(d, delta_b)

    delta_a = new_filled_a - old_filled_a
    if delta_a != 0:
        bit_a.update(d, delta_a)


def _answer_query(query, bit_b, bit_a, n, k):
    """
    Computes the answer for a type-2 query:
    orders filled before maintenance plus orders filled after maintenance.
    """
    p = int(query[1])

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
            _apply_update_query(query, orders, bit_b, bit_a, a, b)
        elif query_type == 2:
            total_filled = _answer_query(query, bit_b, bit_a, n, k)
            sys.stdout.write(str(total_filled) + '\n')


if __name__ == "__main__":
    solve()
```

- Extracted the type-1 update logic into `_apply_update_query` to reduce the size of `solve` and isolate the state mutation logic.
- Extracted the type-2 computation into `_answer_query` to separate answer calculation from output handling.
- Kept the original parsing, exception handling, loop structure, public names, and output behavior unchanged to preserve runtime semantics.
- Left `FenwickTree` unchanged because it is already small, clear, and stable.