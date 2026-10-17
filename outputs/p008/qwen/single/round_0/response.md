```python
import collections


def _is_2x2_all_ones(matrix, r, c):
    """Returns True if the 2x2 block starting at (r, c) contains only ones."""
    return (matrix[r][c] == 1 and
            matrix[r + 1][c] == 1 and
            matrix[r][c + 1] == 1 and
            matrix[r + 1][c + 1] == 1)


# Helper function to check if a matrix contains a 2x2 sub-matrix of all 1s
def has_2x2_ones(matrix, M, N):
    """Checks for a 2x2 sub-matrix of ones."""
    for r in range(M - 1):
        for c in range(N - 1):
            if _is_2x2_all_ones(matrix, r, c):
                return True
    return False


# Helper function to convert a list-of-lists matrix to a hashable tuple-of-tuples
def to_tuple(matrix):
    """Converts a matrix to a hashable tuple for use in a set."""
    return tuple(tuple(row) for row in matrix)


def _read_input():
    """Reads matrix dimensions and matrix rows from standard input."""
    M, N = map(int, input().split())
    matrix = [list(map(int, input().split())) for _ in range(M)]
    return M, N, matrix


def _copy_matrix(matrix):
    """Returns a row-wise copy of the matrix."""
    return [row[:] for row in matrix]


def _flip_submatrix(matrix, r1, c1, r2, c2):
    """Flips all bits in the inclusive sub-matrix defined by the corners."""
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            matrix[r][c] = 1 - matrix[r][c]


def _next_matrices(current_matrix, M, N):
    """Yields all matrices reachable by flipping one non-1x1 sub-matrix."""
    for r1 in range(M):
        for c1 in range(N):
            for r2 in range(r1, M):
                for c2 in range(c1, N):
                    if r1 == r2 and c1 == c2:
                        continue

                    new_matrix = _copy_matrix(current_matrix)
                    _flip_submatrix(new_matrix, r1, c1, r2, c2)
                    yield new_matrix


def _find_minimum_moves(initial_matrix, M, N):
    """Returns the minimum number of moves to obtain a 2x2 block of ones."""
    if has_2x2_ones(initial_matrix, M, N):
        return 0

    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}

    while queue:
        current_matrix, moves = queue.popleft()

        for new_matrix in _next_matrices(current_matrix, M, N):
            new_matrix_tuple = to_tuple(new_matrix)

            if new_matrix_tuple not in visited:
                if has_2x2_ones(new_matrix, M, N):
                    return moves + 1

                visited.add(new_matrix_tuple)
                queue.append((new_matrix, moves + 1))

    return -1


def solve():
    """Main function to solve the problem using BFS."""
    try:
        M, N, initial_matrix = _read_input()
    except (IOError, ValueError):
        # Handle potential empty input or malformed lines
        print(-1)
        return

    print(_find_minimum_moves(initial_matrix, M, N))


# Run the solver
solve()
```

- Extracted the 2x2 block condition into `_is_2x2_all_ones` to simplify the loop in `has_2x2_ones`.
- Moved input parsing into `_read_input` while keeping the same exception handling behavior in `solve`.
- Split matrix mutation logic into `_copy_matrix` and `_flip_submatrix` to make state generation easier to read.
- Moved the deeply nested sub-matrix enumeration into `_next_matrices`, preserving the original generation order.
- Extracted the BFS logic into `_find_minimum_moves`, leaving `solve` focused on input/output.
- Public interfaces (`has_2x2_ones`, `to_tuple`, `solve`) remain unchanged.