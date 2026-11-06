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


def solve(prophesy):
    date_count = _count_valid_dates(prophesy)
    return _first_date_with_max_count(date_count)


def _count_valid_dates(prophesy):
    date_count = {}

    # Check every possible 10-character substring
    for i in range(len(prophesy) - 9):
        substring = prophesy[i:i + 10]

        # Check if it matches dd-mm-yyyy pattern
        if _has_date_format(substring):
            try:
                day, month, year = _parse_date_fields(substring)

                # Check if it's a valid date
                if is_valid_date(day, month, year):
                    _increment_date_count(date_count, substring)
            except ValueError:
                continue

    return date_count


def _has_date_format(substring):
    return len(substring) == 10 and substring[2] == '-' and substring[5] == '-'


def _parse_date_fields(substring):
    day = int(substring[0:2])
    month = int(substring[3:5])
    year = int(substring[6:10])
    return day, month, year


def _increment_date_count(date_count, date_str):
    date_count[date_str] = date_count.get(date_str, 0) + 1


def _first_date_with_max_count(date_count):
    # Find the date with maximum count
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date


def _read_input():
    return input().strip()


def _print_output(result):
    print(result)


def main():
    prophesy = _read_input()
    result = solve(prophesy)
    _print_output(result)


if __name__ == "__main__":
    main()
```

- Moved the top-level input/output code into `_read_input()`, `_print_output()`, and `main()`, then guarded execution with `if __name__ == "__main__":` so importing the module no longer runs program logic.
- Removed the top-level `prophesy` variable, eliminating global state while preserving the same data flow through parameters and return values.
- Kept public function names and signatures unchanged: `is_valid_date(day, month, year)` and `solve(prophesy)`.
- Extracted date-format checking, parsing, counting, and max-count selection into small helper functions to improve structure and avoid repeated inline logic.
- Preserved original behavior exactly, including the `ValueError` handling during parsing, the first-inserted tie-breaking order for maximum counts, and the exception raised when no valid dates are found.