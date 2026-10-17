```python
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


t = int(input())
for _ in range(t):
    s = input()
    print(count_balanced_substrings(s))
```

- Extracted the split check into a private helper, reducing nesting in `count_balanced_substrings` while keeping the counting logic and public interface unchanged.