from collections import defaultdict, deque
import sys


def _make_reader(data):
    idx = 0

    def read_int():
        nonlocal idx
        val = int(data[idx])
        idx += 1
        return val

    return read_int


def _read_edges(read_int, n, m):
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = read_int()
        v = read_int()
        w = read_int()
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def _read_queries(read_int, q):
    queries = []
    for _ in range(q):
        a = read_int()
        b = read_int()
        queries.append((a, b))
    return queries


def _read_input():
    read_int = _make_reader(sys.stdin.read().split())
    n = read_int()
    m = read_int()
    k = read_int()
    q = read_int()
    adj = _read_edges(read_int, n, m)
    queries = _read_queries(read_int, q)
    centrals = set(range(1, k + 1))
    return adj, queries, centrals


def _explore_neighbors(node, energy, cap, adj, centrals, visited, queue):
    for nei, weight in adj[node]:
        if weight > energy:
            continue
        new_energy = energy - weight
        if nei in centrals:
            new_energy = cap
        if nei not in visited or visited[nei] < new_energy:
            visited[nei] = new_energy
            queue.append((nei, new_energy))


def _can_do_mission(start, end, cap, adj, centrals):
    visited = {}
    queue = deque()
    queue.append((start, cap))
    visited[start] = cap

    while queue:
        node, energy = queue.popleft()
        if node == end:
            return True
        _explore_neighbors(node, energy, cap, adj, centrals, visited, queue)
    return False


def _find_capacity(a, b, adj, centrals):
    low = 0
    high = 1 << 40
    res = -1
    while low <= high:
        mid = (low + high) // 2
        if _can_do_mission(a, b, mid, adj, centrals):
            res = mid
            high = mid - 1
        else:
            low = mid + 1
    return res


def _compute_results(adj, queries, centrals):
    results = []
    for a, b in queries:
        results.append(_find_capacity(a, b, adj, centrals))
    return results


def _print_results(results):
    print("\n".join(map(str, results)))


def main():
    adj, queries, centrals = _read_input()
    results = _compute_results(adj, queries, centrals)
    _print_results(results)


if __name__ == "__main__":
    main()
