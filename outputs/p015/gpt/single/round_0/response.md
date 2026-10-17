```python
def hex_to_bin(hex_str):
    """Convert a hexadecimal string to a binary string."""
    bin_str = ''
    for char in hex_str:
        if char.isdigit():
            bin_str += format(int(char), '04b')
        else:
            bin_str += format(int(char, 16), '04b')
    return bin_str


def _block_is_uniform(matrix, i, j, x):
    val = matrix[i][j]
    for di in range(x):
        for dj in range(x):
            if matrix[i + di][j + dj] != val:
                return False
    return True


def can_compress(matrix, x):
    """Check if the matrix can be x-compressed."""
    n = len(matrix)
    for i in range(0, n, x):
        for j in range(0, n, x):
            if not _block_is_uniform(matrix, i, j, x):
                return False
    return True


def solve(n, matrix):
    """Find the maximum x such that an x-compression of the given matrix is possible."""
    max_x = 1
    for x in range(2, n + 1):
        if n % x == 0 and can_compress(matrix, x):
            max_x = x
    return max_x


def main():
    n = int(input())
    matrix = []
    for _ in range(n):
        hex_str = input()
        bin_str = hex_to_bin(hex_str)
        matrix.append([int(bit) for bit in bin_str])
    print(solve(n, matrix))


if __name__ == "__main__":
    main()
```

- Extracted the per-block comparison into `_block_is_uniform`, reducing nesting in `can_compress` while preserving its check order and early return.
- Left the conversion, search, and input logic unchanged to preserve their behavior.