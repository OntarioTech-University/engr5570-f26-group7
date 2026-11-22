def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    n = int(data[0])
    lines = data[1:]
    x = 0
    y = 0
    prev_trailing_c = 0
    for line in lines:
        max_in_day = 0
        curr_streak = 0
        for ch in line:
            if ch == 'C':
                curr_streak += 1
                max_in_day = max(max_in_day, curr_streak)
            else:
                curr_streak = 0
        x = max(x, max_in_day)
        leading_c = 0
        for ch in line:
            if ch != 'C':
                leading_c += 1
            else:
                break
        trailing_c = 0
        for ch in reversed(line):
            if ch == 'C':
                trailing_c += 1
            else:
                break
        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)
        y = max(y, max_in_day)
        prev_trailing_c = trailing_c
    print(x, y)
if __name__ == '__main__':
    main()
