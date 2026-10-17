```python
def count_balanced_substrings(s):
    count = 0
    n = len(s)
    for l in range(n):
        for r in range(l, n):
            if has_balanced_split(s, l, r):
                count += 1
    return count


def has_balanced_split(s, l, r):
    for x in range(l, r + 1):
        left_4 = s[l:x].count('4')
        right_7 = s[x:r + 1].count('7')
        if left_4 == right_7:
            return True
    return False


t = int(input())
for _ in range(t):
    s = input()
    print(count_balanced_substrings(s))
```

### Summary of changes

- **Extracted `has_balanced_split` helper function**  
  Moved the innermost loop and conditional logic into a well-named function. This reduces nesting depth and makes the main function easier to follow by separating the "check if a substring has a balanced split" concern from the substring enumeration.

- **Replaced `break` with early `return` in the helper**  
  The original `break` only exited the innermost loop; the new `return True` makes the intent clearer and avoids the need for a flag variable or post-loop check.

- **No behavioral changes**  
  The refactored code preserves the exact same logic, output, and side effects as the original. Public function signatures remain unchanged.