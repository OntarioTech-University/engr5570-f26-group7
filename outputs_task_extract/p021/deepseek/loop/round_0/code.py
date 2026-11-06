def is_valid_date(day, month, year):
    if year < 2013 or year > 2015:
        return False
    if month < 1 or month > 12:
        return False

    # Days in each month for non-leap years
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    max_days = days_in_month[month - 1]

    return 1 <= day <= max_days


def _has_date_pattern(substring):
    return len(substring) == 10 and substring[2] == '-' and substring[5] == '-'


def _parse_date_parts(substring):
    try:
        day = int(substring[0:2])
        month = int(substring[3:5])
        year = int(substring[6:10])
    except ValueError:
        return None

    return day, month, year


def _iter_10_char_substrings(prophesy):
    for i in range(len(prophesy) - 9):
        yield prophesy[i:i + 10]


def _count_valid_dates(prophesy):
    date_count = {}

    for substring in _iter_10_char_substrings(prophesy):
        if not _has_date_pattern(substring):
            continue

        date_parts = _parse_date_parts(substring)
        if date_parts is None:
            continue

        day, month, year = date_parts
        if is_valid_date(day, month, year):
            date_count[substring] = date_count.get(substring, 0) + 1

    return date_count


def _find_most_frequent_date(date_count):
    max_count = max(date_count.values())

    for date, count in date_count.items():
        if count == max_count:
            return date


def solve(prophesy):
    date_count = _count_valid_dates(prophesy)
    return _find_most_frequent_date(date_count)


def read_input():
    return input().strip()


def print_output(result):
    print(result)


def main():
    prophesy = read_input()
    result = solve(prophesy)
    print_output(result)


main()
