```python
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


import sys
input = sys.stdin.read


def _read_header(data):
    idx = 0

    n = int(data[idx])
    idx += 1

    k = int(data[idx])
    idx += 1

    a = int(data[idx])
    idx += 1

    b = int(data[idx])
    idx += 1

    q = int(data[idx])
    idx += 1

    return n, k, a, b, q, idx


def _apply_order_increase(bit_pre, bit_suf, orders, d, x, pre_limit, suf_limit):
    old_pre_val = min(orders[d], pre_limit)
    old_suf_val = min(orders[d], suf_limit)

    orders[d] += x

    new_pre_val = min(orders[d], pre_limit)
    new_suf_val = min(orders[d], suf_limit)

    bit_pre.update(d, new_pre_val - old_pre_val)
    bit_suf.update(d, new_suf_val - old_suf_val)


def _maintenance_sum(bit_pre, bit_suf, n, p, k):
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    return pre_sum + suf_sum


def main():
    data = input().split()
    n, k, a, b, q, idx = _read_header(data)

    # orders[i]: number of orders for day i (1-based)
    orders = [0] * (n + 1)

    # BITs for prefix and suffix
    bit_pre = BIT(n)   # stores min(order_count[i], b)
    bit_suf = BIT(n)   # stores min(order_count[i], a)

    results = []

    for _ in range(q):
        t = int(data[idx])
        idx += 1

        if t == 1:
            d = int(data[idx])
            idx += 1

            x = int(data[idx])
            idx += 1

            _apply_order_increase(
                bit_pre,
                bit_suf,
                orders,
                d,
                x,
                pre_limit=b,
                suf_limit=a,
            )
        else:
            p = int(data[idx])
            idx += 1

            # Maintenance from p to p+k-1 inclusive
            results.append(_maintenance_sum(bit_pre, bit_suf, n, p, k))

    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
```

- Extracted initial token parsing into `_read_header` to make `main` start with a clear initialization step while preserving the original token order and conversions.
- Moved the day-update logic into `_apply_order_increase` to isolate the capped-value delta calculation and preserve the original order of reading old values, mutating `orders`, computing new values, and updating both BITs.
- Moved the maintenance query arithmetic into `_maintenance_sum` to clarify the intent of the query branch while preserving the exact BIT query order and arithmetic.
- Kept `BIT`, `main`, and the module-level `input` binding unchanged to preserve public interfaces and runtime behavior.