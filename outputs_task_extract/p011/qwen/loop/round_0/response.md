```python
import sys


def _read_day_count():
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None


def _read_day_log():
    return sys.stdin.readline().strip()


def _longest_streak_in_day(day_log):
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


def _update_max_streaks(max_daily_streak, overall_max_streak, longest_in_day):
    if longest_in_day > max_daily_streak:
        max_daily_streak = longest_in_day
    if longest_in_day > overall_max_streak:
        overall_max_streak = longest_in_day
    return max_daily_streak, overall_max_streak


def _start_streak_length(day_log):
    start_streak = 0
    for char in day_log:
        if char == 'C':
            start_streak += 1
        else:
            break
    return start_streak


def _update_overall_with_combined(overall_max_streak, streak_from_prev_day, start_streak):
    combined_streak = streak_from_prev_day + start_streak
    if combined_streak > overall_max_streak:
        overall_max_streak = combined_streak
    return overall_max_streak


def _trailing_streak_length(day_log):
    end_streak = 0
    for char in reversed(day_log):
        if char == 'C':
            end_streak += 1
        else:
            break
    return end_streak


def _next_carryover_streak(day_log, streak_from_prev_day, start_streak):
    if start_streak == len(day_log) and len(day_log) > 0:
        return streak_from_prev_day + len(day_log)
    return _trailing_streak_length(day_log)


def _process_day(day_log, max_daily_streak, overall_max_streak, streak_from_prev_day):
    longest_in_day = _longest_streak_in_day(day_log)
    max_daily_streak, overall_max_streak = _update_max_streaks(
        max_daily_streak, overall_max_streak, longest_in_day
    )
    start_streak = _start_streak_length(day_log)
    overall_max_streak = _update_overall_with_combined(
        overall_max_streak, streak_from_prev_day, start_streak
    )
    streak_from_prev_day = _next_carryover_streak(
        day_log, streak_from_prev_day, start_streak
    )
    return max_daily_streak, overall_max_streak, streak_from_prev_day


def _process_days(n):
    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0
    for _ in range(n):
        day_log = _read_day_log()
        result = _process_day(
            day_log, max_daily_streak, overall_max_streak, streak_from_prev_day
        )
        max_daily_streak, overall_max_streak, streak_from_prev_day = result
    return max_daily_streak, overall_max_streak


def _print_results(max_daily_streak, overall_max_streak):
    print(f"{max_daily_streak} {overall_max_streak}")


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    """
    n = _read_day_count()
    if n is None:
        return
    max_daily_streak, overall_max_streak = _process_days(n)
    _print_results(max_daily_streak, overall_max_streak)


solve()
```

- Extracted input reading into `_read_day_count` and `_read_day_log`, preserving the original exception handling and stdin read order.
- Split each computation step into focused helpers: daily longest streak, starting streak, trailing streak, carryover streak, and max-streak updates.
- Moved per-day orchestration into `_process_day` and multi-day orchestration into `_process_days`, keeping each function short and single-purpose.
- Moved output printing into `_print_results` to separate side effects from computation.
- Kept the public `solve()` signature and runtime behavior unchanged.