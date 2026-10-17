```python
from collections import defaultdict, deque
import sys


def _build_graph(read_int, node_count, edge_count):
    adj = [[] for _ in range(node_count + 1)]
    for _ in range(edge_count):
        u = read_int()
        v = read_int()
        w = read_int()
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def _read_queries(read_int, query_count):
    queries = []
    for _ in range(query_count):
        a = read_int()
        b = read_int()
        queries.append((a, b))
    return queries


def _can_do_mission(adj, centrals, start, end, capacity):
    visited = {start: capacity}
    queue = deque([(start, capacity)])

    while queue:
        node, energy = queue.popleft()
        if node == end:
            return True

        for neighbor, weight in adj[node]:
            if weight > energy:
                continue

            new_energy = energy - weight
            if neighbor in centrals:
                new_energy = capacity

            if neighbor not in visited or visited[neighbor] < new_energy:
                visited[neighbor] = new_energy
                queue.append((neighbor, new_energy))

    return False


def _minimum_capacity(adj, centrals, start, end):
    low = 0
    high = 1 << 40
    answer = -1

    while low <= high:
        mid = (low + high) // 2
        if _can_do_mission(adj, centrals, start, end, mid):
            answer = mid
            high = mid - 1
        else:
            low = mid + 1

    return answer


def main():
    import sys
    read_stdin = sys.stdin.read
    data = read_stdin().split()

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

    adj = _build_graph(read_int, n, m)
    queries = _read_queries(read_int, q)
    centrals = set(range(1, k + 1))

    results = []
    for a, b in queries:
        results.append(_minimum_capacity(adj, centrals, a, b))

    print("\n".join(map(str, results)))


if __name__ == "__main__":
    main()
```

- Extracted graph construction into `_build_graph` to separate edge parsing/adjacency building from `main`.
- Extracted query parsing into `_read_queries` so input handling is divided into smaller, focused steps.
- Moved the BFS feasibility check into `_can_do_mission` with explicit parameters, reducing closure coupling and making the logic easier to read.
- Extracted the per-query binary search into `_minimum_capacity`, simplifying the main query-processing loop.
- Kept `main`’s public signature, input reading behavior, algorithmic steps, output printing, and exception behavior unchanged.