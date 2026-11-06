def read_input_lines():
    import sys
    return sys.stdin.read().splitlines()


def max_c_streak_in_line(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            max_in_day = max(max_in_day, curr_streak)
        else:
            curr_streak = 0

    return max_in_day


def count_initial_c_streak(chars):
    count = 0

    for ch in chars:
        if ch == 'C':
            count += 1
        else:
            break

    return count


def compute_max_streaks(data):
    n = int(data[0])
    lines = data[1:]

    x = 0  # Max within a single day
    y = 0  # Max across multiple days

    prev_trailing_c = 0  # Trailing C's from previous day

    for line in lines:
        max_in_day = max_c_streak_in_line(line)
        x = max(x, max_in_day)

        leading_c = count_initial_c_streak(line)
        trailing_c = count_initial_c_streak(reversed(line))

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)

        y = max(y, max_in_day)

        prev_trailing_c = trailing_c

    return x, y


def print_results(x, y):
    print(x, y)


def main():
    data = read_input_lines()
    x, y = compute_max_streaks(data)
    print_results(x, y)


if __name__ == "__main__":
    main()
