import sys


def read_day_count():
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None


def read_day_log():
    return sys.stdin.readline().strip()


def longest_daily_streak(day_log):
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


def leading_streak(day_log):
    streak = 0
    for char in day_log:
        if char == 'C':
            streak += 1
        else:
            break
    return streak


def trailing_streak(day_log):
    streak = 0
    for char in reversed(day_log):
        if char == 'C':
            streak += 1
        else:
            break
    return streak


def next_carryover_streak(day_log, start_streak, previous_streak):
    if start_streak == len(day_log) and len(day_log) > 0:
        return previous_streak + len(day_log)
    return trailing_streak(day_log)


def process_day(day_log, max_daily_streak, overall_max_streak, previous_streak):
    longest_in_day = longest_daily_streak(day_log)
    if longest_in_day > max_daily_streak:
        max_daily_streak = longest_in_day
    if longest_in_day > overall_max_streak:
        overall_max_streak = longest_in_day
    start_streak = leading_streak(day_log)
    combined_streak = previous_streak + start_streak
    if combined_streak > overall_max_streak:
        overall_max_streak = combined_streak
    carryover = next_carryover_streak(day_log, start_streak, previous_streak)
    return max_daily_streak, overall_max_streak, carryover


def print_result(max_daily_streak, overall_max_streak):
    print(f"{max_daily_streak} {overall_max_streak}")


def solve():
    """Calculate the longest daily and overall coding streaks."""
    N = read_day_count()
    if N is None:
        return

    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0
    for _ in range(N):
        day_log = read_day_log()
        max_daily_streak, overall_max_streak, streak_from_prev_day = process_day(
            day_log, max_daily_streak, overall_max_streak, streak_from_prev_day
        )
    print_result(max_daily_streak, overall_max_streak)


solve()
