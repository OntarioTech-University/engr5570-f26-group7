import sys
sys.setrecursionlimit(200005 + 5)

def solve():
    """
    Main function to read input, solve the problem, and print the output.
    """
    try:
        readline = sys.stdin.readline
        n = int(readline())
        s = list(map(int, readline().split()))
    except (IOError, ValueError):
        return
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

    def update(node, start, end, idx, val):
        """
        Updates the value at a specific index (leaf) and propagates changes up.
        """
        if start == end:
            tree[node] = val
            return
        mid = (start + end) // 2
        if start < idx <= mid:
            update(2 * node, start, mid, idx, val)
        else:
            update(2 * node + 1, mid + 1, end, idx, val)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    def find_by_sum(node, start, end, k):
        """
        Finds the number corresponding to a given prefix sum 'k'.
        """
        if start == end:
            return start
        mid = (start + end) // 2
        left_sum = tree[2 * node]
        if k < left_sum:
            return find_by_sum(2 * node, start, mid, k)
        else:
            return find_by_sum(2 * node + 1, mid + 1, end, k - left_sum)
    build(1, 1, n)
    p = [0] * n
    for i in range(n - 1, -1, -1):
        target_sum = s[i]
        value = find_by_sum(1, 1, n, target_sum)
        p[i] = value
        update(1, 1, n, value, 0)
    print(*p)
solve()
