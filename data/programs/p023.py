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

def solve():
    """
    Main function to read input, process queries, and print output.
    """
    try:
        # Read problem parameters
        n, k, a, b, q = map(int, sys.stdin.readline().strip().split())
    except (IOError, ValueError):
        # Handle cases with no input
        return

    # orders[d] stores the total number of orders for day d.
    # We use a simple list as we only need point access to update it.
    # The size is n+1 for 1-based indexing (days 1 to n).
    orders = [0] * (n + 1)

    # We use two Fenwick Trees to maintain sums efficiently.
    
    # bit_b will maintain prefix sums for the production rate 'b'.
    # Each element at index 'd' conceptually stores min(orders[d], b).
    bit_b = FenwickTree(n)
    
    # bit_a will maintain prefix sums for the production rate 'a'.
    # Each element at index 'd' conceptually stores min(orders[d], a).
    bit_a = FenwickTree(n)

    # Process all q queries
    for _ in range(q):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        
        query = line.split()
        query_type = int(query[0])

        if query_type == 1:
            # This is an update query: 1 d_i a_i
            # It adds 'a_i' new orders for day 'd_i'.
            d, val = int(query[1]), int(query[2])
            
            # To update the Fenwick Trees, we calculate the change (delta)
            # in the number of fillable orders for day 'd'.
            
            # Fillable orders before the update
            old_filled_b = min(orders[d], b)
            old_filled_a = min(orders[d], a)
            
            # Update the total orders for day 'd'
            orders[d] += val
            
            # Fillable orders after the update
            new_filled_b = min(orders[d], b)
            new_filled_a = min(orders[d], a)
            
            # Calculate the deltas and update the trees if there's a change.
            delta_b = new_filled_b - old_filled_b
            if delta_b != 0:
                bit_b.update(d, delta_b)
            
            delta_a = new_filled_a - old_filled_a
            if delta_a != 0:
                bit_a.update(d, delta_a)

        elif query_type == 2:
            # This is a question query: 2 p_i
            # It asks for the max orders filled if maintenance starts on day 'p_i'.
            p = int(query[1])
            
            # The total filled orders is the sum of two parts:
            # 1. Orders filled before maintenance: days [1, p-1] with capacity 'b'.
            # 2. Orders filled after maintenance: days [p+k, n] with capacity 'a'.
            
            # Part 1: Sum for days [1, p-1] with capacity 'b'.
            # This is a prefix sum query on bit_b.
            sum_b = bit_b.query(p - 1)
            
            # Part 2: Sum for days [p+k, n] with capacity 'a'.
            # This is a range sum query on bit_a.
            # A range sum [L, R] is calculated as query(R) - query(L-1).
            # Here, L = p+k and R = n.
            sum_a = bit_a.query(n) - bit_a.query(p + k - 1)
            
            # The total is the sum of the two parts.
            total_filled = sum_b + sum_a
            sys.stdout.write(str(total_filled) + '\n')

if __name__ == "__main__":
    solve()
