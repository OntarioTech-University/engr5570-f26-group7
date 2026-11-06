```python
def read_input():
    password = input().strip()
    n = int(input().strip())
    words = []
    for _ in range(n):
        words.append(input().strip())
    return password, words


def has_character_at(words, index, character):
    for word in words:
        if word[index] == character:
            return True
    return False


def check_password(password, words):
    if password in words:
        return "YES"

    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = has_character_at(words, 1, first_char_needed)
    can_start_with_second = has_character_at(words, 0, second_char_needed)

    if can_end_with_first and can_start_with_second:
        return "YES"
    return "NO"


def print_result(result):
    print(result)


def main():
    password, words = read_input()
    result = check_password(password, words)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Separated input, computation, and output into functions, passing data through parameters and return values instead of global variables.
- Replaced the two word-search loops with a shared helper. Both searches still run in the original order, preserving their exception behavior.
- Moved execution under the `main()` guard so importing the file does not run the program.