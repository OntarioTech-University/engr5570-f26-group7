Here's the refactored version of the code:

```python
import sys

HEX_TO_BINARY = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
    'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
}


def read_matrix():
    """Read matrix from stdin in hex format and convert to binary."""
    n = int(input())
    matrix = []
    for _ in range(n):
        hex_row = input()
        binary_row = ''.join(HEX_TO_BINARY[digit] for digit in hex_row)
        matrix.append([int(bit) for bit in binary_row])
    return matrix


def is_identical_submatrix(matrix, start_row, start_col, size):
    """Check if a submatrix of given size contains identical values."""
    first_value = matrix[start_row][start_col]
    for row in range(start_row, start_row + size):
        for col in range(start_col, start_col + size):
            if matrix[row][col] != first_value:
                return False
    return True


def is_valid_compression(matrix, block_size):
    """Check if matrix can be compressed by given block size."""
    n = len(matrix)
    for start_row in range(0, n, block_size):
        for start_col in range(0, n, block_size):
            if not is_identical_submatrix(matrix, start_row, start_col, block_size):
                return False
    return True


def find_max_compression_factor(matrix):
    """Find the maximum compression factor for the matrix."""
    n = len(matrix)
    max_factor = 1
    for factor in range(2, n + 1):
        if n % factor == 0 and is_valid_compression(matrix, factor):
            max_factor = factor
    return max_factor


def main():
    matrix = read_matrix()
    result = find_max_compression_factor(matrix)
    print(result)


if __name__ == "__main__":
    main()
```

**Summary of changes:**

- **Extracted `read_matrix()` function**: Separates input parsing and hex-to-binary conversion from the main logic, making the code more modular and easier to test.
- **Extracted `is_valid_compression()` function**: Encapsulates the nested loop logic that checks if a compression factor is valid, eliminating deeply nested conditional logic.
- **Extracted `find_max_compression_factor()` function**: Isolates the algorithm for finding the maximum compression factor, making the main flow clearer.
- **Extracted `main()` function**: Provides a clear entry point and separates orchestration from implementation details.
- **Renamed variables for clarity**: Changed `x` to `factor`, `i`/`j` to `start_row`/`start_col`, and `val` to `first_value` to better express intent.
- **Moved `HEX_TO_BINARY` to module level**: Makes it a constant that's clearly separated from the logic, improving readability.
- **Used generator expression in `read_matrix()`**: Replaces the explicit loop for hex-to-binary conversion with a more concise and readable approach.
- **Added docstrings**: Documents the purpose of each function, making the code self-explanatory.
- **Added `if __name__ == "__main__"` guard**: Standard Python practice that allows the module to be imported without executing the main code.