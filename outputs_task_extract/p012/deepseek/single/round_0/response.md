```python
def read_input():
    import sys
    data = sys.stdin.read().splitlines()
    int(data[0])  # Preserve original validation of the first line
    return data[1:]


def max_streak_in_line(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            if curr_streak > max_in_day:
                max_in_day = curr_streak
        else:
            curr_streak = 0

    return max_in_day


def count_leading_c(line):
    count = 0
    for ch in line:
        if ch == 'C':
            count += 1
        else:
            break
    return count


def count_trailing_c(line):
    count = 0
    for ch in reversed(line):
        if ch == 'C':
            count += 1
        else:
            break
    return count


def compute_day_stats(line):
    return (
        max_streak_in_line(line),
        count_leading_c(line),
        count_trailing_c(line),
    )


def process_lines(lines):
    x = 0
    y = 0
    prev_trailing_c = 0

    for line in lines:
        max_in_day, leading_c, trailing_c = compute_day_stats(line)

        if max_in_day > x:
            x = max_in_day

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            if combined > y:
                y = combined

        if max_in_day > y:
            y = max_in_day

        prev_trailing_c = trailing_c

    return x, y


def print_result(x, y):
    print(x, y)


def main():
    lines = read_input()
    x, y = process_lines(lines)
    print_result(x, y)


if __name__ == "__main__":
    main()
```

- Extracted `read_input()` to isolate stdin reading and preserve the original first-line `int()` validation.
- Extracted `max_streak_in_line()`, `count_leading_c()`, and `count_trailing_c()` to give each per-line metric a single clear responsibility.
- Extracted `compute_day_stats()` to combine the three per-line metrics without duplicating logic.
- Extracted `process_lines()` to own the cross-day state updates (`x`, `y`, `prev_trailing_c`) and keep the main loop short.
- Extracted `print_result()` to separate output formatting from computation.
- Kept `main()` as the only public entry point, preserving its signature and runtime behavior.