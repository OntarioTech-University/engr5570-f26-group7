def _has_balanced_split(s, l, r):
    for x in range(l, r + 1):
        left_4 = s[l:x].count('4')
        right_7 = s[x:r + 1].count('7')
        if left_4 == right_7:
            return True
    return False


def count_balanced_substrings(s):
    count = 0
    n = len(s)
    for l in range(n):
        for r in range(l, n):
            if _has_balanced_split(s, l, r):
                count += 1
    return count


def _read_case_count():
    return int(input())


def _read_string():
    return input()


def _print_count(count):
    print(count)


def _run_case():
    s = _read_string()
    count = count_balanced_substrings(s)
    _print_count(count)


def _main():
    t = _read_case_count()
    for _ in range(t):
        _run_case()


_main()
