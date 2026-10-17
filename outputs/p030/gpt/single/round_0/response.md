```python
from collections import defaultdict, deque
import sys


def _read_graph(n, m, read_int):
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = read_int()
        v = read_int()
        w = read_int()
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def _read_queries(q, read_int):
    queries = []
    for _ in range(q):
        a = read_int()
        b = read_int()
        queries.append((a, b))
    return queries


def _can_do_mission(start, end, cap, adj, centrals):
    visited = {}  # node -> max_energy_when_visited
    queue = deque()
    queue.append((start, cap))  # node, energy
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


def _minimum_capacity(start, end, adj, centrals, upper_bound):
    low = 0
    high = upper_bound
    res = -1

    while low <= high:
        mid = (low + high) // 2
        if _can_do_mission(start, end, mid, adj, centrals):
            res = mid
            high = mid - 1
        else:
            low = mid + 1

    return res


def main():
    import sys
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

    adj = _read_graph(n, m, read_int)
    queries = _read_queries(q, read_int)
    centrals = set(range(1, k + 1))

    results = []
    INF = 1 << 40
    for a, b in queries:
        results.append(_minimum_capacity(a, b, adj, centrals, INF))

    print("\n".join(map(str, results)))


if __name__ == "__main__":
    main()
```

- Separated graph and query parsing so `main()` shows the overall sequence more clearly.
- Moved mission feasibility and capacity search into named helpers, reducing nesting while retaining their algorithms and iteration order.