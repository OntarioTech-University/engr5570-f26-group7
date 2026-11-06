import sys


def _read_configuration():
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
        return t, m
    except (IOError, ValueError):
        return None


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


def _print_result(value):
    print(value)


def _allocate(n, m, memory, next_id, active_ids):
    found_pos = _find_free_block(memory, m, n)
    if found_pos == -1:
        _print_result("NULL")
        return next_id

    _print_result(next_id)
    active_ids.add(next_id)
    for k in range(found_pos, found_pos + n):
        memory[k] = next_id
    return next_id + 1


def _erase(x, m, memory, active_ids):
    if x > 0 and x in active_ids:
        active_ids.remove(x)
        for i in range(m):
            if memory[i] == x:
                memory[i] = 0
    else:
        _print_result("ILLEGAL_ERASE_ARGUMENT")


def _defragment(memory, m):
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def _process_operation(line, m, memory, next_id, active_ids):
    parts = line.split()
    command = parts[0]
    if command == "alloc":
        n = int(parts[1])
        next_id = _allocate(n, m, memory, next_id, active_ids)
    elif command == "erase":
        x = int(parts[1])
        _erase(x, m, memory, active_ids)
    elif command == "defragment":
        memory = _defragment(memory, m)
    return memory, next_id


def _process_operations(t, m, memory, next_id, active_ids):
    for _ in range(t):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        memory, next_id = _process_operation(
            line, m, memory, next_id, active_ids
        )


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    configuration = _read_configuration()
    if configuration is None:
        return

    t, m = configuration
    memory = [0] * m
    next_id = 1
    active_ids = set()
    _process_operations(t, m, memory, next_id, active_ids)


if __name__ == "__main__":
    memory_manager()
