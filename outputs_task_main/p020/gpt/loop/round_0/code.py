import sys


def read_prophesy():
    return sys.stdin.readline().strip()


def compute_apocalypse_date(prophesy):
    date_counts = {}
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(len(prophesy) - 9):
        candidate = prophesy[i : i + 10]

        if candidate[2] != '-' or candidate[5] != '-':
            continue

        dd_str = candidate[0:2]
        mm_str = candidate[3:5]
        yyyy_str = candidate[6:10]

        if not (dd_str.isdigit() and mm_str.isdigit() and yyyy_str.isdigit()):
            continue

        d = int(dd_str)
        m = int(mm_str)
        y = int(yyyy_str)

        if not (2013 <= y <= 2015):
            continue
        if not (1 <= m <= 12):
            continue
        if not (1 <= d <= days_in_month[m]):
            continue

        date_counts[candidate] = date_counts.get(candidate, 0) + 1

    return max(date_counts, key=date_counts.get)


def print_apocalypse_date(apocalypse_date):
    print(apocalypse_date)


def find_apocalypse_date():
    """
    Read a prophesy string, find its most frequent valid date, and print it.
    """
    prophesy = read_prophesy()
    apocalypse_date = compute_apocalypse_date(prophesy)
    print_apocalypse_date(apocalypse_date)


def main():
    find_apocalypse_date()


if __name__ == "__main__":
    main()
