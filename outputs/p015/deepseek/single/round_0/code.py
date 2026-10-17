def hex_to_bin(hex_str):
    """Convert a hexadecimal string to a binary string."""
    return ''.join(format(int(char, 16), '04b') for char in hex_str)


def is_uniform_block(matrix, row, col, size):
    """Check if all elements in the block starting at (row, col) are equal."""
    first_value = matrix[row][col]
    for i in range(row, row + size):
        for j in range(col, col + size):
            if matrix[i][j] != first_value:
                return False
    return True


def can_compress(matrix, x):
    """Check if the matrix can be x-compressed."""
    n = len(matrix)
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not is_uniform_block(matrix, i, j, x):
                return False
    return True


def solve(n, matrix):
    """Find the maximum x such that an x-compression of the given matrix is possible."""
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0 and can_compress(matrix, x):
            max_x = x
    return max_x


def read_matrix(n):
    """Read n lines of hexadecimal input and convert them to a binary matrix."""
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    return matrix


def main():
    n = int(input())
    matrix = read_matrix(n)
    print(solve(n, matrix))


if __name__ == "__main__":
    main()
