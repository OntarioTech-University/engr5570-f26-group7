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
    """Reads problem input from stdin and returns (M, N, matrix) or None on error."""
    try:
        M, N = map(int, input().split())
        initial_matrix = [list(map(int, input().split())) for _ in range(M)]
        return M, N, initial_matrix
    except (IOError, ValueError):
        return None

def compute_min_moves(initial_matrix, M, N):
    """Computes the minimum number of moves to reach a solution, or -1 if impossible."""
    # 1. Initial Check: Check if the starting board is already a solution
    if has_2x2_ones(initial_matrix, M, N):
        return 0

    # 2. Initialization for BFS
    queue = collections.deque([(initial_matrix, 0)])
    visited = {to_tuple(initial_matrix)}

    # 3. BFS Execution
    while queue:
        current_matrix, moves = queue.popleft()

        # Generate all possible next states by flipping every valid sub-matrix
        # A sub-matrix is defined by its top-left (r1, c1) and bottom-right (r2, c2) corners
        for r1 in range(M):
            for c1 in range(N):
                for r2 in range(r1, M):
                    for c2 in range(c1, N):
                        # The move is valid if the sub-matrix is not 1x1
                        if r1 == r2 and c1 == c2:
                            continue

                        # Create a new matrix for the next state (deep copy)
                        new_matrix = [row[:] for row in current_matrix]

                        # Flip the bits in the chosen sub-matrix
                        for r in range(r1, r2 + 1):
                            for c in range(c1, c2 + 1):
                                new_matrix[r][c] = 1 - new_matrix[r][c]

                        # Convert to tuple for checking 'visited' set
                        new_matrix_tuple = to_tuple(new_matrix)

                        # If this state has not been visited before
                        if new_matrix_tuple not in visited:
                            # Check if this new state is a solution
                            if has_2x2_ones(new_matrix, M, N):
                                return moves + 1

                            # If not a solution, add to queue and visited set
                            visited.add(new_matrix_tuple)
                            queue.append((new_matrix, moves + 1))

    # 4. Termination: If queue is empty and no solution found
    return -1

def print_result(result):
    """Prints the computed result."""
    print(result)

def solve():
    """Orchestrates reading input, computing the answer, and printing the result."""
    input_data = read_input()
    if input_data is None:
        print_result(-1)
        return

    M, N, initial_matrix = input_data
    result = compute_min_moves(initial_matrix, M, N)
    print_result(result)

def main():
    """Entry point when the script is run directly."""
    solve()

if __name__ == "__main__":
    main()
