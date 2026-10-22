import sys


def read_memory_size_and_operation_count():
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
    except (IOError, ValueError):
        return None
    return t, m


def read_operations(t):
    for _ in range(t):
        yield sys.stdin.readline().strip()


def find_free_block(memory, m, n):
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


def erase_block(memory, m, block_id):
    for i in range(m):
        if memory[i] == block_id:
            memory[i] = 0


def defragment_memory(memory, m):
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def process_operations(operations, m):
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
            found_pos = find_free_block(memory, m, n)

            if found_pos != -1:
                yield next_id
                active_ids.add(next_id)
                for k in range(found_pos, found_pos + n):
                    memory[k] = next_id
                next_id += 1
            else:
                yield "NULL"

        elif command == "erase":
            x = int(parts[1])

            if x > 0 and x in active_ids:
                active_ids.remove(x)
                erase_block(memory, m, x)
            else:
                yield "ILLEGAL_ERASE_ARGUMENT"

        elif command == "defragment":
            memory = defragment_memory(memory, m)


def print_result(result):
    print(result)


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    configuration = read_memory_size_and_operation_count()
    if configuration is None:
        return

    t, m = configuration
    for result in process_operations(read_operations(t), m):
        print_result(result)


if __name__ == "__main__":
    memory_manager()
