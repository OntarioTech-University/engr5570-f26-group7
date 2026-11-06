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
    return _find_most_frequent_date(date_count)


def _count_valid_dates(prophesy):
    date_count = {}
    for substring in _date_substrings(prophesy):
        if _has_date_format(substring):
            _add_date_if_valid(substring, date_count)
    return date_count


def _date_substrings(prophesy):
    for i in range(len(prophesy) - 9):
        yield prophesy[i:i + 10]


def _has_date_format(substring):
    return len(substring) == 10 and substring[2] == '-' and substring[5] == '-'


def _add_date_if_valid(substring, date_count):
    try:
        day, month, year = _parse_date(substring)
        if is_valid_date(day, month, year):
            _increment_date_count(date_count, substring)
    except ValueError:
        return


def _parse_date(substring):
    day = int(substring[0:2])
    month = int(substring[3:5])
    year = int(substring[6:10])
    return day, month, year


def _increment_date_count(date_count, date_str):
    date_count[date_str] = date_count.get(date_str, 0) + 1


def _find_most_frequent_date(date_count):
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date


def _read_prophesy():
    return input().strip()


def _print_result(result):
    print(result)


def _main():
    prophesy = _read_prophesy()
    result = solve(prophesy)
    _print_result(result)


_main()
```

- Kept `is_valid_date` and `solve` signatures unchanged to preserve the public interface.
- Split the counting logic from `solve` into `_count_valid_dates`, keeping `solve` as a short orchestrator.
- Extracted candidate substring generation into `_date_substrings` and format checking into `_has_date_format`.
- Moved parsing, validation/counting, and count incrementing into `_parse_date`, `_add_date_if_valid`, and `_increment_date_count`.
- Extracted selection of the most frequent date into `_find_most_frequent_date`, preserving the original tie-breaking order.
- Moved input reading and output printing into `_read_prophesy` and `_print_result`, with `_main` handling the top-level flow.