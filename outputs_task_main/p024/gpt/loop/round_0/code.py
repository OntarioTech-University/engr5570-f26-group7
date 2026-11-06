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


def read_input():
    return sys.stdin.read().split()


def capped_delta(old_count, new_count, cap):
    return min(new_count, cap) - min(old_count, cap)


def compute_results(data):
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
            old_count = orders[d]
            orders[d] += x
            new_count = orders[d]
            bit_pre.update(d, capped_delta(old_count, new_count, b))
            bit_suf.update(d, capped_delta(old_count, new_count, a))
        else:
            p = int(data[idx]); idx += 1
            # Maintenance from p to p+k-1 inclusive
            pre_sum = bit_pre.query(p - 1)
            suf_sum = bit_suf.query(n) - bit_suf.query(p + k - 1)
            results.append(pre_sum + suf_sum)

    return results


def print_output(results):
    print('\n'.join(map(str, results)))


def main():
    data = read_input()
    results = compute_results(data)
    print_output(results)


if __name__ == "__main__":
    main()
