import sys


def _read_initial_input():
    line = sys.stdin.readline()
    if not line:
        return None
    t, m = map(int, line.split())
    return t, m


def _find_free_block(memory, m, n):
    i = 0
    while i <= m - n:
        if memory[i] == 0:
            j = i
            while j < m and memory[j] == 0:
                j += 1

            if j - i >= n:
                return i
            i = j
        else:
            i += 1

    return -1


def _handle_alloc(memory, m, parts, next_id, active_ids):
    n = int(parts[1])
    found_pos = _find_free_block(memory, m, n)

    if found_pos == -1:
        print("NULL")
        return next_id

    print(next_id)
    active_ids.add(next_id)
    for k in range(found_pos, found_pos + n):
        memory[k] = next_id

    return next_id + 1


def _is_valid_erase_target(block_id, active_ids):
    return block_id > 0 and block_id in active_ids


def _free_block(memory, m, block_id):
    for i in range(m):
        if memory[i] == block_id:
            memory[i] = 0


def _handle_erase(memory, m, parts, active_ids):
    block_id = int(parts[1])

    if not _is_valid_erase_target(block_id, active_ids):
        print("ILLEGAL_ERASE_ARGUMENT")
        return

    active_ids.remove(block_id)
    _free_block(memory, m, block_id)


def _defragment_memory(memory, m):
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    try:
        initial_input = _read_initial_input()
    except (IOError, ValueError):
        return

    if initial_input is None:
        return

    t, m = initial_input
    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        line = sys.stdin.readline().strip()
        if not line:
            continue

        parts = line.split()
        command = parts[0]

        if command == "alloc":
            next_id = _handle_alloc(memory, m, parts, next_id, active_ids)
        elif command == "erase":
            _handle_erase(memory, m, parts, active_ids)
        elif command == "defragment":
            memory = _defragment_memory(memory, m)


if __name__ == "__main__":
    memory_manager()
