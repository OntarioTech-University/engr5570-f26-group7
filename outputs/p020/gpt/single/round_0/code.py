import sys


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


def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    prophesy = sys.stdin.readline().strip()
    n = len(prophesy)
    date_counts = {}

    # Index 0 is a placeholder for 1-based month indexing.
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(n - 9):
        candidate = prophesy[i : i + 10]
        if _is_valid_date(candidate, days_in_month):
            date_counts[candidate] = date_counts.get(candidate, 0) + 1

    apocalypse_date = max(date_counts, key=date_counts.get)
    print(apocalypse_date)


if __name__ == "__main__":
    find_apocalypse_date()
