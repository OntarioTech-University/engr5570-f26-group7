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


def print_result(value):
    """Prints a final answer."""
    print(value)


def read_dimensions():
    """Reads the matrix dimensions from standard input."""
    return map(int, input().split())


def read_matrix(M):
    """Reads M rows of matrix data from standard input."""
    return [list(map(int, input().split())) for _ in range(M)]


def read_initial_state():
    """Reads the full initial problem state."""
    M, N = read_dimensions()
    matrix = read_matrix(M)
    return M, N, matrix


def copy_matrix(matrix):
    """Creates a shallow copy of a list-of-lists matrix."""
    return [row[:] for row in matrix]


def flip_submatrix(matrix, r1, c1, r2, c2):
    """Flips all bits in the given inclusive sub-matrix."""
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            matrix[r][c] = 1 - matrix[r][c]


def generate_next_matrices(matrix, M, N):
    """Yields all matrices reachable by one valid flip."""
    for r1 in range(M):
        for c1 in range(N):
            for r2 in range(r1, M):
                for c2 in range(c1, N):
                    if r1 == r2 and c1 == c2:
                        continue
                    new_matrix = copy_matrix(matrix)
                    flip_submatrix(new_matrix, r1, c1, r2, c2)
                    yield new_matrix


def create_search_queue(matrix):
    """Creates the initial BFS queue."""
    return collections.deque([(matrix, 0)])


def create_visited_set(matrix):
    """Creates the initial BFS visited set."""
    return {to_tuple(matrix)}


def initialize_bfs(matrix):
    """Prepares the queue and visited set for BFS."""
    return create_search_queue(matrix), create_visited_set(matrix)


def add_state(queue, visited, matrix, matrix_tuple, moves):
    """Records a newly discovered BFS state."""
    visited.add(matrix_tuple)
    queue.append((matrix, moves))


def handle_candidate(new_matrix, moves, M, N, queue, visited):
    """Processes one generated state and reports if solved."""
    new_matrix_tuple = to_tuple(new_matrix)
    if new_matrix_tuple in visited:
        return False
    if has_2x2_ones(new_matrix, M, N):
        print_result(moves + 1)
        return True
    add_state(queue, visited, new_matrix, new_matrix_tuple, moves + 1)
    return False


def process_current_state(current_matrix, moves, M, N, queue, visited):
    """Expands one BFS state."""
    for new_matrix in generate_next_matrices(current_matrix, M, N):
        if handle_candidate(new_matrix, moves, M, N, queue, visited):
            return True
    return False


def run_bfs(queue, visited, M, N):
    """Runs BFS until a solution is found or states are exhausted."""
    while queue:
        current_matrix, moves = queue.popleft()
        if process_current_state(current_matrix, moves, M, N, queue, visited):
            return
    print_result(-1)


def solve():
    """Main function to solve the problem using BFS."""
    try:
        M, N, initial_matrix = read_initial_state()
    except (IOError, ValueError):
        print_result(-1)
        return

    if has_2x2_ones(initial_matrix, M, N):
        print_result(0)
        return

    queue, visited = initialize_bfs(initial_matrix)
    run_bfs(queue, visited, M, N)


solve()
