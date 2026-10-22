import sys


def read_number_of_days():
    """
    Reads and parses the number of days from standard input.
    Returns None if input is empty or invalid.
    """
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None


def read_day_logs(num_days):
    """
    Reads N day logs from standard input.
    Returns a list of stripped day log strings.
    """
    return [sys.stdin.readline().strip() for _ in range(num_days)]


def calculate_longest_streak_in_day(day_log):
    """
    Calculates the longest coding streak contained entirely within a single day.
    Returns the length of the longest streak.
    """
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


def calculate_start_streak(day_log):
    """
    Calculates the length of the coding streak at the beginning of a day.
    Returns the length of the starting streak.
    """
    start_streak = 0
    for char in day_log:
        if char == 'C':
            start_streak += 1
        else:
            break
    return start_streak


def calculate_end_streak(day_log):
    """
    Calculates the length of the coding streak at the end of a day.
    Returns the length of the ending streak.
    """
    end_streak = 0
    for char in reversed(day_log):
        if char == 'C':
            end_streak += 1
        else:
            break
    return end_streak


def process_day_logs(day_logs):
    """
    Processes all day logs to calculate the maximum daily streak (X)
    and the overall maximum streak (Y).
    Returns a tuple (max_daily_streak, overall_max_streak).
    """
    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for day_log in day_logs:
        # Calculate the longest streak within the current day
        longest_in_day = calculate_longest_streak_in_day(day_log)
        
        # Update max_daily_streak (X)
        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day
        
        # Update overall_max_streak (Y) with within-day streak
        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day
        
        # Handle streaks that span across midnight
        start_streak = calculate_start_streak(day_log)
        combined_streak = streak_from_prev_day + start_streak
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak
        
        # Prepare for next day's calculation
        if start_streak == len(day_log) and len(day_log) > 0:
            streak_from_prev_day += len(day_log)
        else:
            streak_from_prev_day = calculate_end_streak(day_log)
    
    return max_daily_streak, overall_max_streak


def print_results(max_daily_streak, overall_max_streak):
    """
    Prints the calculated values for X and Y.
    """
    print(f"{max_daily_streak} {overall_max_streak}")


def solve():
    """
    Solves the Roy and Coding Streak problem by processing N days of activity logs.
    It calculates X, the maximum of the longest daily coding streaks, and
    Y, the absolute longest coding streak across all N days.
    """
    num_days = read_number_of_days()
    if num_days is None:
        return
    
    day_logs = read_day_logs(num_days)
    max_daily_streak, overall_max_streak = process_day_logs(day_logs)
    print_results(max_daily_streak, overall_max_streak)


def main():
    """
    Main entry point for the program.
    """
    solve()


if __name__ == "__main__":
    main()
