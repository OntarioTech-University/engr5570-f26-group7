import sys


def read_size():
    return int(input())


n = read_size()
matrix = []
hex_to_bin = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}


def convert_hex_row(hex_num):
    binary_row = ''
    for digit in hex_num:
        binary_row += hex_to_bin[digit]
    return [int(bit) for bit in binary_row]


def read_matrix():
    for _ in range(n):
        hex_num = input()
        matrix.append(convert_hex_row(hex_num))


read_matrix()


def is_identical_submatrix(i, j, x):
    val = matrix[i][j]
    for row in range(i, i + x):
        for col in range(j, j + x):
            if matrix[row][col] != val:
                return False
    return True


def is_valid_compression_factor(x):
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not is_identical_submatrix(i, j, x):
                return False
    return True


def find_max_compression_factor():
    max_factor = 1
    for x in range(2, n + 1):
        if n % x == 0 and is_valid_compression_factor(x):
            max_factor = x
    return max_factor


def print_result(result):
    print(result)


max_x = find_max_compression_factor()
print_result(max_x)
