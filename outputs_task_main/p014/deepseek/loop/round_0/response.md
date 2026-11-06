```python
def read_input():
    n = int(input())
    hex_to_bin = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }
    matrix = []
    for _ in range(n):
        hex_num = input()
        binary_row = ''
        for digit in hex_num:
            binary_row += hex_to_bin[digit]
        matrix.append([int(bit) for bit in binary_row])
    return matrix


def is_identical_submatrix(matrix, i, j, x):
    val = matrix[i][j]
    for row in range(i, i + x):
        for col in range(j, j + x):
            if matrix[row][col] != val:
                return False
    return True


def find_max_compression_factor(matrix):
    n = len(matrix)
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0:
            valid = True
            for i in range(0, n, x):
                for j in range(0, n, x):
                    if not is_identical_submatrix(matrix, i, j, x):
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                max_x = x
    return max_x


def print_result(result):
    print(result)


def main():
    matrix = read_input()
    result = find_max_compression_factor(matrix)
    print_result(result)


if __name__ == "__main__":
    main()
```

- Moved all top-level logic into a `main()` function and guarded it with `if __name__ == "__main__":`.
- Extracted input reading and hex-to-binary conversion into `read_input()`, which returns the matrix.
- Extracted the main computation into `find_max_compression_factor(matrix)`, which returns the maximum compression factor.
- Extracted output printing into `print_result(result)`.
- Updated `is_identical_submatrix` to accept `matrix` as a parameter, removing the dependency on a global variable.
- Removed the unused `import sys` statement.