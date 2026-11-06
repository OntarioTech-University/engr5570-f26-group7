import sys
from collections import deque


def _read_tokens():
    return sys.stdin.read().split()


def _make_int_reader(tokens):
    index = 0

    def read_int():
        nonlocal index
        value = int(tokens[index])
        index += 1
        return value

    return read_int


def _parse_graph(reader):
    n = reader()
    m = reader()
    k = reader()
    q = reader()

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = reader()
        v = reader()
        w = reader()
        adj[u].append((v, w))
        adj[v].append((u, w))

    return k, q, adj


def _parse_queries(reader, q):
    queries = []
    for _ in range(q):
        a = reader()
        b = reader()
        queries.append((a, b))
    return queries


def _build_centrals(k):
    return set(range(1, k + 1))


def _can_reach(adj, centrals, start, end, cap):
    queue = deque([(start, cap)])
    best_energy = {start: cap}
    while queue:
        node, energy = queue.popleft()
        if node == end:
            return True
        for neighbor, weight in adj[node]:
            if weight > energy:
                continue
            new_energy = cap if neighbor in centrals else energy - weight
            if neighbor not in best_energy or best_energy[neighbor] < new_energy:
                best_energy[neighbor] = new_energy
                queue.append((neighbor, new_energy))
    return False


def _minimum_capacity(adj, centrals, start, end):
    max_capacity = 1 << 40
    low = 0
    high = max_capacity
    best = -1

    while low <= high:
        mid = (low + high) // 2
        if _can_reach(adj, centrals, start, end, mid):
            best = mid
            high = mid - 1
        else:
            low = mid + 1

    return best


def _compute_results(adj, centrals, queries):
    results = []
    for start, end in queries:
        result = _minimum_capacity(adj, centrals, start, end)
        results.append(result)
    return results


def _print_results(results):
    print("\n".join(map(str, results)))


def main():
    tokens = _read_tokens()
    reader = _make_int_reader(tokens)
    k, q, adj = _parse_graph(reader)
    queries = _parse_queries(reader, q)
    centrals = _build_centrals(k)
    results = _compute_results(adj, centrals, queries)
    _print_results(results)


if __name__ == "__main__":
    main()
