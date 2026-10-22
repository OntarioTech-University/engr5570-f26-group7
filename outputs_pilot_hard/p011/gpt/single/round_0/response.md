```python
import sys


def read_input():
    """Read the number of days and return an iterator over their logs."""
    days = int(sys.stdin.readline())
    return (sys.stdin.readline().strip() for _ in range(days))


def longest_streak(day_log):
    """Find the longest coding streak contained within one day."""
    current_streak = 0
    longest = 0

    for char in day_log:
        if char == 'C':
            current_streak += 1
        else:
            if current_streak > longest:
                longest = current_streak
            current_streak = 0

    if current_streak > longest:
        longest = current_streak

    return longest


def starting_streak(chars):
    """Count consecutive coding characters at the start of an iterable."""
    streak = 0
    for char in chars:
        if char == 'C':
            streak += 1
        else:
            break
    return streak


def calculate_streaks(day_logs):
    """Calculate the maximum daily and overall coding streaks."""
    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for day_log in day_logs:
        longest_in_day = longest_streak(day_log)

        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day
        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day

        start_streak = starting_streak(day_log)
        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            streak_from_prev_day = starting_streak(reversed(day_log))

    return max_daily_streak, overall_max_streak


def print_result(max_daily_streak, overall_max_streak):
    print(f"{max_daily_streak} {overall_max_streak}")


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    It calculates X, the maximum of the longest daily coding streaks, and
    Y, the absolute longest coding streak across all N days.
    """
    try:
        day_logs = read_input()
    except (ValueError, IndexError):
        return

    max_daily_streak, overall_max_streak = calculate_streaks(day_logs)
    print_result(max_daily_streak, overall_max_streak)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Separated input reading, streak calculation, and output printing into functions. Day logs remain lazily read, preserving when input is consumed and where read errors occur.
- Moved repeated start/end streak counting into one helper.
- Kept `solve()` unchanged as the public entry point and placed execution under the `__main__` guard.