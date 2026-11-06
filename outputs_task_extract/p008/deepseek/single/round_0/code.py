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

def _read_initial_state():
    """Read M, N and the initial matrix; return None for malformed input."""
    try:
        M, N = map(int, input().split())
        matrix = [list(map(int, input().split())) for _ in range(M)]
        return M, N, matrix
    except (IOError, ValueError):
        return None

def _print_result(value):
    """Print the computed result."""
    print(value)

def _valid_submatrix_ranges(M, N):
    """Yield corners of every non-1x1 sub-matrix."""
    for r1 in range(M):
        for c1 in range(N):
            for r2 in range(r1, M):
                for c2 in range(c1, N):
                    if r1 == r2 and c1 == c2:
                        continue
                    yield r1, c1, r2, c2

def _flip_submatrix(matrix, r1, c1, r2, c2):
    """Return a copy of matrix with the chosen sub-matrix flipped."""
    new_matrix = [row[:] for row in matrix]
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            new_matrix[r][c] = 1 - new_matrix[r][c]
    return new_matrix

def _generate_next_states(current_matrix, M, N):
    """Yield all matrices reachable by one valid sub-matrix flip."""
    for r1, c1, r2, c2 in _valid_submatrix_ranges(M, N):
        yield _flip_submatrix(current_matrix, r1, c1, r2, c2)

def _process_new_state(matrix, M, N, moves, queue, visited):
    """Process a newly generated matrix state.

    Returns the number of moves if it solves the puzzle, otherwise queues it
    and returns None.
    """
    matrix_tuple = to_tuple(matrix)
    if matrix_tuple in visited:
        return None

    if has_2x2_ones(matrix, M, N):
        return moves + 1

    visited.add(matrix_tuple)
    queue.append((matrix, moves + 1))
    return None

def _find_minimum_moves(M, N, initial_matrix):
    """Run BFS to find the minimum number of moves, or -1 if unsolvable."""
    if has_2x2_ones(initial_matrix, M, N):
        return 0

    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}

    while queue:
        current_matrix, moves = queue.popleft()
        for new_matrix in _generate_next_states(current_matrix, M, N):
            result = _process_new_state(new_matrix, M, N, moves, queue, visited)
            if result is not None:
                return result

    return -1

def solve():
    """Main function to solve the problem using BFS."""
    initial_state = _read_initial_state()
    if initial_state is None:
        _print_result(-1)
        return

    M, N, initial_matrix = initial_state
    _print_result(_find_minimum_moves(M, N, initial_matrix))

solve()
