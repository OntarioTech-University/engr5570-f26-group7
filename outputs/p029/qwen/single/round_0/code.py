from collections import deque, defaultdict
import sys
input = sys.stdin.read


def main():
    data = input().split()
    idx = 0

    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1

    adj = [set() for _ in range(n + 1)]
    deg = [0] * (n + 1)

    results = []

    for _ in range(m):
        u = int(data[idx])
        idx += 1
        v = int(data[idx])
        idx += 1

        _add_undirected_edge(adj, deg, u, v)
        results.append(_count_remaining_nodes(n, adj, deg, k))

    print('\n'.join(map(str, results)))


def _add_undirected_edge(adj, deg, u, v):
    if v not in adj[u]:
        adj[u].add(v)
        adj[v].add(u)
        deg[u] += 1
        deg[v] += 1


def _count_remaining_nodes(n, adj, deg, k):
    cur_deg = deg[:]
    queue = _initial_low_degree_queue(n, cur_deg, k)
    removed = [False] * (n + 1)

    _prune_low_degree_nodes(adj, cur_deg, removed, queue, k)

    return sum(1 for node in range(1, n + 1) if not removed[node])


def _initial_low_degree_queue(n, cur_deg, k):
    queue = deque()
    for node in range(1, n + 1):
        if cur_deg[node] < k:
            queue.append(node)
    return queue


def _prune_low_degree_nodes(adj, cur_deg, removed, queue, k):
    while queue:
        node = queue.popleft()
        if removed[node]:
            continue

        removed[node] = True

        for neighbor in adj[node]:
            if not removed[neighbor]:
                cur_deg[neighbor] -= 1
                if cur_deg[neighbor] < k:
                    queue.append(neighbor)


if __name__ == "__main__":
    main()
