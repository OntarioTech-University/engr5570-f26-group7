import sys


def _read_num_days():
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None


def _read_day_log():
    return sys.stdin.readline().strip()


def _read_day_logs(num_days):
    return (_read_day_log() for _ in range(num_days))


def _longest_coding_streak_in_day(day_log):
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


def _consecutive_coding_streak(day_log, reverse=False):
    streak = 0
    chars = reversed(day_log) if reverse else day_log

    for char in chars:
        if char == 'C':
            streak += 1
        else:
            break

    return streak


def _leading_coding_streak(day_log):
    return _consecutive_coding_streak(day_log)


def _trailing_coding_streak(day_log):
    return _consecutive_coding_streak(day_log, reverse=True)


def _compute_streaks(day_logs):
    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for day_log in day_logs:
        longest_in_day = _longest_coding_streak_in_day(day_log)

        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day

        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day

        start_streak = _leading_coding_streak(day_log)

        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            streak_from_prev_day = _trailing_coding_streak(day_log)

    return max_daily_streak, overall_max_streak


def _print_results(max_daily_streak, overall_max_streak):
    print(f"{max_daily_streak} {overall_max_streak}")


def main():
    num_days = _read_num_days()
    if num_days is None:
        return

    day_logs = _read_day_logs(num_days)
    max_daily_streak, overall_max_streak = _compute_streaks(day_logs)
    _print_results(max_daily_streak, overall_max_streak)


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    It calculates X, the maximum of the longest daily coding streaks, and
    Y, the absolute longest coding streak across all N days.
    """
    main()


if __name__ == "__main__":
    main()
