from collections import deque, defaultdict
import sys
input = sys.stdin.read


def read_tokens():
    return input().split()


def read_header(data, idx):
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    return n, m, k, idx


def initialize_graph(n):
    adj = [set() for _ in range(n + 1)]
    deg = [0] * (n + 1)
    return adj, deg


def read_edge(data, idx):
    u = int(data[idx])
    idx += 1
    v = int(data[idx])
    idx += 1
    return u, v, idx


def add_edge(adj, deg, u, v):
    if v not in adj[u]:
        adj[u].add(v)
        adj[v].add(u)
        deg[u] += 1
        deg[v] += 1


def initial_low_degree_queue(cur_deg, n, k):
    queue = deque()
    for i in range(1, n + 1):
        if cur_deg[i] < k:
            queue.append(i)
    return queue


def remove_low_degree_nodes(adj, cur_deg, queue, removed, k):
    while queue:
        node = queue.popleft()
        if removed[node]:
            continue
        removed[node] = True
        for nei in adj[node]:
            if not removed[nei]:
                cur_deg[nei] -= 1
                if cur_deg[nei] < k:
                    queue.append(nei)


def count_not_removed(removed, n):
    return sum(1 for i in range(1, n + 1) if not removed[i])


def compute_remaining_count(adj, deg, n, k):
    cur_deg = deg[:]
    queue = initial_low_degree_queue(cur_deg, n, k)
    removed = [False] * (n + 1)
    remove_low_degree_nodes(adj, cur_deg, queue, removed, k)
    return count_not_removed(removed, n)


def process_edges(data, idx, m, n, k, adj, deg):
    results = []
    for _ in range(m):
        u, v, idx = read_edge(data, idx)
        add_edge(adj, deg, u, v)
        results.append(compute_remaining_count(adj, deg, n, k))
    return results


def print_results(results):
    print('\n'.join(map(str, results)))


def main():
    data = read_tokens()
    idx = 0
    n, m, k, idx = read_header(data, idx)
    adj, deg = initialize_graph(n)
    results = process_edges(data, idx, m, n, k, adj, deg)
    print_results(results)


if __name__ == "__main__":
    main()
