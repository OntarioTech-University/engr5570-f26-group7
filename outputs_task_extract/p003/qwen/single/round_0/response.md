```python
def read_password():
    return input().strip()


def read_word_count():
    return int(input().strip())


def read_words(count):
    words = []
    for _ in range(count):
        words.append(input().strip())
    return words


def read_input():
    password = read_password()
    count = read_word_count()
    words = read_words(count)
    return password, words


def is_password_in_words(password, words):
    return password in words


def has_word_with_second_char(words, char):
    for word in words:
        if word[1] == char:
            return True
    return False


def has_word_with_first_char(words, char):
    for word in words:
        if word[0] == char:
            return True
    return False


def can_form_password_across_word_boundaries(password, words):
    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = has_word_with_second_char(words, first_char_needed)
    can_start_with_second = has_word_with_first_char(words, second_char_needed)

    return can_end_with_first and can_start_with_second


def is_password_accepted(password, words):
    if is_password_in_words(password, words):
        return True

    return can_form_password_across_word_boundaries(password, words)


def print_result(accepted):
    if accepted:
        print("YES")
    else:
        print("NO")


def main():
    password, words = read_input()
    accepted = is_password_accepted(password, words)
    print_result(accepted)


main()
```

- Split input reading into `read_password`, `read_word_count`, `read_words`, and `read_input` so each input concern is isolated.
- Moved membership checking into `is_password_in_words` to separate the direct password check from fallback logic.
- Extracted the two character-search loops into `has_word_with_second_char` and `has_word_with_first_char`, preserving the original traversal order and index access.
- Kept the boundary-forming computation in `can_form_password_across_word_boundaries`, preserving the original evaluation order and exception behavior.
- Added `is_password_accepted` to centralize the decision flow without changing the original branching.
- Moved output printing into `print_result` to isolate side-effectful output.
- Kept a top-level `main()` call so the script still executes immediately, preserving the original runtime behavior.