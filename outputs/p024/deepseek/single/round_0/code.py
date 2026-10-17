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


def parse_input(data):
    """Parse the initial input values and return them along with the starting index."""
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = int(data[idx]); idx += 1
    b = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1
    return n, k, a, b, q, idx


def process_order_update(orders, bit_pre, bit_suf, d, x, a, b):
    """Update order counts and BITs for a type 1 query."""
    old_b_val = min(orders[d], b)
    old_a_val = min(orders[d], a)
    orders[d] += x
    new_b_val = min(orders[d], b)
    new_a_val = min(orders[d], a)
    bit_pre.update(d, new_b_val - old_b_val)
    bit_suf.update(d, new_a_val - old_a_val)


def process_query(bit_pre, bit_suf, p, k, n):
    """Calculate and return the result for a type 2 query."""
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    return pre_sum + suf_sum


def main():
    data = sys.stdin.read().split()
    n, k, a, b, q, idx = parse_input(data)

    orders = [0] * (n + 1)
    bit_pre = BIT(n)   # stores min(order_count[i], b)
    bit_suf = BIT(n)   # stores min(order_count[i], a)

    results = []

    for _ in range(q):
        t = int(data[idx]); idx += 1
        if t == 1:
            d = int(data[idx]); idx += 1
            x = int(data[idx]); idx += 1
            process_order_update(orders, bit_pre, bit_suf, d, x, a, b)
        else:
            p = int(data[idx]); idx += 1
            results.append(process_query(bit_pre, bit_suf, p, k, n))

    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
