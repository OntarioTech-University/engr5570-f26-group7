```python
import sys


def read_input():
    n = int(input())
    matrix = []
    hex_to_bin = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }

    for _ in range(n):
        hex_num = input()
        matrix.append(_hex_row_to_bits(hex_num, hex_to_bin))

    return n, matrix


def _hex_row_to_bits(hex_num, hex_to_bin):
    binary_row = ''
    for digit in hex_num:
        binary_row += hex_to_bin[digit]
    return [int(bit) for bit in binary_row]


def compute_max_x(n, matrix):
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0:
            if _is_valid_block_size(n, matrix, x):
                max_x = x
    return max_x


def _is_valid_block_size(n, matrix, x):
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not is_identical_submatrix(matrix, i, j, x):
                return False
    return True


def is_identical_submatrix(matrix, i, j, x):
    val = matrix[i][j]
    for row in range(i, i + x):
        for col in range(j, j + x):
            if matrix[row][col] != val:
                return False
    return True


def print_result(result):
    print(result)


def main():
    n, matrix = read_input()
    result = compute_max_x(n, matrix)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved all executable script logic into `main()` under `if __name__ == "__main__":`, so importing the file no longer runs the program.
- Split the program into `read_input()`, `compute_max_x()`, and `print_result()` to separate input, computation, and output concerns.
- Eliminated global state by returning `n` and `matrix` from `read_input()` and passing them explicitly to the computation functions.
- Extracted hexadecimal-row conversion into `_hex_row_to_bits()` so input parsing is centralized and reusable.
- Extracted block validation into `_is_valid_block_size()` and made `is_identical_submatrix()` receive the matrix explicitly instead of relying on a global variable.