def is_valid_date(day, month, year):
    if year < 2013 or year > 2015:
        return False
    if month < 1 or month > 12:
        return False
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    max_days = days_in_month[month - 1]
    return 1 < day <= max_days

def solve(prophesy):
    date_count = {}
    for i in range(len(prophesy) - 9):
        substring = prophesy[i:i + 10]
        if len(substring) == 10 and substring[2] == '-' and (substring[5] == '-'):
            try:
                day = int(substring[0:2])
                month = int(substring[3:5])
                year = int(substring[6:10])
                if is_valid_date(day, month, year):
                    date_str = substring
                    date_count[date_str] = date_count.get(date_str, 0) + 1
            except ValueError:
                continue
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date
prophesy = input().strip()
print(solve(prophesy))
