```python
def _is_balanced_split(s, l, r, x):
    return s[l:x].count('4') == s[x:r + 1].count('7')


def _has_balanced_split(s, l, r):
    for x in range(l, r + 1):
        if _is_balanced_split(s, l, r, x):
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


def read_test_count():
    return int(input())


def read_string():
    return input()


def print_result(result):
    print(result)


def main():
    t = read_test_count()
    for _ in range(t):
        s = read_string()
        result = count_balanced_substrings(s)
        print_result(result)


main()
```

- Extracted the split-checking logic into `_is_balanced_split` and `_has_balanced_split` to separate the condition from the substring iteration.
- Kept `count_balanced_substrings` focused on iterating substrings and counting valid ones.
- Moved input reading into `read_test_count` and `read_string`.
- Moved output printing into `print_result`.
- Added a `main` function to orchestrate reading, computation, and printing, preserving the original top-level execution behavior.