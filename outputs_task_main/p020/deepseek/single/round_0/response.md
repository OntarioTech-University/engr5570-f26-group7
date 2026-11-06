```python
import sys

def read_prophecy():
    """Reads the prophecy string from standard input."""
    return sys.stdin.readline().strip()

def find_most_frequent_date(prophecy):
    """
    Finds the most frequently occurring valid date in the prophecy string.
    Returns the date as a string in "dd-mm-yyyy" format.
    """
    n = len(prophecy)
    date_counts = {}

    # Days in each month for a non-leap year (years 2013-2015).
    # Index 0 is a placeholder to allow for 1-based month indexing.
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(n - 9):
        candidate = prophecy[i : i + 10]

        # Validate format: "xx-xx-xxxx"
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

    # The problem guarantees that a unique apocalypse date exists.
    return max(date_counts, key=date_counts.get)

def print_apocalypse_date(date):
    """Prints the apocalypse date."""
    print(date)

def find_apocalypse_date():
    """
    This function reads a prophesy string, finds all valid dates within it,
    counts their occurrences, and prints the date that appears most frequently.
    """
    prophecy = read_prophecy()
    apocalypse_date = find_most_frequent_date(prophecy)
    print_apocalypse_date(apocalypse_date)

def main():
    find_apocalypse_date()

if __name__ == "__main__":
    main()
```

- **Separated input, computation, and output** into `read_prophecy`, `find_most_frequent_date`, and `print_apocalypse_date` respectively, each with a single responsibility.
- **Removed top-level logic** by placing all executable code inside functions and calling `main()` only under the `if __name__ == "__main__":` guard.
- **Eliminated global variables** by keeping all data local to functions and passing values via parameters and return values.
- **Preserved the public interface** `find_apocalypse_date()` unchanged in name and signature; it now orchestrates the helper functions while maintaining identical behavior.
- **No duplicated code** was present in the original implementation, so no shared helper for duplication was required.