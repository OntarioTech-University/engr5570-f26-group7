```python
def read_input_lines():
    import sys
    return sys.stdin.read().splitlines()


def max_c_streak_in_line(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            max_in_day = max(max_in_day, curr_streak)
        else:
            curr_streak = 0

    return max_in_day


def count_initial_c_streak(chars):
    count = 0

    for ch in chars:
        if ch == 'C':
            count += 1
        else:
            break

    return count


def compute_max_streaks(data):
    n = int(data[0])
    lines = data[1:]

    x = 0  # Max within a single day
    y = 0  # Max across multiple days

    prev_trailing_c = 0  # Trailing C's from previous day

    for line in lines:
        max_in_day = max_c_streak_in_line(line)
        x = max(x, max_in_day)

        leading_c = count_initial_c_streak(line)
        trailing_c = count_initial_c_streak(reversed(line))

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)

        y = max(y, max_in_day)

        prev_trailing_c = trailing_c

    return x, y


def print_results(x, y):
    print(x, y)


def main():
    data = read_input_lines()
    x, y = compute_max_streaks(data)
    print_results(x, y)


if __name__ == "__main__":
    main()
```

- Moved stdin reading into `read_input_lines()` so input handling is isolated and no logic runs at import time.
- Moved the core algorithm into `compute_max_streaks(data)` and made it return the results instead of mutating local top-level state.
- Moved output handling into `print_results(x, y)` so printing is separate from computation.
- Extracted the per-line maximum streak loop into `max_c_streak_in_line(line)` to keep the main computation clearer.
- Replaced the duplicated leading/trailing counting loops with a shared helper, `count_initial_c_streak(chars)`, reused for both forward and reversed iteration.
- Preserved the existing public `main()` signature and the original parsing of `n`, keeping the same runtime behavior and exception behavior.