def hex_to_bin(hex_str):
    """Convert a hexadecimal string to a binary string."""
    bin_str = ''
    for char in hex_str:
        if char.isdigit():
            bin_str += format(int(char), '04b')
        else:
            bin_str += format(int(char, 16), '04b')
    return bin_str


def can_compress(matrix, x):
    """Check if the matrix can be x-compressed."""
    n = len(matrix)
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not _is_uniform_block(matrix, i, j, x):
                return False
    return True


def _is_uniform_block(matrix, start_i, start_j, size):
    """Return True if the square block starting at (start_i, start_j) has one value."""
    value = matrix[start_i][start_j]
    for di in range(size):
        for dj in range(size):
            if matrix[start_i + di][start_j + dj] != value:
                return False
    return True


def solve(n, matrix):
    """Find the maximum x such that an x-compression of the given matrix is possible."""
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0 and can_compress(matrix, x):
            max_x = x
    return max_x


def _read_matrix(n):
    """Read n hexadecimal rows and convert them to a binary matrix."""
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    return matrix


def main():
    n = int(input())
    matrix = _read_matrix(n)
    print(solve(n, matrix))


if __name__ == "__main__":
    main()
