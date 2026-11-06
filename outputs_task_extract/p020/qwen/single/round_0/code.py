import sys


def _read_prophesy():
    return sys.stdin.readline().strip()


def _get_days_in_month():
    return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _iter_date_candidates(prophesy):
    for i in range(len(prophesy) - 9):
        yield prophesy[i:i + 10]


def _has_valid_format(candidate):
    return candidate[2] == '-' and candidate[5] == '-'


def _extract_date_parts(candidate):
    return candidate[0:2], candidate[3:5], candidate[6:10]


def _has_digit_parts(dd_str, mm_str, yyyy_str):
    return dd_str.isdigit() and mm_str.isdigit() and yyyy_str.isdigit()


def _parse_date_parts(dd_str, mm_str, yyyy_str):
    return int(dd_str), int(mm_str), int(yyyy_str)


def _is_valid_year(year):
    return 2013 <= year <= 2015


def _is_valid_month(month):
    return 1 <= month <= 12


def _is_valid_day(day, month, days_in_month):
    return 1 <= day <= days_in_month[month]


def _is_valid_date(candidate, days_in_month):
    if not _has_valid_format(candidate):
        return False

    dd_str, mm_str, yyyy_str = _extract_date_parts(candidate)

    if not _has_digit_parts(dd_str, mm_str, yyyy_str):
        return False

    day, month, year = _parse_date_parts(dd_str, mm_str, yyyy_str)

    return (
        _is_valid_year(year)
        and _is_valid_month(month)
        and _is_valid_day(day, month, days_in_month)
    )


def _increment_date_count(date_counts, candidate):
    date_counts[candidate] = date_counts.get(candidate, 0) + 1


def _count_valid_dates(prophesy):
    date_counts = {}
    days_in_month = _get_days_in_month()

    for candidate in _iter_date_candidates(prophesy):
        if _is_valid_date(candidate, days_in_month):
            _increment_date_count(date_counts, candidate)

    return date_counts


def _find_most_frequent_date(date_counts):
    return max(date_counts, key=date_counts.get)


def _print_apocalypse_date(apocalypse_date):
    print(apocalypse_date)


def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    prophesy = _read_prophesy()
    date_counts = _count_valid_dates(prophesy)
    apocalypse_date = _find_most_frequent_date(date_counts)
    _print_apocalypse_date(apocalypse_date)


if __name__ == "__main__":
    find_apocalypse_date()
