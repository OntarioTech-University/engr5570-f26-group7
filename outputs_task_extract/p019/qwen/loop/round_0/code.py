import heapq
from sys import stdin


def read_input_data():
    import sys
    input = sys.stdin.read
    return input().split()


def parse_counts(data):
    idx = 0
    n = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    return n, k, idx


def parse_books(data, n, idx):
    books = []
    for _ in range(n):
        t = int(data[idx])
        idx += 1
        a = int(data[idx])
        idx += 1
        b = int(data[idx])
        idx += 1
        books.append((t, a, b))
    return books


def separate_books(books):
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


def sort_categories(ab, a_only, b_only):
    ab.sort()
    a_only.sort()
    b_only.sort()


def make_prefix(arr):
    res = [0]
    s = 0
    for x in arr:
        s += x
        res.append(s)
    return res


def build_prefix_sums(ab, a_only, b_only):
    p_ab = make_prefix(ab)
    p_a = make_prefix(a_only)
    p_b = make_prefix(b_only)
    return p_ab, p_a, p_b


def compute_min_time(ab, a_only, b_only, p_ab, p_a, p_b, k):
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


def print_result(min_time):
    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)


def main():
    data = read_input_data()
    n, k, idx = parse_counts(data)
    books = parse_books(data, n, idx)
    ab, a_only, b_only, none = separate_books(books)
    sort_categories(ab, a_only, b_only)
    p_ab, p_a, p_b = build_prefix_sums(ab, a_only, b_only)
    min_time = compute_min_time(ab, a_only, b_only, p_ab, p_a, p_b, k)
    print_result(min_time)


if __name__ == "__main__":
    main()
