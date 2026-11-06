import sys

def read_input():
    """
    Reads the first line containing t and m, then reads t operation lines.
    Returns (t, m, operations) or None if the first line is missing or invalid.
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
    except (IOError, ValueError):
        return None

    operations = []
    for _ in range(t):
        operations.append(sys.stdin.readline().strip())
    return t, m, operations


def find_free_block(memory, n):
    """
    Finds the first contiguous block of n free bytes using first-fit.
    Returns the starting index or -1 if no suitable block exists.
    """
    m = len(memory)
    found_pos = -1
    i = 0
    while i <= m - n:
        if memory[i] == 0:
            j = i
            while j < m and memory[j] == 0:
                j += 1
            if (j - i) >= n:
                found_pos = i
                break
            else:
                i = j
        else:
            i += 1
    return found_pos


def erase_block(memory, block_id):
    """Frees all bytes belonging to the given block ID."""
    for i in range(len(memory)):
        if memory[i] == block_id:
            memory[i] = 0


def print_output(line):
    """Prints a single line of output."""
    print(line)


def process_operations(t, m, operations):
    """
    Processes the list of operations and prints output as each operation is handled.
    State is kept local to this function.
    """
    memory = [0] * m
    next_id = 1
    active_ids = set()

    for line in operations:
        if not line:
            continue

        parts = line.split()
        command = parts[0]

        if command == "alloc":
            n = int(parts[1])
            found_pos = find_free_block(memory, n)

            if found_pos != -1:
                print_output(next_id)
                active_ids.add(next_id)
                for k in range(found_pos, found_pos + n):
                    memory[k] = next_id
                next_id += 1
            else:
                print_output("NULL")

        elif command == "erase":
            x = int(parts[1])
            if x > 0 and x in active_ids:
                active_ids.remove(x)
                erase_block(memory, x)
            else:
                print_output("ILLEGAL_ERASE_ARGUMENT")

        elif command == "defragment":
            occupied_blocks = [block for block in memory if block != 0]
            memory = occupied_blocks + [0] * (m - len(occupied_blocks))


def main():
    """Reads input, processes operations, and prints output."""
    input_data = read_input()
    if input_data is None:
        return
    t, m, operations = input_data
    process_operations(t, m, operations)


def memory_manager():
    """Public wrapper that delegates to main()."""
    main()


if __name__ == "__main__":
    main()
