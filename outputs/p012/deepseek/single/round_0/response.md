```python
def main():
    import sys
    data = sys.stdin.read().splitlines()
    
    n = int(data[0])
    lines = data[1:]
    
    x = 0  # Max within a single day
    y = 0  # Max across multiple days
    
    prev_trailing_c = 0  # Trailing C's from previous day
    
    for line in lines:
        max_in_day = find_max_streak_in_day(line)
        x = max(x, max_in_day)
        
        leading_c = count_leading_c(line)
        trailing_c = count_trailing_c(line)
        
        y = update_cross_day_max(y, prev_trailing_c, leading_c, max_in_day)
        
        prev_trailing_c = trailing_c
    
    print(x, y)


def find_max_streak_in_day(line):
    """Find the maximum consecutive 'C' streak within a single day."""
    max_in_day = 0
    curr_streak = 0
    
    for ch in line:
        if ch == 'C':
            curr_streak += 1
            max_in_day = max(max_in_day, curr_streak)
        else:
            curr_streak = 0
    
    return max_in_day


def count_leading_c(line):
    """Count consecutive 'C' characters from the start of the line."""
    leading_c = 0
    for ch in line:
        if ch == 'C':
            leading_c += 1
        else:
            break
    return leading_c


def count_trailing_c(line):
    """Count consecutive 'C' characters from the end of the line."""
    trailing_c = 0
    for ch in reversed(line):
        if ch == 'C':
            trailing_c += 1
        else:
            break
    return trailing_c


def update_cross_day_max(y, prev_trailing_c, leading_c, max_in_day):
    """Update the cross-day maximum based on previous day's trailing and current day's leading C's."""
    if prev_trailing_c > 0 and leading_c > 0:
        combined = prev_trailing_c + leading_c
        y = max(y, combined)
    
    return max(y, max_in_day)


if __name__ == "__main__":
    main()
```

**Changes made:**

- **Extracted helper functions** for `find_max_streak_in_day`, `count_leading_c`, `count_trailing_c`, and `update_cross_day_max` to break the monolithic loop into smaller, well-named units.
- **Simplified the main loop** by delegating each logical step to a dedicated function, making the flow easier to follow.
- **Removed redundant comments** that described what the code was doing, replacing them with descriptive function names and docstrings.
- **Preserved all behavior** including input parsing, variable names, output format, and edge-case handling (e.g., empty lines, all non-'C' characters).