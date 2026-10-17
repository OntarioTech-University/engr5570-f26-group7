Here's the refactored code:

```python
import sys

DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MIN_YEAR = 2013
MAX_YEAR = 2015
DATE_LENGTH = 10

def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    prophesy = sys.stdin.readline().strip()
    date_counts = count_valid_dates(prophesy)
    apocalypse_date = find_most_frequent_date(date_counts)
    print(apocalypse_date)

def count_valid_dates(prophesy):
    """Count occurrences of all valid dates in the prophesy string."""
    date_counts = {}
    
    for i in range(len(prophesy) - DATE_LENGTH + 1):
        candidate = prophesy[i : i + DATE_LENGTH]
        if is_valid_date(candidate):
            date_counts[candidate] = date_counts.get(candidate, 0) + 1
    
    return date_counts

def is_valid_date(candidate):
    """Check if a string represents a valid date in dd-mm-yyyy format."""
    if not has_valid_format(candidate):
        return False
    
    day, month, year = parse_date_parts(candidate)
    return is_valid_date_components(day, month, year)

def has_valid_format(candidate):
    """Check if the string has the correct format with hyphens in the right positions."""
    return candidate[2] == '-' and candidate[5] == '-'

def parse_date_parts(candidate):
    """Extract and convert date components from the candidate string."""
    day_str = candidate[0:2]
    month_str = candidate[3:5]
    year_str = candidate[6:10]
    
    if not (day_str.isdigit() and month_str.isdigit() and year_str.isdigit()):
        return None, None, None
    
    return int(day_str), int(month_str), int(year_str)

def is_valid_date_components(day, month, year):
    """Validate date components against the given rules."""
    if day is None or month is None or year is None:
        return False
    
    if not (MIN_YEAR <= year <= MAX_YEAR):
        return False
    
    if not (1 <= month <= 12):
        return False
    
    return 1 <= day <= DAYS_IN_MONTH[month]

def find_most_frequent_date(date_counts):
    """Find the date with the highest occurrence count."""
    return max(date_counts, key=date_counts.get)

# Standard entry point for the script.
if __name__ == "__main__":
    find_apocalypse_date()
```

**Changes made:**

- **Extracted constants**: Moved magic numbers (`DAYS_IN_MONTH`, `MIN_YEAR`, `MAX_YEAR`, `DATE_LENGTH`) to module-level constants for better readability and maintainability.
- **Split into smaller functions**: Broke down the monolithic `find_apocalypse_date()` into focused functions: `count_valid_dates()`, `is_valid_date()`, `has_valid_format()`, `parse_date_parts()`, `is_valid_date_components()`, and `find_most_frequent_date()`.
- **Simplified conditional logic**: Replaced deeply nested conditionals with early returns and guard clauses, making the validation flow clearer and easier to follow.
- **Improved function naming**: Each function now has a clear, descriptive name that indicates its specific responsibility.
- **Reduced complexity**: The main function now orchestrates the flow at a higher level, while each helper function handles one specific aspect of the date validation process.