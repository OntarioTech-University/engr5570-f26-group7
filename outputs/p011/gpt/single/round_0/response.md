```python
import sys


def longest_streak_in_day(day_log):
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


def leading_coding_streak(chars):
    streak = 0
    for char in chars:
        if char == 'C':
            streak += 1
        else:
            break
    return streak


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
        longest_in_day = longest_streak_in_day(day_log)

        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day
        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day

        start_streak = leading_coding_streak(day_log)
        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            streak_from_prev_day = leading_coding_streak(reversed(day_log))

    print(f"{max_daily_streak} {overall_max_streak}")


solve()
```

- Extracted the within-day streak calculation so `solve()` focuses on processing days and updating totals.
- Reused one helper for leading and trailing streaks, removing a duplicate loop without changing when either streak is calculated.