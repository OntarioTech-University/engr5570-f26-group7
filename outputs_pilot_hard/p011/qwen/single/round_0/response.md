```python
import sys


def _read_day_log():
    return sys.stdin.readline().strip()


def _read_day_logs(num_days):
    return (_read_day_log() for _ in range(num_days))


def _read_input():
    try:
        num_days = int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None

    return _read_day_logs(num_days)


def _prefix_coding_streak(chars):
    streak = 0
    for char in chars:
        if char == 'C':
            streak += 1
        else:
            break
    return streak


def _leading_coding_streak(day_log):
    return _prefix_coding_streak(day_log)


def _trailing_coding_streak(day_log):
    return _prefix_coding_streak(reversed(day_log))


def _longest_coding_streak(day_log):
    current_day_streak = 0
    longest_in_day = 0

    for char in day_log:
        if char == 'C':
            current_day_streak += 1
        else:
            if current_day_streak > longest_in_day:
                longest_in_day = current_day_streak
            current_day_streak = 0

    if current_day_streak > longest_in_day:
        longest_in_day = current_day_streak

    return longest_in_day


def _next_carryover_streak(day_log, start_streak, streak_from_prev_day):
    if start_streak == len(day_log) and len(day_log) > 0:
        return streak_from_prev_day + len(day_log)

    return _trailing_coding_streak(day_log)


def _compute_streaks(day_logs):
    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for day_log in day_logs:
        longest_in_day = _longest_coding_streak(day_log)

        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day

        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day

        start_streak = _leading_coding_streak(day_log)
        combined_streak = streak_from_prev_day + start_streak

        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

        streak_from_prev_day = _next_carryover_streak(
            day_log,
            start_streak,
            streak_from_prev_day
        )

    return max_daily_streak, overall_max_streak


def _print_result(max_daily_streak, overall_max_streak):
    print(f"{max_daily_streak} {overall_max_streak}")


def main():
    day_logs = _read_input()

    if day_logs is None:
        return

    max_daily_streak, overall_max_streak = _compute_streaks(day_logs)
    _print_result(max_daily_streak, overall_max_streak)


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    It calculates X, the maximum of the longest daily coding streaks, and
    Y, the absolute longest coding streak across all N days.
    """
    main()


if __name__ == "__main__":
    main()
```

- Moved the top-level `solve()` call into `main()` guarded by `if __name__ == "__main__":`, while keeping `solve()` as a public wrapper.
- Split input reading, computation, and output printing into `_read_input()` / `_read_day_logs()`, `_compute_streaks()`, and `_print_result()`.
- Extracted repeated streak-counting logic into helper functions: `_longest_coding_streak()`, `_prefix_coding_streak()`, `_leading_coding_streak()`, and `_trailing_coding_streak()`.
- Used a lazy day-log generator to preserve the original streaming behavior and avoid introducing global state.
- Preserved the original `solve()` signature, return behavior, exception handling, and printed output format.