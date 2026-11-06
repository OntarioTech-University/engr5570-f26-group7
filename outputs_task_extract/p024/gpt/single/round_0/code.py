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


def read_input():
    data = input().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = int(data[idx]); idx += 1
    b = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1
    return data, idx, n, k, a, b, q


def create_state(n):
    orders = [0] * (n + 1)
    bit_pre = BIT(n)
    bit_suf = BIT(n)
    results = []
    return orders, bit_pre, bit_suf, results


def process_update(data, idx, orders, a, b, bit_pre, bit_suf):
    d = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1
    old_b_val = min(orders[d], b)
    old_a_val = min(orders[d], a)
    orders[d] += x
    new_b_val = min(orders[d], b)
    new_a_val = min(orders[d], a)
    bit_pre.update(d, new_b_val - old_b_val)
    bit_suf.update(d, new_a_val - old_a_val)
    return idx


def process_query(data, idx, n, k, bit_pre, bit_suf, results):
    p = int(data[idx]); idx += 1
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    results.append(pre_sum + suf_sum)
    return idx


def process_queries(data, idx, n, k, a, b, q, orders, bit_pre, bit_suf, results):
    for _ in range(q):
        t = int(data[idx]); idx += 1
        if t == 1:
            idx = process_update(data, idx, orders, a, b, bit_pre, bit_suf)
        else:
            idx = process_query(data, idx, n, k, bit_pre, bit_suf, results)


def print_results(results):
    print('\n'.join(map(str, results)))


def main():
    data, idx, n, k, a, b, q = read_input()
    orders, bit_pre, bit_suf, results = create_state(n)
    process_queries(data, idx, n, k, a, b, q, orders, bit_pre, bit_suf, results)
    print_results(results)


if __name__ == "__main__":
    main()
