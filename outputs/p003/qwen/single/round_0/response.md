```python
def _read_words(count):
    words = []
    for _ in range(count):
        words.append(input().strip())
    return words


def _has_word_with_char_at(words, char, index):
    for word in words:
        if word[index] == char:
            return True
    return False


# Read input
password = input().strip()
n = int(input().strip())
words = _read_words(n)

# Check if password exists as a word
if password in words:
    print("YES")
else:
    # Check if we can form password across word boundaries
    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = _has_word_with_char_at(words, first_char_needed, 1)
    can_start_with_second = _has_word_with_char_at(words, second_char_needed, 0)

    if can_end_with_first and can_start_with_second:
        print("YES")
    else:
        print("NO")
```

- Extracted the word-reading loop into `_read_words(count)` to reduce top-level clutter while preserving the exact input order, stripping behavior, and list construction.
- Replaced the two duplicated search loops with `_has_word_with_char_at(words, char, index)` to make the repeated pattern explicit and easier to read.
- Kept the original top-level control flow, variable names, and eager evaluation of both boundary checks, preserving the original outputs, evaluation order, and possible exceptions.