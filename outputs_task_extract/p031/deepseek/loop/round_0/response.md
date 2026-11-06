```python
from collections import defaultdict, deque


def find_interesting_cities(n, edges):
    graph = _build_graph(edges)
    interesting_cities = _collect_interesting_cities(graph, n)
    return _apply_threshold(n, interesting_cities)


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


def _build_graph(edges):
    graph = defaultdict(list)
    for origin, destination in edges:
        graph[origin].append(destination)
    return graph


def _find_paths_by_destination(graph, source, city_count):
    paths_by_destination = defaultdict(set)
    for destination in range(1, city_count + 1):
        if destination != source:
            paths_by_destination[destination] = find_simple_paths(
                graph, source, destination
            )
    return paths_by_destination


def _all_destinations_have_single_path(paths_by_destination, source, city_count):
    return all(
        len(paths_by_destination[destination]) == 1
        for destination in range(1, city_count + 1)
        if destination != source
    )


def _is_interesting_city(graph, city, city_count):
    paths_by_destination = _find_paths_by_destination(graph, city, city_count)
    return _all_destinations_have_single_path(
        paths_by_destination, city, city_count
    )


def _collect_interesting_cities(graph, city_count):
    interesting_cities = []
    for city in range(1, city_count + 1):
        if _is_interesting_city(graph, city, city_count):
            interesting_cities.append(city)
    return interesting_cities


def _apply_threshold(city_count, interesting_cities):
    if len(interesting_cities) < 0.2 * city_count:
        return [-1]
    return interesting_cities


def _read_test_case_count():
    return int(input())


def _read_test_case():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    return n, edges


def _process_test_case(n, edges):
    return find_interesting_cities(n, edges)


def _print_result(result):
    print(' '.join(map(str, result)))


def _main():
    t = _read_test_case_count()
    for _ in range(t):
        n, edges = _read_test_case()
        result = _process_test_case(n, edges)
        _print_result(result)


_main()
```

- Extracted graph construction into `_build_graph`.
- Split the computation into `_find_paths_by_destination`, `_all_destinations_have_single_path`, `_is_interesting_city`, `_collect_interesting_cities`, and `_apply_threshold`.
- Moved input reading, test case processing, and output printing into `_read_test_case_count`, `_read_test_case`, `_process_test_case`, `_print_result`, and `_main`.
- Preserved the original public interfaces `find_interesting_cities` and `find_simple_paths` unchanged.
- Kept a top-level `_main()` call to preserve the original script execution behavior.