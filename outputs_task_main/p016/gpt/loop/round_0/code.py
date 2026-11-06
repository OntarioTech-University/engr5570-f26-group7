import sys


def _read_input():
    try:
        readline = sys.stdin.readline
        n = int(readline())
        s = list(map(int, readline().split()))
    except (IOError, ValueError):
        return None
    return n, s


def _refresh_node(tree, node):
    tree[node] = tree[2 * node] + tree[2 * node + 1]


def _build(tree, node, start, end):
    if start == end:
        tree[node] = start
        return

    mid = (start + end) // 2
    _build(tree, 2 * node, start, mid)
    _build(tree, 2 * node + 1, mid + 1, end)
    _refresh_node(tree, node)


def _update(tree, node, start, end, idx, val):
    if start == end:
        tree[node] = val
        return

    mid = (start + end) // 2
    if start <= idx <= mid:
        _update(tree, 2 * node, start, mid, idx, val)
    else:
        _update(tree, 2 * node + 1, mid + 1, end, idx, val)
    _refresh_node(tree, node)


def _find_by_sum(tree, node, start, end, k):
    if start == end:
        return start

    mid = (start + end) // 2
    left_sum = tree[2 * node]

    if k < left_sum:
        return _find_by_sum(tree, 2 * node, start, mid, k)
    else:
        return _find_by_sum(tree, 2 * node + 1, mid + 1, end, k - left_sum)


def _compute_permutation(n, s):
    tree = [0] * (4 * n)
    _build(tree, 1, 1, n)

    p = [0] * n
    for i in range(n - 1, -1, -1):
        value = _find_by_sum(tree, 1, 1, n, s[i])
        p[i] = value
        _update(tree, 1, 1, n, value, 0)

    return p


def _print_output(p):
    print(*p)


def solve():
    """Read input, compute the permutation, and print it."""
    sys.setrecursionlimit(200005 + 5)

    data = _read_input()
    if data is None:
        return

    n, s = data
    p = _compute_permutation(n, s)
    _print_output(p)


def main():
    solve()


if __name__ == "__main__":
    main()
