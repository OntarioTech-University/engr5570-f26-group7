import sys


def read_input():
    days = int(sys.stdin.readline())
    return (sys.stdin.readline().strip() for _ in range(days))


def count_initial_streak(characters):
    streak = 0
    for char in characters:
        if char == 'C':
            streak += 1
        else:
            break
    return streak


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


def calculate_streaks(day_logs):
    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for day_log in day_logs:
        longest_in_day = longest_daily_streak(day_log)

        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day

        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day

        start_streak = count_initial_streak(day_log)
        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            streak_from_prev_day = count_initial_streak(reversed(day_log))

    return max_daily_streak, overall_max_streak


def print_output(max_daily_streak, overall_max_streak):
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
    print_output(max_daily_streak, overall_max_streak)


def main():
    solve()


if __name__ == "__main__":
    main()
