```python
def _char_to_bin(char):
    """Convert a single hexadecimal character to a 4-bit binary string."""
    if char.isdigit():
        return format(int(char), '04b')
    return format(int(char, 16), '04b')


def hex_to_bin(hex_str):
    """Convert a hexadecimal string to a binary string."""
    bin_str = ''
    for char in hex_str:
        bin_str += _char_to_bin(char)
    return bin_str


def can_compress(matrix, x):
    """Check if the matrix can be x-compressed."""
    n = len(matrix)
    for i in range(0, n, x):
        for j in range(0, n, x):
            val = matrix[i][j]
            for di in range(x):
                for dj in range(x):
                    if matrix[i + di][j + dj] != val:
                        return False
    return True


def solve(n, matrix):
    """Find the maximum x such that an x-compression of the given matrix is possible."""
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0 and can_compress(matrix, x):
            max_x = x
    return max_x


def read_input():
    """Read n and the matrix from standard input."""
    n = int(input())
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    return n, matrix


def print_output(result):
    """Print the result to standard output."""
    print(result)


def main():
    n, matrix = read_input()
    result = solve(n, matrix)
    print_output(result)


if __name__ == "__main__":
    main()
```

- Moved input reading into `read_input()` and output printing into `print_output()`, so `main()` only orchestrates the flow.
- Extracted per-character hex-to-binary conversion into `_char_to_bin()`, removing duplicated `format(...)` logic while preserving exact behavior.
- Data is now passed between functions through parameters and return values instead of being handled directly in `main()`.
- No logic runs at the top level and no global variables are used; only function definitions and the standard `if __name__ == "__main__":` guard remain.
- Public function signatures (`hex_to_bin`, `can_compress`, `solve`, `main`) are unchanged.