def read_input():
    import sys
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    lines = data[1:]
    return n, lines


def max_consecutive_c(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            if curr_streak > max_in_day:
                max_in_day = curr_streak
        else:
            curr_streak = 0

    return max_in_day


def _count_edge_c(line, reverse=False):
    chars = reversed(line) if reverse else line
    count = 0

    for ch in chars:
        if ch == 'C':
            count += 1
        else:
            break

    return count


def count_leading_c(line):
    return _count_edge_c(line, reverse=False)


def count_trailing_c(line):
    return _count_edge_c(line, reverse=True)


def compute_streaks(lines):
    max_single_day = 0
    max_multi_day = 0
    prev_trailing_c = 0

    for line in lines:
        max_in_day = max_consecutive_c(line)

        if max_in_day > max_single_day:
            max_single_day = max_in_day

        leading_c = count_leading_c(line)
        trailing_c = count_trailing_c(line)

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            if combined > max_multi_day:
                max_multi_day = combined

        if max_in_day > max_multi_day:
            max_multi_day = max_in_day

        prev_trailing_c = trailing_c

    return max_single_day, max_multi_day


def print_streaks(max_single_day, max_multi_day):
    print(max_single_day, max_multi_day)


def main():
    _, lines = read_input()
    max_single_day, max_multi_day = compute_streaks(lines)
    print_streaks(max_single_day, max_multi_day)


if __name__ == "__main__":
    main()
