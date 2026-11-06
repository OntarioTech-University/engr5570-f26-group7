```python
from collections import defaultdict, deque


def _build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    return graph


def _paths_from_city(graph, city, n):
    paths = defaultdict(set)
    for dest in range(1, n + 1):
        if city != dest:
            paths[dest] = find_simple_paths(graph, city, dest)
    return paths


def _has_one_path_to_each_destination(paths, city, n):
    return all(
        len(paths[dest]) == 1
        for dest in range(1, n + 1)
        if city != dest
    )


def _collect_interesting_cities(graph, n):
    interesting_cities = []
    for city in range(1, n + 1):
        paths = _paths_from_city(graph, city, n)
        if _has_one_path_to_each_destination(paths, city, n):
            interesting_cities.append(city)
    return interesting_cities


def find_interesting_cities(n, edges):
    graph = _build_graph(edges)
    interesting_cities = _collect_interesting_cities(graph, n)
    if len(interesting_cities) < 0.2 * n:
        return [-1]
    return interesting_cities


def find_simple_paths(graph, source, dest):
    queue = deque([(source, [source])])
    paths = set()
    while queue:
        city, path = queue.popleft()
        if city == dest:
            paths.add(tuple(path))
        else:
            for neighbor in graph[city]:
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))
    return paths


def _read_test_count():
    return int(input())


def _read_case():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    return n, edges


def _print_result(result):
    print(' '.join(map(str, result)))


def _main():
    t = _read_test_count()
    for _ in range(t):
        n, edges = _read_case()
        result = find_interesting_cities(n, edges)
        _print_result(result)


_main()
```

- Split graph construction, path collection, and city qualification into small functions while keeping the public function signatures unchanged.
- Moved input reading and output printing into dedicated functions. `_main()` is still called unconditionally, preserving execution when the file is run or imported.