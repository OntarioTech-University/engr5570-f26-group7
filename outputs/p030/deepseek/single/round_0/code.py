from collections import defaultdict, deque
import sys


def read_input():
    """Read all input data and return parsed values."""
    input_data = sys.stdin.read().split()
    idx = 0

    def read_int():
        nonlocal idx
        val = int(input_data[idx])
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

    return n, k, adj, queries


def can_complete_mission(start, end, capacity, adj, centrals):
    """Check if a mission can be completed with the given capacity."""
    visited = {}  # node -> max_energy_when_visited
    queue = deque([(start, capacity)])
    visited[start] = capacity

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


def find_minimum_capacity(start, end, adj, centrals):
    """Binary search for the minimum capacity needed to complete a mission."""
    INF = 1 << 40
    low = 0
    high = INF
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if can_complete_mission(start, end, mid, adj, centrals):
            result = mid
            high = mid - 1
        else:
            low = mid + 1

    return result


def main():
    n, k, adj, queries = read_input()
    centrals = set(range(1, k + 1))

    results = [
        find_minimum_capacity(a, b, adj, centrals)
        for a, b in queries
    ]

    print("\n".join(map(str, results)))


if __name__ == "__main__":
    main()
