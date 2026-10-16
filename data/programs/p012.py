def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    lines = data[1:]
    
    x = 0  # Max within a single day
    y = 0  # Max across multiple days
    
    prev_trailing_c = 0  # Trailing C's from previous day
    
    for line in lines:
        # Find max streak within this day
        max_in_day = 0
        curr_streak = 0
        
        for ch in line:
            if ch == 'C':
                curr_streak += 1
                max_in_day = max(max_in_day, curr_streak)
            else:
                curr_streak = 0
        
        x = max(x, max_in_day)
        
        # Now process for across-day streaks
        # Count leading C's
        leading_c = 0
        for ch in line:
            if ch == 'C':
                leading_c += 1
            else:
                break
        
        # Count trailing C's
        trailing_c = 0
        for ch in reversed(line):
            if ch == 'C':
                trailing_c += 1
            else:
                break
        
        # Combine with previous day's trailing C's
        if prev_trailing_c > 0 and leading_c > 0:
            combined = prev_trailing_c + leading_c
            y = max(y, combined)
        
        # Also consider max_in_day itself for Y
        y = max(y, max_in_day)
        
        prev_trailing_c = trailing_c
    
    print(x, y)

if __name__ == "__main__":
    main()
