import sys

# Increase recursion limit for deep segment tree traversals, a good practice in Python.
sys.setrecursionlimit(200005 + 5)


def solve():
    """
    Main function to read input, solve the problem, and print the output.
    """
    n, s = _read_input()
    if n is None:
        return

    tree = [0] * (4 * n)
    _build_segment_tree(tree, 1, 1, n)

    p = _construct_permutation(tree, n, s)
    print(*p)


def _read_input():
    """
    Reads and parses input. Returns (n, s) or (None, None) on failure.
    """
    try:
        readline = sys.stdin.readline
        n = int(readline())
        s = list(map(int, readline().split()))
        return n, s
    except (IOError, ValueError):
        return None, None


def _build_segment_tree(tree, node, start, end):
    """
    Recursively builds the segment tree with initial values.
    """
    if start == end:
        tree[node] = start
        return

    mid = (start + end) // 2
    _build_segment_tree(tree, 2 * node, start, mid)
    _build_segment_tree(tree, 2 * node + 1, mid + 1, end)
    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _update_segment_tree(tree, node, start, end, idx, val):
    """
    Updates the value at a specific index (leaf) and propagates changes up.
    """
    if start == end:
        tree[node] = val
        return

    mid = (start + end) // 2
    if start <= idx <= mid:
        _update_segment_tree(tree, 2 * node, start, mid, idx, val)
    else:
        _update_segment_tree(tree, 2 * node + 1, mid + 1, end, idx, val)

    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _find_by_sum(tree, node, start, end, k):
    """
    Finds the number corresponding to a given prefix sum 'k'.
    """
    if start == end:
        return start

    mid = (start + end) // 2
    left_sum = tree[2 * node]

    if k < left_sum:
        return _find_by_sum(tree, 2 * node, start, mid, k)
    return _find_by_sum(tree, 2 * node + 1, mid + 1, end, k - left_sum)


def _construct_permutation(tree, n, s):
    """
    Constructs the permutation by iterating from n down to 1.
    """
    p = [0] * n

    for i in range(n - 1, -1, -1):
        target_sum = s[i]
        value = _find_by_sum(tree, 1, 1, n, target_sum)
        p[i] = value
        _update_segment_tree(tree, 1, 1, n, value, 0)

    return p


solve()
