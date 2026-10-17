```python
def _max_streak_in_day(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            max_in_day = max(max_in_day, curr_streak)
        else:
            curr_streak = 0

    return max_in_day


def _count_initial_c(characters):
    count = 0
    for ch in characters:
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

    x = 0  # Max within a single day
    y = 0  # Max across multiple days
    prev_trailing_c = 0  # Trailing C's from previous day

    for line in lines:
        max_in_day = _max_streak_in_day(line)
        x = max(x, max_in_day)

        leading_c = _count_initial_c(line)
        trailing_c = _count_initial_c(reversed(line))

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)

        y = max(y, max_in_day)
        prev_trailing_c = trailing_c

    print(x, y)


if __name__ == "__main__":
    main()
```

- Extracted the within-day streak calculation so `main` focuses on processing each day.
- Reused one counting function for leading and trailing C’s, removing duplicate loops while preserving their behavior.