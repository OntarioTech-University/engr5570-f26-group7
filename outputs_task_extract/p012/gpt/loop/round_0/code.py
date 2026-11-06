def read_lines():
    import sys

    input = sys.stdin.read
    data = input().splitlines()
    n = int(data[0])
    lines = data[1:]
    return lines


def max_streak_in_day(line):
    max_in_day = 0
    curr_streak = 0

    for ch in line:
        if ch == 'C':
            curr_streak += 1
            max_in_day = max(max_in_day, curr_streak)
        else:
            curr_streak = 0

    return max_in_day


def count_initial_cs(characters):
    count = 0
    for ch in characters:
        if ch == 'C':
            count += 1
        else:
            break
    return count


def compute_maxima(lines):
    x = 0
    y = 0
    prev_trailing_c = 0

    for line in lines:
        max_in_day = max_streak_in_day(line)
        x = max(x, max_in_day)
        leading_c = count_initial_cs(line)
        trailing_c = count_initial_cs(reversed(line))

        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)

        y = max(y, max_in_day)
        prev_trailing_c = trailing_c

    return x, y


def print_results(x, y):
    print(x, y)


def main():
    lines = read_lines()
    x, y = compute_maxima(lines)
    print_results(x, y)


if __name__ == "__main__":
    main()
