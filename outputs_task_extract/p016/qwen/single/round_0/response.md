```python
import sys

# Increase recursion limit for deep segment tree traversals, a good practice in Python.
sys.setrecursionlimit(200005 + 5)


def _read_input():
    readline = sys.stdin.readline
    n = int(readline())
    s = list(map(int, readline().split()))
    return n, s


def _build(tree, node, start, end):
    if start == end:
        tree[node] = start
        return

    mid = (start + end) // 2
    _build(tree, 2 * node, start, mid)
    _build(tree, 2 * node + 1, mid + 1, end)
    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _update(tree, node, start, end, idx, val):
    if start == end:
        tree[node] = val
        return

    mid = (start + end) // 2
    if start <= idx <= mid:
        _update(tree, 2 * node, start, mid, idx, val)
    else:
        _update(tree, 2 * node + 1, mid + 1, end, idx, val)

    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _find_by_sum(tree, node, start, end, k):
    if start == end:
        return start

    mid = (start + end) // 2
    left_sum = tree[2 * node]

    if k < left_sum:
        return _find_by_sum(tree, 2 * node, start, mid, k)

    return _find_by_sum(tree, 2 * node + 1, mid + 1, end, k - left_sum)


def _initialize_tree(n):
    tree = [0] * (4 * n)
    _build(tree, 1, 1, n)
    return tree


def _reconstruct_permutation(n, s, tree):
    p = [0] * n

    for i in range(n - 1, -1, -1):
        target_sum = s[i]
        value = _find_by_sum(tree, 1, 1, n, target_sum)
        p[i] = value
        _update(tree, 1, 1, n, value, 0)

    return p


def _print_output(p):
    print(*p)


def solve():
    """
    Main function to read input, solve the problem, and print the output.
    """
    try:
        n, s = _read_input()
    except (IOError, ValueError):
        return

    tree = _initialize_tree(n)
    p = _reconstruct_permutation(n, s, tree)
    _print_output(p)


solve()
```

- Extracted input reading into `_read_input()` so parsing is isolated while preserving the original exception handling in `solve()`.
- Moved segment tree construction, update, and query logic into small private helper functions: `_build()`, `_update()`, and `_find_by_sum()`.
- Added `_initialize_tree()` to encapsulate tree allocation and initial construction as one clear setup step.
- Added `_reconstruct_permutation()` to contain the permutation reconstruction loop and tree mutation steps.
- Added `_print_output()` to isolate output printing.
- Kept `solve()`’s public signature, top-level invocation, control flow, error handling, and observable behavior unchanged.