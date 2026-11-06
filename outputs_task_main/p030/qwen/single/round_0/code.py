from collections import defaultdict, deque
import sys


def _read_int(data, idx):
    val = int(data[idx])
    idx += 1
    return val, idx


def _read_edges(data, idx, node_count, edge_count):
    adj = [[] for _ in range(node_count + 1)]
    for _ in range(edge_count):
        u, idx = _read_int(data, idx)
        v, idx = _read_int(data, idx)
        w, idx = _read_int(data, idx)
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj, idx


def _read_queries(data, idx, query_count):
    queries = []
    for _ in range(query_count):
        a, idx = _read_int(data, idx)
        b, idx = _read_int(data, idx)
        queries.append((a, b))
    return queries, idx


def _read_input():
    data = sys.stdin.read().split()
    idx = 0

    n, idx = _read_int(data, idx)
    m, idx = _read_int(data, idx)
    k, idx = _read_int(data, idx)
    q, idx = _read_int(data, idx)

    adj, idx = _read_edges(data, idx, n, m)
    queries, idx = _read_queries(data, idx, q)

    return k, adj, queries


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


def _minimum_capacities(adj, centrals, queries):
    results = []

    INF = 1 << 40
    for a, b in queries:
        low = 0
        high = INF
        res = -1
        while low <= high:
            mid = (low + high) // 2
            if _can_do_mission(a, b, mid, adj, centrals):
                res = mid
                high = mid - 1
            else:
                low = mid + 1
        results.append(res)

    return results


def _solve(k, adj, queries):
    centrals = set(range(1, k + 1))
    return _minimum_capacities(adj, centrals, queries)


def _print_results(results):
    print("\n".join(map(str, results)))


def main():
    k, adj, queries = _read_input()
    results = _solve(k, adj, queries)
    _print_results(results)


if __name__ == "__main__":
    main()
