```python
def _max_c_streak(line):
    max_streak = 0
    current_streak = 0

    for ch in line:
        if ch == 'C':
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            current_streak = 0

    return max_streak


def _leading_c_count(line):
    count = 0

    for ch in line:
        if ch == 'C':
            count += 1
        else:
            break

    return count


def _trailing_c_count(line):
    count = 0

    for ch in reversed(line):
        if ch == 'C':
            count += 1
        else:
            break

    return count


def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    n = int(data[0])
    lines = data[1:]

    max_within_single_day = 0
    max_across_days = 0

    prev_trailing_c = 0

    for line in lines:
        max_in_day = _max_c_streak(line)
        max_within_single_day = max(max_within_single_day, max_in_day)

        leading_c = _leading_c_count(line)
        trailing_c = _trailing_c_count(line)

        if prev_trailing_c > 0 and leading_c > 0:
            max_across_days = max(max_across_days, prev_trailing_c + leading_c)

        max_across_days = max(max_across_days, max_in_day)

        prev_trailing_c = trailing_c

    print(max_within_single_day, max_across_days)


if __name__ == "__main__":
    main()
```

- Extracted the intra-day streak calculation into `_max_c_streak` to reduce nesting and make the main loop easier to read.
- Extracted leading and trailing `'C'` counting into `_leading_c_count` and `_trailing_c_count`, giving each small responsibility a clear name.
- Renamed local accumulators `x` and `y` to `max_within_single_day` and `max_across_days` for clarity without affecting runtime behavior.
- Preserved the original parsing of `n`, input reading order, processing order, conditionals, and final `print` behavior to keep outputs and exceptions unchanged.