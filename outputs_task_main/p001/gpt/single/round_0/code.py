def read_input():
    r1, r2 = map(int, input().split())
    c1, c2 = map(int, input().split())
    d1, d2 = map(int, input().split())
    return r1, r2, c1, c2, d1, d2


def solve_magic_box(r1, r2, c1, c2, d1, d2):
    # Iterate through all possible combinations of a, b, c, and d
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                for d in range(1, 10):
                    if len({a, b, c, d}) == 4 and \
                       a + b == r1 and \
                       c + d == r2 and \
                       a + c == c1 and \
                       b + d == c2 and \
                       a + d == d1 and \
                       b + c == d2:
                        return f"{a} {b}\n{c} {d}"
    return "-1"


def print_result(result):
    print(result)


def main():
    values = read_input()
    result = solve_magic_box(*values)
    print_result(result)


if __name__ == "__main__":
    main()
