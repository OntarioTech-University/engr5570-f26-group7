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
    date_count = {}
    
    # Check every possible 10-character substring
    for i in range(len(prophesy) - 9):
        substring = prophesy[i:i+10]
        
        # Check if it matches dd-mm-yyyy pattern
        if len(substring) == 10 and substring[2] == '-' and substring[5] == '-':
            try:
                day = int(substring[0:2])
                month = int(substring[3:5])
                year = int(substring[6:10])
                
                # Check if it's a valid date
                if is_valid_date(day, month, year):
                    date_str = substring
                    date_count[date_str] = date_count.get(date_str, 0) + 1
            except ValueError:
                continue
    
    # Find the date with maximum count
    max_count = max(date_count.values())
    for date, count in date_count.items():
        if count == max_count:
            return date


def read_input():
    return input().strip()


def print_result(result):
    print(result)


def main():
    prophesy = read_input()
    result = solve(prophesy)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved top-level input reading and output printing into dedicated `read_input()` and `print_result()` functions.
- Added a `main()` function that orchestrates the flow: read input → compute result → print output.
- Called `main()` only under the `if __name__ == "__main__":` guard, eliminating top-level execution.
- Removed global variables; all data is passed through function parameters and return values.
- Preserved the public interfaces `is_valid_date` and `solve` exactly as before.
- No duplicated code was found, so no shared helper extraction was needed.