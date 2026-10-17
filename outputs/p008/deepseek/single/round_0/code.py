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
    """Reads matrix dimensions and initial state from stdin."""
    M, N = map(int, input().split())
    initial_matrix = [list(map(int, input().split())) for _ in range(M)]
    return M, N, initial_matrix


def create_flipped_matrix(matrix, r1, c1, r2, c2):
    """Creates a new matrix with the specified sub-matrix flipped."""
    new_matrix = [row[:] for row in matrix]
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            new_matrix[r][c] = 1 - new_matrix[r][c]
    return new_matrix


def generate_next_states(current_matrix, M, N):
    """Generates all valid next states by flipping sub-matrices."""
    for r1 in range(M):
        for c1 in range(N):
            for r2 in range(r1, M):
                for c2 in range(c1, N):
                    # Skip 1x1 sub-matrices
                    if r1 == r2 and c1 == c2:
                        continue
                    
                    new_matrix = create_flipped_matrix(current_matrix, r1, c1, r2, c2)
                    yield new_matrix


def solve():
    """Main function to solve the problem using BFS."""
    try:
        M, N, initial_matrix = read_input()
    except (IOError, ValueError):
        print(-1)
        return

    # Check if the starting board is already a solution
    if has_2x2_ones(initial_matrix, M, N):
        print(0)
        return

    # Initialize BFS
    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}

    # BFS execution
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

    # No solution found
    print(-1)


# Run the solver
solve()
