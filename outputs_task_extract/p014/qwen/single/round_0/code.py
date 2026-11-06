import sys


def read_size():
    return int(input())


def build_hex_to_bin():
    return {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111',
    }


def convert_hex_num_to_binary_digits(hex_num, hex_to_bin):
    binary_row = ''
    for digit in hex_num:
        binary_row += hex_to_bin[digit]
    return [int(bit) for bit in binary_row]


def read_matrix_row(hex_to_bin):
    hex_num = input()
    return convert_hex_num_to_binary_digits(hex_num, hex_to_bin)


def read_matrix_rows(n, matrix, hex_to_bin):
    for _ in range(n):
        matrix.append(read_matrix_row(hex_to_bin))


def is_identical_submatrix(i, j, x):
    val = matrix[i][j]
    for row in range(i, i + x):
        for col in range(j, j + x):
            if matrix[row][col] != val:
                return False
    return True


def is_valid_partition(n, x):
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not is_identical_submatrix(i, j, x):
                return False
    return True


def find_max_compression_factor(n):
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0 and is_valid_partition(n, x):
            max_x = x
    return max_x


def print_result(max_x):
    print(max_x)


def main():
    global n, matrix, hex_to_bin
    n = read_size()
    matrix = []
    hex_to_bin = build_hex_to_bin()
    read_matrix_rows(n, matrix, hex_to_bin)
    max_x = find_max_compression_factor(n)
    print_result(max_x)


main()
