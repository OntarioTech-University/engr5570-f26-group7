import sys


def _read_prophesy():
    return sys.stdin.readline().strip()


def _has_valid_format(candidate):
    if candidate[2] != '-' or candidate[5] != '-':
        return False

    dd_str = candidate[0:2]
    mm_str = candidate[3:5]
    yyyy_str = candidate[6:10]
    return dd_str.isdigit() and mm_str.isdigit() and yyyy_str.isdigit()


def _has_valid_date_values(candidate, days_in_month):
    d = int(candidate[0:2])
    m = int(candidate[3:5])
    y = int(candidate[6:10])

    if not (2013 <= y <= 2015):
        return False
    if not (1 <= m <= 12):
        return False
    return 1 <= d <= days_in_month[m]


def _count_valid_dates(prophesy):
    date_counts = {}
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(len(prophesy) - 9):
        candidate = prophesy[i : i + 10]
        if not _has_valid_format(candidate):
            continue
        if not _has_valid_date_values(candidate, days_in_month):
            continue
        date_counts[candidate] = date_counts.get(candidate, 0) + 1

    return date_counts


def _most_frequent_date(date_counts):
    return max(date_counts, key=date_counts.get)


def _print_date(date):
    print(date)


def find_apocalypse_date():
    """Read a prophesy and print its most frequently occurring valid date."""
    prophesy = _read_prophesy()
    date_counts = _count_valid_dates(prophesy)
    apocalypse_date = _most_frequent_date(date_counts)
    _print_date(apocalypse_date)


if __name__ == "__main__":
    find_apocalypse_date()
