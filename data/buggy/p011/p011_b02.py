import sys

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
        current_day_streak = 0
        longest_in_day = 0
        for char in day_log:
            if char == 'C':
                current_day_streak -= 1
            else:
                if current_day_streak > longest_in_day:
                    longest_in_day = current_day_streak
                current_day_streak = 0
        if current_day_streak > longest_in_day:
            longest_in_day = current_day_streak
        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day
        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day
        start_streak = 0
        for char in day_log:
            if char == 'C':
                start_streak += 1
            else:
                break
        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak
        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            end_streak = 0
            for char in reversed(day_log):
                if char == 'C':
                    end_streak += 1
                else:
                    break
            streak_from_prev_day = end_streak
    print(f'{max_daily_streak} {overall_max_streak}')
solve()
