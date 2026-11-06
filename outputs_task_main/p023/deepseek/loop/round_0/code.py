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
    Read problem parameters from standard input.
    Returns a tuple (n, k, a, b, q) or None if input is invalid.
    """
    try:
        n, k, a, b, q = map(int, sys.stdin.readline().strip().split())
        return n, k, a, b, q
    except (IOError, ValueError):
        return None


def read_query():
    """
    Read a single query from standard input.
    Returns a list of query parts or None if no more input.
    """
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def process_update_query(query_parts, orders, bit_b, bit_a, b, a):
    """
    Process an update query (type 1).
    Updates the orders list and both Fenwick trees.
    """
    d, val = int(query_parts[1]), int(query_parts[2])
    
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


def process_query_query(query_parts, bit_b, bit_a, n, k):
    """
    Process a question query (type 2).
    Returns the total filled orders as an integer.
    """
    p = int(query_parts[1])
    
    sum_b = bit_b.query(p - 1)
    sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
    
    return sum_b + sum_a


def process_queries(n, k, a, b, q):
    """
    Process all queries and return a list of output strings.
    """
    orders = [0] * (n + 1)
    bit_b = FenwickTree(n)
    bit_a = FenwickTree(n)
    outputs = []
    
    for _ in range(q):
        query_parts = read_query()
        if query_parts is None:
            continue
        
        query_type = int(query_parts[0])
        
        if query_type == 1:
            process_update_query(query_parts, orders, bit_b, bit_a, b, a)
        elif query_type == 2:
            result = process_query_query(query_parts, bit_b, bit_a, n, k)
            outputs.append(str(result))
    
    return outputs


def print_outputs(outputs):
    """
    Print all output strings to standard output.
    """
    for output in outputs:
        sys.stdout.write(output + '\n')


def solve():
    """
    Main function to read input, process queries, and print output.
    """
    params = read_parameters()
    if params is None:
        return
    
    n, k, a, b, q = params
    outputs = process_queries(n, k, a, b, q)
    print_outputs(outputs)


if __name__ == "__main__":
    solve()
