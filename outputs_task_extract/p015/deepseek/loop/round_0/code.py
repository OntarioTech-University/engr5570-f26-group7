def hex_to_bin(hex_str):
    """Convert a hexadecimal string to a binary string."""
    return ''.join(_hex_char_to_bin(char) for char in hex_str)


def _hex_char_to_bin(char):
    """Convert a single hexadecimal character to a 4-bit binary string."""
    if char.isdigit():
        return format(int(char), '04b')
    return format(int(char, 16), '04b')


def can_compress(matrix, x):
    """Check if the matrix can be x-compressed."""
    n = len(matrix)
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not _is_uniform_block(matrix, i, j, x):
                return False
    return True


def _is_uniform_block(matrix, row, col, size):
    """Check whether a size x size block contains identical values."""
    val = matrix[row][col]
    for di in range(size):
        for dj in range(size):
            if matrix[row + di][col + dj] != val:
                return False
    return True


def solve(n, matrix):
    """Find the maximum x such that an x-compression of the given matrix is possible."""
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0 and can_compress(matrix, x):
            max_x = x
    return max_x


def read_size():
    """Read the matrix size from standard input."""
    return int(input())


def read_matrix(n):
    """Read an n x n matrix from standard input."""
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    return matrix


def print_result(result):
    """Print the computed result."""
    print(result)


def main():
    n = read_size()
    matrix = read_matrix(n)
    result = solve(n, matrix)
    print_result(result)


if __name__ == "__main__":
    main()
