import sys

def read_number_of_days():
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None

def read_day_log():
    return sys.stdin.readline().strip()

def compute_longest_streak_in_day(day_log):
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

def compute_start_streak(day_log):
    start_streak = 0
    for char in day_log:
        if char == 'C':
            start_streak += 1
        else:
            break
    return start_streak

def compute_end_streak(day_log):
    end_streak = 0
    for char in reversed(day_log):
        if char == 'C':
            end_streak += 1
        else:
            break
    return end_streak

def compute_carry_over_streak(day_log, streak_from_prev_day, start_streak):
    if start_streak == len(day_log) and len(day_log) > 0:
        return streak_from_prev_day + len(day_log)
    return compute_end_streak(day_log)

def update_maxima(max_daily_streak, overall_max_streak, longest_in_day, combined_streak):
    if longest_in_day > max_daily_streak:
        max_daily_streak = longest_in_day
    if longest_in_day > overall_max_streak:
        overall_max_streak = longest_in_day
    if combined_streak > overall_max_streak:
        overall_max_streak = combined_streak
    return max_daily_streak, overall_max_streak

def process_day(day_log, streak_from_prev_day, max_daily_streak, overall_max_streak):
    longest_in_day = compute_longest_streak_in_day(day_log)
    start_streak = compute_start_streak(day_log)
    combined_streak = streak_from_prev_day + start_streak

    max_daily_streak, overall_max_streak = update_maxima(
        max_daily_streak, overall_max_streak, longest_in_day, combined_streak
    )

    new_streak_from_prev_day = compute_carry_over_streak(
        day_log, streak_from_prev_day, start_streak
    )

    return max_daily_streak, overall_max_streak, new_streak_from_prev_day

def print_result(max_daily_streak, overall_max_streak):
    print(f"{max_daily_streak} {overall_max_streak}")

def solve():
    N = read_number_of_days()
    if N is None:
        return

    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for _ in range(N):
        day_log = read_day_log()
        max_daily_streak, overall_max_streak, streak_from_prev_day = process_day(
            day_log, streak_from_prev_day, max_daily_streak, overall_max_streak
        )

    print_result(max_daily_streak, overall_max_streak)

solve()
