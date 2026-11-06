```python
import collections


# Helper function to check if a matrix contains a 2x2 sub-matrix of all 1s
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


# Helper function to convert a list-of-lists matrix to a hashable tuple-of-tuples
def to_tuple(matrix):
    """Converts a matrix to a hashable tuple for use in a set."""
    return tuple(tuple(row) for row in matrix)


def read_input():
    M, N = map(int, input().split())
    initial_matrix = [list(map(int, input().split())) for _ in range(M)]
    return M, N, initial_matrix


def flip_submatrix(matrix, r1, c1, r2, c2):
    new_matrix = [row[:] for row in matrix]
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            new_matrix[r][c] = 1 - new_matrix[r][c]
    return new_matrix


def generate_next_matrices(matrix, M, N):
    for r1 in range(M):
        for c1 in range(N):
            for r2 in range(r1, M):
                for c2 in range(c1, N):
                    if r1 == r2 and c1 == c2:
                        continue
                    yield flip_submatrix(matrix, r1, c1, r2, c2)


def find_min_moves(initial_matrix, M, N):
    if has_2x2_ones(initial_matrix, M, N):
        return 0

    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}
    while queue:
        current_matrix, moves = queue.popleft()
        for new_matrix in generate_next_matrices(current_matrix, M, N):
            new_matrix_tuple = to_tuple(new_matrix)
            if new_matrix_tuple not in visited:
                if has_2x2_ones(new_matrix, M, N):
                    return moves + 1
                visited.add(new_matrix_tuple)
                queue.append((new_matrix, moves + 1))
    return -1


def print_result(result):
    print(result)


def solve():
    """Main function to solve the problem using BFS."""
    try:
        M, N, initial_matrix = read_input()
    except (IOError, ValueError):
        print_result(-1)
        return

    print_result(find_min_moves(initial_matrix, M, N))


# Run the solver
solve()
```

- Separated input reading and output printing while keeping the same input-error handling in `solve()`.
- Extracted sub-matrix flipping and move generation from the BFS loop, preserving move order and visited-state checks.
- Kept `solve()`, `has_2x2_ones()`, and `to_tuple()` signatures unchanged.