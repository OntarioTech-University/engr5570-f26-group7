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

def _read_input():
    return input().split()

def _parse_header(data):
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

def _initialize_orders(n):
    return [0] * (n + 1)

def _initialize_trees(n):
    bit_pre = BIT(n)
    bit_suf = BIT(n)
    return bit_pre, bit_suf

def _apply_order_update(data, idx, orders, bit_pre, bit_suf, a, b):
    d = int(data[idx])
    idx += 1
    x = int(data[idx])
    idx += 1
    old_b_val = min(orders[d], b)
    old_a_val = min(orders[d], a)
    orders[d] += x
    new_b_val = min(orders[d], b)
    new_a_val = min(orders[d], a)
    bit_pre.update(d, new_b_val - old_b_val)
    bit_suf.update(d, new_a_val - old_a_val)
    return idx

def _compute_maintenance_answer(data, idx, n, k, bit_pre, bit_suf):
    p = int(data[idx])
    idx += 1
    pre_sum = bit_pre.query(p - 1)
    suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
    return idx, pre_sum + suf_sum

def _process_queries(data, idx, n, k, a, b, q):
    orders = _initialize_orders(n)
    bit_pre, bit_suf = _initialize_trees(n)
    results = []
    for _ in range(q):
        t = int(data[idx])
        idx += 1
        if t == 1:
            idx = _apply_order_update(data, idx, orders, bit_pre, bit_suf, a, b)
        else:
            idx, answer = _compute_maintenance_answer(data, idx, n, k, bit_pre, bit_suf)
            results.append(answer)
    return results

def _print_results(results):
    print('\n'.join(map(str, results)))

def main():
    data = _read_input()
    n, k, a, b, q, idx = _parse_header(data)
    results = _process_queries(data, idx, n, k, a, b, q)
    _print_results(results)

if __name__ == "__main__":
    main()
