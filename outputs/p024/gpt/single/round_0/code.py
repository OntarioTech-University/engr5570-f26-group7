import sys


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


input = sys.stdin.read


def _add_orders(orders, day, count, a, b, bit_pre, bit_suf):
    old_b_val = min(orders[day], b)
    old_a_val = min(orders[day], a)

    orders[day] += count

    new_b_val = min(orders[day], b)
    new_a_val = min(orders[day], a)
    bit_pre.update(day, new_b_val - old_b_val)
    bit_suf.update(day, new_a_val - old_a_val)


def _total_outside_maintenance(bit_pre, bit_suf, p, k, n):
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    return pre_sum + suf_sum


def main():
    data = input().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = int(data[idx]); idx += 1
    b = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1

    # orders[i]: number of orders for day i (1-based)
    orders = [0] * (n + 1)

    # BITs for prefix and suffix
    bit_pre = BIT(n)   # stores min(order_count[i], b)
    bit_suf = BIT(n)   # stores min(order_count[i], a)

    results = []

    for _ in range(q):
        t = int(data[idx]); idx += 1
        if t == 1:
            d = int(data[idx]); idx += 1
            x = int(data[idx]); idx += 1
            _add_orders(orders, d, x, a, b, bit_pre, bit_suf)
        else:
            p = int(data[idx]); idx += 1
            # Maintenance from p to p+k-1 inclusive
            results.append(_total_outside_maintenance(bit_pre, bit_suf, p, k, n))

    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
