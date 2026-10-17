from collections import defaultdict, deque


def find_interesting_cities(n, edges):
    graph = build_graph(edges)
    interesting_cities = [
        city for city in range(1, n + 1)
        if has_unique_paths_to_all_others(graph, city, n)
    ]

    if len(interesting_cities) < 0.2 * n:
        return [-1]
    return interesting_cities


def build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    return graph


def has_unique_paths_to_all_others(graph, city, n):
    return all(
        len(find_simple_paths(graph, city, dest)) == 1
        for dest in range(1, n + 1)
        if city != dest
    )


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


t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    result = find_interesting_cities(n, edges)
    print(' '.join(map(str, result)))
