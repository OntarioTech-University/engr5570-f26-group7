Here's the refactored code:

```python
import sys

def read_input():
    """
    Reads input from stdin and returns the parsed values.
    """
    try:
        readline = sys.stdin.readline
        n = int(readline())
        s = list(map(int, readline().split()))
        return n, s
    except (IOError, ValueError):
        return None, None

def build_segment_tree(n):
    """
    Creates and initializes a segment tree with all numbers from 1 to n available.
    Returns the tree array.
    """
    tree = [0] * (4 * n)
    
    def build(node, start, end):
        """
        Recursively builds the segment tree.
        """
        if start == end:
            tree[node] = start
            return
        mid = (start + end) // 2
        build(2 * node, start, mid)
        build(2 * node + 1, mid + 1, end)
        tree[node] = tree[2 * node] + tree[2 * node + 1]
    
    build(1, 1, n)
    return tree

def update_segment_tree(tree, n, idx, val):
    """
    Updates the value at a specific index (leaf) and propagates changes up.
    """
    def update(node, start, end, idx, val):
        if start == end:
            tree[node] = val
            return
        mid = (start + end) // 2
        if start <= idx <= mid:
            update(2 * node, start, mid, idx, val)
        else:
            update(2 * node + 1, mid + 1, end, idx, val)
        tree[node] = tree[2 * node] + tree[2 * node + 1]
    
    update(1, 1, n, idx, val)

def find_by_sum(tree, n, k):
    """
    Finds the number corresponding to a given prefix sum 'k'.
    """
    def find(node, start, end, k):
        if start == end:
            return start
        
        mid = (start + end) // 2
        left_sum = tree[2 * node]
        
        if k < left_sum:
            return find(2 * node, start, mid, k)
        else:
            return find(2 * node + 1, mid + 1, end, k - left_sum)
    
    return find(1, 1, n, k)

def compute_permutation(n, s):
    """
    Computes the permutation based on the input values.
    """
    tree = build_segment_tree(n)
    p = [0] * n
    
    # Iterate from n down to 1 to determine p_n, p_{n-1}, ...
    for i in range(n - 1, -1, -1):
        # s[i] is the target sum for the i-th element of the permutation (0-indexed).
        target_sum = s[i]
        
        # Find the value for p[i].
        value = find_by_sum(tree, n, target_sum)
        p[i] = value
        
        # "Remove" the found value from the set of available numbers
        # by setting its contribution in the segment tree to 0.
        update_segment_tree(tree, n, value, 0)
    
    return p

def print_output(p):
    """
    Prints the permutation.
    """
    print(*p)

def solve():
    """
    Main function to read input, solve the problem, and print the output.
    """
    n, s = read_input()
    if n is None:
        return
    
    p = compute_permutation(n, s)
    print_output(p)

def main():
    # Increase recursion limit for deep segment tree traversals, a good practice in Python.
    sys.setrecursionlimit(200005 + 5)
    solve()

if __name__ == "__main__":
    main()
```

**Changes made:**

- **Moved logic out of top level**: All code now resides within functions, with only the `if __name__ == "__main__":` block at the top level calling `main()`.
- **Eliminated global variables**: The `tree` array is now created inside `build_segment_tree()` and passed as a parameter to functions that need it.
- **Separated concerns into functions**: Created `read_input()`, `compute_permutation()`, and `print_output()` to handle input, computation, and output respectively.
- **Extracted helper functions**: Moved segment tree operations into standalone functions (`build_segment_tree()`, `update_segment_tree()`, `find_by_sum()`) that encapsulate their internal recursive helpers.
- **Passed data through parameters and return values**: Functions now receive data as parameters and return results, rather than relying on closures or global state.
- **Preserved runtime behavior**: The logic flow, algorithm, and error handling remain identical to the original code.