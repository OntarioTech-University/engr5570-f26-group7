```python
def read_input():
    password = input().strip()
    n = int(input().strip())
    words = []
    for _ in range(n):
        words.append(input().strip())
    return password, words


def has_word_with_char_at(words, index, char):
    for word in words:
        if word[index] == char:
            return True
    return False


def can_form_password(password, words):
    if password in words:
        return True

    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = has_word_with_char_at(words, 1, first_char_needed)
    can_start_with_second = has_word_with_char_at(words, 0, second_char_needed)

    return can_end_with_first and can_start_with_second


def print_result(result):
    if result:
        print("YES")
    else:
        print("NO")


def main():
    password, words = read_input()
    result = can_form_password(password, words)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved all top-level logic into a `main()` function and guarded it with `if __name__ == "__main__":`.
- Extracted input reading into `read_input()`, which returns the password and word list.
- Extracted the core decision logic into `can_form_password()`, which returns a boolean instead of printing directly.
- Extracted output printing into `print_result()`.
- Removed duplicated loop logic by adding `has_word_with_char_at()` and reusing it for both character checks.
- No global variables are used; all data is passed through parameters and return values.