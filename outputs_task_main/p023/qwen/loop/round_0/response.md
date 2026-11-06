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


def read_problem_parameters():
    """
    Reads the first input line and returns the problem parameters.
    Returns None if the line is missing or cannot be parsed.
    """
    import sys
    try:
        n, k, a, b, q = map(int, sys.stdin.readline().strip().split())
    except (IOError, ValueError):
        return None
    return n, k, a, b, q


def read_query_tokens():
    """
    Reads one query line and returns its tokens.
    Returns None for a blank line.
    """
    import sys
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def write_result(value):
    """
    Writes one query result to standard output.
    """
    import sys
    sys.stdout.write(str(value) + '\n')


def update_tree_if_changed(bit, index, delta):
    """
    Applies a Fenwick Tree update only when the delta is non-zero.
    """
    if delta != 0:
        bit.update(index, delta)


def apply_order_update(orders, bit_b, bit_a, day, added_orders, capacity_b, capacity_a):
    """
    Updates the per-day order count and both Fenwick Trees for one day.
    """
    old_filled_b = min(orders[day], capacity_b)
    old_filled_a = min(orders[day], capacity_a)

    orders[day] += added_orders

    new_filled_b = min(orders[day], capacity_b)
    new_filled_a = min(orders[day], capacity_a)

    delta_b = new_filled_b - old_filled_b
    update_tree_if_changed(bit_b, day, delta_b)

    delta_a = new_filled_a - old_filled_a
    update_tree_if_changed(bit_a, day, delta_a)


def compute_filled_orders(bit_b, bit_a, n, k, maintenance_start):
    """
    Computes the total number of filled orders for a maintenance query.
    """
    sum_b = bit_b.query(maintenance_start - 1)
    sum_a = bit_a.query(n) - bit_a.query(maintenance_start + k - 1)
    return sum_b + sum_a


def process_queries(n, k, a, b, q):
    """
    Processes all queries, updating internal state and printing answers.
    """
    orders = [0] * (n + 1)

    # bit_b maintains prefix sums capped by production rate b.
    bit_b = FenwickTree(n)

    # bit_a maintains prefix sums capped by production rate a.
    bit_a = FenwickTree(n)

    for _ in range(q):
        query = read_query_tokens()
        if query is None:
            continue

        query_type = int(query[0])

        if query_type == 1:
            d, val = int(query[1]), int(query[2])
            apply_order_update(orders, bit_b, bit_a, d, val, b, a)

        elif query_type == 2:
            p = int(query[1])
            total_filled = compute_filled_orders(bit_b, bit_a, n, k, p)
            write_result(total_filled)


def main():
    """
    Program entry point: reads parameters and processes all queries.
    """
    parameters = read_problem_parameters()
    if parameters is None:
        return

    n, k, a, b, q = parameters
    process_queries(n, k, a, b, q)


def solve():
    """
    Backward-compatible public entry point.
    """
    main()


if __name__ == "__main__":
    main()
```

- Added `main()` and made the script call it under `if __name__ == "__main__":`, so executable logic is not run directly at the top level.
- Kept `solve()` with its original public signature as a thin wrapper to avoid breaking external callers.
- Moved initial input parsing into `read_problem_parameters()`, preserving the original caught exceptions and early-return behavior.
- Moved per-line query reading into `read_query_tokens()`, preserving blank-line skipping and exception propagation.
- Moved output printing into `write_result()`, keeping the exact output format.
- Moved the main query-processing loop and state initialization into `process_queries()`, passing all needed data through parameters.
- Extracted the repeated non-zero Fenwick update logic into `update_tree_if_changed()`.
- Extracted the update-query state transition into `apply_order_update()` to centralize the previously duplicated update logic.
- Extracted the range-sum calculation into `compute_filled_orders()` while preserving the original query call order.
- Avoided module-level mutable/global state; `sys` is imported locally inside I/O helpers to keep the module top level limited to definitions only.