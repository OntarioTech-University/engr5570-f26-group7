```python
import sys

DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def read_prophesy():
    return sys.stdin.readline().strip()


def has_valid_format(candidate):
    if candidate[2] != '-' or candidate[5] != '-':
        return False
    return (
        candidate[0:2].isdigit()
        and candidate[3:5].isdigit()
        and candidate[6:10].isdigit()
    )


def parse_date_parts(candidate):
    return int(candidate[0:2]), int(candidate[3:5]), int(candidate[6:10])


def is_valid_calendar_date(day, month, year):
    if not (2013 <= year <= 2015):
        return False
    if not (1 <= month <= 12):
        return False
    return 1 <= day <= DAYS_IN_MONTH[month]


def is_valid_date(candidate):
    if not has_valid_format(candidate):
        return False
    day, month, year = parse_date_parts(candidate)
    return is_valid_calendar_date(day, month, year)


def count_valid_dates(prophesy):
    date_counts = {}
    n = len(prophesy)

    for i in range(n - 9):
        candidate = prophesy[i : i + 10]
        if is_valid_date(candidate):
            date_counts[candidate] = date_counts.get(candidate, 0) + 1

    return date_counts


def find_most_frequent_date(date_counts):
    return max(date_counts, key=date_counts.get)


def print_apocalypse_date(date):
    print(date)


def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    prophesy = read_prophesy()
    date_counts = count_valid_dates(prophesy)
    apocalypse_date = find_most_frequent_date(date_counts)
    print_apocalypse_date(apocalypse_date)


if __name__ == "__main__":
    find_apocalypse_date()
```

- Extracted input reading into `read_prophesy()` to isolate I/O from computation.
- Moved the date format and digit validation into `has_valid_format()` and `parse_date_parts()` to keep each validation step small and focused.
- Separated calendar validation into `is_valid_calendar_date()` so date rules are independent from string parsing.
- Created `is_valid_date()` as a small orchestrator for the validation helpers.
- Moved the main counting loop into `count_valid_dates()` to separate iteration and aggregation from validation.
- Added `find_most_frequent_date()` and `print_apocalypse_date()` to isolate result selection and output.
- Kept `find_apocalypse_date()` as the public entry point, preserving its original signature and behavior.
- Introduced a module-level `DAYS_IN_MONTH` constant to avoid recreating the list on every call while preserving the original values.