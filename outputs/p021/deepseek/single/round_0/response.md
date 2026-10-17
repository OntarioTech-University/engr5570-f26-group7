```python
def is_valid_date(day, month, year):
    if year < 2013 or year > 2015:
        return False
    if month < 1 or month > 12:
        return False
    
    # Days in each month for non-leap years
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    max_days = days_in_month[month - 1]
    
    return 1 <= day <= max_days


def _extract_date_parts(substring):
    """Parse a dd-mm-yyyy formatted string into (day, month, year) or None."""
    if len(substring) != 10 or substring[2] != '-' or substring[5] != '-':
        return None
    
    try:
        day = int(substring[0:2])
        month = int(substring[3:5])
        year = int(substring[6:10])
        return day, month, year
    except ValueError:
        return None


def _count_valid_dates(prophesy):
    """Count occurrences of valid dd-mm-yyyy dates in the string."""
    date_count = {}
    
    for i in range(len(prophesy) - 9):
        substring = prophesy[i:i+10]
        date_parts = _extract_date_parts(substring)
        
        if date_parts is None:
            continue
        
        day, month, year = date_parts
        if is_valid_date(day, month, year):
            date_count[substring] = date_count.get(substring, 0) + 1
    
    return date_count


def _find_most_frequent_date(date_count):
    """Return the date with the highest count from the dictionary."""
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date


def solve(prophesy):
    date_count = _count_valid_dates(prophesy)
    return _find_most_frequent_date(date_count)


# Read input and solve
prophesy = input().strip()
print(solve(prophesy))
```