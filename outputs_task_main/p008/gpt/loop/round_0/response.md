```python
import collections


def has_2x2_ones(matrix, M, N):
    """Checks for a 2x2 sub-matrix of ones."""
    for r in range(M - 1):
        for c in range(N - 1):
            if (matrix[r][c] == 1 and
                matrix[r + 1][c] == 1 and
                matrix[r][c + 1] == 1 and
                matrix[r + 1][c + 1] == 1):
                return True
    return False


def to_tuple(matrix):
    """Converts a matrix to a hashable tuple for use in a set."""
    return tuple(tuple(row) for row in matrix)


def read_input():
    M, N = map(int, input().split())
    initial_matrix = [list(map(int, input().split())) for _ in range(M)]
    return M, N, initial_matrix


def compute_moves(M, N, initial_matrix):
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


def print_output(result):
    print(result)


def solve():
    """Reads the input, solves the problem, and prints the result."""
    try:
        M, N, initial_matrix = read_input()
    except (IOError, ValueError):
        print_output(-1)
        return

    print_output(compute_moves(M, N, initial_matrix))


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Separated input reading, BFS computation, and output printing into functions that pass data through parameters and return values.
- Kept `solve()` and the existing helper signatures unchanged, including its input-error handling and return behavior.
- Moved the executable call under the `__main__` guard and consolidated printing through one helper.