import sys


def read_num_days():
    """
    Reads the number of days from standard input.
    Returns None if the input is empty or not a valid integer.
    """
    try:
        return int(sys.stdin.readline())
    except (ValueError, IndexError):
        return None


def read_day_log():
    """Reads and returns a single day's activity log, stripped of whitespace."""
    return sys.stdin.readline().strip()


def longest_streak(day_log):
    """Returns the length of the longest consecutive 'C' streak in day_log."""
    current = 0
    longest = 0
    for char in day_log:
        if char == 'C':
            current += 1
        else:
            if current > longest:
                longest = current
            current = 0
    if current > longest:
        longest = current
    return longest


def prefix_streak(day_log):
    """Returns the number of consecutive 'C' characters at the start of day_log."""
    count = 0
    for char in day_log:
        if char == 'C':
            count += 1
        else:
            break
    return count


def suffix_streak(day_log):
    """Returns the number of consecutive 'C' characters at the end of day_log."""
    count = 0
    for char in reversed(day_log):
        if char == 'C':
            count += 1
        else:
            break
    return count


def compute_day_stats(day_log, streak_from_prev_day):
    """
    Computes statistics for a single day.

    Returns:
        longest_in_day: longest streak entirely within the day
        combined_streak: streak from previous day plus start-of-day streak
        new_streak_from_prev_day: streak to carry into the next day
    """
    longest_in_day = longest_streak(day_log)
    start_streak = prefix_streak(day_log)
    combined_streak = streak_from_prev_day + start_streak

    if start_streak == len(day_log) and len(day_log) > 0:
        new_streak_from_prev_day = streak_from_prev_day + len(day_log)
    else:
        new_streak_from_prev_day = suffix_streak(day_log)

    return longest_in_day, combined_streak, new_streak_from_prev_day


def print_result(max_daily_streak, overall_max_streak):
    """Prints the final X and Y values."""
    print(f"{max_daily_streak} {overall_max_streak}")


def main():
    """Main program flow: read input, compute, and print output."""
    n = read_num_days()
    if n is None:
        return

    max_daily_streak = 0
    overall_max_streak = 0
    streak_from_prev_day = 0

    for _ in range(n):
        day_log = read_day_log()
        longest_in_day, combined_streak, streak_from_prev_day = compute_day_stats(
            day_log, streak_from_prev_day
        )

        if longest_in_day > max_daily_streak:
            max_daily_streak = longest_in_day
        if longest_in_day > overall_max_streak:
            overall_max_streak = longest_in_day
        if combined_streak > overall_max_streak:
            overall_max_streak = combined_streak

    print_result(max_daily_streak, overall_max_streak)


def solve():
    """Backward-compatible wrapper for the original public solve() function."""
    main()


if __name__ == "__main__":
    main()
