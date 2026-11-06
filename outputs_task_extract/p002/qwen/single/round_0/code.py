def read_pair():
    x, y = map(int, input().split())
    return x, y


def read_input():
    first_row = read_pair()
    second_row = read_pair()
    third_row = read_pair()
    return first_row, second_row, third_row


def has_valid_values(b, c, d):
    return 1 <= b <= 9 and 1 <= c <= 9 and 1 <= d <= 9


def has_distinct_values(a, b, c, d):
    return len({a, b, c, d}) == 4


def satisfies_remaining_constraints(b, c, d, r2, c2, d2):
    return c + d == r2 and b + d == c2 and b + c == d2


def find_solution(r1, r2, c1, c2, d1, d2):
    for a in range(1, 10):
        b = r1 - a
        c = c1 - a
        d = d1 - a

        if has_valid_values(b, c, d):
            if has_distinct_values(a, b, c, d):
                if satisfies_remaining_constraints(b, c, d, r2, c2, d2):
                    return [[a, b], [c, d]]

    return None


def print_solution(solution):
    if solution is None:
        print(-1)
    else:
        print(solution[0][0], solution[0][1])
        print(solution[1][0], solution[1][1])


def main():
    (r1, r2), (c1, c2), (d1, d2) = read_input()
    solution = find_solution(r1, r2, c1, c2, d1, d2)
    print_solution(solution)


main()
