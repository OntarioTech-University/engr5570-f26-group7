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


def _next_int(tokens, idx):
    return int(tokens[idx]), idx + 1


def _capped_values(order_count, a, b):
    return min(order_count, b), min(order_count, a)


def read_input():
    import sys
    return sys.stdin.read().split()


def compute_results(tokens):
    idx = 0
    n, idx = _next_int(tokens, idx)
    k, idx = _next_int(tokens, idx)
    a, idx = _next_int(tokens, idx)
    b, idx = _next_int(tokens, idx)
    q, idx = _next_int(tokens, idx)

    # orders[i]: number of orders for day i (1-based)
    orders = [0] * (n + 1)

    # BITs for prefix and suffix
    bit_pre = BIT(n)   # stores min(order_count[i], b)
    bit_suf = BIT(n)   # stores min(order_count[i], a)

    results = []

    for _ in range(q):
        t, idx = _next_int(tokens, idx)
        if t == 1:
            d, idx = _next_int(tokens, idx)
            x, idx = _next_int(tokens, idx)
            old_b_val, old_a_val = _capped_values(orders[d], a, b)
            orders[d] += x
            new_b_val, new_a_val = _capped_values(orders[d], a, b)
            bit_pre.update(d, new_b_val - old_b_val)
            bit_suf.update(d, new_a_val - old_a_val)
        else:
            p, idx = _next_int(tokens, idx)
            # Maintenance from p to p+k-1 inclusive
            pre_sum = bit_pre.query(p - 1)
            suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
            results.append(pre_sum + suf_sum)

    return results


def print_results(results):
    print('\n'.join(map(str, results)))


def main():
    tokens = read_input()
    results = compute_results(tokens)
    print_results(results)


if __name__ == "__main__":
    main()
```

- Removed the top-level `input = sys.stdin.read` global and moved the `sys` import into `read_input`, so no module-level variables are created.
- Added `read_input()` to read all stdin tokens and return them.
- Added `compute_results(tokens)` to parse tokens and perform all BIT/order computations, returning results.
- Added `print_results(results)` to handle output formatting and printing.
- Added `_next_int(tokens, idx)` to remove repeated `int(tokens[idx]); idx += 1` parsing.
- Added `_capped_values(order_count, a, b)` to remove duplicated `min(orders[d], ...)` calculations.
- `main()` now only orchestrates the three functions, and the guarded `if __name__ == "__main__":` block calls it.
- Preserved the public `BIT` class and `main()` signature, and preserved runtime behavior.