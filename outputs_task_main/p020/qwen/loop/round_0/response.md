```python
import sys


def _read_prophesy():
    return sys.stdin.readline().strip()


def _is_valid_date(candidate, days_in_month):
    if candidate[2] != '-' or candidate[5] != '-':
        return False

    dd_str = candidate[0:2]
    mm_str = candidate[3:5]
    yyyy_str = candidate[6:10]

    if not (dd_str.isdigit() and mm_str.isdigit() and yyyy_str.isdigit()):
        return False

    d = int(dd_str)
    m = int(mm_str)
    y = int(yyyy_str)

    if not (2013 <= y <= 2015):
        return False

    if not (1 <= m <= 12):
        return False

    if not (1 <= d <= days_in_month[m]):
        return False

    return True


def _count_valid_dates(prophesy):
    date_counts = {}
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    n = len(prophesy)

    for i in range(n - 9):
        candidate = prophesy[i : i + 10]
        if _is_valid_date(candidate, days_in_month):
            date_counts[candidate] = date_counts.get(candidate, 0) + 1

    return date_counts


def _find_most_frequent_date(date_counts):
    return max(date_counts, key=date_counts.get)


def _print_apocalypse_date(apocalypse_date):
    print(apocalypse_date)


def main():
    prophesy = _read_prophesy()
    date_counts = _count_valid_dates(prophesy)
    apocalypse_date = _find_most_frequent_date(date_counts)
    _print_apocalypse_date(apocalypse_date)


def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    main()


if __name__ == "__main__":
    main()
```

- Added a `main()` function and moved script execution under `if __name__ == "__main__":` so no program logic runs at import time.
- Extracted input reading into `_read_prophesy()` and output printing into `_print_apocalypse_date()` to separate I/O from processing.
- Moved the scanning/counting logic into `_count_valid_dates()` and the per-candidate validation into `_is_valid_date()` so the validation rules are maintained in one shared place.
- Extracted selection of the most frequent date into `_find_most_frequent_date()` so `main()` explicitly passes data between input, computation, and output steps.
- Preserved the public `find_apocalypse_date()` signature and observable behavior by keeping it as a thin wrapper around the new pipeline.