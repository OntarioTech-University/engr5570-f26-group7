def _hex_char_to_bits(char):
    """Convert a single hexadecimal character to a 4-bit binary string."""
    if char.isdigit():
        value = int(char)
    else:
        value = int(char, 16)
    return format(value, '04b')


def hex_to_bin(hex_str):
    """Convert a hexadecimal string to a binary string."""
    bin_str = ''
    for char in hex_str:
        bin_str += _hex_char_to_bits(char)
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


def _read_input():
    """Read the matrix size and hexadecimal rows from standard input."""
    n = int(input())
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    return n, matrix


def _print_result(result):
    """Print the final result."""
    print(result)


def main():
    n, matrix = _read_input()
    result = solve(n, matrix)
    _print_result(result)


if __name__ == "__main__":
    main()
