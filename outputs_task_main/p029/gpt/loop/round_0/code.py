from collections import deque, defaultdict
import sys


def read_input():
    return sys.stdin.read().split()


def count_eligible_nodes(n, k, adj, deg):
    cur_deg = deg[:]
    queue = deque()

    for i in range(1, n + 1):
        if cur_deg[i] < k:
            queue.append(i)

    removed = [False] * (n + 1)
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

    return sum(1 for i in range(1, n + 1) if not removed[i])


def compute_results(data):
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

        if v not in adj[u]:
            adj[u].add(v)
            adj[v].add(u)
            deg[u] += 1
            deg[v] += 1

        results.append(count_eligible_nodes(n, k, adj, deg))

    return results


def print_results(results):
    print('\n'.join(map(str, results)))


def main():
    data = read_input()
    results = compute_results(data)
    print_results(results)


if __name__ == "__main__":
    main()
