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
    import sys
    read = sys.stdin.read
    return read().split()


def read_int(data, idx):
    return int(data[idx]), idx + 1


def parse_header(data):
    idx = 0
    n, idx = read_int(data, idx)
    k, idx = read_int(data, idx)
    a, idx = read_int(data, idx)
    b, idx = read_int(data, idx)
    q, idx = read_int(data, idx)
    return n, k, a, b, q, idx


def capped_value(count, limit):
    return min(count, limit)


def apply_order_update(orders, bit_pre, bit_suf, d, x, b, a):
    old_b_val = capped_value(orders[d], b)
    old_a_val = capped_value(orders[d], a)

    orders[d] += x

    new_b_val = capped_value(orders[d], b)
    new_a_val = capped_value(orders[d], a)

    bit_pre.update(d, new_b_val - old_b_val)
    bit_suf.update(d, new_a_val - old_a_val)


def maintenance_sum(bit_pre, bit_suf, p, k, n):
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    return pre_sum + suf_sum


def process_queries(data, idx, n, k, a, b, q):
    orders = [0] * (n + 1)

    bit_pre = BIT(n)
    bit_suf = BIT(n)

    results = []

    for _ in range(q):
        t, idx = read_int(data, idx)

        if t == 1:
            d, idx = read_int(data, idx)
            x, idx = read_int(data, idx)
            apply_order_update(orders, bit_pre, bit_suf, d, x, b, a)
        else:
            p, idx = read_int(data, idx)
            results.append(maintenance_sum(bit_pre, bit_suf, p, k, n))

    return results


def print_results(results):
    print('\n'.join(map(str, results)))


def main():
    data = read_input()
    n, k, a, b, q, idx = parse_header(data)
    results = process_queries(data, idx, n, k, a, b, q)
    print_results(results)


if __name__ == "__main__":
    main()
