```python
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


def _read_initial_parameters(input_stream):
    """
    Reads the first input line and parses the problem parameters.

    Returns:
        A tuple (n, k, a, b, q) on success.
        None if the first line is missing or invalid.
    """
    try:
        n, k, a, b, q = map(int, input_stream.readline().strip().split())
    except (IOError, ValueError):
        return None
    return n, k, a, b, q


def _read_query_tokens(input_stream):
    """
    Reads one query line and splits it into tokens.

    Returns:
        A list of tokens for a non-blank line.
        None for a blank line.
    """
    line = input_stream.readline().strip()
    if not line:
        return None
    return line.split()


def _write_total(output_stream, total_filled):
    """
    Writes one query answer using the original output format.
    """
    output_stream.write(str(total_filled) + '\n')


def _add_capped_delta(tree, index, old_total, new_total, capacity):
    """
    Updates a Fenwick Tree by the change in min(total, capacity).
    """
    delta = min(new_total, capacity) - min(old_total, capacity)
    if delta != 0:
        tree.update(index, delta)


def _apply_order_update(orders, bit_b, bit_a, d, val, capacity_a, capacity_b):
    """
    Applies an order-increase query to the raw order counts and both trees.
    """
    old_total = orders[d]
    new_total = old_total + val
    orders[d] = new_total

    _add_capped_delta(bit_b, d, old_total, new_total, capacity_b)
    _add_capped_delta(bit_a, d, old_total, new_total, capacity_a)


def _compute_filled_orders(bit_b, bit_a, n, k, p):
    """
    Computes the answer for a maintenance-start query.
    """
    sum_b = bit_b.query(p - 1)
    sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
    return sum_b + sum_a


def _process_queries(input_stream, output_stream, n, k, a, b, q):
    """
    Processes all queries using Fenwick trees and per-day order totals.
    """
    orders = [0] * (n + 1)

    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)

    for _ in range(q):
        query = _read_query_tokens(input_stream)
        if query is None:
            continue

        query_type = int(query[0])

        if query_type == 1:
            d = int(query[1])
            val = int(query[2])
            _apply_order_update(orders, bit_b, bit_a, d, val, a, b)

        elif query_type == 2:
            p = int(query[1])
            total_filled = _compute_filled_orders(bit_b, bit_a, n, k, p)
            _write_total(output_stream, total_filled)


def main():
    """
    Program entry point.
    """
    import sys

    params = _read_initial_parameters(sys.stdin)
    if params is None:
        return

    n, k, a, b, q = params
    _process_queries(sys.stdin, sys.stdout, n, k, a, b, q)


def solve():
    """
    Main function to read input, process queries, and print output.

    Kept with its original public signature for backward compatibility.
    """
    main()


if __name__ == "__main__":
    main()
```

- Added a `main()` entry point and moved the top-level call under `if __name__ == "__main__":`, so no program logic runs during import.
- Kept `solve()` with its original signature as a thin wrapper to preserve the existing public interface.
- Extracted first-line parsing into `_read_initial_parameters()`, preserving the original `IOError`/`ValueError` handling and early return behavior.
- Extracted per-query line reading into `_read_query_tokens()`, preserving blank-line skipping and EOF behavior.
- Moved the core loop and state handling into `_process_queries()`, passing all needed data through parameters.
- Extracted answer computation into `_compute_filled_orders()` and output writing into `_write_total()` to separate computation from printing.
- Removed duplicated update logic by introducing `_add_capped_delta()` and `_apply_order_update()`, while preserving the original update order and side effects.
- Avoided module-level mutable state; streams and data are passed explicitly through function parameters.