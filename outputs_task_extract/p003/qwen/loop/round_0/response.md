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


def password_is_word(password, words):
    return password in words


def has_word_with_second_character(words, character):
    for word in words:
        if word[1] == character:
            return True
    return False


def has_word_with_first_character(words, character):
    for word in words:
        if word[0] == character:
            return True
    return False


def can_form_across_word_boundaries(password, words):
    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = has_word_with_second_character(words, first_char_needed)
    can_start_with_second = has_word_with_first_character(words, second_char_needed)

    return can_end_with_first and can_start_with_second


def is_valid_password(password, words):
    if password_is_word(password, words):
        return True
    return can_form_across_word_boundaries(password, words)


def print_result(is_valid):
    if is_valid:
        print("YES")
    else:
        print("NO")


def main():
    password, words = read_input()
    is_valid = is_valid_password(password, words)
    print_result(is_valid)


main()
```

- Extracted input reading into `read_password`, `read_word_count`, `read_words`, and `read_input` to isolate I/O while preserving the original input order.
- Moved the direct password membership check into `password_is_word` so that step is separate from the cross-word check.
- Split the two word-scanning loops into `has_word_with_second_character` and `has_word_with_first_character`, preserving the original indexing and evaluation order.
- Collected the cross-word construction logic in `can_form_across_word_boundaries`, keeping the original password character accesses before the word scans.
- Added `is_valid_password`, `print_result`, and `main` to separate decision logic, output, and orchestration, leaving only a single top-level call.