```python
def read_case_count():
    return int(input())


def read_case_string():
    return input()


def print_result(result):
    print(result)


def has_balanced_split(s, left, right):
    for split in range(left, right + 1):
        left_4 = s[left:split].count('4')
        right_7 = s[split:right + 1].count('7')
        if left_4 == right_7:
            return True
    return False


def count_balanced_substrings(s):
    count = 0
    n = len(s)
    for left in range(n):
        for right in range(left, n):
            if has_balanced_split(s, left, right):
                count += 1
    return count


def main():
    case_count = read_case_count()
    for _ in range(case_count):
        case_string = read_case_string()
        result = count_balanced_substrings(case_string)
        print_result(result)


main()
```

- Extracted input reading into `read_case_count` and `read_case_string` so input handling is isolated.
- Extracted output printing into `print_result` so output handling is isolated.
- Moved the inner split-checking logic into `has_balanced_split`, preserving the original loop behavior and early exit.
- Kept `count_balanced_substrings` as the public computation entry point with the same signature and return value.
- Wrapped the top-level script flow in `main()` while still calling it immediately to preserve the original runtime behavior.