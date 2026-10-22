Here is the refactored code:

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
    """
    Reads the problem parameters from standard input.
    Returns a tuple (n, k, a, b, q) or None if input is invalid.
    """
    try:
        n, k, a, b, q = map(int, sys.stdin.readline().strip().split())
        return n, k, a, b, q
    except (IOError, ValueError):
        return None


def process_update_query(orders, bit_b, bit_a, d, val, a, b):
    """
    Processes an update query for a given day.
    Updates the orders list and both Fenwick trees.
    """
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


def process_query(orders, bit_b, bit_a, n, k, a, b):
    """
    Processes a single query from standard input.
    Returns the result string for query type 2, or None for query type 1.
    """
    line = sys.stdin.readline().strip()
    if not line:
        return None
    
    query = line.split()
    query_type = int(query[0])

    if query_type == 1:
        d, val = int(query[1]), int(query[2])
        process_update_query(orders, bit_b, bit_a, d, val, a, b)
        return None
    elif query_type == 2:
        p = int(query[1])
        sum_b = bit_b.query(p - 1)
        sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
        total_filled = sum_b + sum_a
        return str(total_filled) + '\n'
    return None


def process_all_queries(orders, bit_b, bit_a, n, k, a, b, q):
    """
    Processes all queries and returns a list of output strings.
    """
    outputs = []
    for _ in range(q):
        result = process_query(orders, bit_b, bit_a, n, k, a, b)
        if result is not None:
            outputs.append(result)
    return outputs


def print_outputs(outputs):
    """
    Prints all output strings to standard output.
    """
    for output in outputs:
        sys.stdout.write(output)


def solve():
    """
    Main function to read input, process queries, and print output.
    """
    params = read_parameters()
    if params is None:
        return
    
    n, k, a, b, q = params
    
    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)
    
    outputs = process_all_queries(orders, bit_b, bit_a, n, k, a, b, q)
    print_outputs(outputs)


if __name__ == "__main__":
    solve()
```

**Summary of changes:**

- **Removed top-level logic**: All logic is now contained within functions; no code runs at the top level except the `if __name__ == "__main__":` guard.
- **Eliminated global variables**: All data is passed between functions via parameters and return values.
- **Separated concerns into functions**: 
  - `read_parameters()` handles input reading.
  - `process_update_query()` handles the update logic.
  - `process_query()` handles a single query and returns output if applicable.
  - `process_all_queries()` orchestrates query processing and collects outputs.
  - `print_outputs()` handles output printing.
- **Removed duplicated code**: The update logic for both Fenwick trees is now in a single helper function `process_update_query()`, eliminating duplication.
- **Preserved behavior**: The refactoring maintains the exact same runtime behavior, including input handling, output formatting, and exception handling.