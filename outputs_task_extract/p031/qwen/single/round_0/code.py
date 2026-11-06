from collections import defaultdict, deque


def find_interesting_cities(n, edges):
    graph = build_graph(edges)
    interesting_cities = collect_interesting_cities(graph, n)
    return select_final_result(interesting_cities, n)


def build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    return graph


def collect_interesting_cities(graph, n):
    interesting_cities = []
    for city in range(1, n + 1):
        if is_interesting_city(graph, city, n):
            interesting_cities.append(city)
    return interesting_cities


def is_interesting_city(graph, city, n):
    paths = find_paths_to_all_destinations(graph, city, n)
    return has_unique_path_to_each_destination(paths, city, n)


def find_paths_to_all_destinations(graph, city, n):
    paths = defaultdict(set)
    for dest in range(1, n + 1):
        if city != dest:
            paths[dest] = find_simple_paths(graph, city, dest)
    return paths


def has_unique_path_to_each_destination(paths, city, n):
    return all(
        len(paths[dest]) == 1
        for dest in range(1, n + 1)
        if city != dest
    )


def select_final_result(interesting_cities, n):
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


def read_test_count():
    return int(input())


def read_test_case():
    n, m = map(int, input().split())
    edges = read_edges(m)
    return n, edges


def read_edges(m):
    return [
        tuple(map(int, input().split()))
        for _ in range(m)
    ]


def print_result(result):
    print(' '.join(map(str, result)))


def main():
    t = read_test_count()
    for _ in range(t):
        n, edges = read_test_case()
        result = find_interesting_cities(n, edges)
        print_result(result)


main()
