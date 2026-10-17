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


def _parse_date(substring):
    day = int(substring[0:2])
    month = int(substring[3:5])
    year = int(substring[6:10])
    return day, month, year


def solve(prophesy):
    date_count = {}

    # Check every possible 10-character substring
    for i in range(len(prophesy) - 9):
        substring = prophesy[i:i + 10]

        # Check if it matches dd-mm-yyyy pattern
        if not _has_date_pattern(substring):
            continue

        try:
            day, month, year = _parse_date(substring)

            # Check if it's a valid date
            if is_valid_date(day, month, year):
                date_count[substring] = date_count.get(substring, 0) + 1
        except ValueError:
            continue

    # Find the date with maximum count
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date


# Read input and solve
prophesy = input().strip()
print(solve(prophesy))
