import sys

# Increase recursion limit for deep segment tree traversals.
sys.setrecursionlimit(200005 + 5)


def _read_input():
    try:
        readline = sys.stdin.readline
        n = int(readline())
        s = list(map(int, readline().split()))
    except (IOError, ValueError):
        return None
    return n, s


def _build_tree(tree, node, start, end):
    if start == end:
        tree[node] = start
        return
    mid = (start + end) // 2
    _build_tree(tree, 2 * node, start, mid)
    _build_tree(tree, 2 * node + 1, mid + 1, end)
    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _update_tree(tree, node, start, end, idx, val):
    if start == end:
        tree[node] = val
        return
    mid = (start + end) // 2
    if start <= idx <= mid:
        _update_tree(tree, 2 * node, start, mid, idx, val)
    else:
        _update_tree(tree, 2 * node + 1, mid + 1, end, idx, val)
    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _find_by_sum(tree, node, start, end, k):
    if start == end:
        return start
    mid = (start + end) // 2
    left_sum = tree[2 * node]
    if k < left_sum:
        return _find_by_sum(tree, 2 * node, start, mid, k)
    return _find_by_sum(tree, 2 * node + 1, mid + 1, end, k - left_sum)


def _recover_permutation(n, s, tree):
    p = [0] * n
    for i in range(n - 1, -1, -1):
        value = _find_by_sum(tree, 1, 1, n, s[i])
        p[i] = value
        _update_tree(tree, 1, 1, n, value, 0)
    return p


def _print_result(p):
    print(*p)


def solve():
    """Read input, recover the permutation, and print it."""
    inputs = _read_input()
    if inputs is None:
        return
    n, s = inputs
    tree = [0] * (4 * n)
    _build_tree(tree, 1, 1, n)
    p = _recover_permutation(n, s, tree)
    _print_result(p)


solve()
