import heapq
from sys import stdin


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

    ab.sort()
    a_only.sort()
    b_only.sort()
    return ab, a_only, b_only


def _make_prefix(arr):
    res = [0]
    s = 0
    for x in arr:
        s += x
        res.append(s)
    return res


def _minimum_time(ab, a_only, b_only, k):
    p_ab = _make_prefix(ab)
    p_a = _make_prefix(a_only)
    p_b = _make_prefix(b_only)

    min_time = float('inf')
    max_ab = len(ab)

    for cnt_ab in range(max_ab + 1):
        alice_needed = max(0, k - cnt_ab)
        bob_needed = max(0, k - cnt_ab)

        if alice_needed > len(a_only) or bob_needed > len(b_only):
            continue

        total_time = p_ab[cnt_ab] + p_a[alice_needed] + p_b[bob_needed]
        min_time = min(min_time, total_time)

    return min_time


def main():
    import sys
    input = sys.stdin.read
    data = input().split()

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

    ab, a_only, b_only = _categorize_books(books)
    min_time = _minimum_time(ab, a_only, b_only, k)

    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)


if __name__ == "__main__":
    main()
