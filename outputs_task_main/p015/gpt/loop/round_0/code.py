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
    n = int(input())
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    return n, matrix


def print_output(result):
    print(result)


def main():
    n, matrix = read_input()
    result = solve(n, matrix)
    print_output(result)


if __name__ == "__main__":
    main()
