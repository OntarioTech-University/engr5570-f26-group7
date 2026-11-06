from collections import defaultdict, deque
import sys


def _read_input_data():
    import sys
    input = sys.stdin.read
    data = input().split()
    return data


def _read_int(data, idx):
    val = int(data[idx])
    idx += 1
    return val, idx


def _read_counts(data, idx):
    n, idx = _read_int(data, idx)
    m, idx = _read_int(data, idx)
    k, idx = _read_int(data, idx)
    q, idx = _read_int(data, idx)
    return n, m, k, q, idx


def _read_edges(data, idx, n, m):
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, idx = _read_int(data, idx)
        v, idx = _read_int(data, idx)
        w, idx = _read_int(data, idx)
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj, idx


def _read_queries(data, idx, q):
    queries = []
    for _ in range(q):
        a, idx = _read_int(data, idx)
        b, idx = _read_int(data, idx)
        queries.append((a, b))
    return queries, idx


def _build_central_set(k):
    return set(range(1, k + 1))


def _process_neighbors(node, energy, cap, adj, centrals, visited, queue):
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
        _process_neighbors(node, energy, cap, adj, centrals, visited, queue)
    return False


def _find_minimum_capacity(start, end, adj, centrals, high_limit):
    low = 0
    high = high_limit
    res = -1
    while low <= high:
        mid = (low + high) // 2
        if _can_do_mission(start, end, mid, adj, centrals):
            res = mid
            high = mid - 1
        else:
            low = mid + 1
    return res


def _solve_queries(queries, adj, centrals):
    results = []
    high_limit = 1 << 40
    for a, b in queries:
        results.append(_find_minimum_capacity(a, b, adj, centrals, high_limit))
    return results


def _print_results(results):
    print("\n".join(map(str, results)))


def main():
    data = _read_input_data()
    idx = 0
    n, m, k, q, idx = _read_counts(data, idx)
    adj, idx = _read_edges(data, idx, n, m)
    queries, idx = _read_queries(data, idx, q)
    centrals = _build_central_set(k)
    results = _solve_queries(queries, adj, centrals)
    _print_results(results)


if __name__ == "__main__":
    main()
