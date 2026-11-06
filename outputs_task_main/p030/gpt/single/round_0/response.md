```python
from collections import defaultdict, deque
import sys


def read_input():
    input = sys.stdin.read
    data = input().split()

    idx = 0

    def read_int():
        nonlocal idx
        val = int(data[idx])
        idx += 1
        return val

    n = read_int()
    m = read_int()
    k = read_int()
    q = read_int()

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = read_int()
        v = read_int()
        w = read_int()
        adj[u].append((v, w))
        adj[v].append((u, w))

    queries = []
    for _ in range(q):
        a = read_int()
        b = read_int()
        queries.append((a, b))

    return k, adj, queries


def can_do_mission(start, end, cap, adj, centrals):
    visited = {}
    queue = deque()
    queue.append((start, cap))
    visited[start] = cap

    while queue:
        node, energy = queue.popleft()
        if node == end:
            return True
        for nei, weight in adj[node]:
            if weight > energy:
                continue
            new_energy = energy - weight
            if nei in centrals:
                new_energy = cap
            if nei not in visited or visited[nei] < new_energy:
                visited[nei] = new_energy
                queue.append((nei, new_energy))
    return False


def compute_results(k, adj, queries):
    centrals = set(range(1, k + 1))
    results = []

    INF = 1 << 40
    for a, b in queries:
        low = 0
        high = INF
        res = -1
        while low <= high:
            mid = (low + high) // 2
            if can_do_mission(a, b, mid, adj, centrals):
                res = mid
                high = mid - 1
            else:
                low = mid + 1
        results.append(res)

    return results


def print_results(results):
    print("\n".join(map(str, results)))


def main():
    k, adj, queries = read_input()
    results = compute_results(k, adj, queries)
    print_results(results)


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and output printing into named functions, with data passed through parameters and return values.
- Moved the mission check into a shared helper instead of nesting it inside `main()`.
- Kept `main()` as the guarded entry point and left the input, search, and printing behavior unchanged.