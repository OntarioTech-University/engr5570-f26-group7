import heapq
from sys import stdin


def _read_input_tokens():
    import sys
    read_all = sys.stdin.read
    return read_all().split()


def _parse_input(data):
    idx = 0

    n = int(data[idx])
    idx += 1

    k = int(data[idx])
    idx += 1

    books = []
    for _ in range(n):
        t = int(data[idx])
        idx += 1

        a = int(data[idx])
        idx += 1

        b = int(data[idx])
        idx += 1

        books.append((t, a, b))

    return k, books


def _categorize_and_sort_book_times(books):
    ab = []
    a_only = []
    b_only = []

    for t, a, b in books:
        if a == 1 and b == 1:
            ab.append(t)
        elif a == 1 and b == 0:
            a_only.append(t)
        elif a == 0 and b == 1:
            b_only.append(t)

    ab.sort()
    a_only.sort()
    b_only.sort()

    return ab, a_only, b_only


def _make_prefix_sums(values):
    prefix = [0]
    total = 0

    for value in values:
        total += value
        prefix.append(total)

    return prefix


def _find_minimum_total_time(
    k,
    ab_count,
    a_only_count,
    b_only_count,
    ab_prefix,
    a_prefix,
    b_prefix,
):
    min_time = float('inf')

    for cnt_ab in range(ab_count + 1):
        needed = max(0, k - cnt_ab)

        if needed > a_only_count or needed > b_only_count:
            continue

        total_time = ab_prefix[cnt_ab] + a_prefix[needed] + b_prefix[needed]
        min_time = min(min_time, total_time)

    return min_time


def main():
    data = _read_input_tokens()
    k, books = _parse_input(data)

    ab, a_only, b_only = _categorize_and_sort_book_times(books)

    p_ab = _make_prefix_sums(ab)
    p_a = _make_prefix_sums(a_only)
    p_b = _make_prefix_sums(b_only)

    min_time = _find_minimum_total_time(
        k,
        len(ab),
        len(a_only),
        len(b_only),
        p_ab,
        p_a,
        p_b,
    )

    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)


if __name__ == "__main__":
    main()
