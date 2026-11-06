Here's the refactored code with structural improvements:

```python
from collections import defaultdict, deque
import sys


def read_input():
    """Read and parse all input data from stdin."""
    data = sys.stdin.read().split()
    
    idx = 0
    def read_int():
        nonlocal idx
        val = int(data[idx])
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


def can_do_mission(adj, centrals, start, end, cap):
    """Check if a mission can be completed with given capacity."""
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


def find_min_capacity(adj, centrals, start, end):
    """Binary search for minimum capacity needed for a mission."""
    INF = 1 << 40
    low = 0
    high = INF
    res = -1
    
    while low <= high:
        mid = (low + high) // 2
        if can_do_mission(adj, centrals, start, end, mid):
            res = mid
            high = mid - 1
        else:
            low = mid + 1
    
    return res


def compute_results(n, k, adj, queries):
    """Compute minimum capacity for all queries."""
    centrals = set(range(1, k + 1))
    results = []
    
    for a, b in queries:
        result = find_min_capacity(adj, centrals, a, b)
        results.append(result)
    
    return results


def print_results(results):
    """Print results to stdout."""
    print("\n".join(map(str, results)))


def main():
    n, k, adj, queries = read_input()
    results = compute_results(n, k, adj, queries)
    print_results(results)


if __name__ == "__main__":
    main()
```

**Changes made:**

- **Removed top-level logic**: All code now resides within functions, with only the `if __name__ == "__main__":` guard at the top level
- **Eliminated global variables**: All data is passed between functions through parameters and return values
- **Separated concerns into functions**:
  - `read_input()`: Handles all input parsing and returns structured data
  - `compute_results()`: Orchestrates the main computation
  - `print_results()`: Handles output formatting and printing
- **Extracted helper functions**:
  - `can_do_mission()`: Moved from nested function to module-level function
  - `find_min_capacity()`: Extracted binary search logic from the main loop
- **Removed duplicate code**: The `import sys` statement was duplicated inside `main()` and removed
- **Improved parameter passing**: Functions receive only the data they need rather than relying on closure variables