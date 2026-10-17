```python
# Read input
password = input().strip()
n = int(input().strip())
words = [input().strip() for _ in range(n)]


def can_form_password(password, words):
    """Check if password can be formed from the given words."""
    if password in words:
        return True

    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = any(word[1] == first_char_needed for word in words)
    can_start_with_second = any(word[0] == second_char_needed for word in words)

    return can_end_with_first and can_start_with_second


if can_form_password(password, words):
    print("YES")
else:
    print("NO")
```

**Changes made:**

- **Extracted password-checking logic into a helper function** `can_form_password` to separate input/output from the core logic, making the code easier to test and understand.
- **Replaced manual loops with `any()` generator expressions** to reduce boilerplate and make the intent clearer.
- **Used a list comprehension** for reading words to shorten the input loop and improve readability.
- **Simplified the conditional structure** by returning a boolean directly from the helper function, eliminating nested `if/else` blocks in the main flow.