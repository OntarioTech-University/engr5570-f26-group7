```python
import sys


def _longest_c_streak(day_log):
    """Return the longest contiguous run of 'C' characters in a single day log."""
    current_streak = 0
    longest_streak = 0

    for char in day_log:
        if char == 'C':
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0

    if current_streak > longest_streak:
        longest_streak = current_streak

    return longest_streak


def _leading_c_streak(day_log):
    """Return the number of consecutive 'C' characters at the start of the log."""
    streak = 0

    for char in day_log:
        if char == 'C':
            streak += 1
        else:
            break

    return streak


def _trailing_c_streak(day_log):
    """Return the number of consecutive 'C' characters at the end of the log."""
    streak = 0

    for char in reversed(day_log):
        if char == 'C':
            streak += 1
        else:
            break

    return streak


def _next_streak_from_prev_day(day_log, start_streak, streak_from_prev_day):
    """Return the coding streak to carry forward after processing this day."""
    if start_streak == len(day_log) and len(day_log) > 0:
        return streak_from_prev_day + len(day_log)

    return _trailing_c_streak(day_log)


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    It calculates X, the maximum of the longest daily coding streaks, and
    Y, the absolute longest coding streak across all N days.
    """
    try:
        N = int(sys.stdin.readline())
    except (ValueError, IndexError):
        return

    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for _ in range(N):
        day_log = sys.stdin.readline().strip()

        longest_in_day = _longest_c_streak(day_log)
        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day
        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day

        start_streak = _leading_c_streak(day_log)
        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

        streak_from_prev_day = _next_streak_from_prev_day(
            day_log,
            start_streak,
            streak_from_prev_day,
        )

    print(f"{max_daily_streak} {overall_max_streak}")


solve()
```

- Extracted the within-day streak scan into `_longest_c_streak` to reduce nesting in `solve` and make the purpose of the loop explicit.
- Extracted prefix and suffix streak scans into `_leading_c_streak` and `_trailing_c_streak` to clarify the cross-midnight streak logic.
- Moved the carry-over decision into `_next_streak_from_prev_day` so the main loop focuses on processing days rather than low-level streak rules.
- Preserved the original `solve` signature, input parsing, exception handling, update order, final output, and unconditional `solve()` call to maintain existing runtime behavior.