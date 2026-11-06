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


def read_parameters():
    return map(int, sys.stdin.readline().strip().split())


def read_query():
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def filled_orders(orders, day, b, a):
    return min(orders[day], b), min(orders[day], a)


def update_tree(tree, day, old_filled, new_filled):
    delta = new_filled - old_filled
    if delta != 0:
        tree.update(day, delta)


def print_output(total_filled):
    sys.stdout.write(str(total_filled) + '\n')


def process_queries(n, k, a, b, q):
    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)

    for _ in range(q):
        query = read_query()
        if query is None:
            continue

        query_type = int(query[0])

        if query_type == 1:
            d, val = int(query[1]), int(query[2])

            old_filled_b, old_filled_a = filled_orders(orders, d, b, a)
            orders[d] += val
            new_filled_b, new_filled_a = filled_orders(orders, d, b, a)

            update_tree(bit_b, d, old_filled_b, new_filled_b)
            update_tree(bit_a, d, old_filled_a, new_filled_a)

        elif query_type == 2:
            p = int(query[1])
            sum_b = bit_b.query(p - 1)
            sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
            print_output(sum_b + sum_a)


def solve():
    """
    Read input, process queries, and print output.
    """
    try:
        n, k, a, b, q = read_parameters()
    except (IOError, ValueError):
        return

    process_queries(n, k, a, b, q)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Separated input reading, query processing, and output writing into named functions while retaining `solve()` and its signature.
- Moved repeated capacity calculations and tree-update logic into helpers.
- Kept state local to the computation and added a `main()` entry point; queries are still read and answered in order.