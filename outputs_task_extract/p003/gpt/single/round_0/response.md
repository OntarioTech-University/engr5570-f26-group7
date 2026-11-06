```python
def read_input():
    password = input().strip()
    n = int(input().strip())
    words = []
    for _ in range(n):
        words.append(input().strip())
    return password, words


def has_word_ending_with(words, character):
    for word in words:
        if word[1] == character:
            return True
    return False


def has_word_starting_with(words, character):
    for word in words:
        if word[0] == character:
            return True
    return False


def can_form_password(password, words):
    if password in words:
        return True

    first_char_needed = password[0]
    second_char_needed = password[1]
    can_end_with_first = has_word_ending_with(words, first_char_needed)
    can_start_with_second = has_word_starting_with(words, second_char_needed)
    return can_end_with_first and can_start_with_second


def print_result(can_form):
    if can_form:
        print("YES")
    else:
        print("NO")


def main():
    password, words = read_input()
    result = can_form_password(password, words)
    print_result(result)


main()
```

- Moved input reading, the two word searches, the overall check, and output printing into small functions.
- Kept the searches separate and in their original order, including when the first search fails, to preserve exception behavior.