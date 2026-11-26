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

def read_initial_state():
    """Reads M, N and the initial matrix from standard input."""
    M, N = map(int, input().split())
    initial_matrix = [list(map(int, input().split())) for _ in range(M)]
    return M, N, initial_matrix

def flip_submatrix(matrix, r1, c1, r2, c2):
    """Returns a new matrix with the specified sub-matrix flipped."""
    new_matrix = [row[:] for row in matrix]
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            new_matrix[r][c] = 1 - new_matrix[r][c]
    return new_matrix

def generate_next_states(matrix, M, N):
    """Yields all valid next states by flipping every non-1x1 sub-matrix."""
    for r1 in range(M):
        for c1 in range(N):
            for r2 in range(r1, M):
                for c2 in range(c1, N):
                    if r1 == r2 and c1 == c2:
                        continue
                    yield flip_submatrix(matrix, r1, c1, r2, c2)

def solve():
    """Main function to solve the problem using BFS."""
    try:
        M, N, initial_matrix = read_initial_state()
    except (IOError, ValueError):
        print(-1)
        return

    if has_2x2_ones(initial_matrix, M, N):
        print(0)
        return

    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}

    while queue:
        current_matrix, moves = queue.popleft()

        for new_matrix in generate_next_states(current_matrix, M, N):
            new_matrix_tuple = to_tuple(new_matrix)

            if new_matrix_tuple not in visited:
                if has_2x2_ones(new_matrix, M, N):
                    print(moves + 1)
                    return

                visited.add(new_matrix_tuple)
                queue.append((new_matrix, moves + 1))

    print(-1)

solve()
```

- Extracted `read_initial_state` to separate input parsing from the BFS logic, making `solve` shorter and clearer.
- Extracted `flip_submatrix` to encapsulate deep copying and bit flipping, removing nested loops from the main BFS loop.
- Extracted `generate_next_states` as a generator to isolate the four-level sub-matrix iteration and the 1x1 skip condition, reducing indentation and improving readability.
- Simplified the BFS loop by iterating over generated next states instead of inline nested loops, preserving the original order and behavior.
- Added docstrings to new helper functions for clarity without changing any public interfaces or runtime behavior.