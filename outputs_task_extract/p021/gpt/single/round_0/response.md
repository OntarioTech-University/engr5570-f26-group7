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


def has_date_pattern(substring):
    return len(substring) == 10 and substring[2] == '-' and substring[5] == '-'


def count_date(substring, date_count):
    if not has_date_pattern(substring):
        return

    try:
        day = int(substring[0:2])
        month = int(substring[3:5])
        year = int(substring[6:10])

        if is_valid_date(day, month, year):
            date_str = substring
            date_count[date_str] = date_count.get(date_str, 0) + 1
    except ValueError:
        return


def count_dates(prophesy):
    date_count = {}
    for i in range(len(prophesy) - 9):
        substring = prophesy[i:i+10]
        count_date(substring, date_count)
    return date_count


def most_common_date(date_count):
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date


def solve(prophesy):
    date_count = count_dates(prophesy)
    return most_common_date(date_count)


def read_prophesy():
    return input().strip()


def print_answer(answer):
    print(answer)


def main():
    prophesy = read_prophesy()
    print_answer(solve(prophesy))


main()
```

- Separated pattern checking, date counting, and result selection into small functions, leaving `solve` to coordinate them.
- Moved input reading and output printing into dedicated functions while retaining execution at the top level.
- Kept the public function signatures, date-counting order, and `ValueError` handling unchanged.