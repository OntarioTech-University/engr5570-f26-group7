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
    try:
        return tuple(map(int, sys.stdin.readline().strip().split()))
    except (IOError, ValueError):
        return None


def read_queries(q):
    for _ in range(q):
        yield sys.stdin.readline().strip()


def write_result(total_filled):
    sys.stdout.write(str(total_filled) + '\n')


def update_capped_tree(tree, day, old_orders, new_orders, capacity):
    delta = min(new_orders, capacity) - min(old_orders, capacity)
    if delta != 0:
        tree.update(day, delta)


def process_queries(n, k, a, b, query_lines, output_result):
    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)

    for line in query_lines:
        if not line:
            continue

        query = line.split()
        query_type = int(query[0])

        if query_type == 1:
            d, val = int(query[1]), int(query[2])
            old_orders = orders[d]
            orders[d] += val
            new_orders = orders[d]

            update_capped_tree(bit_b, d, old_orders, new_orders, b)
            update_capped_tree(bit_a, d, old_orders, new_orders, a)

        elif query_type == 2:
            p = int(query[1])
            sum_b = bit_b.query(p - 1)
            sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
            output_result(sum_b + sum_a)


def solve():
    """Read input, process queries, and print results."""
    parameters = read_parameters()
    if parameters is None:
        return

    n, k, a, b, q = parameters
    process_queries(n, k, a, b, read_queries(q), write_result)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Separated input reading, query processing, and output writing while retaining the existing `solve()` interface.
- Moved the repeated capped-tree update calculation into one helper.
- Kept query reading and output streaming in their original order, with execution starting through `main()` under the module guard.