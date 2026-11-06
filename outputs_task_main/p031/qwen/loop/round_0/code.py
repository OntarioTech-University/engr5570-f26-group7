from collections import defaultdict, deque


def find_interesting_cities(n, edges):
    graph = _build_graph(edges)

    interesting_cities = []
    for city in range(1, n + 1):
        paths = _find_paths_to_other_cities(graph, city, n)
        if _has_one_path_to_every_other_city(paths, city, n):
            interesting_cities.append(city)

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


def _build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    return graph


def _find_paths_to_other_cities(graph, city, n):
    paths = defaultdict(set)
    for dest in range(1, n + 1):
        if city != dest:
            paths[dest] = find_simple_paths(graph, city, dest)
    return paths


def _has_one_path_to_every_other_city(paths, city, n):
    return all(len(paths[dest]) == 1 for dest in range(1, n + 1) if city != dest)


def _read_test_case_count():
    return int(input())


def _read_test_case():
    n, m = map(int, input().split())
    edges = _read_edges(m)
    return n, edges


def _read_edges(m):
    return [tuple(map(int, input().split())) for _ in range(m)]


def _print_result(result):
    print(' '.join(map(str, result)))


def main():
    t = _read_test_case_count()
    for _ in range(t):
        n, edges = _read_test_case()
        result = find_interesting_cities(n, edges)
        _print_result(result)


if __name__ == "__main__":
    main()
