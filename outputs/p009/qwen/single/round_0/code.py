def _has_balanced_split(s, left, right):
    for split in range(left, right + 1):
        left_fours = s[left:split].count('4')
        right_sevens = s[split:right + 1].count('7')

        if left_fours == right_sevens:
            return True

    return False


def count_balanced_substrings(s):
    count = 0
    n = len(s)

    for left in range(n):
        for right in range(left, n):
            if _has_balanced_split(s, left, right):
                count += 1

    return count


t = int(input())
for _ in range(t):
    s = input()
    print(count_balanced_substrings(s))
