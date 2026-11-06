from collections import defaultdict, deque


def find_interesting_cities(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    interesting_cities = []
    for city in range(1, n + 1):
        paths = defaultdict(set)
        for dest in range(1, n + 1):
            if city != dest:
                paths[dest] = find_simple_paths(graph, city, dest)
        if all(len(paths[dest]) == 1 for dest in range(1, n + 1) if city != dest):
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


def read_test_count():
    return int(input())


def read_case():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    return n, edges


def print_result(result):
    print(' '.join(map(str, result)))


def main():
    t = read_test_count()
    for _ in range(t):
        n, edges = read_case()
        result = find_interesting_cities(n, edges)
        print_result(result)


if __name__ == "__main__":
    main()
