import sys


def _read_input():
    data = sys.stdin.read().split()
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

    return n, k, books


def _categorize_books(books):
    ab = []
    a_only = []
    b_only = []
    none = []

    for t, a, b in books:
        if a == 1 and b == 1:
            ab.append(t)
        elif a == 1 and b == 0:
            a_only.append(t)
        elif a == 0 and b == 1:
            b_only.append(t)
        else:
            none.append(t)

    return ab, a_only, b_only, none


def _prefix_sums(arr):
    res = [0]
    s = 0
    for x in arr:
        s += x
        res.append(s)
    return res


def _compute_min_time(k, books):
    ab, a_only, b_only, _ = _categorize_books(books)

    ab.sort()
    a_only.sort()
    b_only.sort()

    p_ab = _prefix_sums(ab)
    p_a = _prefix_sums(a_only)
    p_b = _prefix_sums(b_only)

    min_time = float('inf')

    for cnt_ab in range(len(ab) + 1):
        needed = max(0, k - cnt_ab)

        if needed > len(a_only) or needed > len(b_only):
            continue

        total_time = p_ab[cnt_ab] + p_a[needed] + p_b[needed]
        min_time = min(min_time, total_time)

    return min_time


def _print_result(min_time):
    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)


def main():
    _, k, books = _read_input()
    min_time = _compute_min_time(k, books)
    _print_result(min_time)


if __name__ == "__main__":
    main()
