```python
def read_input():
    return input()


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


def print_output(value):
    print(value)


def main():
    t = int(read_input())
    for _ in range(t):
        s = read_input()
        print_output(count_balanced_substrings(s))


if __name__ == "__main__":
    main()
```

- Moved the execution loop into `main()` and guarded it, so importing the file does not run the program.
- Separated input reading and output printing into functions while retaining the existing computation function and its signature.
- Kept input, computation, and printing in their original per-case order.