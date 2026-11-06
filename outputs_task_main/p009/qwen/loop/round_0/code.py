def count_balanced_substrings(s):
    count = 0
    n = len(s)
    for l in range(n):
        for r in range(l, n):
            for x in range(l, r + 1):
                left_4 = s[l:x].count('4')
                right_7 = s[x:r + 1].count('7')
                if left_4 == right_7:
                    count += 1
                    break
    return count


def read_case_count():
    return int(input())


def read_case():
    return input()


def print_result(result):
    print(result)


def main():
    case_count = read_case_count()
    for _ in range(case_count):
        s = read_case()
        result = count_balanced_substrings(s)
        print_result(result)


if __name__ == "__main__":
    main()
