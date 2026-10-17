```python
import sys


def read_number_of_days():
    """Read the number of days from stdin, returning None if input is invalid."""
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None


def longest_streak_in_string(s):
    """Return the length of the longest consecutive 'C' streak in string s."""
    current_streak = 0
    longest_streak = 0
    for char in s:
        if char == 'C':
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0
    return max(longest_streak, current_streak)


def leading_streak_length(s):
    """Return the length of the consecutive 'C' streak at the start of string s."""
    count = 0
    for char in s:
        if char == 'C':
            count += 1
        else:
            break
    return count


def trailing_streak_length(s):
    """Return the length of the consecutive 'C' streak at the end of string s."""
    count = 0
    for char in reversed(s):
        if char == 'C':
            count += 1
        else:
            break
    return count


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    It calculates X, the maximum of the longest daily coding streaks, and
    Y, the absolute longest coding streak across all N days.
    """
    n = read_number_of_days()
    if n is None:
        return

    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for _ in range(n):
        day_log = sys.stdin.readline().strip()

        longest_in_day = longest_streak_in_string(day_log)

        max_daily_streak = max(max_daily_streak, longest_in_day)
        overall_max_streak = max(overall_max_streak, longest_in_day)

        start_streak = leading_streak_length(day_log)
        combined_streak = streak_from_prev_day + start_streak
        overall_max_streak = max(overall_max_streak, combined_streak)

        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            streak_from_prev_day = trailing_streak_length(day_log)

    print(f"{max_daily_streak} {overall_max_streak}")


solve()
```

### Summary of changes

- **Extracted helper functions** for reading input, finding the longest streak in a string, and finding leading/trailing streak lengths. This reduces duplication and makes the main loop easier to follow.
- **Replaced manual max-update blocks** with the built-in `max()` function to simplify conditional logic and reduce nesting.
- **Removed redundant comments** that described what the code was doing rather than why, keeping only high-level explanatory comments where helpful.
- **Renamed local variables** to be more concise while preserving clarity (e.g., `N` → `n`, `current_day_streak` → `current_streak` inside the helper).
- **Preserved all behavior**: input handling, edge cases (empty day logs, all-`C` days, invalid input), and output formatting remain identical.