```python
import collections


def has_2x2_ones(matrix, M, N):
    """Checks for a 2x2 sub-matrix of ones."""
    for r in range(M - 1):
        for c in range(N - 1):
            if (matrix[r][c] == 1 and
                matrix[r+1][c] == 1 and
                matrix[r][c+1] == 1 and
                matrix[r+1][c+1] == 1):
                return True
    return False


def to_tuple(matrix):
    """Converts a matrix to a hashable tuple for use in a set."""
    return tuple(tuple(row) for row in matrix)


def read_input():
    """Reads matrix dimensions and initial matrix from standard input."""
    try:
        M, N = map(int, input().split())
        initial_matrix = [list(map(int, input().split())) for _ in range(M)]
        return M, N, initial_matrix
    except (IOError, ValueError):
        return None, None, None


def find_min_moves(M, N, initial_matrix):
    """Finds the minimum number of moves to get a 2x2 sub-matrix of ones using BFS."""
    if has_2x2_ones(initial_matrix, M, N):
        return 0

    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}

    while queue:
        current_matrix, moves = queue.popleft()

        for r1 in range(M):
            for c1 in range(N):
                for r2 in range(r1, M):
                    for c2 in range(c1, N):
                        if r1 == r2 and c1 == c2:
                            continue

                        new_matrix = [row[:] for row in current_matrix]

                        for r in range(r1, r2 + 1):
                            for c in range(c1, c2 + 1):
                                new_matrix[r][c] = 1 - new_matrix[r][c]

                        new_matrix_tuple = to_tuple(new_matrix)

                        if new_matrix_tuple not in visited:
                            if has_2x2_ones(new_matrix, M, N):
                                return moves + 1

                            visited.add(new_matrix_tuple)
                            queue.append((new_matrix, moves + 1))

    return -1


def print_result(result):
    """Prints the result to standard output."""
    print(result)


def main():
    """Main function to orchestrate input, computation, and output."""
    M, N, initial_matrix = read_input()
    if M is None:
        print_result(-1)
        return

    result = find_min_moves(M, N, initial_matrix)
    print_result(result)


if __name__ == "__main__":
    main()
```

- **Moved all logic into functions**: Input reading, computation, and output are now in `read_input()`, `find_min_moves()`, and `print_result()` respectively, with `main()` orchestrating them.
- **Eliminated global variables**: All data is passed between functions via parameters and return values.
- **Removed top-level execution**: The `solve()` function was replaced by `main()`, which is only called under `if __name__ == "__main__":`.
- **Preserved behavior**: The BFS logic, error handling, and output format remain identical to the original code.