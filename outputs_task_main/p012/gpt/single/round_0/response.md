```python
def read_input():
    import sys

    data = sys.stdin.read().splitlines()
    int(data[0])
    return data[1:]


def max_streak_in_day(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            max_in_day = max(max_in_day, curr_streak)
        else:
            curr_streak = 0

    return max_in_day


def count_consecutive_c(characters):
    count = 0
    for ch in characters:
        if ch == 'C':
            count += 1
        else:
            break
    return count


def calculate_streaks(lines):
    x = 0  # Max within a single day
    y = 0  # Max across multiple days
    prev_trailing_c = 0

    for line in lines:
        max_in_day = max_streak_in_day(line)
        x = max(x, max_in_day)

        leading_c = count_consecutive_c(line)
        trailing_c = count_consecutive_c(reversed(line))

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)

        y = max(y, max_in_day)
        prev_trailing_c = trailing_c

    return x, y


def print_results(x, y):
    print(x, y)


def main():
    lines = read_input()
    x, y = calculate_streaks(lines)
    print_results(x, y)


if __name__ == "__main__":
    main()
```

- Separated input, computation, and output into functions, with data passed through return values and parameters.
- Moved the repeated leading and trailing `C` counting into one helper.
- Kept the original integer conversion, including its exception behavior, even though its value is unused.