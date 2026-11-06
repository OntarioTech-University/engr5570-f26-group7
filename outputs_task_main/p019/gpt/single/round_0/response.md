```python
import heapq
from sys import stdin


def read_input():
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

    return k, books


def make_prefix(arr):
    res = [0]
    s = 0
    for x in arr:
        s += x
        res.append(s)
    return res


def compute_min_time(k, books):
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

    p_ab = make_prefix(ab)
    p_a = make_prefix(a_only)
    p_b = make_prefix(b_only)

    min_time = float('inf')
    max_ab = len(ab)

    for cnt_ab in range(max_ab + 1):
        needed = max(0, k - cnt_ab)

        if needed > len(a_only) or needed > len(b_only):
            continue

        total_time = p_ab[cnt_ab] + p_a[needed] + p_b[needed]
        min_time = min(min_time, total_time)

    return min_time


def print_output(min_time):
    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)


def main():
    k, books = read_input()
    min_time = compute_min_time(k, books)
    print_output(min_time)


if __name__ == "__main__":
    main()
```

- Separated input, computation, and output into functions, with `main()` passing data between them.
- Moved the prefix-sum helper out of `main()` so the computation can reuse it without a nested definition.
- Calculated the identical Alice and Bob requirement once per iteration, removing duplicated code without changing the result.