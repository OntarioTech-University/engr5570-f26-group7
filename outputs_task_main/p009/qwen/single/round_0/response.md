```python
def count_balanced_substrings(s):
    count = 0
    n = len(s)
    for l in range(n):
        for r in range(l, n):
            for x in range(l, r + 1):
                left_4 = s[l:x].count('4')
                right_7 = s[x:r + 1].count('7')
                if left_4 == right_7:
                    count += 1
                    break
    return count


def read_case_count():
    return int(input())


def read_case():
    return input()


def print_result(result):
    print(result)


def main():
    case_count = read_case_count()
    for _ in range(case_count):
        s = read_case()
        result = count_balanced_substrings(s)
        print_result(result)


if __name__ == "__main__":
    main()
```

- Moved all executable script logic out of the module top level and into `main()`, guarded by `if __name__ == "__main__":`, so importing the file no longer triggers input/output side effects.
- Added `read_case_count()` and `read_case()` to isolate input handling and return values instead of using top-level variables.
- Kept `count_balanced_substrings()` unchanged as the main computation function, preserving its public signature and behavior.
- Added `print_result()` to isolate output handling and avoid direct `print()` calls in the orchestration logic.
- Preserved the original per-case read-compute-print order to keep runtime behavior, output ordering, and exception timing the same.
- No duplicated computation was present; the shared helpers centralize the repeated I/O structure.