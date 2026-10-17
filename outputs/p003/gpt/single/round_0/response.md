```python
# Read input
password = input().strip()
n = int(input().strip())
words = []
for _ in range(n):
    words.append(input().strip())

# Check if password exists as a word
if password in words:
    print("YES")
else:
    # Check whether the password can be formed across word boundaries.
    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = any(word[1] == first_char_needed for word in words)
    can_start_with_second = any(word[0] == second_char_needed for word in words)

    print("YES" if can_end_with_first and can_start_with_second else "NO")
```

- Replaced the two search loops with `any()`, retaining their order and short-circuit behavior.
- Collapsed the final conditional into one print statement while preserving the same output.