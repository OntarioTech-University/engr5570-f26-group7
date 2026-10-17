from collections import deque, defaultdict
import sys

input = sys.stdin.read


def read_graph_parameters(data, idx):
    """Read n, m, k from input data."""
    n = int(data[idx])
    m = int(data[idx + 1])
    k = int(data[idx + 2])
    return n, m, k, idx + 3


def initialize_graph(n):
    """Initialize adjacency list and degree array."""
    adj = [set() for _ in range(n + 1)]
    deg = [0] * (n + 1)
    return adj, deg


def add_edge(adj, deg, u, v):
    """Add an undirected edge between u and v if not already present."""
    if v not in adj[u]:
        adj[u].add(v)
        adj[v].add(u)
        deg[u] += 1
        deg[v] += 1


def find_nodes_below_threshold(deg, k, n):
    """Find all nodes with degree below k."""
    return [i for i in range(1, n + 1) if deg[i] < k]


def remove_nodes_below_threshold(adj, cur_deg, k, n):
    """Remove nodes with degree < k and return count of remaining nodes."""
    queue = deque(find_nodes_below_threshold(cur_deg, k, n))
    removed = [False] * (n + 1)
    
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
    
    return sum(1 for i in range(1, n + 1) if not removed[i])


def calculate_max_group_size(adj, deg, k, n):
    """Calculate max group size satisfying the degree condition."""
    cur_deg = deg[:]
    return remove_nodes_below_threshold(adj, cur_deg, k, n)


def main():
    data = input().split()
    idx = 0
    
    n, m, k, idx = read_graph_parameters(data, idx)
    adj, deg = initialize_graph(n)
    results = []
    
    for _ in range(m):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        
        add_edge(adj, deg, u, v)
        count = calculate_max_group_size(adj, deg, k, n)
        results.append(count)
    
    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
