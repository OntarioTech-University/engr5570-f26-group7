```python
def read_input():
    password = input().strip()
    word_count = int(input().strip())
    words = [input().strip() for _ in range(word_count)]
    return password, words


def is_password_in_words(password, words):
    return password in words


def can_form_password_across_word_boundaries(password, words):
    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = any(word[1] == first_char_needed for word in words)
    can_start_with_second = any(word[0] == second_char_needed for word in words)

    return can_end_with_first and can_start_with_second


def should_print_yes(password, words):
    if is_password_in_words(password, words):
        return True
    return can_form_password_across_word_boundaries(password, words)


def print_answer(answer_is_yes):
    if answer_is_yes:
        print("YES")
    else:
        print("NO")


def main():
    password, words = read_input()
    answer_is_yes = should_print_yes(password, words)
    print_answer(answer_is_yes)


main()
```

- Split input handling into `read_input`, so all stdin parsing is isolated in one small function.
- Added `is_password_in_words` to encapsulate the direct membership check.
- Added `can_form_password_across_word_boundaries` to isolate the two cross-word boundary checks.
- Added `should_print_yes` to combine the two checks in the original order and preserve short-circuit behavior.
- Added `print_answer` to centralize output printing.
- Added `main` to orchestrate input, computation, and output; the top-level `main()` call preserves the original script’s execution behavior.
- Replaced the manual flag-and-break loops with `any` for readability while keeping the same short-circuit behavior.