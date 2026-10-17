import sys

# Read input
n = int(input())
matrix = []
hex_to_bin = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}

# Read the matrix in hexadecimal format and convert it to binary
for _ in range(n):
    hex_num = input()
    binary_row = ''
    for digit in hex_num:
        binary_row += hex_to_bin[digit]
    matrix.append([int(bit) for bit in binary_row])

# Function to check if a submatrix of size (n/x) x (n/x) is identical
def is_identical_submatrix(i, j, x):
    val = matrix[i][j]
    for row in range(i, i + x):
        for col in range(j, j + x):
            if matrix[row][col] != val:
                return False
    return True

# Find the maximum compression factor
max_x = 1
for x in range(2, n + 1):
    if n % x == 0:
        valid = True
        for i in range(0, n, x):
            for j in range(0, n, x):
                if not is_identical_submatrix(i, j, x):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            max_x = x

# Output the result
print(max_x)
