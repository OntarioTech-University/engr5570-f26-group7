```python
import sys


def _is_valid_date(candidate, days_in_month):
    """
    Return True if candidate is a valid date string in the "dd-mm-yyyy" format
    according to the rules used by find_apocalypse_date.
    """
    # 1. Check the basic format: "xx-xx-xxxx"
    # The hyphens must be in the correct positions.
    if candidate[2] != '-' or candidate[5] != '-':
        return False

    # 2. Extract day, month, and year parts.
    dd_str = candidate[0:2]
    mm_str = candidate[3:5]
    yyyy_str = candidate[6:10]

    # 3. Check if all parts are composed of digits.
    if not (dd_str.isdigit() and mm_str.isdigit() and yyyy_str.isdigit()):
        return False

    # 4. Convert parts to integers for numerical validation.
    d = int(dd_str)
    m = int(mm_str)
    y = int(yyyy_str)

    # 5. Validate the date against the given rules.
    # Year must be between 2013 and 2015.
    if not (2013 <= y <= 2015):
        return False

    # Month must be between 1 and 12.
    if not (1 <= m <= 12):
        return False

    # Day must be valid for the given month.
    if not (1 <= d <= days_in_month[m]):
        return False

    return True


def _count_valid_dates(prophesy):
    """
    Scan prophesy and return a dictionary mapping each valid date substring
    to the number of times it appears.
    """
    # Days in each month for a non-leap year (years 2013-2015).
    # Index 0 is a placeholder to allow for 1-based month indexing.
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # A dictionary to store the frequency of each valid date found.
    # Key: date string "dd-mm-yyyy", Value: count
    date_counts = {}

    n = len(prophesy)

    # Iterate through the prophesy string to find all possible 10-character
    # substrings that could represent a date in the "dd-mm-yyyy" format.
    for i in range(n - 9):
        # Extract a potential date substring of length 10.
        candidate = prophesy[i : i + 10]

        if _is_valid_date(candidate, days_in_month):
            date_counts[candidate] = date_counts.get(candidate, 0) + 1

    return date_counts


def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    prophesy = sys.stdin.readline().strip()

    date_counts = _count_valid_dates(prophesy)

    # The problem guarantees that a unique apocalypse date exists.
    # Find the date (key) with the highest count (value) in the dictionary.
    apocalypse_date = max(date_counts, key=date_counts.get)

    print(apocalypse_date)


# Standard entry point for the script.
if __name__ == "__main__":
    find_apocalypse_date()
```

- Extracted date validation into `_is_valid_date` to reduce clutter in the main loop while preserving the exact validation order and rules.
- Extracted scanning and frequency counting into `_count_valid_dates` so `find_apocalypse_date` focuses only on input, selecting the maximum, and printing.
- Kept the public function `find_apocalypse_date` signature and observable behavior unchanged.
- Preserved the original dictionary-based counting and `max(..., key=date_counts.get)` behavior, including tie ordering and exception behavior for empty input.