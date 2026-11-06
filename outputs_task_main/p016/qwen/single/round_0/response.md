```python
import sys


def _configure_recursion_limit():
    # Increase recursion limit for deep segment tree traversals, a good practice in Python.
    sys.setrecursionlimit(200005 + 5)


def _read_input():
    readline = sys.stdin.readline
    n = int(readline())
    s = list(map(int, readline().split()))
    return n, s


def _compute_permutation(n, s):
    # Segment Tree stores sums of available numbers.
    # Size 4*n is a safe upper bound for the array representation.
    tree = [0] * (4 * n)

    def midpoint(start, end):
        return (start + end) // 2

    def left_child(node):
        return 2 * node

    def right_child(node):
        return 2 * node + 1

    def refresh_node(node):
        tree[node] = tree[left_child(node)] + tree[right_child(node)]

    def build(node, start, end):
        """
        Recursively builds the segment tree.
        """
        if start == end:
            tree[node] = start
            return
        mid = midpoint(start, end)
        build(left_child(node), start, mid)
        build(right_child(node), mid + 1, end)
        refresh_node(node)

    def update(node, start, end, idx, val):
        """
        Updates the value at a specific index (leaf) and propagates changes up.
        """
        if start == end:
            tree[node] = val
            return
        mid = midpoint(start, end)
        if start <= idx <= mid:
            update(left_child(node), start, mid, idx, val)
        else:
            update(right_child(node), mid + 1, end, idx, val)
        refresh_node(node)

    def find_by_sum(node, start, end, k):
        """
        Finds the number corresponding to a given prefix sum 'k'.
        """
        if start == end:
            return start

        mid = midpoint(start, end)
        left = left_child(node)
        left_sum = tree[left]

        if k < left_sum:
            return find_by_sum(left, start, mid, k)
        else:
            return find_by_sum(right_child(node), mid + 1, end, k - left_sum)

    # Initialize the segment tree with all numbers from 1 to n available.
    build(1, 1, n)

    p = [0] * n
    # Iterate from n down to 1 to determine p_n, p_{n-1}, ...
    for i in range(n - 1, -1, -1):
        # s[i] is the target sum for the i-th element of the permutation (0-indexed).
        target_sum = s[i]

        # Find the value for p[i].
        value = find_by_sum(1, 1, n, target_sum)
        p[i] = value

        # "Remove" the found value from the set of available numbers
        # by setting its contribution in the segment tree to 0.
        update(1, 1, n, value, 0)

    return p


def _print_output(p):
    print(*p)


def solve():
    """
    Main function to read input, solve the problem, and print the output.
    """
    _configure_recursion_limit()

    try:
        n, s = _read_input()
    except (IOError, ValueError):
        return

    p = _compute_permutation(n, s)
    _print_output(p)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Replaced the top-level `solve()` call with a `main()` function invoked under `if __name__ == "__main__":`, so no program logic runs at import time.
- Moved recursion-limit setup into `_configure_recursion_limit()` and kept the same limit value, preserving the runtime recursion configuration before segment-tree operations.
- Split the monolithic `solve()` into `_read_input()`, `_compute_permutation()`, and `_print_output()`, passing data explicitly through parameters and return values.
- Kept the public `solve()` function name and signature unchanged; it now orchestrates the separated steps.
- Extracted repeated segment-tree details (`midpoint`, child indices, and parent-node sum refresh) into shared nested helper functions to reduce duplication.
- Preserved the original input exception handling: only `IOError` and `ValueError` during input reading are caught and cause an early return.