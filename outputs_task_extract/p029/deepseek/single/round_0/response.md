Here's the refactored code with improved structure and maintainability:

```python
from collections import deque, defaultdict
import sys

input = sys.stdin.read

def read_input_data():
    """Read and parse the input data."""
    data = input().split()
    idx = 0
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    return data, idx, n, m, k

def initialize_graph(n):
    """Initialize adjacency list and degree arrays."""
    adj = [set() for _ in range(n + 1)]
    deg = [0] * (n + 1)
    return adj, deg

def add_edge(adj, deg, u, v):
    """Add an edge to the graph if it doesn't already exist."""
    if v not in adj[u]:
        adj[u].add(v)
        adj[v].add(u)
        deg[u] += 1
        deg[v] += 1

def calculate_max_group_size(adj, deg, n, k):
    """Calculate the maximum group size satisfying the degree condition."""
    cur_deg = deg[:]
    queue = deque()
    
    # Enqueue all nodes with degree < k
    for i in range(1, n + 1):
        if cur_deg[i] < k:
            queue.append(i)
    
    removed = [False] * (n + 1)
    remove_nodes_with_low_degree(adj, cur_deg, queue, removed, k)
    
    return count_remaining_nodes(removed, n)

def remove_nodes_with_low_degree(adj, cur_deg, queue, removed, k):
    """Remove nodes with degree < k and update neighbors."""
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

def count_remaining_nodes(removed, n):
    """Count nodes that haven't been removed."""
    return sum(1 for i in range(1, n + 1) if not removed[i])

def process_edges(data, idx, adj, deg, n, m, k):
    """Process all edges and calculate results."""
    results = []
    for _ in range(m):
        u = int(data[idx])
        idx += 1
        v = int(data[idx])
        idx += 1
        
        add_edge(adj, deg, u, v)
        count = calculate_max_group_size(adj, deg, n, k)
        results.append(count)
    
    return results

def print_results(results):
    """Print the results."""
    print('\n'.join(map(str, results)))

def main():
    data, idx, n, m, k = read_input_data()
    adj, deg = initialize_graph(n)
    results = process_edges(data, idx, adj, deg, n, m, k)
    print_results(results)

if __name__ == "__main__":
    main()
```

**Summary of changes:**

- **Split input reading into `read_input_data()`**: Separates parsing logic from the main flow, making it easier to understand and test.
- **Created `initialize_graph()`**: Encapsulates graph data structure initialization.
- **Created `add_edge()`**: Isolates edge addition logic with duplicate checking.
- **Created `calculate_max_group_size()`**: Extracts the core computation for each edge addition.
- **Created `remove_nodes_with_low_degree()`**: Separates the BFS-based node removal algorithm.
- **Created `count_remaining_nodes()`**: Isolates the counting logic for remaining nodes.
- **Created `process_edges()`**: Manages the loop over edges and collects results.
- **Created `print_results()`**: Handles output formatting and printing.
- **Simplified `main()`**: Now serves as a clear orchestrator, calling each function in sequence.
- **Added docstrings**: Each function has a clear description of its purpose.
- **Preserved all behavior**: No logic changes, error handling modifications, or interface changes were made.