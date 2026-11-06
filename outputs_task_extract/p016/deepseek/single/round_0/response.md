```python
import sys

sys.setrecursionlimit(200005 + 5)

def read_input():
    """Read n and the target sums from stdin."""
    readline = sys.stdin.readline
    n = int(readline())
    s = list(map(int, readline().split()))
    return n, s

def build_segment_tree(tree, node, start, end):
    """Recursively build the segment tree with initial values."""
    if start == end:
        tree[node] = start
        return
    mid = (start + end) // 2
    build_segment_tree(tree, 2 * node, start, mid)
    build_segment_tree(tree, 2 * node + 1, mid + 1, end)
    tree[node] = tree[2 * node] + tree[2 * node + 1]

def update_segment_tree(tree, node, start, end, idx, val):
    """Update a leaf and propagate the change up the tree."""
    if start == end:
        tree[node] = val
        return
    mid = (start + end) // 2
    if start <= idx <= mid:
        update_segment_tree(tree, 2 * node, start, mid, idx, val)
    else:
        update_segment_tree(tree, 2 * node + 1, mid + 1, end, idx, val)
    tree[node] = tree[2 * node] + tree[2 * node + 1]

def find_by_sum(tree, node, start, end, k):
    """Find the number corresponding to a given prefix sum k."""
    if start == end:
        return start
    mid = (start + end) // 2
    left_sum = tree[2 * node]
    if k < left_sum:
        return find_by_sum(tree, 2 * node, start, mid, k)
    else:
        return find_by_sum(tree, 2 * node + 1, mid + 1, end, k - left_sum)

def compute_permutation(n, s):
    """Build the permutation from the target sums."""
    tree = [0] * (4 * n)
    build_segment_tree(tree, 1, 1, n)
    p = [0] * n
    for i in range(n - 1, -1, -1):
        target_sum = s[i]
        value = find_by_sum(tree, 1, 1, n, target_sum)
        p[i] = value
        update_segment_tree(tree, 1, 1, n, value, 0)
    return p

def print_permutation(p):
    """Print the permutation space-separated."""
    print(*p)

def solve():
    """
    Main function to read input, solve the problem, and print the output.
    """
    try:
        n, s = read_input()
    except (IOError, ValueError):
        return
    p = compute_permutation(n, s)
    print_permutation(p)

solve()
```

- Extracted input reading into `read_input()` to isolate I/O and parsing.
- Moved segment tree operations (`build_segment_tree`, `update_segment_tree`, `find_by_sum`) to module-level functions with an explicit `tree` parameter, improving reusability and testability.
- Extracted permutation construction into `compute_permutation()` to separate the core algorithm from I/O.
- Extracted output printing into `print_permutation()`.
- Kept `solve()` as the public entry point, now orchestrating the smaller functions while preserving original exception handling and flow.
- No behavior changes: same recursion limit, same algorithm, same output format, and same top-level `solve()` call.