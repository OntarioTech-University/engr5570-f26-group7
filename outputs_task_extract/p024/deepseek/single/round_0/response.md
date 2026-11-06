```python
import sys
input = sys.stdin.read

class BIT:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (size + 1)

    def update(self, idx, delta):
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & (-idx)
        return res


def read_input():
    return input().split()


def read_int(data, idx):
    value = int(data[idx[0]])
    idx[0] += 1
    return value


def parse_initial_params(data, idx):
    n = read_int(data, idx)
    k = read_int(data, idx)
    a = read_int(data, idx)
    b = read_int(data, idx)
    q = read_int(data, idx)
    return n, k, a, b, q


def handle_order_update(data, idx, orders, bit_pre, bit_suf, a, b):
    d = read_int(data, idx)
    x = read_int(data, idx)
    old_b_val = min(orders[d], b)
    old_a_val = min(orders[d], a)
    orders[d] += x
    new_b_val = min(orders[d], b)
    new_a_val = min(orders[d], a)
    bit_pre.update(d, new_b_val - old_b_val)
    bit_suf.update(d, new_a_val - old_a_val)


def handle_query(data, idx, bit_pre, bit_suf, n, k):
    p = read_int(data, idx)
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    return pre_sum + suf_sum


def process_queries(data, idx, n, k, a, b, q, orders, bit_pre, bit_suf):
    results = []
    for _ in range(q):
        t = read_int(data, idx)
        if t == 1:
            handle_order_update(data, idx, orders, bit_pre, bit_suf, a, b)
        else:
            results.append(handle_query(data, idx, bit_pre, bit_suf, n, k))
    return results


def print_results(results):
    print('\n'.join(map(str, results)))


def main():
    data = read_input()
    idx = [0]
    n, k, a, b, q = parse_initial_params(data, idx)
    orders = [0] * (n + 1)
    bit_pre = BIT(n)
    bit_suf = BIT(n)
    results = process_queries(data, idx, n, k, a, b, q, orders, bit_pre, bit_suf)
    print_results(results)


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_input` and `read_int` helpers, preserving the original `sys.stdin.read` alias.
- Extracted initial parameter parsing into `parse_initial_params`.
- Extracted order update logic into `handle_order_update`.
- Extracted query handling into `handle_query`.
- Extracted the main query loop into `process_queries`.
- Extracted output printing into `print_results`.
- `main` now orchestrates the steps while keeping the `BIT` class and all public signatures unchanged.