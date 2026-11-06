import heapq
from sys import stdin

def _read_input():
    import sys
    return sys.stdin.read().split()

def _parse_int(data, idx):
    return int(data[idx]), idx + 1

def _parse_books(data):
    n, idx = _parse_int(data, 0)
    k, idx = _parse_int(data, idx)
    books = []
    for _ in range(n):
        t, idx = _parse_int(data, idx)
        a, idx = _parse_int(data, idx)
        b, idx = _parse_int(data, idx)
        books.append((t, a, b))
    return k, books

def _classify_books(books):
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
    return ab, a_only, b_only

def _make_prefix(arr):
    res = [0]
    total = 0
    for value in arr:
        total += value
        res.append(total)
    return res

def _prepare_prefixes(ab, a_only, b_only):
    p_ab = _make_prefix(ab)
    p_a = _make_prefix(a_only)
    p_b = _make_prefix(b_only)
    return p_ab, p_a, p_b

def _compute_min_time(k, ab, a_only, b_only):
    ab.sort()
    a_only.sort()
    b_only.sort()
    p_ab, p_a, p_b = _prepare_prefixes(ab, a_only, b_only)
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
    data = _read_input()
    k, books = _parse_books(data)
    ab, a_only, b_only = _classify_books(books)
    min_time = _compute_min_time(k, ab, a_only, b_only)
    _print_result(min_time)

if __name__ == "__main__":
    main()
