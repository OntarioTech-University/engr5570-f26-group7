```python
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
```

- Extracted the innermost loop into a private helper function, `_has_balanced_split`, so `count_balanced_substrings` no longer contains three nested loops and is easier to read.
- Renamed short loop variables `l`, `r`, and `x` to `left`, `right`, and `split` to make the substring boundaries and split point clearer.
- Kept the public function name, signature, return value, top-level input/output behavior, and evaluation order unchanged.
- Preserved the original early-exit behavior: once a valid split is found for a substring, no further splits are checked for that substring.