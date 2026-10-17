```python
import sys

# Increase recursion limit for deep segment tree traversals.
sys.setrecursionlimit(200005 + 5)


def _reconstruct_permutation(n, s):
    # Segment tree stores sums of available numbers.
    tree = [0] * (4 * n)

    def build(node, start, end):
        if start == end:
            tree[node] = start
            return

        mid = (start + end) // 2
        build(2 * node, start, mid)
        build(2 * node + 1, mid + 1, end)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

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

    def find_by_sum(node, start, end, k):
        if start == end:
            return start

        mid = (start + end) // 2
        left_sum = tree[2 * node]

        if k < left_sum:
            return find_by_sum(2 * node, start, mid, k)
        return find_by_sum(2 * node + 1, mid + 1, end, k - left_sum)

    build(1, 1, n)

    p = [0] * n
    for i in range(n - 1, -1, -1):
        value = find_by_sum(1, 1, n, s[i])
        p[i] = value
        update(1, 1, n, value, 0)

    return p


def solve():
    """Read input, reconstruct the permutation, and print it."""
    try:
        readline = sys.stdin.readline
        n = int(readline())
        s = list(map(int, readline().split()))
    except (IOError, ValueError):
        return

    print(*_reconstruct_permutation(n, s))


solve()
```

- Separated permutation reconstruction from input and output, making `solve()` easier to read without changing its interface.
- Removed a redundant `else` and shortened the reconstruction loop while retaining the same tree operations and error handling.