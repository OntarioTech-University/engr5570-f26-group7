import sys


def read_initial_configuration():
    """Read the operation count and memory size from standard input."""
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
    except (IOError, ValueError):
        return None
    return t, m


def read_operation_line():
    """Read one operation line from standard input."""
    return sys.stdin.readline().strip()


def parse_integer_argument(parts):
    """Return the second token of a split command line as an integer."""
    return int(parts[1])


def write_output(value):
    """Write one line of program output."""
    print(value)


def find_first_fit(memory, m, n):
    """Return the first starting position with at least n free bytes, or -1."""
    i = 0
    while i <= m - n:
        if memory[i] == 0:
            j = i
            while j < m and memory[j] == 0:
                j += 1

            if (j - i) >= n:
                return i

            i = j
        else:
            i += 1

    return -1


def allocate_block(memory, start, n, block_id):
    """Mark n bytes beginning at start as occupied by block_id."""
    for k in range(start, start + n):
        memory[k] = block_id


def erase_block(memory, m, block_id):
    """Free every byte currently occupied by block_id."""
    for i in range(m):
        if memory[i] == block_id:
            memory[i] = 0


def defragment_memory(memory, m):
    """Return a compacted copy of memory with occupied bytes moved left."""
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def is_valid_erase_target(block_id, active_ids):
    """Return True if block_id refers to an active block."""
    return block_id > 0 and block_id in active_ids


def process_operations(t, m):
    """Execute the memory-manager operation loop."""
    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        line = read_operation_line()
        if not line:
            continue

        parts = line.split()
        command = parts[0]

        if command == "alloc":
            n = parse_integer_argument(parts)
            found_pos = find_first_fit(memory, m, n)

            if found_pos != -1:
                write_output(next_id)
                active_ids.add(next_id)
                allocate_block(memory, found_pos, n, next_id)
                next_id += 1
            else:
                write_output("NULL")

        elif command == "erase":
            x = parse_integer_argument(parts)

            if is_valid_erase_target(x, active_ids):
                active_ids.remove(x)
                erase_block(memory, m, x)
            else:
                write_output("ILLEGAL_ERASE_ARGUMENT")

        elif command == "defragment":
            memory = defragment_memory(memory, m)


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    configuration = read_initial_configuration()
    if configuration is None:
        return

    t, m = configuration
    process_operations(t, m)


def main():
    """Program entry point."""
    memory_manager()


if __name__ == "__main__":
    main()
