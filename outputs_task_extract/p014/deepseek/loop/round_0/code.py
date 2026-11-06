import sys

HEX_TO_BIN = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
    'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
}


def read_matrix_size():
    """Read and return the size of the matrix."""
    return int(input())


def hex_to_binary(hex_string):
    """Convert a hexadecimal string to a binary string."""
    binary_string = ''
    for digit in hex_string:
        binary_string += HEX_TO_BIN[digit]
    return binary_string


def read_matrix(n):
    """Read an n x n matrix in hexadecimal format and return it as binary."""
    matrix = []
    for _ in range(n):
        hex_row = input()
        binary_row = hex_to_binary(hex_row)
        matrix.append([int(bit) for bit in binary_row])
    return matrix


def is_identical_submatrix(matrix, start_row, start_col, size):
    """Check if a submatrix of given size starting at (start_row, start_col) is identical."""
    first_value = matrix[start_row][start_col]
    for row in range(start_row, start_row + size):
        for col in range(start_col, start_col + size):
            if matrix[row][col] != first_value:
                return False
    return True


def is_valid_compression(matrix, n, compression_factor):
    """Check if the matrix can be compressed by the given factor."""
    for start_row in range(0, n, compression_factor):
        for start_col in range(0, n, compression_factor):
            if not is_identical_submatrix(matrix, start_row, start_col, compression_factor):
                return False
    return True


def find_max_compression_factor(matrix, n):
    """Find and return the maximum compression factor for the matrix."""
    max_factor = 1
    for factor in range(2, n + 1):
        if n % factor == 0 and is_valid_compression(matrix, n, factor):
            max_factor = factor
    return max_factor


def main():
    """Main function to orchestrate the program flow."""
    n = read_matrix_size()
    matrix = read_matrix(n)
    max_compression = find_max_compression_factor(matrix, n)
    print(max_compression)


if __name__ == "__main__":
    main()
