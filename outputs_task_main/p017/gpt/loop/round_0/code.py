import sys


def read_input(input_line):
    n_str = input_line()
    if not n_str:
        return None

    n = int(n_str)
    a = list(map(int, input_line().split()))
    m = int(input_line())
    return n, a, m


def compute_answers(n, a, m, input_line):
    indexed_a = []
    for i in range(n):
        indexed_a.append((a[i], i))

    indexed_a.sort(key=lambda x: (-x[0], x[1]))
    return _iter_answers(indexed_a, m, input_line)


def _iter_answers(indexed_a, m, input_line):
    optimal_subs_cache = {}

    for _ in range(m):
        k, pos = map(int, input_line().split())

        if k not in optimal_subs_cache:
            top_k_pairs = indexed_a[:k]
            top_k_pairs.sort(key=lambda x: x[1])
            optimal_subs_cache[k] = [pair[0] for pair in top_k_pairs]

        yield optimal_subs_cache[k][pos - 1]


def write_output(answers):
    for result in answers:
        sys.stdout.write(str(result) + '\n')


def solve():
    try:
        input_line = sys.stdin.readline
        data = read_input(input_line)
        if data is None:
            return

        answers = compute_answers(*data, input_line)
        write_output(answers)
    except (IOError, ValueError):
        pass


def main():
    solve()


if __name__ == "__main__":
    main()
