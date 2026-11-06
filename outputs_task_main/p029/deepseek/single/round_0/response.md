```python
from collections import deque
import sys


def read_input():
    """Read all input tokens from stdin."""
    return sys.stdin.read().split()


def parse_header(tokens):
    """Parse n, m, k from the beginning of the token list."""
    idx = 0
    n = int(tokens[idx])
    idx += 1
    m = int(tokens[idx])
    idx += 1
    k = int(tokens[idx])
    idx += 1
    return n, m, k, idx


def compute_results(tokens, n, m, k, start_idx):
    """Process edges and compute the maximum group size after each addition."""
    adj = [set() for _ in range(n + 1)]
    deg = [0] * (n + 1)
    results = []
    idx = start_idx

    for _ in range(m):
        u = int(tokens[idx])
        idx += 1
        v = int(tokens[idx])
        idx += 1

        if v not in adj[u]:
            adj[u].add(v)
            adj[v].add(u)
            deg[u] += 1
            deg[v] += 1

        count = _max_group_size(n, k, adj, deg)
        results.append(count)

    return results


def _max_group_size(n, k, adj, deg):
    """Return the number of vertices left after removing those with degree < k."""
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


def print_results(results):
    """Print each result on its own line."""
    print('\n'.join(map(str, results)))


def main():
    tokens = read_input()
    n, m, k, idx = parse_header(tokens)
    results = compute_results(tokens, n, m, k, idx)
    print_results(results)


if __name__ == "__main__":
    main()
```

- Moved `sys.stdin.read` from a top-level global assignment into the `read_input()` function to eliminate global variables and top-level logic.
- Extracted header parsing into `parse_header()` so input reading and initial parsing are separated.
- Moved edge processing and result calculation into `compute_results()`, preserving the original interleaved parsing/computation order by passing the token list and starting index.
- Extracted the degree-pruning group size calculation into the `_max_group_size()` helper, removing duplication and isolating the core algorithm.
- Added `print_results()` to separate output printing from computation.
- Updated `main()` to orchestrate the new functions, and kept the `if __name__ == "__main__":` guard.
- Removed the unused `defaultdict` import.